# Execution — 2026-06-24

Site: https://hazelboutique.com/ · Cycle: 2026-06-24 · Branch: `hobbes-cycle-2026-06-24` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s order, implements the code against the **real codebase**, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

> This run carries the **2026-06-24 cycle data** (baseline/findings/diff/digests, 31 findings) **plus** the one theme-code fix that data justifies — giving the **footer logos real intrinsic dimensions** so the unsized-image flag clears (SYS-1, PERF-14) — in **one branch and one PR**, `hobbes-cycle-2026-06-24`, so the scorecard and the fix travel together. The re-measurement is what makes this honest: it **validated** the Mailchimp popup shim (`frame-title` 6 → 0, now live), so **§D axe is clean on all six golden runs** and Accessibility reads 100 everywhere; today's search-app shim (#22) is in `main` awaiting publish. With the a11y surface banked, the genuinely-open theme lever this run is the footer-logo CLS defect the prior plans missed.

## 1. Batch selection — effort budget B = 100 ("do everything safe")

The run's budget is **100** — far above a full plan (~12 pts), i.e. *clear every system the run can legitimately clear*. The budget is **not** the binding constraint. What bounds this run is what's left after the merged/awaiting-publish work, filtered to **theme code Hobbes can author without a browser** — because the run writes only to GitHub and cannot run a browser or the CLI.

Walking `plan.md`'s order top-down against the **verified** current state of `main`:

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Image sizing (unsized images / CLS) | 1 | ✅ **(code)** | the one unshipped, theme-authorable lever — footer logos ship invalid `width="100%" height="auto"`; real intrinsic dims + additive CSS, known values, theme-wide sweep |
| 2 | SYS-2 · Heading outline & structural a11y | 2 | ⛔ content | cascade banked (185→2); the 2–3 remainders live in admin `{{ page.content }}` bodies |
| 3 | SYS-3 · Image alt coverage | 4 | ⚪ merged / content | card-image alt fallback merged (axe image-alt 0); meaningful alt is content; theme sweep clean |
| 4 | SYS-4 · Page metadata | 2 | ⛔ content | 5 dup descriptions = bespoke admin copy |
| 5 | SYS-5 · Image delivery & weight | 4 | ⛔ content | HEIC/oversized re-exports are source-asset work (Jenna), not a theme edit |
| 6 | SYS-6 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + app-injected scripts, not a repo change |
| 7 | SYS-7 · Theme CSS path | 3 | ⛔ no clean+safe code | base.css deferral = FOUC risk; RM Neue/reflow app-injected; PERF-15 has no clean Liquid cross-section dedup and is benign |
| 8 | SYS-8 · Security headers | 2 | ⚪ merged / platform | Referrer-Policy merged; Permissions-Policy is platform/edge-bound |

**Why the batch is SYS-1, and why that is "do everything safe," not under-delivery.** The heading cascade, the hero label fix, the Mailchimp `frame-title` shim, and today's search-app shim are **already in `main`**, and the re-crawl proves the a11y front works (skipped-level 185→2; `frame-title` 6→0; §D clean). Re-doing any of them is wasted motion. The *genuinely remaining* work is then:
- **Theme code Hobbes can ship → SYS-1** (this batch). The footer logos carry `width="100%" height="auto"` — invalid HTML dimension attributes that give the browser no aspect ratio, which is exactly PERF-14's "unsized images" on the 2 non-index golden pages. The dims are known (the hero already declares the same source files; the content images measured from the CDN; `icon-with-text` reads the Shopify image object). Authored from source; bucket-2, flagged for browser confirmation.
- **Human-owned, by proof, not assertion:** SYS-2 (two admin page bodies — the theme repo can't reach `{{ page.content }}`), SYS-4 (5 duplicate descriptions = bespoke copy), SYS-5 (HEIC/oversized re-exports = source assets), SYS-6 (per-app business decisions + app-injected scripts), SYS-8 Permissions-Policy (no `<meta>` mechanism on Shopify — platform/edge), and SYS-3 meaningful alt at scale.
- **SYS-7** has no slice that is both clean and safe to author blind: deferring `base.css` risks above-the-fold FOUC, the RM Neue `@font-face` and forced-reflow are app-injected, and PERF-15's duplicated JS has no reliable Liquid cross-section dedup while being functionally benign (Dawn guards `customElements.define`). 4 KB at impact 2 is not worth a core-commerce-path edit that can't be verified here.

So "do everything" resolves to: **ship the one contained, theme-authorable fix that remains — SYS-1 — and hand each non-code remainder to its proven owner.**

**Deferred this cycle (named, not silent), with owner:**
- **SYS-2 heading outline (2–3 pages)** — demote the stray search-results h1; insert the missing `<h2>` on `/pages/sizing`, both in the admin page body → Jenna/Britni.
- **SYS-3 meaningful alt at scale** — per-product admin image alt → Jenna/Britni.
- **SYS-4 duplicate descriptions** — 5 sets of bespoke copy in admin → Jenna/Britni.
- **SYS-5 oversized/HEIC re-exports** — re-export to WebP/AVIF at sane dimensions → Jenna.
- **SYS-6 third-party app JS** — per-app business decision + per-removal testing (start with Route, flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-7 theme CSS/JS path** — base.css critical-CSS deferral and any JS-loading change touch above-the-fold styling or core commerce scripts; held for a dedicated PR with the browser gate this run can't run.
- **SYS-8 Permissions-Policy** — no theme/meta mechanism on Shopify → confirm with Shopify support.

## 2. Implementation plan — against the real source

The change is the web-standard fix for unsized images: give each `<img>` its real intrinsic `width`/`height` (so the browser reserves the correct aspect-ratio box → no layout shift) and let CSS `width:100%; height:auto` keep it responsive. Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle.

### Task A — SYS-1 · Footer logos (PERF-14, golden path) ✅
- **The defect:** `sections/footer.liquid` renders the non-index footer logos with `width="100%" height="auto"` (lines ~208–223). Those are *invalid* values for the HTML `width`/`height` content attributes (integer pixels only), so the browser gets no aspect ratio and reserves the wrong box — PERF-14's "unsized images." The footer block renders on Collection + Product (not `/`, which shows the hero block), matching PERF-14's "flagged on 2 page(s)" and the evidence (`alt="Hazel Boutique"`, `hazel-mobile-logo.png?v=1713641093&width=760`).
- **The fix:**
  - Desktop `script-logo.png` → `width="4335" height="531"` (the hero declares the identical file at these dims; confirmed against the CDN source).
  - Mobile `hazel-mobile-logo.png?…&width=760` → `width="760" height="316"` (the CDN-served size; same aspect ratio as the 1053×438 source).
  - `assets/section-footer.css` — add `width: 100%; height: auto;` to `.footerLogo--desktop` and `.footerLogo--mobile` so the logos keep their responsive full-width display (previously supplied by the now-removed inline `width="100%"`). The rules already live in that file under the `/* mason */` Hazel section — kept there to match the surrounding code rather than scattering one rule into `base.css`.
- **Why bucket-2:** it changes how the footer logos are sized, so the rendered result needs a browser to confirm. Authored from known dims; flagged for confirmation at review.
- **Closes (code side):** PERF-14's 2 golden-path nodes. The next baseline's PERF-14 page count is the test.

### Task B — SYS-1 sweep · `snippets/icon-with-text.liquid` ✅
- **The defect:** the three optional block images render with `width="auto" height="auto"` — invalid, same family as the footer. Off the golden path (a product-page block), so PSI didn't flag it, but it's the same pattern — and the EXECUTE template's rule is "one pattern → one exhaustive sweep."
- **The fix:** emit the Shopify image object's own dimensions — `width="{{ block.settings.image_N.width }}" height="{{ block.settings.image_N.height }}"`. The object always carries correct intrinsic dims, so this is the canonical Dawn pattern and zero-risk: `.icon-with-text img` already pins display to a fixed `--icon-size` square with `object-fit: contain`, so the attributes only add the aspect-ratio hint and change no rendered size.
- **Closes:** the unsized-image pattern in this snippet (not separately measured; prevents resurfacing).

### Task C — SYS-1 sweep · `sections/main-page.liquid` (`/pages/our-story`) ✅
- **The defect:** the about-page hero and the script-logo title image render with `width="100%" height="auto"`. Only on `/pages/our-story` — off the golden path and not in the crawl's PERF flags — but the same anti-pattern.
- **The fix:**
  - About hero `IMG_1248…webp` (served as JPEG) → `width="2367" height="3247"` (measured from the CDN source).
  - Title `script-logo_5.png` → `width="1729" height="493"` (measured from the CDN source).
  - `assets/base.css` — add `width: 100%; height: auto;` to `.main--about--image` (no prior rule) and `.main--about--titleImage` (previously margin-only), preserving the author's explicit `width="100%"` full-width intent while giving a defined aspect-ratio box. Added in `base.css` beside the existing `.main--about--*` rules (where this page's Hazel CSS already lives).
- **Why bucket-2 (and slightly more cautious than A/B):** `/pages/our-story` is a bespoke editorial layout this run can't see, and `width="100%"` as an HTML attribute is ambiguous across browsers. The fix is authored to preserve the evident full-width intent, but the human should confirm the our-story layout is unchanged at review. If the about hero was relying on a cover-crop, this is the one hunk to eyeball.
- **Closes:** the unsized-image pattern on `/pages/our-story` (not separately measured; prevents resurfacing).

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. The change is authored to pass them:
- **Theme Check:** no new offenses — the edits swap attribute values and add a few CSS declarations; no new files, no `settings_data.json`, no new translation keys (the footer/our-story alt text is the theme's existing hardcoded English). Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):**
  - **Footer (Task A) —** on Collection + Product, mobile **and** desktop: the footer logo still displays full-width and centered as before, and no longer shifts as it loads. Re-run PSI/axe if convenient: PERF-14 should no longer flag these pages.
  - **icon-with-text (Task B) —** if any product uses an icon-with-text block with images, confirm the icons render at the same size (the `--icon-size` square) — no change expected.
  - **our-story (Task C) —** load `/pages/our-story` mobile + desktop and confirm the hero image and the script-logo title render as before (full column width, no distortion or unexpected crop).
  - No new console errors on any of the above.
- **Fork-safe:** attribute + CSS edits only; no Dawn-core restyle, no `settings_data.json`, Hazel CSS kept in the existing Hazel sections.
- **No baseline regression** against `baseline.md` targets — the change only adds aspect-ratio information and cannot worsen CLS.
- **No unnecessary comments**; the edits match the surrounding files' style.

## 4. Todo

**Phase 1 — SYS-1 image sizing (code)**
- [x] A · `sections/footer.liquid` — real intrinsic dims on both footer logos (PERF-14)
- [x] A · `assets/section-footer.css` — `width:100%; height:auto` on `.footerLogo--desktop` / `.footerLogo--mobile` to preserve responsive display (PERF-14)
- [x] B · `snippets/icon-with-text.liquid` — emit the image object's `.width`/`.height` on all three block images (PERF-14 sweep)
- [x] C · `sections/main-page.liquid` — real intrinsic dims on the our-story hero + title images (PERF-14 sweep)
- [x] C · `assets/base.css` — `width:100%; height:auto` on `.main--about--image` / `.main--about--titleImage` (PERF-14 sweep)
- [x] Sweep verified — no remaining `width="100%"` / `height="auto"` / `width="auto"` on any theme `<img>`

**Phase 2 — handoff**
- [x] H1 · branch `hobbes-cycle-2026-06-24`, `git add -A` (cycle data + plan/execution + image-sizing fix), commit, push
- [x] H2 · open ONE PR (cycle data + fix) with before/after + named deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md` / `diff.md`):**
- PERF-14 unsized images — **flagged on 2 golden pages** (Collection + Product, mobile), evidence `alt="Hazel Boutique"` + `hazel-mobile-logo.png?…&width=760` = the footer logos. Target: explicit `width`/`height` on image elements (BASELINE Targets, CLS).
- §D axe — **0 failing audits on all six golden runs** (`frame-title` 6 → 0 this cycle; Accessibility 100 everywhere). §F crawl still reads "missing aria-labels: 1" (the `isp_*` search box — named by today's merged-but-unpublished search-app shim).
- §C field — CrUX passes LCP/INP/CLS on all three golden pages (all ✓); CLS specifically Home 0.08 / Collection 0.01 / Product 0.0. The 3 "field regressions" in `diff.md` are sub-ms CrUX jitter, all still "good."

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the **next cycle's `diff.md`**; link it back to this PR to close the loop. The decisive signal will be **PERF-14 dropping its 2 flagged pages** (as `frame-title` 6→0 confirmed the Mailchimp shim). No after is fabricated here.

**Shipped this PR (theme code):** SYS-1 — real intrinsic `width`/`height` on the footer logos (`sections/footer.liquid`) + responsive CSS (`section-footer.css`); the same fix swept through `snippets/icon-with-text.liquid` (via the Shopify image object) and `sections/main-page.liquid` + `base.css` (our-story). Adds only aspect-ratio information; cannot worsen CLS.

**Already merged (awaiting publish):** today's search-app shim (`snippets/a11y-search-app.liquid`, #22) and the Mailchimp `frame-title` shim (validated this cycle: `frame-title` 6→0). Earlier PRs — the cart-drawer `card_heading_tag` heading cascade (185→2), slideshow/pagination labels, card-image alt fallback, hero label fix, meta-description + OG/Twitter, hero-logo dims + LCP fetchpriority, Referrer-Policy meta.

**Human to-do (by owner):**

*Publish — Mason (every PR)*
- [ ] Merge → push to a dev/unpublished theme → verify mobile + desktop → publish live → add the `published` label. (Steps in `PUBLISH-TEMPLATE.md`.) Closes the loop on this PR + the awaiting-publish search-app and frame-title shims.

*Browser-confirm at review — Mason (bucket-2, authored-but-unverified)*
- [ ] **Footer (SYS-1/PERF-14):** Collection + Product, mobile + desktop — footer logo still full-width/centered and no longer shifts on load; PERF-14 no longer flags these pages.
- [ ] **icon-with-text (SYS-1 sweep):** any product using an icon-with-text block — icons render at the same `--icon-size`, no change.
- [ ] **our-story (SYS-1 sweep):** `/pages/our-story` mobile + desktop — hero + script-logo render as before, no distortion/crop.

*Content — Jenna / Britni*
- [ ] **SYS-2:** demote the stray `<h1>` on `/pages/search-results`; insert the missing `<h2>` on `/pages/sizing` (admin page bodies).
- [ ] **SYS-3:** author meaningful per-product image `alt` where blank (admin).
- [ ] **SYS-4:** rewrite the 5 sets of duplicate meta descriptions to be unique (admin).
- [ ] **SYS-5:** re-export oversized JPEGs and the raw `.heic` source files to WebP/AVIF at sane dimensions.

*App / platform — Mason + Jenna / Britni / Brenda*
- [ ] **SYS-6:** app-by-app JS audit — start with Route (flagged for removal in `DEVELOPMENT.md`), defer/async the rest.
- [ ] **SYS-8:** confirm with Shopify support whether `Permissions-Policy` is settable on Advanced (no theme/`<meta>` mechanism).

That open PR **is** the handoff to `publish` — execution is done. The cycle closes only after publish takes it live and the next baseline confirms the after (PERF-14 dropping its 2 pages).
