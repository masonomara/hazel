# Plan — 2026-06-22

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The **36 findings** of this cycle, grouped into **10 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) first; discoverability (priority 2) next; the expensive performance work — where CrUX already passes for real users — waits behind the cheap, certain theme-code wins.

**Three realities that shaped every rating — each verified against the source, not assumed:**

- **Field passes, lab "regressed" but didn't.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages. `diff.md` vs 2026-06-21 shows **0 field regressions**. The lab perf scores fell across the board (Home desktop 86→56, Product desktop 87→70, Collection mobile 75→51) — but that is PSI's fixed-throttle lab volatility, not a real-user move: CrUX held and the §A 3-run spreads are wide (Product mobile 50/50/69). The trustworthy signal says nothing got worse for shoppers. What genuinely improved this cycle is the **a11y/SEO front**: heading-order 1→0 and image-alt 4→0 on the golden axe pass, sitewide missing meta descriptions **76→0**, multiple-H1 **2→1**, golden SEO **92→100** on all three pages.

- **Most of the safe theme code is already in `main`, awaiting publish — I verified this in the source, I did not take it on faith.** The meta-description fallback chain (`layout/theme.liquid:27–47`), OG/Twitter tags (`snippets/meta-tags.liquid`), the Referrer-Policy `<meta>` (`layout/theme.liquid:8`), the card-image alt fallback (`snippets/card-product.liquid:93`), the JS-rendered image alt on the footer "Recently viewed" grid (`sections/footer.liquid:140–141`) and the cart-drawer upsell (`snippets/cart-drawer.liquid:35`), and the hero LCP `fetchpriority="high"` (`sections/hero.liquid:98,182`) are **all present in `main` right now**. The crawl and PSI still enumerate these as open because they measure the **live** site, and the live theme lags `main` until a human publishes. Those findings clear on publish, not on more code.

- **The one finding a prior pass assumed was handled is, in fact, still broken in `main` — and it is the cycle's real code win.** Re-reading the live source against `findings.md` surfaced **A11Y-1**: the mobile hero slide links still build their `aria-label` from `block.settings.heading | escape` (`sections/hero.liquid:59`). On an `inline_richtext` heading carrying markup, `escape` pushes tag literals into the accessible name, so it no longer contains the visible rendered text → `label-content-name-mismatch`, 3 nodes on Home — mobile. This is genuinely new, unshipped, and clean to fix. It is rank 1.

- **Resource ≠ "code."** A large share of this catalog is **content or platform**, not Liquid Hobbes can author: 4 duplicate collection titles (SEO-3), 9 duplicate descriptions (SEO-4), meaningful per-product alt at scale (SEO-2), oversized/HEIC source files to re-export (PERF-2), the per-section `heading_size` choices in admin-generated JSON that drive the homepage outline (SEO-1), the Mailchimp embed (A11Y-2), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Theme accessibility control — hero slide-link name
- **Findings:** A11Y-1
- **The system:** The mobile hero (`sections/hero.liquid`) renders each slide as an `<a>` whose accessible name comes from `aria-label="{{ block.settings.heading | default: 'View slide' | escape }}"` (line 59), while the same heading is the link's **visible** text inside `.textyText` (line 106). `heading` is an `inline_richtext` field — when a merchant adds any markup (a `<strong>`, a line break), `escape` renders that markup as literal tag text *into the accessible name*, which then no longer contains the plain visible text → axe `label-content-name-mismatch`. Three slides, three nodes, exactly matching A11Y-1's count on Home — mobile. The desktop hero link (lines 124–138) carries **no** `aria-label` and does not fire — confirming the defect is isolated to the mobile `aria-label`. The fix aligns the accessible name with the visible text: `strip_html` the heading before it becomes the label, so the name is the same plain text the user sees.
- **Effort:** 1/5 — Mason; one filter added to one line, no markup/layout/behavior touched, cannot regress (for a plain-text heading the output is byte-identical to today's). The only thing Hobbes cannot do is run axe in a browser to confirm the rule clears — that is the human's gate at review.
- **Impact:** 4/5 — Priority 1 (accessibility), on the golden path's most-visited page, clears all 3 live A11Y-1 nodes. No field caveat — structure/semantics have no lab/field split.
- **Priority:** 4 ÷ 1 = **4.0**

## SYS-3 · Heading hierarchy & document structure
- **Findings:** SEO-1, A11Y-3
- **The system:** One structural root, sitewide — the bulk of A11Y-3's 1,756 HTML-structural warnings are heading-order. Three distinct sources, none a clean blind edit:
  - **Homepage multiple-H1** (still 1 page in §F) — the header ships three CSS-toggled logo `<h1>` variants (`sections/header.liquid:185/225/381`) plus per-section `heading_size: "h1"` choices that live in admin-generated `index.json`/`settings_data.json` (`DEVELOPMENT.md` forbids hand-editing those). A merchant-settings + rendered-DOM question.
  - **The leading `h3 → h3 → h3 → h3 → h1` pattern** that opens nearly every page's outline (SEO-1 evidence). The document's first heading is an `h3`, not the page `<h1>`. A real sitewide skip, but pinning *which* early-DOM element emits those `h3`s needs the rendered page — not a guess.
  - **`/pages/sizing` and `/pages/search-results`** — a second `<h1>` inside merchant rich-text / a custom page. Content/template owner, confirm in browser.
- **Effort:** 3/5 — merchant `heading_size` settings (Jenna, in the editor) + a browser-DOM diagnosis pass; not authorable blind here without a browser to verify no visual/layout regression.
- **Impact:** 5/5 — Priority 1 (a11y) *and* Priority 2 (SEO) at once; the single largest cascade in the cycle (185 pages). No field caveat.
- **Priority:** 5 ÷ 3 = **1.67**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less iframes (`#PopupSignupForm_0`) on **every page** → `frame-title` fails sitewide (6 runs). Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), a wrapper, or a product decision to drop the popup (a marketing call).
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access or a marketing decision, not a change in this repo.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also remove.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-5 · Page metadata — duplicate titles & descriptions
- **Findings:** SEO-3, SEO-4
- **The system:** The discoverability gap left after the metadata code went live. **4 duplicate titles** (SEO-3: Tops, Dresses, Under $50, New Arrivals — two collections each) and **9 duplicate descriptions** (SEO-4) are admin renames/rewrites. **Watch item:** SEO-4 now shows `"Shop New Arrivals at Hazel Boutique." ×2`, `"Hazel Boutique" ×5`, etc. — that is the **templated fallback chain (now live)** doing its job: every page now *has* a description, but the generic fallback is identical across same-named collections. Not a defect — the fallback is correct — the duplicates only clear when those collections get distinct, bespoke titles/descriptions.
- **Effort:** 3/5 — no code to write; bespoke copy + collection renames are content (Jenna/Britni).
- **Impact:** 4/5 — Priority 2; the duplicate-title/description rows are what hold §F's SEO score under a clean pass.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-13, PERF-19
- **The system:** Images are the heaviest payload class and the LCP driver on throttled mobile. **(a) Theme code — already in `main`:** the hero LCP `fetchpriority="high"` on the first slide (PERF-19, `hero.liquid:98,182`) is shipped and awaits publish. **(b) Content — open:** oversized product images (234–375 KB) and **HEIC source files served raw** (`image_*.heic`, 114–183 KB; PERF-2) need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. This is the mission's explicit "Image & asset loading." **(c) Browser-gated:** PERF-13 (unsized-images) flags `hazel-mobile-logo.png` + alt "Hazel Boutique"; the theme's header logo (`image_tag`, `header.liquid:194`) and hero logo (`hero.liquid:204–211`) both already carry explicit `width`/`height`, so the flagged instance must be pinned in the rendered DOM before any edit — not blind-authorable.
- **Effort:** 3/5 — code done; content re-exports are Jenna; PERF-13 needs a browser to localise.
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-2 · Image alt text — meaningful alt at scale
- **Findings:** SEO-2
- **The system:** The "is the alt *meaningful*" content gap. The **code** that emits a fallback `alt` on every theme-rendered image is already in `main` — `card-product.liquid:93` (`… | default: card_product.title | escape`), the footer recently-viewed JS grid (`footer.liquid:140–141`, `alt="${item.productTitle}"`), and the cart-drawer upsell (`cart-drawer.liquid:35`, `alt="${product.title}"`); the decorative hover image is correctly `alt=""` (`card-product.liquid:116`). What remains in SEO-2's golden counts (19/43 Home, 45/88 Collection, 16/24 Product) is partly that correctly-empty decorative image and partly **admin image-alt only Jenna/Britni can author per product**.
- **Effort:** 5/5 — client content at scale, ongoing; no code left to write.
- **Impact:** 4/5 — Priority 1 *and* 2, but the code slice is already banked; the residual is the content tail.
- **Priority:** 4 ÷ 5 = **0.8**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-5, PERF-6, PERF-7, PERF-12, PERF-20, BP-1, BP-2
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB), **Route's `protect.widget.js`/`protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, free-shipping bar, portable-wallets, GA, plus a console-error/inspector trail (BP-1/BP-2). Together they drive uncached bytes (PERF-3), total payload (PERF-4), execution + main-thread time (PERF-5/PERF-7), unused + legacy JS (PERF-6/PERF-12), and network chaining (PERF-20). **PERF-1 frames it:** mobile lab 50–70, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, not theme files — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical render path
- **Findings:** PERF-8, PERF-9, PERF-10, PERF-11, PERF-14, PERF-15, PERF-16, PERF-17, PERF-18
- **The system:** The render path. `base.css` render-blocks ~1,473 ms with a chain of component CSS behind it (PERF-10); the LCP element-render-delay dominates the breakdown (PERF-11, 2,072 ms); unused CSS incl. an app `RM Neue`/Bootstrap bundle (PERF-9); CLS culprits + large layout shifts on the newsletter/country-code block (PERF-8/PERF-16); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-14 — 4 KB); a forced reflow (PERF-15); and app-injected unminified CSS/JS (PERF-17/PERF-18). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC; the RM Neue/reflow/minify items are app-injected; PERF-14 has **no clean Liquid cross-section dedup** (sections can't share state) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1, SEC-2
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` is already in `main`** (`layout/theme.liquid:8`) — the crawl reads HTTP response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no meta equivalent** — platform/edge-controlled — so it's confirm-and-escalate (Shopify support), not a theme change. SEC-2 (`Access-Control-Allow-Origin: *`) is on public CDN assets where `*` is expected and benign.
- **Effort:** 2/5 — Referrer-Policy meta done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair.
- **Priority:** 1 ÷ 2 = **0.5**

## SYS-10 · Image-format & inline-SVG best practices (sitewide cosmetic)
- **Findings:** BP-3, BP-4, BP-5, BP-6
- **The system:** SiteOne's sitewide best-practice flags — invalid inline SVG (BP-3, 10 warnings), duplicate inline SVG (BP-4, 1), and WebP/AVIF "support" (BP-5/BP-6, 1 each). All **"0 critical, N warning"** — Dawn/platform-level cosmetic markers, no user-facing defect. Inline-SVG dedup via `<use>` is a broad Dawn-core change with poor return; the WebP/AVIF flags are about Shopify's CDN format negotiation, not theme code.
- **Effort:** 2/5 — broad, low-value Dawn-core edits.
- **Impact:** 1/5 — not a mission priority; cosmetic warnings only.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Hero slide-link a11y name | 4 | 1 | 4.0 | **the cycle's one new, clean, unshipped theme-code win** — strips markup from the mobile hero `aria-label` so it matches the visible text; clears all 3 live A11Y-1 nodes |
| 2 | SYS-3 · Heading hierarchy & structure | 5 | 3 | 1.67 | a11y + SEO at once, 185 pages — but homepage multi-h1 + leading-h3 root + page-content h1 are merchant settings + a browser-DOM question |
| 3 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config / drop decision) |
| 4 | SYS-5 · Page metadata | 4 | 3 | 1.33 | duplicate titles/descriptions; the fallback code is live, the renames + bespoke copy are content |
| 5 | SYS-6 · Image delivery & sizing | 3 | 3 | 1.0 | mission asset-loading gap; LCP code in `main`, heavy/HEIC re-exports are content, PERF-13 browser-gated |
| 6 | SYS-2 · Meaningful alt at scale | 4 | 5 | 0.8 | code slice already in `main`; residual is per-product admin alt (content) |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy meta in `main`, Permissions-Policy platform-bound |
| 10 | SYS-10 · SVG/image-format BP | 1 | 2 | 0.5 | cosmetic sitewide warnings; broad Dawn-core change, poor return |

The shape of it: **rank 1 (SYS-1) is the only genuinely-new, clean, source-grounded theme code this cycle** — and it is the fix a prior pass wrongly assumed was already merged. Most other code (metadata, OG/Twitter, Referrer-Policy meta, card/JS image alt, hero fetchpriority) is **already in `main`, awaiting the human publish**; the rest is content (Jenna/Britni), app/business decisions (SYS-4, SYS-7), platform (Permissions-Policy), browser-gated CSS/JS (SYS-8), or a rendered-DOM question (SYS-3, PERF-13).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-21** (slowest URLs) — slowest page 0.71 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave. (Grouped under SYS-9.)
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95. (Grouped under SYS-7.)
- **BP-3 / BP-4 / BP-5 / BP-6** (invalid/duplicate inline SVG, WebP/AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. (Grouped under SYS-10.)

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. Ranks 2–10 are either already merged into `main` (awaiting publish), content, app/business decisions, platform-bound, or browser-gated — so the budget flows to **rank 1 (SYS-1)**: the top of the *unshipped, safely-authorable* code, and a fix no current `main` code touches. Every other system's non-code part is handed to its owner. After execution, re-baseline and diff the next cycle: closed findings and any regressions tell you whether the plan worked.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
