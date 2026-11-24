# Findings — 2026-11-24-B

Site: https://hazelboutique.com/ · Generated 2026-11-24 12:52 EST by `hobbes/tools/evaluation.py` from `raw/`.

The problem catalog — dense, deterministic, agent-facing. 26 findings. Every failing check is enumerated straight from `raw/` — no shortlist, no mission weighting, no hand-picking; same raw always yields the same findings. Where a list is long it is capped with an explicit `+N more`, never silently trimmed. Numbers and scorecard in `01-baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. See `hobbes/templates/02-evaluation-template.md`.

## A11Y — Accessibility

### A11Y-1 · Missing aria labels (sitewide)
- **What / why:** Missing aria labels — flagged across the crawl. An interactive element has no accessible name (aria-label / aria-labelledby). A screen reader announces it by role alone — 'button', 'link', 'textbox'. This hits icon-only controls and unlabeled inputs like the search box.
- **Source:** SiteOne crawl · accessibility detail
- **Target → measured:** 0 issues (BASELINE §F) → 2395 element(s) across 100 pattern(s)
- **Scope:** sitewide: 16 page(s)
- **Evidence:**
  - [warning] ×348 · `<a class="link link-* list-* list-*" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×326 · `<a ***>` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×80 · `<button class="menu-* link link-* focus-*" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×48 · `<a class="button" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×32 · `<a class="megaMenuCollection megaMenuCollectionTwo" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×32 · `<button class="alerts-* button button-* button-*" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - (+94 more pattern(s) — see raw/crawl-report.html)

### A11Y-2 · Missing form labels (sitewide)
- **What / why:** Missing form labels — flagged across the crawl. Accessibility issue SiteOne flagged across the site.
- **Source:** SiteOne crawl · accessibility detail
- **Target → measured:** 0 issues (BASELINE §F) → 128 element(s) across 4 pattern(s)
- **Scope:** sitewide: 16 pages crawled
- **Evidence:**
  - [warning] ×32 · `<input class="field_*" name="EMAIL" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×32 · `<input name="b_bb68751aca24eb8005a87da31_7488b9bad***" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×32 · `<input class="field_*" name="SMSPHONE" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)
  - [warning] ×32 · `<input name="mc-SMSPHONE-ack" *** >` · /pages/shipping-and-delivery, /pages/divider, / (+2 more)

## SEO — SEO & discoverability

— all checks pass.

## PERF — Performance

### PERF-1 · Lab performance below target
- **What / why:** Lighthouse Performance score and the lab metrics behind it, per page × device. PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in 01-baseline.md §C: CrUX may already pass even where lab fails. The pass bar is still lab ≥ 90.
- **Source:** PSI Lighthouse · performance
- **Target → measured:** Performance ≥ 90, mobile + desktop (BASELINE Targets) → score range 47–72 across runs (see §A)
- **Scope:** golden path: all golden pages × device
- **Evidence:**
  - Home — mobile: perf 59 · LCP 20.18s · TBT 338.0ms · SI 6.91s · CLS 0.0
  - Home — desktop: perf 47 · LCP 2.46s · TBT 351.0ms · SI 1.03s · CLS 1.0
  - Collection — mobile: perf 56 · LCP 4.95s · TBT 159.0ms · SI 1.69s · CLS 0.988
  - Collection — desktop: perf 60 · LCP 2.32s · TBT 155.0ms · SI 1.08s · CLS 1.0
  - Product — mobile: perf 56 · LCP 5.03s · TBT 100.0ms · SI 2.57s · CLS 0.985
  - Product — desktop: perf 72 · LCP 1.24s · TBT 72.0ms · SI 1.03s · CLS 1.0

### PERF-2 · Improve image delivery
- **What / why:** Reducing the download time of images can improve the perceived load time of the page and LCP. Learn more about optimizing image size.
- **Source:** PSI Lighthouse · performance · `image-delivery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 1867 KB across 38 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - IMG_5674.jpg?v=1795136244&width=3840 · 441 KB
  - IMG_5695.jpg?v=1795136248&width=3840 · 345 KB
  - IMG_5677.jpg?v=1795136247&width=3840 · 302 KB
  - library-AA1DA762-AC00-4FDB-B725-824A17B708D2-L0-001.jpg?v=1… · 44 KB
  - library-F1E77C1A-99FC-4D97-90A6-2FC7DC9D0BF0-L0-001.jpg?v=1… · 36 KB
  - library-7CC5762E-FF55-4E60-8116-D714177138DA-L0-001.jpg?v=1… · 35 KB
  - library-100FF316-B6F6-46F6-A63F-CFE8DEC8D838-L0-001.jpg?v=1… · 32 KB
  - library-8604DB98-6CCE-4EF6-A46A-0891B0E8B15C-L0-001.jpg?v=1… · 32 KB
  - (+30 more — see raw/*.psi.json)

### PERF-3 · Avoid enormous network payloads
- **What / why:** Large network payloads cost users real money and are highly correlated with long load times. Learn how to reduce payload sizes.
- **Source:** PSI Lighthouse · performance · `total-byte-weight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2910 KB across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 542 KB
  - IMG_5674.jpg?v=1795136244&width=3840 · 456 KB
  - 6ec9a0fa.D7fKZKSJ.js · 371 KB
  - IMG_5695.jpg?v=1795136248&width=3840 · 358 KB
  - IMG_5677.jpg?v=1795136247&width=3840 · 313 KB
  - js?id=G-G3RDTGKWR4 · 160 KB
  - protect.widget.js · 110 KB
  - 11A7A393-C1D9-40E2-B701-6FCD102C4B90.jpg?v=1721329642&width… · 107 KB
  - (+7 more — see raw/*.psi.json)

### PERF-4 · Reduce JavaScript execution time
- **What / why:** Consider reducing the time spent parsing, compiling, and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to reduce Javascript execution time.
- **Source:** PSI Lighthouse · performance · `bootup-time` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2742 ms across 15 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Unattributable · 551 ms
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 507 ms
  - / · 468 ms
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 205 ms
  - shopify-perf-kit-3.16.1.min.js · 141 ms
  - instafeed-f7b8eba84b8f7bd54aa596dae96229ce.js · 135 ms
  - js?id=G-G3RDTGKWR4 · 131 ms
  - scripts.js?v=93736053516032179081771610579 · 108 ms
  - (+7 more — see raw/*.psi.json)

### PERF-5 · Use efficient cache lifetimes
- **What / why:** A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
- **Source:** PSI Lighthouse · performance · `cache-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 860 KB across 14 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 542 KB
  - protect.widget.js · 110 KB
  - portable-wallets.en.js · 80 KB
  - protect.core.js?shop=hazelboutique.com · 54 KB
  - da-restock.js?shop=hazelboutiquenj.myshopify.com · 23 KB
  - modal.js?shop=hazelboutiquenj.myshopify.com · 21 KB
  - analytics.js · 16 KB
  - da-restock.css · 5 KB
  - (+6 more — see raw/*.psi.json)

### PERF-6 · Duplicated JavaScript
- **What / why:** Remove large, duplicate JavaScript modules from bundles to reduce unnecessary bytes consumed by network activity
- **Source:** PSI Lighthouse · performance · `duplicated-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 109 KB across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - node_modules/@route/platform-ui · 60 KB
  - node_modules/react-dom · 41 KB
  - /cdn/shop/t/51/assets/quick-add.js?v=131073536309624707681771610528 · 2 KB
  - /cdn/shop/t/51/assets/product-form.js?v=3603548357138963301771610529 · 2 KB
  - node_modules/react · 2 KB
  - node_modules/scheduler · 1 KB
  - node_modules/style-loader · 1 KB

### PERF-7 · Minimize main-thread work
- **What / why:** Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. Learn how to minimize main-thread work
- **Source:** PSI Lighthouse · performance · `mainthread-work-breakdown` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 3215 ms across 7 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - Script Evaluation · 1346 ms
  - Other · 666 ms
  - Script Parsing & Compilation · 546 ms
  - Style & Layout · 454 ms
  - Parse HTML & CSS · 76 ms
  - Garbage Collection · 66 ms
  - Rendering · 60 ms

### PERF-8 · Reduce unused JavaScript
- **What / why:** Reduce unused JavaScript and defer loading scripts until they are required to decrease bytes consumed by network activity. Learn how to reduce unused JavaScript.
- **Source:** PSI Lighthouse · performance · `unused-javascript` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 649 KB across 6 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 402 KB
  - js?id=G-G3RDTGKWR4 · 92 KB
  - portable-wallets.en.js · 54 KB
  - protect.widget.js · 51 KB
  - modal.js?shop=hazelboutiquenj.myshopify.com · 28 KB
  - instafeed-f7b8eba84b8f7bd54aa596dae96229ce.js · 23 KB

### PERF-9 · Render-blocking requests
- **What / why:** Requests are blocking the page’s initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.
- **Source:** PSI Lighthouse · performance · `render-blocking-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 28 KB across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - base.css?v=62921087886021084181795478032 · 20 KB · 651 ms
  - accelerated-checkout-backwards-compat.css · 3 KB · 489 ms
  - component-slider.css?v=76902739753078838911779286626 · 3 KB · 489 ms
  - component-slideshow.css?v=128144104580933199301771610528 · 2 KB · 489 ms

### PERF-10 · Forced reflow
- **What / why:** A forced reflow occurs when JavaScript queries geometric properties (such as `offsetWidth`) after styles have been invalidated by a change to the DOM state. This can result in poor performance. Learn more about forced reflows and possible mitigations.
- **Source:** PSI Lighthouse · performance · `forced-reflow-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 191 ms across 4 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - scripts.js?v=93736053516032179081771610579 · 87 ms
  - instafeed-f7b8eba84b8f7bd54aa596dae96229ce.js · 47 ms
  - jquery-2.2.4.min.js · 33 ms
  - modal.js?shop=hazelboutiquenj.myshopify.com · 24 ms

### PERF-11 · Legacy JavaScript
- **What / why:** Polyfills and transforms enable older browsers to use new JavaScript features. However, many aren’t necessary for modern browsers. Consider modifying your JavaScript build process to not transpile Baseline features, unless you know you must support older browsers. Learn why most sites can deploy ES6+ code without transpiling.
- **Source:** PSI Lighthouse · performance · `legacy-javascript-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 23 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - protect.core.js?shop=hazelboutique.com · 9 KB
  - shopify.widget.js?shop=hazelboutiquenj.myshopify.com · 7 KB
  - portable-wallets.en.js · 7 KB

### PERF-12 · Reduce unused CSS
- **What / why:** Reduce unused rules from stylesheets and defer CSS not used for above-the-fold content to decrease bytes consumed by network activity. Learn how to reduce unused CSS.
- **Source:** PSI Lighthouse · performance · `unused-css-rules` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 57 KB across 3 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 29 KB
  - base.css?v=62921087886021084181795478032 · 16 KB
  - instafeed-17.10.0.css · 11 KB

### PERF-13 · Layout shift culprits
- **What / why:** Layout shifts occur when elements move absent any user interaction. Investigate the causes of layout shifts, such as elements being added, removed, or their fonts changing as the page loads.
- **Source:** PSI Lighthouse · performance · `cls-culprits-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 2 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - 404 Page not found Continue shopping
  - BE THE FIRST TO KNOW ABOUT DROPS & RESTOCKS
  - COLLECTION: ALL HAZEL BRAND FILTER AND SORT THE HZL GUMDROP TANK TOP REGULAR PR…

### PERF-14 · Avoid large layout shifts
- **What / why:** These are the largest layout shifts observed on the page. Each table item represents a single layout shift, and shows the element that shifted the most. Below each item are possible root causes that led to the layout shift. Some of these layout shifts may not be included in the CLS metric value due to windowing. Learn how to improve CLS
- **Source:** PSI Lighthouse · performance · `layout-shifts` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 2 layout shifts found
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - 404 Page not found Continue shopping
  - BE THE FIRST TO KNOW ABOUT DROPS & RESTOCKS
  - COLLECTION: ALL HAZEL BRAND FILTER AND SORT THE HZL GUMDROP TANK TOP REGULAR PR…

### PERF-15 · LCP request discovery
- **What / why:** Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
- **Source:** PSI Lighthouse · performance · `lcp-discovery-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 1 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - LCP resources shouldn’t use loading=lazy
  - fetchpriority=high should be applied

### PERF-16 · Minify CSS
- **What / why:** Minifying CSS files can reduce network payload sizes. Learn how to minify CSS.
- **Source:** PSI Lighthouse · performance · `unminified-css` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → 6 KB across 1 resource(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - @font-face{font-family:RM Neue; … } … · 6 KB

### PERF-17 · Network dependency tree
- **What / why:** Avoid chaining critical requests by reducing the length of chains, reducing the download size of resources, or deferring the download of unnecessary resources to improve page load
- **Source:** PSI Lighthouse · performance · `network-dependency-tree-insight` (mobile runs)
- **Target → measured:** Performance ≥ 90 (BASELINE Targets) → flagged on 3 page(s)
- **Scope:** golden path: golden pages, mobile
- **Evidence:**
  - (see raw/*.psi.json)

### PERF-18 · Slowest URLs (server response, sitewide)
- **What / why:** The slowest pages to respond across the whole crawl — server response / TTFB-class timing. SiteOne's per-URL request timing, a broad complement to the golden-path lab metrics. Slow server response delays everything downstream; a consistently slow template or collection is worth a look even when the golden path looks fine.
- **Source:** SiteOne crawl · slowest-urls
- **Target → measured:** Fast server response, all pages (BASELINE Targets) → slowest 0.27s; top 20 listed
- **Scope:** sitewide: 20 slowest of crawl
- **Evidence:**
  - sizing · 0.27s (200)
  - / · 0.23s (200)
  - pants · 0.20s (200)
  - the-hzl-honeysuckle-mockneck · 0.19s (200)
  - the-hzl-summer-spritz-robe · 0.17s (200)
  - news · 0.17s (200)
  - privacy-policy · 0.17s (200)
  - hb-merry-little-cocktail-ornament · 0.17s (200)
  - gift-certificates · 0.16s (200)
  - shipping-and-delivery · 0.16s (200)
  - divider · 0.16s (200)
  - our-story · 0.16s (200)
  - (+8 more — see raw/crawl.json)

## SEC — Security

### SEC-1 · Missing security response headers
- **What / why:** Standard hardening headers absent from responses. These reduce XSS, clickjacking, and referrer-leak exposure. On a hosted platform the host often sets some headers and limits what the app/template can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.
- **Source:** SiteOne crawl · security table
- **Target → measured:** All present (BASELINE §F) → 4 of 4 missing
- **Scope:** sitewide: all responses
- **Evidence:**
  - HSTS: not set (162 responses) — Strict-Transport-Security header is not set. It enforces secure connections and protects against MITM attacks.
  - CSP: not set (162 responses) — Content-Security-Policy header is not set. It restricts resources the page can load and prevents XSS attacks.
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
- **Target → measured:** Best Practices ≥ 95 (BASELINE Targets) → on 3 run(s)
- **Scope:** golden path: Collection — mobile, Product — desktop, Product — mobile
- **Evidence:**
  - Failed to load resource: the server responded with a status of 429 (Too Many Requests)
  - Failed to load resource: the server responded with a status of 404 (Not Found)

### BP-2 · Duplicate inline SVGs
- **What / why:** Duplicate inline SVGs — flagged sitewide by the crawl. The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common where an icon set is inlined per use — low priority.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 1 element(s) across 1 pattern(s)
- **Scope:** sitewide: of 16 pages
- **Evidence:**
  - [warning] ×1 · `6x SVG (1436 B): <svg aria-hidden="true" focusable="false" class="icon icon-plus" width="19" height="19" view…` · /products/the-hzl-summer-spritz-robe

### BP-3 · WebP support
- **What / why:** WebP support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 16 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl-report.html

### BP-4 · AVIF support
- **What / why:** AVIF support — flagged sitewide by the crawl. Structural/best-practice issue SiteOne flagged across the site.
- **Source:** SiteOne crawl · best-practices detail
- **Target → measured:** 0 issues (BASELINE §F) → 0 critical, 1 warning
- **Scope:** sitewide: of 16 pages
- **Evidence:**
  - 0 critical, 1 warning — see raw/crawl-report.html
