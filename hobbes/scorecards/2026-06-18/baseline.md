# Baseline scorecard — 2026-06-18

Client: Hazel Boutique · Site: hazelboutique.com · Platform: Shopify Advanced · Run by: Mason · Date: 2026-06-18

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

`✓` = pass / present · `✗` = fail / missing · `✗cut` = PSI run truncated before network-idle (value is the cutoff) · blank = human sign-off pending.

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

## E. SEO checklist (golden path)

| Item | Home | Collection | Product |
|---|---|---|---|
| Unique, descriptive title | ✓ | ✓ | ✓ |
| Meta description present | ✗ | ✗ | ✓ |
| Canonical correct | ✓ | ✓ | ✓ |
| Single H1 + ordered headings | ✗ | ✓ | ✓ |
| Valid structured data | ✓ | ✓ | ✓ |
| Open Graph / Twitter tags | ✗ | ✓ | ✓ |
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
| SEO | 9.3 |
| Security | 8.5 |
| Accessibility | 5.0 |
| Best practices | 4.7 |

| SEO / structure | Count | Pass |
|---|---|---|
| Broken links (4xx) | 0 | ✓ |
| Redirects | 0 | ✓ |
| Missing titles | 0 | ✓ |
| Duplicate titles | 4 | ✗ |
| Missing meta descriptions | 76 | ✗ |
| Pages with multiple H1 | 2 | ✗ |
| Pages with skipped heading levels | 185 | ✗ |

| Accessibility | Count | Pass |
|---|---|---|
| Pages missing image alt | 185 | ✗ |
| Pages missing aria-labels | 185 | ✗ |
| Pages missing roles | 185 | ✗ |
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
