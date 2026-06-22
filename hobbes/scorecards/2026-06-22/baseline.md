# Baseline scorecard — 2026-06-22

Client: Hazel Boutique · Site: hazelboutique.com · Platform: Shopify Advanced · Run by: Mason · Date: 2026-06-22

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

`✓` = pass / present · `✗` = fail / missing · `✗cut` = PSI run truncated before network-idle (value is the cutoff) · blank = human sign-off pending.

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
