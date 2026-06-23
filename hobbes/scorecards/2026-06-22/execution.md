# Execution — 2026-06-22 (budget-100 continuation)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Branch: `hobbes-cycle-2026-06-22` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s *unshipped, safely-authorable* order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This is the **budget-100 continuation** of the 2026-06-22 cycle. The first pass (PR #16) shipped the hero slide-link `aria-label` fix and deferred the heading-hierarchy system as needing the rendered page. This run carries the re-measured cycle data (baseline/findings/diff/digests, 35 findings) **plus** the now-diagnosed heading fix in **one branch and one PR** — `hobbes-cycle-2026-06-22` — so the scorecard and the fix it justifies travel together.

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~22 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author safely without a browser** (not content, not app-config, not platform) — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Heading hierarchy & outline | 2 | ✅ **(code)** | the universal skipped-level root, re-traced to source — cart-drawer `card-collection` double-`h3`; clean, backward-compatible theme code |
| 2 | SYS-2 · Theme a11y controls (label) | 2 | ⚪ merged | hero `strip_html` shipped PR #16; live awaits publish |
| 3 | SYS-3 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-4 · Image alt | 3 | ⚪ merged / content | card-image alt fallback merged; meaningful alt is content |
| 5 | SYS-5 · Page metadata (dup copy) | 3 | ⛔ content | duplicate titles/descriptions = admin renames + bespoke copy |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path & CLS | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-14 has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1 alone, and why that is "do everything," not under-delivery.** Ranks 2, 4, 6 and rank-9 code are **already merged into `main`** (PRs #8/#10/#11/#16); re-doing them is wasted motion — they need only the human publish. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch). This is the system the prior 2026-06-22 pass deferred — and the deferral was honest (it lacked the rendered DOM). This run closed that gap by tracing the four leading `<h3>` to the cart-drawer empty-state `card-collection` render from source, so it is now safely authorable.
- **Human-owned, by proof, not assertion:** SYS-3 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts the theme repo can't touch), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-3/4 duplicate titles+descriptions, PERF-2/5 image re-exports, SYS-4 meaningful alt.
- **SYS-8** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected (not in the repo), and PERF-14's duplicated JS has no reliable Liquid cross-section dedup while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **ship every safe, source-grounded theme-code fix that remains — SYS-1 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-3 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-4 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-5 duplicate titles + descriptions** — collection renames + bespoke copy in admin → Jenna/Britni.
- **SYS-6 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

Every change is a self-contained snippet edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this repo at branch point. The grouping root is **SEO-1 / A11Y-3 (heading outline)**.

### Task A — SYS-1 · backward-compatible heading tag on `card-collection.liquid` (SEO-1 / A11Y-3)
- **The defect:** `card-collection.liquid` hardcodes `<h3 class="card__heading">` in all three of its title branches (`:111` always-on, `:134` card-style, `:189` placeholder). When a collection has a featured image, **both `:111` and `:134` render**, so each card emits **two `<h3>`** into the DOM. The cart drawer's empty-cart state renders this snippet twice (`cart-drawer.liquid:106,114`, the two `cart_drawer_collection*` settings) and the cart drawer is global (`layout/theme.liquid:482`) → **four `<h3>` on every page**, ahead of the page `<h1>` → "page's first heading is not `<h1>`" + skipped level, on all 185 pages. This is the root the prior pass couldn't pin blind, and it matches the `h3 h3 h3 h3 → h1` evidence on `/`, `/pages/sizing`, `/blogs/news` exactly.
- **The fix — backward-compatible heading-tag parameter (mirrors the proven card-product pattern):**
  - `snippets/card-collection.liquid` — add `assign card_heading_tag = card_heading_tag | default: 'h3'` in the head `liquid` block, and render the three `card__heading` open/close tags as `<{{ card_heading_tag }}>` / `</{{ card_heading_tag }}>`. Default `'h3'` → **the other three callers (`collage`, `collection-list`, `main-list-collections`) are byte-identical.**
  - `snippets/cart-drawer.liquid:106,114` — pass `card_heading_tag: 'div'` on both empty-cart `card-collection` renders, so the off-canvas promo cards leave the global document outline entirely.
- **Why it's safe to author for review:** the visible size/style is the `.card__heading` **class**, untouched; **all CSS targets `.card__heading` (and `.card__heading a`), never `h3.card__heading`** (verified in `component-card.css`), and **no JS references `card__heading`** (verified, `assets/*.js`). The promo card's accessible name is carried by its "SHOP {title}" link, not the heading, so dropping heading semantics in the drawer loses no name. The change is **purely semantic** — zero visual or behavioral change by construction.
- **Scope held deliberately tight:** only the **cart drawer** moves off `<h3>` this run (the proven global source of the four leading headings). The same parameter is now available to `collage`/`collection-list`/`main-list-collections`, but those keep the `h3` default — those are real in-page section headings and are correct as `<h3>` under their section `<h2>`; touching them is a separate, browser-verified call.
- **Closes (code side):** the global leading-`h3` share of SEO-1's 185/185 skipped-level count and the corresponding A11Y-3 HTML-structural warnings. The next baseline's skipped-level count is the test.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. Each change is authored to pass them:
- **Theme Check:** no new offenses — edits are a Liquid `assign`, three tag-name swaps via a variable, and one render parameter on two calls; no new Liquid risk, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **View-Source/axe shows the empty cart-drawer promo collections as `<div class="card__heading">` (size unchanged) and the document outline starting at the page `<h1>`** with no leading `<h3>` run. Confirm the drawer promo cards look identical and the "SHOP {title}" links still work. Re-run the SiteOne crawl and confirm skipped-level drops off 185.
- **Fork-safe:** self-contained snippet edits; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-1 heading outline (code)**
- [x] A1 · `card-collection.liquid` add `card_heading_tag` default `'h3'` + render the 3 `card__heading` elements from it (SEO-1 / A11Y-3)
- [x] A2 · `cart-drawer.liquid:106,114` pass `card_heading_tag: 'div'` on both empty-cart `card-collection` renders (SEO-1 / A11Y-3)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-22`, `git add -A`, commit, push
- [x] H2 · open ONE PR (cycle data + fix) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- SEO-1 heading structure — **185 of 185** pages flag a skipped heading level (flat across 06-20/06-21/06-22) and **1** page multiple-H1; golden Home flagged. The global leading-`h3` run (this PR's target) is the universal cause. Target: single H1 + ordered headings, all pages (BASELINE §E/§F).
- A11Y-3 sitewide a11y prevalence — **1,761 flagged elements across 185 pages** (1,756 HTML-structural, the heading-order family). Target: 0.
- Cycle deltas vs 2026-06-21 (`diff.md`): **0 field regressions**; a11y rules improved — heading-order 1→0, image-alt 4→0; sitewide multiple-H1 2→1; total findings 39→35.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the **next cycle's `diff.md`**; link it back to this PR to close the loop. The decisive signal will be **skipped-level moving off 185/185**. No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — `card-collection.liquid` gains a backward-compatible `card_heading_tag` (default `h3`, all existing callers unchanged); the global cart-drawer empty-cart promo cards render it as `div` so they stop injecting four `<h3>` ahead of every page's `<h1>`.

**Already merged (awaiting publish):** PR #16 — SYS-2 hero slide-link `strip_html`. Earlier PRs — slideshow/pagination labels, card-image alt fallback, card-product `h3→h2` + stray product `h1→h2`, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Deferred (named in §1, with owner):** SYS-3 Mailchimp (app/marketing), SYS-4 meaningful alt (content), SYS-5 duplicate titles+descriptions (content), SYS-6 image re-exports (content), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SYS-9 Permissions-Policy (platform).
