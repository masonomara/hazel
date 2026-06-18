# Baseline scorecard — 2026-06-17

Client: Hazel Boutique · Site: hazelboutique.com · Platform: Shopify Advanced · Run by: Mason · Date: 2026-06-17

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

**MVP baseline** — sections A–E captured automatically (`psi.py` → A–D, `seo.py` → E per-page, `crawl.py` → E site-wide counts). Section F (manual a11y) is the above-and-beyond pass, blank pending human sign-off; a page is not certified fully pass until F is signed.

## A. Lighthouse scores (LAB — PSI server)

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile ⚠ | 57 ✗cut | 97 | 92 | 92 |
| Home — desktop ⚠ | 85 | 97 | 92 | 92 |
| Collection — mobile ⚠ | 77 | 93 | 96 | 92 |
| Collection — desktop ⚠ | 94 | 94 | 92 | 92 |
| Product — mobile ⚠ | 52 ✗cut | 88 | 96 | 92 |
| Product — desktop ⚠ | 93 | 88 | 73 | 92 |

## B. Lab metrics (LAB — not real INP; TBT is the lab stand-in)

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile ⚠ | 12.91 ✗cut | 0.065 | 2.56 | 0.01 | 398 | 5.55 |
| Home — desktop ⚠ | 2.51 | 0.014 | 0.61 | 0.01 | 71 | 1.42 |
| Collection — mobile ⚠ | 4.73 | 0.0 | 1.97 | 0.01 | 200 | 3.77 |
| Collection — desktop ⚠ | 1.27 | 0.014 | 0.63 | 0.01 | 129 | 1.14 |
| Product — mobile ⚠ | 13.01 ✗cut | 0.0 | 3.55 | 0.01 | 432 | 6.04 |
| Product — desktop ⚠ | 1.65 | 0.013 | 0.5 | 0.01 | 72 | 1.16 |

## C. Field data (CrUX 28-day, per page — the only real INP)

| Page | LCP (s) | INP (ms) | CLS | Overall |
|---|---|---|---|---|
| Home | 1.581 | 104.0 | 0.08 | FAST |
| Collection | 0.783 | 78.0 | 0.01 | FAST |
| Product — origin agg. | 1.013 | 96.0 | 0.0 | FAST |

## D. Accessibility — automated (axe-core via PSI)

Failing axe audits straight from PSI's a11y category — `color-contrast` is the contrast-error count, `image-alt` the alt gaps. The manual rows (keyboard, focus visible, screen reader, contrast-by-eye, reduced motion) are NOT here — those stay human.

| Page / Device | Failing axe audits | Details (rule × nodes) |
|---|---|---|
| Home — mobile ⚠ | 2 | label-content-name-mismatch×3, frame-title×1 |
| Home — desktop ⚠ | 2 | label-content-name-mismatch×3, frame-title×1 |
| Collection — mobile ⚠ | 4 | label-content-name-mismatch×4, color-contrast×1, frame-title×1, heading-order×1 |
| Collection — desktop ⚠ | 3 | label-content-name-mismatch×4, color-contrast×1, frame-title×1 |
| Product — mobile ⚠ | 3 | button-name×5, image-alt×2, frame-title×1 |
| Product — desktop ⚠ | 3 | button-name×5, image-alt×2, frame-title×1 |

> ⚠ **Never reached network-idle** — PSI cut these runs at its time limit. The early metrics still hold: FCP, CLS, TBT, Speed Index and the Accessibility / SEO / Best-Practices scores are trustworthy. Re-measuring won't help (local Lighthouse hits the same wall) — **investigate why the page never idles** (a background script keeping the network busy). Rows: Home mobile, Home desktop, Collection mobile, Collection desktop, Product mobile, Product desktop

> ✗cut **LCP truncated** — on these rows the LCP, and its LCP-weighted Performance score, is the cutoff value rather than a real paint. Treat both as unknown, not as the page's number: Home mobile, Product mobile

## E. SEO checklist

| Item | Home | Collection | Product |
|---|---|---|---|
| Unique, descriptive title | ✓ | ✓ | ✓ |
| Meta description present | ✗ missing | ✗ missing | ✓ |
| Canonical correct | ✓ | ✓ | ✓ |
| Single H1 + ordered headings | ✗ 2 h1 | ✓ | ✓ |
| Valid structured data | ✓ Organization,WebSite | ✓ Organization | ✓ Organization,Product |
| Open Graph / Twitter tags | ✗ no image | ✓ | ✓ |
| All images have meaningful alt | ⚠ 20/45 missing (quality: human) | ⚠ 44/88 missing (quality: human) | ⚠ 16/25 missing (quality: human) |
| Indexable (robots OK) | ✓ | ✓ | ✓ |

| Site-level (once per site) | Present |
|---|---|
| `sitemap.xml` | x |
| `robots.txt` | x |

| Site-wide (crawl) | Count |
|---|---|
| Broken links (4xx/5xx) | 1 |
| Redirects | 0 |
| Missing titles | 0 |
| Duplicate titles | 0 |
| Missing meta descriptions | 32 |
| Missing H1 | 1 |

## F. Accessibility — manual (optional; human sign-off, tools cannot judge these)

Optional per cycle — the automated baseline (A–E) stands on its own — but **a page cannot be certified fully pass until these manual rows are signed.** D gives the automated counts; here you judge keyboard flow, screen-reader sense, and whether the alt text that *exists* is meaningful.

| Page / Device | Keyboard | Focus visible | Logical order | Screen reader | Alt meaningful | Contrast (by eye) | Reduced motion |
|---|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |  |
