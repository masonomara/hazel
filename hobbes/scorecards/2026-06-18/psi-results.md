# PSI results — 2026-06-18 09:29

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Transcribe these
into scorecard sections A–D; SEO (E) comes from seo.py and the manual a11y
rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 66 ✗cut | 97 | 88 | 92 |
| Home — desktop | 68 | 97 | 88 | 92 |
| Collection — mobile | 46 ✗cut | 93 | 96 | 92 |
| Collection — desktop | 71 | 94 | 96 | 92 |
| Product — mobile | 49 | 88 | 96 | 92 |
| Product — desktop | 72 | 88 | 73 | 92 |

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 11.18 ✗cut | 0.035 | 1.97 | 0.01 | 233 | 4.91 |
| Home — desktop | 2.06 | 0.011 | 0.57 | 0.01 | 487 | 1.45 |
| Collection — mobile | 19.85 ✗cut | 0 | 5.81 | 0.01 | 465 | 7.56 |
| Collection — desktop | 1.53 | 0.011 | 0.61 | 0.01 | 516 | 1.37 |
| Product — mobile | 5.63 | 0.0 | 1.98 | 0.01 | 1444 | 4.83 |
| Product — desktop | 1.65 | 0.015 | 0.57 | 0.01 | 461 | 1.37 |

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
