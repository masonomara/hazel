#!/usr/bin/env python3
"""
crawl.py — whole-site SiteOne crawl. Summary counts feed scorecard Section E
(site-level); the per-URL detail feeds the findings doc.

Covers what the golden-path tools can't: every URL on the site. Reports broken
links, redirects, missing titles, duplicate titles, missing meta descriptions,
and missing H1s — site-wide.

Mirrors psi.py / seo.py: gentle live crawl, a cached crawl.json (reused on
--resume / re-crawled on --fresh), and a durable hobbes/tools/crawl-results.md.

USAGE:
  python3 hobbes/tools/crawl.py            # reuse cached crawl.json if present
  python3 hobbes/tools/crawl.py --fresh    # re-crawl the site
  python3 hobbes/tools/crawl.py --out PATH # write artifact elsewhere
"""

import json
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from psi import DEFAULT_URLS  # single source of truth for the site

BIN = "siteone-crawler"
CACHE = TOOLS / "crawl.json"
LIMITS = ["--max-reqs-per-sec=5", "--workers=3", "--timeout=10", "--max-visited-urls=2000"]


def site_root():
    p = urllib.parse.urlparse(DEFAULT_URLS[0][1])
    return f"{p.scheme}://{p.netloc}/"


def run_crawl(fresh):
    if not fresh and CACHE.exists():
        print(f"  ⤿ cached crawl ({CACHE.name})", file=sys.stderr, flush=True)
        return json.loads(CACHE.read_text())
    if not shutil.which(BIN):
        sys.exit(f"✗ {BIN} not found — install: brew install janreges/tap/siteone-crawler")
    root = site_root()
    print(f"… crawling {root} (gentle: 5 req/s, 3 workers, ≤2000 urls)", file=sys.stderr, flush=True)
    cmd = [BIN, f"--url={root}", "--output=json", f"--output-json-file={CACHE}",
           "--hide-progress-bar", "--no-color"] + LIMITS
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL)
    if r.returncode != 0 or not CACHE.exists():
        sys.exit(f"✗ crawl failed (exit {r.returncode}).")
    print("  ✓ crawl complete", file=sys.stderr, flush=True)
    return json.loads(CACHE.read_text())


def table_rows(tables, name):
    return (tables.get(name) or {}).get("rows") or []


def main():
    args = sys.argv[1:]
    fresh = "--fresh" in args
    out = TOOLS / "crawl-results.md"
    if "--out" in args:
        out = Path(args[args.index("--out") + 1])

    data = run_crawl(fresh)
    tables = data.get("tables", {})

    broken = table_rows(tables, "404")
    redirects = table_rows(tables, "redirects")
    seo = table_rows(tables, "seo")
    missing_title = [r for r in seo if not (r.get("title") or "").strip()]
    missing_desc = [r for r in seo if not (r.get("description") or "").strip()]
    missing_h1 = [r for r in seo if not (r.get("h1") or "").strip()]
    dup_title = [r for r in table_rows(tables, "non-unique-titles") if (r.get("title") or "").strip()]
    dup_desc = [r for r in table_rows(tables, "non-unique-descriptions") if (r.get("description") or "").strip()]

    def path(r):
        return r.get("urlPathAndQuery") or "/"

    def detail(items, render):
        return [f"- {render(r)}" for r in items] or ["- (none)"]

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# Crawl results — {stamp}",
        "",
        "Captured by `hobbes/tools/crawl.py` (SiteOne, gentle whole-site crawl). The",
        "count table feeds scorecard **Section E**; the detail feeds **findings**.",
        "",
        f"Site: {site_root()} · HTML pages analysed: {len(seo)}",
        "",
        "## Site-wide (crawl) — Section E counts",
        "",
        "| Site-wide (crawl) | Count |",
        "|---|---|",
        f"| Broken links (4xx/5xx) | {len(broken)} |",
        f"| Redirects | {len(redirects)} |",
        f"| Missing titles | {len(missing_title)} |",
        f"| Duplicate titles | {len(dup_title)} |",
        f"| Missing meta descriptions | {len(missing_desc)} |",
        f"| Missing H1 | {len(missing_h1)} |",
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
        "",
        "### Missing H1",
        *detail(missing_h1, path),
    ]
    report = "\n".join(L) + "\n"
    print(report)
    out.write_text(report)
    print(f"→ written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
