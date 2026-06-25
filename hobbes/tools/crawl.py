#!/usr/bin/env python3
"""
crawl.py — whole-site SiteOne crawl. Emits scorecard Section F (site-wide
grades + counts); the per-URL detail feeds the findings doc.

Covers what the golden-path tools can't: every URL on the site. Section F holds
SiteOne's 0–10 quality grades plus site-wide counts — broken links, redirects,
missing/duplicate titles, missing meta descriptions, multiple/skipped headings,
missing alt/aria/roles/lang, invalid/duplicate SVGs, and the security headers.

DRIVEN BY THE SITEMAP, for a reproducible page set. Earlier cycles seeded a
link-discovery crawl from the homepage with a hard URL cap; the sample wandered
(200→164 pages) because the host throttled a different random subset each run and
the cap truncated the rest — so cycle-over-cycle counts were noise. Now we expand
the sitemap to the authoritative page list (SiteOne does NOT recurse a nested
sitemap *index*, so we expand it here), serve it as one flat sitemap on localhost,
and crawl exactly that set: pinned with --include-regex, gentle pace so 429s stay
near zero, no truncation. Same sitemap → same pages → comparable numbers.

Mirrors psi.py / seo.py: gentle live crawl, a cached crawl.json, and the same
capture/render split — capture() crawls into raw/crawl.json; scorecard_section()
renders §F straight from that JSON. main() does both; baseline.py calls the same
two, so the digest and a standalone run share one renderer.

USAGE:
  python3 hobbes/tools/crawl.py            # reuse cached crawl.json if present
  python3 hobbes/tools/crawl.py --fresh    # re-crawl (stratified sitemap sample)
  python3 hobbes/tools/crawl.py --full     # crawl the entire sitemap (slow — occasional audit)
  python3 hobbes/tools/crawl.py --out PATH # also write the digest to PATH
  python3 hobbes/tools/crawl.py --run-dir DIR # cycle folder (raw/crawl.json)
"""

import html
import http.server
import json
import re
import shutil
import socketserver
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import config
from psi import DEFAULT_URLS  # single source of truth for the site

BIN = "siteone-crawler"
UA = "hobbes-baseline/1.0 (+SiteOne sitemap crawl)"
# Pace: hosts often rate-limit site HTML hard (a leaky bucket — a burst of ~33
# pages then 429 for the rest), and SiteOne has no 429 retry, so a throttled page
# is a lost page and the sample wanders again. We stay UNDER the limit: 1 req/s,
# 1 worker, serialized. Images are skipped — alt/heading/SEO/security are HTML/
# header checks that don't need the bytes (and pulling hundreds of images would
# both crawl for hours and, ironically, was the only thing diluting the origin
# hit-rate; we replace that dilution with a low rate instead). Image weight/format
# is judged on the golden path by PSI.
LIMITS = ["--max-reqs-per-sec=1", "--workers=1", "--timeout=15",
          "--disable-images", "--regex-filtering-only-for-pages"]

# Default crawl is a STRATIFIED SAMPLE, not the whole sitemap: every distinct
# low-volume page type every cycle, plus a fixed deterministic slice of the one
# high-volume type (named by [cycle].sample_path, e.g. "/products/"). That type is
# template-driven, so a slice reveals the same template-level issues (missing
# description, heading order, missing alt) as the whole would — without hammering
# the host past its throttle. With no sample_path set, every page is crawled.
# --full overrides this and crawls the entire sitemap (slow; for an occasional
# complete audit). The sample is deterministic, so the page set — and the counts —
# are identical every cycle.
SAMPLE_SIZE = 100   # how many of the high-volume page type to keep when subsampling


def select_pages(pages, full):
    """Choose the crawl set from the full sitemap. Returns (chosen, note).
    Subsamples the one high-volume page type named by [cycle].sample_path; with no
    sample_path set (or --full), takes every page."""
    pat = config.sample_path()
    if full or not pat:
        return pages, "full sitemap" if full else "all pages (no sample_path set)"
    bucket = [p for p in pages if pat in p]
    other = [p for p in pages if pat not in p]
    if len(bucket) > SAMPLE_SIZE:
        step = len(bucket) // SAMPLE_SIZE           # deterministic: every Nth, sorted
        sample = bucket[::step][:SAMPLE_SIZE]
    else:
        sample = bucket
    chosen = sorted(set(other) | set(sample))
    note = f"all {len(other)} other + {len(sample)}/{len(bucket)} '{pat}' sampled"
    return chosen, note


def resolve_run_dir(args):
    """Per-cycle output folder: hobbes/cycle/<date>-<letter>/. crawl.json lives in
    raw/. baseline.py passes --run-dir so psi/seo/crawl share one cycle folder;
    standalone attaches to the latest cycle (or a fresh one)."""
    if "--run-dir" in args:
        d = Path(args[args.index("--run-dir") + 1])
    else:
        d = config.default_run_dir(HOBBES / "cycle")
    (d / "raw").mkdir(parents=True, exist_ok=True)
    return d


def site_root():
    p = urllib.parse.urlparse(DEFAULT_URLS[0][1])
    return f"{p.scheme}://{p.netloc}/"


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def _locs(xml):
    return [html.unescape(m.strip()) for m in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]


def _is_page(url):
    """A crawlable HTML page — a clean path with no file extension. Page URLs are
    extensionless paths; this drops child sitemaps (.xml) and non-HTML sitemap
    entries like /agents.md or /robots.txt."""
    last = urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    return "." not in last


def expand_sitemap(root):
    """The authoritative page list. SiteOne crawls a *flat* sitemap but does NOT
    recurse a sitemap *index* (many hosts serve `sitemap.xml` as an index of
    child sitemaps), so we expand it here: fetch the index, follow each child,
    collect every non-sitemap <loc>. Returns (sorted unique pages, note)."""
    idx = _fetch(root + "sitemap.xml")
    top = _locs(idx)
    pages, notes = [], []
    if "<sitemapindex" in idx:
        for child in top:
            if child.lower().rstrip("/").split("?")[0].endswith(".xml") or "sitemap" in child.lower():
                try:
                    pages += [u for u in _locs(_fetch(child)) if _is_page(u)]
                except Exception as e:
                    notes.append(f"child sitemap failed ({child.split('/')[-1].split('?')[0]}): {e}")
            elif _is_page(child):
                pages.append(child)
    else:                                   # already a flat sitemap
        pages = [u for u in top if _is_page(u)]
    return sorted(set(pages)), notes


def serve_flat_sitemap(pages):
    """Serve the expanded page list as one flat sitemap on an ephemeral localhost
    port. SiteOne is seeded here, then crawls the real (external) page URLs via
    --allowed-domain-for-crawling. Returns (httpd, seed_url); caller shuts it down."""
    body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"<url><loc>{html.escape(u)}</loc></url>\n" for u in pages)
            + "</urlset>\n").encode("utf-8")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/sitemap.xml"


def pin_regex(pages):
    """A PCRE that matches exactly the sitemap pages (optional trailing slash).
    With --regex-filtering-only-for-pages this pins crawled *pages* to the sitemap
    set — no link-discovery wander — while assets still load for analysis."""
    return "^(" + "|".join(re.escape(u) for u in pages) + ")/?$"


def run_crawl(fresh, cache, full=False):
    if not fresh and cache.exists():
        print(f"  ⤿ cached crawl ({cache.name})", file=sys.stderr, flush=True)
        return json.loads(cache.read_text())
    if not shutil.which(BIN):
        sys.exit(f"✗ {BIN} not found — install: brew install janreges/tap/siteone-crawler")
    root = site_root()
    host = urllib.parse.urlparse(root).netloc

    print(f"… expanding sitemap for {root}", file=sys.stderr, flush=True)
    try:
        sitemap, notes = expand_sitemap(root)
    except Exception as e:
        sys.exit(f"✗ could not read sitemap ({e}). The crawl is sitemap-driven; "
                 f"confirm {root}sitemap.xml is reachable.")
    for n in notes:
        print(f"  ⚠ {n}", file=sys.stderr, flush=True)
    if not sitemap:
        sys.exit("✗ sitemap expanded to 0 pages — nothing to crawl.")
    pages, sample_note = select_pages(sitemap, full)
    print(f"  ✓ {len(sitemap)} pages in sitemap → crawling {len(pages)} ({sample_note})",
          file=sys.stderr, flush=True)

    httpd, seed = serve_flat_sitemap(pages)
    print(f"… crawling {len(pages)} pages (1 req/s, 1 worker, images off) — be patient",
          file=sys.stderr, flush=True)
    # JSON → raw/ is the only durable output: it's the machine source evaluation.py
    # reads, and scorecard_section() renders §F from it. The SiteOne HTML report
    # (~1 MB/cycle, regenerable, read by nobody in the pipeline) is deliberately
    # NOT emitted; the default tmp/ text dump is off too. Seed from the localhost
    # flat sitemap; pin pages to the chosen set; allow crawling/asset-loading on
    # the real domain.
    cmd = [BIN, f"--url={seed}",
           f"--allowed-domain-for-crawling={host}",
           "--allowed-domain-for-external-files=*",
           f"--include-regex={pin_regex(pages)}",
           f"--max-visited-urls={len(pages) * 2 + 1000}",
           "--output=json", f"--output-json-file={cache}",
           "--output-text-file=",
           "--hide-progress-bar", "--no-color"] + LIMITS
    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL)
    finally:
        httpd.shutdown()
    if r.returncode != 0 or not cache.exists():
        sys.exit(f"✗ crawl failed (exit {r.returncode}).")
    data = json.loads(cache.read_text())
    data["_sitemapPages"] = len(sitemap)     # carried into coverage reporting
    data["_sampledPages"] = len(pages)
    data["_sampleNote"] = sample_note
    data["_full"] = full                     # so scorecard_section() can label §F from raw/
    cache.write_text(json.dumps(data))
    print(f"  ✓ crawl complete · {cache.name}", file=sys.stderr, flush=True)
    return data


def capture(raw, fresh, full):
    """Crawl the whole site into raw/crawl.json (or reuse the cache). Network
    side-effects only; §F is rendered from the JSON by scorecard_section(), so
    baseline.py captures once then renders the same way crawl.py does standalone."""
    return run_crawl(fresh, raw / "crawl.json", full)


def table_rows(tables, name):
    return (tables.get(name) or {}).get("rows") or []


def quality_scores(data):
    """SiteOne's weighted 0–10 grades, keyed by category name."""
    cats = ((data.get("qualityScores") or {}).get("categories")) or []
    return {c.get("name"): c.get("score") for c in cats}


def rollup_texts(data):
    """Every headline line SiteOne computed — summary items + quality-score
    deduction reasons. Page-level counts ('52 page(s) with …') live ONLY here,
    not in the per-URL tables, so the scorecard reads them from this rollup."""
    texts = [i.get("text", "") for i in ((data.get("summary") or {}).get("items") or [])]
    for c in ((data.get("qualityScores") or {}).get("categories")) or []:
        for d in (c.get("deductions") or []):
            texts.append(d.get("reason", ""))
    return texts


def count_for(texts, needle):
    """First integer in the first rollup line that mentions `needle` (case-
    insensitive), else 0 — e.g. count_for(t, 'skipped heading') -> 52."""
    nl = needle.lower()
    for t in texts:
        if nl in t.lower():
            m = re.search(r"\d+", t)
            if m:
                return int(m.group())
    return 0


def header_set(tables, name):
    """A security header counts as 'set' only if the crawl flagged no critical/
    warning responses for it; if it's absent from the table, nothing flagged it."""
    for r in table_rows(tables, "security"):
        if (r.get("header") or "").lower() == name.lower():
            return int(r.get("critical") or 0) == 0 and int(r.get("warning") or 0) == 0
    return True


def coverage_line(data, html_pages):
    """One honest line on what the crawl actually reached, so a partial run can't
    pass for the whole site. The default crawl SAMPLES the sitemap, so a gap below
    the full count is intentional — but analysing fewer pages than we *chose* to
    crawl, or any 429, is a real shortfall and is flagged."""
    sm = data.get("_sitemapPages")
    sampled = data.get("_sampledPages") or sm
    note = data.get("_sampleNote")
    stats = data.get("stats", {}) or {}
    cbs = {str(k): int(v) for k, v in (stats.get("countByStatus") or {}).items()}
    throttled = cbs.get("429", 0)
    parts = [f"{html_pages} HTML pages analysed"]
    if sampled and sm and sampled < sm:
        parts.append(f"of {sampled} sampled ({note}) — sitemap has {sm}")
    elif sm:
        parts.append(f"of {sm} in sitemap (full)")
    shortfall = sampled and html_pages < sampled
    if shortfall:
        parts.append(f"⚠ {sampled - html_pages} chosen page(s) NOT reached")
    if throttled:
        parts.append(f"⚠ {throttled} request(s) throttled (429)")
    non2xx = sorted(c for c in cbs if not c.startswith("2"))
    if non2xx:
        parts.append("responses: " + ", ".join(f"{c}×{cbs[c]}" for c in non2xx))
    return " · ".join(parts), (throttled > 0 or shortfall)


def scorecard_section(raw):
    """Scorecard Section F (site-wide grades + counts), rendered from
    raw/crawl.json — the exact block baseline.py drops into the digest and crawl.py
    prints under its standalone header — one renderer, two callers."""
    data = json.loads((raw / "crawl.json").read_text())
    full = bool(data.get("_full"))
    tables = data.get("tables", {})
    qs = quality_scores(data)
    texts = rollup_texts(data)

    seo = table_rows(tables, "seo")
    n = len(seo)
    broken = table_rows(tables, "404")
    redirects = table_rows(tables, "redirects")
    missing_title = [r for r in seo if not (r.get("title") or "").strip()]
    missing_desc = [r for r in seo if not (r.get("description") or "").strip()]
    dup_title = [r for r in table_rows(tables, "non-unique-titles") if (r.get("title") or "").strip()]

    # Page-level counts — SiteOne's own rollup (not derivable from the per-URL tables).
    multi_h1 = count_for(texts, "multiple <h1>")
    skipped_h = count_for(texts, "skipped heading")
    no_alt = count_for(texts, "without image alt")
    no_aria = count_for(texts, "without aria")
    no_roles = count_for(texts, "without role")
    no_lang = count_for(texts, "missing html lang") or count_for(texts, "without html lang")
    invalid_svg = count_for(texts, "invalid inline svg")
    dup_svg = count_for(texts, "duplicated inline svg")
    phone = count_for(texts, "non-clickable")
    no_brotli = count_for(texts, "brotli")
    invalid_html = count_for(texts, "invalid html")
    tls_ok = any("certificate is valid" in t.lower() for t in texts) or site_root().startswith("https")

    def p(ok):
        return "✓" if ok else "✗"

    def qsv(name):
        s = qs.get(name)
        return f"{s:.1f}" if isinstance(s, (int, float)) else "—"

    L = [
        f"## F. Site-wide ({'whole-site' if full else 'sitemap sample'} crawl — {n} pages)",
        "",
        "| SiteOne quality score (0–10) | Value |",
        "|---|---|",
        f"| Performance | {qsv('Performance')} |",
        f"| SEO | {qsv('SEO')} |",
        f"| Security | {qsv('Security')} |",
        f"| Accessibility | {qsv('Accessibility')} |",
        f"| Best practices | {qsv('Best Practices')} |",
        "",
        "| SEO / structure | Count | Pass |",
        "|---|---|---|",
        f"| Broken links (4xx) | {len(broken)} | {p(len(broken) == 0)} |",
        f"| Redirects | {len(redirects)} | {p(len(redirects) == 0)} |",
        f"| Missing titles | {len(missing_title)} | {p(len(missing_title) == 0)} |",
        f"| Duplicate titles | {len(dup_title)} | {p(len(dup_title) == 0)} |",
        f"| Missing meta descriptions | {len(missing_desc)} | {p(len(missing_desc) == 0)} |",
        f"| Pages with multiple H1 | {multi_h1} | {p(multi_h1 == 0)} |",
        f"| Pages with skipped heading levels | {skipped_h} | {p(skipped_h == 0)} |",
        "",
        "| Accessibility | Count | Pass |",
        "|---|---|---|",
        f"| Pages missing image alt | {no_alt} | {p(no_alt == 0)} |",
        f"| Pages missing aria-labels | {no_aria} | {p(no_aria == 0)} |",
        f"| Pages missing roles | {no_roles} | {p(no_roles == 0)} |",
        f"| Pages missing html lang | {no_lang} | {p(no_lang == 0)} |",
        "",
        "| Best practices | Count | Pass |",
        "|---|---|---|",
        f"| Pages with invalid inline SVG | {invalid_svg} | {p(invalid_svg == 0)} |",
        f"| Pages with duplicate inline SVG | {dup_svg} | {p(dup_svg == 0)} |",
        f"| Pages with non-clickable phone numbers | {phone} | {p(phone == 0)} |",
        f"| Valid HTML | {n - invalid_html} | {p(invalid_html == 0)} |",
        "",
        "| Security | Pass |",
        "|---|---|",
        f"| HSTS header | {p(header_set(tables, 'Strict-Transport-Security'))} |",
        f"| Content-Security-Policy | {p(header_set(tables, 'Content-Security-Policy'))} |",
        f"| Referrer-Policy | {p(header_set(tables, 'Referrer-Policy'))} |",
        f"| Permissions-Policy | {p(header_set(tables, 'Permissions-Policy'))} |",
        f"| Brotli compression | {p(no_brotli == 0)} |",
        f"| HTTPS / valid TLS cert | {p(tls_ok)} |",
    ]
    return "\n".join(L).rstrip()


def main():
    args = sys.argv[1:]
    fresh = "--fresh" in args
    full = "--full" in args
    rd = resolve_run_dir(args)
    raw = rd / "raw"
    out = None                                    # no default file: --out opts in
    if "--out" in args:
        out = Path(args[args.index("--out") + 1])

    data = capture(raw, fresh, full)
    tables = data.get("tables", {})
    seo = table_rows(tables, "seo")
    n = len(seo)
    broken = table_rows(tables, "404")
    redirects = table_rows(tables, "redirects")
    missing_title = [r for r in seo if not (r.get("title") or "").strip()]
    missing_desc = [r for r in seo if not (r.get("description") or "").strip()]
    dup_title = [r for r in table_rows(tables, "non-unique-titles") if (r.get("title") or "").strip()]

    def path(r):
        return r.get("urlPathAndQuery") or "/"

    def detail(items, render):
        return [f"- {render(r)}" for r in items] or ["- (none)"]

    cov, partial = coverage_line(data, n)
    if partial:
        print(f"  ⚠ coverage: {cov}", file=sys.stderr, flush=True)
    stamp = config.stamp()
    L = [
        f"# Crawl results — {stamp}",
        "",
        "Captured by `hobbes/tools/crawl.py` (SiteOne, sitemap-driven whole-site crawl).",
        "The Section F block below feeds the scorecard; the detail feeds **findings**.",
        "",
        f"Site: {site_root()}",
        f"**Coverage:** {cov}",
        "",
        scorecard_section(raw),
        "",
        "## Detail — for findings",
        "",
        "### Broken links (4xx/5xx)",
        *detail(broken, lambda r: f"{r.get('url')} ({r.get('statusCode')})"),
        "",
        "### Redirects",
        *detail(redirects, lambda r: f"{r.get('url')} → {r.get('targetUrl')} ({r.get('statusCode')})"),
        "",
        "### Missing titles",
        *detail(missing_title, path),
        "",
        "### Duplicate titles",
        *detail(dup_title, lambda r: f"\"{r.get('title')}\" ×{r.get('count')}"),
        "",
        "### Missing meta descriptions",
        *detail(missing_desc, path),
    ]
    report = "\n".join(L) + "\n"
    print(report)                                 # stdout — human-readable standalone digest
    if out:                                        # --out only; no default per-tool file
        out.write_text(report)
        print(f"→ written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
