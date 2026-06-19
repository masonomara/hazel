# Plan — 2026-06-18

Site: https://hazelboutique.com/ · Cycle: 2026-06-18 · Authored by Hobbes from `findings.md` + `baseline.md` + `raw/`.

The 41 findings of this cycle, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) and the high-leverage cascades go first; the expensive performance work — where CrUX already passes for real users — waits behind the cheap wins.

**Two realities that shaped every rating:**
- **Field passes, lab fails.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages. The mobile Lighthouse scores of 52–65 are the fixed-throttle lab, not real users. So every performance system serves the *lab-score* target (mission §3, "≥ 90") far more than it serves a real user — and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content**, not Liquid — 1127 images needing alt, 76 pages needing descriptions — owned by Jenna/Britni in admin, not Mason. Effort names the resource, because "Mason ships a snippet" and "Jenna writes 76 descriptions" are different costs.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Theme accessibility controls
- **Findings:** A11Y-1, A11Y-2, A11Y-4
- **The system:** Three Dawn components, each shipping one accessibility defect, all theme-owned and fixable in Liquid/CSS with no content or app dependency. (1) **A11Y-1** — the hero slideshow slide links (`slideshow__slide`) carry an aria-label that doesn't contain their visible text → `label-content-name-mismatch`, 7 nodes across Home + Collection. (2) **A11Y-2** — the product media-zoom toggle buttons (`product__media-toggle`) have no accessible name → `button-name`, 5 nodes on Product; this is the main reason Product's a11y score sits at **88**, the lowest on the board. (3) **A11Y-4** — the sold-out price text (`price-item--sold-out`) fails WCAG AA contrast — a CSS-token value, not markup. Different components, one body of work: Dawn-component a11y, shipped together in a single upgrade-safe pass.
- **Effort:** 2/5 — Mason, theme code/CSS, self-contained. aria-label on the slide links and the media toggles; one contrast token for the sold-out price. No content, no app, no Dawn-core risk; selectors and snippets are already in the findings. High confidence.
- **Impact:** 5/5 — Priority 1, the standing accessibility requirement. Directly lifts the golden-path a11y score toward the mission's 100, with `button-name` the single biggest score drag. No field caveat — a11y has no lab/field split.
- **Priority:** 5 ÷ 2 = **2.5**

## SYS-2 · Heading hierarchy
- **Findings:** A11Y-5, SEO-2
- **The system:** One cascading root, sitewide. Every page's outline opens `h2 → h3 → h3 … → h1` because the **cart drawer** renders its headings (Your cart / Estimated total / recently-viewed card titles) into the DOM *before* the page's own h1 — so all 185 crawled pages report skipped-heading errors and Home shows 2 h1. **A11Y-5** is the same disease on the collection card (`card__heading h5` rendered as an h3 with no h2 parent). Fix the drawer's heading levels once (demote to non-heading markup or correct the level) and fix the card heading level once, and the error clears across the whole site — the largest page-count cascade in the cycle, spanning both SEO (single-H1 / heading checklist) and A11y (document outline).
- **Effort:** 2/5 — Mason, theme code, two self-contained snippets (cart-drawer template, card heading). Minor investigation to confirm the drawer is the emitter — the findings' heading trees already point at it — and care not to restyle the drawer. No content, no apps.
- **Impact:** 4/5 — one fix, 185 pages, two priorities (SEO §2 + A11y §1). Per-page severity is modest (skipped headings don't kill rankings), but the cascade breadth and dual-domain reach make it high-leverage; also clears the SEO checklist's single-H1 item on Home.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-3 · Image alt text
- **Findings:** A11Y-6, A11Y-7, SEO-3
- **The system:** The site's single largest accessibility debt — **1127 images flagged without alt sitewide** (A11Y-7), the golden Product card image (A11Y-6), and 20/45 Home, 44/88 Collection, 16/25 Product images missing alt (SEO-3). Two tracks, two resources: **(a)** a theme fallback — bind `alt` to the image's set alt or the product title in the card/media `<img>` snippets — is a quick Liquid change that drops the coverage count and passes the automated "all images have alt" check; **(b)** meaningful alt at scale — the quality the a11y standing-requirement and the manual pass actually want — is per-image content work, owned by Jenna/Britni in admin. Ship (a) this cycle; open (b) as ongoing content. Execution must not mistake the fallback for "done."
- **Effort:** 3/5 — blended. The theme fallback alone is a 2; meaningful alt across 1127 images is a 5 (client content, ongoing). Resource is **code *and* client content**.
- **Impact:** 5/5 — largest a11y volume in the catalog, dual priority (A11y §1 + the SEO checklist's "all images have alt", failing on all three golden pages).
- **Priority:** 5 ÷ 3 = **1.67**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-3
- **The system:** The Mailchimp signup popup (`PopupSignupForm_0`, `mc-banner` / `mc-modal`) injects two title-less iframes on **every page** (all 6 runs) → `frame-title` fails everywhere. Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a title), wrapping the embed, or a product decision to drop the popup (a marketing call → Brenda/Jenna). It must clear to reach a11y 100, because it's on every page.
- **Effort:** 2/5 — small, but app-config + a decision rather than pure code. Medium confidence: depends on what Mailchimp's embed exposes.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also just remove. Necessary-but-small for the a11y-100 target.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-5 · Page metadata — descriptions, titles, Open Graph
- **Findings:** SEO-1, SEO-4, SEO-5, SEO-6
- **The system:** The discoverability layer on collection/page templates. **76 pages** have no meta description (SEO-1 — mostly collections, policies, system pages), 5 share a duplicate description (SEO-6 — templated vintage/candle copy), 4 share a duplicate title (SEO-5 — e.g. "Dresses", "Tops" collections), and 43 pages plus golden Home lack a full OG/Twitter set (SEO-4 — Home missing `og:image`). Mixed resource: a **templated default** (collection description → meta description; a `theme.liquid` `og:image` fallback) is code that auto-fills the bulk and passes the checklist; unique copy for the top collections and the duplicate-title renames are admin/content (Jenna/Britni).
- **Effort:** 3/5 — template defaults are a quick Mason win that covers most of it; bespoke copy for key collections and the title renames are content. Code + content.
- **Impact:** 4/5 — Priority 2 (discoverability), 76+ pages, and it moves the SEO-checklist items (meta description, OG) holding the golden-path SEO score under 95. Serves the mission's "discoverable" directly.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-12, PERF-14, BP-2
- **The system:** Images are the heaviest payload class and the LCP driver on the throttled mobile runs. Oversized product images (350–667 KB each), **HEIC source files served raw** (`image_*.heic` — a phone-camera format browsers handle poorly, that should be re-exported to WebP/AVIF), the logo shipped unsized (PERF-12) and at the wrong aspect ratio (BP-2), and the LCP image neither `fetchpriority=high` nor discoverable from HTML (PERF-14). Mixed resource: theme `<img>` work (logo dims, LCP `fetchpriority`, responsive `sizes`) is Mason; re-exporting the HEIC and oversized originals is content (Jenna's assets). This is the mission's explicit "Image & asset loading — confirm consistent loading site-wide."
- **Effort:** 3/5 — code for dims/fetchpriority/sizes (moderate); content for the heavy/HEIC re-exports (Jenna).
- **Impact:** 3/5 — Priority 3, and **field already passes** (real-user LCP is fine), so the lab lever is real but the real-user gain is small. Nudged above the other perf systems because the mission names asset loading as a gap and big images cost mobile shoppers real bytes.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-7, PERF-8, PERF-9, PERF-11, PERF-16, BP-1, BP-4
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (560 KB, the single biggest resource and largest unused-JS block at 392 KB), Fera reviews (`fera.js`; also the source of the BP-1 "Error fetching recommendations 422" console error), **Route's `protect.widget.js` / `protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, the free-shipping bar, portable-wallets, GA, and a deprecated WPM script (BP-4). Together they drive uncached bytes (PERF-3), execution and main-thread time (PERF-4/9), unused + legacy JS (PERF-7/11), forced reflow (PERF-8), and the console-error count that holds Best Practices down (BP-1). **PERF-1 is the landscape that frames this whole system:** mobile lab 52–65, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route, where the decision is already made; investigate what `shopify.widget.js` actually is and whether it's removable), defer/async the rest.
- **Effort:** 4/5 — the biggest coordination cost in the cycle. Each app is a business decision (Route is a revenue feature, Fera is reviews, the free-shipping bar is merchandising), so it's app-config + Jenna/Britni/Brenda coordination + test-each-removal, not a change Mason makes alone.
- **Impact:** 3/5 — Priority 3 and the single biggest *lab* lever, but **field passes** so real users are already fine; the gain is the lab score plus a cleaner Best-Practices score from killing console errors. Removing Route also banks an existing mission decision. Dampened by the field reality.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical path
- **Findings:** PERF-6, PERF-10, PERF-13, PERF-15, PERF-17
- **The system:** The theme's own render path. `base.css` render-blocks for 1351 ms with a chain of component CSS behind it (PERF-6); there's unused CSS (PERF-10 — a bootstrap `:root` block from an app, the RM Neue `@font-face`), the RM Neue font CSS is unminified (PERF-15), two theme JS modules (`quick-add.js`, `product-form.js`) load duplicated (PERF-13), and the critical-request chain is long (PERF-17). All Mason, theme-side — defer/inline critical CSS, dedupe the JS modules, prune unused rules.
- **Effort:** 3/5 — theme code, but critical-CSS work is fiddly on a Dawn fork (easy to break above-the-fold styling) and needs careful mobile + desktop verification. Pure Mason, no content/apps.
- **Impact:** 2/5 — Priority 3, field passes, and the numbers are small next to SYS-7 (47 KB render-blocking, 93 KB unused CSS, 4 KB duplicated JS). Real but minor.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset (SEC-1). HSTS and CSP — the two that mattered most — now pass (baseline §F has improved since they were flagged). On Shopify-hosted Advanced, response headers are largely platform-controlled and a theme can't freely set them, so the real first step is investigating what's settable at all, not writing a fix.
- **Effort:** 3/5 — mostly investigation; likely limited or not fixable without platform support. Low code, uncertain payoff.
- **Impact:** 1/5 — security is not a mission priority (the mission is a11y / SEO / perf), and these are the lower-severity pair. Lowest leverage in the cycle.
- **Priority:** 1 ÷ 3 = **0.33**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Theme a11y controls | 5 | 2 | 2.5 | Priority-1 a11y; small theme fixes that lift the lowest scores fast |
| 2 | SYS-2 · Heading hierarchy | 4 | 2 | 2.0 | one snippet cascades across 185 pages; a11y + SEO at once |
| 3 | SYS-3 · Image alt text | 5 | 3 | 1.67 | largest a11y debt — ship the theme fallback now, content ongoing |
| 4 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100; small embed/config fix |
| 5 | SYS-5 · Page metadata | 4 | 3 | 1.33 | SEO checklist + 76 pages; template default covers the bulk |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; field passes, so a lab-side gain |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly, field passes |
| 9 | SYS-9 · Security headers | 1 | 3 | 0.33 | not a mission priority; mostly platform-bound |

The shape of it: **ranks 1–4 are accessibility** (mission priority 1, the standing requirement) and they're all cheap theme work — that's the front of the queue. **Rank 5 is SEO** (priority 2). **Ranks 6–8 are performance** (priority 3), held back not because the numbers are small but because CrUX already passes, so they buy a lab score more than a faster store. Security sits last.

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding is accounted for, none silently dropped.

- **PERF-18** (slowest URLs) — the slowest page responds in 0.91 s, every URL is under 1 s and 200. Server response is healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none are credentialed, then leave.
- **BP-3** (inspector-issues) — 2 runs, no detail surfaced in the audit; revisit only if Best Practices must reach 95.
- **BP-5 / BP-6 / BP-7 / BP-8** (invalid / duplicate inline SVG, WebP / AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Low value, defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar (browser-verified mobile + desktop, no new console errors, Theme Check clean, no baseline regression) before moving on. Ranks 1–2 are the natural first PR — all theme code, all accessibility, no content or app dependency, shippable without waiting on anyone. After execution, re-baseline and diff the next cycle against this one: closed findings and any regressions tell you whether the plan worked.
