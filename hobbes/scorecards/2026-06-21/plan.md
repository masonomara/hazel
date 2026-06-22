# Plan — 2026-06-21

Site: https://hazelboutique.com/ · Cycle: 2026-06-21 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 39 findings of this cycle, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) and the high-leverage structural cascade go first; the discoverability layer (priority 2) next; the expensive performance work — where CrUX already passes for real users — waits behind the cheap theme-code wins.

**Three realities that shaped every rating:**
- **Field passes, lab fails.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages. `diff.md` since 2026-06-20 is noise — two INP wobbles (Home 103→105, Product 96→98) and small LCP improvements. The mobile Lighthouse 65–75 is PSI's fixed-throttle lab, not real users. So every performance system serves the *lab-score* target (mission §3, "≥ 90") far more than a real shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content**, not Liquid — 76 pages needing descriptions, duplicate collection titles to rename, every product image needing meaningful alt, oversized/HEIC source files to re-export — owned by Jenna/Britni in admin, not Mason. Effort names the resource, because "Mason ships a snippet" and "Jenna writes 76 descriptions" are different costs.
- **The a11y code front is already written.** `diff.md` shows `label-content-name-mismatch` 11→3 — the 2026-06-20 PR (nested-heading, slideshow/pagination labels, card-image alt fallback) is merged into `main` and verified-pending-publish. The findings below still enumerate those a11y rules because the **live site** hasn't been republished; the catalog measures live, not `main`. This is the plan's grouping regardless; **execution** owns the "already-in-main" accounting.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-2 · Heading hierarchy & document structure
- **Findings:** A11Y-3, A11Y-5, SEO-2
- **The system:** One structural root, sitewide. `snippets/card-product.liquid` renders the product-card title; the nested heading-in-heading (`<h3><h3>…</h3></h3>`) that drove **A11Y-3** (heading-order) and the bulk of **A11Y-5**'s ~1,758 sitewide "HTML structural" warnings (every card multiplied it) was fixed in the 2026-06-20 PR — the title is now `<h3><span class="full-unstyled-link">`. That code is in `main`; A11Y-3/A11Y-5 persist in this catalog only because the live site predates publish. What **remains** is the deeper **SEO-2** outline failure that the snippet fix does *not* clear: 185 pages flag a skipped heading level (card grids emit h3s before the page's h1; sections jump h1→h3 with no h2), and 2 pages carry multiple h1 (Home = header-logo h1-on-index + a section h1; /pages/search-results). The header logo is already correctly `<h1>`-on-index only (`sections/header.liquid:176/200/216/240`), so the multi-h1 is a per-page section-heading question, and the skipped-levels are a site-wide heading-level reorder. Both change visible heading hierarchy and **must be verified in the browser** — they are not a blind snippet edit.
- **Effort:** 2/5 for the shipped nested-heading fix (done); the remaining outline reorder is a **4** on its own — Dawn-layout-touching, needs per-section heading-level decisions and visual verification. Blended down because the high-frequency cascade is already banked.
- **Impact:** 5/5 — Priority 1 (a11y) *and* Priority 2 (SEO) at once; the single largest cascade in the cycle (one snippet touched every card on 185 pages). No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 2 = **2.5**

## SYS-1 · Theme accessibility controls
- **Findings:** A11Y-1
- **The system:** Two theme-owned `label-content-name-mismatch` defects, both pure markup. (1) **Hero slideshow** (`sections/hero.liquid:59/104`) — the mobile-hero slide link's `aria-label` and the decorative "00N" counter span. (2) **Pagination** (`snippets/pagination.liquid:37/43/54`) — the zero-padded visible "08" vs an unpadded "Page 8" accessible name. **Both fixes are in `main` from the 2026-06-20 PR** (aria-label now defaults to the heading + counter `aria-hidden`; pagination computes one padded `page_label` for both the label and the visible text). `diff.md` confirms the drop 11→3 nodes. The 3 nodes still in A11Y-1 are the pre-publish live state.
- **Effort:** 2/5 — Mason, theme code, two self-contained snippet edits. Done; awaits publish.
- **Impact:** 4/5 — Priority 1, removes failing axe audits on the golden path (Home-mobile, Collection desktop+mobile). No field caveat.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup (`PopupSignupForm_0`, `mc-banner` / `mc-modal`) injects two `about:blank`, title-less iframes on **every page** (all 6 runs) → `frame-title` fails everywhere. Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), wrapping the embed, or a product decision to drop the popup (a marketing call → Brenda/Jenna). It must clear to reach a11y 100, because it's on every page.
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access to the Mailchimp embed or a marketing decision, not a change Mason makes in this repo. Medium confidence — depends on what the embed exposes.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also just remove. Necessary-but-small for the a11y-100 target.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Image alt text
- **Findings:** A11Y-4, SEO-3
- **The system:** The site's image-alt debt, two tracks with two owners. **(a) Theme fallback** — the product-card featured image (`snippets/card-product.liquid:89`) now binds `alt="{{ ...alt | default: card_product.title | escape }}"` (shipped 2026-06-20, in `main`), so every card image has a meaningful name even when the admin alt is blank. **(b) Meaningful alt at scale** — the quality the a11y standing-requirement and the manual pass actually want — is per-image content work in admin, owned by Jenna/Britni. SEO-3's golden counts (19/44 Home, 45/89 Collection) are partly the **decorative hover image** (`:112`, hardcoded `alt=""`), which is *correctly* empty — chasing that coverage number to zero would announce every product twice. **A11Y-4**'s single missing-alt node is a bare `<img>` (no srcset/sizes/class) that does **not** match card-product's output — likely an app- or custom-injected image; its source must be identified in the browser at review, not assumed.
- **Effort:** 3/5 — blended. The theme fallback (a 2) is shipped; meaningful alt across the catalog is a 5 (client content, ongoing). Resource is **code (done) *and* client content (open)**.
- **Impact:** 4/5 — dual priority (A11y §1 + the SEO checklist's "all images have alt", failing on all three golden pages). Dampened from a 5 because the headline coverage counts are partly the decorative-by-design hover image.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-5 · Page metadata — descriptions, titles, Open Graph
- **Findings:** SEO-1, SEO-4, SEO-5, SEO-6
- **The system:** The discoverability layer on collection/page templates, and the highest-leverage **unshipped** code in the cycle. **76 pages** have no meta description (SEO-1 — mostly collections, policies, system pages); the head only emits `<meta name="description">` when the admin set one (`layout/theme.liquid:25`), so the fix is a **templated fallback** in the head — collection description → a generated "Shop {title} at {shop}" line → product/page/article content → shop description. **43 pages plus golden Home lack a full OG/Twitter set** (SEO-4 — Home missing `og:image`); `snippets/meta-tags.liquid:22` only emits `og:image` when `page_image` exists and ships **no `twitter:image` at all**, so the fix is an image fallback (`page_image` → a new `share_image` setting → `settings.logo`) plus the missing `twitter:image`. Both are pure Mason theme code that auto-fills the bulk and passes the checklist. The remainder is content: 4 duplicate titles (SEO-5 — "Tops", "Dresses", "Under $50", "New Arrivals" collections) and 4 duplicate descriptions (SEO-6 — templated vintage/candle copy) are admin renames/rewrites (Jenna/Britni), not code.
- **Effort:** 3/5 — the templated head defaults are a quick, high-confidence Mason win covering the bulk; the duplicate-title renames and bespoke copy are content. Code + content.
- **Impact:** 4/5 — Priority 2 (discoverability), 76+ pages, and it moves the SEO-checklist items (meta description, OG) holding the golden-path SEO score under 95. Serves the mission's "discoverable" directly.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-12, PERF-14, PERF-17, BP-3
- **The system:** Images are the heaviest payload class and the LCP driver on the throttled mobile runs. Two tracks. **(a) Theme code** — the two brand logos in the hero-logo block (`sections/hero.liquid:194/202`, `script-logo.png` 4335×531, `hazel-mobile-logo.png` 1053×438) ship with invalid `width="100%" height="auto"` attributes → unsized (PERF-12) and aspect-ratio-mismatch (BP-3); and the LCP hero image carries no `fetchpriority` (PERF-14). All Mason, self-contained. **(b) Content** — oversized product images (234–667 KB each, PERF-2/5) and **HEIC source files served raw** (`image_*.heic`, a phone-camera format browsers handle poorly) need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. PERF-17 (network dependency tree) is largely app-script chaining, tracked under SYS-7. This is the mission's explicit "Image & asset loading — confirm consistent loading site-wide."
- **Effort:** 3/5 — code for logo dims + LCP `fetchpriority` (low, high-confidence); content for the heavy/HEIC re-exports (Jenna).
- **Impact:** 3/5 — Priority 3, and **field already passes** (real-user LCP is fine), so the lab lever is real but the real-user gain is small. Held above the other perf systems because the mission names asset loading as a gap and big images cost mobile shoppers real bytes.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-7, PERF-8, PERF-9, PERF-11, PERF-16, BP-1, BP-4
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB, the single biggest resource and largest unused-JS block at 392 KB), Fera reviews (`fera.js`; also the source of the BP-1 "Error fetching recommendations 422" console error), **Route's `protect.widget.js` / `protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, the free-shipping bar, portable-wallets, GA, and a deprecated API (BP-4). Together they drive uncached bytes (PERF-3), execution and main-thread time (PERF-4/8), unused + legacy JS (PERF-7/11), an unminified app script (PERF-16), unused app CSS (PERF-9), and the console-error count that holds Best Practices down (BP-1). **PERF-1 is the landscape that frames this whole system:** mobile lab 65–75, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route, where the decision is already made), defer/async the rest.
- **Effort:** 4/5 — the biggest coordination cost in the cycle. Each app is a business decision (Route is a revenue feature, Fera is reviews, the free-shipping bar is merchandising), so it's app-config + Jenna/Britni/Brenda coordination + test-each-removal, not a change Mason makes alone in the theme repo.
- **Impact:** 3/5 — Priority 3 and the single biggest *lab* lever, but **field passes** so real users are already fine; the gain is the lab score plus a cleaner Best-Practices score from killing console errors. Removing Route also banks an existing mission decision. Dampened by the field reality.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical path
- **Findings:** PERF-6, PERF-10, PERF-13, PERF-15
- **The system:** The theme's own render path. `base.css` render-blocks for ~1,051 ms with a chain of component CSS behind it (PERF-6); there's a forced reflow in app + page JS (PERF-10), an unminified `RM Neue` `@font-face` block (PERF-15, app-injected), and two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across sections (PERF-13 — 4 KB). The shippable theme piece (CSS deferral, JS-include dedup) is small in bytes and **fiddly on a Dawn fork** — deferring base.css risks above-the-fold FOUC, and pulling a `quick-add`/`product-form` script tag risks breaking quick-add or the product form. Every change here needs careful mobile + desktop browser verification.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a Dawn fork and the JS dedup touches core commerce paths; needs the browser gate. Pure Mason, no content/apps.
- **Impact:** 2/5 — Priority 3, field passes, and the numbers are small next to SYS-7 (47 KB render-blocking, 4 KB duplicated JS). Real but minor.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset (SEC-1). HSTS and CSP — the two that mattered most — now pass (baseline §F). On Shopify-hosted Advanced, response headers are largely platform-controlled: a theme **can** set `Referrer-Policy` via a `<meta name="referrer">` tag in the head (a real, shippable fix), but `Permissions-Policy` has **no meta equivalent** — it must come from the platform/edge, so it's a confirm-and-escalate, not a theme change.
- **Effort:** 2/5 — the Referrer-Policy meta is a one-line head edit; Permissions-Policy is investigation only. Low code, partial coverage.
- **Impact:** 1/5 — security is not a mission priority (the mission is a11y / SEO / perf), and these are the lower-severity pair. Lowest leverage in the cycle.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-2 · Heading hierarchy & structure | 5 | 2 | 2.5 | one snippet fix cascaded across every card on 185 pages; a11y + SEO at once (cascade shipped 06-20; outline reorder remains) |
| 2 | SYS-1 · Theme a11y controls | 4 | 2 | 2.0 | Priority-1 a11y; two pinned label-mismatch bugs (shipped 06-20) |
| 3 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 4 | SYS-3 · Image alt text | 4 | 3 | 1.33 | dual-priority; theme fallback shipped 06-20, meaningful alt is content |
| 5 | SYS-5 · Page metadata | 4 | 3 | 1.33 | SEO checklist + 76 pages; templated head defaults cover the bulk — top unshipped code |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; field passes, so a lab-side gain; logo dims + LCP code |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy shippable, Permissions-Policy platform-bound |

The shape of it: **ranks 1–4 are accessibility** (mission priority 1) and their theme code is already in `main` from the 2026-06-20 PR. **Rank 5 is SEO** (priority 2) — the top of the *unshipped* code, and the natural anchor of this cycle's PR. **Ranks 6–8 are performance** (priority 3), held back not because the numbers are small but because CrUX already passes, so they buy a lab score more than a faster store. Security sits last.

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding is accounted for, none silently dropped.

- **PERF-18** (slowest URLs) — the slowest page responds in 0.54 s, every URL under 1 s and 200. Server response is healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none are credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced in the audit; revisit only if Best Practices must reach 95.
- **BP-5 / BP-6 / BP-7 / BP-8** (invalid / duplicate inline SVG, WebP / AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Low value, defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar before moving on. Ranks 1–4 are accessibility and **already code-complete in `main`** (awaiting the human publish), so the budget flows to **rank 5 (page metadata) and the code halves of rank 6 (image delivery) and rank 9 (Referrer-Policy)** — all theme code, no content or app dependency, shippable without waiting on anyone. The verification-bound (SYS-8, SYS-2 reorder) and human-owned (SYS-4, SYS-7) systems are deferred with reasons. After execution, re-baseline and diff the next cycle against this one: closed findings and any regressions tell you whether the plan worked.
