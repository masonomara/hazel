#!/usr/bin/env python3
"""
publish-review.py — the review phase's capture orchestrator (a twin of baseline.py).

baseline.py captures the PRE-publish site into <cycle>/raw/. This captures the
**live** site AFTER a publish into <cycle>/raw-review/ — the same three tools
(psi/seo/crawl) driven the same way, the same renderers — then writes the rendered
after-digest to <cycle>/raw-review/review-baseline.md. So before and after live in one
cycle folder, side by side. review.py then diffs the cycle's pre-publish
01-baseline.md (the before — everything leading up to the PR) against this
after-digest into 06-review.md, honest by tier.

No evaluation here: the review only needs the measured before/after, not a rebuilt
problem catalog.

CAPTURE then RENDER, in-process — exactly baseline.py's contract, but pointed at
raw-review/ instead of raw/. Imports psi/seo/crawl and calls each tool's capture()
(network → raw-review/) then its scorecard_section(s)() (rendered straight from
raw-review/), so the after-digest can't disagree with a standalone tool run.

USAGE:
  python3 hobbes/tools/publish-review.py            # the latest cycle (the PR's)
  python3 hobbes/tools/publish-review.py --run-dir DIR
  python3 hobbes/tools/publish-review.py --resume   # reuse raw-review/ cache
  python3 hobbes/tools/publish-review.py --no-crawl # skip the site-wide crawl
  python3 hobbes/tools/publish-review.py --full     # crawl the whole sitemap (slow)
"""

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent

sys.path.insert(0, str(TOOLS))
import config
import psi
import seo
import crawl
from psi import DEFAULT_URLS  # single source of truth for the golden path
from config import client_meta

CONFIG = client_meta()  # [client] from hobbes.toml


def main():
    args = sys.argv[1:]
    no_crawl = "--no-crawl" in args
    full = "--full" in args
    fresh = "--resume" not in args                 # fresh re-capture by default; --resume reuses cache
    date = config.today()
    if "--run-dir" in args:
        rundir = Path(args[args.index("--run-dir") + 1]).resolve()
    else:
        rundir = config.latest_cycle(HOBBES / "cycle")   # attach to the PR's cycle
        if rundir is None:
            sys.exit("✗ no cycle folder to review — run a cycle first.")
    raw = rundir / "raw-review"                    # the AFTER, beside the pre-publish raw/
    raw.mkdir(parents=True, exist_ok=True)
    urls = DEFAULT_URLS

    # Capture: each tool fetches the LIVE site into raw-review/ (the network step).
    psi.capture(raw, urls, fresh)
    seo.capture(raw, urls, fresh)
    if not no_crawl:
        crawl.capture(raw, fresh, full)

    # Render: the same scorecard sections baseline.py emits (A–F), from raw-review/.
    abcd = psi.scorecard_sections(raw, urls)        # A, B, C, D (+ failed-call note)
    e = seo.scorecard_section(raw, urls)            # E + site-level
    if not (abcd and e):
        sys.exit("✗ couldn't render sections from raw-review/ — check the capture step ran.")
    f = crawl.scorecard_section(raw) if not no_crawl else ""

    golden = " · ".join(f"[{lbl}]({u})" for lbl, u in urls)
    doc = "\n".join([
        f"# Post-publish re-baseline — {date}",
        "",
        f"Client: {CONFIG['name']} · Site: {CONFIG['site']} · Platform: "
        f"{CONFIG['platform']} · Run by: {CONFIG['run_by']} · Date: {date}",
        "",
        f"Golden path: {golden}",
        "",
        "The **live** site re-measured after publish. The before→after diff against the "
        "pre-publish `01-baseline.md` is review.py's job (`06-review.md`).",
        "",
        abcd,
        "",
        e,
        "",
        f,
    ]) + "\n"

    out = raw / "review-baseline.md"
    out.write_text(doc)
    print(f"\n✓ post-publish re-baseline written → {out}", file=sys.stderr)
    print(f"  Cycle folder: {rundir} (raw-review/ alongside the pre-publish raw/).", file=sys.stderr)
    print("  Next: python3 hobbes/tools/review.py — diffs before→after into 06-review.md.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
