# PSI results — 2026-06-22 22:46 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 63 | 97 | 92 | 100 |
| Home — desktop | 48 | 97 | 96 | 100 |
| Collection — mobile | 62 | 97 | 96 | 100 |
| Collection — desktop | 51 | 97 | 92 | 100 |
| Product — mobile | 70 | 97 | 92 | 100 |
| Product — desktop | 60 | 97 | 92 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 63/63/63 · Home — desktop 48/48/48 · Collection — mobile 62/62/62 · Collection — desktop 51/51/51 · Product — mobile 52/70/70 · Product — desktop 60/60/60.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 12.6 | 0.138 | 1.89 | 0.01 | 150 | 5.11 |
| Home — desktop | 2.38 | 1.01 | 0.52 | 0.01 | 302 | 1.61 |
| Collection — mobile | 13.95 | 0.06 | 2.94 | 0.01 | 182 | 5.53 |
| Collection — desktop | 1.7 | 1.008 | 0.52 | 0.01 | 384 | 1.25 |
| Product — mobile | 5.55 | 0.123 | 1.83 | 0.01 | 158 | 4.49 |
| Product — desktop | 1.56 | 1.01 | 0.52 | 0.01 | 247 | 1.29 |

## C. Field data (CrUX 28-day)

| Page | LCP (s) | INP (ms) | CLS | Pass |
|---|---|---|---|---|
| Home | 1.551 | 105.0 | 0.08 | ✓ |
| Collection | 0.731 | 78.0 | 0.01 | ✓ |
| Product — origin agg. | 1.028 | 98.0 | 0.0 | ✓ |

## D. Accessibility — automated (axe via PSI)

| Page / Device | Failing audits | Pass | Details (rule × nodes) |
|---|---|---|---|
| Home — mobile | 2 | ✗ | label-content-name-mismatch×3, frame-title×1 |
| Home — desktop | 1 | ✗ | frame-title×1 |
| Collection — mobile | 1 | ✗ | frame-title×1 |
| Collection — desktop | 1 | ✗ | frame-title×1 |
| Product — mobile | 1 | ✗ | frame-title×1 |
| Product — desktop | 1 | ✗ | frame-title×1 |
