# Plan — 2026-06-22 (budget-100 continuation)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

> This is the **budget-100 continuation** of the 2026-06-22 cycle, run against the re-measured data (35 findings, crawl/PSI re-run at 19:17 CDT). The first 2026-06-22 pass (PR #16) shipped the hero slide-link `aria-label` fix and **explicitly deferred the heading-hierarchy system** because it could not pin, blind, *which* early-DOM element emits the leading `<h3>` run — "pinning which early-DOM element emits those `h3`s needs the rendered page." This run did that diagnosis from source. The heading system is no longer browser-gated; it is the cycle's clean code win, and it leads.

The 35 findings, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** the re-diagnosed heading-outline root — one clean, source-grounded theme-code fix — leads, because it is dual-priority and sitewide; then the rest of the a11y/SEO front (mostly merged or human-owned), then the performance work where CrUX already passes for real users.

**Three realities that shaped every rating:**
- **Field passes, lab fails — and the lab fell as noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages; `diff.md` shows **0 field regressions** vs 2026-06-21. The lab perf scores fell hard this cycle (Home-mobile 65→41, Product-desktop 87→77, Collection-mobile 75→52) — but the §A 3-run spreads are wide (Home-mobile 41/41/60, Product-mobile 45/48/59) and CrUX held, so that is PSI's fixed-throttle volatility over app-injected JS, not a real-user move. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content or app/platform**, not Liquid Hobbes can author: duplicate collection titles (SEO-3), duplicate/templated descriptions (SEO-4), meaningful per-product alt at scale (SEO-2), oversized/HEIC source files to re-export (PERF-2/5), the Mailchimp embed (A11Y-2), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe code front is largely shipped — and one prior heading call is now disproven by data.** Slideshow/pagination labels, card-image alt fallback, meta-description + OG/Twitter, hero-logo dims + LCP `fetchpriority`, Referrer-Policy meta, the hero slide-link `strip_html` fix (PR #16), and last cycle's card-**product**-grid `h3→h2` + stray product `h1→h2` are all in `main`; the findings still enumerate them because the catalog measures the **live** site, which lags the unpublished code. **But the data refutes last cycle's heading call** (see SYS-1): the card-product fix shipped — `diff.md` confirms multiple-H1 dropped 2→1, same PR — yet skipped-level held flat at 185/185 for three cycles. The root was misattributed. Re-tracing it from source is this run's win.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Heading hierarchy & document outline
- **Findings:** SEO-1, A11Y-3
- **The system:** One structural root, sitewide — re-found this run because the data killed last cycle's call. Last cycle blamed the collection product-grid `h1→h3` skip for the 185-page skipped-level count and shipped a card-product `h3→h2` fix. That fix is partly live (`diff.md`: multiple-H1 2→1, the same PR's stray product `h1→h2`), **yet skipped-level held flat at 185/185 across 06-20, 06-21, 06-22.** A fix that moved one row of its PR but not this one means the root was misattributed. Traced from source this run:
  - **The real root is a global four-`<h3>` run before every page's `<h1>`.** The skip flags on all 185 pages, including non-collection pages — `/`, `/pages/sizing`, `/blogs/news` all open `h3 → h3 → h3 → h3 → h1 …` (SEO-1 evidence). So it is rendered on *every* page, not the collection grid. `layout/theme.liquid:482` renders `cart-drawer` globally; its **empty-cart state** (the crawler's state) renders two promo collections — `settings.cart_drawer_collection` + `..._two` (`cart-drawer.liquid:106,114`) — and **`card-collection.liquid` emits two `<h3 class="card__heading">` per card when a featured image is present** (the always-on heading at `:111` *and* the card-style heading at `:134`). Two collections × two `<h3>` = the **exact four leading `<h3>`** in every page's outline, before the page `<h1>` → "first heading isn't h1" + skipped level, on all 185 pages.
  - **A11Y-3**'s 1,756 sitewide "HTML structural" warnings are the same outline family, measured at element scale.
- **The fix (this run's code):** mirror the proven card-product pattern — add a backward-compatible `card_heading_tag` param to `card-collection.liquid` (default `'h3'` → the other three callers, `collage`/`collection-list`/`main-list-collections`, are byte-identical), and have the **cart drawer** pass `card_heading_tag: 'div'` so its off-canvas empty-cart promo cards stop injecting headings into the global outline. Safe by construction: all CSS targets the `.card__heading` **class** (never `h3.card__heading`), no JS references it (both verified), and the clickable "SHOP {title}" link keeps the accessible name. Promo links in an empty-cart drawer genuinely aren't page headings.
- **Effort:** 2/5 — Mason, theme code: one snippet param + one caller edit, an already-proven pattern, no `settings_data.json`. Higher confidence than last cycle because the root is traced to source, not inferred. The only thing Hobbes can't do is run the crawl/axe in a browser — the human's gate at review.
- **Impact:** 5/5 — Priority 1 (a11y outline) **and** Priority 2 (SEO) at once; the single largest cascade in the cycle — the universal skipped-level root on 185/185 pages. No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 2 = **2.5**

## SYS-2 · Theme accessibility controls (label mismatch)
- **Findings:** A11Y-1
- **The system:** The mobile hero slide links built their `aria-label` from `block.settings.heading | escape`; on an `inline_richtext` heading carrying markup, `escape` pushed tag literals into the accessible name so it no longer matched the visible rendered text → `label-content-name-mismatch` (3 nodes, Home — mobile). **The `strip_html` fix shipped in PR #16 and is in `main`** (`sections/hero.liquid:59`); byte-identical for plain headings, cannot regress. The 3 nodes still in A11Y-1 are the pre-publish live state.
- **Effort:** 2/5 — Mason, theme code, one self-contained snippet edit. Done; awaits publish + re-measure.
- **Impact:** 4/5 — Priority 1, removes a failing axe audit on the golden path. No field caveat.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-3 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less iframes on **every page** (`#PopupSignupForm_0`) → `frame-title` fails everywhere (2 nodes, 6 runs). Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), a wrapper, or a product decision to drop the popup (a marketing call).
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access or a marketing decision, not a change Mason makes in this repo.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also remove.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-4 · Image alt text
- **Findings:** SEO-2
- **The system:** Two tracks, two owners. **(a) Theme fallback** — the product-card featured image binds `alt` to the admin alt with a `card_product.title` fallback (shipped/merged), so every card image has a meaningful name even when admin alt is blank. **(b) Meaningful alt at scale** — per-image content work in admin, owned by Jenna/Britni. SEO-2's golden counts (19/43 Home, 45/88 Collection, 16/24 Product) are partly the **decorative hover image** (hardcoded `alt=""`), which is *correctly* empty — so the headline coverage number overstates the real gap.
- **Effort:** 3/5 — theme fallback shipped (a 2); meaningful alt across the catalog is a 5 (client content, ongoing).
- **Impact:** 4/5 — dual priority (a11y + SEO); dampened because the headline coverage counts are partly the decorative-by-design hover image.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-5 · Page metadata — duplicate titles & descriptions
- **Findings:** SEO-3, SEO-4
- **The system:** The discoverability layer's remaining gap is **content, not code** — the templated head defaults (meta-description fallback chain, OG/Twitter) already shipped. What's left: **4 duplicate titles** (SEO-3 — "New Arrivals", "Tops", "Dresses", "Under $50" each ×2: two collections sharing a name) and **9 duplicate descriptions** (SEO-4 — "Hazel Boutique" ×5, templated "Shop X at Hazel Boutique." pairs, repeated product copy). **Watch item:** the templated `"Shop X at Hazel Boutique." ×2` duplicates are the **now-live fallback chain** doing its job — every page *has* a description; the generic fallback is just identical across same-named collections. Not a defect — they clear only when those collections get distinct, bespoke copy in admin (Jenna/Britni).
- **Effort:** 3/5 — no code; admin renames + bespoke copy at modest scale (13 strings).
- **Impact:** 3/5 — Priority 2; real but bounded — 13 strings across a few collections/products, not a sitewide cascade.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-17, PERF-18
- **The system:** Images are the heaviest payload class and the LCP driver on throttled mobile. **(a) Theme code — shipped/merged:** the hero-logo intrinsic dimensions (PERF-18) and the LCP hero `fetchpriority="high"` (PERF-17). **(b) Content — open:** oversized product images (PERF-2 2,363 KB / PERF-5 3,408 KB; 234–667 KB each) and **HEIC source files served raw** (`*.heic`, 78–183 KB) need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. This is the mission's explicit "Image & asset loading."
- **Effort:** 3/5 — code done; content re-exports are Jenna's, at catalog scale.
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-6, PERF-8, PERF-12, PERF-16, PERF-19, BP-1
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB), **Route's `protect.widget.js`/`protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, free-shipping bar, portable-wallets, GA, a legacy-JS transpile (PERF-12), an unminified app script (PERF-16). Together they drive uncached bytes (PERF-3), execution/main-thread/bootup time (PERF-4/8), unused JS (PERF-6), critical-request chains (PERF-19), and the console-error count (BP-1). **PERF-1 frames it:** mobile lab 41–52, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, not theme files — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS, critical path & layout shift
- **Findings:** PERF-7, PERF-9, PERF-10, PERF-11, PERF-13, PERF-14, PERF-15, BP-4
- **The system:** The theme's render path and CLS. `base.css` render-blocks ~1,201 ms with a chain of component CSS behind it (PERF-10); unused CSS incl. an app `RM Neue`/Bootstrap bundle (PERF-9, 93 KB); a forced reflow in app + page JS (PERF-7); an unminified app-injected `RM Neue` `@font-face` (PERF-15); CLS culprits + large shifts on the home hero/logo/newsletter (PERF-11/13); two theme JS modules (`quick-add.js`, `product-form.js`) duplicated across coexisting sections (PERF-14, 4 KB); duplicate inline SVG (BP-4). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, and PERF-14 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate this run can't run.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` were unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` is shipped/merged**; the crawl reads HTTP response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no meta equivalent** — platform/edge-controlled — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy meta done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Heading hierarchy & outline | 5 | 2 | 2.5 | a11y + SEO at once; re-diagnosed the universal skipped-level root (cart-drawer `card-collection` double-`h3` on 185/185 pages) — the prior pass's deferred system, now clean theme code |
| 2 | SYS-2 · Theme a11y controls (label) | 4 | 2 | 2.0 | Priority-1 a11y; hero slide-link `strip_html` fix shipped (PR #16), in `main` |
| 3 | SYS-3 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 4 | SYS-4 · Image alt text | 4 | 3 | 1.33 | dual-priority; theme fallback merged, meaningful alt is content |
| 5 | SYS-5 · Page metadata (dup copy) | 3 | 3 | 1.0 | SEO; 13 duplicate strings, all admin content |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; code merged, heavy/HEIC re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path & CLS | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy merged, Permissions-Policy platform-bound |

The shape of it: **ranks 2, 4, 6 and rank 9's code are already merged into `main`**, awaiting only the human publish. The cycle's one genuinely-new *unshipped theme code* is the **SYS-1 outline fix** — the system the prior 2026-06-22 pass deferred as "needs the rendered page." Re-tracing the root from source turned a flat, three-cycle-stuck 185/185 finding into a clean, contained, high-leverage win, and it tops the order on its own merits. The rest of every system is content (SYS-4/5/6), app/business decisions (SYS-3, SYS-7), platform (Permissions-Policy), or a browser-gated CSS/JS slice (SYS-8).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-20** (slowest URLs) — slowest page 0.77 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced (2 runs); revisit only if Best Practices must reach 95.
- **BP-3** (invalid inline SVG), **BP-5 / BP-6** (WebP/AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Defer. (BP-1 console errors carried under SYS-7; BP-4 duplicate inline SVG under SYS-8.)

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. Ranks 2, 4, 6 and rank-9 code are already merged (awaiting publish), so the budget flows to **rank 1 (SYS-1 heading outline)** — the top of the order *and* the only unshipped, safely-authorable theme code. Every other system's non-code part is handed to its owner. After execution, re-baseline and diff the next cycle: **whether skipped-level finally moves off 185** is the direct test of this re-diagnosis.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
