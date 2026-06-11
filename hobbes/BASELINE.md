# Baseline — operator guide

This is the runbook **you, the operator, follow** to capture a web baseline. You drive the cycle. Hobbes assists: it runs what can be automated, it does the write-up, and it keeps `MISSION.md` honest — but a human makes the judgment calls no tool can make and signs off the manual rows.

Run it at the start of an engagement and at the start of each work cycle. It produces a dated scorecard and a findings doc. The numbers feed `hobbes/MISSION.md`.

## Who does what

**You own the cycle.** You run the manual passes (all of Group E, plus the human half of Group F), you make the calls a tool can't — "does this strain to read," "does the screen reader make sense" — and you sign off the accessibility and interaction rows. A page is never marked green on automated numbers alone.

**Hobbes assists.** Where the tooling is wired up (Lighthouse CLI, axe CLI, fetching field data and page source, a site crawl) Hobbes can run the automated captures itself; otherwise you run them in DevTools and Hobbes records the numbers. Hobbes owns the paperwork: filling the scorecard, drafting the findings doc, turning each gap into a `baseline → target` priority in `MISSION.md`, and appending the result to `CHANGELOG.md`.

Each group below is labeled **Automated** (you or Hobbes can run it), **Human** (only you can), or **Both** (a tool captures, a person confirms).

## The cycle

1. **Orient.** Read `hobbes/MISSION.md` and `hobbes/DEVELOPMENT.md` in full. (Hobbes does this at session start anyway.)
2. **Capture.** Measure the golden-path pages and record a dated scorecard in `hobbes/scorecards/`.
3. **Prioritize.** Turn each gap into a testable priority — written `baseline → target` — and update `MISSION.md`.
4. **Execute.** Close the gaps. Reuse the systems already in the codebase rather than standing up new ones.
5. **Verify.** Rerun the baseline. Confirm targets on both devices. Flag anything that moved.
6. **Append.** Record what changed in `hobbes/CHANGELOG.md`.

Run it every cycle against the previous baseline. Any metric that slipped below its target since last cycle is a **regression** and jumps the queue. Month over month the scorecards become the proof that the system works.

## Tools

Everything here is free unless noted. You will not need all of them every time, but know what each is for.

- **Lighthouse (Chrome DevTools)** — the all-in-one lab score for performance, accessibility, best practices, and SEO.
- **PageSpeed Insights** — `pagespeed.web.dev`. Runs Lighthouse for you and, more importantly, shows **field data**: real measurements from actual visitors over the last 28 days. This is the only trustworthy source for INP.
- **axe DevTools** — Chrome extension that scans a page for accessibility problems and sorts them by severity.
- **WAVE** — optional second accessibility checker (`wave.webaim.org` or extension). A visual double-check against axe.
- **Screaming Frog SEO Spider** — free up to 500 pages. Crawls the whole site at once and lists missing titles, descriptions, alt text, and broken links. Far faster than page-by-page.
- **Google Rich Results Test** — `search.google.com/test/rich-results`. Confirms the page's structured data is valid.
- **Google Search Console** — Google's own search report. Free but needs client-granted access. Use it when you have it.
- **Shopify admin → Online Store Speed report + `theme check`** — Shopify clients only. Shopify's own performance score, plus a scan of the theme code for errors and warnings.
- **WebPageTest** — `webpagetest.org`. Optional, advanced. A deeper test for working out *why* a page is slow. Skip it unless performance needs investigating.

## Setup — once per client

- [ ] **Identify the client.** Record name, site URL, platform, date, who set it up, and anything else worth documenting.
- [ ] **Lock the golden path.** Pick 3–4 important pages with exact URLs — typically home, collection, product. Reuse these exact URLs every cycle so results stay comparable.
- [ ] **Establish the measurement method.** Chrome Incognito with extensions off (or Lighthouse CLI). Mobile uses Lighthouse default throttling (Moto G / slow 4G); desktop uses the desktop preset. Measure each page 3× per device and record the median.

## The run — repeat for each page × mobile + desktop

Do every group below for each of the 6 combinations: 3 pages (home, collection, product) × 2 devices. A few steps marked **once per site** are done a single time, not six.

### Group A — Lighthouse scores (Automated)

1. Open Chrome, start a new Incognito window (Ctrl+Shift+N / Cmd+Shift+N). Incognito disables extensions so they do not distort the result.
2. Go to the exact locked-in page URL.
3. Open DevTools (F12 or right-click → Inspect) → **Lighthouse** tab (click the » arrow if hidden).
4. Set **Mode** = Navigation, **Device** = Mobile or Desktop, and tick all four categories: Performance, Accessibility, Best Practices, SEO.
5. Click **Analyze page load**, wait ~30–60s. You get four scores, 0–100.
6. Run 3× and record the **median Performance** score (the other three rarely move). Put all four in Scorecard A.

### Group B — Speed metrics (Automated)

7. In the finished report, scroll to the **Metrics** box. Record FCP, LCP, TBT, CLS, and Speed Index in Scorecard B.
8. Lighthouse gives no real INP. It only estimates responsiveness via TBT. The true INP comes from field data in Group C.

### Group C — Field data / real users (Automated; once per page, not per device)

9. Go to `pagespeed.web.dev`, paste the page URL, click Analyze.
10. If a panel titled "Discover what your real users are experiencing" appears, that is the field data. Record real LCP, INP, and CLS in Scorecard B, marked "field".
11. If there is no field data, the site lacks the traffic. Write "no field data," rely on lab numbers, and flag INP as unverified.

### Group D — Accessibility scan (Automated)

12. One-time: install the free axe DevTools extension.
13. On the page, DevTools (F12) → axe DevTools tab → **Scan all of my page**.
14. Results group as Critical / Serious / Moderate / Minor. Record Critical and Serious counts in Scorecard C; copy the most common issue names into the findings doc.

### Group E — Manual accessibility pass (Human — tools cannot judge these)

15. **Keyboard only.** Set the mouse aside. Tab forward, Shift+Tab back, Enter/Space to activate. Try browse → open a product → add to cart → reach checkout without the mouse. Note anywhere you get stuck or cannot get out — a "trap".
16. **Visible focus.** As you Tab, confirm you can always see what is selected (outline or ring). Note any element where the highlight vanishes.
17. **Logical order.** Does Tab move in the order things appear on screen (roughly top to bottom)? Note strange jumps.
18. **Screen reader.** Turn it on (Mac VoiceOver `Cmd+F5`; Windows NVDA/Narrator). Listen to the top of the page and one product. Does it make sense? Are buttons announced by what they do ("Add to cart") rather than just "button"?
19. **Alt-text quality.** Confirm product images describe themselves ("sage green mock neck, front view") rather than a filename ("IMG_0421.jpg") or nothing. A tool only checks that alt text *exists*; you check that it is *useful*.
20. **Color contrast.** Look for hard-to-read text — light gray on white, text over a busy photo, button text on hover. Note anything that strains.
21. **Reduced motion.** Turn on the OS "reduce motion" setting (Mac: System Settings → Accessibility → Display → Reduce motion). Confirm animations actually calm down. Record pass/fail and any counts in Scorecard C.

### Group F — SEO checks (Both)

22. **Title & description.** Right-click → View Page Source. Confirm a unique `<title>` and a `<meta name="description">`. Read them — relevant, specific, not generic.
23. **Headings.** Exactly one `<h1>`; headings step down in order (H1 → H2 → H3) without skipping a level.
24. **Structured data.** `search.google.com/test/rich-results` → paste the URL → confirm `Product` / `Breadcrumb` / `Organization` with no errors.
25. **Open Graph.** In source, confirm `og:title`, `og:image`, etc. so shared links preview well.
26. **Indexable.** The page is not accidentally `noindex`, and its canonical points to itself.
27. **Whole-site crawl (once per site).** Run Screaming Frog to list missing titles, descriptions, alt text, and broken links across all pages at once.
28. **Site-level files (once per site).** Visit `/sitemap.xml` and `/robots.txt` and confirm both load. Record in Scorecard D/E.

**Two numbers a green lab result will lie about:** INP (lab shows TBT only) and interaction-driven CLS. Never mark these "pass" on lab data — confirm with manual interaction or field data.

**The handoff:** Hobbes produces the scorecard; you sign off the accessibility and interaction rows before any page is marked pass. A page is never green on automated numbers alone.

## The scorecard

Copy `hobbes/scorecards/TEMPLATE.md` to `hobbes/scorecards/baseline-YYYY-MM.md` and fill it in. That filled file **is** the baseline. Compare every number to the **Targets** below.

## Targets — the pass bar (same for every client)

- **Lighthouse performance:** ≥ 90, desktop and mobile
- **Lighthouse accessibility:** 100, desktop and mobile
- **Lighthouse best practices:** ≥ 95, desktop and mobile
- **Lighthouse SEO:** ≥ 95, desktop and mobile
- **LCP:** ≤ 2.5s, desktop and mobile
- **INP:** ≤ 200ms, desktop and mobile
- **CLS:** ≤ 0.1, desktop and mobile
- **axe critical / serious:** 0 / 0, desktop and mobile
- **Manual a11y:** keyboard pass · focus visible · screen reader pass · 0 contrast fails · 100% meaningful alt
- **SEO checklist:** every item passing

## Deliverables

- `hobbes/scorecards/baseline-YYYY-MM.md` — the filled scorecard (the numbers).
- `hobbes/scorecards/findings-YYYY-MM.md` — each failure as: *page → what is failing → the fix → effort (S/M/L)*.
- `hobbes/MISSION.md` — priorities updated with each gap, written `baseline → target` so it is testable.

## Site-type adaptations

The **Targets** never change — they are the standard. What adapts per archetype is (1) the test surface (which pages), (2) the extra checks that carry more weight, and (3) which data source you trust.

If a target genuinely cannot be met (e.g. ad-funded performance), document the exception in the findings doc with field-data justification. Do not silently lower the bar.

**Shopify storefront (default).** Covered above. Watch for JS bloat from installed Shopify apps — each adds scripts. Use `theme check`, Product JSON-LD, and Shop Pay / express checkout.

**Non-Shopify ecommerce (WooCommerce / Magento / BigCommerce / headless).** Same three core pages. What changes:

- Swap the platform tools — no Shopify speed report or `theme check`. Use Query Monitor (Woo), the built-in profiler (Magento), or a bundle analyzer (headless).
- Add **TTFB** to the lab metrics. Self-hosting exposes server response time that Shopify hides; slow TTFB from uncached queries and plugin bloat is often the real villain.
- Headless (Next / Nuxt / Remix): check hydration cost, bundle size, and image-optimization config. These are dev-controlled, so a11y/perf targets are more achievable than on a locked SaaS theme.

**Content-heavy / editorial / publisher.** Core pages shift to home, an article page, a category hub (add a listing/archive template if distinct). What changes:

- SEO weight rises: structured data is Article / NewsArticle / BreadcrumbList / FAQ, plus author/date markup. The full SEO checklist still applies.
- Ad tech and third-party embeds dominate total blocking time and cause late CLS. Trust field data (CrUX) over lab here — lab cannot model real ad auctions. This is where the lab-vs-field distinction matters most.
- A11y: long-form reading order, heading-hierarchy depth, and descriptive link text carry more weight.

**B2B / SaaS marketing or B2B commerce.** Core pages shift to home, a key solution/landing page, and the conversion page (pricing, contact/demo, quote request). What changes:

- Measure the primary lead form as its own surface: labels, keyboard, and validation with clear error states — the highest-stakes a11y check here, because the form is the conversion.
- Lighthouse cannot log into gated pages (portals, dashboards, quote flows). Script authenticated runs (Playwright/Puppeteer with a test login) or test manually, and flag them as human-only surfaces.
- Marketing/CRM scripts (HubSpot, Marketo, Salesforce, chat widgets, analytics) are the usual TBT culprits. Inventory them.
- SEO structured data is Organization / Product / FAQ; the checklist applies in full.
