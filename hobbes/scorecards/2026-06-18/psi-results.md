# PSI results — 2026-06-18 12:06

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Transcribe these
into scorecard sections A–D; SEO (E) comes from seo.py and the manual a11y
rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 53 ✗cut | 97 | 96 | 92 |
| Home — desktop | 73 | 97 | 92 | 92 |
| Collection — mobile | 49 ✗cut | 93 | 92 | 92 |
| Collection — desktop | 80 | 94 | 96 | 92 |
| Product — mobile | 66 | 88 | 96 | 92 |
| Product — desktop | 72 | 88 | 77 | 92 |

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 20.65 ✗cut | 0.063 | 4.38 | 0.01 | 240 | 8.17 |
| Home — desktop | 2.15 | 0.01 | 0.61 | 0.01 | 349 | 1.4 |
| Collection — mobile | 20.04 ✗cut | 0 | 3.67 | 0.01 | 460 | 7.61 |
| Collection — desktop | 1.62 | 0.013 | 0.63 | 0.01 | 304 | 1.34 |
| Product — mobile | 5.63 | 0.0 | 2.26 | 0.01 | 320 | 4.85 |
| Product — desktop | 1.62 | 0.01 | 0.61 | 0.01 | 490 | 1.3 |

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
