# PSI results — 2026-06-22 18:11 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 54 | 97 | 92 | 100 |
| Home — desktop | 56 | 97 | 92 | 100 |
| Collection — mobile | 51 | 97 | 96 | 100 |
| Collection — desktop | 65 | 97 | 96 | 100 |
| Product — mobile | 50 | 97 | 96 | 100 |
| Product — desktop | 70 | 97 | 96 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 54/54/54 · Home — desktop 56/56/56 · Collection — mobile 51/51/51 · Collection — desktop 62/65/66 · Product — mobile 50/50/69 · Product — desktop 70/70/70.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 23.48 | 0 | 6.25 | 0.01 | 192 | 9.3 |
| Home — desktop | 2.34 | 1.01 | 0.56 | 0.01 | 193 | 1.45 |
| Collection — mobile | 5.55 | 0.984 | 1.89 | 0.01 | 164 | 3.12 |
| Collection — desktop | 1.51 | 0.203 | 0.52 | 0.01 | 443 | 1.33 |
| Product — mobile | 19.78 | 0 | 6.2 | 0.01 | 323 | 8.01 |
| Product — desktop | 1.67 | 0.205 | 0.52 | 0.02 | 300 | 1.45 |

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
