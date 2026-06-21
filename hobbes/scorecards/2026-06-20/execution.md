# Execution — 2026-06-20

Site: https://hazelboutique.com/ · Cycle: 2026-06-20 · Branch: `hobbes-fix-2026-06-20` · Driven by Hobbes from `plan.md`. Authored 2026-06-21.

This run takes the top of `plan.md`'s order, selects the batch the effort budget allows, writes the code-level implementation against the **real codebase**, implements it, and stops at a pushed branch + open PR for human review. It does **not** run the Shopify CLI, Theme Check, or any publish — verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review (per the run's hard rules and `DEVELOPMENT.md`).

## 1. Batch selection — effort budget B = 6

Walking `plan.md`'s order top-down, summing effort, drawing the line where the budget runs out:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-2 · Heading hierarchy & structure | 2 | ✅ (code half) | nested-heading snippet fix, sitewide cascade |
| 2 | SYS-1 · Theme a11y controls | 2 | ✅ (full) | two pinned label-mismatch bugs, pure theme code |
| 3 | SYS-4 · Mailchimp popup a11y | 2 | ⛔ deferred | **entirely human-owned** — app-config / marketing decision, no theme code to ship |
| 4 | SYS-3 · Image alt text | 3 | ✅ (code half) | featured-image alt fallback (~2) fits remainder; meaningful alt is content |

**Budget math:** SYS-2 (2) + SYS-1 (2) = 4. SYS-4 (rank 3) carries **no theme-code work** this run — it is app-config or a marketing call, so it is deferred whole, not counted. SYS-3 is pulled up: its shippable code portion (the alt fallback, ~2) fits the remaining budget and stands cleanly on its own; its content half (meaningful alt at scale) is the template's explicitly-allowed human deferral. **Code effort spent ≈ 6.**

**Batch = SYS-2 + SYS-1 + SYS-3 (code).** Three theme-code systems, the entire accessibility front of the queue (mission priority 1) plus the SEO structural cascade — one PR, no content or app dependency, shippable without waiting on anyone.

**Deferred this cycle (named, not silent):**
- **SYS-4 Mailchimp popup** — human-owned (Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna).
- **SYS-3 meaningful alt at scale** — per-image admin content → Jenna/Britni. The code fallback ships now; the quality pass is ongoing content.
- **SYS-2 deeper outline work** — the duplicate header-logo h1 on non-home pages and section-level h2s (full SEO-2 clearance) touch shared Dawn layout; held for a dedicated PR with its own verification.
- **Ranks 5–9** (page metadata, image delivery, app JS, theme CSS, security headers) — next cycles.

## 2. Implementation plan — against the real source

Every change is a self-contained snippet/section edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this repo at branch point.

### Task A — SYS-2 · kill the nested heading-in-heading (A11Y-3, A11Y-5, SEO-2 partial)
- **Where:** `snippets/card-product.liquid:130–135`.
- **Now:** `<h3 class="card__heading"><h3 class="full-unstyled-link">{{ title }}</h3></h3>` — a heading nested inside a heading, emitted on every product card on every grid page (185 pages). This is the concrete cause of A11Y-3 (heading-order) and the bulk of A11Y-5's 1,746 "HTML structural" warnings.
- **Fix:** change the inner `<h3 class="full-unstyled-link">` to `<span class="full-unstyled-link">`, matching the file's own correct variant at `:189–203` (`<h3>` → `<span class="full-unstyled-link">`). The whole card is already an anchor (`:39 <a class="card-wrapper" href>`), so the title needs no link of its own; the `full-unstyled-link` class is preserved so styling is unchanged.
- **Closes:** A11Y-3; the bulk of A11Y-5 (card-multiplied structural warnings). **Does not** clear SEO-2's header-logo duplicate-h1 or section-h2 skips — deferred (see §1).

### Task B — SYS-1 · hero slideshow label mismatch (A11Y-1)
- **Where:** `sections/hero.liquid:59` (mobile-hero slide link `aria-label`) and `:104` (visible counter span).
- **Now:** `aria-label="Go to {{ block.settings.heading }}"` → renders "Go to " (empty) when a slide has no heading, and where a heading exists the name ("Go to Shop HZL NEW") omits the visible "00N" counter the link shows → `label-content-name-mismatch`.
- **Fix:** set `aria-label="{{ block.settings.heading | default: 'View slide' | escape }}"` (drops the "Go to" prefix and the empty-label bug, adds a fallback name), and mark the decorative counter span `aria-hidden="true"` so the visible label text equals the heading and is contained in the accessible name.
- **Closes:** A11Y-1 (slideshow nodes, Home-mobile).

### Task C — SYS-1 · pagination label mismatch (A11Y-1)
- **Where:** `snippets/pagination.liquid:38–56` (link + current-page variants).
- **Now:** visible page number is zero-padded — `{{ part.title | prepend: '0' | slice: -2, 2 }}` → "08" — but `aria-label` is `'general.pagination.page' | t: number: part.title` → "Page 8" (locale string confirmed `"Page {{ number }}"`). "08" ⊄ "Page 8" → `label-content-name-mismatch` on every paginated collection.
- **Fix:** compute the padded label once (`assign page_label = part.title | prepend: '0' | slice: -2, 2`) and feed it to **both** the `aria-label` (`number: page_label` → "Page 08") and the visible text. "08" ⊂ "Page 08" → match.
- **Closes:** A11Y-1 (pagination nodes, Collection desktop + mobile).

### Task D — SYS-3 · product-card image alt fallback (A11Y-4 partial, SEO-3 partial)
- **Where:** `snippets/card-product.liquid:89` (featured-media `<img>`).
- **Now:** `alt="{{ card_product.featured_media.alt | escape }}"` — ships `alt=""` whenever the admin alt is blank.
- **Fix:** `alt="{{ card_product.featured_media.alt | default: card_product.title | escape }}"` — falls back to the product title so every card image has a meaningful name. The decorative hover image (`:112`, `alt=""`) is left as-is by design — empty alt is correct for a duplicate, and chasing SEO-3's coverage count to zero would announce every product twice.
- **Closes:** the blank-alt half of SEO-3 on card grids. **Open/verify:** A11Y-4's single missing-alt node is a bare `<img>` (no srcset/sizes/class) that does **not** match card-product's output — likely app- or custom-injected; its source must be identified in the browser at review, not assumed fixed.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. Each change is authored to pass them:
- **Theme Check:** no new offenses — edits are markup-attribute and tag-name changes in self-contained snippets; no new Liquid constructs, no `settings_data.json`. Bar is "no *new* offenses vs base," not zero (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors — card titles still render and link, slideshow + pagination still navigate, card images still display.
- **Fork-safe:** self-contained snippet/section edits, no Dawn-core restyle.
- **No baseline regression** against `baseline.md` targets.

## 4. Todo

**Phase 1 — SYS-2 (Task A)**
- [x] A1 · `card-product.liquid:130–135` inner `<h3 class="full-unstyled-link">` → `<span>` (closes A11Y-3, bulk of A11Y-5)

**Phase 2 — SYS-1 (Tasks B, C)**
- [x] B1 · `hero.liquid:59` aria-label → heading-with-fallback, drop "Go to" (A11Y-1 slideshow)
- [x] B2 · `hero.liquid:104` counter span `aria-hidden="true"` (A11Y-1 slideshow)
- [x] C1 · `pagination.liquid` assign padded `page_label`, use in aria-label + visible text, both variants (A11Y-1 pagination)

**Phase 3 — SYS-3 (Task D)**
- [x] D1 · `card-product.liquid:89` alt fallback to `card_product.title` (SEO-3 / A11Y-4 code half)

**Phase 4 — handoff**
- [x] H1 · branch `hobbes-fix-2026-06-20`, commit, push
- [x] H2 · open PR with before/after + deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured state, from `baseline.md` / `findings.md`):**
- A11Y-1 `label-content-name-mismatch` — 4 nodes across Home-mobile + Collection desktop/mobile (baseline §D). Target: 0.
- A11Y-3 `heading-order` — 1 node, Collection-mobile. Target: 0.
- A11Y-5 sitewide structural — 1,746 "HTML structural" warnings across 185 pages. Target: 0.
- A11Y-4 `image-alt` — 1 missing-alt node, Product. Target: 0.
- SEO-3 image-alt coverage — Home 20/45, Collection 44/88, Product 16/25 imgs missing alt. Target: all images have alt.
- Golden a11y scores: Home-mobile 97, Collection-mobile 96, Product 92 (§A).

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the next cycle's `diff.md`; link it back to this PR to close the loop. No after is fabricated here.

**Shipped / human-owned:** SYS-2 nested-heading fix, SYS-1 slideshow + pagination label fixes, SYS-3 card-image alt fallback — all theme code. Deferred (named in §1): SYS-4 Mailchimp (human), SYS-3 meaningful alt at scale (content), SYS-2 header-logo h1 / section h2 (dedicated PR), ranks 5–9.
