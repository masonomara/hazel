# Execution — 2026-06-23

Site: https://hazelboutique.com/ · Cycle: 2026-06-23 · Branch: `hobbes-cycle-2026-06-23` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This run carries the **2026-06-23 cycle data** (baseline/findings/diff/digests, 33 findings) **plus** the one theme-code fix that data justifies — titling the Mailchimp popup iframes (SYS-1, A11Y-1) — in **one branch and one PR**, `hobbes-cycle-2026-06-23`, so the scorecard and the fix travel together. The re-measurement is what makes this honest: it **validated** last cycle's hero label fix (`label-content-name-mismatch` 3 → 0, now live), which leaves **`frame-title` as the only failing golden-path axe audit**. SYS-1 is the contained theme-side fix for it.

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~18 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author without a browser** — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Mailchimp popup frame-title | 1 | ✅ **(code)** | the only unshipped, theme-authorable lever; a contained, additive shim titles the runtime-injected popup iframes — clears the last failing golden-path axe audit |
| 2 | SYS-2 · Heading outline (admin pages) | 2 | ⛔ content | cascade validated (185→2); the 2 remainders live in admin `{{ page.content }}` bodies |
| 3 | SYS-3 · Search-app a11y | 2 | ⛔ app-owned | all A11Y-2 slivers are `isp_*` search-app markup on /pages/search-results — not theme |
| 4 | SYS-4 · Image alt | 4 | ⚪ merged / content | card-image alt fallback merged (axe image-alt 4→0); meaningful alt is content; theme sweep clean |
| 5 | SYS-5 · Page metadata | 2 | ⛔ content | dup titles fixed (4→0); 5 dup descriptions = bespoke admin copy |
| 6 | SYS-6 · Image delivery | 3 | ⚪ merged / content | logo dims + LCP fetchpriority merged; HEIC/oversized re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-15 has no clean Liquid cross-section dedup and is benign |
| 9 | SYS-9 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1 alone, and why that is "do everything safe," not under-delivery.** The structural heading cascade (cart-drawer `card_heading_tag`) and last cycle's hero label fix are **already in `main`** and the re-crawl proves both worked (skipped-level 185→2; `label-content-name-mismatch` 3→0); re-doing either is wasted motion. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch). The Mailchimp popup is runtime-injected, so the clean fix is the embed config — but a small, additive shim titles the iframes from the theme without waiting on app-config, clearing the last failing golden-path axe audit. Bucket-2: authored, flagged for browser confirmation.
- **Human-owned, by proof, not assertion:** SYS-2 (two admin page bodies — the theme repo can't reach `{{ page.content }}`), SYS-3 (the `isp_*` search app owns the form-label/image-alt/unnamed-link slivers — verified absent from theme source), SYS-7 (per-app business decisions + app-injected scripts), SYS-9 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and the **content** layer — SEO-3 duplicate descriptions, PERF-2/5 image re-exports, SYS-4 meaningful alt.
- **SYS-8** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected, and PERF-15's duplicated JS has no reliable Liquid cross-section dedup while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **ship the one contained, theme-authorable fix that remains — SYS-1 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 heading outline (2 pages)** — remove/demote the stray search-results h1; insert the missing `<h2>` on /pages/sizing, both in the admin page body → Jenna/Britni.
- **SYS-3 search-app a11y** — label the `isp_main_search_box` input, alt the `isp_watermark_img`, name the unnamed link via the search app's config/template → Mason to ID the app + Jenna.
- **SYS-4 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-5 duplicate descriptions** — 5 sets of bespoke copy in admin → Jenna/Britni.
- **SYS-6 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna.
- **SYS-7 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

The change is a self-contained snippet rendered from a single line, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle.

### Task A — SYS-1 · Mailchimp popup frame-title (A11Y-1)
- **The defect:** the Mailchimp embed injects two `about:blank` iframes with no `title` on every page — `#PopupSignupForm_0 > .mc-banner … > iframe` and `#PopupSignupForm_0 > .mc-modal … > iframe` (from `findings.md` A11Y-1 evidence) — so axe's `frame-title` fires (2 nodes, all 6 golden runs). The markup is **not** in the theme: a repo-wide search for `PopupSignupForm` / `mc-banner` / `mailchimp` returns only the scorecard files, never source. The popup is added at runtime by the embed, so there is no author-time iframe to put a `title` on in Liquid.
- **The fix (a contained, additive shim):** new snippet `snippets/a11y-frame-title.liquid`, rendered once from `layout/theme.liquid` just before `</body>`. It sets `title="Newsletter sign-up"` on any iframe inside `[id^="PopupSignupForm"]` that lacks one, on initial run and via a `MutationObserver` (the popup injects late, on delay/exit-intent), then **disconnects the observer after 20 s** so it adds no perpetual main-thread cost. The selector `:not([title])` makes it idempotent — each mutation only touches new, untitled frames.
- **Why it's safe to author for review:** the shim is **purely additive** — it only sets a `title` attribute on iframes that have none. It adds no markup, changes no styles, touches no app behavior, and removes nothing. The selector is scoped to the Mailchimp container (`[id^="PopupSignupForm"]`), so it cannot mislabel an unrelated embed (e.g. a video iframe). Worst case if the selector or timing is off: `frame-title` still flags and nothing else changes. It's fork-safe (one snippet + one render line, no Dawn-core edit) and bounded (observer disconnects at 20 s).
- **Why bucket-2, not bucket-1:** the popup is runtime-injected, so the fix can only be *confirmed* with a browser — axe must re-run against the live, popped DOM. Authored from the source-true container id in the evidence; flagged for browser confirmation at review.
- **Scope / sweep:** `frame-title` across the theme is exactly these two Mailchimp iframes (the only iframes the catalog flags, and the only `about:blank` app-injected frames on the golden path). No other in-theme iframe lacks a title; the shim's container scope means it acts only on the Mailchimp popup.
- **Closes (code side):** A11Y-1's 2 golden-path nodes (sitewide). The next baseline's A11Y-1 node count is the test.

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. The change is authored to pass them:
- **Theme Check:** no new offenses — the edit adds one snippet (plain JS in a `<script>`, no Liquid objects beyond a comment) and one `{% render %}` line; no `settings_data.json`, no new translation keys (the title is a plain string, matching the theme's existing hardcoded English like the hero logo alt). Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors, and **axe shows 0 `frame-title` once the Mailchimp popup is open** (trigger the banner + modal so both iframes exist, then re-run axe). Confirm the popup still appears and behaves identically (the shim only adds a `title` attribute) and no other iframe was mislabeled.
- **Fork-safe:** self-contained snippet + single render line; no Dawn-core restyle, no `settings_data.json`.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; the snippet's one comment block explains why the title is set in the theme (the markup is app-injected) and that the shim is removable once the embed config carries a title.

## 4. Todo

**Phase 1 — SYS-1 Mailchimp popup frame-title (code)**
- [x] A1 · new `snippets/a11y-frame-title.liquid` — title untitled iframes inside `[id^="PopupSignupForm"]`, idempotent, self-disconnecting observer (A11Y-1)
- [x] A2 · `layout/theme.liquid` — render `a11y-frame-title` once before `</body>` (A11Y-1)

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-23`, `git add -A` (cycle data + plan/execution + frame-title fix), commit, push
- [x] H2 · open ONE PR (cycle data + fix) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- A11Y-1 `frame-title` — **2 nodes, sitewide** (the Mailchimp popup banner + modal iframes); the only failing golden-path axe audit (§D, all 6 runs). Target: 0 failing a11y audits (BASELINE §D).
- A11Y-2 sitewide a11y prevalence — **1,716 flagged elements across 181 pages** (1,711 HTML-structural = the heading-order family; 3 image-alt + 1 form-label + 1 unnamed-link = the `isp_*` search app on /pages/search-results). Target: 0.
- Cycle deltas vs 2026-06-22 (`diff.md`): a11y rule improved — **`label-content-name-mismatch` 3 → 0** (last cycle's hero fix, now live); sitewide **duplicate titles 4 → 0**, invalid inline SVG 185 → 181; total findings 35 → 33. The 4 "field regressions" are sub-ms CrUX jitter, all still "good" (§C all ✓).

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the **next cycle's `diff.md`**; link it back to this PR to close the loop. The decisive signal will be **A11Y-1 `frame-title` dropping off 2 nodes** (as `label-content-name-mismatch` 3→0 confirmed last cycle's fix). No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — `snippets/a11y-frame-title.liquid` + one render line in `layout/theme.liquid`, titling the runtime-injected Mailchimp popup iframes so axe's `frame-title` clears. Purely additive (only sets a missing `title`); zero visual/behavioral change; self-disconnecting observer (no perpetual cost).

**Already merged (awaiting publish):** last cycle's hero slideshow naming fix (validated this cycle: `label-content-name-mismatch` 3→0). Earlier PRs — the cart-drawer `card_heading_tag` heading cascade (185→2), slideshow/pagination labels, card-image alt fallback, card-product `h3→h2` + stray product `h1→h2`, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Deferred (named in §1, with owner):** SYS-2 heading outline (2 admin page bodies — content), SYS-3 search-app a11y (`isp_*` app-config), SYS-4 meaningful alt (content), SYS-5 duplicate descriptions (content), SYS-6 image re-exports (content), SYS-7 app JS (business + app-config), SYS-8 CSS/JS path (browser-gate), SYS-9 Permissions-Policy (platform).
