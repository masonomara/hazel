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
CYCLES = HOBBES / "cycle"
COVERAGE_OK = 0.8   # §F counts compared only if min/max crawl-page ratio ≥ this


def cycle_dirs():
    ds = [d for d in CYCLES.glob("[0-9]" * 4 + "-[0-9][0-9]-[0-9][0-9]")
          if (d / "01-baseline.md").exists()]
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
    f = run / "02-evaluation.md"
    m = re.search(r"(\d+)\s+findings", f.read_text()) if f.exists() else None
    return int(m.group(1)) if m else None


# Short parse keys → the scorecard's own display labels, so the diff speaks the
# same language 01-baseline.md does (not "perf"/"bp"/"lcp").
SCORE_LABELS = {"perf": "Performance", "a11y": "Accessibility", "bp": "Best Practices", "seo": "SEO"}
FIELD_LABELS = {"lcp": "LCP (s)", "inp": "INP (ms)", "cls": "CLS"}


def _fmt(v):
    """Ints plain, floats trimmed (50.0 → '50', 1.562 → '1.562')."""
    return f"{v:g}" if isinstance(v, float) else str(v)


def _deltas(d_cur, d_prior, worse, label):
    """Changed keys shared by both cycles → [(label, before, after, improved)].
    `worse`: 'gt' (higher = regression) or 'lt' (lower = regression)."""
    rows = []
    for k in sorted(d_cur.keys() & d_prior.keys()):
        a, b = d_prior[k], d_cur[k]
        if a == b:
            continue
        regressed = (b > a) if worse == "gt" else (b < a)
        rows.append((label(k), a, b, not regressed))
    return rows


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


def _axe_deltas(cur, prior):
    """axe nodes over the UNION of rules (a rule fixed to 0 leaves §D, so absent = 0).
    Fewer failing nodes = better → [(rule, before, after, improved)]."""
    rows = []
    for k in sorted(cur.keys() | prior.keys()):
        a, b = prior.get(k, 0), cur.get(k, 0)
        if a == b:
            continue
        rows.append((k, a, b, b < a))
    return rows


def _tier(title, prior_name, cur_name, rows, note=""):
    """One tier of the diff, rendered like a baseline section: a before→after table
    of only the rows that moved — or a single 'no change' line if none did."""
    out = [f"## {title}", ""]
    if note:
        out += [f"*{note}*", ""]
    if not rows:
        return out + ["_No change._", ""]
    out += [f"| Item | {prior_name} | {cur_name} | |", "|---|---|---|---|"]
    for label, a, b, improved in rows:
        out.append(f"| {label} | {_fmt(a)} | {_fmt(b)} | {'▲' if improved else '▼'} |")
    return out + [""]


def main():
    args = sys.argv[1:]
    runs = cycle_dirs()
    cur = Path(args[args.index("--run-dir") + 1]).resolve() if "--run-dir" in args else (runs[-1] if runs else None)
    if cur is None or not (cur / "01-baseline.md").exists():
        sys.exit("✗ no cycle with 01-baseline.md to diff")
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

    cb, pb = (cur / "01-baseline.md").read_text(), (prior / "01-baseline.md").read_text()
    cs, ps = scores(cb), scores(pb)
    cf, pf = field(cb), field(pb)
    if not (cs.keys() & ps.keys()) and not (cf.keys() & pf.keys()):
        out.write_text(f"# Diff — {cur.name} vs {prior.name}\n\nGenerated {stamp}.\n\n"
                       f"**Prior cycle ({prior.name}) has no comparable sections — older "
                       f"scorecard format. No diff computed.**\n")
        print(f"{cur.name}: prior {prior.name} not comparable (older format)")
        return

    field_rows = _deltas(cf, pf, "gt", lambda k: f"{k[0]} · {FIELD_LABELS[k[1]]}")   # field: lower better
    score_rows = _deltas(cs, ps, "lt", lambda k: f"{k[0]} · {SCORE_LABELS[k[1]]}")   # lab: higher better
    axe_rows = _axe_deltas(axe(cb), axe(pb))                                          # §D axe nodes: lower better

    cpg, ppg = crawl_pages(cb), crawl_pages(pb)
    coverage_gap = cpg and ppg and min(cpg, ppg) / max(cpg, ppg) < COVERAGE_OK
    count_rows, findings_row = [], None
    if not coverage_gap:
        count_rows = _deltas(counts(cb), counts(pb), "gt", lambda k: k)
        cft, pft = findings_total(cur), findings_total(prior)
        if cft is not None and pft is not None and cft != pft:
            findings_row = (f"Findings (catalog total)", pft, cft, cft < pft)

    field_regr = [r for r in field_rows if not r[3]]
    axe_impr = [r for r in axe_rows if r[3]]
    count_regr = [r for r in count_rows if not r[3]]
    tldr = f"{len(field_regr)} field regression(s) vs {prior.name}"
    if axe_impr:
        tldr += f" · {len(axe_impr)} a11y rule(s) improved"
    if coverage_gap:
        tldr += f" · ⚠ crawl {ppg}→{cpg} pages, counts omitted"
    elif count_regr:
        tldr += f" · {len(count_regr)} site-wide count regression(s)"

    pn, cn = prior.name, cur.name
    L = [f"# Diff — {cn} vs {pn}", "",
         f"Generated {stamp}. **{tldr}.**", "",
         "▲ better · ▼ worse · only rows that changed are shown.", ""]
    L += _tier("Field data — CrUX (28-day, the trustworthy signal)", pn, cn, field_rows,
               "Real-user data — a just-published change lands here in a later cycle, not now.")
    L += _tier("Lab scores — Lighthouse §A", pn, cn, score_rows,
               "PSI lab swings ±~10 even at median-of-3; treat small moves as noise.")
    L += _tier("Accessibility — axe failing nodes (§D, golden path)", pn, cn, axe_rows)
    if coverage_gap:
        L += ["## Site-wide counts — §F", "",
              f"⚠ Crawl coverage changed **{ppg} → {cpg} pages** — counts aren't comparable this "
              f"cycle, so they're omitted. A smaller crawl drops every count; that's sample size, "
              f"not improvement.", ""]
    else:
        L += _tier("Site-wide counts — §F (whole-site crawl)", pn, cn,
                   count_rows + ([findings_row] if findings_row else []))
    out.write_text("\n".join(L).rstrip() + "\n")
    print(tldr)


if __name__ == "__main__":
    main()
