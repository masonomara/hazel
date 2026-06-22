# PSI results — 2026-06-22 12:42 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 63 ✗cut | 97 | 88 | 92 |
| Home — desktop | 84 | 97 | 96 | 100 |
| Collection — mobile | 74 | 97 | 96 | 100 |
| Collection — desktop | 55 | 97 | 96 | 100 |
| Product — mobile | 73 | 92 | 92 | 92 |
| Product — desktop | 85 | 97 | 73 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 49/63/68 · Home — desktop 67/84/84 · Collection — mobile 53/74/78 · Collection — desktop 55/55/73 · Product — mobile 70/73/73 · Product — desktop 68/85/87.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 10.6 ✗cut | 0.117 | 2.33 | 0.01 | 161 | 4.93 |
| Home — desktop | 2.38 | 0.014 | 0.5 | 0.01 | 140 | 1.13 |
| Collection — mobile | 4.43 | 0.0 | 2.56 | 0.01 | 300 | 3.61 |
| Collection — desktop | 1.64 | 0.042 | 0.64 | 0.01 | 4035 | 3.55 |
| Product — mobile | 5.78 | 0.0 | 2.56 | 0.01 | 112 | 3.89 |
| Product — desktop | 1.83 | 0.014 | 0.61 | 0.01 | 207 | 1.21 |

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
| Product — mobile | 2 | ✗ | image-alt×2, frame-title×1 |
| Product — desktop | 1 | ✗ | frame-title×1 |
