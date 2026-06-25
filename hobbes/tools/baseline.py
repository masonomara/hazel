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

Each tool prints its rendered scorecard sections to stdout; baseline.py captures
those and assembles the ONE combined digest — 01-baseline.md — so there are no
per-tool *-results.md intermediates. Writes the whole cycle into one folder:
hobbes/cycle/YYYY-MM-DD/ — 01-baseline.md beside the raw artifacts (raw/), so
the baseline and the generated 02-evaluation.md sit beside the data they came from.
"""

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
TEMPLATE = HOBBES / "templates" / "TEMPLATE.md"

sys.path.insert(0, str(TOOLS))
from psi import DEFAULT_URLS  # single source of truth for the golden path

import config
from config import client_meta

CONFIG = client_meta()  # [client] from hobbes.toml


def run_tool(name, passthrough):
    print(f"\n=== running {name} ===", file=sys.stderr, flush=True)
    # Capture stdout (the rendered scorecard sections) and return it — this is the
    # one digest's source, so the tools no longer write their own *-results.md.
    # stderr is left to flow so the per-call progress / ⚠ warnings stay visible.
    r = subprocess.run(
        [sys.executable, str(TOOLS / name)] + passthrough,
        stdout=subprocess.PIPE,
        text=True,
    )
    if r.returncode != 0:
        sys.exit(
            f"\n✗ {name} failed (exit {r.returncode}) — aborting; "
            f"fix it or `--resume` to reuse cached calls."
        )
    return r.stdout


def after(text, marker):
    i = text.find(marker)
    return text[i:].rstrip() if i >= 0 else ""


def between(text, start, end):
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i)
    return (text[i:j] if j >= 0 else text[i:]).rstrip()


def section_g(template_text):
    """Section G (manual a11y) — intro + column header come from TEMPLATE.md; the
    page rows are generated from the golden path so G speaks the same URL-derived
    labels as A–F. The template's own rows are illustrative and dropped."""
    g = after(template_text, "## G.")
    head = []
    for ln in g.splitlines():
        head.append(ln)
        if (
            "|" in ln and "-" in ln and set(ln) <= set("|-: \t")
        ):  # the header separator row
            break
    ncols = head[-1].count("|") - 1
    rows = [
        f"| {lbl} — {strat} |" + "  |" * (ncols - 1)
        for lbl, _ in DEFAULT_URLS
        for strat in ("mobile", "desktop")
    ]
    return "\n".join(head + rows)


def main():
    args = sys.argv[1:]
    no_crawl = "--no-crawl" in args
    full = "--full" in args
    date = config.today()
    if "--run-dir" in args:  # honor an explicit folder (e.g. the review's post-publish)
        rundir = Path(args[args.index("--run-dir") + 1]).resolve()
    else:
        rundir = HOBBES / "cycle" / date  # default: one dated folder per cycle
    (rundir / "raw").mkdir(parents=True, exist_ok=True)
    # Thread the cycle folder through every tool so raw artifacts land together.
    # Each tool prints its rendered sections to stdout; we slice the ones the
    # scorecard wants straight from that — no per-tool *-results.md in between.
    passthrough = ([] if "--resume" in args else ["--fresh"]) + [
        "--run-dir",
        str(rundir),
    ]
    psi = run_tool("psi.py", passthrough)
    seo = run_tool("seo.py", passthrough)
    crawl = ""
    if not no_crawl:
        # --full cascades to crawl.py only: the whole sitemap instead of the sample.
        crawl = run_tool("crawl.py", passthrough + (["--full"] if full else []))

    tmpl = TEMPLATE.read_text()

    abcd = after(psi, "## A.")  # A, B, C, D (+ failed-call note)
    e = between(seo, "## E.", "## Page titles")  # E + site-level
    g = section_g(tmpl)  # manual a11y — page rows from the golden path
    if not (abcd and e and g):
        sys.exit(
            "✗ couldn't extract sections from the tool output — check psi.py / seo.py / TEMPLATE.md"
        )

    # F — site-wide grades + counts straight from crawl.py's stdout (the per-URL
    # detail it also prints is for findings, which reads raw/crawl.json directly).
    f = ""
    if not no_crawl:
        f = between(crawl, "## F. Site-wide", "## Detail")

    golden = " · ".join(f"[{lbl}]({u})" for lbl, u in DEFAULT_URLS)
    doc = (
        "\n".join(
            [
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
            ]
        )
        + "\n"
    )

    out = rundir / "01-baseline.md"
    out.write_text(doc)
    print(f"\n✓ MVP baseline written → {out}", file=sys.stderr)
    print(
        "  A–F filled from the tools; Section G (manual a11y) left for human sign-off.",
        file=sys.stderr,
    )
    print(
        f"  Cycle folder: {rundir} (raw/ alongside; 01-baseline.md is the one digest).",
        file=sys.stderr,
    )
    print(
        "  Next: python3 hobbes/tools/evaluation.py — builds 02-evaluation.md (the problem catalog) from raw/.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
