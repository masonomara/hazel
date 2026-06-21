# Plan — 2026-06-20

Site: https://hazelboutique.com/ · Cycle: 2026-06-20 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 39 findings of this cycle, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) and the high-leverage structural cascades go first; the expensive performance work — where CrUX already passes for real users — waits behind the cheap theme-code wins.

**Two realities that shaped every rating:**
- **Field passes, lab fails.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages — the one move since 2026-06-18 is a 0.012s Product-LCP wobble (`diff.md`), noise. The mobile Lighthouse 63–73 is the fixed-throttle lab, not real users. So every performance system serves the *lab-score* target (mission §3, "≥ 90") far more than a real shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content**, not Liquid — 76 pages needing descriptions, every product image needing meaningful alt — owned by Jenna/Britni in admin, not Mason. Effort names the resource, because "Mason ships a snippet" and "Jenna writes 76 descriptions" are different costs.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-2 · Heading hierarchy & document structure
- **Findings:** A11Y-3, A11Y-5, SEO-2
- **The system:** One structural root, sitewide, and it is a real markup defect — not a styling drift. `snippets/card-product.liquid:124–135` renders the product-card title as a **heading nested inside a heading** — `<h3 class="card__heading"><h3 class="full-unstyled-link">…</h3></h3>` — on every card on every grid page. The *other* card variant in the same file (`:189–203`) already does it correctly (`<h3>` wrapping a `<span class="full-unstyled-link">`), which is the proof of the fix. That nested-heading is the concrete cause behind **A11Y-3** (heading-order on the collection card) and the lion's share of **A11Y-5**'s 1,746 sitewide "HTML structural" warnings (every card multiplies it). **SEO-2** is the broader outline failure it sits inside — 185 pages flag a skipped level and Home shows 2 h1 (the header logo h1 at `sections/header.liquid:177/217/372` plus the page h1). Fixing the nested heading clears A11Y-3 and the bulk of A11Y-5 in one self-contained snippet edit; the deeper SEO-2 work (section-level h2s so cards don't skip from h1→h3, and demoting the duplicate header logo h1 off non-home pages) is a larger, Dawn-layout-touching follow-up flagged inside this system, not a token tweak.
- **Effort:** 2/5 — Mason, theme code. The nested-heading fix is one mechanical snippet edit (match the file's own correct variant), high confidence, no content or app. The full SEO-2 outline pass (header-logo h1 + section h2s) is the part that pushes this past a 1 — riskier, touches shared layout, deferred within the system.
- **Impact:** 5/5 — Priority 1 (a11y) *and* Priority 2 (SEO) at once, and the single largest cascade in the cycle: one snippet touches every product card on all 185 pages. No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 2 = **2.5**

## SYS-1 · Theme accessibility controls
- **Findings:** A11Y-1
- **The system:** Two theme-owned `label-content-name-mismatch` defects, both pure markup, no content or app dependency. (1) **Hero slideshow** (`sections/hero.liquid:59`) — the mobile-hero slide link's `aria-label="Go to {{ block.settings.heading }}"` renders the literal "**Go to **" when a slide has no heading (the empty node in the evidence), and where a heading exists the accessible name ("Go to Shop HZL NEW") omits the visible counter ("001 …") the link actually shows → mismatch. (2) **Pagination** (`snippets/pagination.liquid:42/44, 53/55`) — the visible page number is zero-padded to "**08**" but the `aria-label` is built from the raw title as "Page **8**", so the visible text isn't contained in the accessible name → mismatch on every paginated collection. Both are fixed by making the accessible name contain (or align to) the visible text. This is what holds Home-mobile and Collection at a failing automated-a11y row in baseline §D.
- **Effort:** 2/5 — Mason, theme code, two self-contained snippet edits; selectors and root cause already pinned. High confidence.
- **Impact:** 4/5 — Priority 1, directly removes failing axe audits on the golden path (Home-mobile, Collection desktop+mobile), moving those scores toward the mission's 100. No field caveat.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup (`PopupSignupForm_0`, `mc-banner` / `mc-modal`) injects two `about:blank`, title-less iframes on **every page** (all 6 runs) → `frame-title` fails everywhere. Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), wrapping the embed, or a product decision to drop the popup (a marketing call → Brenda/Jenna). It must clear to reach a11y 100, because it's on every page.
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access to the Mailchimp embed or a marketing decision, not a change Mason makes in this repo. Medium confidence — depends on what the embed exposes.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also just remove. Necessary-but-small for the a11y-100 target.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Image alt text
- **Findings:** A11Y-4, SEO-3
- **The system:** The site's image-alt debt, two tracks with two owners. **(a) Theme fallback** — the product-card featured image (`snippets/card-product.liquid:89`) binds `alt` straight to the admin alt (`card_product.featured_media.alt`), so when the admin alt is blank the card ships `alt=""`. Binding a fallback to the product title is a one-line Liquid change that gives every card a meaningful name and passes the automated "all images have alt" check. **(b) Meaningful alt at scale** — the quality the a11y standing-requirement and the manual pass actually want — is per-image content work in admin, owned by Jenna/Britni. SEO-3's golden counts (20/45 Home, 44/88 Collection) are inflated by the **decorative hover image** (`:112`, hardcoded `alt=""`), which is *correctly* empty for a11y — chasing that coverage number to zero would announce every product twice and is the wrong call. **A11Y-4**'s single missing-alt node is a bare `<img>` (no srcset/sizes/class) that does **not** match card-product's output — likely an app- or custom-injected image; its source must be identified at review, not assumed. Ship (a) now; open (b) as ongoing content; verify the A11Y-4 node's origin.
- **Effort:** 3/5 — blended. The theme fallback alone is a 2; meaningful alt across the catalog is a 5 (client content, ongoing). Resource is **code *and* client content**.
- **Impact:** 4/5 — dual priority (A11y §1 + the SEO checklist's "all images have alt", failing on all three golden pages); the code fallback is a real, if partial, lift. Dampened from a 5 because the headline coverage counts are partly the decorative-by-design hover image.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-5 · Page metadata — descriptions, titles, Open Graph
- **Findings:** SEO-1, SEO-4, SEO-5, SEO-6
- **The system:** The discoverability layer on collection/page templates. **76 pages** have no meta description (SEO-1 — mostly collections, policies, system pages), 5 share a duplicate description (SEO-6 — templated vintage/candle copy), 4 share a duplicate title (SEO-5 — "Dresses", "Tops", "Under $50", "New Arrivals" collections), and 43 pages plus golden Home lack a full OG/Twitter set (SEO-4 — Home missing `og:image`). Mixed resource: a **templated default** (collection description → meta description; a `theme.liquid` `og:image` fallback) is code that auto-fills the bulk and passes the checklist; unique copy for the top collections and the duplicate-title renames are admin/content (Jenna/Britni).
- **Effort:** 3/5 — template defaults are a quick Mason win that covers most of it; bespoke copy for key collections and the title renames are content. Code + content.
- **Impact:** 4/5 — Priority 2 (discoverability), 76+ pages, and it moves the SEO-checklist items (meta description, OG) holding the golden-path SEO score under 95. Serves the mission's "discoverable" directly.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-12, PERF-14, PERF-17, BP-3
- **The system:** Images are the heaviest payload class and the LCP driver on the throttled mobile runs. Oversized product images (234–667 KB each, PERF-2/5), **HEIC source files served raw** (`image_*.heic` — a phone-camera format browsers handle poorly, that should be re-exported to WebP/AVIF), the logo shipped unsized (PERF-12) and at the wrong aspect ratio (BP-3), the LCP image neither `fetchpriority=high` nor discoverable from HTML (PERF-14), and a long critical-request chain (PERF-17). Mixed resource: theme `<img>` work (logo dims, LCP `fetchpriority`, responsive `sizes`) is Mason; re-exporting the HEIC and oversized originals is content (Jenna's assets). This is the mission's explicit "Image & asset loading — confirm consistent loading site-wide."
- **Effort:** 3/5 — code for dims/fetchpriority/sizes (moderate); content for the heavy/HEIC re-exports (Jenna).
- **Impact:** 3/5 — Priority 3, and **field already passes** (real-user LCP is fine), so the lab lever is real but the real-user gain is small. Nudged above the other perf systems because the mission names asset loading as a gap and big images cost mobile shoppers real bytes.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-7, PERF-8, PERF-9, PERF-11, PERF-16, BP-1, BP-4
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB, the single biggest resource and largest unused-JS block at 392 KB), Fera reviews (`fera.js`; also the source of the BP-1 "Error fetching recommendations 422" console error), **Route's `protect.widget.js` / `protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, the free-shipping bar, portable-wallets, GA, and a deprecated API (BP-4). Together they drive uncached bytes (PERF-3), execution and main-thread time (PERF-4/9), unused + legacy JS (PERF-7/11), forced reflow (PERF-8), an unminified app script (PERF-16), and the console-error count that holds Best Practices down (BP-1). **PERF-1 is the landscape that frames this whole system:** mobile lab 63–73, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route, where the decision is already made), defer/async the rest.
- **Effort:** 4/5 — the biggest coordination cost in the cycle. Each app is a business decision (Route is a revenue feature, Fera is reviews, the free-shipping bar is merchandising), so it's app-config + Jenna/Britni/Brenda coordination + test-each-removal, not a change Mason makes alone.
- **Impact:** 3/5 — Priority 3 and the single biggest *lab* lever, but **field passes** so real users are already fine; the gain is the lab score plus a cleaner Best-Practices score from killing console errors. Removing Route also banks an existing mission decision. Dampened by the field reality.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical path
- **Findings:** PERF-6, PERF-10, PERF-13, PERF-15
- **The system:** The theme's own render path. `base.css` render-blocks for ~1,142 ms with a chain of component CSS behind it (PERF-6); there's unused CSS (PERF-10 — a bootstrap `:root` block from an app, the RM Neue `@font-face`), the RM Neue font CSS is unminified (PERF-15), and two theme JS modules (`quick-add.js`, `product-form.js`) load duplicated (PERF-13). All Mason, theme-side — defer/inline critical CSS, dedupe the JS modules, prune unused rules.
- **Effort:** 3/5 — theme code, but critical-CSS work is fiddly on a Dawn fork (easy to break above-the-fold styling) and needs careful mobile + desktop verification. Pure Mason, no content/apps.
- **Impact:** 2/5 — Priority 3, field passes, and the numbers are small next to SYS-7 (47 KB render-blocking, 93 KB unused CSS, 4 KB duplicated JS). Real but minor.
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset (SEC-1). HSTS and CSP — the two that mattered most — now pass (baseline §F). On Shopify-hosted Advanced, response headers are largely platform-controlled; a theme can set `Referrer-Policy` via a `<meta name="referrer">` tag but `Permissions-Policy` has no meta equivalent, so the real first step is confirming what's settable, not writing a fix.
- **Effort:** 3/5 — mostly investigation; likely only partially fixable from the theme. Low code, uncertain payoff.
- **Impact:** 1/5 — security is not a mission priority (the mission is a11y / SEO / perf), and these are the lower-severity pair. Lowest leverage in the cycle.
- **Priority:** 1 ÷ 3 = **0.33**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-2 · Heading hierarchy & structure | 5 | 2 | 2.5 | one snippet fix cascades across every card on 185 pages; a11y + SEO at once |
| 2 | SYS-1 · Theme a11y controls | 4 | 2 | 2.0 | Priority-1 a11y; two pinned label-mismatch bugs, pure theme code |
| 3 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 4 | SYS-3 · Image alt text | 4 | 3 | 1.33 | dual-priority; ship the theme fallback now, meaningful alt is content |
| 5 | SYS-5 · Page metadata | 4 | 3 | 1.33 | SEO checklist + 76 pages; template default covers the bulk |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; field passes, so a lab-side gain |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly, field passes |
| 9 | SYS-9 · Security headers | 1 | 3 | 0.33 | not a mission priority; mostly platform-bound |

The shape of it: **ranks 1–4 are accessibility** (mission priority 1, the standing requirement) and the theme-code ones are all cheap — that's the front of the queue. **Rank 5 is SEO** (priority 2). **Ranks 6–8 are performance** (priority 3), held back not because the numbers are small but because CrUX already passes, so they buy a lab score more than a faster store. Security sits last.

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding is accounted for, none silently dropped.

- **PERF-18** (slowest URLs) — the slowest page responds in 0.60 s, every URL under 1 s and 200. Server response is healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none are credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced in the audit; revisit only if Best Practices must reach 95.
- **BP-5 / BP-6 / BP-7 / BP-8** (invalid / duplicate inline SVG, WebP / AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Low value, defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar (browser-verified mobile + desktop, no new console errors, Theme Check no new offenses, no baseline regression) before moving on. Ranks 1–2 plus the code half of rank 4 are the natural first PR — all theme code, all accessibility, no content or app dependency, shippable without waiting on anyone. After execution, re-baseline and diff the next cycle against this one: closed findings and any regressions tell you whether the plan worked.
