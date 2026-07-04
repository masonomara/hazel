# Findings — 2026-07-03-B

Site: https://hazelboutique.com/ · Generated 2026-07-03 19:52 EDT by `hobbes/tools/evaluation.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 30 findings. Every failing check is enumerated straight from `raw/` — no shortlist, no mission weighting, no hand-picking; same raw always yields the same findings. Where a list is long it is capped with an explicit `+N more`, never silently trimmed. Numbers and scorecard in `01-baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/templates/02-evaluation-template.md`.

## A11Y — Accessibility

### A11Y-1 · Missing aria labels (sitewide)
- **What / why:** Missing aria labels — flagged across the crawl. An interactive element has no accessible name (aria-label / aria-labelledby). A screen reader announces it by role alone — 'button', 'link', 'textbox'. This hits icon-only controls and unlabeled inputs like the search box.
- **Source:** SiteOne crawl · accessibility detail
- **Target → measured:** 0 issues (BASELINE §F) → 27199 element(s) across 100 pattern(s)
- **Scope:** sitewide: 177 page(s)
- **Evidence:**
  - [warning] ×3884 · `<a class="link link-* list-* list-*" *** >` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×3124 · `<a ***>` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×1528 · `<a class="card-* product-* underline-*" id="CardLink-template--26596969251130__product-grid-***" *** >` · /collections/harley-tees, /collections/best-selling-clothing, /collections/new-clothing (+2 more)
  - [warning] ×885 · `<button class="menu-* link link-* focus-*" *** >` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×531 · `<a class="button" *** >` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×354 · `<a class="megaMenuCollection" *** >` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - (+94 more pattern(s) — see raw/crawl-report.html)

### A11Y-2 · Missing roles (sitewide)
- **What / why:** Missing roles — flagged across the crawl. A landmark or interactive element has no role, so assistive tech can't place it in the page structure or navigate to it.
- **Source:** SiteOne crawl · accessibility detail
- **Target → measured:** 0 issues (BASELINE §F) → 1129 element(s) across 7 pattern(s)
- **Scope:** sitewide: 177 page(s)
- **Evidence:**
  - [warning] ×354 · `<header class="header header-* header-* page-* header-* header-*">` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×177 · `<nav class="menu-*">` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×177 · `<nav class="header_* nutTestTest">` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×177 · `<footer class="footer color-* gradient section-*">` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×177 · `<nav class="header_*">` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)
  - [warning] ×66 · `<aside class="facets-* page-*" id="main-collection-filters" *** >` · /collections/harley-tees, /collections/best-selling-clothing, /collections/new-clothing (+2 more)
  - (+1 more pattern(s) — see raw/crawl-report.html)

### A11Y-3 · Missing image alt (sitewide)
- **What / why:** Missing image alt — flagged across the crawl. An <img> has no alt attribute. A screen reader skips it or reads the filename. These are content/card images; alt comes from the admin image field or the template <img>.
- **Source:** SiteOne crawl · accessibility detail
- **Target → measured:** 0 issues (BASELINE §F) → 183 element(s) across 1 pattern(s)
- **Scope:** sitewide: 177 page(s)
- **Evidence:**
  - [warning] ×183 · `<img ***>` · /products/hzl-tank-top-baby-blue, /collections/harley-tees, /collections/best-selling-clothing (+2 more)

## SEO — SEO & discoverability

### SEO-1 · Image alt coverage
- **What / why:** Images on the page with no alt attribute (coverage, not quality). Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Content/card images get alt from the CMS/admin image field or the template <img>.
- **Source:** seo.py · golden path
- **Target → measured:** All images have alt (BASELINE §E) → golden pages failing: Home, Collection, Product
- **Scope:** golden path: Home, Collection, Product
- **Evidence:**
  - golden Home: 1 of 45 img(s) missing alt
  -   ↳ 59C10513-C6FA-48BC-A792-5C2409C4FAF8.png?v=1782922882&width…
  - golden Collection: 1 of 88 img(s) missing alt
  -   ↳ 59C10513-C6FA-48BC-A792-5C2409C4FAF8.png?v=1782922882&width…
  - golden Product: 1 of 25 img(s) missing alt
  -   ↳ 59C10513-C6FA-48BC-A792-5C2409C4FAF8.png?v=1782922882&width…

### SEO-2 · Duplicate meta descriptions
- **What / why:** Two or more pages share an identical meta description. Duplicate descriptions blur how pages differ in search and weaken each snippet; templated descriptions repeated across products/collections are the usual cause. (Empty descriptions are counted in the missing-description finding above, not here.)
- **Source:** SiteOne crawl · non-unique-descriptions
- **Target → measured:** 0 duplicate descriptions (BASELINE §F) → 8 duplicated description(s)
- **Evidence:**
  - "Evi11 Twin Vintage One of A Kind Pre- Loved ( may have minor rips / s…" ×5
  - "Hazel Boutique" ×5
  - "Ornaments ITEM MATERIAL: GLASS" ×2
  - "Evil Twin Vintage One Of A Kind One Size - Oversized Fit" ×2
  - "14k Gold Filled Necklace" ×2
  - "Tank Tops By HZL Stretchy Fit Comes in XS-LARGE 46.5% Rayon 46.5% Cot…" ×2
  - "Hazel Exclusive Printed Sweatpants Joggers with Pockets Matching Hood…" ×2
  - "18k Gold Plated Hypoallergenic" ×2

## PERF — Performance

### PERF-1 · Lab performance below target
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in 01-baseline.md §C: CrUX may already pass even where lab fails. The pass bar is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (BASELINE Targets) → score range 45–83 across runs (see §A)
- **Scope:** golden path: all golden pages × device
- **Evidence:**
  - Home — mobile: perf 45 · LCP 8.48s · TBT 157.0ms · SI 4.39s · CLS 1.084
  - Home — desktop: perf 70 · LCP 1.34s · TBT 103.0ms · SI 1.24s · CLS 1.0
  - Collection — mobile: perf 61 · LCP 12.93s · TBT 270.0ms · SI 4.42s · CLS 0.06
  - Collection — desktop: perf 62 · LCP 2.33s · TBT 123.0ms · SI 0.72s · CLS 1.0
  - Product — mobile: perf 61 · LCP 16.3s · TBT 283.0ms · SI 4.29s · CLS 0.06
  - Product — desktop: perf 83 · LCP 1.7s · TBT 96.0ms · SI 0.93s · CLS 0.194

### PERF-2 · Improve image delivery
- **What / why:** Reducing the download time of images can improve the perceived load time of the page and LCP. Learn more about optimizing image size
- **Source:** PSI Lighthouse · performance · `image-delivery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1282 KB across 42 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - 6A7D4890-31E0-4472-B81F-3FD80DEDE6FE.jpg?v=1782935211&width… · 249 KB
  - DFBAC904-3A89-4CEF-B414-E8CF8DBBE1BD.jpg?v=1782935268&width… · 156 KB
  - AEBE0FF0-2422-4DD1-AD96-1E75C8A22CF8.jpg?v=1782935268&width… · 155 KB
  - script-logo.png?v=1713629.5093 · 82 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 78 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 51 KB
  - E127AD96-E452-41C1-BA63-E911E78476D9.jpg?v=1782926062&width… · 39 KB
  - IMG-1767.jpg?v=1711642495&width=600 · 34 KB
  - (+34 more — see raw/*.psi.json)

### PERF-3 · Use efficient cache lifetimes
- **What / why:** A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
- **Source:** PSI Lighthouse · performance · `cache-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1416 KB across 23 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 400 KB
  - protect.widget.js · 109 KB
  - portable-wallets.en.js · 75 KB
  - embed.js · 70 KB
  - protect.core.js?shop=hazelboutique.com · 56 KB
  - popup.js · 34 KB
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 23 KB
  - (+15 more — see raw/*.psi.json)

### PERF-4 · Avoid enormous network payloads
- **What / why:** Large network payloads cost users real money and are highly correlated with long load times. Learn how to reduce payload sizes.
- **Source:** PSI Lighthouse · performance · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3195 KB across 16 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 667 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - 6A7D4890-31E0-4472-B81F-3FD80DEDE6FE.jpg?v=1782935211&width… · 278 KB
  - hydrate.DTH4K6uP.js · 210 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 183 KB
  - DFBAC904-3A89-4CEF-B414-E8CF8DBBE1BD.jpg?v=1782935268&width… · 174 KB
  - AEBE0FF0-2422-4DD1-AD96-1E75C8A22CF8.jpg?v=1782935268&width… · 172 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 156 KB
  - (+8 more — see raw/*.psi.json)

### PERF-5 · Reduce JavaScript execution time
- **What / why:** Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to reduce Javascript execution time.
- **Source:** PSI Lighthouse · performance · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3482 ms across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - all-hazel-brand · 779 ms
  - Unattributable · 522 ms
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 507 ms
  - the-capri-collection-baby-pink · 483 ms
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 220 ms
  - loader.js · 165 ms
  - jquery-2.2.4.min.js · 148 ms
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 137 ms
  - (+7 more — see raw/*.psi.json)

### PERF-6 · Reduce unused JavaScript
- **What / why:** Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. Learn how to reduce unused JavaScript.
- **Source:** PSI Lighthouse · performance · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 750 KB across 10 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 392 KB
  - js?id=G-G3RDTGKWR4 · 84 KB
  - protect.widget.js · 50 KB
  - portable-wallets.en.js · 43 KB
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 36 KB
  - freeshippingbar.js?shop=hazelboutiquenj.myshopify.com · 33 KB
  - embed.js · 31 KB
  - popup.js · 29 KB
  - (+2 more — see raw/*.psi.json)

### PERF-7 · Minimize main-thread work
- **What / why:** Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to minimize main-thread work
- **Source:** PSI Lighthouse · performance · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3205 ms across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 1488 ms
  - Other · 541 ms
  - Script Parsing & Compilation · 483 ms
  - Style & Layout · 428 ms
  - Garbage Collection · 120 ms
  - Parse HTML & CSS · 79 ms
  - Rendering · 66 ms

### PERF-8 · Forced reflow
- **What / why:** A forced reflow occurs when JavaScript queries geometric properties (such as offsetWidth) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about forced reflows and possible mitigations.
- **Source:** PSI Lighthouse · performance · `forced-reflow-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 127 ms across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - scripts.js?v=93736053516032179081771610579 · 37 ms
  - b4074779awe500cddcp1e53a49dm5f7c656em.js · 29 ms
  - the-capri-collection-baby-pink · 29 ms
  - / · 18 ms
  - global.js?v=11113922878925400371771610528 · 15 ms

### PERF-9 · Reduce unused CSS
- **What / why:** Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. Learn how to reduce unused CSS.
- **Source:** PSI Lighthouse · performance · `unused-css-rules` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 93 KB across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 29 KB
  - :root,[data-bs-theme="light"]{--bs-blue: #0d6efd;--bs-indigo: #6610f2;--bs-purple: #6f42c… · 26 KB
  - base.css?v=37222019180666774901782422959 · 15 KB
  - instafeed-17.10.0.css · 11 KB
  - widget_v3_base.css · 11 KB

### PERF-10 · Layout shift culprits
- **What / why:** Layout shifts occur when elements move absent any user interaction. Investigate the causes of layout shifts, such as elements being added, removed, or their fonts changing as the page loads.
- **Source:** PSI Lighthouse · performance · `cls-culprits-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 1 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - 01 SHOP HZL NEW 02 SHOP HZL NEW 03 SHOW HZL NEW
  - 01 SHOP HZL NEW 02 SHOP HZL NEW 03 SHOW HZL NEW NEW ARRIVALS VIEW MORE THE HZ…
  - HAZEL POLICIES
  - Hazel Boutique Mobile Logo
  - Intuit Mailchimp logo

### PERF-11 · Render-blocking requests
- **What / why:** Requests are blocking the page's initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.
- **Source:** PSI Lighthouse · performance · `render-blocking-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 28 KB across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - base.css?v=37222019180666774901782422959 · 20 KB · 1201 ms
  - accelerated-checkout-backwards-compat.css · 3 KB · 477 ms
  - component-slider.css?v=76902739753078838911779286626 · 3 KB · 160 ms
  - component-slideshow.css?v=128144104580933199301771610528 · 2 KB · 477 ms

### PERF-12 · Avoid large layout shifts
- **What / why:** These are the largest layout shifts observed on the page. Each table item represents a single layout shift, and shows the element that shifted the most. Below each item are possible root causes that led to the layout shift. Some of these layout shifts may not be included in the CLS metric value due to windowing. Learn how to improve CLS
- **Source:** PSI Lighthouse · performance · `layout-shifts` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 5 layout shifts found
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - 01 SHOP HZL NEW 02 SHOP HZL NEW 03 SHOW HZL NEW
  - 01 SHOP HZL NEW 02 SHOP HZL NEW 03 SHOW HZL NEW NEW ARRIVALS VIEW MORE THE HZ…
  - HAZEL POLICIES
  - Hazel Boutique Mobile Logo

### PERF-13 · Legacy JavaScript
- **What / why:** Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren't necessary for modern browsers. Consider modifying your JavaScript build process to not transpile Baseline features, unless you know you must support older browsers. Learn why most sites can deploy ES6+ code without transpiling
- **Source:** PSI Lighthouse · performance · `legacy-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 23 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - protect.core.js?shop=hazelboutique.com · 10 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 7 KB
  - portable-wallets.en.js · 6 KB

### PERF-14 · Duplicated JavaScript
- **What / why:** Remove large, duplicate JavaScript modules from bundles to reduce unnecessary bytes consumed by network activity.
- **Source:** PSI Lighthouse · performance · `duplicated-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 4 KB across 2 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - /cdn/shop/t/51/assets/quick-add.js?v=131073536309624707681771610528 · 2 KB
  - /cdn/shop/t/51/assets/product-form.js?v=3603548357138963301771610529 · 2 KB

### PERF-15 · Minify CSS
- **What / why:** Minifying CSS files can reduce network payload sizes. Learn how to minify CSS.
- **Source:** PSI Lighthouse · performance · `unminified-css` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 6 KB

### PERF-16 · Minify JavaScript
- **What / why:** Minifying JavaScript files can reduce payload sizes and script parse time. Learn how to minify JavaScript.
- **Source:** PSI Lighthouse · performance · `unminified-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - d9aa649c0e2ad063e057bdd8c.js?shop=hazelboutiquenj.myshopify… · 3 KB

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
- **Target → measured:** Fast server response, all pages (BASELINE Targets) → slowest 1.26s; top 20 listed
- **Scope:** sitewide: 20 slowest of crawl
- **Evidence:**
  - home · 1.26s (200)
  - the-hzl-hibiscus-tee · 1.23s (200)
  - the-camel-windbreaker · 1.06s (200)
  - 20-rack · 0.96s (200)
  - 14k-gold-filled-lucky-italian-horn-necklace · 0.96s (200)
  - new-arrivals-1 · 0.95s (200)
  - the-hb-hunter-hoodie · 0.95s (200)
  - all-hazel-brand · 0.89s (200)
  - the-hb-kimmie-crewneck · 0.89s (200)
  - all-accessories · 0.85s (200)
  - 30-rack · 0.85s (200)
  - shorts · 0.84s (200)
  - (+8 more — see raw/crawl.json)

## SEC — Security

### SEC-1 · Missing security response headers
- **What / why:** Standard hardening headers absent from responses. These reduce XSS, clickjacking, and referrer-leak exposure. On a hosted platform the host often sets some headers and limits what the app/template can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.
- **Source:** SiteOne crawl · security table
- **Target → measured:** All present (BASELINE §F) → 4 of 4 missing
- **Scope:** sitewide: all responses
- **Evidence:**
  - HSTS: not set (1 responses) — Strict-Transport-Security header is not set. It enforces secure connections and protects against MITM attacks.
  - CSP: not set (1 responses) — Content-Security-Policy header is not set. It restricts resources the page can load and prevents XSS attacks.
  - Referrer-Policy: not set (178 responses) — Referrer-Policy header is not set. It controls referrer header sharing and enhances privacy and security.
  - Permissions-Policy: not set (178 responses) — Permissions-Policy header is not set. It allows enabling/disabling browser APIs and features for security.

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
  - Failed to load resource: the server responded with a status of 429 (Too Many Requests)
  - qe: Error producing to the Monorail Edge. Response received: {"status":400,"message":"Invalid agent: Mozilla/5.0 (Linux…
  - (+3 more)

### BP-2 · inspector-issues
- **What / why:** Issues Chrome's Issues panel flagged (cookies, mixed content, etc.). Browser-level warnings; open the raw audit for the specifics.
- **Source:** PSI Lighthouse · best-practices · `inspector-issues`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 2 run(s)
- **Scope:** golden path: Collection — desktop, Home — desktop
- **Evidence:**
  - (see raw/*.psi.json)

### BP-3 · Duplicate inline SVGs
- **What / why:** Duplicate inline SVGs — flagged sitewide by the crawl. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common where an icon set is inlined per use — low priority.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 12 element(s) across 4 pattern(s)
- **Scope:** sitewide: of 177 pages
- **Evidence:**
  - [warning] ×9 · `6x SVG (1436 B): <svg aria-hidden="true" focusable="false" class="icon icon-plus" width="19" height="19" view…` · /products/the-hzl-summer-sorbet-shorts-lemon, /products/the-hzl-miss-america-shorts-cherry, /products/the-hzl-sunday-brunch-mockneck-blueberry-pancake (+2 more)
  - [warning] ×1 · `8x SVG (1436 B): <svg aria-hidden="true" focusable="false" class="icon icon-plus" width="19" height="19" view…` · /products/the-hzl-winter-wonderland-sweatpants
  - [warning] ×1 · `13x SVG (1436 B): <svg aria-hidden="true" focusable="false" class="icon icon-plus" width="19" height="19" vie…` · /products/evi11-twin-vintage-jewels-drop-1
  - [warning] ×1 · `7x SVG (1436 B): <svg aria-hidden="true" focusable="false" class="icon icon-plus" width="19" height="19" view…` · /products/the-hb-cider-sweatpants

### BP-4 · WebP support
- **What / why:** WebP support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 177 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl-report.html

### BP-5 · AVIF support
- **What / why:** AVIF support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 177 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl-report.html
