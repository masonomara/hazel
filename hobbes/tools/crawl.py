#!/usr/bin/env python3
"""
crawl.py — whole-site SiteOne crawl. Emits scorecard Section F (site-wide
grades + counts); the per-URL detail feeds the findings doc.

Covers what the golden-path tools can't: every URL on the site. Section F holds
SiteOne's 0–10 quality grades plus site-wide counts — broken links, redirects,
missing/duplicate titles, missing meta descriptions, multiple/skipped headings,
missing alt/aria/roles/lang, invalid/duplicate SVGs, and the security headers.

Mirrors psi.py / seo.py: gentle live crawl, a cached crawl.json (reused on
--resume / re-crawled on --fresh), and a durable crawl-results.md in the cycle folder.

USAGE:
  python3 hobbes/tools/crawl.py            # reuse cached crawl.json if present
  python3 hobbes/tools/crawl.py --fresh    # re-crawl the site
  python3 hobbes/tools/crawl.py --out PATH # write digest elsewhere
  python3 hobbes/tools/crawl.py --run-dir DIR # cycle folder (raw/crawl.json + crawl.html + digest)
"""

import json
import re
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from psi import DEFAULT_URLS  # single source of truth for the site

BIN = "siteone-crawler"
LIMITS = ["--max-reqs-per-sec=5", "--workers=3", "--timeout=10", "--max-visited-urls=2000"]


def resolve_run_dir(args):
    """Per-cycle output folder: hobbes/scorecards/<date>/. crawl.json lives in
    raw/, the human-readable crawl.html and digest sit at the top. baseline.py
    passes --run-dir so psi/seo/crawl share one cycle folder; standalone defaults
    to today's."""
    if "--run-dir" in args:
        d = Path(args[args.index("--run-dir") + 1])
    else:
        d = HOBBES / "scorecards" / datetime.now().strftime("%Y-%m-%d")
    (d / "raw").mkdir(parents=True, exist_ok=True)
    return d


def site_root():
    p = urllib.parse.urlparse(DEFAULT_URLS[0][1])
    return f"{p.scheme}://{p.netloc}/"


def run_crawl(fresh, cache, html_out):
    if not fresh and cache.exists():
        print(f"  ⤿ cached crawl ({cache.name})", file=sys.stderr, flush=True)
        return json.loads(cache.read_text())
    if not shutil.which(BIN):
        sys.exit(f"✗ {BIN} not found — install: brew install janreges/tap/siteone-crawler")
    root = site_root()
    print(f"… crawling {root} (gentle: 5 req/s, 3 workers, ≤2000 urls)", file=sys.stderr, flush=True)
    # JSON → raw/ (the machine source); the full SiteOne HTML report → crawl.html
    # (the robust human view, kept in the cycle folder, not dumped in tmp/). The
    # default tmp/ text dump is disabled.
    cmd = [BIN, f"--url={root}", "--output=json", f"--output-json-file={cache}",
           f"--output-html-report={html_out}", "--output-text-file=",
           "--hide-progress-bar", "--no-color"] + LIMITS
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL)
    if r.returncode != 0 or not cache.exists():
        sys.exit(f"✗ crawl failed (exit {r.returncode}).")
    print(f"  ✓ crawl complete · report → {html_out.name}", file=sys.stderr, flush=True)
    return json.loads(cache.read_text())


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


def main():
    args = sys.argv[1:]
    fresh = "--fresh" in args
    rd = resolve_run_dir(args)
    cache = rd / "raw" / "crawl.json"
    html_out = rd / "crawl.html"
    out = rd / "crawl-results.md"
    if "--out" in args:
        out = Path(args[args.index("--out") + 1])

    data = run_crawl(fresh, cache, html_out)
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

    def path(r):
        return r.get("urlPathAndQuery") or "/"

    def detail(items, render):
        return [f"- {render(r)}" for r in items] or ["- (none)"]

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# Crawl results — {stamp}",
        "",
        "Captured by `hobbes/tools/crawl.py` (SiteOne, gentle whole-site crawl).",
        "The Section F block below feeds the scorecard; the detail feeds **findings**.",
        "",
        f"Site: {site_root()} · HTML pages analysed: {n}",
        "",
        f"## F. Site-wide (whole-site crawl — {n} pages)",
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
    print(report)
    out.write_text(report)
    print(f"→ written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
