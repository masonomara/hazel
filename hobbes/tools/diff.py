#!/usr/bin/env python3
"""
diff.py — cycle-over-cycle diff, honest about what's trustworthy.

  Field data (CrUX, §C)   stable 28-day signal → real regressions/improvements.
  Lab scores (§A)         volatile (PSI lab swings even at median-of-3) → shown, labelled.
  Site-wide counts (§F)   scale with crawl coverage → compared ONLY when the two
                          cycles' page counts are close; a collapsed crawl must
                          never read as a sitewide "improvement".

Writes diff.md into the cycle folder; prints a one-line summary led by the
trustworthy (field) regression count. Reads only the system's own artifacts.

USAGE:
  python3 hobbes/tools/diff.py                 # newest cycle vs the one before
  python3 hobbes/tools/diff.py --run-dir DIR   # treat DIR as the current cycle
  python3 hobbes/tools/diff.py --prior DIR     # pin the baseline to compare against
  python3 hobbes/tools/diff.py --out PATH      # write diff elsewhere
"""

import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import config
SCORECARDS = HOBBES / "scorecards"
COVERAGE_OK = 0.8   # §F counts compared only if min/max crawl-page ratio ≥ this


def cycle_dirs():
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
    """§A Lighthouse scores: {(page-device, metric): value}. Higher is better."""
    out = {}
    for line in _section(md, "## A.").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 5 and "—" in c[0]:
            for metric, cell in zip(("perf", "a11y", "bp", "seo"), c[1:]):
                v = _num(cell)
                if v is not None:
                    out[(c[0], metric)] = v
    return out


def field(md):
    """§C CrUX field: {(page, metric): value}. metric ∈ lcp/inp/cls. Lower is better."""
    out = {}
    for line in _section(md, "## C.").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 5 and c[0] not in ("Page", "") and not c[0].startswith("---"):
            page = c[0].split("—")[0].strip()           # drop "— origin agg."
            for metric, cell in zip(("lcp", "inp", "cls"), c[1:4]):
                v = _num(cell)
                if v is not None:
                    out[(page, metric)] = v
    return out


def counts(md):
    """§F site-wide count rows: {metric: count}. Lower is better."""
    out = {}
    for line in _section(md, "## F.").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 3 and re.fullmatch(r"\d+", c[1]):
            out[c[0]] = int(c[1])
    return out


def crawl_pages(md):
    """The page count the crawl actually analysed, from the §F header."""
    m = re.search(r"## F\. Site-wide \([^)]*?(\d+)\s*pages?\)", md)
    return int(m.group(1)) if m else None


def findings_total(run):
    f = run / "findings.md"
    m = re.search(r"(\d+)\s+findings", f.read_text()) if f.exists() else None
    return int(m.group(1)) if m else None


def _delta_lines(d_cur, d_prior, worse):
    """(regressions, improvements) for two {key: value} dicts. `worse` says which
    direction is a regression: 'gt' (higher = worse) or 'lt' (lower = worse)."""
    regr, impr = [], []
    for k in sorted(d_cur.keys() & d_prior.keys()):
        a, b = d_prior[k], d_cur[k]
        if a == b:
            continue
        label = (f"{k[0]} {k[1]}" if isinstance(k, tuple) else k) + f": {a:g} → {b:g}"
        bad = (b > a) if worse == "gt" else (b < a)
        (regr if bad else impr).append(label)
    return regr, impr


def axe(md):
    """§D axe accessibility: {rule: total failing nodes across the golden path}. Lower is better.
    A rule fixed to zero drops out of the §D table entirely, so _axe_delta works over the union."""
    out = {}
    for line in _section(md, "## D.").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 4:                                   # | page — device | n | pass | rule×nodes, … |
            for item in c[3].split(","):
                m = re.match(r"([a-z0-9-]+)\s*×\s*(\d+)", item.strip())
                if m:
                    out[m.group(1)] = out.get(m.group(1), 0) + int(m.group(2))
    return out


def _axe_delta(cur, prior):
    """(regressions, improvements) over the UNION of rules — a rule fixed to 0 vanishes from
    §D, so absent = 0. Fewer failing nodes is better."""
    regr, impr = [], []
    for k in sorted(cur.keys() | prior.keys()):
        a, b = prior.get(k, 0), cur.get(k, 0)
        if a == b:
            continue
        (regr if b > a else impr).append(f"{k}: {a} → {b}")
    return regr, impr


def main():
    args = sys.argv[1:]
    runs = cycle_dirs()
    cur = Path(args[args.index("--run-dir") + 1]).resolve() if "--run-dir" in args else (runs[-1] if runs else None)
    if cur is None or not (cur / "baseline.md").exists():
        sys.exit("✗ no cycle with baseline.md to diff")
    out = Path(args[args.index("--out") + 1]) if "--out" in args else cur / "diff.md"
    if "--prior" in args:
        prior = Path(args[args.index("--prior") + 1]).resolve()
    else:
        earlier = [d for d in runs if d.name < cur.name]
        prior = earlier[-1] if earlier else None
    stamp = config.stamp()

    if prior is None:
        out.write_text(f"# Diff — {cur.name}\n\nGenerated {stamp}.\n\n"
                       f"**Baseline established — no prior cycle to diff.**\n")
        print(f"{cur.name}: baseline established (no prior)")
        return

    cb, pb = (cur / "baseline.md").read_text(), (prior / "baseline.md").read_text()
    cs, ps = scores(cb), scores(pb)
    cf, pf = field(cb), field(pb)
    if not (cs.keys() & ps.keys()) and not (cf.keys() & pf.keys()):
        out.write_text(f"# Diff — {cur.name} vs {prior.name}\n\nGenerated {stamp}.\n\n"
                       f"**Prior cycle ({prior.name}) has no comparable sections — older "
                       f"scorecard format. No diff computed.**\n")
        print(f"{cur.name}: prior {prior.name} not comparable (older format)")
        return

    field_regr, field_impr = _delta_lines(cf, pf, worse="gt")          # field: lower better
    score_regr, score_impr = _delta_lines(cs, ps, worse="lt")          # lab: higher better
    lab = [f"▼ {r}" for r in score_regr] + [f"▲ {i}" for i in score_impr]
    axe_regr, axe_impr = _axe_delta(axe(cb), axe(pb))                   # §D axe nodes: lower better

    cpg, ppg = crawl_pages(cb), crawl_pages(pb)
    coverage_gap = cpg and ppg and min(cpg, ppg) / max(cpg, ppg) < COVERAGE_OK
    count_regr, count_impr, findings_line = [], [], ""
    if not coverage_gap:
        count_regr, count_impr = _delta_lines(counts(cb), counts(pb), worse="gt")
        cft, pft = findings_total(cur), findings_total(prior)
        if cft is not None and pft is not None and cft != pft:
            (count_regr if cft > pft else count_impr).append(f"findings: {pft} → {cft}")

    tldr = f"{len(field_regr)} field regression(s) vs {prior.name}"
    if axe_impr:
        tldr += f" · {len(axe_impr)} a11y rule(s) improved"
    if coverage_gap:
        tldr += f" · ⚠ crawl {ppg}→{cpg} pages, counts omitted"
    elif count_regr:
        tldr += f" · {len(count_regr)} site-wide count regression(s)"

    L = [f"# Diff — {cur.name} vs {prior.name}", "", f"Generated {stamp}. **{tldr}.**", "",
         "## Field data — CrUX, the trustworthy signal (lower = better)", "",
         "**Regressions:**", *([f"- {r}" for r in field_regr] or ["- (none)"]),
         "", "**Improvements:**", *([f"- {i}" for i in field_impr] or ["- (none)"]),
         "", "## Lab scores — §A, volatile (PSI lab swings ±~10 even at median-of-3; small moves are noise)", "",
         *(lab or ["- (no change)"]),
         "", "## Accessibility — §D axe findings (failing nodes on the golden path, lower = better)", "",
         "**Fixed / improved:**", *([f"- {i}" for i in axe_impr] or ["- (none)"]),
         "", "**Regressions:**", *([f"- {r}" for r in axe_regr] or ["- (none)"]),
         "", "## Site-wide counts — §F (crawl-coverage dependent)", ""]
    if coverage_gap:
        L += [f"⚠ Crawl coverage changed **{ppg} → {cpg} pages** — site-wide counts are not "
              f"comparable this cycle and are omitted. A smaller crawl drops every count; "
              f"that is sample size, not improvement."]
    else:
        L += ["**Regressions:**", *([f"- {r}" for r in count_regr] or ["- (none)"]),
              "", "**Improvements:**", *([f"- {i}" for i in count_impr] or ["- (none)"])]
    out.write_text("\n".join(L) + "\n")
    print(tldr)


if __name__ == "__main__":
    main()
