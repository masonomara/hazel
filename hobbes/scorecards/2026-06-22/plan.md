# Plan — 2026-06-22 (re-measured)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

> **This run is against the re-measured 2026-06-22 data**, and that re-measurement settles two prior calls with evidence:
> 1. **The heading fix worked.** Last run traced the universal skipped-level count to the global cart-drawer `card-collection` double-`<h3>` and shipped a `card_heading_tag` fix (now in `main`). The re-crawl confirms it: **skipped-heading pages 185 → 2** (§F / `diff.md`). The cascade is closed but for two admin page bodies.
> 2. **The hero label fix did *not* work — and couldn't have.** A prior pass changed the hero slide link's `aria-label` to `… | strip_html | …` to clear `label-content-name-mismatch`. The re-crawl still shows **A11Y-1 = 3 nodes, unchanged.** That isn't a publish lag — it's a misdiagnosis: the three flagged headings carry no HTML ("Shop HZL NEW"; blank → "View slide"), so `strip_html` is a *no-op* on them. The real cause is the **visible slide counter** (`01/02/03`) sitting inside the link but absent from the `aria-label`. That re-diagnosis is this run's code win (SYS-1).

The 35 findings, grouped into **9 systems** and ordered by leverage. Every finding lands in exactly one system or the explicit won't-chase list — nothing dropped, nothing invented. Effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`; the findings they rest on are fixed.

**The strategy in one line:** the structural cascade is banked and validated, so the one clean theme-code lever left — the correctly-diagnosed hero slideshow naming — leads; everything below it is content, app-config, platform, or browser-gated.

**Three realities that shaped every rating:**
- **Field passes, lab fails — and the lab is noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages; `diff.md` confirms **0 field regressions** vs 2026-06-21. The §A lab perf scores swing hard between passes (Home-mobile 41↔63, Product-desktop 77↔60) while CrUX holds flat — that is PSI's fixed-throttle volatility over app-injected JS, not a real-user move. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly.
- **Resource ≠ "code."** A large share of this catalog is **content or app/platform**, not Liquid Hobbes can author: the two remaining heading pages live in `{{ page.content }}` (admin rich text), 4 duplicate collection titles (SEO-3), 9 duplicate/templated descriptions (SEO-4), meaningful per-product alt at scale (SEO-2), oversized/HEIC source files (PERF-2/4), the Mailchimp embed (A11Y-2), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe code front is nearly exhausted — by design, not neglect.** Slideshow/pagination labels, card-image alt fallback, meta-description + OG/Twitter, hero-logo dims + LCP `fetchpriority`, Referrer-Policy meta, and the cart-drawer `card_heading_tag` heading fix are all in `main`; the catalog still enumerates them because it measures the **live** site, which lags unpublished code. What is genuinely *both* unshipped *and* safely theme-authorable this run is exactly one thing: the re-diagnosed hero label fix (SYS-1).

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Hero slideshow accessible naming
- **Findings:** A11Y-1
- **The system:** Three `label-content-name-mismatch` nodes, all the **mobile** hero slide links (`sections/hero.liquid`, the `slideshow-component.mobile-hero` block). The slide `<a>` sets `aria-label="{{ block.settings.heading | strip_html | default: 'View slide' }}"`, but the link's *visible* inner text is the slide counter — `01`/`02`/`03`, rendered in `<span class="rteMidge">` — **plus** the heading. The counter is visually shown but never appears in the `aria-label`, so visible text ⊄ accessible name on every slide → mismatch. The proof it's purely this aria-label/content conflict: the **desktop** hero block renders the identical slide link with **no aria-label** (name from content) and a non-hidden counter, and does **not** flag. The proof `strip_html` can't fix it: the flagged headings carry no markup, so the filter is a no-op — the re-crawl held A11Y-1 at 3 nodes. Voice-control users can't activate a slide by its visible label.
- **The fix (this run's code):** mirror the passing desktop block — **drop the conflicting `aria-label`** from the mobile slide link so the name derives from content, and **un-hide the counter** (`<span class="rteMidge">`, removing `aria-hidden="true"`) so the content-derived name equals the visible text *and* blank-heading slides are still named by their counter (no new `link-name` violation). Safe by construction: `.rteMidge`/`.textyText` are styled by **class** (verified in `base.css`/`component-hero.css`), no JS references the slide link's `aria-label` or `slideshow__slide` (verified) — zero visual/behavioral change; it only removes two ARIA attributes, exactly matching the desktop sibling that already passes.
- **Effort:** 1/5 — Mason, one self-contained section edit (two attribute removals), an already-proven in-file pattern. Needs only axe/browser confirmation at review.
- **Impact:** 4/5 — Priority 1 (accessibility), clears the only theme-owned failing axe audit on the golden path (Home — mobile). No field caveat — naming has no lab/field split.
- **Priority:** 4 ÷ 1 = **4.0**

## SYS-2 · Heading outline — the last two pages
- **Findings:** SEO-1, A11Y-3
- **The system:** The heading cascade is validated and all but closed — sitewide skipped-heading pages fell **185 → 2** once the cart-drawer `card_heading_tag` fix removed the four leading `<h3>` from the global outline. What remains (SEO-1) is **two admin-authored page bodies**, both rendered through `sections/main-page.liquid` as `<h1>{{ page.title }}</h1>` followed by `{{ page.content }}` (admin rich text):
  - **/pages/sizing** — `h1 → h3 → h3 → h3 → h3 → h2`: the size-chart sub-heads in the page body jump to `<h3>` with no `<h2>` between. The h1 is theme; the h3s live in the **page content** (admin).
  - **/pages/search-results** — `h1 → h1 → h2`: a second `<h1>` inside the page body (the §F multiple-H1 = 1). The title h1 is theme; the stray h1 is in the **page content** (admin).
  - **A11Y-3** (sitewide a11y prevalence, 1761 flagged elements) rolls up here: 1756 of 1761 are "HTML structural" warnings — the same outline family — with only 3 image-alt + 1 form-label + 1 unnamed-link slivers (tracked under SYS-4/SYS-3). It's an aggregate signal, not a separate fix.
- **Effort:** 2/5 — small, but **content, not code**: edit two page bodies in the admin (demote the size-chart h3s to h2; remove/demote the stray search-results h1). Jenna/Britni in the theme editor — the theme repo can't reach `{{ page.content }}`.
- **Impact:** 3/5 — Priority 1 + 2 (structure serves both), but only 2 of 185 pages remain; the cascade already banked the win.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Third-party embed accessibility
- **Findings:** A11Y-2
- **The system:** The Mailchimp signup popup injects two `about:blank`, title-less `<iframe>`s on **every page** (`#PopupSignupForm_0` banner + modal) → `frame-title` fails sitewide (2 nodes, 6 of 6 golden runs). Not our markup — the Mailchimp embed — so the fix is the embed/app config (add a frame title), a wrapper, or a product decision to drop the popup (a marketing call).
- **Effort:** 2/5 — small, but **entirely human-owned**: Mailchimp app-config access or a marketing decision (Brenda/Jenna), not a change Mason makes in this repo.
- **Impact:** 3/5 — Priority 1 and on every page, but a single rule on a third-party embed we could also remove.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-4 · Image alt at scale
- **Findings:** SEO-2
- **The system:** Coverage of `alt` on images across the golden pages (Home 19/43, Collection 45/88, Product 16/24 `<img>` missing alt). Two tracks: **(a) Theme — done.** The product-card featured image binds `alt` to the product title (merged), which is why axe's **image-alt dropped 4 → 0** on the golden path (`diff.md`). A full theme sweep this run confirms **every live theme `<img>` already carries an `alt`** — the only bare `<img>` is inside the fully `{%- comment -%}`-disabled `recent-viewed-product-js.liquid` (dead, never rendered). **(b) Content + apps — open.** The remaining missing-alt counts are admin product images where the merchant left alt blank, plus app-injected widget images (Judge.me, Instafeed) — per-image content work, Jenna/Britni. SEO-2's count also includes the decorative hover image, correctly `alt=""`.
- **Effort:** 4/5 — theme side shipped (a 1); meaningful alt across the catalog is the cost (client content at scale, ongoing).
- **Impact:** 4/5 — dual priority (a11y + SEO); dampened because the theme defect is closed and the residue is partly decorative-by-design.
- **Priority:** 4 ÷ 4 = **1.0**

## SYS-5 · Page metadata uniqueness
- **Findings:** SEO-3, SEO-4
- **The system:** Duplicate `<title>`s (SEO-3, 4 pairs — Under $50, Tops, New Arrivals, Dresses) and duplicate meta descriptions (SEO-4, 9 sets — "Hazel Boutique" ×5, templated "Shop X at Hazel Boutique." pairs, repeated product copy). Search engines can't tell the pages apart. The templated-head fallback chain (shipped) handles *absent* metadata — note the `"Shop X …" ×2` duplicates are that fallback doing its job, every page *has* a description; **distinguishing** near-identical pages is bespoke copy. Admin renames + rewrites per collection/page (Jenna/Britni). No theme mechanism makes two genuinely-similar collections unique.
- **Effort:** 3/5 — no code; ~13 admin strings (4 title renames + 9 description rewrites), Jenna/Britni.
- **Impact:** 3/5 — Priority 2, but bounded and the golden-path SEO score already reads 100.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-6 · Image delivery & sizing
- **Findings:** PERF-2, PERF-4, PERF-14, PERF-18
- **The system:** Images are the heaviest payload class and the mobile-LCP driver — oversized product JPEGs (350/257/234 KB, PERF-2; the 667 KB hero in PERF-4) and **HEIC source files served raw** need re-exporting to WebP/AVIF at sane dimensions (Jenna's assets). PERF-14 (unsized images) and PERF-18 (LCP wants `fetchpriority=high`): the theme hero/header logos already carry intrinsic `width`/`height` and the first hero image already sets `fetchpriority="high"` (shipped) — the residual flags are an app-injected logo image and the collection/product LCP element, where adding `fetchpriority` blind risks mis-prioritizing a `loading="lazy"` card image. The mission's explicit "Image & asset loading."
- **Effort:** 3/5 — theme code done; oversized/HEIC re-exports are Jenna (content); any new `fetchpriority` needs the rendered page to pick the true LCP element (browser-gated).
- **Impact:** 3/5 — Priority 3, and **field already passes**, so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 3 = **1.0**

## SYS-7 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-5, PERF-6, PERF-8, PERF-12, PERF-17, BP-1
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (559 KB), **Route's `protect.widget.js`/`protect.core.js` (already flagged for removal in `DEVELOPMENT.md`)**, DA-Restock, free-shipping bar, portable-wallets, GA. Together they drive uncached bytes (PERF-3), JS execution + main-thread + bootup time (PERF-5/8), unused + legacy JS (PERF-6/12), an unminified app script (PERF-17), and the console errors (BP-1: `ERR_BLOCKED_BY_CLIENT`, 400/403, CSP frame-ancestors). **PERF-1 frames it:** mobile lab 62–70, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, **not theme files** — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus a cleaner Best-Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-8 · Theme CSS & layout-shift path
- **Findings:** PERF-7, PERF-9, PERF-10, PERF-11, PERF-13, PERF-15, PERF-16, PERF-19
- **The system:** The theme's render path and CLS. `base.css` render-blocks ~1,201 ms with component CSS behind it (PERF-11/19); unused CSS (PERF-10, 93 KB) and an unminified app-injected `RM Neue` `@font-face` (PERF-16); a forced reflow in app + page JS (PERF-7); CLS culprits + large shifts on the cart/logo/Mailchimp (PERF-9/13); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-15 — ~4 KB). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, the CLS culprits are app/cart widgets, and PERF-15 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-7 (28 KB render-blocking, 4 KB dup JS).
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-9 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` shipped**; the crawl reads response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no `<meta>` equivalent** — it's a response header, platform/edge-controlled on Shopify — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Hero slideshow accessible naming | 4 | 1 | 4.0 | Priority-1 a11y; the one clean theme-code win — re-diagnosed (visible counter, not markup), drop the aria-label + un-hide counter to match the passing desktop block |
| 2 | SYS-2 · Heading outline (last 2 pages) | 3 | 2 | 1.5 | a11y + SEO, cascade validated (185→2); the 2 remainders live in admin page bodies (content) |
| 3 | SYS-3 · Third-party embed a11y | 3 | 2 | 1.5 | needed for a11y-100, but entirely human-owned (Mailchimp app-config/decision) |
| 4 | SYS-4 · Image alt at scale | 4 | 4 | 1.0 | dual-priority; theme side closed (axe 4→0), meaningful alt is content |
| 5 | SYS-5 · Page metadata uniqueness | 3 | 3 | 1.0 | SEO; 4 dup titles + 9 dup descriptions are admin renames/rewrites |
| 6 | SYS-6 · Image delivery & sizing | 3 | 3 | 1.0 | mission asset-loading gap; theme dims/fetchpriority done, re-exports are content |
| 7 | SYS-7 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination, app-injected |
| 8 | SYS-8 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 9 | SYS-9 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy done, Permissions-Policy platform-bound |

The shape of it: the structural cascade is **live, validated, and closed** (185→2). The cycle's one remaining piece of clean, contained, source-grounded **theme code is SYS-1** — the hero slideshow naming, re-diagnosed from the counter conflict that `strip_html` never touched. Every system below it is content (Jenna/Britni: SYS-2, SYS-4, SYS-5, SYS-6 re-exports), an app/business decision (SYS-3, SYS-7), platform (SYS-9 Permissions-Policy), or a browser-gated CSS/JS slice (SYS-8).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-20** (slowest URLs) — slowest page 0.79 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-2** (inspector-issues) — no detail surfaced; revisit only if Best Practices must reach 95.
- **BP-3 / BP-4** (invalid / duplicate inline SVG) — "0 critical, N warning"; Dawn/platform-level cosmetic DOM flags. Defer. (BP-1 console errors carried under SYS-7.)
- **BP-5 / BP-6** (WebP / AVIF "support") — "0 critical, 1 warning" each; platform/CDN format flags, not a theme defect. Defer.

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. The budget flows to **rank 1 (SYS-1)** — the top of, and the whole of, the *unshipped, safely-authorable* theme code. Every system below it is handed to its proven owner (content → Jenna/Britni, app/business → Brenda/Jenna/Mason, platform → Shopify support, browser-gated → a dedicated PR). After execution, re-baseline and diff the next cycle: **whether A11Y-1 finally drops off 3 nodes** is the direct test of this re-diagnosis, just as **skipped-level 185→2** proved the last one.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `diff.md` — what moved vs 2026-06-21 (the heading cascade landing).
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
