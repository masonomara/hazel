#!/usr/bin/env python3
"""
baseline.py — one-command MVP baseline runner.

Runs psi.py (A–D), seo.py (E), and crawl.py (site-wide F), then stamps a dated
scorecard from baseline-template.md with the header populated and sections A–F pasted in.
Section G (manual a11y) is left blank for the human — the above-and-beyond pass.

A baseline should reflect the CURRENT site, so this fetches fresh by default.
If a fresh run stalls partway, every successful call is still cached, so
`--resume` picks up the cached ones and only re-fetches what's missing.

USAGE:
  python3 hobbes/tools/baseline.py            # fresh capture (correct baseline)
  python3 hobbes/tools/baseline.py --resume   # reuse cache (recover a stalled run)
  python3 hobbes/tools/baseline.py --no-crawl # skip the site-wide crawl (quick rerun)
  python3 hobbes/tools/baseline.py --full     # crawl the entire sitemap, not the sample (slow)

CAPTURE then RENDER, in-process. baseline.py imports psi/seo/crawl and calls each
tool's capture() (the network step, into raw/) then its scorecard_section(s)()
(rendered straight from raw/). Those are the SAME renderers the tools use
standalone — so the digest and a standalone tool run can't disagree, and there's
no stdout to scrape or section markers to slice. Writes the whole cycle into one
folder: hobbes/cycle/YYYY-MM-DD/ — 01-baseline.md beside the raw artifacts (raw/),
so the baseline and the generated 02-evaluation.md sit beside the data they came from.
"""

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
TEMPLATE = HOBBES / "templates" / "baseline-template.md"

sys.path.insert(0, str(TOOLS))
import config
import psi
import seo
import crawl
from psi import DEFAULT_URLS  # single source of truth for the golden path
from config import client_meta

CONFIG = client_meta()  # [client] from hobbes.toml


def after(text, marker):
    i = text.find(marker)
    return text[i:].rstrip() if i >= 0 else ""


def section_g(template_text):
    """Section G (manual a11y) — intro + column header come from baseline-template.md; the
    page rows are generated from the golden path so G speaks the same URL-derived
    labels as A–F. The template's own rows are illustrative and dropped."""
    g = after(template_text, "## G.")
    head = []
    for ln in g.splitlines():
        head.append(ln)
        if "|" in ln and "-" in ln and set(ln) <= set("|-: \t"):   # the header separator row
            break
    ncols = head[-1].count("|") - 1
    rows = [f"| {lbl} — {strat} |" + "  |" * (ncols - 1)
            for lbl, _ in DEFAULT_URLS for strat in ("mobile", "desktop")]
    return "\n".join(head + rows)


def main():
    args = sys.argv[1:]
    no_crawl = "--no-crawl" in args
    full = "--full" in args
    fresh = "--resume" not in args                 # fresh capture by default; --resume reuses cache
    date = config.today()
    if "--run-dir" in args:                        # honor an explicit folder (e.g. the review's post-publish)
        rundir = Path(args[args.index("--run-dir") + 1]).resolve()
    else:
        rundir = HOBBES / "cycle" / date           # default: one dated folder per cycle
    raw = rundir / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    urls = DEFAULT_URLS

    # Capture: each tool fetches into raw/ (the network step). psi/seo share the
    # golden path; crawl is whole-site. --full cascades to the crawl only.
    psi.capture(raw, urls, fresh)
    seo.capture(raw, urls, fresh)
    if not no_crawl:
        crawl.capture(raw, fresh, full)

    # Render: pull each scorecard section straight from raw/ via the tools' own
    # renderers — the exact functions a standalone tool run uses — so the digest
    # and a standalone run can't disagree. No stdout capture, no text slicing.
    tmpl = TEMPLATE.read_text()
    abcd = psi.scorecard_sections(raw, urls)        # A, B, C, D (+ failed-call note)
    e = seo.scorecard_section(raw, urls)            # E + site-level
    g = section_g(tmpl)                             # manual a11y — page rows from the golden path
    if not (abcd and e and g):
        sys.exit("✗ couldn't render sections from raw/ — check the capture step ran and raw/ exists.")

    # F — site-wide grades + counts from the crawl (skipped with --no-crawl).
    f = crawl.scorecard_section(raw) if not no_crawl else ""

    golden = " · ".join(f"[{lbl}]({u})" for lbl, u in urls)
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

    out = rundir / "01-baseline.md"
    out.write_text(doc)
    print(f"\n✓ MVP baseline written → {out}", file=sys.stderr)
    print("  A–F filled from the tools; Section G (manual a11y) left for human sign-off.",
          file=sys.stderr)
    print(f"  Cycle folder: {rundir} (raw/ alongside; 01-baseline.md is the one digest).", file=sys.stderr)
    print("  Next: python3 hobbes/tools/evaluation.py — builds 02-evaluation.md (the problem catalog) from raw/.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
