# PSI results — 2026-06-18 17:29

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 65 ✗cut | 97 | 88 | 92 |
| Home — desktop | 69 | 97 | 92 | 92 |
| Collection — mobile | 53 ✗cut | 93 | 96 | 92 |
| Collection — desktop | 76 | 94 | 96 | 92 |
| Product — mobile | 52 ✗cut | 88 | 96 | 92 |
| Product — desktop | 84 | 88 | 73 | 92 |

> Perf-score spread across 3 runs (median kept): Home — mobile 50/65/67 · Home — desktop 65/69/81 · Collection — mobile 45/53/62 · Collection — desktop 70/76/94 · Product — mobile 45/52/66 · Product — desktop 73/84/88.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 10.95 ✗cut | 0.037 | 1.97 | 0.01 | 252 | 5.25 |
| Home — desktop | 2.19 | 0.011 | 0.61 | 0.01 | 418 | 1.42 |
| Collection — mobile | 14.07 ✗cut | 0.0 | 3.57 | 0.01 | 410 | 5.89 |
| Collection — desktop | 1.54 | 0.014 | 0.61 | 0.01 | 411 | 1.21 |
| Product — mobile | 22.6 ✗cut | 0 | 6.76 | 0.01 | 261 | 8.09 |
| Product — desktop | 2.19 | 0.01 | 0.61 | 0.02 | 145 | 1.54 |

## C. Field data (CrUX 28-day)

| Page | LCP (s) | INP (ms) | CLS | Pass |
|---|---|---|---|---|
| Home | 1.61 | 104.0 | 0.08 | ✓ |
| Collection | 0.77 | 78.0 | 0.01 | ✓ |
| Product — origin agg. | 1.017 | 96.0 | 0.0 | ✓ |

## D. Accessibility — automated (axe via PSI)

| Page / Device | Failing audits | Pass | Details (rule × nodes) |
|---|---|---|---|
| Home — mobile | 2 | ✗ | label-content-name-mismatch×3, frame-title×1 |
| Home — desktop | 2 | ✗ | label-content-name-mismatch×3, frame-title×1 |
| Collection — mobile | 4 | ✗ | label-content-name-mismatch×4, color-contrast×1, frame-title×1, heading-order×1 |
| Collection — desktop | 3 | ✗ | label-content-name-mismatch×4, color-contrast×1, frame-title×1 |
| Product — mobile | 3 | ✗ | button-name×5, image-alt×2, frame-title×1 |
| Product — desktop | 3 | ✗ | button-name×5, image-alt×2, frame-title×1 |
