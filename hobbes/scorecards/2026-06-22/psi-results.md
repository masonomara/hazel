# PSI results — 2026-06-22 11:02 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 65 ✗cut | 97 | 92 | 100 |
| Home — desktop | 86 | 97 | 92 | 100 |
| Collection — mobile | 45 ✗cut | 96 | 92 | 100 |
| Collection — desktop | 78 | 97 | 92 | 100 |
| Product — mobile | 60 ✗cut | 92 | 92 | 92 |
| Product — desktop | 85 | 92 | 77 | 92 |

> Perf-score spread across 3 runs (median kept): Home — mobile 55/65/66 · Home — desktop 66/86/86 · Collection — mobile 45/45/75 · Collection — desktop 71/78/81 · Product — mobile 60/60/66 · Product — desktop 77/85/85.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 11.87 ✗cut | 0.028 | 1.97 | 0.03 | 257 | 4.92 |
| Home — desktop | 2.36 | 0.014 | 0.61 | 0.01 | 64 | 1.29 |
| Collection — mobile | 18.33 ✗cut | 0 | 4.22 | 0.01 | 596 | 7.1 |
| Collection — desktop | 1.1 | 0.022 | 0.61 | 0.01 | 427 | 1.4 |
| Product — mobile | 16.39 ✗cut | 0.0 | 3.55 | 0.01 | 170 | 6.95 |
| Product — desktop | 2.17 | 0.013 | 0.57 | 0.01 | 154 | 1.18 |

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
| Collection — mobile | 2 | ✗ | frame-title×1, heading-order×1 |
| Collection — desktop | 1 | ✗ | frame-title×1 |
| Product — mobile | 2 | ✗ | image-alt×2, frame-title×1 |
| Product — desktop | 2 | ✗ | image-alt×2, frame-title×1 |
