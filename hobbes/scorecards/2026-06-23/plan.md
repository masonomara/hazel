# Plan — 2026-06-23

Site: https://hazelboutique.com/ · Cycle: 2026-06-23 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 33 findings, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list — nothing dropped, nothing invented. The findings are fixed; effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`.

> **What this cycle's re-measurement settles.** Last cycle shipped the re-diagnosed hero slideshow naming fix (drop the conflicting `aria-label`, un-hide the slide counter). `diff.md` confirms it landed and worked: **`label-content-name-mismatch` 3 → 0** — the "1 a11y rule improved." The hero block is closed; `sections/hero.liquid` now renders the counter with no `aria-hidden` and the slide link with no `aria-label` (verified in source). With that gone, the **single remaining failing golden-path axe audit is `frame-title`** (A11Y-1) — the Mailchimp popup's two injected iframes. That is this cycle's one theme-code lever (SYS-1).

**The strategy in one line:** the hero a11y win is banked and validated, so the one remaining failing golden-path axe audit — the Mailchimp popup frame-title — leads with a contained theme shim; everything below it is content, app-config, platform, or browser-gated.

**Three realities that shaped every rating:**
- **Field passes, lab fails — and the lab is noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages (all ✓). The 4 "field regressions" in `diff.md` are sub-millisecond / single-ms CrUX jitter (Collection LCP 0.731→0.737, Product INP 98→102) — still comfortably inside "good," not a real-user move. Meanwhile §A lab perf swings hard (Product-mobile 70→45, Home-desktop 48→41) while CrUX holds — PSI's fixed-throttle volatility over app-injected JS. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly.
- **Resource ≠ "code."** Most of this catalog is **content or app/platform**, not Liquid Hobbes can author: two admin page bodies for the heading outline (SEO-1, `{{ page.content }}`), 5 duplicate descriptions (SEO-3), meaningful per-product alt at scale (SEO-2), oversized/HEIC source files (PERF-2/5), the Mailchimp popup (A11Y-1), the **`isp_*` third-party search app** that owns every A11Y-2 sliver on `/pages/search-results`, the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe theme front is nearly exhausted — by design.** Card-image alt fallback, slideshow/pagination labels, the cart-drawer `card_heading_tag` heading cascade (185→2, banked), hero-logo dims + LCP `fetchpriority`, Referrer-Policy meta, and last cycle's hero label fix are all in `main`; the catalog still enumerates them because it measures the **live** site, which lags unpublished code. What is genuinely *both* unshipped *and* theme-authorable this cycle is exactly one thing: a contained shim that titles the Mailchimp popup iframes (SYS-1).

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Mailchimp popup frame-title
- **Findings:** A11Y-1
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less `<iframe>`s on **every page** — `#PopupSignupForm_0 > .mc-banner … > iframe` (banner) and `#PopupSignupForm_0 > .mc-modal … > iframe` (modal) — so axe's `frame-title` fails sitewide (2 nodes, 6 of 6 golden runs). The markup is **not** in the theme (`PopupSignupForm`/`mc-` appear nowhere in source — verified); the embed adds it at runtime. The clean fix is the Mailchimp embed config (add a frame title) or dropping the popup — both human-owned. But the run is GitHub-only and this is the **only failing golden-path axe audit left**, so the theme can carry a contained, additive shim: a small script that sets `title` on any untitled iframe inside `#PopupSignupForm_0` (idempotent, self-disconnecting, zero visual/behavioral change). That clears `frame-title` without waiting on app-config.
- **Effort:** 1/5 — Mason, one self-contained snippet rendered from a single line in `theme.liquid`; purely additive (only sets a missing attribute). Bucket-2: needs axe/browser confirmation at review (the popup is runtime-injected).
- **Impact:** 4/5 — Priority 1 (accessibility); clears the **only** failing golden-path axe audit, sitewide. No field caveat — naming has no lab/field split.
- **Priority:** 4 ÷ 1 = **4.0**

## SYS-2 · Heading outline — the last admin page bodies
- **Findings:** SEO-1, A11Y-2
- **The system:** The heading cascade is validated and all but closed — sitewide skipped-heading pages fell 185 → 2 once the cart-drawer `card_heading_tag` fix removed the four leading `<h3>` from the global outline (banked in `main`). What remains (SEO-1, §F: 1 multiple-H1 + 2 skipped-level) is **admin-authored page bodies**, rendered through `sections/main-page.liquid` as `<h1>{{ page.title }}</h1>` + `{{ page.content }}`:
  - **/pages/search-results** — a second `<h1>` inside the body (the §F multiple-H1 = 1) and a skipped level (crawl: "h4 after h1"). Theme renders one h1; the stray h1/h4 live in the page content **and** in the `isp_*` search-app markup (see SYS-3).
  - **/pages/sizing** — the size-chart sub-heads jump to `<h3>` with no `<h2>` between (admin rich text).
  - **A11Y-2** (sitewide prevalence, 1,716 flagged elements) rolls up here: **1,711 of 1,716** are "HTML structural" warnings — the same heading-order family — with only 3 image-alt + 1 form-label + 1 unnamed-link slivers (those tracked under SYS-3). It's an aggregate signal, not a separate fix.
- **Effort:** 2/5 — small, but **content, not code**: edit two page bodies in the admin (remove/demote the stray search-results h1; insert the missing `<h2>` on sizing). Jenna/Britni in the theme editor — the theme repo can't reach `{{ page.content }}`.
- **Impact:** 3/5 — Priority 1 + 2 (structure serves both), but only 2 of 181 pages remain; the cascade already banked the win.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Third-party search-app accessibility
- **Findings:** A11Y-2 (the non-structural slivers)
- **The system:** Every non-heading A11Y-2 sliver lives on **`/pages/search-results`** and belongs to a **third-party search app** whose elements carry the `isp_*` prefix (verified absent from the theme source): the search `<input class="isp_*" id="isp_main_search_box">` with no label (missing-form-label = 1), `<img id="isp_watermark_img">` and a sibling `<img>` with no alt (missing-image-alt = 2 of the 3), and the page's unnamed link/button. None of it is theme markup — the fix is the search app's config or template, or a decision to replace the app.
- **Effort:** 2/5 — small, but **app-owned**: search-app settings/config (the app vendor's template), not a change Mason makes in this repo. Owner: Mason to identify the app + Jenna for the config call.
- **Impact:** 2/5 — Priority 1, but off the golden path, one app on one page type, low node count.
- **Priority:** 2 ÷ 2 = **1.0**

## SYS-4 · Image alt at scale
- **Findings:** SEO-2
- **The system:** `alt` coverage across the golden pages (Home 19/43, Collection 45/88, Product 16/24 `<img>` missing alt). Two tracks: **(a) Theme — done.** The product-card featured image binds `alt` to the product title (merged); a full theme sweep confirms every live theme `<img>` carries an `alt` (the only bare one is in the fully comment-disabled `recent-viewed-product-js.liquid`, never rendered). **(b) Content + apps — open.** The remaining counts are admin product images the merchant left blank, plus app-injected widget images (Judge.me, Instafeed). SEO-2's count also includes decorative hover images correctly `alt=""`.
- **Effort:** 4/5 — theme side shipped (a 1); meaningful alt across the catalog is the cost (client content at scale, ongoing) — Jenna/Britni.
- **Impact:** 4/5 — dual priority (a11y + SEO); dampened because the theme defect is closed and the residue is partly decorative-by-design.
- **Priority:** 4 ÷ 4 = **1.0**

## SYS-5 · Page metadata uniqueness
- **Findings:** SEO-3
- **The system:** 5 sets of duplicate meta descriptions (SEO-3) — "Hazel Boutique" ×5, a repeated 18 oz candle spec ×4, repeated EVI11 vintage copy ×4/×2, a bracelet line ×2. (Duplicate **titles** are gone — `diff.md`: 4 → 0, fixed in admin last cycle; only descriptions remain.) Distinguishing near-identical product/collection pages is bespoke copy, not a theme mechanism: the templated head fallback already gives every page *a* description; making genuinely-similar pages *unique* is admin rewrites — Jenna/Britni.
- **Effort:** 2/5 — no code; ~9 admin description rewrites, Jenna/Britni.
- **Impact:** 2/5 — Priority 2, but bounded and the golden-path SEO score already reads 100.
- **Priority:** 2 ÷ 2 = **1.0**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-14, PERF-18
- **The system:** Images are the heaviest payload class and the mobile-LCP driver — oversized product JPEGs (350/257/234 KB, PERF-2) and **HEIC source files served raw** (the 78/51 KB `.heic` in PERF-2) need re-exporting to WebP/AVIF at sane dimensions (Jenna's assets). PERF-14 (unsized images) and PERF-18 (LCP wants `fetchpriority=high`): the theme hero/header logos already carry intrinsic `width`/`height` (verified — both hero-logo `<img>` set width/height; the header logo sizes via `image_tag`) and the first hero image already sets `fetchpriority="high"` (shipped). The residual flags are app-injected images and the collection/product LCP element, where adding `fetchpriority` blind risks mis-prioritizing a `loading="lazy"` card image — browser-gated. The mission's explicit "Image & asset loading."
- **Effort:** 3/5 — theme code done; oversized/HEIC re-exports are Jenna (content); any new `fetchpriority` needs the rendered page to pick the true LCP element (browser-gated).
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-5, PERF-6, PERF-8, PERF-13, PERF-17, BP-1
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB), **Route's `protect.widget.js`/`protect.core.js` (already flagged for removal in `DEVELOPMENT.md`)**, DA-Restock, free-shipping bar, portable-wallets, GA. Together they drive uncached bytes (PERF-3), JS execution + main-thread + bootup time (PERF-4/8), the network payload (PERF-5), unused + legacy JS (PERF-6/13), an unminified app script (PERF-17), and the console errors (BP-1: `ERR_BLOCKED_BY_CLIENT`, 400/429, Monorail). **PERF-1 frames it:** mobile lab 45–63, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, **not theme files** — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & layout-shift path
- **Findings:** PERF-7, PERF-9, PERF-10, PERF-11, PERF-12, PERF-15, PERF-16, PERF-19
- **The system:** The theme's render path and CLS. `base.css` render-blocks ~901 ms with component CSS behind it (PERF-11/19); unused CSS (PERF-9, 93 KB) and an unminified app-injected `RM Neue` `@font-face` (PERF-16); a forced reflow in app + page JS (PERF-7); CLS culprits + large shifts on the cart/logo/Mailchimp (PERF-10/12); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-15 — ~4 KB). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, the CLS culprits are app/cart widgets, and PERF-15 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7 (28 KB render-blocking, 4 KB dup JS).
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` shipped** (verified in `theme.liquid`); the crawl reads response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no `<meta>` equivalent** — it's a response header, platform/edge-controlled on Shopify — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Mailchimp popup frame-title | 4 | 1 | 4.0 | Priority-1 a11y; the only failing golden-path axe audit and the one unshipped theme-authorable lever — a contained shim that titles the injected iframes |
| 2 | SYS-2 · Heading outline (last admin pages) | 3 | 2 | 1.5 | a11y + SEO, cascade validated (185→2); the 2 remainders live in admin page bodies (content) |
| 3 | SYS-3 · Third-party search-app a11y | 2 | 2 | 1.0 | all A11Y-2 slivers are `isp_*` search-app markup on /pages/search-results — app-config |
| 4 | SYS-4 · Image alt at scale | 4 | 4 | 1.0 | dual-priority; theme side closed (axe image-alt 4→0), meaningful alt is content |
| 5 | SYS-5 · Page metadata uniqueness | 2 | 2 | 1.0 | SEO; dup titles fixed (4→0), 5 dup descriptions remain — admin rewrites |
| 6 | SYS-6 · Image delivery & sizing | 3 | 3 | 1.0 | mission asset-loading gap; theme dims/fetchpriority done, re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination, app-injected |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy done, Permissions-Policy platform-bound |

The shape of it: the structural heading cascade is **live, validated, and closed** (185→2), and last cycle's hero a11y fix landed (`label-content-name-mismatch` 3→0). The cycle's one remaining piece of unshipped, theme-authorable code is **SYS-1** — titling the Mailchimp popup iframes to clear the last failing golden-path axe audit. Every system below it is content (Jenna/Britni: SYS-2, SYS-4, SYS-5, SYS-6 re-exports), an app/business decision (SYS-3 search app, SYS-7 app JS), platform (SYS-9 Permissions-Policy), or a browser-gated CSS/JS slice (SYS-8).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-20** (slowest URLs) — slowest page 0.53 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95.
- **BP-3 / BP-4** (invalid / duplicate inline SVG) — "0 critical, N warning"; the duplicate is Dawn's `icon-plus` inlined 6× — Dawn/platform-level cosmetic DOM flags. Defer. (BP-1 console errors carried under SYS-7.)
- **BP-5 / BP-6** (WebP / AVIF "support") — "0 critical, 1 warning" each; platform/CDN format flags, not a theme defect. Defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. The budget flows to **rank 1 (SYS-1)** — the whole of the unshipped, theme-authorable code this cycle. Every system below it is handed to its proven owner (content → Jenna/Britni, app/business → Mason + Jenna/Brenda, platform → Shopify support, browser-gated → a dedicated PR). After execution, re-baseline and diff the next cycle: **whether A11Y-1 `frame-title` drops off 2 nodes** is the direct test of this fix, just as **`label-content-name-mismatch` 3→0** confirmed last cycle's hero fix.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `diff.md` — what moved vs 2026-06-22 (the hero label fix landing: `label-content-name-mismatch` 3→0).
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
