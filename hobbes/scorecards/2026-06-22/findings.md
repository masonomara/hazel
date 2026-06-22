# Findings — 2026-06-22

Site: https://hazelboutique.com/ · Generated 2026-06-22 18:15 CDT by `hobbes/tools/findings.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 36 findings. Every failing check is enumerated straight from `raw/` — no shortlist, no mission weighting, no hand-picking; same raw always yields the same findings. Where a list is long it is capped with an explicit `+N more`, never silently trimmed. Numbers and scorecard in `baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/templates/FINDINGS-TEMPLATE.md`.

## A11Y — Accessibility

### A11Y-1 · label-content-name-mismatch — 3 node(s)
- **What / why:** A control's visible text isn't contained in its accessible name. Voice-control users can't activate it by its visible label. Common on slideshow/hero slide links and pagination, where an aria-label omits the visible text.
- **Source:** PSI Lighthouse · accessibility · `label-content-name-mismatch`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 3 node(s), 1 run(s)
- **Scope:** golden path: Home — mobile
- **Evidence:**
  - `section#shopify-section-template--26596969316666__hero_QK67RC > slideshow-component.mobile-hero > d…`
  -   ↳ <a href="/collections/new-arrivals-1" aria-label="Shop HZL NEW" tabindex="0" target="_top" class="slideshow__slide grid…
  - `section#shopify-section-template--26596969316666__hero_QK67RC > slideshow-component.mobile-hero > d…`
  -   ↳ <a href="/collections/all-clothing" aria-label="View slide" tabindex="0" target="_top" class="slideshow__slide grid__it…
  - `section#shopify-section-template--26596969316666__hero_QK67RC > slideshow-component.mobile-hero > d…`
  -   ↳ <a href="/collections/all-clothing" aria-label="View slide" tabindex="0" target="_top" class="slideshow__slide grid__it…

### A11Y-2 · frame-title — 2 node(s)
- **What / why:** An <iframe> has no title attribute. Announced with no purpose. Often a third-party embed (Mailchimp popup, video, map) we don't author directly — fix in the embed config or wrap it.
- **Source:** PSI Lighthouse · accessibility · `frame-title`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 2 node(s), 6 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - `div#PopupSignupForm_0 > div.mc-banner > div.mc-layout__bannerContent > iframe`
  -   ↳ <iframe src="about:blank" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="width: 100%; height: 1…
  - `div#PopupSignupForm_0 > div.mc-modal > div.mc-layout__modalContent > iframe`
  -   ↳ <iframe src="about:blank" frameborder="0" marginwidth="0" marginheight="0" style="width: 100%; height: 379px;" data-doj…

### A11Y-3 · Sitewide a11y prevalence
- **What / why:** How widespread the a11y gaps are across the whole site — element-level counts. SiteOne's per-analysis totals over every crawled page: real element counts, not the blunt one-flag-per-page rollup. The PSI rules above are authoritative for the golden path; this shows the scale beyond it.
- **Source:** SiteOne crawl · accessibility table
- **Target → measured:** 0 issues (BASELINE §F) → 1761 flagged element(s) across 185 pages
- **Scope:** sitewide: 185 pages crawled
- **Evidence:**
  - HTML structural issues: 0 critical, 1756 warning
  - Missing image alt attributes: 0 critical, 3 warning
  - Unnamed links/buttons: 0 critical, 1 warning
  - Missing form labels: 0 critical, 1 warning

## SEO — SEO & discoverability

### SEO-1 · Heading structure (single H1 + order)
- **What / why:** Pages with no/multiple H1 or a skipped heading level. Headings are the outline assistive tech and search engines read. A skipped level (h1→h3) or a second h1 breaks that outline. In Dawn, section/card heading levels (h2/h3/h5) drift when sections are reordered or a banner ships an h1.
- **Source:** SiteOne crawl · seo-headings  ·  seo.py · golden path
- **Target → measured:** Single H1 + ordered headings, all pages (BASELINE §E/§F) → 1 multi-H1, 185 skipped-level of 185
- **Scope:** sitewide: 185 / 185 pages with heading errors
- **Evidence:**
  - /pages/sizing: 8 error(s) — h3 → h3 → h3 → h3 → h1 → h3 → h3 → h3 → h3 → h2
  - /pages/search-results: 6 error(s) — h3 → h3 → h3 → h3 → h1 → h1 → h2
  - /: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h3 → h3 → h3 → h3 → h3 → h3…
  - /blogs/news: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2
  - /collections/100-200: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h2 → h2
  - /collections/12-year-anniversary-collection: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h2 → h2 → h2 → h2…
  - /collections/14k-gold-filled: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h2 → h2 → h2 → h2…
  - /collections/20-final-sale: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h2 → h2 → h2 → h2…
  - (+177 more page(s) with heading errors)

### SEO-2 · Image alt coverage
- **What / why:** Images on the page with no alt attribute (coverage, not quality). Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Product/card images get alt from the admin image alt or the theme <img>.
- **Source:** seo.py · golden path
- **Target → measured:** All images have alt (BASELINE §E) → golden pages failing: Home, Collection, Product
- **Scope:** golden path: Home, Collection, Product
- **Evidence:**
  - golden Home: 19 of 43 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+16 more on this page)
  - golden Collection: 45 of 88 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+42 more on this page)
  - golden Product: 16 of 24 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+13 more on this page)

### SEO-3 · Duplicate page titles
- **What / why:** Two or more pages share an identical <title>. Search engines can't tell the pages apart and may pick the wrong one to rank. Usually two collections/pages built from the same title source.
- **Source:** SiteOne crawl · non-unique-titles
- **Target → measured:** 0 duplicate titles (BASELINE §F) → 4 duplicated title(s)
- **Evidence:**
  - "Dresses – Hazel Boutique" ×2
  - "New Arrivals – Hazel Boutique" ×2
  - "Under $50 – Hazel Boutique" ×2
  - "Tops – Hazel Boutique" ×2

### SEO-4 · Duplicate meta descriptions
- **What / why:** Two or more pages share an identical meta description. Duplicate descriptions blur how pages differ in search and weaken each snippet; templated descriptions repeated across products/collections are the usual cause. (Empty descriptions are counted in the missing-description finding above, not here.)
- **Source:** SiteOne crawl · non-unique-descriptions
- **Target → measured:** 0 duplicate descriptions (BASELINE §F) → 9 duplicated description(s)
- **Evidence:**
  - "Hazel Boutique" ×5
  - "Fill (oz): 18 Fill (g/ml): 510 Natural Wick(s): 1 Vegan Imperial Dime…" ×4
  - "Evi11 Twin Vintage One of A Kind Pre- Loved ( may have minor rips / s…" ×4
  - "EVI11 TWIN VINTAGE ONE OF A KIND PRE- LOVED ( MAY HAVE MINOR RIPS / S…" ×2
  - "Shop Under $50 at Hazel Boutique." ×2
  - "Shop New Arrivals at Hazel Boutique." ×2
  - "Shop Tops at Hazel Boutique." ×2
  - "14k Gold Bracelet Hazel Bracelet Each Bracelet Sold Separately" ×2
  - "Shop Dresses at Hazel Boutique." ×2

## PERF — Performance

### PERF-1 · Lab performance below target
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in baseline.md §C: CrUX may already pass even where lab fails. The pass bar is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (BASELINE Targets) → score range 50–70 across runs (see §A)
- **Scope:** golden path: all golden pages × device
- **Evidence:**
  - Home — mobile: perf 54 · LCP 23.48s · TBT 192.0ms · SI 9.3s · CLS 0.0
  - Home — desktop: perf 56 · LCP 2.34s · TBT 193.0ms · SI 1.45s · CLS 1.01
  - Collection — mobile: perf 51 · LCP 5.55s · TBT 164.0ms · SI 3.12s · CLS 0.984
  - Collection — desktop: perf 65 · LCP 1.51s · TBT 443.0ms · SI 1.33s · CLS 0.203
  - Product — mobile: perf 50 · LCP 19.78s · TBT 323.0ms · SI 8.01s · CLS 0.0
  - Product — desktop: perf 70 · LCP 1.67s · TBT 300.0ms · SI 1.45s · CLS 0.205

### PERF-2 · Improve image delivery
- **What / why:** Reducing the download time of images can improve the perceived load time of the page and LCP. Learn more about optimizing image size
- **Source:** PSI Lighthouse · performance · `image-delivery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2285 KB across 48 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 375 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 275 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 251 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 141 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 114 KB
  - B63E7E4D-8A47-4FF8-A0EB-50A2E2099CA7.jpg?v=1781808485&width… · 58 KB
  - A0A8C32C-CEAC-4D84-B603-3C7749016C49.jpg?v=1781235184&width… · 56 KB
  - 639CDF20-2DC2-4050-984B-8D3C37151A52.jpg?v=1781808485&width… · 52 KB
  - (+40 more — see raw/*.psi.json)

### PERF-3 · Use efficient cache lifetimes
- **What / why:** A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
- **Source:** PSI Lighthouse · performance · `cache-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1420 KB across 23 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 400 KB
  - protect.widget.js · 110 KB
  - embed.js · 75 KB
  - portable-wallets.en.js · 73 KB
  - protect.core.js?shop=hazelboutique.com · 56 KB
  - popup.js · 34 KB
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 23 KB
  - (+15 more — see raw/*.psi.json)

### PERF-4 · Avoid enormous network payloads
- **What / why:** Large network payloads cost users real money and are highly correlated with long load times. Learn how to reduce payload sizes.
- **Source:** PSI Lighthouse · performance · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3408 KB across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 667 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 389 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 286 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 261 KB
  - hydrate.BM6jDpDH.js · 222 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 183 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 156 KB
  - (+7 more — see raw/*.psi.json)

### PERF-5 · Reduce JavaScript execution time
- **What / why:** Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to reduce Javascript execution time.
- **Source:** PSI Lighthouse · performance · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2612 ms across 13 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 552 ms
  - the-capri-collection-baby-pink · 419 ms
  - Unattributable · 418 ms
  - faro-web-sdk.iife.js · 198 ms
  - loader.js · 186 ms
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 151 ms
  - embed.js · 148 ms
  - b48f264e1w8fb36573pab670d30m380d3b3cm.js · 146 ms
  - (+5 more — see raw/*.psi.json)

### PERF-6 · Reduce unused JavaScript
- **What / why:** Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. Learn how to reduce unused JavaScript.
- **Source:** PSI Lighthouse · performance · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 749 KB across 10 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 392 KB
  - js?id=G-G3RDTGKWR4 · 82 KB
  - protect.widget.js · 50 KB
  - portable-wallets.en.js · 42 KB
  - b48f264e1w8fb36573pab670d30m380d3b3cm.js · 36 KB
  - embed.js · 33 KB
  - freeshippingbar.js?shop=hazelboutiquenj.myshopify.com · 33 KB
  - popup.js · 29 KB
  - (+2 more — see raw/*.psi.json)

### PERF-7 · Minimize main-thread work
- **What / why:** Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to minimize main-thread work
- **Source:** PSI Lighthouse · performance · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3216 ms across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 1504 ms
  - Script Parsing & Compilation · 522 ms
  - Other · 507 ms
  - Style & Layout · 362 ms
  - Garbage Collection · 205 ms
  - Parse HTML & CSS · 60 ms
  - Rendering · 57 ms

### PERF-8 · Layout shift culprits
- **What / why:** Layout shifts occur when elements move absent any user interaction. Investigate the causes of layout shifts, such as elements being added, removed, or their fonts changing as the page loads.
- **Source:** PSI Lighthouse · performance · `cls-culprits-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 2 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - COLLECTION: COLLECTION: ALL HAZEL BRAND FILTER AND SORT THE HZL LEILANI CREWNEC…
  - Country Code
  - Get exclusive updates and offers!
  - HAZEL POLICIES
  - Intuit Mailchimp logo
  - body

### PERF-9 · Reduce unused CSS
- **What / why:** Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. Learn how to reduce unused CSS.
- **Source:** PSI Lighthouse · performance · `unused-css-rules` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 93 KB across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 29 KB
  - :root,[data-bs-theme="light"]{--bs-blue: #0d6efd;--bs-indigo: #6610f2;--bs-purple: #6f42c… · 26 KB
  - base.css?v=38272640574550089181782154911 · 15 KB
  - instafeed-17.10.0.css · 11 KB
  - widget_v3_base.css · 11 KB

### PERF-10 · Render-blocking requests
- **What / why:** Requests are blocking the page's initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.
- **Source:** PSI Lighthouse · performance · `render-blocking-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 28 KB across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - base.css?v=38272640574550089181782154911 · 20 KB · 1473 ms
  - accelerated-checkout-backwards-compat.css · 3 KB · 492 ms
  - component-slider.css?v=76902739753078838911779286626 · 3 KB · 165 ms
  - component-slideshow.css?v=128144104580933199301771610528 · 2 KB · 492 ms

### PERF-11 · LCP breakdown
- **What / why:** Each subpart has specific improvement strategies. Ideally, most of the LCP time should be spent on loading the resources, not within delays.
- **Source:** PSI Lighthouse · performance · `lcp-breakdown-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2505 ms across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Element render delay · 2072 ms
  - Resource load delay · 362 ms
  - Resource load duration · 62 ms
  - Time to first byte · 9 ms

### PERF-12 · Legacy JavaScript
- **What / why:** Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren't necessary for modern browsers. Consider modifying your JavaScript build process to not transpile Baseline features, unless you know you must support older browsers. Learn why most sites can deploy ES6+ code without transpiling
- **Source:** PSI Lighthouse · performance · `legacy-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 23 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - protect.core.js?shop=hazelboutique.com · 10 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 7 KB
  - portable-wallets.en.js · 6 KB

### PERF-13 · Image elements do not have explicit `width` and `height`
- **What / why:** Set an explicit width and height on image elements to reduce layout shifts and improve CLS. Learn how to set image dimensions
- **Source:** PSI Lighthouse · performance · `unsized-images` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 2 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Hazel Boutique
  - hazel-mobile-logo.png?v=1713641093&width=760

### PERF-14 · Duplicated JavaScript
- **What / why:** Remove large, duplicate JavaScript modules from bundles to reduce unnecessary bytes consumed by network activity.
- **Source:** PSI Lighthouse · performance · `duplicated-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 4 KB across 2 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - /cdn/shop/t/51/assets/quick-add.js?v=131073536309624707681771610528 · 2 KB
  - /cdn/shop/t/51/assets/product-form.js?v=3603548357138963301771610529 · 2 KB

### PERF-15 · Forced reflow
- **What / why:** A forced reflow occurs when JavaScript queries geometric properties (such as offsetWidth) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about forced reflows and possible mitigations.
- **Source:** PSI Lighthouse · performance · `forced-reflow-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 125 ms across 2 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - / · 63 ms
  - b48f264e1w8fb36573pab670d30m380d3b3cm.js · 63 ms

### PERF-16 · Avoid large layout shifts
- **What / why:** These are the largest layout shifts observed on the page. Each table item represents a single layout shift, and shows the element that shifted the most. Below each item are possible root causes that led to the layout shift. Some of these layout shifts may not be included in the CLS metric value due to windowing. Learn how to improve CLS
- **Source:** PSI Lighthouse · performance · `layout-shifts` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6 layout shifts found
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - COLLECTION: COLLECTION: ALL HAZEL BRAND FILTER AND SORT THE HZL LEILANI CREWNEC…
  - HAZEL POLICIES

### PERF-17 · Minify CSS
- **What / why:** Minifying CSS files can reduce network payload sizes. Learn how to minify CSS.
- **Source:** PSI Lighthouse · performance · `unminified-css` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 6 KB

### PERF-18 · Minify JavaScript
- **What / why:** Minifying JavaScript files can reduce payload sizes and script parse time. Learn how to minify JavaScript.
- **Source:** PSI Lighthouse · performance · `unminified-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - d9aa649c0e2ad063e057bdd8c.js?shop=hazelboutiquenj.myshopify… · 3 KB

### PERF-19 · LCP request discovery
- **What / why:** Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
- **Source:** PSI Lighthouse · performance · `lcp-discovery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 1 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - fetchpriority=high should be applied

### PERF-20 · Network dependency tree
- **What / why:** Avoid chaining critical requests by reducing the length of chains, reducing the download size of resources, or deferring the download of unnecessary resources to improve page load.
- **Source:** PSI Lighthouse · performance · `network-dependency-tree-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 3 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - (see raw/*.psi.json)

### PERF-21 · Slowest URLs (server response, sitewide)
- **What / why:** The slowest pages to respond across the whole crawl — server response / TTFB-class timing. SiteOne's per-URL request timing, a broad complement to the golden-path lab metrics. Slow server response delays everything downstream; a consistently slow template or collection is worth a look even when the golden path looks fine.
- **Source:** SiteOne crawl · slowest-urls
- **Target → measured:** Fast server response, all pages (BASELINE Targets) → slowest 0.71s; top 20 listed
- **Scope:** sitewide: 20 slowest of crawl
- **Evidence:**
  - best-selling-collection · 0.71s (200)
  - under-50 · 0.68s (200)
  - 14k-gold-filled · 0.66s (200)
  - new-arrivals · 0.65s (200)
  - earrings · 0.61s (200)
  - all-accessories · 0.59s (200)
  - over-100 · 0.57s (200)
  - dresses-1 · 0.57s (200)
  - all-home-decor · 0.56s (200)
  - tops-1 · 0.53s (200)
  - all-products · 0.53s (200)
  - testestest · 0.52s (200)
  - (+8 more — see crawl.html)

## SEC — Security

### SEC-1 · Missing security response headers
- **What / why:** Standard hardening headers absent from responses. These reduce XSS, clickjacking, and referrer-leak exposure. On Shopify (hosted, Advanced plan) the platform sets some headers and limits what a theme can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.
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
- **What / why:** JavaScript errors logged to the browser console. Each is a script failing at runtime — broken behavior, often from an app embed or a theme script. Read the messages; they name the file.
- **Source:** PSI Lighthouse · best-practices · `errors-in-console`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 6 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
  - Failed to load resource: the server responded with a status of 400 (Bad Request)
  - Failed to load resource: the server responded with a status of 403 ()
  - Framing 'https://shop.app/' violates the following Content Security Policy directive: "frame-ancestors 'self' https://s…
  - (+3 more)

### BP-2 · inspector-issues
- **What / why:** Issues Chrome's Issues panel flagged (cookies, mixed content, etc.). Browser-level warnings; open the raw audit for the specifics.
- **Source:** PSI Lighthouse · best-practices · `inspector-issues`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 2 run(s)
- **Scope:** golden path: Home — desktop, Home — mobile
- **Evidence:**
  - (see raw/*.psi.json)

### BP-3 · Invalid inline SVGs
- **What / why:** Invalid inline SVGs — flagged sitewide by the crawl. Malformed inline SVG markup — can render wrong or bloat the DOM. Usually a theme snippet or app-injected icon.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 10 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 10 warning — see crawl.html

### BP-4 · Duplicate inline SVGs
- **What / why:** Duplicate inline SVGs — flagged sitewide by the crawl. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common in Dawn — low priority.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html

### BP-5 · WebP support
- **What / why:** WebP support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open crawl.html for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html

### BP-6 · AVIF support
- **What / why:** AVIF support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open crawl.html for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html
