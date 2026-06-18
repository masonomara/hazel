# Findings — 2026-06-18

Site: https://hazelboutique.com/ · Generated 2026-06-18 10:20 by `hobbes/tools/findings.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 28 findings. Numbers and scorecard in `baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/scorecards/FINDINGS-TEMPLATE.md`.

## A11Y — Accessibility  (MISSION priority 1)

### A11Y-1 · label-content-name-mismatch — 7 node(s)
- **What / why:** A control's visible text isn't contained in its accessible name. Voice-control users can't activate it by its visible label. Common on slideshow/hero slide links and pagination, where an aria-label omits the visible text.
- **Source:** PSI Lighthouse · accessibility · `label-content-name-mismatch`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 7 node(s), 4 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile
- **Evidence:**
  - `main#MainContent > section#shopify-section-template--26596969316666__hero_QK67RC > div.desktop-hero…`
  -   ↳ <a href="/collections/new-arrivals-1" tabindex="0" target="_top" class="slideshow__slide grid__item grid--1-col slider_…
  - `main#MainContent > section#shopify-section-template--26596969316666__hero_QK67RC > div.desktop-hero…`
  -   ↳ <a href="/collections/all-clothing" tabindex="0" target="_top" class="slideshow__slide grid__item grid--1-col slider__s…
  - `main#MainContent > section#shopify-section-template--26596969316666__hero_QK67RC > div.desktop-hero…`
  -   ↳ <a href="/collections/all-clothing" tabindex="0" target="_top" class="slideshow__slide grid__item grid--1-col slider__s…
  - (+4 more node(s) — see raw/*.psi.json)

### A11Y-2 · button-name — 5 node(s)
- **What / why:** A <button> has no accessible name. A screen reader announces it as just 'button'. In Dawn this hits icon-only buttons — media zoom toggles, quantity steppers, drawer close icons — that need aria-label or visually-hidden text.
- **Source:** PSI Lighthouse · accessibility · `button-name`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 5 node(s), 2 run(s)
- **Scope:** golden path: Product — desktop, Product — mobile
- **Evidence:**
  - `li#Slide-template--26596969644346__main-24187529232444 > div.product-media-container > modal-opener…`
  -   ↳ <button class="product__media-toggle quick-add-hidden product__media-zoom-lightbox" type="button" aria-haspopup="dialog…
  - `li#Slide-template--26596969644346__main-24187529330748 > div.product-media-container > modal-opener…`
  -   ↳ <button class="product__media-toggle quick-add-hidden product__media-zoom-lightbox" type="button" aria-haspopup="dialog…
  - `li#Slide-template--26596969644346__main-34941295526202 > div.product-media-container > modal-opener…`
  -   ↳ <button class="product__media-toggle quick-add-hidden product__media-zoom-lightbox" type="button" aria-haspopup="dialog…
  - (+2 more node(s) — see raw/*.psi.json)

### A11Y-3 · frame-title — 2 node(s)
- **What / why:** An <iframe> has no title attribute. Announced with no purpose. Often a third-party embed (Mailchimp popup, video, map) we don't author directly — fix in the embed config or wrap it.
- **Source:** PSI Lighthouse · accessibility · `frame-title`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 2 node(s), 6 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - `div#PopupSignupForm_0 > div.mc-banner > div.mc-layout__bannerContent > iframe`
  -   ↳ <iframe src="about:blank" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="width: 100%; height: 1…
  - `div#PopupSignupForm_0 > div.mc-modal > div.mc-layout__modalContent > iframe`
  -   ↳ <iframe src="about:blank" frameborder="0" marginwidth="0" marginheight="0" style="width: 100%; height: 379px;" data-doj…

### A11Y-4 · color-contrast — 1 node(s)
- **What / why:** Text/background contrast is below WCAG AA. Low-vision users can't read it. Often sale/sold-out price text, placeholder grey, or button text on hover — a token/CSS value, not markup.
- **Source:** PSI Lighthouse · accessibility · `color-contrast`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 1 node(s), 2 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile
- **Evidence:**
  - `div.card-information > div.price > div.price__container > span.price-item`
  -   ↳ <span class="price-item price-item--sold-out">

### A11Y-5 · heading-order — 1 node(s)
- **What / why:** Headings skip a level (e.g. h3 with no h2). Breaks the document outline a screen reader navigates by. In Dawn, card titles (h3/h5) under a section with no h2 are the usual cause.
- **Source:** PSI Lighthouse · accessibility · `heading-order`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 1 node(s), 1 run(s)
- **Scope:** golden path: Collection — mobile
- **Evidence:**
  - `div.card > div.card__content > div.card__information > h3#title-template--26596969251130__product-g…`
  -   ↳ <h3 class="card__heading h5" id="title-template--26596969251130__product-grid-10326913024314">

### A11Y-6 · image-alt — 1 node(s)
- **What / why:** An <img> has no alt attribute. A screen reader skips it or reads the filename. On Shopify these are product/card images; alt comes from the image's alt set in admin or the theme's <img> tag.
- **Source:** PSI Lighthouse · accessibility · `image-alt`
- **Target → measured:** 0 failing a11y audits (BASELINE §D) → 1 node(s), 2 run(s)
- **Scope:** golden path: Product — desktop, Product — mobile
- **Evidence:**
  - `div.card__inner > div.card__media > div.media > img`
  -   ↳ <img src="//hazelboutique.com/cdn/shop/files/IMG-1767.jpg?v=1711642495" loading="lazy" width="1200">

### A11Y-7 · Sitewide a11y prevalence
- **What / why:** How widespread the golden-path a11y gaps are across all pages. SiteOne's blunt page-level flags — one missing-alt image flags the whole page. They show prevalence, not per-node detail; the PSI rules above are authoritative for the golden path.
- **Source:** SiteOne crawl · summary rollup
- **Target → measured:** 0 pages (BASELINE §F) → alt 203, aria 203, roles 203 of 200
- **Scope:** sitewide: 200 pages crawled
- **Evidence:**
  - 203 page(s) with an image missing alt
  - 203 page(s) flagged without aria labels
  - 203 page(s) flagged without role attributes

## SEO — SEO & discoverability  (MISSION priority 2)

### SEO-1 · Missing meta descriptions
- **What / why:** Pages with no <meta name=description>. Google then invents the SERP snippet from page text — usually worse copy, lower click-through. On Shopify, collection/policy/system pages have none unless the theme or admin sets one.
- **Source:** SiteOne crawl · seo table  ·  seo.py · golden path
- **Target → measured:** Every page (BASELINE §E + §F) → 51 of 200 sitewide; golden: Home, Collection
- **Scope:** golden path: Home, Collection · sitewide: 51 / 200
- **Evidence:**
  - /
  - /cart
  - /collections/20-rack
  - /collections/30-rack
  - /collections/accessories
  - /collections/all
  - /collections/all-accessories
  - /collections/all-clothing
  - /collections/all-hazel-brand
  - /collections/all-home-decor
  - /collections/all-sale
  - /collections/best-selling-accessories
  - /collections/best-selling-accessories?page=3
  - /collections/best-selling-clothing
  - /collections/bestselling-hazel-brand
  - /collections/bestselling-hazel-brand?page=2
  - /collections/bestselling-hazel-brand?page=3
  - /collections/bestselling-hazel-brand?page=8
  - /collections/bottoms
  - /collections/candles
  - /collections/custom
  - /collections/dresses-1
  - /collections/earrings
  - /collections/fine-collection
  - /collections/hazel-bracelets
  - /collections/hazel-bracelets?page=2
  - /collections/hazel-brand
  - /collections/hazel-minis
  - /collections/hazel-sport
  - /collections/home
  - /collections/lifestyle
  - /collections/mocknecks
  - /collections/necklaces-chokers
  - /collections/new-accessories
  - /collections/new-arrivals
  - /collections/new-arrivals-1
  - /collections/new-clothing
  - /collections/new-hazel-brand
  - /collections/new-home-decor
  - /collections/perfume
  - /collections/prints
  - /collections/sweats
  - /collections/swimwear
  - /collections/tops-1
  - /collections/vintage
  - /pages/divider
  - /policies/contact-information
  - /policies/privacy-policy
  - /policies/refund-policy
  - /policies/shipping-policy
  - /policies/terms-of-service

### SEO-2 · Heading structure (single H1 + order)
- **What / why:** Pages with no/multiple H1 or a skipped heading level. Headings are the outline assistive tech and search engines read. A skipped level (h1→h3) or a second h1 breaks that outline. In Dawn, section/card heading levels (h2/h3/h5) drift when sections are reordered or a banner ships an h1.
- **Source:** SiteOne crawl · seo-headings  ·  seo.py · golden path
- **Target → measured:** Single H1 + ordered headings, all pages (BASELINE §E/§F) → 2 multi-H1, 204 skipped-level of 200
- **Scope:** golden path: Home · sitewide: 200 / 200 pages with heading errors
- **Evidence:**
  - golden Home: 2 h1, order ok — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h1 → h2 → h3 → h3…
  - /pages/sizing: 11 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h3 → h3 → h3 → h3…
  - /: 9 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h1 → h2 → h3 → h3…
  - /cart: 9 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h1 → h2 → h2 → h2
  - /policies/shipping-policy: 9 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h3 → h3 → h2
  - /collections/20-rack: 7 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h2 → h2 → h2 → h3…
  - /collections/30-rack: 7 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h2 → h2 → h2 → h3…
  - /collections/accessories: 7 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h2 → h2 → h2 → h3…
  - /collections/all: 7 error(s) — h2 → h3 → h3 → h3 → h3 → h2 → h2 → h1 → h2 → h2 → h2 → h3…
  - (+192 more page(s) with heading errors)

### SEO-3 · Image alt coverage
- **What / why:** Images on the page with no alt attribute (coverage, not quality). Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Product/card images get alt from the admin image alt or the theme <img>.
- **Source:** seo.py · golden path
- **Target → measured:** All images have alt (BASELINE §E) → golden pages failing: Home, Collection, Product
- **Scope:** golden path: Home, Collection, Product
- **Evidence:**
  - golden Home: 20 of 45 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+17 more on this page)
  - golden Collection: 44 of 88 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+41 more on this page)
  - golden Product: 16 of 25 img(s) missing alt
  -   ↳ 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width…
  -   ↳ IMG_2024-05-08-170032.jpg?v=1715288472&width=1500
  -   ↳ E30CD770-43BC-4641-A2C6-C7814C095A9F.jpg?v=1780627337&width…
  -   (+13 more on this page)

### SEO-4 · Open Graph / Twitter tags
- **What / why:** Pages missing og:title/og:image (and the rest of the OG/Twitter set). These control the link preview when the page is shared (social, iMessage, etc.). Missing them = an ugly or blank share card. Set in the theme <head>; Dawn ships them but custom templates can drop them.
- **Source:** seo.py · golden path  ·  SiteOne crawl · open-graph
- **Target → measured:** OG/Twitter present, all pages → 16 of 200 sitewide
- **Scope:** golden path: Home · sitewide: 16 / 200
- **Evidence:**
  - golden Home: missing image
  - sitewide: 16 of 200 page(s) missing og:title or og:image

### SEO-5 · Duplicate page titles
- **What / why:** Two or more pages share an identical <title>. Search engines can't tell the pages apart and may pick the wrong one to rank. Usually two collections/pages built from the same title source.
- **Source:** SiteOne crawl · non-unique-titles
- **Target → measured:** 0 duplicate titles (BASELINE §F) → 1 duplicated title(s)
- **Evidence:**
  - "New Arrivals – Hazel Boutique" ×2

### SEO-6 · Broken links (4xx/5xx)
- **What / why:** A linked URL returns an error status. Dead end for users and crawlers; wastes crawl budget and leaks link equity. Fix the link or restore/redirect the target.
- **Source:** SiteOne crawl · 404 table
- **Target → measured:** 0 broken links (BASELINE §F) → 1 broken
- **Evidence:**
  - https://hazelboutique.com/policies/ (404)

## PERF — Performance  (MISSION priority 3)

### PERF-1 · Lab performance below target (mobile)
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in baseline.md §C: CrUX may already pass even where lab fails. The MISSION target is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (MISSION 3) → mobile 46–72, desktop 68–72 (see §A)
- **Scope:** golden path: all golden pages, mobile
- **Evidence:**
  - Home — mobile: perf 63 ✗cut · LCP 10.31s · TBT 258.0ms · SI 4.89s · CLS 0.082
  - Home — desktop: perf 89 ✗cut · LCP 1.89s · TBT 118.0ms · SI 1.31s · CLS 0.01
  - Collection — mobile: perf 38 ✗cut · LCP 13.81s · TBT 1145.0ms · SI 7.18s · CLS 0.0
  - Collection — desktop: perf 91 ✗cut · LCP 1.57s · TBT 145.0ms · SI 1.21s · CLS 0.014
  - Product — mobile: perf 73 ✗cut · LCP 5.81s · TBT 148.0ms · SI 4.33s · CLS 0.0
  - Product — desktop: perf 88 ✗cut · LCP 1.85s · TBT 146.0ms · SI 1.38s · CLS 0.01

### PERF-2 · Total byte weight
- **What / why:** PSI opportunity/diagnostic: total byte weight. Each entry is a real resource Lighthouse flagged on the mobile run — the JS/CSS/image bytes and main-thread time dragging the score. These are the levers behind the low mobile Performance number.
- **Source:** PSI Lighthouse · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (MISSION 3) → 3691 KB across 17
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - a9718981-6dfa-7456-9050-fa81f3c911dd.jpg · 667 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 559 KB
  - A5F28067-4796-4A74-B37E-B7A62E82074C.jpg?v=1780627508&width… · 389 KB
  - DEDBDABF-D6B8-4640-86AD-813F871F8085.jpg?v=1780627416&width… · 286 KB
  - 0C044970-DB33-4536-AA9C-D5B7E2C56231.jpg?v=1780627508&width… · 261 KB
  - hydrate.BmC6CJqD.js · 223 KB
  - image_87259bf7-e93b-44ef-a04c-888aa23b10da.heic?v=171164249… · 183 KB
  - IMG-1767.jpg?v=1711642495 · 158 KB
  - (+9 more — see raw/*.psi.json)

### PERF-3 · Unused JavaScript
- **What / why:** PSI opportunity/diagnostic: unused javascript. Each entry is a real resource Lighthouse flagged on the mobile run — the JS/CSS/image bytes and main-thread time dragging the score. These are the levers behind the low mobile Performance number.
- **Source:** PSI Lighthouse · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (MISSION 3) → 815 KB across 11
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 392 KB
  - js?id=G-G3RDTGKWR4 · 82 KB
  - fera.js · 67 KB
  - protect.widget.js · 50 KB
  - portable-wallets.en.js · 42 KB
  - b0638fccbw0def4e15pf2fc89d8m825804c5m.js · 35 KB
  - embed.js · 33 KB
  - freeshippingbar.js?shop=hazelboutiquenj.myshopify.com · 33 KB
  - (+3 more — see raw/*.psi.json)

### PERF-4 · JS bootup (parse/compile/exec)
- **What / why:** PSI opportunity/diagnostic: js bootup (parse/compile/exec). Each entry is a real resource Lighthouse flagged on the mobile run — the JS/CSS/image bytes and main-thread time dragging the score. These are the levers behind the low mobile Performance number.
- **Source:** PSI Lighthouse · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (MISSION 3) → 15959 ms across 23
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - all-hazel-brand · 4542 ms
  - / · 2787 ms
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 1740 ms
  - the-capri-collection-baby-pink · 1716 ms
  - Unattributable · 1376 ms
  - fera.js · 1102 ms
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 430 ms
  - embed.js · 357 ms
  - (+15 more — see raw/*.psi.json)

### PERF-5 · Main-thread work
- **What / why:** PSI opportunity/diagnostic: main-thread work. Each entry is a real resource Lighthouse flagged on the mobile run — the JS/CSS/image bytes and main-thread time dragging the score. These are the levers behind the low mobile Performance number.
- **Source:** PSI Lighthouse · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (MISSION 3) → 11893 ms across 7
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 6116 ms
  - Other · 2437 ms
  - Style & Layout · 1578 ms
  - Script Parsing & Compilation · 994 ms
  - Garbage Collection · 282 ms
  - Rendering · 260 ms
  - Parse HTML & CSS · 227 ms

## SEC — Security

### SEC-1 · Missing security response headers
- **What / why:** Standard hardening headers absent from responses. These reduce XSS, clickjacking, and referrer-leak exposure. On Shopify (hosted, Advanced plan) the platform sets some headers and limits what a theme can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.
- **Source:** SiteOne crawl · security table
- **Target → measured:** All present (BASELINE §F) → 4 of 4 missing
- **Scope:** sitewide: all responses
- **Evidence:**
  - HSTS: not set — Strict-Transport-Security header is not set. It enforces secure connections and protects against MITM attacks.
  - CSP: not set — Content-Security-Policy header is not set. It restricts resources the page can load and prevents XSS attacks.
  - Referrer-Policy: not set — Referrer-Policy header is not set. It controls referrer header sharing and enhances privacy and security.
  - Permissions-Policy: not set — Permissions-Policy header is not set. It allows enabling/disabling browser APIs and features for security.

### SEC-2 · Access-Control-Allow-Origin: *
- **What / why:** A response allows any origin to read it. Usually fine for public CDN assets, a risk if it's on anything credentialed. Check which responses carry it.
- **Source:** SiteOne crawl · security table
- **Target → measured:** No over-permissive CORS → flagged
- **Scope:** sitewide: flagged responses
- **Evidence:**
  - Access-Control-Allow-Origin is set to '*' which allows any origin to access the resource. This can be a security risk.

### SEC-3 · No Brotli compression
- **What / why:** Responses aren't served with Brotli. Brotli beats gzip on text (HTML/CSS/JS), trimming transfer bytes. On Shopify this is largely platform-controlled — likely not theme-fixable; record as a platform note unless proven otherwise.
- **Source:** SiteOne crawl · summary rollup
- **Target → measured:** Brotli on (BASELINE §F) → 203 of 200 pages
- **Scope:** sitewide: 203 / 200
- **Evidence:**
  - 203 page(s) served without Brotli

## BP — Best practices / structure

### BP-1 · errors-in-console
- **What / why:** JavaScript errors logged to the browser console. Each is a script failing at runtime — broken behavior, often from an app embed or a theme script. Read the messages; they name the file.
- **Source:** PSI Lighthouse · best-practices · `errors-in-console`
- **Target → measured:** Best Practices ≥ 95 (MISSION) → on 6 run(s)
- **Scope:** golden path: Collection — desktop, Collection — mobile, Home — desktop, Home — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - Error fetching recommendations: Error: HTTP error! Status: 422 at https://hazelboutique.com/:904:17
  - Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
  - Failed to load resource: the server responded with a status of 400 (Bad Request)
  - Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)
  - (+8 more)

### BP-2 · image-aspect-ratio
- **What / why:** An image is displayed at a ratio that doesn't match its file. Looks stretched/squashed; can also shift layout. A width/height or CSS sizing mismatch.
- **Source:** PSI Lighthouse · best-practices · `image-aspect-ratio`
- **Target → measured:** Best Practices ≥ 95 (MISSION) → on 2 run(s)
- **Scope:** golden path: Home — desktop, Home — mobile
- **Evidence:**
  - https://cdn.shopify.com/s/files/1/0051/3264/8566/files/script-logo.png?v=1713629.5093
  - https://cdn.shopify.com/s/files/1/0051/3264/8566/files/hazel-mobile-logo.png?v=1713629.5093

### BP-3 · inspector-issues
- **What / why:** Issues Chrome's Issues panel flagged (cookies, mixed content, etc.). Browser-level warnings; open the raw audit for the specifics.
- **Source:** PSI Lighthouse · best-practices · `inspector-issues`
- **Target → measured:** Best Practices ≥ 95 (MISSION) → on 2 run(s)
- **Scope:** golden path: Collection — desktop, Product — desktop
- **Evidence:**
  - (see raw/*.psi.json)

### BP-4 · deprecations
- **What / why:** Use of a deprecated browser API. Will break in a future browser version. Usually inside a third-party script.
- **Source:** PSI Lighthouse · best-practices · `deprecations`
- **Target → measured:** Best Practices ≥ 95 (MISSION) → on 1 run(s)
- **Scope:** golden path: Product — desktop
- **Evidence:**
  - https://hazelboutique.com/products/the-capri-collection-baby-pink

### BP-5 · Invalid inline SVG
- **What / why:** 204 page(s) flagged: invalid inline svg. Malformed inline SVG markup — can render wrong or bloat the DOM. Usually a theme snippet or app-injected icon.
- **Source:** SiteOne crawl · summary rollup
- **Target → measured:** 0 pages (BASELINE §F) → 204 of 200
- **Scope:** sitewide: 204 / 200
- **Evidence:**
  - 204 page(s) flagged — see crawl.html

### BP-6 · Duplicated inline SVG
- **What / why:** 23 page(s) flagged: duplicated inline svg. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common in Dawn — low priority.
- **Source:** SiteOne crawl · summary rollup
- **Target → measured:** 0 pages (BASELINE §F) → 23 of 200
- **Scope:** sitewide: 23 / 200
- **Evidence:**
  - 23 page(s) flagged — see crawl.html

### BP-7 · Non-clickable phone number
- **What / why:** 1 page(s) flagged: non-clickable. A phone number shown as text with no tel: link. On mobile it can't be tapped to call.
- **Source:** SiteOne crawl · summary rollup
- **Target → measured:** 0 pages (BASELINE §F) → 1 of 200
- **Scope:** sitewide: 1 / 200
- **Evidence:**
  - 1 page(s) flagged — see crawl.html
