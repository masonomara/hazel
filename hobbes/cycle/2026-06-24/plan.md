# Plan — 2026-06-24

Site: https://hazelboutique.com/ · Cycle: 2026-06-24 · Authored by Hobbes from `findings.md` + `baseline.md` + `diff.md` + `raw/`.

The 31 findings, grouped into **8 systems** plus an explicit won't-chase list, ordered by leverage. Every finding lands in exactly one system or the won't-chase list — nothing dropped, nothing invented. Findings are fixed; effort and impact are my judgment, rated against `MISSION.md`, `DEVELOPMENT.md`, and `CONTEXT.md`.

> **What this cycle's re-measurement settles.** The a11y front is clean and the wins are banked. `diff.md` confirms **`frame-title` 6 → 0** (the Mailchimp popup shim landed), so **§D axe now shows 0 failing audits on all six golden runs** and Lighthouse Accessibility reads **100 on every golden page × device**. Today's search-app shim (`snippets/a11y-search-app.liquid`, merged in #22) names the runtime-injected `isp_*` search box + watermark; it's in `main` but **not yet published**, so the §F crawl still reads "missing aria-labels: 1" until it goes live. With both the golden-path axe surface clean and the search-app shim banked, the prior runs' theme levers are spent — so this run's question was: *what theme-authorable defect is still open that the last several runs didn't catch?* The answer is **PERF-14 (unsized images)** — and it's a real one the prior plans walked past.

**The strategy in one line:** the a11y surface is clean and banked, so the one genuinely-open, theme-authorable defect this run is the **footer logos shipping invalid `width="100%" height="auto"` attributes** (PERF-14) — a real CLS lever on Collection + Product that prior runs missed by verifying only the hero/header logos — so it leads, with a theme-wide sweep of the same anti-pattern; everything below it is content, app-config, platform, or browser-gated.

**Three realities that shaped every rating:**
- **Field passes; lab is noise.** Baseline §C: CrUX (real users) passes LCP/INP/CLS on all three golden pages (all ✓). The "3 field regressions" in `diff.md` are sub-millisecond / single-ms CrUX jitter (Collection LCP 0.737→0.747 = +10µs; Home INP 105→111; Product INP 102→103) — still comfortably "good," not a real-user move. Meanwhile §A lab perf swung hard the *other* way this run (Collection-mobile 58→45, Home-mobile 63→56, Product-mobile 45→39) while CrUX held — PSI's fixed-throttle volatility over app-injected JS. Every performance system serves the *lab-score* target (mission §3, "≥ 90"), not a shopper, and is dampened accordingly. **CLS specifically already passes in the field** (Home 0.08, Collection 0.01, Product 0.0), so PERF-14 is a code-correctness + lab lever, not a real-user emergency.
- **Resource ≠ "code."** Most of this catalog is **content or app/platform**, not Liquid Hobbes can author: meaningful per-product alt at scale (SEO-1), 5 duplicate descriptions (SEO-2), oversized/HEIC source files (PERF-2/5), the heading-order residue in two admin page bodies (A11Y-1's structural warnings), the installed-app JS bundles (the PERF/BP cluster), and `Permissions-Policy` (platform/edge). Effort names the resource each time.
- **The safe theme front is nearly exhausted — but not empty.** The heading cascade (cart-drawer `card_heading_tag`, 185→2), card-image alt fallback, slideshow/pagination labels, hero-logo dims + LCP `fetchpriority`, the Referrer-Policy meta, the hero label fix, the Mailchimp `frame-title` shim, and today's search-app shim are all in `main`. What prior plans declared closed under "image sizing" — `width`/`height` on logos — they verified for the **hero and header** only. The **footer** logos (and two off-path content images) still carry the invalid `width="100%" height="auto"` pattern. That is the one unshipped, theme-authorable lever this run (SYS-1).

> Formula: ordered by **leverage = Impact ÷ Effort** (high impact, low cost, first), not the brief's literal `impact × effort` — which would surface the hardest work first and bury the quick wins. Scores are 1–5.

---

## SYS-1 · Image sizing — unsized images & CLS
- **Findings:** PERF-14, and the theme-side of PERF-18
- **The system:** Lighthouse flags **unsized images** on 2 golden pages (PERF-14) — evidence names alt `"Hazel Boutique"` and `hazel-mobile-logo.png?v=1713641093&width=760`. Both trace to the **footer logos** in `sections/footer.liquid` (the non-index footer block), which set `width="100%" height="auto"` — *invalid* HTML dimension attributes (the `width`/`height` content attributes accept integer pixels, not `%`/`auto`), so the browser gets no reliable aspect ratio and reserves the wrong box → layout shift as the image loads. Prior plans recorded "hero/header logos carry intrinsic width/height (verified)" and called image-sizing done — but never checked the **footer** logos, which are the actual PERF-14 culprit (the hero block renders on `/`, the footer block on Collection + Product, which is exactly where PERF-14 fired). A repo sweep finds the same anti-pattern in two more spots off the golden path: `snippets/icon-with-text.liquid` (`width="auto" height="auto"`) and `sections/main-page.liquid` (the `/pages/our-story` hero + script-logo). PERF-18 ("`fetchpriority=high` should be applied," 1 page) is partly here: the hero already sets it; the residual LCP element is the collection/product card image, browser-gated (see SYS-7). The fix is the web-standard pattern — real intrinsic `width`/`height` on the `<img>` (for the aspect-ratio box) + CSS `width:100%; height:auto` for responsive display — and the dims are known: the hero declares the same logo files (script-logo 4335×531, hazel-mobile-logo 760×316 as served); the content images measured from the CDN (our-story hero 2367×3247, our-story title 1729×493); `icon-with-text` uses Shopify image objects that carry their own `.width`/`.height`.
- **Effort:** 1/5 — Mason; a handful of attribute swaps + small additive CSS, self-contained, known dims, no Dawn-core restyle, no `settings_data.json`. Bucket-2: a layout-affecting change, so browser-confirm at review (footer logos still full-width on Collection/Product mobile + desktop; no new shift).
- **Impact:** 3/5 — Priority 3 (CLS is a Core Web Vital); fixes invalid markup and removes the only *measured, theme-authorable* PERF flag on the golden path (PERF-14, 2 pages), and serves the mission's explicit "Image & asset loading." Dampened because **field CLS already passes** (§C), so the real-user gain is small — the win is the lab flag + valid, shift-safe markup.
- **Priority:** 3 ÷ 1 = **3.0**

## SYS-2 · Heading outline & structural a11y
- **Findings:** A11Y-1
- **The system:** A11Y-1 rolls up SiteOne's element-level a11y prevalence — **1,699 flagged elements across 179 pages**, of which **1,698 are "HTML structural" warnings** (the heading-order family) and **1 is an unnamed link/button**. The §F rollup pins the real remainder: **1 page with multiple H1** and **2 with skipped heading levels**. The cart-drawer `card_heading_tag` cascade already cleared the bulk (185→2, banked in `main`); what's left lives in **admin-authored page bodies** rendered through `sections/main-page.liquid` as `<h1>{{ page.title }}</h1>` + `{{ page.content }}` — a second `<h1>` / skipped level inside `/pages/search-results` (also partly `isp_*` search-app markup) and the size-chart sub-heads on `/pages/sizing` jumping to `<h3>`. The theme renders exactly one correct `<h1>`; the strays are in content the repo can't reach. The single unnamed link/button is the search-app control already named by today's shim (awaiting publish).
- **Effort:** 2/5 — small, but **content, not code**: edit two page bodies in the admin (demote the stray search-results h1; insert the missing `<h2>` on sizing). Jenna/Britni in the theme editor — the theme repo can't reach `{{ page.content }}`.
- **Impact:** 3/5 — Priority 1 + 2 (structure serves a11y and SEO), but only 2–3 of 179 pages remain; the cascade already banked the win and §D axe is clean.
- **Priority:** 3 ÷ 2 = **1.5**

## SYS-3 · Image alt coverage
- **Findings:** SEO-1
- **The system:** `alt` coverage across the golden pages (Home 19/43, Collection 45/88, Product 16/24 `<img>` missing alt). Two tracks: **(a) Theme — done.** The product-card featured image binds `alt` to the product title (merged); a full theme `<img>` sweep confirms every live theme image carries an `alt` (the only bare one is in the fully comment-disabled `recent-viewed-product-js.liquid`, never rendered), and today's search-app shim adds the empty `alt` to the `isp_watermark_img`. **(b) Content + apps — open.** The remaining counts are admin product images the merchant left blank plus app-injected widget images (Judge.me, Instafeed); the count also includes decorative hover images correctly `alt=""`.
- **Effort:** 4/5 — theme side shipped (a 1); meaningful alt across the catalog is the cost (client content at scale, ongoing) — Jenna/Britni.
- **Impact:** 4/5 — dual priority (a11y + SEO), but §D axe `image-alt` already reads 0 on the golden path; the residue is content quality + partly decorative-by-design, so dampened.
- **Priority:** 4 ÷ 4 = **1.0**

## SYS-4 · Page metadata uniqueness
- **Findings:** SEO-2
- **The system:** 5 sets of duplicate meta descriptions — "Hazel Boutique" ×5, a repeated 18 oz candle spec ×4, repeated EVI11 vintage copy ×4/×2, a bracelet line ×2. (Duplicate **titles** are already gone — fixed in admin a prior cycle; only descriptions remain.) The templated head fallback already gives every page *a* description; making genuinely-similar product/collection pages *unique* is bespoke copy, not a theme mechanism — admin rewrites, Jenna/Britni.
- **Effort:** 2/5 — no code; ~9 admin description rewrites, Jenna/Britni.
- **Impact:** 2/5 — Priority 2, but bounded and the golden-path SEO score already reads 100.
- **Priority:** 2 ÷ 2 = **1.0**

## SYS-5 · Image delivery & weight
- **Findings:** PERF-2, PERF-5
- **The system:** Images are the heaviest payload class and the mobile-LCP driver — oversized product JPEGs (350/257/234 KB, PERF-2), **HEIC source files served raw** (the 78/51 KB `.heic` in PERF-2), and a 667 KB hero JPEG (PERF-5, which also lists the app JS bundles tracked under SYS-6). These need re-exporting to WebP/AVIF at sane dimensions — **source-asset work, Jenna's**, not a theme edit (the theme already requests CDN-resized variants; the source files themselves are too big). The mission's explicit "Image & asset loading." Note the overlap with SYS-1: SYS-1 fixes the *markup* (aspect ratio / CLS); SYS-5 fixes the *bytes* (re-export).
- **Effort:** 4/5 — content: oversized/HEIC re-exports are Jenna; ongoing, per-asset.
- **Impact:** 3/5 — Priority 3, and **field LCP already passes** (§C), so the lab lever is real but the real-user gain is small.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-6 · Third-party app JavaScript weight
- **Findings:** PERF-1, PERF-3, PERF-4, PERF-6, PERF-8, PERF-11, PERF-17, BP-1, BP-2
- **The system:** Installed apps inject the dominant JS drag — `shopify.widget.js` (558 KB), **Route's `protect.widget.js`/`protect.core.js` (already flagged for removal in `DEVELOPMENT.md`)**, DA-Restock, free-shipping bar, portable-wallets, GA. Together they drive uncached bytes (PERF-3, 1,420 KB), JS execution + bootup time (PERF-4), main-thread + reflow (PERF-8), unused + legacy JS (PERF-6/11), an unminified app script (PERF-17), and the console + inspector noise (BP-1/BP-2: `ERR_BLOCKED_BY_CLIENT`, 400/403, CSP frame-ancestors). **PERF-1 frames it:** mobile lab 39–67, CrUX passing. The fix is an app-by-app audit — drop what isn't earning its weight (start with Route), defer/async the rest. The scripts are app-injected, **not theme files** — no theme-repo edit reaches them.
- **Effort:** 4/5 — the biggest coordination cost: each app is a business decision + per-removal testing → app-config + Jenna/Britni/Brenda, not a change Mason makes alone.
- **Impact:** 3/5 — biggest *lab* lever, but **field passes**; the gain is the lab score plus cleaner Best Practices from killing console errors. Removing Route also banks an existing decision.
- **Priority:** 3 ÷ 4 = **0.75**

## SYS-7 · Theme CSS & layout-shift path
- **Findings:** PERF-7, PERF-9, PERF-10, PERF-12, PERF-13, PERF-15, PERF-16, PERF-19
- **The system:** The theme's render path and CLS culprits. `base.css` render-blocks ~1,132 ms with component CSS behind it (PERF-10/19); unused CSS (PERF-9, 93 KB) and an unminified app-injected `RM Neue` `@font-face` (PERF-16); a forced reflow in app + page JS (PERF-7); CLS culprits + large shifts on the collection/policies/product templates (PERF-12/13); two theme JS modules (`quick-add.js`, `product-form.js`) loaded duplicated across coexisting sections (PERF-15, ~4 KB). The realizable theme piece is small and **fiddly on a Dawn fork**: deferring `base.css` risks above-the-fold FOUC, the RM Neue/reflow items are app-injected, the CLS culprits are app/cart widgets, and PERF-15 has **no clean Liquid cross-section dedup** (sections can't share state; a global include would regress onto card-less pages) and is benign anyway (Dawn guards `customElements.define`). Every shippable change here needs the browser gate — distinct from SYS-1, whose dims are known and whose change is additive.
- **Effort:** 3/5 — theme code, but critical-CSS work is delicate on a fork and the JS dedup touches core commerce paths; all of it needs the browser gate this run can't run.
- **Impact:** 2/5 — Priority 3, field passes, numbers small next to SYS-6 (28 KB render-blocking, 4 KB dup JS).
- **Priority:** 2 ÷ 3 = **0.67**

## SYS-8 · Security response headers
- **Findings:** SEC-1
- **The system:** `Referrer-Policy` and `Permissions-Policy` are unset as **HTTP headers** (SEC-1); HSTS and CSP pass. The **Referrer-Policy `<meta>` shipped** (in `theme.liquid`); the crawl reads response headers, so the meta won't flip the header row, but it is the settable mitigation on a hosted platform. `Permissions-Policy` has **no `<meta>` equivalent** — it's a response header, platform/edge-controlled on Shopify — so it's a confirm-and-escalate (Shopify support), not a theme change.
- **Effort:** 2/5 — Referrer-Policy done; Permissions-Policy is investigation only.
- **Impact:** 1/5 — security is not a mission priority; the lower-severity pair. Lowest leverage.
- **Priority:** 1 ÷ 2 = **0.5**

---

## Order — highest leverage first

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Image sizing (unsized images / CLS) | 3 | 1 | 3.0 | the one unshipped theme-authorable defect — footer logos ship invalid `width="100%" height="auto"` (PERF-14, golden path); known dims, additive CSS, theme-wide sweep |
| 2 | SYS-2 · Heading outline & structural a11y | 3 | 2 | 1.5 | a11y + SEO; cascade banked (185→2), the 2–3 remainders live in admin page bodies (content) |
| 3 | SYS-3 · Image alt coverage | 4 | 4 | 1.0 | dual-priority; theme side closed (axe image-alt 0), meaningful alt is content |
| 4 | SYS-4 · Page metadata uniqueness | 2 | 2 | 1.0 | SEO; dup titles fixed, 5 dup descriptions remain — admin rewrites |
| 5 | SYS-5 · Image delivery & weight | 3 | 4 | 0.75 | mission asset-loading gap; oversized/HEIC re-exports are content |
| 6 | SYS-6 · Third-party app JS | 3 | 4 | 0.75 | biggest lab lever, but field passes + heavy human coordination, app-injected |
| 7 | SYS-7 · Theme CSS path | 2 | 3 | 0.67 | small bytes, fiddly on the fork, field passes, needs browser gate |
| 8 | SYS-8 · Security headers | 1 | 2 | 0.5 | not a mission priority; Referrer-Policy done, Permissions-Policy platform-bound |

The shape of it: the heading cascade is **live and closed** (185→2), §D axe is **fully clean** on the golden path (`frame-title` 6→0 this cycle), and the search-app shim is merged awaiting publish. The run's one remaining piece of unshipped, theme-authorable code is **SYS-1** — giving the footer logos (and two off-path content images) real intrinsic dimensions so the unsized-image flag clears and the markup is valid + shift-safe. Every system below it is content (Jenna/Britni: SYS-2 page bodies, SYS-3 alt, SYS-4 descriptions, SYS-5 re-exports), an app/business decision (SYS-6 app JS), platform (SYS-8 Permissions-Policy), or a browser-gated CSS/JS slice (SYS-7).

## Won't-chase this cycle (coverage, with reasons)

Listed so coverage is total — every finding accounted for, none silently dropped.

- **PERF-20** (slowest URLs) — slowest page 0.95 s, every URL < 1 s and 200. Server response healthy; nothing to fix.
- **SEC-2** (`Access-Control-Allow-Origin: *`) — on public CDN assets, where `*` is expected and benign. Confirm none credentialed, then leave.
- **BP-3 / BP-4** (invalid / duplicate inline SVG) — "0 critical, N warning"; the duplicate is Dawn's inlined icon set — Dawn/platform-level cosmetic DOM flags. Defer. (BP-1/BP-2 console + inspector noise carried under SYS-6.)
- **BP-5 / BP-6** (WebP / AVIF "support") — "0 critical, 1 warning" each; platform/CDN format flags, not a theme defect. Defer. (Image *bytes* are SYS-5; image *markup* is SYS-1.)

## The handoff

Execution works the table top-down, proving each system against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar. The budget flows to **rank 1 (SYS-1)** — the whole of the unshipped, theme-authorable code this run. Every system below it is handed to its proven owner (content → Jenna/Britni, app/business → Mason + Jenna/Brenda, platform → Shopify support, browser-gated CSS/JS → a dedicated PR). After execution, re-baseline and diff the next cycle: **whether PERF-14 drops its 2 flagged pages** is the direct test of this fix, just as **`frame-title` 6→0** confirmed the Mailchimp shim and **`label-content-name-mismatch` 3→0** the hero fix before it.

## Pointers

- `findings.md` — the problems this plan groups (cite the IDs).
- `baseline.md` — the numbers and field-vs-lab context.
- `diff.md` — what moved vs 2026-06-23 (`frame-title` 6→0; the 3 field "regressions" are sub-ms CrUX jitter, all still ✓).
- `MISSION.md` — what impact is rated against.
- `DEVELOPMENT.md` · `CONTEXT.md` — the stack, constraints, and people behind every effort estimate.
