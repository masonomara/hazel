# Execution — 2026-06-22 (21:44 re-measurement · validation pass)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Branch: `hobbes-cycle-2026-06-22` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s order, checks it against the **real codebase and the re-measured data**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This is the **21:44 CDT re-measurement** of the 2026-06-22 cycle. The prior pass (PR #17, 19:17 data) shipped the cart-drawer `card-collection` heading fix into `main` and bet that skipped-level would move off 185/185. This run carries the **fresh crawl/PSI taken after that merge** — and the bet paid: **skipped-level 185 → 4**, SiteOne Accessibility 5.0 → 5.8. The deliverable is therefore the **refreshed cycle data + plan + execution**, carried in one branch and one PR, recording the measured proof and handing each remainder to its owner. There is no new theme code, and that is the honest result, not under-delivery (see §1).

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~22 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged work, filtered to **theme code Hobbes can author safely without a browser** (not content, not app-config, not platform) — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main` and the re-measured findings:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Heading hierarchy & outline | 1 | ⚪ **merged + proven** | cart-drawer `card_heading_tag: 'div'` is in `main` (PR #17); this run's crawl confirms it (185 → 4). Residual = publish + content + app, no code |
| 2 | SYS-2 · Theme a11y controls (label) | 2 | ⚪ merged | hero `strip_html` in `main`; live awaits publish |
| 3 | SYS-3 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-4 · Image alt | 3 | ⚪ merged / content | card-image alt fallback merged; meaningful alt is content |
| 5 | SYS-5 · Page metadata (dup copy) | 3 | ⛔ content | duplicate titles/descriptions = admin renames + bespoke copy |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path & CLS | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; dup JS has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is empty of new code, and why that is "do everything," not under-delivery.** Every system's theme code is **already merged into `main`** (PRs #8/#10/#11/#16/#17). The top system, SYS-1, was the one open question carried into this cycle — *did the cart-drawer fix actually move the universal skipped-level count?* The re-measurement answers it: **yes, 185 → 4** (`diff.md`; §F Accessibility 5.0 → 5.8). With that confirmed, the *genuinely remaining* work decomposes to:

- **Theme code Hobbes can ship → none.** SYS-1's code is merged and now measured-good. I traced the 4 residual heading pages from `raw/crawl.json` (`seo-headings`) to be sure no *new* code closes them:
  - `/` and `/collections/new-arrivals-1` still emit the cart-drawer promo collections' four `<h3>` ("Fine Jewelry" ×2, "All Sale Items" ×2). This is the **exact defect PR #17 fixed**; it persists only because the crawler still rendered the empty-cart drawer on these two pages and the fix is unpublished. **Publishing `main` closes them** — re-applying the same fix would be a no-op.
  - `/pages/sizing` — `h1 → h3` skip from the size-chart sub-headings in the **admin page body** (`page.json` is `main-page` only; the headings are content, not Liquid). **Jenna/Britni**, in the page editor.
  - `/pages/search-results` — a second, empty `<h1>` (`#isp_results_summary`) injected by the **search app**. **App config**, not the repo.
- **Human-owned, by proof, not assertion:** SYS-3 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts the theme repo can't touch), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-3/4 duplicate titles+descriptions, PERF-2/5 image re-exports, SYS-4 meaningful alt, the sizing-page headings.
- **SYS-8** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected (not in the repo), and the duplicated JS has no reliable Liquid cross-section dedup while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **every safe theme-code fix that the findings justify is already in `main`; this run records the measured proof that the lead fix works and hands each non-code remainder to its proven owner.** I considered and rejected pushing the `card-collection` double-heading fix further (removing the always-on `:112` heading for in-page `collection-list`/`collage`/`main-list-collections` cards): it is *not* currently flagging any page (those cards sit correctly as `<h3>` under their section `<h2>`), the `:112` heading is the **visible** one for the `card--standard.card--text` style, and changing it is a browser-gated regression risk the data does not justify. Inventing it would violate "invent nothing."

**Deferred this cycle (named, not silent), with owner:**
- **SYS-1 publish** — the merged cart-drawer fix must go live for `/` + `/collections/new-arrivals-1` to clear → **Mason** (publish gate).
- **SYS-1 `/pages/sizing`** — re-tag the four size-chart `<h3>` to `<h2>` (or add a parent `<h2>`) in the page body → **Jenna/Britni** (admin content).
- **SYS-1 `/pages/search-results`** — suppress/relevel the search app's injected `<h1>` → **app config** (whoever owns the search app).
- **SYS-3 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-4 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-5 duplicate titles + descriptions** — collection renames + bespoke copy in admin → Jenna/Britni.
- **SYS-6 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Verification against the real source

No new edits this run, so the "implementation" is a confirmation that the merged code is present and correct and that the data's improvement maps to it:
- **`snippets/card-collection.liquid`** — carries `assign card_heading_tag = card_heading_tag | default: 'h3'` (`:28`) and renders all three `card__heading` elements from it (`:112/:135/:190`). Default `'h3'` keeps the three in-page callers (`collage`, `collection-list`, `main-list-collections`) byte-identical. ✓ in `main`.
- **`snippets/cart-drawer.liquid`** — both empty-cart promo renders pass `card_heading_tag: 'div'` (`:110`, `:119`). ✓ in `main`.
- **Data mapping** — `raw/crawl.json` `seo-headings` shows the leading `h3 h3 h3 h3` run = the two cart-drawer collections, gone from 181/185 pages and present only where the drawer rendered; `diff.md` records 185 → 4. The fix and the measured improvement line up exactly.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review.
- **Theme Check:** no edits to `.liquid` this run → no new offenses by construction. (The pre-existing `icon-shop-pay.liquid` error is out of scope.)
- **Browser (human, at review):** after publish, re-run the SiteOne crawl and confirm `/` + `/collections/new-arrivals-1` drop off the skipped-level list (expected → ~2 remaining: sizing-content + search-app, both human-owned).
- **Fork-safe:** no code change; data + docs only.
- **No baseline regression** against `baseline.md` targets — `diff.md` confirms 0 field regressions.
- **No unnecessary comments**; no code touched.

## 4. Todo

**Phase 1 — SYS-1 heading outline (code)**
- [x] A1 · Confirm `card-collection.liquid` `card_heading_tag` default `'h3'` + 3 elements rendered from it is in `main` (SEO-1 / A11Y-3)
- [x] A2 · Confirm `cart-drawer.liquid:110,119` pass `card_heading_tag: 'div'` is in `main` (SEO-1 / A11Y-3)
- [x] A3 · Trace the 4 residual skipped-level pages from `raw/crawl.json` → cart-drawer (publish), sizing (content), search (app); confirm no new code closes them

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-22`, `git add -A` (refreshed data + plan + execution), commit, push
- [x] H2 · open ONE PR (cycle data + the merged fix it validates) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- SEO-1 heading structure — **4 of 185** pages flag a skipped heading level (down from 185 last cycle) and **1** page multiple-H1. The 4: `/` + `/collections/new-arrivals-1` (cart-drawer residue, publish-gated), `/pages/sizing` (page-body content), `/pages/search-results` (search-app `h1`). Target: single H1 + ordered headings, all pages (BASELINE §E/§F).
- A11Y-3 sitewide a11y prevalence — **1,761 flagged elements across 185 pages** (1,756 HTML-structural, the heading-order family). Falls with the outline as the fix publishes. Target: 0.
- Cycle deltas vs 2026-06-21 (`diff.md`): **0 field regressions**; a11y rules improved — heading-order 1→0, image-alt 4→0; **skipped heading levels 185 → 4**; sitewide multiple-H1 2 → 1; SiteOne Accessibility quality 5.0 → 5.8; total findings 39 → 35.

**After (measured):** the *publish* after for the cart-drawer residue lands in the next cycle's `diff.md` — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The decisive signal will be `/` + `/collections/new-arrivals-1` dropping off the skipped-level list, leaving only sizing-content + search-app. **This run already banks the partial after for the 181 pages the fix cleared (185 → 4)** — measured, not fabricated.

**Carried by this PR:** the refreshed 21:44 cycle data (baseline/findings/diff/digests) + this plan + execution. The theme-code fix it validates — SYS-1 cart-drawer `card_heading_tag: 'div'` — is already in `main` (PR #17); this PR's job is to record the measurement that proves it worked, not to re-ship it.

**Already merged (awaiting publish):** PR #17 — SYS-1 cart-drawer heading fix. PR #16 — hero slide-link `strip_html`. Earlier PRs — slideshow/pagination labels, card-image alt fallback, card-product `h3→h2` + stray product `h1→h2`, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Deferred (named in §1, with owner):** SYS-1 publish (Mason) + sizing content (Jenna/Britni) + search-app `h1` (app); SYS-3 Mailchimp (app/marketing); SYS-4 meaningful alt (content); SYS-5 duplicate titles+descriptions (content); SYS-6 image re-exports (content); SYS-7 app JS (business + app-config); SYS-8 CSS/JS path (browser-gate); SYS-9 Permissions-Policy (platform).
