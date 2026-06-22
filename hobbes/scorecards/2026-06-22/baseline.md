# Baseline scorecard — 2026-06-22

Client: Hazel Boutique · Site: hazelboutique.com · Platform: Shopify Advanced · Run by: Mason · Date: 2026-06-22

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

`✓` = pass / present · `✗` = fail / missing · `✗cut` = PSI run truncated before network-idle (value is the cutoff) · blank = human sign-off pending.

## A. Lighthouse scores

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile | 63 ✗cut | 97 | 88 | 92 |
| Home — desktop | 84 | 97 | 96 | 100 |
| Collection — mobile | 74 | 97 | 96 | 100 |
| Collection — desktop | 55 | 97 | 96 | 100 |
| Product — mobile | 73 | 92 | 92 | 92 |
| Product — desktop | 85 | 97 | 73 | 100 |

> Perf-score spread across 3 runs (median kept): Home — mobile 49/63/68 · Home — desktop 67/84/84 · Collection — mobile 53/74/78 · Collection — desktop 55/55/73 · Product — mobile 70/73/73 · Product — desktop 68/85/87.

## B. Lab metrics

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile | 10.6 ✗cut | 0.117 | 2.33 | 0.01 | 161 | 4.93 |
| Home — desktop | 2.38 | 0.014 | 0.5 | 0.01 | 140 | 1.13 |
| Collection — mobile | 4.43 | 0.0 | 2.56 | 0.01 | 300 | 3.61 |
| Collection — desktop | 1.64 | 0.042 | 0.64 | 0.01 | 4035 | 3.55 |
| Product — mobile | 5.78 | 0.0 | 2.56 | 0.01 | 112 | 3.89 |
| Product — desktop | 1.83 | 0.014 | 0.61 | 0.01 | 207 | 1.21 |

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
| Product — mobile | 2 | ✗ | image-alt×2, frame-title×1 |
| Product — desktop | 1 | ✗ | frame-title×1 |

## E. SEO checklist (golden path)

| Item | Home | Collection | Product |
|---|---|---|---|
| Unique, descriptive title | ✓ | ✓ | ✓ |
| Meta description present | ✓ | ✓ | ✓ |
| Canonical correct | ✓ | ✓ | ✓ |
| Single H1 + ordered headings | ✓ | ✓ | ✓ |
| Valid structured data | ✓ | ✓ | ✓ |
| Open Graph / Twitter tags | ✓ | ✓ | ✓ |
| All images have alt | ✗ | ✗ | ✗ |
| Indexable | ✓ | ✓ | ✓ |

| Site-level | Present |
|---|---|
| sitemap.xml | ✓ |
| robots.txt | ✓ |

## F. Site-wide (sitemap sample crawl — 185 pages)

| SiteOne quality score (0–10) | Value |
|---|---|
| Performance | 10.0 |
| SEO | 9.8 |
| Security | 6.5 |
| Accessibility | 5.0 |
| Best practices | 4.6 |

| SEO / structure | Count | Pass |
|---|---|---|
| Broken links (4xx) | 0 | ✓ |
| Redirects | 0 | ✓ |
| Missing titles | 0 | ✓ |
| Duplicate titles | 4 | ✗ |
| Missing meta descriptions | 0 | ✓ |
| Pages with multiple H1 | 1 | ✗ |
| Pages with skipped heading levels | 185 | ✗ |

| Accessibility | Count | Pass |
|---|---|---|
| Pages missing image alt | 1 | ✗ |
| Pages missing aria-labels | 1 | ✗ |
| Pages missing roles | 0 | ✓ |
| Pages missing html lang | 0 | ✓ |

| Best practices | Count | Pass |
|---|---|---|
| Pages with invalid inline SVG | 185 | ✗ |
| Pages with duplicate inline SVG | 10 | ✗ |
| Pages with non-clickable phone numbers | 0 | ✓ |
| Valid HTML | 185 | ✓ |

| Security | Pass |
|---|---|
| HSTS header | ✓ |
| Content-Security-Policy | ✓ |
| Referrer-Policy | ✗ |
| Permissions-Policy | ✗ |
| Brotli compression | ✓ |
| HTTPS / valid TLS cert | ✓ |

## G. Accessibility — manual (human sign-off)

Tools cannot judge these. A page is not certified fully pass until these rows are signed: keyboard flow, visible focus, logical order, screen-reader sense, whether the alt that exists is meaningful, contrast by eye, reduced motion.

| Page / Device | Keyboard | Focus visible | Logical order | Screen reader | Alt meaningful | Contrast | Reduced motion |
|---|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |  |
