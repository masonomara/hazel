#!/usr/bin/env python3
"""
baseline.py — one-command MVP baseline runner.

Runs psi.py (A–D), seo.py (E), and crawl.py (site-wide F), then stamps a dated
scorecard from TEMPLATE.md with the header populated and sections A–F pasted in.
Section G (manual a11y) is left blank for the human — the above-and-beyond pass.

A baseline should reflect the CURRENT site, so this fetches fresh by default.
If a fresh run stalls partway, every successful call is still cached, so
`--resume` picks up the cached ones and only re-fetches what's missing.

USAGE:
  python3 hobbes/tools/baseline.py            # fresh capture (correct baseline)
  python3 hobbes/tools/baseline.py --resume   # reuse cache (recover a stalled run)
  python3 hobbes/tools/baseline.py --no-crawl # skip the site-wide crawl (quick rerun)
  python3 hobbes/tools/baseline.py --full     # crawl the entire sitemap, not the sample (slow)

Writes the whole cycle into one folder: hobbes/scorecards/YYYY-MM-DD/ —
baseline.md plus the raw artifacts (raw/), the digests, and crawl.html, so the
baseline and the generated findings.md sit beside the artifacts they came from.
"""

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
TEMPLATE = HOBBES / "scorecards" / "TEMPLATE.md"

sys.path.insert(0, str(TOOLS))
import config
from psi import DEFAULT_URLS  # single source of truth for the golden path
from config import client_meta

CONFIG = client_meta()  # [client] from hobbes.toml


def run_tool(name, passthrough):
    print(f"\n=== running {name} ===", file=sys.stderr, flush=True)
    # stdout discarded (the big table also lands in the artifact); stderr flows
    # so the per-call progress / ⚠ warnings stay visible.
    r = subprocess.run([sys.executable, str(TOOLS / name)] + passthrough,
                       stdout=subprocess.DEVNULL)
    if r.returncode != 0:
        sys.exit(f"\n✗ {name} failed (exit {r.returncode}) — aborting; "
                 f"fix it or `--resume` to reuse cached calls.")


def after(text, marker):
    i = text.find(marker)
    return text[i:].rstrip() if i >= 0 else ""


def between(text, start, end):
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i)
    return (text[i:j] if j >= 0 else text[i:]).rstrip()


def main():
    no_crawl = "--no-crawl" in sys.argv[1:]
    full = "--full" in sys.argv[1:]
    date = config.today()
    rundir = HOBBES / "scorecards" / date          # one folder per cycle
    (rundir / "raw").mkdir(parents=True, exist_ok=True)
    # Thread the cycle folder through every tool so raw artifacts + digests land together.
    passthrough = ([] if "--resume" in sys.argv[1:] else ["--fresh"]) + ["--run-dir", str(rundir)]
    run_tool("psi.py", passthrough)
    run_tool("seo.py", passthrough)
    if not no_crawl:
        # --full cascades to crawl.py only: the whole sitemap instead of the sample.
        run_tool("crawl.py", passthrough + (["--full"] if full else []))

    psi = (rundir / "psi-results.md").read_text()
    seo = (rundir / "seo-results.md").read_text()
    tmpl = TEMPLATE.read_text()

    abcd = after(psi, "## A.")                      # A, B, C, D (+ failed-call note)
    e = between(seo, "## E.", "## Page titles")     # E + site-level
    g = after(tmpl, "## G.")                        # manual a11y, blank for the human
    if not (abcd and e and g):
        sys.exit("✗ couldn't extract sections — check psi-results.md / seo-results.md / TEMPLATE.md")

    # F — site-wide grades + counts straight from crawl.py (per-URL detail stays
    # in crawl-results.md for findings).
    f = ""
    if not no_crawl:
        crawl = (rundir / "crawl-results.md").read_text()
        f = between(crawl, "## F. Site-wide", "## Detail")

    golden = " · ".join(f"[{lbl}]({u})" for lbl, u in DEFAULT_URLS)
    doc = "\n".join([
        f"# Baseline scorecard — {date}",
        "",
        f"Client: {CONFIG['name']} · Site: {CONFIG['site']} · Platform: "
        f"{CONFIG['platform']} · Run by: {CONFIG['run_by']} · Date: {date}",
        "",
        f"Golden path: {golden}",
        "",
        "`✓` = pass / present · `✗` = fail / missing · `✗cut` = PSI run truncated "
        "before network-idle (value is the cutoff) · blank = human sign-off pending.",
        "",
        abcd,
        "",
        e,
        "",
        f,
        "",
        g,
    ]) + "\n"

    out = rundir / "baseline.md"
    out.write_text(doc)
    print(f"\n✓ MVP baseline written → {out}", file=sys.stderr)
    print("  A–F filled from the tools; Section G (manual a11y) left for human sign-off.",
          file=sys.stderr)
    print(f"  Cycle folder: {rundir} (raw/ + digests + crawl.html alongside).", file=sys.stderr)
    print("  Next: python3 hobbes/tools/findings.py — builds findings.md (the problem catalog) from raw/.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
