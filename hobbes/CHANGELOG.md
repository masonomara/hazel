# Changelog

The running record of shipped work. One change per entry, numbered in order, newest at the bottom of **Entries**.

**Format:** `YYYY-MM-DD — NNN type/name: what changed.`
**Types:** `feature` · `cleanup` · `fix` · `content` · `config` (extend as needed)**Rule:** every `feature` carries a `RESULTS:` line with a measured outcome. Define the metric first. If you cannot measure it, it is not shipped. Filled baseline scorecards live in `hobbes/scorecards/`.

---

## Entries

**2026-05-18 — 001 cleanup/theme-polish:** Imported and cleaned up the base Dawn theme fork — stripped unused files and dead code. Removed the route-protection plan from the storefront, cleaned up the mobile product-image slideshow, removed the product count from collection pages, and fixed the video play-button behavior on mobile. Ran a theme-check pass to clear warnings, with general style polish throughout. Wrote the initial project-goals doc. *(Work spanned 2026-05-18 to 2026-05-20.)*

**2026-05-20 — 002 cleanup/fonts:** Restored the Pragmatica and Pragmatica Condensed fonts and set up the theme's broader font system and tokens, including product-card typography.

**2026-05-21 — 003 cleanup/collections:** Audited three collections and tagged missing products — Hazel Minis, Mock Necks, Perfume — as `hazelmini`, `mockneck`, `perfume`.

**2026-05-21 — 004 cleanup/sizing-guide:** Added four size charts (hoodie, mock neck, barrel pants, joggers), added the oversized-fit note at the top, and removed all Australian size references.

**2026-05-21 — 005 cleanup/email-address:** Removed and replaced every reference to any email other than shop@hazelboutique.com.

**2026-05-21 — 006 feature/shop-pay:** Enabled Shop Pay express checkout on every page for one-tap checkout. RESULTS: After about 80,000 sessions the share of orders completed with Shop Pay declined from 9.5% to 6.7% and the reached checkout rate went down 15%. Small sample size but nothing suggest sthe SHop Pay buttons helped with checkout.

**2026-06-05 — 007 feature/custom-embroidery:** Built a custom-embroidery add-on that lets customers personalize products on the product page. An "add custom embroidery" button opens a modal with live preview and a thread-color picker, a configurable fee, and a customization that carries through the drawer, cart line items, and the order, editable and removable throughout. Pulls product and variant colors from metafields (`hex_color`, `display_color`), hides the thread-color variant from the standard picker and surfaces it in the modal, and is fully configurable from theme settings. RESULTS: 60 orders on the three mock necks, 3 customizations.

**2026-06-11 — 008 baseline/web-baseline:** Captured the Step 0 web baseline across the golden path (home, collection, product). Lighthouse run via local Chrome — the PSI API quota was zero without a key and the supplied permalinks exposed field data only — median of 3 runs per page/device; Core Web Vitals taken from CrUX field data. Findings: real-user CWV pass on product + collection (LCP ~1s, INP 79–95ms, CLS 0–0.01); Lighthouse Perf mobile 58–78 / desktop 84–94, Accessibility 88–97, Best Practices 69–73, SEO 92 across the board. Home has no field data and the worst lab numbers (mobile LCP 7.5s, CLS 0.11). Scorecard and findings in `hobbes/scorecards/2026-06-11-baseline.md` and `2026-06-11-findings.md`; MISSION priorities updated with the numbers. Measurement only — no code shipped.

**2026-06-12 — 009 cleanup/shop-pay-removal:** Removed the Shop Pay express checkout / installment messaging from the product page (the "4 payments of … with Shop Pay" block in `sections/main-product.liquid`), sunsetting feature 006. RESULTS: removal driven by 006's measured outcome — over ~80,000 sessions the Shop Pay order share fell 9.5%→6.7% and the reached-checkout rate dropped 15% with the buttons enabled; no evidence they helped checkout, so they're gone.
