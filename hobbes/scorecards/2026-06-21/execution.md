# Execution — 2026-06-21

Site: https://hazelboutique.com/ · Cycle: 2026-06-21 · Branch: `hobbes-fix-2026-06-22` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s *unshipped* order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> Why a fresh branch (`hobbes-fix-2026-06-22`): the cycle's first branch `hobbes-fix-2026-06-21` already shipped the budget-20 batch and is **merged** (PRs #10, #11). This is the budget-100 continuation of the same cycle, run the next calendar day, so it gets its own non-colliding branch.

## 1. Batch selection — effort budget B = 100 ("do everything")

`hobbes.toml` raised `effort_budget` to **100** — far above a full plan (~25 pts), i.e. *clear every system the run can legitimately clear*. The budget is therefore **not** the binding constraint. What bounds this run is what's left after the merged work, filtered to **theme code Hobbes can author** (not content, not app-config, not platform) — because the run writes only to GitHub.

Walking `plan.md`'s order top-down, with current `main` state:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Theme a11y controls | 2 | ⚪ merged | shipped PR #8; live awaits publish |
| 2 | SYS-2 · Heading hierarchy | 3 | ✅ **(code)** | card-grid h1→h3 skip + stray product h1 — the top unshipped theme code |
| 3 | SYS-4 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-3 · Image alt | 3 | ⚪ merged / content | card-image alt fallback merged; meaningful alt is content |
| 5 | SYS-5 · Page metadata | 3 | ⚪ merged / content | meta-desc + OG/Twitter code merged (PRs #10/#11); duplicate copy is content |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-13 has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-2 alone, and why that is "do everything," not under-delivery.** The template rightly warns against stopping out of caution — so this is reasoned, not timid. Ranks 1, 4, 5, 6 and rank-9 code are **already merged into `main`** (PRs #8/#10/#11); re-doing them is wasted motion, and they need only the human publish. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-2** (this batch).
- **Human-owned, by proof, not assertion:** SYS-4 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts the theme repo can't touch), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-5/6 duplicate titles+descriptions, PERF-2/5 image re-exports, SYS-3 meaningful alt, and the homepage `heading_size: "h1"` settings that live in admin-generated `templates/index.json` / `settings_data.json` (`DEVELOPMENT.md` forbids hand-editing them).
- **SYS-8** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected (not in the repo), and PERF-13's duplicated JS has no reliable Liquid cross-section dedup (sections don't share state; a layout-level include would regress onto card-less pages) while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **ship every safe, source-grounded theme-code fix that remains — SYS-2 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 homepage multiple-h1** — rooted in per-section `heading_size: "h1"` choices in admin-generated `index.json`/`settings_data.json`, plus the header's CSS-toggled logo-`<h1>` variants (a DOM question). → Jenna in the theme editor for the heading sizes; a browser-confirmed header-markup pass for the logo variants.
- **SYS-4 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **Content** — SEO-5/6 duplicate titles+descriptions, PERF-2/5 oversized/HEIC re-exports, SYS-3 meaningful alt at scale → Jenna/Britni.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

Every change is a self-contained snippet/section edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this repo at branch point. The grouping root for all of these is **SEO-2 / A11Y-3 (heading outline)**.

### Task A — SYS-2 · card-grid heading level on collection pages (SEO-2)
- **The defect:** a populated collection renders `<h1>` (`main-collection-banner.liquid:15`) → product cards `<h3>` (`card-product.liquid`), with **no `<h2>` between** — the grid's only `<h2>` renders solely on an *empty* collection (`main-collection-product-grid.liquid:104`). That h1→h3 skip repeats on ~76+ collection pages and is the bulk of SEO-2's 185-page count.
- **The fix — backward-compatible heading-tag parameter:**
  - `snippets/card-product.liquid` — add `{%- liquid assign card_heading_tag = card_heading_tag | default: 'h3' -%}` and render the three `card__heading` elements as `<{{ card_heading_tag }}>` / `</{{ card_heading_tag }}>` (the two product blocks + the placeholder). Default `'h3'` → **all 8 other render sites are unchanged**.
  - `sections/main-collection-product-grid.liquid:137` — pass `card_heading_tag: 'h2'` so collection cards sit as `<h2>` under the page `<h1>`.
- **Why it's safe to author for review:** the visible size is the `h5`/`h4` **class**, which is untouched, and **all CSS targets `.card__heading` (class), never the `h3` tag; no JS references it** (verified via `assets/component-card.css` + JS grep). The `id="title-…"` and `aria-labelledby` stay on the heading element. So the change is **purely semantic** — zero visual or behavioral change by construction. Multiple `<h2>` siblings under one `<h1>` is valid and is the correct outline.
- **Scope held deliberately tight:** only the collection grid moves to `h2` this run (the proven dominant case). The same parameter is now available to `main-search`, `collage`, `featured-product` and other grids, but those keep the `h3` default — extend them in a follow-up once this approach is browser-verified, so the blast radius stays bounded.
- **Closes (code side):** the collection-page share of SEO-2's skipped-level count, and the related A11Y-3 heading-order on the collection golden path.

### Task B — SYS-2 · stray non-title `<h1>` on the product page (SEO-2)
- **Where:** `sections/main-product.liquid:689` — a product-page "page content" popup block titled `<h1 class="h2">{{ block.settings.page.title }}</h1>`. A second `<h1>` that is not the product title is wrong by semantics.
- **Fix:** `<h1 class="h2">` → `<h2 class="h2">`. The `h2` class is unchanged, so appearance is identical; only the element tag changes.
- **Closes (code side):** the product-page multiple-h1 contribution to SEO-2 wherever a page block is used.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. Each change is authored to pass them:
- **Theme Check:** no new offenses — edits are a Liquid `assign`, tag-name swaps via a variable, and one render parameter; no new Liquid risk, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **View-Source/axe shows collection product-card titles as `<h2>` (size unchanged) and the product page with a single `<h1>`**. Confirm cards look identical (size driven by the unchanged `h5` class) and quick-add still works (the `title-…` id / `aria-labelledby` are preserved).
- **Fork-safe:** self-contained snippet/section edits; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-2 heading hierarchy (code)**
- [x] A1 · `card-product.liquid` add `card_heading_tag` default `'h3'` + render the 3 `card__heading` elements from it (SEO-2 / A11Y-3)
- [x] A2 · `main-collection-product-grid.liquid` pass `card_heading_tag: 'h2'` on the grid render (SEO-2)
- [x] B1 · `main-product.liquid:689` stray `<h1 class="h2">` → `<h2 class="h2">` (SEO-2)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-fix-2026-06-22`, commit, push
- [x] H2 · open PR with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md`):**
- SEO-2 heading structure — **185 of 185** pages flag a skipped heading level; **2** pages multiple-h1; golden Home flagged. The collection-grid h1→h3 skip (this PR's target) is the dominant share (~76+ collection pages). Target: single H1 + ordered headings, all pages.
- A11Y-3 heading-order — 1 node, Collection — mobile. Target: 0 failing a11y audits.
- Golden SEO scores: 92 across all six page/device runs (§A). Target: ≥ 95.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the next cycle's `diff.md`; link it back to this PR to close the loop. No after is fabricated here.

**Shipped this PR (theme code):** SYS-2 — collection product-card headings move `h3 → h2` under the page `h1` (backward-compatible parameter, size class unchanged), and the stray product-page popup `h1 → h2`.

**Already merged (awaiting publish):** PR #8 — SYS-1 slideshow/pagination labels, SYS-2 nested-heading, SYS-3 card-image alt fallback. PRs #10/#11 — SYS-5 meta-description + OG/Twitter, SYS-6 hero-logo dims + LCP fetchpriority, SYS-9 Referrer-Policy.

**Deferred (named in §1, with owner):** SYS-2 homepage multi-h1 (merchant `heading_size` settings + header DOM), SYS-4 Mailchimp (app/marketing), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SEO-5/6 duplicate copy + image re-exports + meaningful alt (content), SEC-1 Permissions-Policy (platform).
