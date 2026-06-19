#!/usr/bin/env python3
"""
diff.py — cycle-over-cycle diff. Compares the current baseline.md against the
previous cycle's and reports regressions (a Lighthouse score that slipped, a
site-wide problem count that grew, more findings) and improvements. Writes
diff.md into the cycle folder and prints a one-line summary (for the PR title).
Reads only the system's own artifacts, so it's codebase-agnostic.

USAGE:
  python3 hobbes/tools/diff.py                 # newest cycle vs the one before
  python3 hobbes/tools/diff.py --run-dir DIR   # treat DIR as the current cycle
  python3 hobbes/tools/diff.py --out PATH      # write diff elsewhere
"""

import re
import sys
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
SCORECARDS = HOBBES / "scorecards"


def cycle_dirs():
    """Dated cycle folders that have a baseline.md, oldest -> newest by name."""
    ds = [d for d in SCORECARDS.glob("[0-9]" * 4 + "-[0-9][0-9]-[0-9][0-9]")
          if (d / "baseline.md").exists()]
    return sorted(ds, key=lambda d: d.name)


def _section(md, header):
    i = md.find(header)
    if i < 0:
        return ""
    j = md.find("\n## ", i + 1)
    return md[i:j] if j > 0 else md[i:]


def _num(cell):
    m = re.search(r"-?\d+(?:\.\d+)?", cell)
    return float(m.group()) if m else None


def scores(md):
    """Section A: {(page-device, metric): value} — higher is better."""
    out = {}
    for line in _section(md, "## A.").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and "—" in cells[0]:
            for metric, cell in zip(("perf", "a11y", "bp", "seo"), cells[1:]):
                v = _num(cell)
                if v is not None:
                    out[(cells[0], metric)] = v
    return out


def counts(md):
    """Section F count rows: {metric: count} — lower is better."""
    out = {}
    for line in _section(md, "## F.").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"\d+", cells[1]):
            out[cells[0]] = int(cells[1])
    return out


def findings_total(run):
    f = run / "findings.md"
    m = re.search(r"(\d+)\s+findings", f.read_text()) if f.exists() else None
    return int(m.group(1)) if m else None


def main():
    args = sys.argv[1:]
    runs = cycle_dirs()
    cur = Path(args[args.index("--run-dir") + 1]).resolve() if "--run-dir" in args else (runs[-1] if runs else None)
    if cur is None or not (cur / "baseline.md").exists():
        sys.exit("✗ no cycle with baseline.md to diff")
    out = Path(args[args.index("--out") + 1]) if "--out" in args else cur / "diff.md"

    earlier = [d for d in runs if d.name < cur.name]
    prior = earlier[-1] if earlier else None
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if prior is None:
        out.write_text(f"# Diff — {cur.name}\n\nGenerated {stamp}.\n\n"
                       f"**Baseline established — no prior cycle to diff.**\n")
        print(f"{cur.name}: baseline established (no prior)")
        return

    cb, pb = (cur / "baseline.md").read_text(), (prior / "baseline.md").read_text()
    cs, ps = scores(cb), scores(pb)
    cc, pc = counts(cb), counts(pb)
    cf, pf = findings_total(cur), findings_total(prior)

    # Don't let zero overlap masquerade as "no change" — flag a non-comparable prior.
    if not (cs.keys() & ps.keys()) and not (cc.keys() & pc.keys()):
        out.write_text(f"# Diff — {cur.name} vs {prior.name}\n\nGenerated {stamp}.\n\n"
                       f"**Prior cycle ({prior.name}) has no comparable sections — likely an "
                       f"older scorecard format. No diff computed.**\n")
        print(f"{cur.name}: prior {prior.name} not comparable (older format)")
        return

    regr, impr = [], []
    for k in sorted(cs.keys() & ps.keys()):
        if cs[k] < ps[k]:
            regr.append(f"{k[0]} {k[1]}: {ps[k]:g} → {cs[k]:g}")
        elif cs[k] > ps[k]:
            impr.append(f"{k[0]} {k[1]}: {ps[k]:g} → {cs[k]:g}")
    for k in sorted(cc.keys() & pc.keys()):
        if cc[k] > pc[k]:
            regr.append(f"{k}: {pc[k]} → {cc[k]}")
        elif cc[k] < pc[k]:
            impr.append(f"{k}: {pc[k]} → {cc[k]}")
    if cf is not None and pf is not None and cf != pf:
        (regr if cf > pf else impr).append(f"findings: {pf} → {cf}")

    tldr = f"{len(regr)} regression(s), {len(impr)} improvement(s) vs {prior.name}"
    L = [f"# Diff — {cur.name} vs {prior.name}", "", f"Generated {stamp}. **{tldr}.**", "",
         "## Regressions (worse than last cycle)", ""]
    L += [f"- {r}" for r in regr] or ["- (none)"]
    L += ["", "## Improvements", ""]
    L += [f"- {i}" for i in impr] or ["- (none)"]
    out.write_text("\n".join(L) + "\n")
    print(tldr)


if __name__ == "__main__":
    main()
