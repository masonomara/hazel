#!/usr/bin/env python3
"""
psi.py — fetch PageSpeed Insights scores for the golden path and print
scorecard-ready markdown. Hobbes runs this; the human signs the manual rows.

WHY THIS EXISTS: run-1 numbers were transcribed by hand and field data got
mixed into lab rows (see hobbes-baseline.md 2.3/2.4/2.8). This pulls lab and
field SEPARATELY from the PSI API and labels them, so the mix can't happen.

KEY: read from $PSI_API_KEY, else from hobbes/.psi-key (git-ignored).
USAGE:
  python3 hobbes/tools/psi.py                 # default golden path
  python3 hobbes/tools/psi.py URL [URL ...]   # custom URLs
  python3 hobbes/tools/psi.py --fresh         # ignore cache, re-fetch all
  python3 hobbes/tools/psi.py --out PATH      # write artifact elsewhere
Prints the scorecard tables AND writes them to hobbes/tools/psi-results.md
(the durable artifact). The keyless PSI API is rate-capped to a shared pool
that is usually exhausted (HTTP 429) — a key is required, not optional.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

# Golden path — keep in sync with the locked URLs in the scorecard.
DEFAULT_URLS = [
    ("Home", "https://hazelboutique.com/"),
    ("Collection", "https://hazelboutique.com/collections/all-hazel-brand"),
    ("Product", "https://hazelboutique.com/products/the-capri-collection-baby-pink"),
]
ENDPOINT = "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]
# PSI runs Lighthouse server-side; a heavy mobile page takes ~60s. Firing all
# calls at once makes Google QUEUE them, so each call's wall-clock becomes
# queue-wait + run-time and blows the timeout — that was the real stall. Cap
# concurrency low so calls actually run when sent, not after a queue.
MAX_CONCURRENCY = 3
CACHE_DIR = Path(__file__).resolve().parent  # *.psi.json here is git-ignored


def cache_path(url, strategy):
    slug = "".join(c if c.isalnum() else "_" for c in url)[:80]
    return CACHE_DIR / f"{slug}-{strategy}.psi.json"


def load_key():
    key = os.environ.get("PSI_API_KEY", "").strip()
    if key:
        return key
    key_file = Path(__file__).resolve().parent.parent / ".psi-key"
    if key_file.exists():
        raw = key_file.read_text().strip()
        # tolerate either "KEY" or "PSI_API_KEY=KEY"
        return raw.split("=", 1)[1].strip() if "=" in raw else raw
    sys.exit("No key: set $PSI_API_KEY or create hobbes/.psi-key")


def fetch(url, strategy, key, tries=8, timeout=75):
    """Returns parsed JSON, or None if all retries are exhausted (one bad
    cell must NOT kill the whole run). Auth/quota errors abort immediately —
    they share the same fault on every call, so retrying is pointless.

    Timeout is short on purpose: a solo PSI call finishes in ~30-60s, but
    concurrent calls on one key intermittently HANG dead forever. A hung
    connection never recovers, so we cut it at 75s and retry FRESH — a fresh
    request usually goes straight through. Waiting 180s on a dead socket is
    the slowest possible move."""
    params = [("url", url), ("strategy", strategy), ("key", key)]
    params += [("category", c) for c in CATEGORIES]
    q = ENDPOINT + "?" + urllib.parse.urlencode(params, doseq=True)
    last = None
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(q, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            msg = json.loads(body).get("error", {}).get("message", body[:200]) if body else str(e)
            if e.code in (401, 403, 429):  # bad key / quota — fatal for every call
                sys.exit(f"PSI API fatal {e.code}: {msg}")
            last = f"HTTP {e.code}: {msg}"  # 5xx and the like are transient — retry
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
        print(f"  retry {attempt}/{tries} ({strategy} {url}): {last}", file=sys.stderr, flush=True)
    print(f"  ✗ GAVE UP {strategy} {url}: {last}", file=sys.stderr, flush=True)
    return None


def score(lh, cat):
    s = lh.get("categories", {}).get(cat, {}).get("score")
    return round(s * 100) if s is not None else "—"


def audit_s(lh, aid):
    v = lh.get("audits", {}).get(aid, {}).get("numericValue")
    return round(v / 1000, 2) if v is not None else "—"  # ms -> s


def audit_ms(lh, aid):
    v = lh.get("audits", {}).get(aid, {}).get("numericValue")
    return round(v) if v is not None else "—"


def audit_raw(lh, aid):
    v = lh.get("audits", {}).get(aid, {}).get("numericValue")
    return round(v, 3) if v is not None else "—"


def field(metrics, mkey, scale=1.0):
    m = metrics.get(mkey)
    if not m or m.get("percentile") is None:
        return "—"
    return round(m["percentile"] * scale, 3 if scale != 1 else 0)


def a11y_fails(lh):
    """Failing accessibility audits from PSI's Lighthouse run — these ARE
    axe-core checks, so no separate axe run is needed. Returns a list of
    (audit_id, failing_node_count) for the binary a11y audits that scored 0.
    Manual checks (keyboard, screen reader, focus) come back as 'manual'
    scoreDisplayMode and are intentionally excluded — those stay human."""
    cat = lh.get("categories", {}).get("accessibility", {})
    audits = lh.get("audits", {})
    fails = []
    for ref in cat.get("auditRefs", []):
        a = audits.get(ref["id"], {})
        if a.get("scoreDisplayMode") == "binary" and a.get("score") == 0:
            nodes = len(a.get("details", {}).get("items", []))
            fails.append((ref["id"], nodes))
    return sorted(fails, key=lambda x: -x[1])


def main():
    args = sys.argv[1:]
    fresh = "--fresh" in args  # ignore cache, re-fetch everything
    out = Path(__file__).resolve().parent / "psi-results.md"  # durable artifact
    if "--out" in args:
        i = args.index("--out")
        out = Path(args[i + 1])
        del args[i:i + 2]
    positional = [a for a in args if a != "--fresh"]
    urls = [(f"URL{i+1}", u) for i, u in enumerate(positional)] or DEFAULT_URLS
    key = load_key()

    # Fire all page×strategy calls at once — wall-clock = slowest call, not the sum.
    # Cached (already-succeeded) calls return instantly, so a re-run only hits the
    # network for what's still missing — which also means lower concurrency and
    # far fewer of the stalls that concurrency triggers.
    jobs = [(label, url, strat) for label, url in urls for strat in ("mobile", "desktop")]

    def run(job):
        label, url, strat = job
        cf = cache_path(url, strat)
        if not fresh and cf.exists():
            print(f"  ⤿ cached {label} {strat}", file=sys.stderr, flush=True)
            return job, json.loads(cf.read_text())
        print(f"… fetching {label} {strat}", file=sys.stderr, flush=True)
        d = fetch(url, strat, key)
        if d is not None:
            cf.write_text(json.dumps(d))  # checkpoint — never re-pay for a success
            print(f"  ✓ {label} {strat}", file=sys.stderr, flush=True)
        return job, d

    with ThreadPoolExecutor(max_workers=min(MAX_CONCURRENCY, len(jobs))) as ex:
        results = dict((j, d) for j, d in ex.map(run, jobs))

    rows_a, rows_lab, rows_field, rows_c = [], [], [], []
    failed = [j for j, d in results.items() if d is None]
    warned = []  # lab runs PSI itself flagged as incomplete — numbers unreliable
    for label, url in urls:
        for strat in ("mobile", "desktop"):
            lh = (results[(label, url, strat)] or {}).get("lighthouseResult", {})
            warn = lh.get("runWarnings") or []
            mark = " ⚠" if warn else ""  # e.g. "page loaded too slowly to finish"
            if warn:
                warned.append((label, strat))
            rows_a.append(
                f"| {label} — {strat}{mark} | {score(lh,'performance')} | "
                f"{score(lh,'accessibility')} | {score(lh,'best-practices')} | {score(lh,'seo')} |"
            )
            rows_lab.append(
                f"| {label} — {strat}{mark} | {audit_s(lh,'largest-contentful-paint')} | "
                f"{audit_raw(lh,'cumulative-layout-shift')} | {audit_s(lh,'first-contentful-paint')} | "
                f"{audit_s(lh,'server-response-time')} | {audit_ms(lh,'total-blocking-time')} | "
                f"{audit_s(lh,'speed-index')} |"
            )
            fails = a11y_fails(lh)
            detail = ", ".join(f"{aid}×{n}" for aid, n in fails) or "none"
            rows_c.append(f"| {label} — {strat}{mark} | {len(fails)} | {detail} |")
        # Field data (CrUX 28-day). PREFER page-level; use the origin aggregate
        # only if neither device has page-level data — and LABEL it when we do,
        # so a whole-site average is never mistaken for this page's real numbers.
        les = [(results[(label, url, s)] or {}).get("loadingExperience", {}) for s in ("mobile", "desktop")]
        page = next((le for le in les if le.get("metrics") and le.get("origin_fallback") is not True), None)
        le = page or next((le for le in les if le.get("metrics")), {})
        fm = le.get("metrics", {})
        tag = " — origin agg." if (fm and le.get("origin_fallback") is True) else ""
        if fm:
            rows_field.append(
                f"| {label}{tag} | {field(fm,'LARGEST_CONTENTFUL_PAINT_MS',0.001)} | "
                f"{field(fm,'INTERACTION_TO_NEXT_PAINT')} | "
                f"{field(fm,'CUMULATIVE_LAYOUT_SHIFT_SCORE',0.01)} | "
                f"{le.get('overall_category','—')} |"
            )
        else:
            rows_field.append(f"| {label} | no field data | no field data | no field data | — |")

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# PSI results — {stamp}",
        "",
        "Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field",
        "are pulled and labelled SEPARATELY so they can't be mixed. Transcribe these",
        "into the scorecard; the manual a11y/SEO rows are signed by a human.",
        "",
        "Golden path: " + " · ".join(f"[{lbl}]({u})" for lbl, u in urls),
        "",
        "## A. Lighthouse scores (LAB — PSI server)",
        "",
        "| Page / Device | Performance | Accessibility | Best Practices | SEO |",
        "|---|---|---|---|---|",
        *rows_a,
        "",
        "## B1. Lab metrics (LAB — not real INP; TBT is the lab stand-in)",
        "",
        "| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |",
        "|---|---|---|---|---|---|---|",
        *rows_lab,
        "",
        "## B2. Field data (CrUX 28-day, per page — the only real INP)",
        "",
        "| Page | LCP (s) | INP (ms) | CLS | Overall |",
        "|---|---|---|---|---|",
        *rows_field,
        "",
        "## C. Accessibility — automated (axe-core via PSI)",
        "",
        "Failing axe audits straight from PSI's a11y category — `color-contrast` is "
        "the contrast-error count, `image-alt` the alt gaps. The manual rows "
        "(keyboard, focus visible, screen reader, contrast-by-eye, reduced motion) "
        "are NOT here — those stay human.",
        "",
        "| Page / Device | Failing axe audits | Details (rule × nodes) |",
        "|---|---|---|",
        *rows_c,
    ]
    if warned:
        L += ["", "> ⚠ Incomplete lab runs — PSI hit its time limit, numbers unreliable, "
              "re-measure with `--fresh`: " + ", ".join(f"{l} {s}" for l, s in warned)]
    if failed:
        L += ["", "> ✗ Failed calls (cells show — above): "
              + ", ".join(f"{lbl} {strat}" for lbl, _u, strat in failed)]
    report = "\n".join(L) + "\n"

    print(report)                                   # stdout, as before
    out.write_text(report)                          # durable artifact
    print(f"→ written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
