# PSI results — 2026-06-21 20:35 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 65 ✗cut | 97 | 92 | 92 |
| Home — desktop | 86 | 97 | 92 | 92 |
| Collection — mobile | 75 | 96 | 92 | 92 |
| Collection — desktop | 83 | 97 | 92 | 92 |
| Product — mobile | 66 | 92 | 92 | 92 |
| Product — desktop | 87 | 92 | 77 | 92 |

> Perf-score spread across 3 runs (median kept): Home — mobile 61/65/66 · Home — desktop 86/86/86 · Collection — mobile 69/75/75 · Collection — desktop 79/83/84 · Product — mobile 61/66/66 · Product — desktop 69/87/95.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 8.87 ✗cut | 0.029 | 1.97 | 0.01 | 262 | 5.03 |
| Home — desktop | 2.31 | 0.01 | 0.61 | 0.01 | 66 | 1.42 |
| Collection — mobile | 4.95 | 0.0 | 1.97 | 0.01 | 200 | 4.2 |
| Collection — desktop | 1.1 | 0.013 | 0.52 | 0.01 | 335 | 1.02 |
| Product — mobile | 6.23 | 0 | 2.56 | 0.01 | 278 | 4.48 |
| Product — desktop | 2.16 | 0.01 | 0.5 | 0.01 | 118 | 1.3 |

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
