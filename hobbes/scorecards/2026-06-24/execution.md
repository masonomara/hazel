# Execution — 2026-06-24

Site: https://hazelboutique.com/ · Cycle: 2026-06-24 · Branch: `hobbes-cycle-2026-06-24` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This run carries the **2026-06-24 cycle data** (baseline/findings/diff/digests, 31 findings) **plus** the one theme-code fix that data justifies — naming the runtime-injected `isp_*` search-app controls (SYS-1, A11Y-1 slivers) — in **one branch and one PR**, `hobbes-cycle-2026-06-24`, so the scorecard and the fix travel together. The re-measurement is what makes this honest: it **validated** last cycle's frame-title shim (`frame-title` 6 → 0, now live), which leaves the golden-path axe **clean** (§D 0 failing audits, Lighthouse a11y 100 everywhere). The only failing a11y signal left is the **sitewide crawl** (§F), and SYS-1 is the contained theme-side fix for the part of it the theme can author correctly.

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~16 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author without a browser** — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Search-app accessibility | 1 | ✅ **(code)** | the only unshipped, theme-authorable lever; a contained additive shim names the runtime-injected `isp_*` search box + decorative watermark — clears the §F crawl a11y rows the mission counts |
| 2 | SYS-2 · Heading outline & aggregate | 2 | ⛔ content/app | cascade validated (185→2); the 1 remaining error page is admin `{{ page.content }}` + `isp_*` search-app markup |
| 3 | SYS-3 · Image alt at scale | 4 | ⚪ merged / content | card-image alt fallback merged (axe image-alt 4→0); meaningful alt is content; theme sweep clean |
| 4 | SYS-4 · Page metadata | 2 | ⛔ content | dup titles fixed; 5 dup descriptions = bespoke admin copy |
| 5 | SYS-5 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content; blind fetchpriority is browser-gated |
| 6 | SYS-6 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 7 | SYS-7 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue app-injected; PERF-14 has no clean Liquid cross-section dedup and is benign |
| 8 | SYS-8 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1 alone, and why that is "do everything safe," not under-delivery.** The structural heading cascade and the last two cycles' axe fixes (hero `label-content-name-mismatch` 3→0, Mailchimp `frame-title` 6→0) are **already in `main`** and the re-crawl proves they worked; re-doing any is wasted motion. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch). The search-app controls are runtime-injected, so the clean fix is the app config — but a small, additive shim names the two controls whose correct names are unambiguous (the search box → `aria-label`, the decorative watermark → `alt=""`) from the theme without waiting on app-config. Bucket-2: authored, flagged for browser confirmation.
- **Human-owned, by proof, not assertion:** SYS-2 (the search-results page body + `isp_*` markup — the theme repo can't reach `{{ page.content }}` and the app owns its own DOM), SYS-3/SYS-4 (content at scale + admin copy), SYS-5 image re-exports (content) and blind LCP `fetchpriority` (browser-gated), SYS-6 (per-app business decisions + app-injected scripts), SYS-7 (FOUC-risky / app-injected / benign), SYS-8 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge).
- **What I deliberately did *not* shim in SYS-1:** the generic content `<img>` flagged on the search page (likely a result/product image whose correct alt is the product name — a generic theme alt would be *meaningless* alt, the very thing the manual pass exists to catch) and the unnamed link/button (naming it blind risks a wrong accessible name). Both stay with the app config — handed off below. So §F missing-image-alt may only *partly* clear (the watermark) while missing-aria-labels should clear fully. I'd rather ship the two correct names than fabricate two wrong ones.

So "do everything" resolves to: **ship the one contained, theme-authorable fix that remains — SYS-1 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 heading outline** — demote the stray `<h1>` on `/pages/search-results` (admin page body) and/or the `isp_*` search-app template → Jenna/Britni + Mason to ID the search app.
- **SYS-2/SYS-1 residue: the generic search-result `<img>` alt + the unnamed `isp_*` link** — supply via the search app's config (correct names need the rendered result context) → Mason to ID the app + Jenna.
- **SYS-3 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-4 duplicate descriptions** — 5 sets of bespoke copy in admin → Jenna/Britni.
- **SYS-5 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna; blind LCP `fetchpriority` on collection/product → a browser-gated PR.
- **SYS-6 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-7 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-8 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

The change is a self-contained snippet rendered from a single line, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. It mirrors the validated `snippets/a11y-frame-title.liquid` exactly, kept as a *separate* snippet so the banked frame-title shim stays byte-for-byte untouched (zero regression risk to the validated win).

### Task A — SYS-1 · Search-app accessibility (A11Y-1 slivers)
- **The defect:** the third-party search app injects, on `/pages/search-results`, an unlabeled `<input id="isp_main_search_box">` (crawl: missing-form-label = 1) and a `<img id="isp_watermark_img">` with no `alt` (crawl: 1 of the missing-image-alt), plus a generic `<img>` and one unnamed link. The markup is **not** in the theme: a repo-wide search for `isp_` returns only the scorecard files, never source. The controls are added at runtime, so there is no author-time element to set attributes on in Liquid.
- **The fix (a contained, additive shim):** new snippet `snippets/a11y-search-app.liquid`, rendered once from `layout/theme.liquid` just before `</body>` (right after the frame-title render). On initial run and via a `MutationObserver` (the search app injects late) it sets, **only when missing**:
  - `aria-label="Search products"` on `#isp_main_search_box` that has no `aria-label`/`aria-labelledby`/`title`;
  - `alt=""` on `#isp_watermark_img` that has no `alt` (the watermark is decorative chrome — empty alt is the correct accessible treatment).
  The observer **disconnects after 20 s** so it adds no perpetual main-thread cost. The `:not(...)` guards make it idempotent — it only ever touches an element that is genuinely unnamed.
- **Why it's safe to author for review:** purely additive — it sets attributes only on elements that lack them, scoped to two specific `isp_*` IDs, so it cannot mislabel an unrelated control. It adds no markup, changes no styles, touches no app behavior, removes nothing. Worst case if a selector/timing is off: the crawl still flags and nothing else changes. Fork-safe (one snippet + one render line, no Dawn-core edit) and bounded (observer disconnects at 20 s).
- **Why bucket-2, not bucket-1:** the controls are runtime-injected, so the fix can only be *confirmed* with a browser — the crawl/axe must re-run against the live search-results DOM. Authored from the source-true `isp_*` IDs in the crawl evidence; flagged for browser confirmation at review.
- **Scope / sweep:** the missing-name pattern across the theme is exactly these runtime-injected `isp_*` controls (no in-theme input/img lacks a name — the card-image alt fallback and the predictive/header search inputs already carry labels). The generic result `<img>` and unnamed link are deliberately left to the app config (see §1 — a blind name would be wrong/meaningless).
- **Closes (code side):** the form-label sliver + the watermark image-alt sliver of A11Y-1, sitewide. The next baseline's §F missing-aria-labels (→ 0) and missing-image-alt rows are the test.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. The change is authored to pass them:
- **Theme Check:** no new offenses — the edit adds one snippet (plain JS in a `<script>`, no Liquid objects beyond a comment) and one `{% render %}` line; no `settings_data.json`, no new translation keys (the label is a plain English string, matching the theme's existing hardcoded English). Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and on `/pages/search-results`: **the crawl/axe shows 0 missing-aria-labels and the watermark no longer counts as missing-alt** once the search app renders. Confirm the search box still behaves identically (the shim only adds an `aria-label`) and no unrelated control was relabeled.
- **Fork-safe:** self-contained snippet + single render line; no Dawn-core restyle, no `settings_data.json`; the validated `a11y-frame-title.liquid` is left untouched.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; the snippet's one comment block explains why the names are set in the theme (the markup is app-injected) and that the shim is removable once the search-app config carries them.

## 4. Todo

**Phase 1 — SYS-1 search-app accessibility (code)**
- [x] A1 · new `snippets/a11y-search-app.liquid` — name untitled `#isp_main_search_box` (aria-label) + `#isp_watermark_img` (alt=""), idempotent, self-disconnecting observer (A11Y-1)
- [x] A2 · `layout/theme.liquid` — render `a11y-search-app` once before `</body>`, after the frame-title render (A11Y-1)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-24`, `git add -A` (cycle data + plan/execution + search-app fix), commit, push
- [x] H2 · open ONE PR (cycle data + fix) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- §F sitewide crawl — **Pages missing aria-labels: 1**, **Pages missing image alt: 1** (both `/pages/search-results`, the `isp_*` search app). Target: 0 (BASELINE §F).
- A11Y-1 sitewide a11y prevalence — **1,716 flagged elements across 181 pages** (1,711 HTML-structural = the heading-order family; 3 image-alt + 1 form-label + 1 unnamed-link = the `isp_*` search app). Target: 0.
- §D golden-path axe — **0 failing audits on all 6 runs**; Lighthouse Accessibility **100** on every golden page × device (the frame-title shim, now live, cleared the last golden-path failure).
- Cycle deltas vs 2026-06-23 (`diff.md`): a11y rule improved — **`frame-title` 6 → 0** (last cycle's shim, now live); total findings 33 → 31. The 3 "field regressions" are sub-ms / single-ms CrUX jitter, all still "good" (§C all ✓).

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the **next cycle's `diff.md`**; link it back to this PR to close the loop. The decisive signal will be **§F missing-aria-labels → 0** and the watermark dropping off missing-image-alt (as `frame-title` 6→0 confirmed last cycle's shim). No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — `snippets/a11y-search-app.liquid` + one render line in `layout/theme.liquid`, naming the runtime-injected `isp_*` search box (`aria-label`) and decorative watermark (`alt=""`) so the sitewide crawl's a11y rows clear. Purely additive (only sets missing attributes); zero visual/behavioral change; self-disconnecting observer (no perpetual cost). The validated frame-title shim is left untouched.

**Already merged (awaiting/at publish):** last cycle's Mailchimp frame-title shim (validated this cycle: `frame-title` 6→0). Earlier PRs — the cart-drawer `card_heading_tag` heading cascade (185→2), the hero label fix (`label-content-name-mismatch` 3→0), slideshow/pagination labels, card-image alt fallback, card-product `h3→h2` + stray product `h1→h2`, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Deferred (named in §1, with owner):** SYS-2 heading outline + the residual search-result `<img>` alt / unnamed link (admin body + `isp_*` app-config), SYS-3 meaningful alt (content), SYS-4 duplicate descriptions (content), SYS-5 image re-exports (content) + blind fetchpriority (browser-gate), SYS-6 app JS (business + app-config), SYS-7 CSS/JS path (browser-gate), SYS-8 Permissions-Policy (platform).
