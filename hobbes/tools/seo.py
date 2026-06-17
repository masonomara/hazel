#!/usr/bin/env python3
"""
seo.py — scorecard Section E (SEO checklist + site-level) for the golden path,
machine-read from each page's HTML. Step two of the agent baseline (step one is psi.py).

Eight checks per page (BASELINE.md Group D), all parseable from HTML or a header:
  title · meta description · canonical · single H1 + heading order ·
  structured data (JSON-LD) · Open Graph/Twitter · image alt COVERAGE · indexable
Plus Section E: sitemap.xml + robots.txt load (once per site).

The ONE thing it can't own is alt-text QUALITY — it reports how many images
lack alt; a human judges whether the alt that exists is meaningful. Same
AI-vs-human split as the manual a11y pass.

No API key needed (plain HTML fetch). Mirrors psi.py: retry, per-page cache
(git-ignored *.seo.json), and a durable artifact at hobbes/tools/seo-results.md.

USAGE:
  python3 hobbes/tools/seo.py                 # default golden path
  python3 hobbes/tools/seo.py URL [URL ...]   # custom URLs
  python3 hobbes/tools/seo.py --fresh         # ignore cache, re-fetch
  python3 hobbes/tools/seo.py --out PATH      # write artifact elsewhere
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_URLS = [
    ("Home", "https://hazelboutique.com/"),
    ("Collection", "https://hazelboutique.com/collections/all-hazel-brand"),
    ("Product", "https://hazelboutique.com/products/the-capri-collection-baby-pink"),
]
CACHE_DIR = Path(__file__).resolve().parent  # *.seo.json here is git-ignored
MAX_CONCURRENCY = 4
OG_REQUIRED = ["og:title", "og:image", "og:url", "og:type"]
LD_KNOWN = {"Product", "BreadcrumbList", "Organization", "WebSite", "WebPage",
            "ItemList", "CollectionPage", "Article", "FAQPage"}


def cache_path(url):
    slug = "".join(c if c.isalnum() else "_" for c in url)[:80]
    return CACHE_DIR / f"{slug}.seo.json"


class Page(HTMLParser):
    """Pulls the SEO-relevant bits out of one page in a single pass."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.metas = {}          # name/property (lowercased) -> content
        self.canonical = None
        self.headings = []       # heading levels in document order
        self.h1 = 0
        self.imgs = 0
        self.imgs_no_alt = 0
        self.jsonld = []         # parsed JSON-LD objects (or {_err:True})
        self._in_ld = False
        self._ld = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.metas[key.lower()] = a.get("content", "") or ""
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            lvl = int(tag[1])
            self.headings.append(lvl)
            if lvl == 1:
                self.h1 += 1
        elif tag == "img":
            self.imgs += 1
            alt = a.get("alt")
            if alt is None or not alt.strip():
                self.imgs_no_alt += 1
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_ld, self._ld = True, []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            try:
                self.jsonld.append(json.loads("".join(self._ld).strip()))
            except Exception:
                self.jsonld.append({"_err": True})

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld.append(data)


def fetch(url, fresh, tries=4, timeout=30):
    """Returns {html, xrobots, final_url} or None. 4xx → page issue, no retry."""
    cf = cache_path(url)
    if not fresh and cf.exists():
        print(f"  ⤿ cached {url}", file=sys.stderr, flush=True)
        return json.loads(cf.read_text())
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (HobbesSEO)"})
    last = None
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                charset = r.headers.get_content_charset() or "utf-8"
                data = {
                    "html": r.read().decode(charset, "replace"),
                    "xrobots": r.headers.get("X-Robots-Tag", "") or "",
                    "final_url": r.geturl(),
                }
            cf.write_text(json.dumps(data))
            print(f"  ✓ {url}", file=sys.stderr, flush=True)
            return data
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500:
                print(f"  ✗ {url}: HTTP {e.code}", file=sys.stderr, flush=True)
                return None
            last = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
        print(f"  retry {attempt}/{tries} ({url}): {last}", file=sys.stderr, flush=True)
    print(f"  ✗ GAVE UP {url}: {last}", file=sys.stderr, flush=True)
    return None


def head_ok(levels):
    """No skipped level going deeper (h2 -> h4 fails); going back up is fine."""
    prev = 0
    for lvl in levels:
        if prev and lvl > prev + 1:
            return False
        prev = lvl
    return True


def ld_types(objs):
    types, err = [], False
    for o in objs:
        if not isinstance(o, dict):
            continue
        if o.get("_err"):
            err = True
            continue
        graph = o.get("@graph")
        for it in (graph if isinstance(graph, list) else [o]):
            t = it.get("@type") if isinstance(it, dict) else None
            if t:
                types += t if isinstance(t, list) else [t]
    return types, err


def norm(u):
    p = urllib.parse.urlparse(u)
    return p.netloc.lower() + p.path.rstrip("/")


def analyze(url, data, dup_titles):
    """Turn one page's parsed data into a compact pass/fail cell per check."""
    p = Page()
    p.feed(data["html"])
    title = " ".join(p.title.split())
    m = p.metas

    if not title:
        t_cell = "✗ empty"
    elif title in dup_titles:
        t_cell = "✗ duplicate"
    else:
        t_cell = "✓"

    desc = m.get("description", "").strip()
    d_cell = "✓" if desc else "✗ missing"

    c_cell = "✓" if p.canonical and norm(p.canonical) == norm(data["final_url"]) else (
        "✗ missing" if not p.canonical else "✗ not self")

    h_cell = "✓" if (p.h1 == 1 and head_ok(p.headings)) else (
        f"✗ {p.h1} h1" if p.h1 != 1 else "✗ skips level")

    types, err = ld_types(p.jsonld)
    good = [t for t in types if t in LD_KNOWN]
    sd_cell = ("✗ parse error" if err else
               (f"✓ {','.join(dict.fromkeys(good))}" if good else
                ("✗ none" if not types else f"⚠ {','.join(dict.fromkeys(types))}")))

    missing_og = [r.replace("og:", "") for r in OG_REQUIRED if not m.get(r)]
    og_cell = "✓" if not missing_og else "✗ no " + ",".join(missing_og)

    if p.imgs == 0:
        alt_cell = "no imgs"
    elif p.imgs_no_alt == 0:
        alt_cell = f"✓ 0/{p.imgs} (quality: human)"
    else:
        alt_cell = f"⚠ {p.imgs_no_alt}/{p.imgs} missing (quality: human)"

    noindex = "noindex" in m.get("robots", "").lower() or "noindex" in data["xrobots"].lower()
    i_cell = "✗ noindex" if noindex else "✓"

    return {
        "Unique, descriptive title": t_cell,
        "Meta description present": d_cell,
        "Canonical correct": c_cell,
        "Single H1 + ordered headings": h_cell,
        "Valid structured data": sd_cell,
        "Open Graph / Twitter tags": og_cell,
        "All images have meaningful alt": alt_cell,
        "Indexable (robots OK)": i_cell,
        "_title": title or "(none)",
    }


def site_file(root, path):
    try:
        req = urllib.request.Request(root + path, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return "x" if r.status == 200 else f"✗ HTTP {r.status}"
    except Exception as e:
        return f"✗ {type(e).__name__}"


def main():
    args = sys.argv[1:]
    fresh = "--fresh" in args
    out = Path(__file__).resolve().parent / "seo-results.md"
    if "--out" in args:
        i = args.index("--out")
        out = Path(args[i + 1])
        del args[i:i + 2]
    positional = [a for a in args if a != "--fresh"]
    urls = [(f"URL{i+1}", u) for i, u in enumerate(positional)] or DEFAULT_URLS

    with ThreadPoolExecutor(max_workers=min(MAX_CONCURRENCY, len(urls))) as ex:
        pages = list(ex.map(lambda lu: (lu, fetch(lu[1], fresh)), urls))

    # Duplicate-title detection needs every title first.
    titles = []
    for (label, url), data in pages:
        if data:
            titles.append(" ".join(_quick_title(data["html"]).split()))
    dup = {t for t in titles if titles.count(t) > 1 and t}

    results = {}
    for (label, url), data in pages:
        results[label] = analyze(url, data, dup) if data else None

    labels = [lbl for lbl, _ in urls]
    rows = ["Unique, descriptive title", "Meta description present", "Canonical correct",
            "Single H1 + ordered headings", "Valid structured data",
            "Open Graph / Twitter tags", "All images have meaningful alt",
            "Indexable (robots OK)"]

    def cell(lbl, check):
        r = results.get(lbl)
        return r[check] if r else "— (fetch failed)"

    root = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(urls[0][1]))
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# SEO results — {stamp}",
        "",
        "Captured by `hobbes/tools/seo.py` — scorecard Section E. Every cell is parsed",
        "from page HTML/headers. Alt-text shows COVERAGE only — a human judges",
        "whether the alt that exists is meaningful.",
        "",
        "Golden path: " + " · ".join(f"[{lbl}]({u})" for lbl, u in urls),
        "",
        "## E. SEO checklist",
        "",
        "| Item | " + " | ".join(labels) + " |",
        "|" + "---|" * (len(labels) + 1),
        *[f"| {chk} | " + " | ".join(cell(lbl, chk) for lbl in labels) + " |" for chk in rows],
        "",
        "| Site-level (once per site) | Present |",
        "|---|---|",
        f"| `sitemap.xml` | {site_file(root, '/sitemap.xml')} |",
        f"| `robots.txt` | {site_file(root, '/robots.txt')} |",
        "",
        "## Page titles (read them — is any brand-only or generic?)",
        "",
        *[f"- **{lbl}:** {results[lbl]['_title']}" if results.get(lbl) else f"- **{lbl}:** —"
          for lbl in labels],
    ]
    failed = [lbl for lbl in labels if results.get(lbl) is None]
    if failed:
        L += ["", "> ✗ Fetch failed (cells show —): " + ", ".join(failed)]
    report = "\n".join(L) + "\n"

    print(report)
    out.write_text(report)
    print(f"→ written to {out}", file=sys.stderr)


def _quick_title(html):
    p = Page()
    p.feed(html)
    return p.title


if __name__ == "__main__":
    main()
