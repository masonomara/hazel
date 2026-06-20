# PSI results — 2026-06-20 16:48 CDT

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
| Home — desktop | 81 | 97 | 92 | 92 |
| Collection — mobile | 69 | 96 | 92 | 92 |
| Collection — desktop | 74 | 97 | 92 | 92 |
| Product — mobile | 73 | 92 | 92 | 92 |
| Product — desktop | 90 | 92 | 73 | 92 |

> Perf-score spread across 3 runs (median kept): Home — mobile 63/63/65 · Home — desktop 80/81/86 · Collection — mobile 40/69/78 · Collection — desktop 72/74/76 · Product — mobile 41/73/73 · Product — desktop 73/90/90.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 9.76 ✗cut | 0.026 | 2.56 | 0.01 | 242 | 5.07 |
| Home — desktop | 2.28 | 0.01 | 0.61 | 0.01 | 186 | 1.5 |
| Collection — mobile | 5.25 | 0.002 | 1.97 | 0.01 | 326 | 4.79 |
| Collection — desktop | 1.32 | 0.013 | 0.61 | 0.01 | 505 | 1.33 |
| Product — mobile | 5.4 | 0.0 | 1.83 | 0.01 | 183 | 4.57 |
| Product — desktop | 1.56 | 0.008 | 0.61 | 0.01 | 170 | 1.2 |

## C. Field data (CrUX 28-day)

| Page | LCP (s) | INP (ms) | CLS | Pass |
|---|---|---|---|---|
| Home | 1.61 | 103.0 | 0.08 | ✓ |
| Collection | 0.754 | 78.0 | 0.01 | ✓ |
| Product — origin agg. | 1.029 | 96.0 | 0.0 | ✓ |

## D. Accessibility — automated (axe via PSI)

| Page / Device | Failing audits | Pass | Details (rule × nodes) |
|---|---|---|---|
| Home — mobile | 2 | ✗ | label-content-name-mismatch×3, frame-title×1 |
| Home — desktop | 1 | ✗ | frame-title×1 |
| Collection — mobile | 3 | ✗ | label-content-name-mismatch×4, frame-title×1, heading-order×1 |
| Collection — desktop | 2 | ✗ | label-content-name-mismatch×4, frame-title×1 |
| Product — mobile | 2 | ✗ | image-alt×2, frame-title×1 |
| Product — desktop | 2 | ✗ | image-alt×2, frame-title×1 |
