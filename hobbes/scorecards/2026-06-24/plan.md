# Plan — 2026-06-24

Site: https://hazelboutique.com/ · Cycle: 2026-06-24 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 31 findings, grouped into **8 systems** plus an explicit won't-chase list, ordered by leverage. Every finding lands in a system or the won't-chase list — nothing dropped, nothing invented. Findings are fixed; effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`.

> **What this cycle's re-measurement settles.** Last cycle shipped the Mailchimp popup frame-title shim (`snippets/a11y-frame-title.liquid`). `diff.md` confirms it landed and worked: **`frame-title` 6 → 0** — the "1 a11y rule improved." With it gone, **§D axe is now clean on all 6 golden runs (0 failing audits)** and Lighthouse Accessibility reads **100 on every golden page × device**. The two a11y wins of the last two cycles (`label-content-name-mismatch` 3→0, then `frame-title` 6→0) are both banked and validated.

**The strategy in one line:** with the golden-path axe clean, the one remaining failing a11y signal is the **sitewide crawl** (§F: 1 page missing image alt, 1 missing aria-labels) — both the `isp_*` third-party search app on `/pages/search-results` — so a contained additive shim (the proven frame-title pattern) leads; everything below it is content, app-business, platform, or browser-gated.

**Three realities that shaped every rating:**
- **Field passes; lab fails; the lab is noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages (all ✓). The 3 "field regressions" in `diff.md` are sub-ms / single-ms CrUX jitter (Collection LCP 0.737, Home INP 105→111, Product INP 102→103) — still comfortably inside "good," not a real-user move. Meanwhile §A lab perf swings hard (Home-mobile 63→51, Collection-mobile 58→50) while CrUX holds — PSI's fixed-throttle volatility over app-injected JS. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly.
- **Resource ≠ "code."** Most of this catalog is **content or app/platform**, not Liquid Hobbes can author: the search-results page body + the `isp_*` search app (SEO-1, A11Y-1 slivers), meaningful per-product alt at scale (SEO-2), 5 duplicate descriptions (SEO-3), oversized/HEIC source files (PERF-2/5), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe theme front is all but exhausted — by design.** The cart-drawer `card_heading_tag` heading cascade (185→2, banked), card-image alt fallback, slideshow/pagination labels, hero-logo dims + LCP `fetchpriority`, the Referrer-Policy meta, last cycle's frame-title shim, and the cycle-before's hero label fix are all in `main`; the catalog still enumerates the live-site lag. What is genuinely *both* unshipped *and* theme-authorable this cycle is exactly one thing: a contained shim that supplies the missing accessible names on the runtime-injected search-app controls (SYS-1).

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Search-app accessibility (the one theme lever left)
- **Findings:** A11Y-1 (the non-structural slivers: 3 image-alt, 1 form-label, 1 unnamed-link)
- **The system:** Every non-heading A11Y-1 sliver lives on **`/pages/search-results`** and belongs to a **third-party search app** whose elements carry the `isp_*` prefix (verified absent from theme source — repo-wide search for `isp_` returns only scorecard files). From the crawl: `<input id="isp_main_search_box">` with no label (missing-form-label = 1), `<img id="isp_watermark_img">` with no alt (1 of the 3 missing-image-alt), a second generic `<img>` with no alt, and one unnamed link/button. None of it is theme markup — the clean fix is the search app's config/template (or replacing the app), which is human-owned. But the run is GitHub-only, and the **frame-title shim just proved (6→0) that a contained, additive theme shim is the right mechanism for runtime-injected markup**. So the theme carries the same pattern here: a scoped, idempotent, self-disconnecting script that sets `aria-label="Search products"` on the unlabeled search box and `alt=""` on the decorative watermark — the two names that are *unambiguously correct and safe to author blind*. The generic content `<img>` (likely a result/product image whose alt should be the product name) and the unnamed link are **not** safely authorable from source — a generic alt/label would be meaningless or wrong — so they stay with the app config.
- **Effort:** 1/5 — Mason, one self-contained snippet (`snippets/a11y-search-app.liquid`) rendered from a single line in `theme.liquid`; purely additive (only sets attributes that are missing). Bucket-2: needs axe/browser confirmation at review (controls are runtime-injected).
- **Impact:** 3/5 — Priority 1 (accessibility); the mission counts the **sitewide crawl**, and this clears §F missing-aria-labels (1→0) and a missing-image-alt sliver. Dampened from 4 because it is **off the golden path** (Lighthouse a11y already 100 there) and one app on one page type — lower leverage than the golden-path frame-title win it follows.
- **Priority:** 3 ÷ 1 = **3.0**

## SYS-2 · Heading outline & structural aggregate
- **Findings:** SEO-1, A11Y-1 (the 1,711 HTML-structural warnings)
- **The system:** The heading cascade is validated and all but closed — sitewide skipped-heading pages fell 185 → 2 once the cart-drawer `card_heading_tag` fix removed the four leading `<h3>` from the global outline (banked in `main`). What remains (SEO-1, §F: 1 multiple-H1 + 2 skipped-level) is **`/pages/search-results`**: `h1 → h1 → h2` — a Shopify page rendered through `sections/main-page.liquid` as `<h1>{{ page.title }}</h1>` + `{{ page.content }}`, where the **second `<h1>` and the order break live in the page body and the `isp_*` search-app markup**, not theme Liquid (the theme emits exactly one `<h1>`). The A11Y-1 aggregate (1,716 flagged elements sitewide) rolls up here: **1,711 of 1,716 are "HTML structural" warnings** — the same heading-order family, a blunt sitewide rollup, not a per-element theme defect; the 5 remaining slivers are SYS-1's.
- **Effort:** 2/5 — small, but **content/app, not theme code**: demote the stray search-results `<h1>` in the page body (admin) and/or the search-app template. Jenna/Britni in the theme editor + the search-app config — the theme repo can't reach `{{ page.content }}` or the `isp_*` markup.
- **Impact:** 2/5 — Priority 1 + 2, but only 1 of 181 pages carries the error and the cascade already banked the win; the 1,711-warning aggregate is benign structural noise, not a fixable defect.
- **Priority:** 2 ÷ 2 = **1.0**

## SYS-3 · Image alt at scale
- **Findings:** SEO-2
- **The system:** `alt` coverage across the golden pages (Home 19/43, Collection 45/88, Product 16/24 `<img>` missing alt). Two tracks: **(a) Theme — done.** The product-card featured image binds `alt` to the product title (merged); a full theme sweep confirms every live theme `<img>` carries an `alt`. **(b) Content + apps — open.** The remaining counts are admin product images the merchant left blank, plus app-injected widget images (Judge.me, Instafeed). The count also includes decorative hover images correctly `alt=""`.
- **Effort:** 4/5 — theme side shipped (a 1); meaningful alt across the catalog is the cost (client content at scale, ongoing) — Jenna/Britni.
- **Impact:** 4/5 — dual priority (a11y + SEO); dampened because the theme defect is closed and the residue is partly decorative-by-design.
- **Priority:** 4 ÷ 4 = **1.0**

## SYS-4 · Page metadata uniqueness
- **Findings:** SEO-3
- **The system:** 5 sets of duplicate meta descriptions — "Hazel Boutique" ×5, a repeated 18 oz candle spec ×4, repeated EVI11 vintage copy ×4/×2, a bracelet line ×2. (Duplicate **titles** are gone — fixed in admin a prior cycle.) Distinguishing near-identical product/collection pages is bespoke copy, not a theme mechanism: the templated head fallback already gives every page *a* description; making genuinely-similar pages *unique* is admin rewrites — Jenna/Britni.
- **Effort:** 2/5 — no code; ~9 admin description rewrites, Jenna/Britni.
- **Impact:** 2/5 — Priority 2, but bounded and the golden-path SEO score already reads 100.
- **Priority:** 2 ÷ 2 = **1.0**

## SYS-5 · Image delivery & sizing
- **Findings:** PERF-2, PERF-13, PERF-17, PERF-18
- **The system:** Images are the heaviest payload class and the mobile-LCP driver — oversized product JPEGs (375/275/251 KB, PERF-2) and **HEIC source files served raw** (141/114 KB `.heic` in PERF-2) need re-exporting to WebP/AVIF at sane dimensions (Jenna's assets). PERF-13 (unsized images): the theme hero/header logos already carry intrinsic `width`/`height` (verified — `sections/hero.liquid` sets `width`/`height` on both logo `<img>`; the header logo sizes via `image_tag`), so the residual flags are app-injected images. PERF-17 (LCP wants `fetchpriority=high`, 1 page) and PERF-18 (network dependency tree): the first hero image already sets `fetchpriority="high"`; the residual is the collection/product LCP element, where adding `fetchpriority` blind risks mis-prioritizing a `loading="lazy"` card image — browser-gated. The mission's explicit "Image & asset loading."
- **Effort:** 3/5 — theme dims/fetchpriority done; oversized/HEIC re-exports are Jenna (content); any new `fetchpriority` needs the rendered page to pick the true LCP element (browser-gated).
- **Impact:** 3/5 — Priority 3, and **field already passes** (CrUX LCP/CLS good on all golden pages), so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-6 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-5, PERF-6, PERF-7, PERF-8, PERF-12, BP-1
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (558 KB), **Route's `protect.widget.js`/`protect.core.js` (already flagged for removal in `DEVELOPMENT.md`)**, DA-Restock, free-shipping bar, portable-wallets, GA. Together they drive uncached bytes (PERF-3, 1420 KB), JS execution + main-thread + bootup (PERF-4/8), the network payload (PERF-5, 3396 KB), unused + legacy JS (PERF-7/12), the forced reflow (PERF-6), and the console errors (BP-1: `ERR_BLOCKED_BY_CLIENT`, 400/429, Monorail). **PERF-1 frames it:** mobile lab 50–62, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, **not theme files** — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-7 · Theme CSS & render path
- **Findings:** PERF-9, PERF-10, PERF-11, PERF-14, PERF-15, PERF-16
- **The system:** The theme's render path and CLS. `base.css` render-blocks ~1468 ms with component CSS behind it (PERF-10/11); unused CSS (PERF-9, 93 KB) and an unminified app-injected `RM Neue` `@font-face` (PERF-15/16); LCP element render delay 2085 ms (PERF-11); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-14 — ~4 KB). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue items are app-injected, and PERF-14 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small (28 KB render-blocking, 4 KB dup JS).
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-8 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` shipped** (verified in `theme.liquid`); the crawl reads response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no `<meta>` equivalent** — it's a response header, platform/edge-controlled on Shopify — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Search-app accessibility | 3 | 1 | 3.0 | the only unshipped, theme-authorable lever; a contained additive shim names the runtime-injected `isp_*` search box + watermark — clears the §F crawl a11y rows the mission counts |
| 2 | SYS-2 · Heading outline & aggregate | 2 | 2 | 1.0 | a11y + SEO, cascade validated (185→2); the 1 remaining error page is admin body + search-app markup (content/app) |
| 3 | SYS-3 · Image alt at scale | 4 | 4 | 1.0 | dual-priority; theme side closed (axe image-alt 4→0), meaningful alt is content |
| 4 | SYS-4 · Page metadata uniqueness | 2 | 2 | 1.0 | SEO; dup titles fixed, 5 dup descriptions remain — admin rewrites |
| 5 | SYS-5 · Image delivery & sizing | 3 | 3 | 1.0 | mission asset-loading gap; theme dims/fetchpriority done, re-exports are content |
| 6 | SYS-6 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination, app-injected |
| 7 | SYS-7 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 8 | SYS-8 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy done, Permissions-Policy platform-bound |

The shape of it: the structural heading cascade is **live, validated, and closed** (185→2), and the last two cycles' axe fixes both landed (`label-content-name-mismatch` 3→0, then `frame-title` 6→0 — golden-path axe now clean). The cycle's one remaining piece of unshipped, theme-authorable code is **SYS-1** — naming the `isp_*` search-app controls to clear the last failing *sitewide-crawl* a11y rows. Every system below it is content (Jenna/Britni: SYS-2 body, SYS-3, SYS-4, SYS-5 re-exports), an app/business decision (SYS-2 search-app markup, SYS-6 app JS), platform (SYS-8 Permissions-Policy), or a browser-gated CSS/JS slice (SYS-7).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-19** (slowest URLs) — slowest page 0.73 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95.
- **BP-3 / BP-4** (invalid / duplicate inline SVG) — "0 critical, N warning"; the duplicate is Dawn's inlined icon set — Dawn/platform-level cosmetic DOM flags. Defer. (BP-1 console errors carried under SYS-6.)
- **BP-5 / BP-6** (WebP / AVIF "support") — "0 critical, 1 warning" each; platform/CDN format flags, not a theme defect. Defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. The budget flows to **rank 1 (SYS-1)** — the whole of the unshipped, theme-authorable code this cycle. Every system below it is handed to its proven owner (content → Jenna/Britni, app/business → Mason + Jenna/Brenda, platform → Shopify support, browser-gated → a dedicated PR). After execution, re-baseline and diff the next cycle: **whether §F missing-aria-labels and a missing-image-alt sliver drop to 0** is the direct test of this fix, just as **`frame-title` 6→0** confirmed last cycle's shim.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `diff.md` — what moved vs 2026-06-23 (the frame-title shim landing: `frame-title` 6→0).
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
