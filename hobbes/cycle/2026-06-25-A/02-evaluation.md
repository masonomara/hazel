# Findings — 2026-06-25-A

Site: https://hazelboutique.com/ · Generated 2026-06-25 17:13 EDT by `hobbes/tools/evaluation.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 30 findings. Every failing check is enumerated straight from `raw/` — no shortlist, no mission weighting, no hand-picking; same raw always yields the same findings. Where a list is long it is capped with an explicit `+N more`, never silently trimmed. Numbers and scorecard in `01-baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/templates/02-evaluation-template.md`.

## A11Y — Accessibility

### A11Y-1 · label-content-name-mismatch — 55 node(s)
- **What / why:** A control's visible text isn't contained in its accessible name. Voice-control users can't activate it by its visible label. Common on slideshow/hero slide links and pagination, where an aria-label omits the visible text.
- **Source:** PSI Lighthouse · accessibility · `label-content-name-mismatch`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 55 node(s), 3 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — mobile
- **Evidence:**
  - `div.collection > ul#product-grid > li.grid__item > a#CardLink-template--26596969251130__product-gri…`
  -   ↳ <a class="card-wrapper product-card-wrapper underline-links-hover" href="/products/the-sunday-brunch-shorts-white" id="…
  - `div.collection > ul#product-grid > li.grid__item > a#CardLink-template--26596969251130__product-gri…`
  -   ↳ <a class="card-wrapper product-card-wrapper underline-links-hover" href="/products/the-sunday-brunch-mockneck-white" id…
  - `div.collection > ul#product-grid > li.grid__item > a#CardLink-template--26596969251130__product-gri…`
  -   ↳ <a class="card-wrapper product-card-wrapper underline-links-hover" href="/products/the-sunday-brunch-barrel-pants-dusty…
  - (+52 more node(s) — see raw/*.psi.json)

### A11Y-2 · Sitewide a11y prevalence
- **What / why:** How widespread the a11y gaps are across the whole site — element-level counts. SiteOne's per-analysis totals over every crawled page: real element counts, not the blunt one-flag-per-page rollup. The PSI rules above are authoritative for the golden path; this shows the scale beyond it.
- **Source:** SiteOne crawl · accessibility table
- **Target → measured:** 0 issues (BASELINE §F) → 168 flagged element(s) across 179 pages
- **Scope:** sitewide: 179 pages crawled
- **Evidence:**
  - HTML structural issues: 0 critical, 167 warning
  - Unnamed links/buttons: 0 critical, 1 warning

## SEO — SEO & discoverability

### SEO-1 · Image alt coverage
- **What / why:** Images on the page with no alt attribute (coverage, not quality). Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Content/card images get alt from the CMS/admin image field or the template <img>.
- **Source:** seo.py · golden path
- **Target → measured:** All images have alt (BASELINE §E) → golden pages failing: Home, Collection, Product
- **Scope:** golden path: Home, Collection, Product
- **Evidence:**
  - golden Home: 15 of 44 img(s) missing alt
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ IMG_3438.png?v=1772741674&width=32
  -   ↳ EE0A3F42-0DCE-4D63-875E-478BF0D96F0D.jpg?v=1781812644&width…
  -   (+12 more on this page)
  - golden Collection: 41 of 89 img(s) missing alt
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ IMG_3438.png?v=1772741674&width=32
  -   ↳ EE0A3F42-0DCE-4D63-875E-478BF0D96F0D.jpg?v=1781812644&width…
  -   (+38 more on this page)
  - golden Product: 2 of 25 img(s) missing alt
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ IMG_3438.png?v=1772741674&width=32

### SEO-2 · Duplicate meta descriptions
- **What / why:** Two or more pages share an identical meta description. Duplicate descriptions blur how pages differ in search and weaken each snippet; templated descriptions repeated across products/collections are the usual cause. (Empty descriptions are counted in the missing-description finding above, not here.)
- **Source:** SiteOne crawl · non-unique-descriptions
- **Target → measured:** 0 duplicate descriptions (BASELINE §F) → 5 duplicated description(s)
- **Evidence:**
  - "Hazel Boutique" ×5
  - "Fill (oz): 18 Fill (g/ml): 510 Natural Wick(s): 1 Vegan Imperial Dime…" ×4
  - "Evi11 Twin Vintage One of A Kind Pre- Loved ( may have minor rips / s…" ×4
  - "14k Gold Bracelet Hazel Bracelet Each Bracelet Sold Separately" ×2
  - "EVI11 TWIN VINTAGE ONE OF A KIND PRE- LOVED ( MAY HAVE MINOR RIPS / S…" ×2

## PERF — Performance

### PERF-1 · Lab performance below target
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in 01-baseline.md §C: CrUX may already pass even where lab fails. The pass bar is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (BASELINE Targets) → score range 52–74 across runs (see §A)
- **Scope:** golden path: all golden pages × device
- **Evidence:**
  - Home — mobile: perf 54 · LCP 27.34s · TBT 167.0ms · SI 9.4s · CLS 0.0
  - Home — desktop: perf 58 · LCP 2.22s · TBT 421.0ms · SI 1.66s · CLS 0.202
  - Collection — mobile: perf 52 · LCP 23.81s · TBT 296.0ms · SI 7.43s · CLS 0.0
  - Collection — desktop: perf 55 · LCP 1.67s · TBT 305.0ms · SI 1.42s · CLS 1.008
  - Product — mobile: perf 61 · LCP 15.45s · TBT 172.0ms · SI 6.19s · CLS 0.06
  - Product — desktop: perf 74 · LCP 1.64s · TBT 251.0ms · SI 1.15s · CLS 0.202

### PERF-2 · Improve image delivery
- **What / why:** Reducing the download time of images can improve the perceived load time of the page and LCP. Learn more about optimizing image size
- **Source:** PSI Lighthouse · performance · `image-delivery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2390 KB across 49 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 375 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 275 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 251 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 78 KB
  - 8E51D4A2-B7CC-49AF-8275-DB0CA3823575.jpg?v=1780627667&width… · 65 KB
  - B63E7E4D-8A47-4FF8-A0EB-50A2E2099CA7.jpg?v=1781808485&width… · 58 KB
  - A0A8C32C-CEAC-4D84-B603-3C7749016C49.jpg?v=1781235184&width… · 56 KB
  - 639CDF20-2DC2-4050-984B-8D3C37151A52.jpg?v=1781808485&width… · 52 KB
  - (+41 more — see raw/*.psi.json)

### PERF-3 · Use efficient cache lifetimes
- **What / why:** A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
- **Source:** PSI Lighthouse · performance · `cache-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1422 KB across 23 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 400 KB
  - protect.widget.js · 109 KB
  - embed.js · 75 KB
  - portable-wallets.en.js · 75 KB
  - protect.core.js?shop=hazelboutique.com · 56 KB
  - popup.js · 34 KB
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 23 KB
  - (+15 more — see raw/*.psi.json)

### PERF-4 · Avoid enormous network payloads
- **What / why:** Large network payloads cost users real money and are highly correlated with long load times. Learn how to reduce payload sizes.
- **Source:** PSI Lighthouse · performance · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3397 KB across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 667 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 389 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 286 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 261 KB
  - hydrate.B1HJu2AB.js · 209 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 183 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 156 KB
  - (+7 more — see raw/*.psi.json)

### PERF-5 · Reduce JavaScript execution time
- **What / why:** Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to reduce Javascript execution time.
- **Source:** PSI Lighthouse · performance · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 4194 ms across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - all-hazel-brand · 848 ms
  - the-capri-collection-baby-pink · 644 ms
  - Unattributable · 625 ms
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 579 ms
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 279 ms
  - loader.js · 198 ms
  - embed.js · 182 ms
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 141 ms
  - (+7 more — see raw/*.psi.json)

### PERF-6 · Reduce unused JavaScript
- **What / why:** Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. Learn how to reduce unused JavaScript.
- **Source:** PSI Lighthouse · performance · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 754 KB across 10 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 392 KB
  - js?id=G-G3RDTGKWR4 · 83 KB
  - protect.widget.js · 50 KB
  - portable-wallets.en.js · 43 KB
  - freeshippingbar.js?shop=hazelboutiquenj.myshopify.com · 36 KB
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 36 KB
  - embed.js · 33 KB
  - popup.js · 29 KB
  - (+2 more — see raw/*.psi.json)

### PERF-7 · Minimize main-thread work
- **What / why:** Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to minimize main-thread work
- **Source:** PSI Lighthouse · performance · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3873 ms across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 1852 ms
  - Other · 663 ms
  - Script Parsing & Compilation · 526 ms
  - Style & Layout · 514 ms
  - Garbage Collection · 181 ms
  - Parse HTML & CSS · 75 ms
  - Rendering · 63 ms

### PERF-8 · Reduce unused CSS
- **What / why:** Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. Learn how to reduce unused CSS.
- **Source:** PSI Lighthouse · performance · `unused-css-rules` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 93 KB across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 29 KB
  - :root,[data-bs-theme="light"]{--bs-blue: #0d6efd;--bs-indigo: #6610f2;--bs-purple: #6f42c… · 26 KB
  - base.css?v=50063936332897354731782337201 · 15 KB
  - instafeed-17.10.0.css · 11 KB
  - widget_v3_base.css · 11 KB

### PERF-9 · Forced reflow
- **What / why:** A forced reflow occurs when JavaScript queries geometric properties (such as offsetWidth) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about forced reflows and possible mitigations.
- **Source:** PSI Lighthouse · performance · `forced-reflow-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 137 ms across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify-perf-kit-3.6.0.min.js · 35 ms
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 33 ms
  - the-capri-collection-baby-pink · 33 ms
  - 14787_1767154164.js?category=bis&v=6&shop=hazelboutiquenj.m… · 32 ms
  - global.js?v=11113922878925400371771610528 · 4 ms

### PERF-10 · Render-blocking requests
- **What / why:** Requests are blocking the page's initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.
- **Source:** PSI Lighthouse · performance · `render-blocking-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 28 KB across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - base.css?v=50063936332897354731782337201 · 20 KB · 1468 ms
  - accelerated-checkout-backwards-compat.css · 3 KB · 490 ms
  - component-slider.css?v=76902739753078838911779286626 · 3 KB · 164 ms
  - component-slideshow.css?v=128144104580933199301771610528 · 2 KB · 490 ms

### PERF-11 · LCP breakdown
- **What / why:** Each subpart has specific improvement strategies. Ideally, most of the LCP time should be spent on loading the resources, not within delays.
- **Source:** PSI Lighthouse · performance · `lcp-breakdown-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2637 ms across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Element render delay · 1978 ms
  - Resource load delay · 438 ms
  - Resource load duration · 210 ms
  - Time to first byte · 11 ms

### PERF-12 · Legacy JavaScript
- **What / why:** Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren't necessary for modern browsers. Consider modifying your JavaScript build process to not transpile Baseline features, unless you know you must support older browsers. Learn why most sites can deploy ES6+ code without transpiling
- **Source:** PSI Lighthouse · performance · `legacy-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 23 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - protect.core.js?shop=hazelboutique.com · 10 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 7 KB
  - portable-wallets.en.js · 6 KB

### PERF-13 · Duplicated JavaScript
- **What / why:** Remove large, duplicate JavaScript modules from bundles to reduce unnecessary bytes consumed by network activity.
- **Source:** PSI Lighthouse · performance · `duplicated-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 4 KB across 2 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - /cdn/shop/t/51/assets/quick-add.js?v=131073536309624707681771610528 · 2 KB
  - /cdn/shop/t/51/assets/product-form.js?v=3603548357138963301771610529 · 2 KB

### PERF-14 · Minify CSS
- **What / why:** Minifying CSS files can reduce network payload sizes. Learn how to minify CSS.
- **Source:** PSI Lighthouse · performance · `unminified-css` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 6 KB

### PERF-15 · Minify JavaScript
- **What / why:** Minifying JavaScript files can reduce payload sizes and script parse time. Learn how to minify JavaScript.
- **Source:** PSI Lighthouse · performance · `unminified-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - d9aa649c0e2ad063e057bdd8c.js?shop=hazelboutiquenj.myshopify… · 3 KB

### PERF-16 · LCP request discovery
- **What / why:** Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
- **Source:** PSI Lighthouse · performance · `lcp-discovery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 1 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - fetchpriority=high should be applied

### PERF-17 · Network dependency tree
- **What / why:** Avoid chaining critical requests by reducing the length of chains, reducing the download size of resources, or deferring the download of unnecessary resources to improve page load.
- **Source:** PSI Lighthouse · performance · `network-dependency-tree-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 3 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - (see raw/*.psi.json)

### PERF-18 · Slowest URLs (server response, sitewide)
- **What / why:** The slowest pages to respond across the whole crawl — server response / TTFB-class timing. SiteOne's per-URL request timing, a broad complement to the golden-path lab metrics. Slow server response delays everything downstream; a consistently slow template or collection is worth a look even when the golden path looks fine.
- **Source:** SiteOne crawl · slowest-urls
- **Target → measured:** Fast server response, all pages (BASELINE Targets) → slowest 0.67s; top 20 listed
- **Scope:** sitewide: 20 slowest of crawl
- **Evidence:**
  - 40-final-sale · 0.67s (200)
  - best-selling-collection · 0.62s (200)
  - sets · 0.62s (200)
  - the-charlotte-set · 0.59s (200)
  - all-accessories · 0.59s (200)
  - vintage · 0.58s (200)
  - all-home-decor · 0.57s (200)
  - home · 0.53s (200)
  - evil-twin-utep-vintage-tee · 0.53s (200)
  - new-accessories · 0.50s (200)
  - over-100 · 0.49s (200)
  - 14k-gold-filled · 0.49s (200)
  - (+8 more — see raw/crawl.json)

## SEC — Security

### SEC-1 · Missing security response headers
- **What / why:** Standard hardening headers absent from responses. These reduce XSS, clickjacking, and referrer-leak exposure. On a hosted platform the host often sets some headers and limits what the app/template can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.
- **Source:** SiteOne crawl · security table
- **Target → measured:** All present (BASELINE §F) → 2 of 4 missing
- **Scope:** sitewide: all responses
- **Evidence:**
  - Referrer-Policy: not set — Referrer-Policy header is not set. It controls referrer header sharing and enhances privacy and security.
  - Permissions-Policy: not set — Permissions-Policy header is not set. It allows enabling/disabling browser APIs and features for security.

### SEC-2 · Access-Control-Allow-Origin: *
- **What / why:** A response allows any origin to read it. Usually fine for public CDN assets, a risk if it's on anything credentialed. Check which responses carry it.
- **Source:** SiteOne crawl · security table
- **Target → measured:** No over-permissive CORS → flagged
- **Scope:** sitewide: flagged responses
- **Evidence:**
  - Access-Control-Allow-Origin is set to '*' which allows any origin to access the resource. This can be a security risk.

## BP — Best practices / structure

### BP-1 · errors-in-console
- **What / why:** JavaScript errors logged to the browser console. Each is a script failing at runtime — broken behavior, often from a third-party embed or a first-party script. Read the messages; they name the file.
- **Source:** PSI Lighthouse · best-practices · `errors-in-console`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 6 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
  - Failed to load resource: the server responded with a status of 400 (Bad Request)
  - Failed to load resource: the server responded with a status of 403 ()
  - Framing 'https://shop.app/' violates the following Content Security Policy directive: "frame-ancestors 'self' https://s…
  - (+4 more)

### BP-2 · inspector-issues
- **What / why:** Issues Chrome's Issues panel flagged (cookies, mixed content, etc.). Browser-level warnings; open the raw audit for the specifics.
- **Source:** PSI Lighthouse · best-practices · `inspector-issues`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 3 run(s)
- **Scope:** golden path: Collection — mobile, Home — desktop, Home — mobile
- **Evidence:**
  - (see raw/*.psi.json)

### BP-3 · Invalid inline SVGs
- **What / why:** Invalid inline SVGs — flagged sitewide by the crawl. Malformed inline SVG markup — can render wrong or bloat the DOM. Usually a template partial or a third-party-injected icon.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 10 warning
- **Scope:** sitewide: of 179 pages
- **Evidence:**
  - 0 critical, 10 warning — see raw/crawl.json

### BP-4 · Duplicate inline SVGs
- **What / why:** Duplicate inline SVGs — flagged sitewide by the crawl. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common where an icon set is inlined per use — low priority.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 179 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl.json

### BP-5 · WebP support
- **What / why:** WebP support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open raw/crawl.json for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 179 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl.json

### BP-6 · AVIF support
- **What / why:** AVIF support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open raw/crawl.json for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 179 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl.json
