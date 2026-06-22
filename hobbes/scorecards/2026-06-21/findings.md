# Findings — 2026-06-21

Site: https://hazelboutique.com/ · Generated 2026-06-21 20:39 CDT by `hobbes/tools/findings.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 39 findings. Every failing check is enumerated straight from `raw/` — no shortlist, no mission weighting, no hand-picking; same raw always yields the same findings. Where a list is long it is capped with an explicit `+N more`, never silently trimmed. Numbers and scorecard in `baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/scorecards/FINDINGS-TEMPLATE.md`.

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

### A11Y-3 · heading-order — 1 node(s)
- **What / why:** Headings skip a level (e.g. h3 with no h2). Breaks the document outline a screen reader navigates by. In Dawn, card titles (h3/h5) under a section with no h2 are the usual cause.
- **Source:** PSI Lighthouse · accessibility · `heading-order`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 1 node(s), 1 run(s)
- **Scope:** golden path: Collection — mobile
- **Evidence:**
  - `div.card > div.card__content > div.card__information > h3#title-template--26596969251130__product-g…`
  -   ↳ <h3 class="card__heading h5" id="title-template--26596969251130__product-grid-10333095985466">

### A11Y-4 · image-alt — 1 node(s)
- **What / why:** An <img> has no alt attribute. A screen reader skips it or reads the filename. On Shopify these are product/card images; alt comes from the image's alt set in admin or the theme's <img> tag.
- **Source:** PSI Lighthouse · accessibility · `image-alt`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 1 node(s), 2 run(s)
- **Scope:** golden path: Product — desktop, Product — mobile
- **Evidence:**
  - `div.card__inner > div.card__media > div.media > img`
  -   ↳ <img src="//hazelboutique.com/cdn/shop/files/IMG-1767.jpg?v=1711642495" loading="lazy" width="1200">

### A11Y-5 · Sitewide a11y prevalence
- **What / why:** How widespread the a11y gaps are across the whole site — element-level counts. SiteOne's per-analysis totals over every crawled page: real element counts, not the blunt one-flag-per-page rollup. The PSI rules above are authoritative for the golden path; this shows the scale beyond it.
- **Source:** SiteOne crawl · accessibility table
- **Target → measured:** 0 issues (BASELINE §F) → 1763 flagged element(s) across 185 pages
- **Scope:** sitewide: 185 pages crawled
- **Evidence:**
  - HTML structural issues: 0 critical, 1758 warning
  - Missing image alt attributes: 0 critical, 3 warning
  - Missing form labels: 0 critical, 1 warning
  - Unnamed links/buttons: 0 critical, 1 warning

## SEO — SEO & discoverability

### SEO-1 · Missing meta descriptions
- **What / why:** Pages with no <meta name=description>. Google then invents the SERP snippet from page text — usually worse copy, lower click-through. On Shopify, collection/policy/system pages have none unless the theme or admin sets one.
- **Source:** SiteOne crawl · seo table  ·  seo.py · golden path
- **Target → measured:** Every page (BASELINE §E + §F) → 76 of 185 sitewide; golden: Home, Collection
- **Scope:** golden path: Home, Collection · sitewide: 76 / 185
- **Evidence:**
  - /
  - /blogs/news
  - /collections/100-200
  - /collections/12-year-anniversary-collection
  - /collections/14k-gold-filled
  - /collections/20-final-sale
  - /collections/20-rack
  - /collections/30-rack
  - /collections/40-final-sale
  - /collections/50-100
  - /collections/50-101
  - /collections/accessories
  - /collections/accessories-sale
  - /collections/all
  - /collections/all-accessories
  - /collections/all-clothing
  - /collections/all-hazel-brand
  - /collections/all-home-decor
  - /collections/all-products
  - /collections/all-sale
  - /collections/best-selling-accessories
  - /collections/best-selling-clothing
  - /collections/best-selling-collection
  - /collections/bestselling-hazel-brand
  - /collections/bottoms
  - /collections/bridal-edit
  - /collections/candles
  - /collections/clothing-sale
  - /collections/custom
  - /collections/dresses
  - /collections/dresses-1
  - /collections/earrings
  - /collections/fine-collection
  - /collections/gift-card
  - /collections/harley-tees
  - /collections/hazel-bracelets
  - /collections/hazel-brand
  - /collections/hazel-brand-sale
  - /collections/hazel-minis
  - /collections/hazel-sport
  - /collections/home
  - /collections/home-decor-sale
  - /collections/hzl-sport
  - /collections/jackets
  - /collections/lifestyle
  - /collections/mocknecks
  - /collections/necklaces-chokers
  - /collections/new-accessories
  - /collections/new-arrivals
  - /collections/new-arrivals-1
  - /collections/new-clothing
  - /collections/new-collection
  - /collections/new-hazel-brand
  - /collections/new-home-decor
  - /collections/over-100
  - /collections/pants
  - /collections/perfume
  - /collections/prints
  - /collections/sets
  - /collections/shorts
  - /collections/skirts
  - /collections/sterling-silver
  - /collections/sweats
  - /collections/swimwear
  - /collections/testestest
  - /collections/the-holiday-shop
  - /collections/the-pointelle-shop
  - /collections/the-smooth-peach-collection
  - /collections/tops
  - /collections/tops-1
  - /collections/under-10
  - /collections/under-50
  - /collections/vintage
  - /pages/divider
  - /pages/gift-certificates
  - /pages/swym-share-wishlist

### SEO-2 · Heading structure (single H1 + order)
- **What / why:** Pages with no/multiple H1 or a skipped heading level. Headings are the outline assistive tech and search engines read. A skipped level (h1→h3) or a second h1 breaks that outline. In Dawn, section/card heading levels (h2/h3/h5) drift when sections are reordered or a banner ships an h1.
- **Source:** SiteOne crawl · seo-headings  ·  seo.py · golden path
- **Target → measured:** Single H1 + ordered headings, all pages (BASELINE §E/§F) → 2 multi-H1, 185 skipped-level of 185
- **Scope:** golden path: Home · sitewide: 185 / 185 pages with heading errors
- **Evidence:**
  - golden Home: 2 h1, order ok — h3 → h3 → h3 → h3 → h1 → h1 → h2 → h3 → h3 → h3 → h3 → h3…
  - /pages/sizing: 8 error(s) — h3 → h3 → h3 → h3 → h1 → h3 → h3 → h3 → h3 → h2
  - /: 6 error(s) — h3 → h3 → h3 → h3 → h1 → h1 → h2 → h3 → h3 → h3 → h3 → h3…
  - /pages/search-results: 6 error(s) — h3 → h3 → h3 → h3 → h1 → h1 → h2
  - /blogs/news: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2
  - /collections/100-200: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h2 → h2
  - /collections/12-year-anniversary-collection: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h3 → h3 → h3 → h3…
  - /collections/14k-gold-filled: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h3 → h3 → h3 → h3…
  - /collections/20-final-sale: 4 error(s) — h3 → h3 → h3 → h3 → h1 → h2 → h2 → h2 → h3 → h3 → h3 → h3…
  - (+177 more page(s) with heading errors)

### SEO-3 · Image alt coverage
- **What / why:** Images on the page with no alt attribute (coverage, not quality). Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Product/card images get alt from the admin image alt or the theme <img>.
- **Source:** seo.py · golden path
- **Target → measured:** All images have alt (BASELINE §E) → golden pages failing: Home, Collection, Product
- **Scope:** golden path: Home, Collection, Product
- **Evidence:**
  - golden Home: 19 of 44 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+16 more on this page)
  - golden Collection: 45 of 89 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+42 more on this page)
  - golden Product: 16 of 25 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+13 more on this page)

### SEO-4 · Open Graph / Twitter tags
- **What / why:** Pages missing og:title/og:image (and the rest of the OG/Twitter set). These control the link preview when the page is shared (social, iMessage, etc.). Missing them = an ugly or blank share card. Set in the theme <head>; Dawn ships them but custom templates can drop them.
- **Source:** seo.py · golden path  ·  SiteOne crawl · open-graph
- **Target → measured:** OG/Twitter present, all pages → 43 of 185 sitewide
- **Scope:** golden path: Home · sitewide: 43 / 185
- **Evidence:**
  - golden Home: missing image
  - sitewide: 43 of 185 page(s) missing og:title or og:image

### SEO-5 · Duplicate page titles
- **What / why:** Two or more pages share an identical <title>. Search engines can't tell the pages apart and may pick the wrong one to rank. Usually two collections/pages built from the same title source.
- **Source:** SiteOne crawl · non-unique-titles
- **Target → measured:** 0 duplicate titles (BASELINE §F) → 4 duplicated title(s)
- **Evidence:**
  - "Tops – Hazel Boutique" ×2
  - "Dresses – Hazel Boutique" ×2
  - "Under $50 – Hazel Boutique" ×2
  - "New Arrivals – Hazel Boutique" ×2

### SEO-6 · Duplicate meta descriptions
- **What / why:** Two or more pages share an identical meta description. Duplicate descriptions blur how pages differ in search and weaken each snippet; templated descriptions repeated across products/collections are the usual cause. (Empty descriptions are counted in the missing-description finding above, not here.)
- **Source:** SiteOne crawl · non-unique-descriptions
- **Target → measured:** 0 duplicate descriptions (BASELINE §F) → 4 duplicated description(s)
- **Evidence:**
  - "Fill (oz): 18 Fill (g/ml): 510 Natural Wick(s): 1 Vegan Imperial Dime…" ×4
  - "Evi11 Twin Vintage One of A Kind Pre- Loved ( may have minor rips / s…" ×4
  - "14k Gold Bracelet Hazel Bracelet Each Bracelet Sold Separately" ×2
  - "EVI11 TWIN VINTAGE ONE OF A KIND PRE- LOVED ( MAY HAVE MINOR RIPS / S…" ×2

## PERF — Performance

### PERF-1 · Lab performance below target
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in baseline.md §C: CrUX may already pass even where lab fails. The pass bar is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (BASELINE Targets) → score range 65–87 across runs (see §A)
- **Scope:** golden path: all golden pages × device
- **Evidence:**
  - Home — mobile: perf 65 ✗cut · LCP 8.87s · TBT 262.0ms · SI 5.03s · CLS 0.029
  - Home — desktop: perf 86 ✗cut · LCP 2.31s · TBT 66.0ms · SI 1.42s · CLS 0.01
  - Collection — mobile: perf 75 ✗cut · LCP 4.95s · TBT 200.0ms · SI 4.2s · CLS 0.0
  - Collection — desktop: perf 83 ✗cut · LCP 1.1s · TBT 335.0ms · SI 1.02s · CLS 0.013
  - Product — mobile: perf 66 ✗cut · LCP 6.23s · TBT 278.0ms · SI 4.48s · CLS 0.0
  - Product — desktop: perf 87 ✗cut · LCP 2.16s · TBT 118.0ms · SI 1.3s · CLS 0.01

### PERF-2 · Improve image delivery
- **What / why:** Reducing the download time of images can improve the perceived load time of the page and LCP. Learn more about optimizing image size
- **Source:** PSI Lighthouse · performance · `image-delivery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1908 KB across 38 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 350 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 257 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 234 KB
  - IMG-1767.jpg?v=1711642495 · 140 KB
  - B0924A6C-3E0F-4751-88B1-786B97F6ABB6.jpg?v=1711642495 · 92 KB
  - script-logo.png?v=1713629.5093 · 82 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 78 KB
  - image_e23ddca7-2070-4190-a17b-75160e36c99e.heic?v=171164249… · 51 KB
  - (+30 more — see raw/*.psi.json)

### PERF-3 · Use efficient cache lifetimes
- **What / why:** A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
- **Source:** PSI Lighthouse · performance · `cache-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1421 KB across 23 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 400 KB
  - protect.widget.js · 110 KB
  - embed.js · 75 KB
  - portable-wallets.en.js · 73 KB
  - protect.core.js?shop=hazelboutique.com · 57 KB
  - popup.js · 34 KB
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 23 KB
  - (+15 more — see raw/*.psi.json)

### PERF-4 · Reduce JavaScript execution time
- **What / why:** Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to reduce Javascript execution time.
- **Source:** PSI Lighthouse · performance · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 10514 ms across 19 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - / · 2773 ms
  - all-hazel-brand · 2319 ms
  - the-capri-collection-baby-pink · 2121 ms
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 824 ms
  - fera.js · 586 ms
  - Unattributable · 540 ms
  - embed.js · 233 ms
  - loader.js · 183 ms
  - (+11 more — see raw/*.psi.json)

### PERF-5 · Avoid enormous network payloads
- **What / why:** Large network payloads cost users real money and are highly correlated with long load times. Learn how to reduce payload sizes.
- **Source:** PSI Lighthouse · performance · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3691 KB across 17 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 667 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 389 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 286 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 261 KB
  - hydrate.Doy0bVKk.js · 223 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 183 KB
  - IMG-1767.jpg?v=1711642495 · 158 KB
  - (+9 more — see raw/*.psi.json)

### PERF-6 · Render-blocking requests
- **What / why:** Requests are blocking the page's initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.
- **Source:** PSI Lighthouse · performance · `render-blocking-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 47 KB across 13 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - base.css?v=22530685120413333581780699239 · 20 KB · 1051 ms
  - component-card.css?v=167388730439994141521779296826 · 3 KB · 601 ms
  - component-localization-form.css?v=5448825362413877953177161… · 3 KB · 301 ms
  - component-cart-drawer.css?v=81773304689423785551771610528 · 3 KB · 165 ms
  - accelerated-checkout-backwards-compat.css · 3 KB · 492 ms
  - component-slider.css?v=76902739753078838911779286626 · 3 KB · 165 ms
  - component-slideshow.css?v=128144104580933199301771610528 · 2 KB · 492 ms
  - component-cart.css?v=17014677181193491701771610528 · 2 KB · 165 ms
  - (+5 more — see raw/*.psi.json)

### PERF-7 · Reduce unused JavaScript
- **What / why:** Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. Learn how to reduce unused JavaScript.
- **Source:** PSI Lighthouse · performance · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 818 KB across 11 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 392 KB
  - js?id=G-G3RDTGKWR4 · 82 KB
  - fera.js · 67 KB
  - protect.widget.js · 50 KB
  - portable-wallets.en.js · 42 KB
  - freeshippingbar.js?shop=hazelboutiquenj.myshopify.com · 36 KB
  - b0d88c59awa19302f9p5122874fmc636b965m.js · 35 KB
  - embed.js · 33 KB
  - (+3 more — see raw/*.psi.json)

### PERF-8 · Minimize main-thread work
- **What / why:** Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to minimize main-thread work
- **Source:** PSI Lighthouse · performance · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6121 ms across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 2854 ms
  - Other · 1404 ms
  - Style & Layout · 900 ms
  - Script Parsing & Compilation · 568 ms
  - Garbage Collection · 197 ms
  - Rendering · 131 ms
  - Parse HTML & CSS · 68 ms

### PERF-9 · Reduce unused CSS
- **What / why:** Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. Learn how to reduce unused CSS.
- **Source:** PSI Lighthouse · performance · `unused-css-rules` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 93 KB across 5 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 29 KB
  - :root,[data-bs-theme="light"]{--bs-blue: #0d6efd;--bs-indigo: #6610f2;--bs-purple: #6f42c… · 26 KB
  - base.css?v=22530685120413333581780699239 · 15 KB
  - instafeed-17.10.0.css · 11 KB
  - widget_v3_base.css · 11 KB

### PERF-10 · Forced reflow
- **What / why:** A forced reflow occurs when JavaScript queries geometric properties (such as offsetWidth) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about forced reflows and possible mitigations.
- **Source:** PSI Lighthouse · performance · `forced-reflow-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 42 ms across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - all-hazel-brand · 18 ms
  - b0d88c59awa19302f9p5122874fmc636b965m.js · 18 ms
  - / · 5 ms
  - the-capri-collection-baby-pink · 0 ms

### PERF-11 · Legacy JavaScript
- **What / why:** Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren't necessary for modern browsers. Consider modifying your JavaScript build process to not transpile Baseline features, unless you know you must support older browsers. Learn why most sites can deploy ES6+ code without transpiling
- **Source:** PSI Lighthouse · performance · `legacy-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 23 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - protect.core.js?shop=hazelboutique.com · 10 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 7 KB
  - portable-wallets.en.js · 6 KB

### PERF-12 · Image elements do not have explicit `width` and `height`
- **What / why:** Set an explicit width and height on image elements to reduce layout shifts and improve CLS. Learn how to set image dimensions
- **Source:** PSI Lighthouse · performance · `unsized-images` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 3 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Hazel Boutique
  - hazel-mobile-logo.png?v=1713629.5093
  - hazel-mobile-logo.png?v=1713641093

### PERF-13 · Duplicated JavaScript
- **What / why:** Remove large, duplicate JavaScript modules from bundles to reduce unnecessary bytes consumed by network activity.
- **Source:** PSI Lighthouse · performance · `duplicated-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 4 KB across 2 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - /cdn/shop/t/51/assets/quick-add.js?v=131073536309624707681771610528 · 2 KB
  - /cdn/shop/t/51/assets/product-form.js?v=3603548357138963301771610529 · 2 KB

### PERF-14 · LCP request discovery
- **What / why:** Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
- **Source:** PSI Lighthouse · performance · `lcp-discovery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 3 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - fetchpriority=high should be applied

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
- **Target → measured:** Fast server response, all pages (BASELINE Targets) → slowest 0.54s; top 20 listed
- **Scope:** sitewide: 20 slowest of crawl
- **Evidence:**
  - 14k-gold-filled · 0.54s (200)
  - shorts · 0.53s (200)
  - necklaces-chokers · 0.49s (200)
  - 50-101 · 0.48s (200)
  - best-selling-accessories · 0.48s (200)
  - over-100 · 0.47s (200)
  - new-accessories · 0.47s (200)
  - under-50 · 0.46s (200)
  - the-lover-shorts · 0.44s (200)
  - hazel-brand-sale · 0.44s (200)
  - best-selling-collection · 0.43s (200)
  - fine-collection · 0.43s (200)
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
  - Error fetching recommendations: Error: HTTP error! Status: 422 at https://hazelboutique.com/:904:17
  - Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
  - Failed to load resource: the server responded with a status of 400 (Bad Request)
  - Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)
  - (+9 more)

### BP-2 · inspector-issues
- **What / why:** Issues Chrome's Issues panel flagged (cookies, mixed content, etc.). Browser-level warnings; open the raw audit for the specifics.
- **Source:** PSI Lighthouse · best-practices · `inspector-issues`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 3 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Product — mobile
- **Evidence:**
  - (see raw/*.psi.json)

### BP-3 · image-aspect-ratio
- **What / why:** An image is displayed at a ratio that doesn't match its file. Looks stretched/squashed; can also shift layout. A width/height or CSS sizing mismatch.
- **Source:** PSI Lighthouse · best-practices · `image-aspect-ratio`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 2 run(s)
- **Scope:** golden path: Home — desktop, Home — mobile
- **Evidence:**
  - https://cdn.shopify.com/s/files/1/0051/3264/8566/files/script-logo.png?v=1713629.5093
  - https://cdn.shopify.com/s/files/1/0051/3264/8566/files/hazel-mobile-logo.png?v=1713629.5093

### BP-4 · deprecations
- **What / why:** Use of a deprecated browser API. Will break in a future browser version. Usually inside a third-party script.
- **Source:** PSI Lighthouse · best-practices · `deprecations`
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 1 run(s)
- **Scope:** golden path: Product — desktop
- **Evidence:**
  - https://hazelboutique.com/products/the-capri-collection-baby-pink

### BP-5 · Invalid inline SVGs
- **What / why:** Invalid inline SVGs — flagged sitewide by the crawl. Malformed inline SVG markup — can render wrong or bloat the DOM. Usually a theme snippet or app-injected icon.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 10 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 10 warning — see crawl.html

### BP-6 · Duplicate inline SVGs
- **What / why:** Duplicate inline SVGs — flagged sitewide by the crawl. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common in Dawn — low priority.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html

### BP-7 · WebP support
- **What / why:** WebP support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open crawl.html for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html

### BP-8 · AVIF support
- **What / why:** AVIF support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site. Open crawl.html for the per-URL list.
- **Source:** SiteOne crawl · best-practices table
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 185 pages
- **Evidence:**
  - 0 critical, 1 warning — see crawl.html
