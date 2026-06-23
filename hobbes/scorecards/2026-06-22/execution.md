# Execution — 2026-06-22 (re-measured)

Site: https://hazelboutique.com/ · Cycle: 2026-06-22 · Branch: `hobbes-cycle-2026-06-22` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s *unshipped, safely-authorable* order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This run carries the **re-measured 2026-06-22 cycle data** (baseline/findings/diff/digests, 35 findings) **plus** the one theme-code fix that data justifies — the re-diagnosed hero slideshow naming (SYS-1) — in **one branch and one PR**, `hobbes-cycle-2026-06-22`, so the scorecard and the fix it justifies travel together. The re-measurement is what makes this run honest: it **validated** the prior heading fix (skipped-level **185 → 2**, already in `main`) and **refuted** the prior hero `strip_html` attempt (A11Y-1 held at 3 nodes — `strip_html` is a no-op on the markup-free flagged headings). SYS-1 is the corrected fix.

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~22 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author safely without a browser** (not content, not app-config, not platform) — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Hero slideshow naming | 1 | ✅ **(code)** | the only unshipped, safely-authorable theme code; re-diagnosed (visible counter, not markup) — drop the conflicting aria-label + un-hide the counter to match the passing desktop block |
| 2 | SYS-2 · Heading outline (last 2 pages) | 2 | ⛔ content | cascade validated (185→2); the 2 remainders live in admin `{{ page.content }}` bodies |
| 3 | SYS-3 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-4 · Image alt | 4 | ⚪ merged / content | card-image alt fallback merged (axe 4→0); meaningful alt is content; theme sweep clean |
| 5 | SYS-5 · Page metadata (dup copy) | 3 | ⛔ content | duplicate titles/descriptions = admin renames + bespoke copy |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-15 has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1 alone, and why that is "do everything safe," not under-delivery.** The structural cascade (the prior cart-drawer `card_heading_tag` heading fix) is **already in `main`** and the re-crawl proves it worked (185→2); re-doing it is wasted motion. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch). This is the hero label fix the previous attempt got *directionally right but mechanically wrong* — it changed the aria-label's filter, but the flagged nodes have no HTML, so it couldn't move. This run fixes the actual cause from source.
- **Human-owned, by proof, not assertion:** SYS-2 (two admin page bodies — the theme repo can't reach `{{ page.content }}`), SYS-3 (Mailchimp embed/app config), SYS-7 (per-app business decisions + app-injected scripts), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-3/4 duplicate titles+descriptions, PERF-2/4 image re-exports, SYS-4 meaningful alt.
- **SYS-8** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected, and PERF-15's duplicated JS has no reliable Liquid cross-section dedup while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **ship the one safe, source-grounded theme-code fix that remains — SYS-1 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 heading outline (2 pages)** — demote the size-chart h3s on /pages/sizing and the stray h1 on /pages/search-results, both in the admin page body → Jenna/Britni.
- **SYS-3 Mailchimp popup** — Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna.
- **SYS-4 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-5 duplicate titles + descriptions** — collection renames + bespoke copy in admin → Jenna/Britni.
- **SYS-6 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

The change is a self-contained section edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this repo at branch point.

### Task A — SYS-1 · hero mobile slide-link naming (A11Y-1)
- **The defect:** `sections/hero.liquid`, the `mobile-hero` block. The slide `<a>` (was line 56) carried `aria-label="{{ block.settings.heading | strip_html | default: 'View slide' | escape }}"`, while its visible content is `<span class="rteMidge" aria-hidden="true">0N</span>` (the slide counter, **visually shown**) plus `{{ block.settings.heading }}`. `label-content-name-mismatch` fires because the visually-rendered counter is not part of the aria-label: slide 1 visible "01 Shop HZL NEW" vs label "Shop HZL NEW"; blank-heading slides visible "02"/"03" vs label "View slide". The previous pass's `strip_html` only affects headings that contain HTML — the three flagged headings don't — so the re-crawl held at 3 nodes. The **desktop** hero block renders the same link with **no aria-label** and a **non-hidden** counter, and does not flag.
- **The fix (mirror the passing desktop block), two attribute removals:**
  - Remove the `aria-label="…"` line from the mobile slide `<a>` → the accessible name now derives from the link's content (the counter + heading), so it equals the visible text by construction.
  - Remove `aria-hidden="true"` from `<span class="rteMidge">` (the counter) → the content-derived name includes the counter (matching the visible text) **and** blank-heading slides keep a non-empty name ("02"/"03"), so no new `link-name` violation is introduced.
- **Why it's safe to author for review:** `label-content-name-mismatch` only evaluates elements whose name comes from `aria-label`/`aria-labelledby`; with the aria-label gone, the rule no longer applies to the link, and the name=content=visible-text invariant holds regardless of whether a heading is plain or rich text. `.rteMidge`/`.textyText` are styled by **class** (`base.css:5049/5054`, `component-hero.css`), and **no JS references the slide link's `aria-label` or `slideshow__slide`** (verified) — so removing two ARIA attributes is **purely semantic**: zero visual or behavioral change, an exact match to the desktop sibling that already passes axe.
- **Scope / sweep:** the `label-content-name-mismatch` pattern across the theme is the hero slide links (this fix); the desktop hero already follows the passing pattern, and the pagination labels were addressed in an earlier PR. No other in-theme control pairs an `aria-label` with conflicting visible text.
- **Closes (code side):** A11Y-1's 3 golden-path nodes (Home — mobile). The next baseline's A11Y-1 node count is the test.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. The change is authored to pass them:
- **Theme Check:** no new offenses — the edit removes two ARIA attributes from one section; no new Liquid, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **axe shows 0 `label-content-name-mismatch` on Home — mobile and 0 new `link-name` violations** (confirm the blank-heading slides are named by their counter). Confirm the hero slides look and behave identically (the counter `01/02/03` is still visible and styled, only its `aria-hidden` is gone) and the slide links still navigate.
- **Fork-safe:** self-contained section edit; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-1 hero slideshow naming (code)**
- [x] A1 · `sections/hero.liquid` mobile slide `<a>` — remove the conflicting `aria-label` so the name derives from content (A11Y-1)
- [x] A2 · `sections/hero.liquid` mobile counter `<span class="rteMidge">` — remove `aria-hidden="true"` so name = visible text and blank-heading slides stay named (A11Y-1)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-22`, `git add -A` (cycle data + plan/execution + hero fix), commit, push
- [x] H2 · open ONE PR (cycle data + fix) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- A11Y-1 `label-content-name-mismatch` — **3 nodes, Home — mobile** (the hero slide links); held flat across the prior `strip_html` attempt. Target: 0 failing a11y audits (BASELINE §D).
- A11Y-3 sitewide a11y prevalence — **1,761 flagged elements across 185 pages** (1,756 HTML-structural, the heading-order family). Target: 0.
- Cycle deltas vs 2026-06-21 (`diff.md`): **0 field regressions**; a11y rules improved — **heading-order 1→0, image-alt 4→0**; sitewide **skipped heading levels 185 → 2** (the prior heading fix, validated), multiple-H1 2→1; total findings 39→35.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the **next cycle's `diff.md`**; link it back to this PR to close the loop. The decisive signal will be **A11Y-1 dropping off 3 nodes** (as skipped-level 185→2 confirmed the previous cycle's fix). No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — `sections/hero.liquid` mobile slide links drop the conflicting `aria-label` and un-hide the slide counter, so the accessible name derives from content and equals the visible text — matching the desktop hero block that already passes axe. Purely semantic; zero visual change.

**Already merged (awaiting publish):** the cart-drawer `card_heading_tag` heading fix (validated this cycle: skipped-level 185→2). Earlier PRs — slideshow/pagination labels, card-image alt fallback, card-product `h3→h2` + stray product `h1→h2`, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Deferred (named in §1, with owner):** SYS-2 heading outline (2 admin page bodies — content), SYS-3 Mailchimp (app/marketing), SYS-4 meaningful alt (content), SYS-5 duplicate titles+descriptions (content), SYS-6 image re-exports (content), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SYS-9 Permissions-Policy (platform).
