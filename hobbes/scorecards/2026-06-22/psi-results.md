# PSI results — 2026-06-22 21:41 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 52 | 97 | 96 | 100 |
| Home — desktop | 49 | 97 | 96 | 100 |
| Collection — mobile | 43 | 97 | 96 | 100 |
| Collection — desktop | 61 | 97 | 96 | 100 |
| Product — mobile | 48 | 97 | 92 | 100 |
| Product — desktop | 67 | 97 | 96 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 52/52/52 · Home — desktop 49/49/49 · Collection — mobile 43/43/43 · Collection — desktop 55/61/65 · Product — mobile 42/48/48 · Product — desktop 65/67/67.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 23.17 | 0 | 5.94 | 0.01 | 269 | 8.93 |
| Home — desktop | 2.07 | 1.008 | 0.52 | 0.01 | 352 | 1.39 |
| Collection — mobile | 5.48 | 0.988 | 1.91 | 0.01 | 408 | 3.74 |
| Collection — desktop | 1.22 | 0.206 | 0.52 | 0.01 | 671 | 1.44 |
| Product — mobile | 19.05 | 0 | 5.64 | 0.01 | 419 | 7.63 |
| Product — desktop | 1.46 | 1.01 | 0.52 | 0.01 | 148 | 1.29 |

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
