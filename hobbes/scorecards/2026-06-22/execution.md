# Execution — 2026-06-22

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Branch: `hobbes-cycle-2026-06-22` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s *unshipped, safely-authorable* order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> Branch. This run carries **both** the cycle data (baseline/findings/diff/digests + this plan + this execution) and the fix in **one branch and one PR** — `hobbes-cycle-2026-06-22` — so the scorecard and the fix it justifies travel together and review sees the whole cycle in context.

## 1. Batch selection — effort budget B = 100 ("do everything")

The run's budget is **100** — far above a full plan (~25 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author safely without a browser** (not content, not app-config, not platform, not a rendered-DOM question) — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Hero slide-link a11y name | 1 | ✅ **(code)** | `hero.liquid:59` mobile slide `aria-label` still built with `\| escape` on an `inline_richtext` heading → `label-content-name-mismatch`. Verified live in source; touched by no current `main` code. The top unshipped, safe theme code. |
| 2 | SYS-3 · Heading hierarchy | 3 | ⛔ DOM / merchant / content | homepage multi-h1 = merchant `heading_size` in admin JSON + 3 CSS-toggled header logo `<h1>`s; leading-`h3` root + page-content `<h1>` need the rendered DOM |
| 3 | SYS-4 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-5 · Page metadata | 3 | ⛔ content | duplicate titles/descriptions are admin renames + bespoke copy; the code fallback is live |
| 5 | SYS-6 · Image delivery | 3 | ⚪ merged / content / DOM | LCP `fetchpriority` in `main`; HEIC/oversized re-exports are content; PERF-13 unsized-image is browser-gated |
| 6 | SYS-2 · Meaningful alt at scale | 5 | ⚪ merged / content | card + footer + cart-drawer alt code in `main`; residual is per-product admin alt |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ no clean+safe blind code | base.css deferral = FOUC risk; RM Neue/reflow/minify app-injected; PERF-14 has no clean Liquid dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy `<meta>` in `main`; Permissions-Policy is platform/edge-bound |
| 10 | SYS-10 · SVG/image-format BP | 2 | ⛔ cosmetic / Dawn-core | "0 critical" warnings; broad Dawn-core change, poor return |

**Why the batch is SYS-1 alone, and why that is "do everything," not under-delivery.** The template rightly warns against stopping out of caution — so this is reasoned, not timid, and it is grounded in reading the actual source, not a PR ledger:

- **The image-alt, metadata, OG/Twitter, Referrer-Policy-meta and hero-fetchpriority work is already in `main`.** I confirmed each in the files (`card-product.liquid:93`, `footer.liquid:140–141`, `cart-drawer.liquid:35`, `theme.liquid:8,27–47`, `meta-tags.liquid`, `hero.liquid:98,182`). The crawl/PSI still list them because they measure the **live** site, which lags `main` until a human publishes. Re-shipping them would be wasted motion; the diff already shows the metadata slice landed live (meta-desc 76→0, SEO 92→100).
- **The genuinely remaining safe theme code is SYS-1** — and it is *new*. A prior pass treated the hero slide-link mismatch as already merged; the live source proves otherwise (`hero.liquid:59` still uses `| escape`). That is this batch.
- **Everything else is human-owned by proof, not assertion:** SYS-4 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts the repo can't touch), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), SYS-10 (cosmetic Dawn/CDN flags), and the **content** layer — SEO-3/4 duplicate titles+descriptions, PERF-2 image re-exports, SEO-2 meaningful alt, and the homepage `heading_size: "h1"` settings in admin-generated JSON (`DEVELOPMENT.md` forbids hand-editing them).
- **SYS-3 remainder and PERF-13 are rendered-DOM questions, not blind-authorable code.** The homepage multiple-`h1` (three CSS-toggled header logo `<h1>` variants + merchant `heading_size`), the leading `h3 → h3 → h3 → h3 → h1` that opens the outline, the `/pages/sizing` + `/pages/search-results` page-content `<h1>` misuse, and the PERF-13 unsized-image instance each need the **rendered DOM** to pin which element to change and to confirm no layout/visual regression. Authoring those blind, with no browser to verify, would violate the "evidence under your feet / no unverifiable regression" bar.
- **SYS-8** has no slice that is both clean and safe to author blind: FOUC risk on `base.css`, app-injected font/reflow/minify, no reliable Liquid JS dedup, benign 4 KB.

So "do everything" resolves to: **ship every safe, source-grounded theme-code fix that remains — SYS-1's hero slide-link name — and hand each non-code / DOM-gated remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-3 heading remainder** — homepage multiple-`h1` (merchant `heading_size` in admin JSON → Jenna in the editor; header logo-`<h1>` variants → browser-confirmed markup pass), the leading-`h3`-before-`h1` outline root (browser-DOM diagnosis), and `/pages/sizing` + `/pages/search-results` page-content `<h1>` (content/template, confirm in browser).
- **SYS-4 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-5 metadata** — SEO-3 4 duplicate titles (collection renames) + SEO-4 9 duplicate descriptions (bespoke copy) → Jenna/Britni. The templated fallback that now fills every page (and so surfaces `"Shop X at Hazel Boutique." ×2`, `"Hazel Boutique" ×5`) is working as designed.
- **SYS-6 image content + PERF-13** — PERF-2 oversized + raw-HEIC re-exports to WebP/AVIF → Jenna; PERF-13 unsized-image instance → browser-localise.
- **SYS-2 meaningful alt (SEO-2)** — per-product admin image alt at scale → Jenna/Britni.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.
- **SYS-10 inline-SVG / WebP-AVIF** — cosmetic; broad Dawn-core change, deferred.

## 2. Implementation plan — against the real source

One change, self-contained, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this branch.

### Task A — SYS-1 · hero mobile slide-link accessible name (A11Y-1)
- **The defect:** `sections/hero.liquid:59` — the mobile hero slide `<a>` sets `aria-label="{{ block.settings.heading | default: 'View slide' | escape }}"`. `block.settings.heading` is an `inline_richtext` field (schema line 357). When the merchant's heading contains any markup, `escape` emits the tag characters as literal text into the accessible name (e.g. `Shop &lt;strong&gt;HZL&lt;/strong&gt; NEW`), while the **visible** text in `.textyText` (line 106) renders tag-free (`Shop HZL NEW`). axe `label-content-name-mismatch` fires because the accessible name no longer contains the visible text — three slides, three nodes, matching A11Y-1 on Home — mobile. The desktop hero link (lines 124–138) has **no** `aria-label`, which is why only mobile fires (baseline §D).
- **The fix:** insert `strip_html` before `default`/`escape`:
  `aria-label="{{ block.settings.heading | strip_html | default: 'View slide' | escape }}"`.
  This makes the accessible name the **plain-text reading of the heading** — exactly the text the user sees — so the name contains the visible text and the mismatch resolves. `default` still supplies `View slide` for an empty heading; `escape` still keeps the attribute value safe.
- **Why it's safe to author for review:** for a plain-text heading the rendered `aria-label` is byte-identical to today's, so there is **zero change** on those slides; for a markup heading it only strips tags out of the *invisible* accessible name — no visible text, layout, CSS, or behavior is touched, and it cannot regress. The `<img>` in the same block (line 96) carries `aria-labelledby="SlideDescription-N"`, so its name is unaffected by this change.
- **Verification boundary (honest):** the change provably aligns the accessible name with the visible text — the exact comparison axe's rule makes — but Hobbes cannot run axe in a browser here. **Confirming the rule clears (0 `label-content-name-mismatch` nodes on Home — mobile) is the human's browser gate at review.** If the live failure has a second, content-shaped cause (e.g. a heading whose plain text still differs from the visible string), that surfaces at the gate and is a content fix, not a code one.
- **Closes (code side):** the live **A11Y-1** label-content-name-mismatch nodes on the mobile hero.

### Explicitly not touched (and why)
- **Desktop hero link** (`hero.liquid:124–138`) — no `aria-label`, does not fire A11Y-1; left alone.
- **`snippets/recent-viewed-product-js.liquid:135`** — carries an alt-less `<img>` but the entire file is wrapped in `{% comment %} … {% endcomment %}` (line 2 → 177) and flagged `theme-check-disable OrphanedSnippet`; it is **inert dead code**, renders nothing, has zero a11y impact. Left untouched to keep the diff tight; flagged so a future edit doesn't resurrect the pattern.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. The change is authored to pass them:
- **Theme Check:** no new offenses — the edit adds one Liquid filter inside an existing attribute; no new tags, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **axe/Lighthouse shows 0 `label-content-name-mismatch` on the Home mobile hero**, with each slide link's accessible name equal to its visible heading. Confirm the hero looks and behaves identically (the aria-label is invisible; nothing else changed).
- **Fork-safe:** one self-contained section edit; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-1 hero slide-link a11y name (code)**
- [x] A1 · `sections/hero.liquid:59` mobile slide `aria-label` → add `strip_html` so the accessible name matches the visible heading text (A11Y-1)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-22`, `git add -A` (cycle data + plan + execution + fix), commit, push
- [x] H2 · open PR with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md`):**
- A11Y-1 `label-content-name-mismatch` — **3 nodes, 1 run**, Home — mobile (the mobile hero slide links). Target: 0 failing a11y audits.
- Golden a11y scores: Home 97 / Collection 97 / Product 97 (§A). Target: 100.
- Golden axe trend (diff vs 2026-06-21): heading-order 1→0, image-alt 4→0 — **0 regressions**, 2 rules improved.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the next cycle's `diff.md`; link it back to this PR to close the loop. No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — the mobile hero slide links now derive their `aria-label` from the **plain text** of the heading (`strip_html`), so the accessible name matches the visible text and the `label-content-name-mismatch` mechanism is removed.

**Already in `main` (awaiting publish), verified in source:** card-image alt fallback (`card-product.liquid:93`), footer "Recently viewed" + cart-drawer upsell image alt (`footer.liquid:140–141`, `cart-drawer.liquid:35`), meta-description fallback chain + OG/Twitter + Referrer-Policy meta (`theme.liquid:8,27–47`, `meta-tags.liquid`), hero LCP `fetchpriority` (`hero.liquid:98,182`). The metadata slice is confirmed **live** by `diff.md` (meta-desc 76→0, SEO 92→100).

**Deferred (named in §1, with owner):** SYS-3 heading remainder (merchant settings + browser-DOM), SYS-4 Mailchimp (app/marketing), SYS-5 duplicate titles+descriptions (content), SYS-6 image re-exports (content) + PERF-13 (browser-localise), SYS-2 meaningful alt at scale (content), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SYS-9 Permissions-Policy (platform), SYS-10 SVG/format BP (cosmetic).
