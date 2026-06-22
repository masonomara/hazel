# Execution — 2026-06-22

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Branch: `hobbes-fix-2026-06-22-image-alt` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s *unshipped* order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> Branch base + name. The 2026-06-22 baseline/findings live in the open cycle PR (#13, `hobbes-cycle-2026-06-22`), not yet merged to `main`. So this branch is cut from `origin/hobbes-cycle-2026-06-22` — so `plan.md` / `execution.md` sit alongside the inputs they cite and the PR shows the whole cycle. The literal name `hobbes-fix-2026-06-22` is already taken by the **merged** PR #12 (the 2026-06-21 cycle's budget-100 run, executed yesterday calendar-side); reusing a merged branch name collides on push, so this run uses the disambiguated, descriptive `hobbes-fix-2026-06-22-image-alt`.

## 1. Batch selection — effort budget B = 100 ("do everything")

`hobbes.toml` sets `effort_budget` to **100** — far above a full plan (~25 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/live work, filtered to **theme code Hobbes can author** (not content, not app-config, not platform, not a DOM question needing the rendered page) — because the run writes only to GitHub and cannot run a browser.

Walking `plan.md`'s order top-down, with current `main` state:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Image alt | 2 | ✅ **(code)** | JS-rendered card images (recently-viewed + cart upsell) have no `alt` — never touched by any prior PR. The top unshipped theme code. |
| 2 | SYS-3 · Theme a11y controls | 2 | ⚪ merged | slideshow/pagination labels shipped PR #8; live awaits publish |
| 3 | SYS-2 · Heading hierarchy | 3 | ⚪ merged / DOM / content | collection `h1→h3` + stray `h1` merged PR #12; homepage multi-h1 + leading-`h3` root + page-content `h1` are merchant settings / a browser-DOM question |
| 4 | SYS-4 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 5 | SYS-5 · Page metadata | 3 | ⛔ content | duplicate titles/descriptions are admin renames + bespoke copy; the code fallback is live |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority live; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-14 has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1 alone, and why that is "do everything," not under-delivery.** The template rightly warns against stopping out of caution — so this is reasoned, not timid. Ranks 2, 3 (code), 6 (code) and rank-9 code are **already merged into `main`** (PRs #8/#10/#11/#12); re-doing them is wasted motion, and they need only the human publish. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch) — and it is *new*, not a re-ship: the alt fallback PR #8 added covers the Liquid card (`card-product.liquid`), but the theme **also builds cards in JS template-literals** that PR #8 never reached. Those are this batch.
- **Human-owned, by proof, not assertion:** SYS-4 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts the theme repo can't touch), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-3/4 duplicate titles+descriptions, PERF-2/5 image re-exports, SEO-2 meaningful alt, and the homepage `heading_size: "h1"` settings in admin-generated `index.json`/`settings_data.json` (`DEVELOPMENT.md` forbids hand-editing them).
- **SYS-2 remainder is a DOM question, not blind-authorable code.** The merged PR #12 already took the clean, contained share (collection `h3→h2` + stray product `h1`). What's left — the homepage multiple-`h1` (three CSS-toggled header logo `<h1>` variants + merchant `heading_size`), the leading `h3 → h3 → h3 → h3 → h1` that opens the outline, and the `/pages/sizing` + `/pages/search-results` page-content `<h1>` misuse — each needs the **rendered DOM** to pin which element to change and to confirm no layout/visual regression. Authoring those blind, with no browser to verify, would violate the "evidence under your feet / no unverifiable regression" bar. Held for a browser-gated pass after PR #12 publishes.
- **SYS-8** has no slice that is both clean and safe to author blind (same reasoning as last cycle: FOUC risk on `base.css`, app-injected font/reflow, no reliable Liquid JS dedup, benign 4 KB).

So "do everything" resolves to: **ship every safe, source-grounded theme-code fix that remains — SYS-1's JS-image alt — and hand each non-code / DOM-gated remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 heading remainder** — homepage multiple-`h1` (merchant `heading_size` in `index.json`/`settings_data.json` → Jenna in the editor; header logo-`<h1>` variants → browser-confirmed markup pass), the leading-`h3`-before-`h1` outline root (browser-DOM diagnosis), and `/pages/sizing` + `/pages/search-results` page-content `<h1>` (content/template, confirm in browser). All gated on PR #12 publishing + a browser pass.
- **SYS-4 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-5 metadata** — SEO-3 4 duplicate titles (collection renames) + SEO-4 9 duplicate descriptions (bespoke copy) → Jenna/Britni. The templated fallback that now fills every page (and so surfaces `"Shop X at Hazel Boutique." ×2`, `"Hazel Boutique" ×5`) is working as designed; the duplicates clear when those collections get distinct titles/descriptions.
- **SYS-6 image content** — PERF-2/5 oversized + raw-HEIC re-exports to WebP/AVIF → Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.
- **Content meaningful alt (SEO-2)** — per-product admin image alt at scale → Jenna/Britni.

## 2. Implementation plan — against the real source

Every change is a self-contained section/snippet edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this branch at branch point. The grouping root is **A11Y-4 / SEO-2 (image alt on theme-rendered images)**.

### Task A — SYS-1 · alt on the "Recently viewed" JS-rendered images (A11Y-4, SEO-2, A11Y-5)
- **The defect:** `sections/footer.liquid` injects a "Recently viewed" product grid client-side, building each card as a JS template-literal. Its two `<img>` tags (`footer.liquid:140` primary, `:141` conditional second image) carry **no `alt`**. This block renders in the footer on every page; on a product page it is the **A11Y-4** node — its evidence (`<img src="…/IMG-1767.jpg?v=1711642495" loading="lazy" width="1200">`) matches this output exactly (the src is `{{ product.featured_image | image_url }}` with no size → the master filename; same `loading="lazy" width="1200"`).
- **The fix:** add `alt="${item.productTitle}"` to both `<img>`. `item.productTitle` is already populated from `'{{ product.title }}'` (footer.liquid:34) and stored per item in `localStorage` — so the alt is the product name, meaningful by construction. Double-quoted to tolerate apostrophes in titles (e.g. "Women's"); the existing `src='…'` single-quote style is left untouched.
- **Why it's safe to author for review:** purely additive (one attribute), no layout/CSS/behavior touched — the card heading already injects the same `${item.productTitle}` as text (footer.liquid:152) without issue. Zero visual change.
- **Heading note:** these cards render `<h3 class="card__heading h5">` (footer.liquid:150) directly under the section's `<h2>Recently viewed</h2>` (footer.liquid:100) → `h2 → h3` is a **correct** outline, not a skip. No heading change needed here.
- **Closes (code side):** the live **A11Y-4** image-alt node, and the recently-viewed share of **SEO-2** / **A11Y-5** unnamed-image coverage.

### Task B — SYS-1 · alt on the cart-drawer "Wear it with" upsell images (A11Y-5, SEO-2)
- **Where:** `snippets/cart-drawer.liquid:46` and `:97` — two `<img class="cartUpsell__image" src="${firstRecommendedProduct.images[0]}" />` in the JS that injects a recommended-product upsell into the cart drawer (one branch per recommendation source). Both `alt`-less.
- **Fix:** add `alt="${firstRecommendedProduct.title}"` to both. `firstRecommendedProduct.title` is already in scope (rendered as text at `:49/:100`), so the alt is the product name.
- **Why it's safe:** additive attribute only; the cart drawer is the live AJAX cart UI and its layout/behavior are untouched.
- **Closes (code side):** the cart-drawer share of **A11Y-5** unnamed-image + **SEO-2** coverage; hardens the drawer for screen-reader users.

### Explicitly not touched (and why)
- **`snippets/recent-viewed-product-js.liquid:135`** carries the same alt-less `<img>` pattern, but the entire file is wrapped in `{% comment %} … {% endcomment %}` (line 2 → 177) and flagged `theme-check-disable OrphanedSnippet` — it is **inert dead code**, renders nothing, and has zero a11y impact. Left untouched to keep the diff tight to live code; flagged here so a future edit doesn't resurrect the bad pattern.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. Each change is authored to pass them:
- **Theme Check:** no new offenses — the edits add one HTML attribute inside existing JS template-literals; no new Liquid, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **axe/Lighthouse shows the product page's "Recently viewed" images and the cart-drawer upsell image with a non-empty `alt`** equal to the product title. Confirm the recently-viewed grid and cart drawer look and behave identically (alt is invisible; nothing else changed).
- **Fork-safe:** self-contained section/snippet edits; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-1 image alt (code)**
- [x] A1 · `sections/footer.liquid:140–141` recently-viewed `<img>` ×2 → add `alt="${item.productTitle}"` (A11Y-4 / SEO-2 / A11Y-5)
- [x] B1 · `snippets/cart-drawer.liquid:46,97` cart-upsell `<img>` ×2 → add `alt="${firstRecommendedProduct.title}"` (SEO-2 / A11Y-5)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-fix-2026-06-22-image-alt` off the cycle branch, commit, push
- [x] H2 · open PR with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md`):**
- A11Y-4 image-alt — **1 node**, Product — desktop + mobile (the recently-viewed footer image). Target: 0 failing a11y audits.
- A11Y-5 sitewide — **1 missing image-alt warning + 1 unnamed link/button** among 1,761 flagged elements across 185 pages. Target: 0.
- SEO-2 image-alt coverage — golden pages failing (Home 19/43, Collection 45/88, Product 16/24 imgs missing alt); the JS-rendered recently-viewed + cart-upsell images are part of this count. Target: all images have alt (decorative hover images correctly excepted with `alt=""`).
- Golden a11y scores: Home 97 / Collection 96–97 / Product 92 (§A). Target: 100.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the next cycle's `diff.md`; link it back to this PR to close the loop. No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — the theme's two JS-rendered card paths (footer "Recently viewed", cart-drawer "Wear it with" upsell) now emit a meaningful `alt` (the product title) on their images — the alt gap PR #8's `card-product.liquid` fallback never reached.

**Already merged (awaiting publish):** PR #8 — SYS-3 slideshow/pagination labels, SYS-2 nested-heading, SYS-1 card-image alt fallback. PR #12 — SYS-2 collection card `h3→h2` + stray product `h1→h2`. (PRs #10/#11 — metadata, OG/Twitter, Referrer-Policy, hero-logo dims, LCP fetchpriority — are now **live**, confirmed by `diff.md`: meta-desc 76→0, SEO 92→100.)

**Deferred (named in §1, with owner):** SYS-2 heading remainder (homepage multi-h1 + leading-h3 root + page-content h1 → merchant settings + browser-DOM), SYS-4 Mailchimp (app/marketing), SYS-5 duplicate titles+descriptions (content), SYS-6 image re-exports (content), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SEO-2 meaningful alt at scale (content), SEC-1 Permissions-Policy (platform).
