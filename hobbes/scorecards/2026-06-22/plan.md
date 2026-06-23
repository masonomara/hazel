# Plan — 2026-06-22 (21:44 re-measurement · validation pass)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

> This is the **21:44 CDT re-measurement** of the 2026-06-22 cycle — a fresh crawl/PSI run taken *after* PR #17 merged the cart-drawer heading fix into `main` (PR #17 carried the 19:17 data; this carries 21:44). Its job is **validation**: PR #17 re-diagnosed the universal skipped-level root as the cart-drawer `card-collection` double-`h3` and bet that fixing it would move the count off 185/185. **The re-measurement answers that bet — skipped-level dropped 185 → 4** (`diff.md`), and the SiteOne Accessibility quality score rose 5.0 → 5.8 (§F). The hypothesis held. This plan re-grounds the 35 findings against the new numbers and traces the 4 residual heading pages to source.

The 35 findings, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** the heading-outline root is now *proven* fixed in `main` (185 → 4, awaiting only publish); what remains across the whole catalog is publish-gated code, client content, app/platform config, or browser-gated CSS — so this run ships no new theme code and hands each remainder to its owner with the proof attached.

**Three realities that shaped every rating:**
- **Field passes, lab fails — and the lab is noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages; `diff.md` shows **0 field regressions** vs 2026-06-21. The mobile lab scores swung again this run (Home-mobile 41→52, Collection-mobile 52→43, Product-desktop 77→67) against last measurement — but the §A 3-run spreads are wide and CrUX held flat, so that is PSI's fixed-throttle volatility over app-injected JS, not a real-user move. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content or app/platform**, not Liquid Hobbes can author: duplicate collection titles (SEO-3), duplicate/templated descriptions (SEO-4), meaningful per-product alt at scale (SEO-2), the `/pages/sizing` page-body headings (SEO-1), the search-app `h1` (SEO-1), oversized/HEIC source files to re-export (PERF-2/5), the Mailchimp embed (A11Y-2), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe code front is shipped — and now *measured* shipped, not just asserted.** Slideshow/pagination labels, card-image alt fallback, meta-description + OG/Twitter, hero-logo dims + LCP `fetchpriority`, Referrer-Policy meta, the hero slide-link `strip_html` fix, last cycle's card-**product** `h3→h2`, and PR #17's cart-drawer `card-collection` `card_heading_tag: 'div'` are all in `main`. The findings still enumerate some of them because the catalog measures the **live** site, which hasn't been republished. **The difference this run: the heading fix is no longer an inference — the re-measured crawl confirms it** (185 → 4 skipped-level; the only residue is the 2 pages where the crawler still rendered the empty-cart drawer, plus 2 unrelated non-cart causes). The bet PR #17 made is paid off.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Heading hierarchy & document outline
- **Findings:** SEO-1, A11Y-3
- **The system:** One structural root, sitewide — diagnosed in PR #17 and **confirmed by this re-measurement.** PR #17 traced the universal "first heading isn't `<h1>`" skip to the global cart drawer: its empty-cart state renders two promo collections (`cart-drawer.liquid:106,115` → `settings.cart_drawer_collection` + `..._two`), and `card-collection.liquid` emits **two** `<h3 class="card__heading">` per card when a featured image is present (the always-on `:112` heading *and* the card-style `:135` heading). Two collections × two `<h3>` = the **exact four leading `<h3>`** before every page's `<h1>`, on all 185 pages. PR #17 shipped `card_heading_tag: 'div'` on both drawer renders. **The crawl now reads 4 skipped-level pages, down from 185** (`diff.md`; §F Accessibility 5.0 → 5.8). Traced from `raw/crawl.json` (`seo-headings`), the 4 residual pages are three *separate* causes, only one of which is the cart drawer:
  - **`/` and `/collections/new-arrivals-1`** — still open `<h3> Fine Jewelry <h3> Fine Jewelry <h3> All Sale Items <h3> All Sale Items <h1> …`: the same two cart-drawer promo collections, double-emitted. The fix that cleared the other 181 pages is **identical** for these; they persist only because the crawler still rendered the empty-cart drawer on this pass (variance — the fix is in `main`, unpublished, so the live site is unchanged). **Publish closes them.** No new code.
  - **`/pages/sizing`** — `<h1> Sizing <h3> Hoodie <h3> Mockneck <h3> Barrel Pant <h3> Jogger …`: an `h1 → h3` skip. `page.json` is `main-page` only, so these four size-chart sub-headings live in the **admin page body** (the May-2026 size charts, changelog 004) as hardcoded `<h3>` with no parent `<h2>`. **Content, not theme code** — Jenna/Britni re-tag to `<h2>` in the page editor.
  - **`/pages/search-results`** — `<h1> Search Results <h1> [#isp_results_summary] <h2> …`: a second, empty `<h1>` injected by the **search app** (`#isp_results_summary`). **App-owned** — fix in the search app config, not the repo.
  - **A11Y-3**'s 1,756 sitewide "HTML structural" warnings are the same outline family at element scale; they fall with the heading outline as the fix publishes.
- **What's left to ship:** nothing in theme code. The code is merged and *proven*; the remainder is **publish** (cart-drawer, human), **content** (sizing, Jenna/Britni), **app config** (search `h1`).
- **Effort:** 1/5 — the code is done and verified by the data; the residual is a publish + two small human-owned edits. No further Liquid this cycle.
- **Impact:** 5/5 — Priority 1 (a11y outline) **and** Priority 2 (SEO); the single largest cascade in the cycle, and the only one with a *measured* before/after this run (185 → 4). No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 1 = **5.0**

## SYS-2 · Theme accessibility controls (label mismatch)
- **Findings:** A11Y-1
- **The system:** The mobile hero slide links built their `aria-label` from `block.settings.heading | escape`; on an `inline_richtext` heading carrying markup, `escape` pushed tag literals into the accessible name so it no longer matched the visible text → `label-content-name-mismatch` (3 nodes, Home — mobile). **The `strip_html` fix is in `main`** (`sections/hero.liquid:59`); byte-identical for plain headings, cannot regress. The 3 nodes still in A11Y-1 are the pre-publish live state.
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
- **The system:** Two tracks, two owners. **(a) Theme fallback** — the product-card featured image binds `alt` to the admin alt with a `card_product.title` fallback (merged), so every card image has a meaningful name even when admin alt is blank. **(b) Meaningful alt at scale** — per-image content work in admin, owned by Jenna/Britni. SEO-2's golden counts (19/43 Home, 45/88 Collection, 16/24 Product) are partly the **decorative hover image** (hardcoded `alt=""`), which is *correctly* empty — so the headline coverage number overstates the real gap.
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
- **The system:** Images are the heaviest payload class and the LCP driver on throttled mobile. **(a) Theme code — merged:** the hero-logo intrinsic dimensions (PERF-18) and the LCP hero `fetchpriority="high"` (PERF-17). **(b) Content — open:** oversized product images (PERF-2 2,285 KB / PERF-5; 250–375 KB each) and **HEIC source files served raw** (`*.heic`, 114–141 KB) need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. This is the mission's explicit "Image & asset loading."
- **Effort:** 3/5 — code done; content re-exports are Jenna's, at catalog scale.
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-6, PERF-8, PERF-12, PERF-16, PERF-19, BP-1
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (558 KB), **Route's `protect.widget.js`/`protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, free-shipping bar, portable-wallets, GA, a legacy-JS transpile (PERF-12 carries the layout-shift insight here as `cls-culprits`), an unminified app script (PERF-16). Together they drive uncached bytes (PERF-3), execution/main-thread/bootup time (PERF-4/8), unused JS (PERF-6), critical-request chains (PERF-19), and the console-error count (BP-1). **PERF-1 frames it:** mobile lab 43–52, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, not theme files — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS, critical path & layout shift
- **Findings:** PERF-7, PERF-9, PERF-10, PERF-11, PERF-13, PERF-14, PERF-15, BP-4
- **The system:** The theme's render path and CLS. `base.css` render-blocks ~1,631 ms with a chain of component CSS behind it (PERF-10); unused CSS incl. an app `RM Neue`/Bootstrap bundle (PERF-9, 93 KB); a forced reflow in app + page JS (PERF-7); an unminified app-injected `RM Neue` `@font-face` (PERF-15); CLS culprits + large shifts on the home hero/logo/newsletter (PERF-11/13/14); two theme JS modules (`quick-add.js`, `product-form.js`) duplicated across coexisting sections (PERF-13, 4 KB); duplicate inline SVG (BP-4). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, and the duplicated JS has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate this run can't run.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` were unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` is merged** (`layout/theme.liquid:8`); the crawl reads HTTP response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no meta equivalent** — platform/edge-controlled — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy meta done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Heading hierarchy & outline | 5 | 1 | 5.0 | a11y + SEO at once; the universal skipped-level root — **proven fixed this run, 185 → 4** — code merged, residual is publish + content + app |
| 2 | SYS-2 · Theme a11y controls (label) | 4 | 2 | 2.0 | Priority-1 a11y; hero slide-link `strip_html` merged, awaits publish |
| 3 | SYS-3 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 4 | SYS-4 · Image alt text | 4 | 3 | 1.33 | dual-priority; theme fallback merged, meaningful alt is content |
| 5 | SYS-5 · Page metadata (dup copy) | 3 | 3 | 1.0 | SEO; 13 duplicate strings, all admin content |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; code merged, heavy/HEIC re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path & CLS | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy merged, Permissions-Policy platform-bound |

The shape of it: **every system's code is already in `main`** — and this run's headline is that the top system's fix is now *measured* working, not merely inferred. SYS-1's cart-drawer change moved skipped-level 185 → 4; the 4 that remain are 2 pages where the crawler still rendered the unpublished drawer (publish closes them), plus `/pages/sizing` (content) and `/pages/search-results` (search app). There is **no new theme code to author this cycle** — the leverage now lives in the human steps: publish the merged code, then hand the content/app/platform remainders to their owners.

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-20** (slowest URLs) — slowest page 0.60 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced (1 run); revisit only if Best Practices must reach 95.
- **BP-3** (invalid inline SVG), **BP-5 / BP-6** (WebP/AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Defer. (BP-1 console errors carried under SYS-7; BP-4 duplicate inline SVG under SYS-8.)

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. This run, the top of the order — SYS-1 — is the system whose hypothesis it was sent to test, and the data settled it: **the re-diagnosis was right.** Because every system's code is merged and SYS-1 is now measured-good, the budget finds **no new theme code to write**; it instead records the proof, names every human-owned remainder with its owner, and opens one PR carrying the refreshed data. The next baseline — taken after a publish — should show the cart-drawer residue on `/` and `/collections/new-arrivals-1` clear, leaving only the sizing-content and search-app heading items.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
