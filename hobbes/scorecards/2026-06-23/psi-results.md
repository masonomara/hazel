# PSI results — 2026-06-23 16:46 CDT

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Each page×device
is the **median of 3 runs** (lab scores swing; the median is the comparable
number). Transcribe these into scorecard sections A–D; SEO (E) comes from
seo.py and the manual a11y rows (F) are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 63 | 97 | 96 | 100 |
| Home — desktop | 41 | 97 | 92 | 100 |
| Collection — mobile | 58 | 97 | 92 | 100 |
| Collection — desktop | 62 | 97 | 92 | 100 |
| Product — mobile | 45 | 97 | 96 | 100 |
| Product — desktop | 62 | 97 | 96 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 63 · Home — desktop 41 · Collection — mobile 39/58 · Collection — desktop 50/62 · Product — mobile 43/45/70 · Product — desktop 62.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 12.23 | 0.138 | 1.89 | 0.01 | 186 | 4.67 |
| Home — desktop | 2.2 | 1.01 | 0.56 | 0.11 | 523 | 1.55 |
| Collection — mobile | 14.5 | 0.06 | 2.72 | 0.01 | 330 | 5.89 |
| Collection — desktop | 1.8 | 1.01 | 0.52 | 0.01 | 196 | 1.17 |
| Product — mobile | 6.75 | 0.987 | 1.89 | 0.01 | 213 | 4.05 |
| Product — desktop | 1.25 | 0.202 | 0.52 | 0.01 | 621 | 1.21 |

## C. Field data (CrUX 28-day)

| Page | LCP (s) | INP (ms) | CLS | Pass |
|---|---|---|---|---|
| Home | 1.596 | 105.0 | 0.08 | ✓ |
| Collection | 0.737 | 78.0 | 0.01 | ✓ |
| Product — origin agg. | 1.054 | 102.0 | 0.0 | ✓ |

## D. Accessibility — automated (axe via PSI)

| Page / Device | Failing audits | Pass | Details (rule × nodes) |
|---|---|---|---|
| Home — mobile | 1 | ✗ | frame-title×1 |
| Home — desktop | 1 | ✗ | frame-title×1 |
| Collection — mobile | 1 | ✗ | frame-title×1 |
| Collection — desktop | 1 | ✗ | frame-title×1 |
| Product — mobile | 1 | ✗ | frame-title×1 |
| Product — desktop | 1 | ✗ | frame-title×1 |
