# PSI results — 2026-06-22 19:14 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 41 | 97 | 92 | 100 |
| Home — desktop | 57 | 97 | 96 | 100 |
| Collection — mobile | 52 | 97 | 96 | 100 |
| Collection — desktop | 58 | 97 | 96 | 100 |
| Product — mobile | 48 | 97 | 96 | 100 |
| Product — desktop | 77 | 97 | 92 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 41/41/60 · Home — desktop 57/57/57 · Collection — mobile 52/52/52 · Collection — desktop 51/58/64 · Product — mobile 45/48/59 · Product — desktop 55/77/77.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 12.3 | 1.027 | 1.83 | 0.02 | 288 | 4.51 |
| Home — desktop | 2.38 | 1.008 | 0.51 | 0.01 | 180 | 1.39 |
| Collection — mobile | 19.92 | 0 | 3.26 | 0.01 | 459 | 6.22 |
| Collection — desktop | 1.8 | 1.01 | 0.51 | 0.01 | 257 | 1.1 |
| Product — mobile | 10.35 | 0 | 2.88 | 0.01 | 751 | 5.28 |
| Product — desktop | 2.13 | 0.205 | 0.5 | 0.01 | 104 | 1.53 |

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
