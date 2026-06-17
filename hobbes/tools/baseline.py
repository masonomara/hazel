#!/usr/bin/env python3
"""
baseline.py — one-command MVP baseline runner.

Runs psi.py (fills A–D) and seo.py (fills E), then stamps a dated scorecard
from TEMPLATE.md with the header populated and sections A–E pasted in. Section
F (manual a11y) is left blank for the human — that's the above-and-beyond pass.

A baseline should reflect the CURRENT site, so this fetches fresh by default.
If a fresh run stalls partway, every successful call is still cached, so
`--resume` picks up the cached ones and only re-fetches what's missing.

USAGE:
  python3 hobbes/tools/baseline.py            # fresh capture (correct baseline)
  python3 hobbes/tools/baseline.py --resume   # reuse cache (recover a stalled run)

Writes hobbes/scorecards/YYYY-MM-DD-baseline.md.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
TEMPLATE = HOBBES / "scorecards" / "TEMPLATE.md"

sys.path.insert(0, str(TOOLS))
from psi import DEFAULT_URLS  # single source of truth for the golden path

# Client metadata — edit per client. The golden path lives in psi.py / seo.py.
CONFIG = {
    "client": "Hazel Boutique",
    "site": "hazelboutique.com",
    "platform": "Shopify Advanced",
    "run_by": "Mason",
}


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
    passthrough = [] if "--resume" in sys.argv[1:] else ["--fresh"]
    run_tool("psi.py", passthrough)
    run_tool("seo.py", passthrough)

    psi = (TOOLS / "psi-results.md").read_text()
    seo = (TOOLS / "seo-results.md").read_text()
    tmpl = TEMPLATE.read_text()

    abcd = after(psi, "## A.")                      # A, B, C, D + the ⚠/✗cut footnotes
    e = between(seo, "## E.", "## Page titles")     # E + site-level
    f = after(tmpl, "## F.")                        # manual a11y, blank for the human
    if not (abcd and e and f):
        sys.exit("✗ couldn't extract sections — check psi-results.md / seo-results.md / TEMPLATE.md")

    date = datetime.now().strftime("%Y-%m-%d")
    golden = " · ".join(f"[{lbl}]({u})" for lbl, u in DEFAULT_URLS)
    doc = "\n".join([
        f"# Baseline scorecard — {date}",
        "",
        f"Client: {CONFIG['client']} · Site: {CONFIG['site']} · Platform: "
        f"{CONFIG['platform']} · Run by: {CONFIG['run_by']} · Date: {date}",
        "",
        f"Golden path: {golden}",
        "",
        "**MVP baseline** — sections A–E captured automatically (`psi.py` → A–D, "
        "`seo.py` → E). Section F (manual a11y) is the above-and-beyond pass, "
        "blank pending human sign-off; a page is not certified fully pass until F is signed.",
        "",
        abcd,
        "",
        e,
        "",
        f,
    ]) + "\n"

    out = HOBBES / "scorecards" / f"{date}-baseline.md"
    out.write_text(doc)
    print(f"\n✓ MVP baseline written → {out}", file=sys.stderr)
    print("  A–E filled from the tools; Section F (manual a11y) left for human sign-off.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
