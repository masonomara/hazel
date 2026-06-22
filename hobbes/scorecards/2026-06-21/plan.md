# Plan — 2026-06-21

Site: https://hazelboutique.com/ · Cycle: 2026-06-21 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 39 findings of this cycle, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list at the foot — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** accessibility (mission priority 1) and the high-leverage structural cascade go first; the discoverability layer (priority 2) next; the expensive performance work — where CrUX already passes for real users — waits behind the cheap theme-code wins.

**Three realities that shaped every rating:**
- **Field passes, lab fails.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages. `diff.md` since 2026-06-20 is noise — two INP wobbles (Home 103→105, Product 96→98) and small LCP improvements. The mobile Lighthouse 65–75 is PSI's fixed-throttle lab, not real users. So every performance system serves the *lab-score* target (mission §3, "≥ 90") far more than a real shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content**, not Liquid — 76 pages needing descriptions, duplicate collection titles to rename, every product image needing meaningful alt, oversized/HEIC source files to re-export, and — proven this cycle from `templates/index.json` — the per-section `heading_size` choices that drive the homepage outline. All owned by Jenna/Britni in admin, not Mason. Effort names the resource, because "Mason ships a snippet" and "Jenna writes 76 descriptions" are different costs.
- **The a11y/SEO/security code front is largely shipped and merged.** PR #8 (06-20) merged the a11y batch (nested-heading, slideshow/pagination labels, card-image alt fallback). PRs #10/#11 (06-21, budget-20 run) merged the SEO-metadata, image-delivery, and Referrer-Policy code — all now in `main`. The findings below still enumerate those rules because the catalog measures the **live** site, which has not been republished since (a human owns publish). This is the plan's grouping regardless; **execution** owns the "already-in-main" accounting and the publish dependency.

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-2 · Heading hierarchy & document structure
- **Findings:** A11Y-3, A11Y-5, SEO-2
- **The system:** One structural root, sitewide. `snippets/card-product.liquid` renders the product-card title; the nested heading-in-heading (`<h3><h3>…</h3></h3>`) that drove **A11Y-3** and the bulk of **A11Y-5**'s ~1,758 sitewide "HTML structural" warnings was fixed and merged in PR #8 — the title is now `<h3><span class="full-unstyled-link">`. What **remains** is the deeper **SEO-2** outline failure (185 pages flag a skipped level; 2 pages multiple-h1), and this cycle's source dig pinned its real roots:
  - **Collection-grid h1→h3 skip (the dominant case, ~76+ collection pages).** On a populated collection the page is `<h1>` (`main-collection-banner.liquid:15`) → product cards `<h3>` (`card-product.liquid`), with **no h2 between** (the grid's only `<h2>` renders solely on an *empty* collection, `main-collection-product-grid.liquid:104`). That h1→h3 jump is the bulk of the 185-page count. Fixable in theme code: the card heading is `<h3 class="… h5">` — Dawn's tag-vs-size-class split, so the **tag** can move to `<h2>` (correct under the page h1) with the size **class** unchanged → zero visual change. All CSS targets `.card__heading` (class), never the `h3` tag; no JS touches it (verified).
  - **Homepage "multiple-h1" is merchant content, not theme code.** Every Dawn content section renders `<h2 class="… {{ heading_size }}">` (fixed tag, size as class), and the custom hero emits its slide heading as plain text in a `<div>` — so the `heading_size: "h1"` settings across `index.json` are visual size classes, **not** real `<h1>`s. The remaining multi-h1 is the header's per-layout logo `<h1>` variants in the DOM (`header.liquid:177/217/373`, CSS-toggled) and/or a stale-crawl artifact — a DOM question to confirm in the browser, not a clean single-line edit.
  - **One stray non-title `<h1>`** at `main-product.liquid:689` — a product-page "page content" popup block titled with `<h1 class="h2">`. Wrong by semantics (not the product title); → `<h2>`, class unchanged.
- **Effort:** 3/5 — the card-grid tag fix + the stray-h1 fix are contained, high-confidence theme code (Mason); the homepage multi-h1 is merchant `heading_size` settings (Jenna, in the editor) plus a header-DOM confirmation. Blended.
- **Impact:** 5/5 — Priority 1 (a11y) *and* Priority 2 (SEO) at once; the single largest cascade in the cycle. No field caveat — structure has no lab/field split.
- **Priority:** 5 ÷ 3 = **1.67**

## SYS-1 · Theme accessibility controls
- **Findings:** A11Y-1
- **The system:** Two theme-owned `label-content-name-mismatch` defects, both pure markup — the hero slideshow slide link's `aria-label`/decorative counter (`sections/hero.liquid`) and the pagination zero-padded label (`snippets/pagination.liquid`). **Both shipped and merged in PR #8**; `diff.md` confirms the drop 11→3 nodes. The 3 nodes still in A11Y-1 are the pre-publish live state.
- **Effort:** 2/5 — Mason, theme code, two self-contained snippet edits. Done; awaits publish.
- **Impact:** 4/5 — Priority 1, removes failing axe audits on the golden path. No field caveat.
- **Priority:** 4 ÷ 2 = **2.0**

## SYS-4 · Mailchimp popup accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less iframes on **every page** → `frame-title` fails everywhere. Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), a wrapper, or a product decision to drop the popup (a marketing call → Brenda/Jenna).
- **Effort:** 2/5 — small, but **entirely human-owned**: app-config access or a marketing decision, not a change Mason makes in this repo.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party we could also remove.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Image alt text
- **Findings:** A11Y-4, SEO-3
- **The system:** Two tracks, two owners. **(a) Theme fallback** — the product-card featured image now binds `alt="{{ …alt | default: card_product.title | escape }}"` (shipped/merged PR #8), so every card image has a meaningful name even when admin alt is blank. **(b) Meaningful alt at scale** — per-image content work in admin, owned by Jenna/Britni. SEO-3's golden counts are partly the **decorative hover image** (hardcoded `alt=""`), which is *correctly* empty. **A11Y-4**'s single missing-alt node is a bare `<img>` that doesn't match card-product's output — likely app/custom-injected; identify its source in the browser at review.
- **Effort:** 3/5 — theme fallback shipped (a 2); meaningful alt across the catalog is a 5 (client content, ongoing).
- **Impact:** 4/5 — dual priority; dampened because the headline coverage counts are partly the decorative-by-design hover image.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-5 · Page metadata — descriptions, titles, Open Graph
- **Findings:** SEO-1, SEO-4, SEO-5, SEO-6
- **The system:** The discoverability layer on collection/page templates. **76 pages** had no meta description (SEO-1); **43 pages + golden Home** lacked a full OG/Twitter set (SEO-4). The **code halves are shipped and merged** in PRs #10/#11 — `layout/theme.liquid` now computes a typed `meta_description` fallback chain and `snippets/meta-tags.liquid` an `og_image` fallback + `twitter:image` (plus a `share_image` setting). The remainder is content: 4 duplicate titles (SEO-5) and 4 duplicate descriptions (SEO-6) are admin renames/rewrites (Jenna/Britni).
- **Effort:** 3/5 — templated head defaults done; duplicate-title renames and bespoke copy are content.
- **Impact:** 4/5 — Priority 2, 76+ pages, moves the SEO-checklist items holding the golden-path SEO score under 95.
- **Priority:** 4 ÷ 3 = **1.33**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-5, PERF-12, PERF-14, PERF-17, BP-3
- **The system:** Images are the heaviest payload class and the LCP driver on throttled mobile. **(a) Theme code — shipped/merged (PRs #10/#11):** the two hero-logo intrinsic dimensions (PERF-12, BP-3) and the LCP hero `fetchpriority="high"` (PERF-14). **(b) Content — open:** oversized product images (234–667 KB, PERF-2/5) and **HEIC source files served raw** need re-exporting to WebP/AVIF at sane dimensions — Jenna's assets. PERF-17 is largely app-script chaining, tracked under SYS-7. This is the mission's explicit "Image & asset loading."
- **Effort:** 3/5 — code done; content re-exports are Jenna.
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-7, PERF-8, PERF-9, PERF-11, PERF-16, BP-1, BP-4
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB), Fera (`fera.js`, also the BP-1 422 console error), **Route's `protect.widget.js`/`protect.core.js` — already flagged for removal in `DEVELOPMENT.md`**, DA-Restock, free-shipping bar, portable-wallets, GA, a deprecated API (BP-4). Together they drive uncached bytes, execution/main-thread time, unused+legacy JS, an unminified app script, unused app CSS, and the console-error count. **PERF-1 frames it:** mobile lab 65–75, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, not theme files — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & critical path
- **Findings:** PERF-6, PERF-10, PERF-13, PERF-15
- **The system:** The theme's render path. `base.css` render-blocks ~1,051 ms with a chain of component CSS behind it (PERF-6); a forced reflow in app + page JS (PERF-10); an unminified app-injected `RM Neue` `@font-face` (PERF-15); and two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-13 — 4 KB). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring base.css risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, and PERF-13 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto pages with no cards) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7 (47 KB render-blocking, 4 KB dup JS).
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` were unset (SEC-1); HSTS and CSP now pass. The **Referrer-Policy `<meta>` is shipped/merged** (PRs #10/#11). `Permissions-Policy` has **no meta equivalent** — platform/edge-controlled — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Theme a11y controls | 4 | 2 | 2.0 | Priority-1 a11y; two label-mismatch bugs (shipped+merged PR #8) |
| 2 | SYS-2 · Heading hierarchy & structure | 5 | 3 | 1.67 | a11y + SEO at once; card-grid h1→h3 skip on ~76+ pages is clean theme code |
| 3 | SYS-4 · Mailchimp popup a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (app-config/decision) |
| 4 | SYS-3 · Image alt text | 4 | 3 | 1.33 | dual-priority; theme fallback merged, meaningful alt is content |
| 5 | SYS-5 · Page metadata | 4 | 3 | 1.33 | SEO checklist + 76 pages; code halves merged, duplicate copy is content |
| 6 | SYS-6 · Image delivery | 3 | 3 | 1.0 | mission asset-loading gap; code merged, heavy/HEIC re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy merged, Permissions-Policy platform-bound |

The shape of it: **ranks 1–6 and rank 9's code are already merged into `main`** (PRs #8/#10/#11), awaiting only the human publish. The cycle's remaining *unshipped theme code* is the **SYS-2 outline work** — and within it, the card-grid h1→h3 skip is the one clean, contained, sitewide win. The rest of every system is content (Jenna/Britni), app/business decisions (SYS-4, SYS-7), platform (Permissions-Policy), or a browser-gated CSS/JS slice (SYS-8).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-18** (slowest URLs) — slowest page 0.54 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95.
- **BP-5 / BP-6 / BP-7 / BP-8** (invalid/duplicate inline SVG, WebP/AVIF "support") — all "0 critical, N warning", Dawn/platform-level cosmetic flags. Defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. Ranks 1, 3–6 and rank-9 code are already merged (awaiting publish), so the budget flows to **rank 2 (SYS-2 heading hierarchy)** — the top of the *unshipped* code. Within SYS-2, the card-grid h1→h3 fix and the stray product-page h1 are clean, contained theme code; the homepage multi-h1 (merchant `heading_size` settings) and the header logo-variant DOM question are handed to their owners. After execution, re-baseline and diff the next cycle: closed findings and any regressions tell you whether the plan worked.
