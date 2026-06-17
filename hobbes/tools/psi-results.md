# PSI results — 2026-06-17 13:54

Captured by `hobbes/tools/psi.py` (PageSpeed Insights API). Lab and field
are pulled and labelled SEPARATELY so they can't be mixed. Transcribe these
into the scorecard; the manual a11y/SEO rows are signed by a human.

Golden path: [Home](https://hazelboutique.com/) · [Collection](https://hazelboutique.com/collections/all-hazel-brand) · [Product](https://hazelboutique.com/products/the-capri-collection-baby-pink)

## A. Lighthouse scores (LAB — PSI server)

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile ⚠ | 62 ✗cut | 97 | 92 | 92 |
| Home — desktop ⚠ | 69 | 97 | 92 | 92 |
| Collection — mobile ⚠ | 65 | 93 | 96 | 92 |
| Collection — desktop ⚠ | 96 | 94 | 96 | 92 |
| Product — mobile ⚠ | 69 | 88 | 92 | 92 |
| Product — desktop ⚠ | 88 | 88 | 77 | 92 |

## B1. Lab metrics (LAB — not real INP; TBT is the lab stand-in)

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile ⚠ | 13.21 ✗cut | 0.087 | 2.11 | 0.01 | 272 | 5.26 |
| Home — desktop ⚠ | 1.93 | 0.009 | 0.61 | 0.01 | 482 | 1.35 |
| Collection — mobile ⚠ | 5.48 | 0.002 | 2.56 | 0.01 | 368 | 4.18 |
| Collection — desktop ⚠ | 1.29 | 0.014 | 0.63 | 0.01 | 67 | 1.11 |
| Product — mobile ⚠ | 5.48 | 0.0 | 1.97 | 0.01 | 343 | 3.95 |
| Product — desktop ⚠ | 2.13 | 0.01 | 0.53 | 0.01 | 88 | 1.24 |

## B2. Field data (CrUX 28-day, per page — the only real INP)

| Page | LCP (s) | INP (ms) | CLS | Overall |
|---|---|---|---|---|
| Home | 1.581 | 104.0 | 0.08 | FAST |
| Collection | 0.783 | 78.0 | 0.01 | FAST |
| Product — origin agg. | 1.013 | 96.0 | 0.0 | FAST |

## C. Accessibility — automated (axe-core via PSI)

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

> ✗cut **LCP truncated** — on these rows the LCP, and its LCP-weighted Performance score, is the cutoff value rather than a real paint. Treat both as unknown, not as the page's number: Home mobile
