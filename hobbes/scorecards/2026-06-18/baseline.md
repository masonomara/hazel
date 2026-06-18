# Baseline scorecard — 2026-06-18

Client: Hazel Boutique · Site: hazelboutique.com · Platform: Shopify Advanced · Run by: Mason · Date: 2026-06-18

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

`✓` = pass / present · `✗` = fail / missing · `✗cut` = PSI run truncated before network-idle (value is the cutoff) · blank = human sign-off pending.

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

## F. Site-wide (whole-site crawl — 200 pages)

| SiteOne quality score (0–10) | Value |
|---|---|
| Performance | 9.5 |
| SEO | 8.8 |
| Security | 6.5 |
| Accessibility | 5.0 |
| Best practices | 4.5 |

| SEO / structure | Count | Pass |
|---|---|---|
| Broken links (4xx) | 1 | ✗ |
| Redirects | 0 | ✓ |
| Missing titles | 0 | ✓ |
| Duplicate titles | 1 | ✗ |
| Missing meta descriptions | 51 | ✗ |
| Pages with multiple H1 | 2 | ✗ |
| Pages with skipped heading levels | 204 | ✗ |

| Accessibility | Count | Pass |
|---|---|---|
| Pages missing image alt | 203 | ✗ |
| Pages missing aria-labels | 203 | ✗ |
| Pages missing roles | 203 | ✗ |
| Pages missing html lang | 0 | ✓ |

| Best practices | Count | Pass |
|---|---|---|
| Pages with invalid inline SVG | 204 | ✗ |
| Pages with duplicate inline SVG | 23 | ✗ |
| Pages with non-clickable phone numbers | 1 | ✗ |
| Valid HTML | 200 | ✓ |

| Security | Pass |
|---|---|
| HSTS header | ✗ |
| Content-Security-Policy | ✗ |
| Referrer-Policy | ✗ |
| Permissions-Policy | ✗ |
| Brotli compression | ✗ |
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
