# Plan — 2026-06-25

Site: https://hazelboutique.com/ · Cycle: 2026-06-25-A · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

The findings are the facts. The systems, the effort, and the impact below are Hobbes' calls. Every system maps to real finding IDs from this cycle; nothing is invented. Where the catalog was a blunt rollup (A11Y-2, the SiteOne §F heading counts), I dropped to `raw/` to make it actionable — that's break-glass, and it's flagged where used.

The frame that decides impact this cycle: **CrUX field data (§C) passes on all three golden pages — LCP, INP, CLS all "good."** Real users are not waiting. That guts the impact of the lab-perf findings (PERF-*), which are mobile-throttle artifacts, and pushes the leverage onto the two Priority-1/2 systems that are code-authorable from this repo: the product-card name mismatch and the image-alt sweep, plus one clean heading bug I traced from the crawl.

## The systems

### SYS-1 · Product-card link — accessible-name mismatch
- **Findings:** A11Y-1 (label-content-name-mismatch, 55 nodes).
- **The system:** `snippets/card-product.liquid:43-48`. The fork made the whole card one `<a>` and gave it `aria-label="{{ card_product.title }}"`. That anchor wraps the title *and* the price *and* the swatches, so its visible inner text is "Title $48.00 …" while its accessible name is just "Title." WCAG 2.5.3 (Label in Name) fails: the visible text isn't contained in the name. One shared snippet renders every product card sitewide (grids, featured collections, search), so the 55 flagged nodes across Home/Collection are one root. Fix: drop the `aria-label` — the link's accessible name then computes from its content, which by definition contains the visible text, and the title text is always present so the link never loses its name.
- **Effort:** 1/5 — minutes · code (Mason), self-contained one-line delete in a shared snippet · trivial · high confidence. Browser/screen-reader confirm at review (bucket 2).
- **Impact:** 5/5 — Priority 1 (accessibility). Clears the only axe failure on the golden path (BASELINE §D), 55 nodes, every card-bearing page sitewide. Lighthouse a11y is already 100 and stays 100; this closes the automated-axe gap behind it.
- **Priority:** 5/1 = 5.0

### SYS-2 · Image-alt coverage sweep
- **Findings:** SEO-1 (golden Home 15/44, Collection 41/89, Product 2/25 images with empty/missing alt).
- **The system:** Traced from `raw/*.seo.json`: every `<img>` already carries an `alt` attribute, so this is **empty** `alt=""`, not missing markup. Three sources:
  1. **Secondary hover image** — `card-product.liquid:116`, hardcoded `alt=""`. This is the dominant count (40 of 41 on Collection, 10 of 15 on Home, 1 on Product). It's the product's second photo, code-owned. Fix in code: mirror the primary image — `alt="{{ card_product.media[1].alt | default: card_product.title | escape }}"`.
  2. **Multicolumn card images** — `sections/multicolumn.liquid:110-117`, `image_tag` with no alt fallback, so empty when the admin image has no alt (4 on Home). Fix in code: pass `alt: image.alt | default: block.settings.title`.
  3. **A 32px `aria-hidden="true"` decorative icon** (`IMG_3438.png`, 1 per page, admin-placed) — `alt=""` here is *correct* (decorative + hidden from AT). Forcing alt would be wrong. Leave it; note as a known coverage-tool over-count.
  - Residual: a handful of admin-uploaded product/content images whose alt field is blank live in Shopify admin, not the repo — content-owned (Britni/Jenna). The code fix clears the bulk; the tool's "All images have alt" row needs the admin alts filled to fully flip.
- **Effort:** 2/5 — minutes for the code (two snippet edits, Mason) · the residual is content at small scale (admin alt fields, Britni/Jenna) · low complexity · high confidence on the code, the content tail is owner-gated. Browser confirm (bucket 2).
- **Impact:** 4/5 — Priority 2 (SEO checklist "All images have alt") and Priority 1 (a11y, alt quality). One snippet edit clears ~50 images sitewide. Caveat: Lighthouse SEO is already 100 — this moves the internal coverage row, not the Lighthouse score; and the secondary-image alt adds mild screen-reader redundancy (the link already names the product), which the manual §G pass should sign off.
- **Priority:** 4/2 = 2.0

### SYS-3 · Sitewide heading / structural hygiene
- **Findings:** A11Y-2 (sitewide: 167 "HTML structural issue" warnings + 1 unnamed link/button, BASELINE §F multiple-H1 ×1, skipped-heading ×1).
- **The system:** A11Y-2 is a prevalence rollup; `raw/crawl.json` (seo-headings) makes it concrete. Every collection H1 renders **"Collection: Collection: <title>"** — `sections/main-collection-banner.liquid` prints the `{{ 'sections.collection_template.title' | t }}: ` ("Collection: ") visually-hidden span **twice**, line 16 (always) and line 26 (in the no-custom-image branch, the common case). Both spans are also `aria-hidden="true"`, so the doubling is invisible to humans and screen readers but real to crawlers and the rendered H1 text. Fix: delete the duplicate span at line 26. The residual A11Y-2 items — 1 page with multiple H1, 1 with a skipped level, 1 unnamed link/button — are single instances that need the specific rendered page identified; flag for a DOM-equipped follow-up, don't guess blind.
- **Effort:** 1/5 — minutes · code (Mason), delete one duplicated hidden span, no human-visible change (removes a crawler-only word doubling) · trivial · high confidence. Browser confirm the collection H1 still shows the title (bucket 2).
- **Impact:** 3/5 — Priority 2 (SEO/heading hygiene) and Priority 1 (clean structure). One file fixes the doubled prefix on every collection page; a cleaner, non-duplicated H1 reads better to search. Lower than SYS-1/2 because the symptom is crawler-facing, not a user-blocking defect.
- **Priority:** 3/1 = 3.0

### SYS-4 · Duplicate meta descriptions
- **Findings:** SEO-2 ("Hazel Boutique" ×5; templated product/collection copy ×4, ×4, ×2, ×2).
- **The system:** Two causes, neither code-fixable this cycle. (a) "Hazel Boutique" ×5 = system/utility pages (home, password, cart, search-class) with no natural description falling to `shop.description`. The theme fallback chain in `layout/theme.liquid:27-47` is already correct (page → collection → product → article → page → shop) — there's no code bug to fix; these pages inherently lack unique copy. (b) The repeated product/collection blurbs (EVI11 vintage one-of-a-kinds, candle spec sheet, bracelet copy) are identical merchant copy in Shopify admin. **Content-owned (Britni/Jenna):** write unique per-item descriptions, or the home/utility pages get a hand-written default in admin.
- **Effort:** 3/5 — content at scale, admin, owner-gated (Britni/Jenna). No code. Not authorable in this repo.
- **Impact:** 2/5 — Priority 2, but Lighthouse SEO is already 100 and the duplicates are mostly one-of-a-kind vintage items where unique copy is genuinely hard. Real discoverability gain is modest.
- **Priority:** 2/3 = 0.67 — **human to-do, not code this cycle.**

### SYS-5 · Performance — lab below target, field already passing
- **Findings:** PERF-1 … PERF-18 (lab scores 52–74, image delivery, cache lifetimes, payload, JS/CSS execution & unused, reflow, render-blocking, LCP breakdown/discovery, legacy/dup/minify JS·CSS, slowest URLs).
- **The system:** **§C CrUX passes on all three pages — LCP, INP, CLS all "good."** The lab failures are PSI's mobile throttle (Moto G4 / slow-4G / 4× CPU); the 27 s and 23 s LCPs are `✗cut` artifacts, not real. The weight sits in third-party and content, not theme code: `shopify.widget.js` (559 KB, Shop), `protect.widget.js`/`protect.core.js` (Route Insurance — **flagged for removal** in DEVELOPMENT.md), `da-restock.js`, Judge.me, Instafeed, GA, freeshippingbar, popup; plus merchant-uploaded **HEIC** hero images (`image_*.heic`, 183 KB+) that should be re-exported. The few first-party code levers (fetchpriority on the LCP image PERF-16; deferring `base.css` PERF-10; the desktop lab CLS) need the **rendered page** to target the right element safely and would risk regression written blind — they belong in a browser-equipped perf cycle.
- **Effort:** 5/5 — integration removal + coordination (Route Insurance, Mason/admin), content re-export (HEIC → JPG/WebP, Britni/Jenna), and the residual code is browser-gated. Scarce, multi-owner.
- **Impact:** 2/5 — real users already pass (§C). Lab score is the only thing failing, and it's the throttle. Highest-value concrete move is the Route Insurance removal already on the books.
- **Priority:** 2/5 = 0.4 — **human/integration to-do + defer risky code to a browser cycle.**

### SYS-6 · Missing security response headers
- **Findings:** SEC-1 (Referrer-Policy, Permissions-Policy absent — 2 of 4), SEC-2 (Access-Control-Allow-Origin: \* on assets).
- **The system:** Response headers on a Shopify-hosted storefront are largely platform-controlled — the theme can't set arbitrary response headers, and CSP/HSTS are already present (host-set). SEC-2's `ACAO: *` is on public CDN assets, which is normal and not a credentialed-endpoint risk. Confirm what's actually settable on Advanced (some via admin/checkout settings or an app) before treating as fixable.
- **Effort:** 4/5 — platform/integration, admin (Mason). Not theme-code-authorable. Gated by what Shopify exposes.
- **Impact:** 2/5 — hardening headers, no user-facing or mission-priority gain; SEC-2 is benign on assets.
- **Priority:** 2/4 = 0.5 — **human/platform to-do.**

### SYS-7 · Best-practices & structural notices
- **Findings:** BP-1 (console errors), BP-2 (inspector issues), BP-3 (invalid inline SVG ×10), BP-4 (duplicate inline SVG ×1), BP-5 (WebP), BP-6 (AVIF).
- **The system:** BP-1/BP-2 are third-party and client-side: `ERR_BLOCKED_BY_CLIENT` (ad blockers), 400/403 from embeds, a `shop.app` frame-ancestors CSP (Shopify) — not first-party bugs to fix. BP-3/BP-4 are "0 critical" warnings (icon snippets inlined per use — minor DOM bloat, low value, upgrade-safety says don't scatter edits). BP-5/BP-6 are informational format-support notices, not defects. Nothing here is a user-blocking or mission-priority gap.
- **Effort:** 3/5 — mostly third-party (can't fix) or low-value warnings; the SVG `<use>` refactor is core-theme churn against the upgrade-safety rule.
- **Impact:** 1/5 — cosmetic/benign; Best-Practices score is already 92–96.
- **Priority:** 1/3 = 0.33 — **won't-chase this cycle; flagged for visibility.**

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Product-card name mismatch | 5 | 1 | 5.0 | Clears the only golden-path axe failure (55 nodes) sitewide, one-line snippet edit |
| 2 | SYS-3 · Heading/structural hygiene | 3 | 1 | 3.0 | Kills doubled "Collection:" H1 on every collection page, one file |
| 3 | SYS-2 · Image-alt coverage | 4 | 2 | 2.0 | One snippet clears ~50 images sitewide; content tail flagged |
| 4 | SYS-4 · Duplicate meta descriptions | 2 | 3 | 0.67 | Content-owned; theme fallback already correct → human to-do |
| 5 | SYS-6 · Security headers | 2 | 4 | 0.5 | Platform-controlled on Shopify → human/platform |
| 6 | SYS-5 · Performance | 2 | 5 | 0.4 | Field already passes; third-party/content/browser-gated → human + defer |
| 7 | SYS-7 · Best-practices notices | 1 | 3 | 0.33 | Third-party + benign warnings → won't-chase |

## The handoff

Execution takes the **code-authorable, no-browser-safe** top of this order — SYS-1, SYS-3, SYS-2 — and ships all three in one PR (effort budget 100; the constraint here isn't points, it's feasibility — a GitHub-only run can't drive a browser). SYS-4/5/6/7 are content-, platform-, integration-, or browser-gated; they're written up as owner-tagged human to-dos in the PR, not dropped. After publish, the review re-baselines the live site and diffs §D (axe), §E (alt coverage), and §F (headings) against this cycle.
