#!/usr/bin/env python3
"""
review.py — the post-publish before/after, honest about what's trustworthy.

The before is the cycle's own **pre-publish** scorecard (01-baseline.md — everything
leading up to the PR). The after is the **live** site re-measured post-publish by
publish-review.py into raw-review/baseline.md. review.py diffs the two, tier by tier:

  Field data (CrUX, §C)   stable 28-day signal → real regressions/improvements.
  Lab scores (§A)         volatile (PSI lab swings even at median-of-3) → shown, labelled.
  §D axe a11y             the failing nodes the agent actually targets.
  Site-wide counts (§F)   scale with crawl coverage → compared ONLY when the before
                          and after page counts are close; a collapsed crawl must
                          never read as a sitewide "improvement".

The tier titles, notes, and caveats live in templates/review-template.md; review.py
fills in the computed tables. Writes 06-review.md into the cycle folder; prints a
one-line summary led by the trustworthy (field) regression count.

USAGE:
  python3 hobbes/tools/review.py                 # newest cycle
  python3 hobbes/tools/review.py --run-dir DIR   # a specific cycle folder
  python3 hobbes/tools/review.py --out PATH      # write the review elsewhere
"""

import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import config
CYCLES = HOBBES / "cycle"
TEMPLATE = HOBBES / "templates" / "review-template.md"
COVERAGE_OK = 0.8   # §F counts compared only if min/max crawl-page ratio ≥ this
BEFORE_COL = "Pre-publish"
AFTER_COL = "Live"


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


# Short parse keys → the scorecard's own display labels, so the review speaks the
# same language 01-baseline.md does (not "perf"/"bp"/"lcp").
SCORE_LABELS = {"perf": "Performance", "a11y": "Accessibility", "bp": "Best Practices", "seo": "SEO"}
FIELD_LABELS = {"lcp": "LCP (s)", "inp": "INP (ms)", "cls": "CLS"}


def _fmt(v):
    """Ints plain, floats trimmed (50.0 → '50', 1.562 → '1.562')."""
    return f"{v:g}" if isinstance(v, float) else str(v)


def _deltas(d_after, d_before, worse, label):
    """Changed keys shared by both sides → [(label, before, after, improved)].
    `worse`: 'gt' (higher = regression) or 'lt' (lower = regression)."""
    rows = []
    for k in sorted(d_after.keys() & d_before.keys()):
        a, b = d_before[k], d_after[k]
        if a == b:
            continue
        regressed = (b > a) if worse == "gt" else (b < a)
        rows.append((label(k), a, b, not regressed))
    return rows


def axe(md):
    """§D axe accessibility: {rule: total failing nodes across the golden path}. Lower is better.
    A rule fixed to zero drops out of the §D table entirely, so _axe_deltas works over the union."""
    out = {}
    for line in _section(md, "## D.").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 4:                                   # | page — device | n | pass | rule×nodes, … |
            for item in c[3].split(","):
                m = re.match(r"([a-z0-9-]+)\s*×\s*(\d+)", item.strip())
                if m:
                    out[m.group(1)] = out.get(m.group(1), 0) + int(m.group(2))
    return out


def _axe_deltas(after, before):
    """axe nodes over the UNION of rules (a rule fixed to 0 leaves §D, so absent = 0).
    Fewer failing nodes = better → [(rule, before, after, improved)]."""
    rows = []
    for k in sorted(after.keys() | before.keys()):
        a, b = before.get(k, 0), after.get(k, 0)
        if a == b:
            continue
        rows.append((k, a, b, b < a))
    return rows


def parse_template(text):
    """Split review-template.md into its head (prose + {placeholders}) and an
    ordered list of (key, title, note) tiers, marked by `<!-- tier: KEY -->`."""
    parts = re.split(r"<!--\s*tier:\s*(\w+)\s*-->", text)
    head = parts[0].rstrip()
    tiers = []
    for i in range(1, len(parts), 2):
        key = parts[i]
        body = [ln for ln in parts[i + 1].strip().splitlines()]
        title = body[0].lstrip("# ").strip() if body else key
        note = " ".join(ln.strip() for ln in body[1:] if ln.strip())
        tiers.append((key, title, note))
    return head, tiers


def render_tier(title, note, rows):
    """One tier rendered like a baseline section: a before→after table of only the
    rows that moved — or a single 'no change' line if none did."""
    out = [f"## {title}", ""]
    if note:
        out += [f"*{note}*", ""]
    if not rows:
        return out + ["_No change._", ""]
    out += [f"| Item | {BEFORE_COL} | {AFTER_COL} | |", "|---|---|---|---|"]
    for label, a, b, improved in rows:
        out.append(f"| {label} | {_fmt(a)} | {_fmt(b)} | {'▲' if improved else '▼'} |")
    return out + [""]


def main():
    args = sys.argv[1:]
    cur = (
        Path(args[args.index("--run-dir") + 1]).resolve()
        if "--run-dir" in args
        else config.latest_cycle(CYCLES)
    )
    if cur is None or not (cur / "01-baseline.md").exists():
        sys.exit("✗ no cycle with 01-baseline.md to review")
    after_path = cur / "raw-review" / "baseline.md"
    if not after_path.exists():
        sys.exit(f"✗ no {after_path} — run publish-review.py first")
    out = Path(args[args.index("--out") + 1]) if "--out" in args else cur / "06-review.md"
    stamp = config.stamp()

    before_md = (cur / "01-baseline.md").read_text()   # everything leading up to the PR
    after_md = after_path.read_text()                  # the live site, post-publish

    sa, sb = scores(after_md), scores(before_md)
    fa, fb = field(after_md), field(before_md)
    if not (sa.keys() & sb.keys()) and not (fa.keys() & fb.keys()):
        out.write_text(
            f"# Post-publish review — {cur.name}\n\nGenerated {stamp}.\n\n"
            f"**The pre-publish baseline and the live re-baseline share no comparable "
            f"sections — nothing to diff.**\n"
        )
        print(f"{cur.name}: no comparable sections")
        return

    rows = {
        "field": _deltas(fa, fb, "gt", lambda k: f"{k[0]} · {FIELD_LABELS[k[1]]}"),   # field: lower better
        "lab": _deltas(sa, sb, "lt", lambda k: f"{k[0]} · {SCORE_LABELS[k[1]]}"),      # lab: higher better
        "axe": _axe_deltas(axe(after_md), axe(before_md)),                            # §D axe nodes: lower better
        "counts": [],
    }

    cpg, ppg = crawl_pages(after_md), crawl_pages(before_md)
    coverage_gap = cpg and ppg and min(cpg, ppg) / max(cpg, ppg) < COVERAGE_OK
    if not coverage_gap:
        rows["counts"] = _deltas(counts(after_md), counts(before_md), "gt", lambda k: k)

    field_regr = [r for r in rows["field"] if not r[3]]
    axe_impr = [r for r in rows["axe"] if r[3]]
    count_regr = [r for r in rows["counts"] if not r[3]]
    tldr = f"{len(field_regr)} field regression(s) vs pre-publish"
    if axe_impr:
        tldr += f" · {len(axe_impr)} a11y rule(s) improved"
    if coverage_gap:
        tldr += f" · ⚠ crawl {ppg}→{cpg} pages, counts omitted"
    elif count_regr:
        tldr += f" · {len(count_regr)} site-wide count regression(s)"

    head, tiers = parse_template(TEMPLATE.read_text())
    head = (head.replace("{cycle}", cur.name)
                .replace("{stamp}", stamp)
                .replace("{tldr}", tldr))
    L = [head, ""]
    for key, title, note in tiers:
        if key == "counts" and coverage_gap:
            L += [f"## {title}", "",
                  f"⚠ Crawl coverage changed **{ppg} → {cpg} pages** — counts aren't comparable "
                  f"this review, so they're omitted. A smaller crawl drops every count; that's "
                  f"sample size, not improvement.", ""]
        else:
            L += render_tier(title, note, rows.get(key, []))
    out.write_text("\n".join(L).rstrip() + "\n")
    print(tldr)


if __name__ == "__main__":
    main()
