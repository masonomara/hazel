# Plan — 2026-06-22

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 37 findings of this cycle, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) goes first; the discoverability layer (priority 2) next; the expensive performance work — where CrUX already passes for real users — waits behind the cheap theme-code wins. Same shape as 2026-06-21, because the catalog is near-identical — but this cycle's *new* unshipped theme code is a different fix.

**Three realities that shaped every rating:**
- **Field passes, lab fails — and the publish moved the field.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages. `diff.md` vs 2026-06-21 shows **0 field regressions** and the publish landing: sitewide missing meta descriptions **76 → 0**, multiple-H1 **2 → 1**, golden SEO **92 → 100** on Home + Collection. So PRs #10/#11 (metadata) are now **live**. The mobile lab dropped (Collection mobile 75 → 45) but that is PSI's fixed-throttle lab volatility (the 3-run spread was 45/45/75), not a real-user regression — CrUX held.
- **Resource ≠ "code."** A large share of this catalog is **content**, not Liquid — 4 duplicate collection titles to rename (SEO-3), 9 duplicate descriptions to rewrite (SEO-4), every product image needing meaningful alt (SEO-2), oversized/HEIC source files to re-export (PERF-2/5), and the per-section `heading_size` choices that drive the homepage outline (SEO-1). All owned by Jenna/Britni in admin, not Mason. Effort names the resource.
- **Most of the a11y/SEO/security code front is shipped — split between live and merged-awaiting-publish.** PRs #10/#11 (metadata, OG/Twitter, Referrer-Policy, hero-logo dims, LCP fetchpriority) are **live** (the diff proves it). PR #8 (slideshow/pagination labels, nested-heading, card-image alt fallback) and PR #12 (collection card `h3→h2`, stray product `h1→h2`) are **merged into `main` but not yet published** — so the crawl, which measures the **live** site, still enumerates those rules (A11Y-1, A11Y-3, SEO-1's collection share). The genuinely *new, unshipped* theme code this cycle is **SYS-1's JS-rendered image-alt gap** — never touched by any prior PR.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Image alt text
- **Findings:** A11Y-4, SEO-2, A11Y-5 (image portion)
- **The system:** Theme-rendered images that ship with **no `alt` attribute**, plus the catalog-wide "is the alt meaningful" content gap. Two tracks, two owners.
  - **(a) Theme code — the new win, unshipped.** PR #8 added an alt fallback to `snippets/card-product.liquid` (the Liquid-rendered card). But the theme **also builds product cards in JavaScript template-literals**, and those were never touched: the **"Recently viewed" block** (`sections/footer.liquid:140–141`, injected on every page) and the **cart-drawer "Wear it with" upsell** (`snippets/cart-drawer.liquid:46,97`). All four emit `<img>` with no `alt`. This is exactly **A11Y-4** — its evidence node (`<img src="…/IMG-1767.jpg?v=1711642495" loading="lazy" width="1200">`, no alt) matches the footer recently-viewed output byte-for-byte (same `image_url`-no-size src, same `loading="lazy" width="1200"`). The product title is already in scope in each template (`item.productTitle`, `firstRecommendedProduct.title`), so a meaningful alt is a pure attribute addition.
  - **(b) Meaningful alt at scale — content.** SEO-2's golden counts (19/43 Home, 45/88 Collection, 16/24 Product) are partly the **decorative hover image** (hardcoded `alt=""`, *correctly* empty) and partly admin image-alt that only Jenna/Britni can author per product.
- **Effort:** 2/5 for the **code slice** — Mason, four attribute additions across two self-contained JS-template blocks, zero visual change. (Meaningful alt across the catalog is a 5 — client content, ongoing; rated separately as the content tail.)
- **Impact:** 4/5 — Priority 1 (a11y) *and* Priority 2 (SEO coverage); the code slice closes the live **A11Y-4** node and trims **A11Y-5**'s sitewide unnamed-image count. Dampened only because the headline coverage numbers are partly the decorative-by-design hover image.
- **Priority (code slice):** 4 ÷ 2 = **2.0**

## SYS-3 · Theme accessibility controls
- **Findings:** A11Y-1
- **The system:** Two theme-owned `label-content-name-mismatch` defects — the hero slideshow slide link's `aria-label` and the pagination zero-padded label. **Shipped and merged in PR #8.** The 3 nodes still in A11Y-1 are the pre-publish live state; the fix is in `main`, awaiting publish.
- **Effort:** 2/5 — Mason, theme code, done; awaits publish.
- **Impact:** 4/5 — Priority 1, removes failing axe audits on the golden path. No field caveat.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-2 · Heading hierarchy & document structure
- **Findings:** A11Y-3, SEO-1, A11Y-5 (structural portion)
- **The system:** One structural root, sitewide. The product-card nested-heading and the collection-grid `h1→h3` skip — the bulk of SEO-1's 185-page count — were fixed in **PR #8** (`card-product.liquid` `<h3><span>`) and **PR #12** (collection cards `h3→h2` under the page `<h1>`, via the backward-compatible `card_heading_tag` parameter; stray product-page `h1→h2`). Both **merged into `main`, not yet published** — so SEO-1 still enumerates them live. What **remains** beyond the merged code:
  - **Homepage multiple-H1** (still 1 page in §F) — rooted in per-section `heading_size: "h1"` choices in admin-generated `index.json`/`settings_data.json` (visual size classes, not real `<h1>`s) plus the header's three CSS-toggled logo-`<h1>` variants (`header.liquid:177/217/373`). A merchant-settings + browser-DOM question, **not** a clean blind edit.
  - **The leading `h3 → h3 → h3 → h3 → h1` pattern** that opens nearly every page's outline (SEO-1 evidence). The document's first heading is an `h3`, not the page `h1` — a real sitewide skip, but its source is a DOM-order question (which early-DOM element emits those `h3`s) that needs the rendered page to pin down, not a guess.
  - **`/pages/sizing` and `/pages/search-results`** — page-content `<h1>` misuse (a second `<h1>` inside merchant rich-text / a custom page). Content/template owner, confirm in browser.
- **Effort:** 3/5 — the high-leverage code is merged (Mason); the remainder is merchant `heading_size` settings (Jenna) + browser-DOM confirmation, not authorable blind here.
- **Impact:** 5/5 — Priority 1 (a11y) *and* Priority 2 (SEO) at once; the single largest cascade in the cycle. No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 3 = **1.67**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less iframes on **every page** → `frame-title` fails sitewide. Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), a wrapper, or a product decision to drop the popup (a marketing call → Brenda/Jenna).
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access or a marketing decision, not a change Mason makes in this repo.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also remove.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-5 · Page metadata — duplicate titles & descriptions
- **Findings:** SEO-3, SEO-4
- **The system:** The remaining discoverability gap after the metadata code went live. **4 duplicate titles** (SEO-3: Tops, Dresses, Under $50, New Arrivals — two collections each) and **9 duplicate descriptions** (SEO-4) are admin renames/rewrites (Jenna/Britni). **Watch item:** SEO-4 now shows `"Shop New Arrivals at Hazel Boutique." ×2`, `"Shop Under $50…" ×2`, etc. and `"Hazel Boutique" ×5` — these are the **templated fallback chain shipped in PRs #10/#11** doing its job (every page now *has* a description), but the generic fallback is identical across same-titled collections and bare on description-less pages. Not a defect — the fallback is correct — but the duplicates only clear when Jenna gives those collections distinct titles/descriptions.
- **Effort:** 3/5 — no code to write; bespoke copy + collection renames are content (Jenna/Britni).
- **Impact:** 4/5 — Priority 2; the duplicate-title/description checklist items are what hold §F's SEO score under a clean pass.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-12, PERF-17
- **The system:** Images are the heaviest payload class and the LCP driver on throttled mobile. **(a) Theme code — shipped/live (PRs #10/#11):** the hero-logo intrinsic dimensions (PERF-12) and the LCP hero `fetchpriority="high"` (PERF-17). PERF-12 now flags only a residual `hazel-mobile-logo.png` instance — confirm post-publish whether one logo render still lacks dims. **(b) Content — open:** oversized product images (234–667 KB, PERF-2/5) and **HEIC source files served raw** (`image_*.heic`, 114–183 KB) need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. This is the mission's explicit "Image & asset loading."
- **Effort:** 3/5 — code done; content re-exports are Jenna.
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-7, PERF-9, PERF-11, PERF-16, PERF-18, BP-1, BP-3
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (558 KB), Fera (`fera.js`, also the BP-1 422 "Error fetching recommendations" console error), **Route's `protect.widget.js`/`protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, free-shipping bar, portable-wallets, GA, a deprecated API (BP-3). Together they drive uncached bytes, execution/main-thread time, unused+legacy JS, an unminified app script, network chaining, and the console-error count. **PERF-1 frames it:** mobile lab 45–86, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, not theme files — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical path
- **Findings:** PERF-6, PERF-8, PERF-10, PERF-13, PERF-14, PERF-15
- **The system:** The theme's render path. `base.css` render-blocks ~1,351 ms with a chain of component CSS behind it (PERF-6); a forced reflow in app + page JS (PERF-8); unused CSS incl. an app `RM Neue`/Bootstrap bundle (PERF-10); a CLS culprit on the newsletter/country-code block (PERF-13); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-14 — 4 KB); and an unminified app-injected `RM Neue` `@font-face` (PERF-15). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC; the RM Neue/reflow items are app-injected; PERF-14 has **no clean Liquid cross-section dedup** (sections can't share state; a global include regresses onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1, SEC-2
- **The system:** `Referrer-Policy` and `Permissions-Policy` were unset (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` is shipped/merged** (PRs #10/#11) — awaiting publish to clear in the crawl. `Permissions-Policy` has **no meta equivalent** — platform/edge-controlled — so it's a confirm-and-escalate (Shopify support), not a theme change. SEC-2 (`Access-Control-Allow-Origin: *`) is on public CDN assets where `*` is expected and benign.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Image alt text | 4 | 2 | 2.0 | **the cycle's one new, clean, unshipped theme-code win** — JS-rendered card images (recently-viewed + cart upsell) get a meaningful `alt`; closes live A11Y-4 |
| 2 | SYS-3 · Theme a11y controls | 4 | 2 | 2.0 | Priority-1 a11y; two label-mismatch bugs — shipped+merged PR #8, awaiting publish |
| 3 | SYS-2 · Heading hierarchy & structure | 5 | 3 | 1.67 | a11y + SEO at once; collection `h1→h3` + stray `h1` merged (PR #12); remainder is merchant settings + DOM |
| 4 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 5 | SYS-5 · Page metadata | 4 | 3 | 1.33 | duplicate titles/descriptions; code halves live, the renames+copy are content |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; code live, heavy/HEIC re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy merged, Permissions-Policy platform-bound |

The shape of it: **rank 1 (SYS-1 code slice) is the only genuinely-new, clean, source-grounded theme code this cycle.** Ranks 2, 3 (code), 6 (code), 9 (code) are already merged into `main` (PRs #8/#10/#11/#12) awaiting only the human publish; everything else is content (Jenna/Britni), app/business decisions (SYS-4, SYS-7), platform (Permissions-Policy), browser-gated CSS/JS (SYS-8), or a DOM question (SYS-2's homepage/leading-h3 remainder).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-19** (slowest URLs) — slowest page 0.50 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave. (Grouped under SYS-9.)
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95.
- **BP-4 / BP-5 / BP-6 / BP-7** (invalid/duplicate inline SVG, WebP/AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. Ranks 2, 3 (code), 6 (code) and rank-9 code are already merged (awaiting publish), so the budget flows to **rank 1 (SYS-1 image alt)** — the top of the *unshipped* code, and a fix no prior PR touched. The SYS-2 remainder (homepage multi-h1, leading-h3 root, page-content h1) and every other system's non-code part are handed to their owners. After execution, re-baseline and diff the next cycle: closed findings and any regressions tell you whether the plan worked.
