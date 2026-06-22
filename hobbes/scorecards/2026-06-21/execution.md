# Execution — 2026-06-21

Site: https://hazelboutique.com/ · Cycle: 2026-06-21 · Branch: `hobbes-fix-2026-06-21` · Driven by Hobbes from `plan.md`.

This run takes the top of `plan.md`'s order, selects the batch the effort budget allows, writes the code-level implementation against the **real codebase**, implements it, and stops at a pushed branch + open PR for human review. Per the run's hard rules and `DEVELOPMENT.md`, it **writes only to GitHub** — it does **not** run the Shopify CLI, Theme Check, or any publish. Verification (Theme Check, browser, mobile + desktop) and the live publish are the human's, at review.

## 1. Batch selection — effort budget B = 20

Walking `plan.md`'s order top-down. The first four ranks are the accessibility front (mission priority 1) and their **theme code is already merged into `main`** by the 2026-06-20 PR (#9) — it is verified-pending-publish, not unbuilt. The findings catalog still lists those a11y rules because it measures the **live** site, which predates publish (`diff.md` already shows the partial publish landing: `label-content-name-mismatch` 11→3). So the budget is not spent re-doing them; it flows to the highest-leverage **unshipped** code.

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-2 · Heading hierarchy | 2 | ⚪ in `main` / partial defer | nested-heading cascade shipped 06-20; outline reorder needs the **browser gate** → deferred |
| 2 | SYS-1 · Theme a11y controls | 2 | ⚪ in `main` | slideshow + pagination label fixes shipped 06-20 |
| 3 | SYS-4 · Mailchimp popup | 2 | ⛔ human-owned | app-config / marketing decision, no theme code to ship |
| 4 | SYS-3 · Image alt | 3 | ⚪ in `main` / partial defer | card-image alt fallback shipped 06-20; meaningful alt at scale is content |
| 5 | SYS-5 · Page metadata | 3 | ✅ **(code half)** | meta-description fallback + OG/Twitter image fallback — top unshipped code |
| 6 | SYS-6 · Image delivery | 3 | ✅ **(code half)** | logo intrinsic dims + LCP `fetchpriority`; heavy/HEIC re-exports are content |
| 7 | SYS-7 · Third-party app JS | 4 | ⛔ human-owned | app removal/defer = business decisions + per-app testing, not a repo change |
| 8 | SYS-8 · Theme CSS path | 3 | ⛔ verify-bound | critical-CSS deferral / JS-include dedup risk FOUC + break quick-add; need the browser gate |
| 9 | SYS-9 · Security headers | 2 | ✅ **(Referrer-Policy)** | one-line head meta; Permissions-Policy is platform-bound |

**Budget math.** The realizable, GitHub-only, high-confidence code this run = SYS-5 code (3) + SYS-6 code (3) + SYS-9 Referrer-Policy (2) = **8 of 20**. The budget is *not* the binding constraint this cycle, and this is a deliberate call, not timidity (the template's caution against under-delivering is noted): ranks 1–4 are already in `main`; ranks 7 (app removal) and 4/3 content are **human-owned**; ranks 8 and the SYS-2 reorder are **browser-verification-bound**, and this run's hard rule forbids running the CLI/Theme Check/browser — so taking them on would mean shipping unverifiable changes to core commerce + above-the-fold paths, exactly what the gate exists to prevent. The honest move is to clear **every** safe code win in the order and flag the rest with its owner, rather than pad the batch with work that can't be verified here.

**Batch = SYS-5 (code) + SYS-6 (code) + SYS-9 (Referrer-Policy).** One PR: the discoverability layer (priority 2), the image-delivery code half (priority 3), and the shippable security header — no content, no app, no waiting on anyone.

**Deferred this cycle (named, not silent):**
- **SYS-4 Mailchimp popup** — human-owned (Mailchimp embed config or a drop-the-popup decision → Brenda/Jenna).
- **SYS-7 Third-party app JS** — per-app business decision + per-removal testing (start with Route, already flagged in `DEVELOPMENT.md`) → Mason + Jenna/Britni/Brenda.
- **SYS-8 Theme CSS path** + **SYS-2 heading-level reorder / Home single-h1** — code, but every change shifts above-the-fold styling or visible heading hierarchy or a core commerce script; held for a dedicated PR with the browser gate this run can't run.
- **SYS-5 duplicate titles/descriptions (SEO-5/6)** + **SYS-6 oversized/HEIC re-exports (PERF-2/5)** + **SYS-3 meaningful alt at scale** — admin/content work → Jenna/Britni.
- **SYS-9 Permissions-Policy** — no theme/meta mechanism on Shopify; platform/edge-controlled → confirm with Shopify support, not a theme change.

## 2. Implementation plan — against the real source

Every change is a self-contained snippet/section/head edit, Hazel-fork-safe, no `settings_data.json`, no Dawn-core restyle. File:line references are from this repo at branch point.

### Task A — SYS-5 · meta-description fallback (SEO-1)
- **Where:** `layout/theme.liquid:25` — was `{% if page_description %}<meta name="description" …>{% endif %}`, emitting nothing for the 76 pages with no admin description.
- **Fix:** compute `meta_description` in the head with a typed fallback chain — `page_description` → (collection) `collection.description`, else a generated `Shop {{ collection.title }} at {{ shop.name }}.` → (product/page/article) the resource body, truncated 160 → `shop.description | default: shop.name`. Emit the tag whenever non-blank, and pass the same value into `meta-tags` so OG/Twitter descriptions match.
- **Why the generated collection line:** it gives each description-less collection a **unique** string, so closing SEO-1 doesn't manufacture new SEO-6 duplicates.
- **Closes:** SEO-1 (code half — every page now ships a description). Home included (falls to `shop.description`).

### Task B — SYS-5 · OG / Twitter image fallback + `twitter:image` (SEO-4)
- **Where:** `snippets/meta-tags.liquid:22` — `og:image` was emitted only when `page_image` existed (Home has none → no card), and there was **no `twitter:image` at all**.
- **Fix:** `assign og_image = page_image | default: settings.share_image | default: settings.logo`; render `og:image` / `:secure_url` / `:width` / `:height` and a new `twitter:image` from `og_image`, constrained to `width: 1200` with a proportional height. Added a `share_image` image-picker to the social-media group in `config/settings_schema.json` so the merchant can set a proper lifestyle share card; until then it falls back to the existing logo, so the finding closes now.
- **Closes:** SEO-4 (Home + the 43 pages missing OG image; adds the absent `twitter:image`).

### Task C — SYS-6 · hero-logo intrinsic dimensions (PERF-12, BP-3)
- **Where:** `sections/hero.liquid:197/203` — both brand logos shipped `width="100%" height="auto"`, invalid `<img>` content attributes → flagged unsized (PERF-12) and aspect-ratio-mismatch (BP-3).
- **Fix:** set the real intrinsic pixel dimensions (confirmed by fetching the live CDN PNGs) — `script-logo.png` `width="4335" height="531"`, `hazel-mobile-logo.png` `width="1053" height="438"` — and add `width: 100%; height: auto;` to `.hero-logo img` in `assets/component-hero.css` (the Hazel-custom hero stylesheet, co-located with the markup) so display sizing is preserved while the attributes supply the correct aspect ratio.
- **Closes:** PERF-12 and BP-3 for both logos.

### Task D — SYS-6 · LCP `fetchpriority` on the hero (PERF-14)
- **Where:** `sections/hero.liquid:95` (mobile hero) and `:179` (desktop hero) — the first slide image is the mobile LCP element but carried no `fetchpriority`.
- **Fix:** add `{% if forloop.first %}fetchpriority="high"{% endif %}` to the first slide's image only (both mobile and desktop loops). The first slide is already eager (no `loading="lazy"`), so this satisfies the LCP-discovery insight without touching the lazy-loaded later slides.
- **Closes:** PERF-14 (the `fetchpriority=high should be applied` flag).

### Task E — SYS-9 · Referrer-Policy meta (SEC-1)
- **Where:** `layout/theme.liquid:7` head.
- **Fix:** add `<meta name="referrer" content="strict-origin-when-cross-origin">` — the theme-side mechanism Shopify allows for the Referrer-Policy.
- **Closes:** the Referrer-Policy half of SEC-1. **Permissions-Policy** has no meta equivalent and is platform/edge-controlled → deferred to a Shopify-support confirmation (named above).

## 3. Quality gates (from `DEVELOPMENT.md`)

The run's hard rule is **write only to GitHub** — Hobbes does **not** run the Shopify CLI / Theme Check / browser here; those gates are the human's at review. Each change is authored to pass them:
- **Theme Check:** no new offenses — edits are additive head/meta tags, an `<img>`-attribute swap, a new schema setting, and two `<meta>` blocks; no new Liquid risk, no `settings_data.json`. Bar is "no *new* offenses vs base" (the pre-existing `icon-shop-pay.liquid` error is out of scope).
- **Browser (human, at review):** verify mobile + desktop, no new console errors — hero logos still render full-width, the first hero slide still loads, and View-Source shows a `<meta name="description">`, `og:image`, `twitter:image`, and `<meta name="referrer">` on Home + a description-less collection.
- **Fork-safe:** self-contained head/snippet/section edits; the only CSS is in the Hazel-custom `component-hero.css`, not Dawn-core.
- **No baseline regression** against `baseline.md` targets.
- **No unnecessary comments**; matched the surrounding file style.

## 4. Todo

**Phase 1 — SYS-5 page metadata**
- [x] A1 · `theme.liquid` typed `meta_description` fallback chain + emit + pass to `meta-tags` (SEO-1)
- [x] B1 · `meta-tags.liquid` `og_image` fallback (`page_image`→`share_image`→`logo`), 1200-wide OG image tags (SEO-4)
- [x] B2 · `meta-tags.liquid` add `twitter:image` (SEO-4)
- [x] B3 · `settings_schema.json` add `share_image` image-picker to the social-media group

**Phase 2 — SYS-6 image delivery (code half)**
- [x] C1 · `hero.liquid` real intrinsic dims on both hero logos (PERF-12, BP-3)
- [x] C2 · `component-hero.css` `.hero-logo img { width:100%; height:auto }` to preserve display sizing
- [x] D1 · `hero.liquid` `fetchpriority="high"` on first slide image, mobile + desktop (PERF-14)

**Phase 3 — SYS-9 security header (code half)**
- [x] E1 · `theme.liquid` `<meta name="referrer" content="strict-origin-when-cross-origin">` (SEC-1 Referrer-Policy)

**Phase 4 — handoff**
- [x] H1 · branch `hobbes-fix-2026-06-21`, commit, push
- [x] H2 · open PR with before/after + deferrals; stop (no publish)

## 5. Handoff — before/after for the PR

**Before (this cycle's measured live state, from `baseline.md` / `findings.md`):**
- SEO-1 missing meta descriptions — **76 of 185** pages (incl. golden Home + Collection); baseline §E Home/Collection ✗. Target: every page.
- SEO-4 OG/Twitter — **43 of 185** pages missing `og:title`/`og:image`; golden Home missing `og:image`; no `twitter:image` sitewide. Target: OG/Twitter present, all pages.
- PERF-12 unsized images — flagged on 3 pages (the two brand logos). Target: explicit width/height.
- BP-3 image aspect-ratio — `script-logo.png`, `hazel-mobile-logo.png`. Target: 0 (Best Practices ≥ 95).
- PERF-14 LCP discovery — `fetchpriority=high should be applied`, 3 pages. Target: applied (Performance ≥ 90).
- SEC-1 security headers — Referrer-Policy ✗ (and Permissions-Policy ✗). Target: present.
- Golden SEO scores: 92 across all six page/device runs (§A). Target: ≥ 95.

**After (measured):** comes post-publish, by necessity — PSI and the crawl only measure the live site, and the fix isn't live until a human publishes. The true after lands in the next cycle's `diff.md`; link it back to this PR to close the loop. No after is fabricated here.

**Shipped this PR (theme code):** SYS-5 meta-description + OG/Twitter image fallbacks (+ `share_image` setting), SYS-6 hero-logo dims + LCP `fetchpriority`, SYS-9 Referrer-Policy meta.
**Already in `main` (06-20 PR, awaiting publish):** SYS-1 slideshow/pagination labels, SYS-2 nested-heading, SYS-3 card-image alt fallback.
**Deferred (named in §1):** SYS-4 Mailchimp (human), SYS-7 app JS (human coordination), SYS-8 + SYS-2 reorder (browser-gate), SEO-5/6 duplicate copy + image re-exports + meaningful alt (content), SEC-1 Permissions-Policy (platform).
