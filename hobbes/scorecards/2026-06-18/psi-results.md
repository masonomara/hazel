# PSI results — 2026-06-18 10:19

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Transcribe these
into scorecard sections A–D; SEO (E) comes from seo.py and the manual a11y
rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 63 ✗cut | 97 | 92 | 92 |
| Home — desktop | 89 | 97 | 92 | 92 |
| Collection — mobile | 38 ✗cut | 93 | 96 | 92 |
| Collection — desktop | 91 | 94 | 92 | 92 |
| Product — mobile | 73 | 88 | 96 | 92 |
| Product — desktop | 88 | 88 | 73 | 92 |

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 10.31 ✗cut | 0.082 | 1.97 | 0.01 | 258 | 4.89 |
| Home — desktop | 1.89 | 0.01 | 0.61 | 0.01 | 118 | 1.31 |
| Collection — mobile | 13.81 ✗cut | 0 | 3.55 | 0.01 | 1145 | 7.18 |
| Collection — desktop | 1.57 | 0.014 | 0.63 | 0.01 | 145 | 1.21 |
| Product — mobile | 5.81 | 0.0 | 1.96 | 0.01 | 148 | 4.33 |
| Product — desktop | 1.85 | 0.01 | 0.61 | 0.01 | 146 | 1.38 |

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
