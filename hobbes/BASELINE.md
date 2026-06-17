# Baseline — operator guide

This is the operating procedure to capture a web baseline. You run the cycle with Hobbes assistance. Hobbes does most of the write-up and then a human makes the judgment calls that no tool can make and a human signs off the manual rows.

Run it at the start of an engagement and at the start of each work cycle. It will produce a dated scorecard and a findings doc.Run it every cycle against the previous baseline. Any metric that slipped below its target since last cycle is a regression. 

## Tools

- **PageSpeed Insights (PSI)** — the primary measurement tool, run by Hobbes through the API: `python3 hobbes/tools/psi.py`. PSI runs Lighthouse on Google's servers and returns all four category scores (Performance, Accessibility, Best Practices, SEO) for mobile and desktop, the lab metrics, *and* CrUX field data — real-user measurements over the last 28 days, the only trustworthy source for INP. The tool pulls lab and field **separately** and labels them, caps concurrency, retries, caches each call, flags incomplete runs, and writes a `hobbes/tools/psi-results.md` artifact. The API key lives at `hobbes/tools/.psi-key`. The human cross-check is the same engine in the browser at `pagespeed.web.dev` (no key needed) — read the field panel first. One hard limit: PSI exposes **no throttle control**; mobile is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so a genuinely heavy page can take ~60s and may return "incomplete." That is real signal about a slow page, not a tool fault.
- **Lighthouse (Chrome DevTools / `npx lighthouse`)** — the local fallback for when PSI cannot reach a URL: an unpublished theme draft, a preview link, localhost, or anything gated. Same four Lighthouse categories, but lab data only — no field data, no real INP, and scores run ~10–15 points off PSI.
- **Accessibility audits (axe-core via PSI)** — the automated a11y scan is already in the PSI run. `psi.py` reads Lighthouse's accessibility audits — which *are* axe-core checks — and reports each failing rule with its node count (Section D): `color-contrast` is the contrast-error count, `image-alt` the alt gaps. No separate scan needed. (WAVE — `wave.webaim.org` — stays available as an optional human spot-check, but it is not part of the automated run.)
- **SiteOne Crawler** — the whole-site crawler. Free, open-source (MIT), no page cap. One crawl reports missing/duplicate titles and descriptions, missing H1s, broken links and redirects, plus accessibility checks (alt text, lang, form labels, ARIA, heading order) and slow URLs, as a sortable HTML report. macOS: `brew install janreges/tap/siteone-crawler`, or the desktop GUI app.
- **Google Rich Results Test** — `search.google.com/test/rich-results`. Confirms the page's structured data is valid.
- **Google Search Console** — Google's own search report. Free but needs client-granted access. Use it when you have it.
- **Shopify admin → Online Store Speed report + `theme check`** — Shopify clients only. Shopify's own performance score, plus a scan of the theme code for errors and warnings.
- **WebPageTest** — `webpagetest.org`. Optional, advanced. A deeper test for working out *why* a page is slow. Skip it unless performance needs investigating.

## Setup — once per client

- [ ] **Identify the client.** Record name, site URL, platform, date, who set it up, and anything else worth documenting.
- [ ] **Lock the golden path.** Pick 3–4 important pages with exact URLs — typically home, collection, product. Reuse these exact URLs every cycle so results stay comparable.
- [ ] **Establish the measurement method.** Hobbes runs the PSI API via `hobbes/tools/psi.py` — Google's standardized server runs it the same way every cycle, so numbers stay comparable. One pass captures Mobile and Desktop. Only when a URL is not publicly reachable (theme draft, localhost, staging) fall back to local Lighthouse (Chrome Incognito, extensions off, median of 3) — and never mix PSI and local scores within one baseline.

## The run

The baseline comes in two tiers, and naming them keeps a partial run honest:

- **MVP baseline (A–E) — fully automated.** Hobbes runs the two tools and fills every cell in sections A–E. This is a *complete* baseline on its own — a real, comparable, trustworthy snapshot. An A–E run is finished work, not a fraction of one.
- **Above-and-beyond (F) — human.** The manual accessibility pass. Optional per cycle; the MVP baseline stands without it, but a page is not certified *fully* pass until F is signed.

The tools cover all 6 page×device combinations in one go; the manual pass is per page.

### 1. Automated capture (Hobbes)

**One command runs the whole MVP baseline:**

```
python3 hobbes/tools/baseline.py            # fresh capture (the real baseline)
python3 hobbes/tools/baseline.py --resume   # reuse cache to recover a stalled run
```

`baseline.py` runs **both tools together — `psi.py` then `seo.py`** — and stamps a dated `hobbes/scorecards/YYYY-MM-DD-baseline.md` from `TEMPLATE.md`: header and golden path filled, sections **A–E** pasted in (A–D from PSI, E from SEO), section **F** left blank for the human pass. It fetches fresh by default (a baseline must reflect the current site); if a run stalls partway the successful calls are cached, so `--resume` picks up the rest. If either tool errors it aborts rather than write a half-scorecard. The two tools it drives:

**`python3 hobbes/tools/psi.py`** — calls the PSI API for each golden-path page × mobile/desktop and fills **A** (category scores), **B** (lab metrics), **C** (field/CrUX), and **D** (accessibility — the failing axe audits, since PSI's a11y category *is* axe-core), writing `hobbes/tools/psi-results.md`. Run it standalone only to refresh A–D alone. What it guarantees, so the run-1 mistakes can't recur:

1. **Field and lab are pulled separately and labelled** — a CrUX field number can never land in a lab row (the failure behind run-1's "Home LCP 1.6 vs 7.5"). **B** is lab only; **C** is field only.
2. **Field is per page** (CrUX, 28 days — the only trustworthy INP). A page without page-level data is marked `origin agg.` (the whole-site average), never passed off as the page's own; no data at all → INP **unverified**.
3. **Incomplete runs are classified, not lumped.** A ⚠ row never reached network-idle — its early metrics (FCP, CLS, TBT, Speed Index, and the category scores) still stand; only a `✗cut` LCP / Performance score is the cutoff artifact, to be treated as unknown. Re-measuring won't help (local Lighthouse hits the same wall) — investigate why the page never idles.
4. **Accessibility (D)** rides the same run — failing axe rules with node counts (`color-contrast` = contrast errors, `image-alt` = alt gaps). No separate WAVE/axe scan.
5. **Agent-reliable** — concurrency capped, calls retried, each success cached (a re-run resumes), one failed call can't kill the run.

**`python3 hobbes/tools/seo.py`** — fetches each page's HTML and fills **E** (SEO checklist + the site-level `sitemap.xml` / `robots.txt`), writing `hobbes/tools/seo-results.md`; run it standalone only to refresh E alone. It parses title, meta description, canonical, single-H1 + heading order, JSON-LD structured-data type, Open Graph/Twitter, image-alt **coverage**, and indexability. Alt-text *quality* is left to the human (F).

**Optional deeper SEO** (not automated, run when a per-page check flags something): the **Google Rich Results Test** (`search.google.com/test/rich-results`) validates structured-data *correctness* — seo.py only confirms a type is present — and **SiteOne Crawler** sweeps the whole site for missing titles/descriptions/alt and broken links.

**Non-public URLs (fallback).** The PSI API only reaches the live, public site. To baseline an unpublished theme draft, preview URL, localhost, or anything gated, run Lighthouse locally instead (Chrome Incognito, extensions off → DevTools → **Lighthouse** → pick the device → run 3× and take the median). Local scores run ~10–15 points off PSI, so never mix the two within one baseline.

### 2. Manual accessibility pass — Section F (Human; tools cannot judge these)

Optional per cycle — the automated baseline (A–E) stands on its own — but **a page is never certified fully pass until these are signed.** A page is never green on automated numbers alone.

1. **Keyboard only.** Set the mouse aside. Tab forward, Shift+Tab back, Enter/Space to activate. Try browse → open a product → add to cart → reach checkout without the mouse. Note anywhere you get stuck or cannot get out — a "trap".
2. **Visible focus.** As you Tab, confirm you can always see what is selected (outline or ring). Note any element where the highlight vanishes.
3. **Logical order.** Does Tab move in the order things appear on screen (roughly top to bottom)? Note strange jumps.
4. **Screen reader.** Turn it on (Mac VoiceOver `Cmd+F5`; Windows NVDA/Narrator). Listen to the top of the page and one product. Does it make sense? Are buttons announced by what they do ("Add to cart") rather than just "button"?
5. **Alt-text quality.** Confirm product images describe themselves ("sage green mock neck, front view") rather than a filename ("IMG_0421.jpg") or nothing. A tool only checks that alt text *exists* (the coverage count is in E); you check that it is *useful*.
6. **Color contrast.** Look for hard-to-read text — light gray on white, text over a busy photo, button text on hover. Note anything that strains (D gives the automated `color-contrast` count; this is the by-eye pass).
7. **Reduced motion.** Turn on the OS "reduce motion" setting (Mac: System Settings → Accessibility → Display → Reduce motion). Confirm animations actually calm down. Record pass/fail in Section F.

**Two numbers a green lab result will lie about:** INP (lab shows TBT only) and interaction-driven CLS. Never mark these "pass" on lab data — confirm with manual interaction or the field data in **C**.

## The scorecard

Copy `hobbes/scorecards/TEMPLATE.md` to `hobbes/scorecards/YYYY-MM-DD-baseline.md` and fill it in. **First fill the header** — replace the `# Baseline scorecard — YYYY-MM-DD` title and the `Client / Site / Platform / Run by / Date / Golden path` line with real values (no leftover placeholders); then paste sections A–E from the tool artifacts. That filled file is the baseline. **Filename convention: `[date]-[name].md`** — date first (ISO 8601), so a directory listing sorts chronologically. Same shape for every deliverable below.

## Targets — the pass bar (same for every client)

- **Lighthouse performance:** ≥ 90, desktop and mobile
- **Lighthouse accessibility:** 100, desktop and mobile
- **Lighthouse best practices:** ≥ 95, desktop and mobile
- **Lighthouse SEO:** ≥ 95, desktop and mobile
- **LCP:** ≤ 2.5s, desktop and mobile
- **INP:** ≤ 200ms, desktop and mobile
- **CLS:** ≤ 0.1, desktop and mobile
- **Accessibility audit failures (axe via PSI, Section D):** 0, including 0 `color-contrast`, desktop and mobile
- **Manual a11y (Section F):** keyboard pass · focus visible · screen reader pass · 0 contrast fails · 100% meaningful alt
- **SEO checklist:** every item passing

## Deliverables

- `hobbes/scorecards/YYYY-MM-DD-baseline.md` — the filled scorecard (the numbers).
- `hobbes/scorecards/YYYY-MM-DD-findings.md` — each failure as: *page → what is failing → the fix → effort (S/M/L)*.
- `hobbes/MISSION.md` — priorities updated with each gap, written `baseline → target` so it is testable.

## Site-type adaptations

The **Targets** never change — they are the standard. What adapts per archetype is (1) the test surface (which pages), (2) the extra checks that carry more weight, and (3) which data source you trust.

If a target genuinely cannot be met (e.g. ad-funded performance), document the exception in the findings doc with field-data justification. Do not silently lower the bar.

**Shopify storefront (default).** Covered above. Watch for JS bloat from installed Shopify apps — each adds scripts. Use `theme check`, Product JSON-LD, and Shop Pay / express checkout.

**Non-Shopify ecommerce (WooCommerce / Magento / BigCommerce / headless).** Same three core pages. What changes:

- Swap the platform tools — no Shopify speed report or `theme check`. Use Query Monitor (Woo), the built-in profiler (Magento), or a bundle analyzer (headless).
- **Weight TTFB harder.** TTFB is a standard Scorecard B column for every site, but on self-hosting it carries more diagnostic weight: you control the server, so slow TTFB from uncached queries and plugin bloat is often the real villain — not a fixed platform cost as on Shopify.
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
