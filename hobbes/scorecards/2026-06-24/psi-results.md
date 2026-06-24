# PSI results — 2026-06-24 07:55 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 51 | 100 | 96 | 100 |
| Home — desktop | 57 | 100 | 96 | 100 |
| Collection — mobile | 50 | 100 | 92 | 100 |
| Collection — desktop | 59 | 100 | 96 | 100 |
| Product — mobile | 51 | 100 | 92 | 100 |
| Product — desktop | 62 | 100 | 92 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 30/51/53 · Home — desktop 57/57/57 · Collection — mobile 50/50/50 · Collection — desktop 59/59/59 · Product — mobile 33/51/70 · Product — desktop 52/62/62.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 22.61 | 0 | 3.79 | 0.01 | 376 | 8.49 |
| Home — desktop | 2.28 | 1.008 | 0.52 | 0.01 | 188 | 1.4 |
| Collection — mobile | 19.66 | 0 | 5.58 | 0.01 | 369 | 7.33 |
| Collection — desktop | 1.19 | 0.196 | 0.52 | 0.01 | 817 | 1.56 |
| Product — mobile | 22.69 | 0 | 6.44 | 0.01 | 307 | 8.18 |
| Product — desktop | 1.47 | 1.01 | 0.52 | 0.01 | 230 | 1.19 |

## C. Field data (CrUX 28-day)

| Page | LCP (s) | INP (ms) | CLS | Pass |
|---|---|---|---|---|
| Home | 1.562 | 111.0 | 0.08 | ✓ |
| Collection | 0.747 | 78.0 | 0.01 | ✓ |
| Product — origin agg. | 1.043 | 103.0 | 0.0 | ✓ |

## D. Accessibility — automated (axe via PSI)

| Page / Device | Failing audits | Pass | Details (rule × nodes) |
|---|---|---|---|
| Home — mobile | 0 | ✓ | none |
| Home — desktop | 0 | ✓ | none |
| Collection — mobile | 0 | ✓ | none |
| Collection — desktop | 0 | ✓ | none |
| Product — mobile | 0 | ✓ | none |
| Product — desktop | 0 | ✓ | none |
