# Plan — 2026-07-03-A

Site: https://hazelboutique.com/ · Cycle: 2026-07-03-A · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

This groups the cycle's **28 findings** into systems, rates each (effort against `DEVELOPMENT.md`/`CONTEXT.md`, impact against `MISSION.md`), and orders by leverage. The facts are the findings; the effort/impact calls are mine.

## The state this cycle measures — read before rating

Another re-measurement cycle. **Both priority gaps are met on the golden path**, same as the last three cycles — but this cycle's crawl pins two things the prior ones left as counts-only, and one of them is a genuine first-party code lever.

- **Accessibility = 100 on all six golden runs, axe failing audits = 0 everywhere** (§A, §D). Priority 1 met on the golden path. What's left is one off-path product page (`A11Y-1`) and the standing manual §G sign-off.
- **SEO = 100 on all six runs, full golden checklist passes except image-alt** (§A, §E). The one golden image `seo.py` flags is `59C10513-…png?…&width=32` — the cursor follower at `layout/theme.liquid:491-498`. Jenna swapped the admin image (last cycle it was `IMG_3438.png`), but the element is unchanged and **still correctly decorative**: `alt="" aria-hidden="true" width="32" height="32"`. SiteOne's sitewide alt count corroborates — 0 broad code-owned alt gap. So `SEO-1` is again a measurement artifact.
- **Performance fails the lab (mobile 41–53) but the field passes.** CrUX is "good" on LCP/INP/CLS for all three golden pages (§C, all ✓). Per the rubric, a lab gap where real users already pass is low impact. The one first-party perf slice a prior cycle found — the cart-drawer upsell image — is **already in `main`** (`snippets/cart-drawer.liquid:26,37`, sized `&width=400` + intrinsic dimensions); the rest of the weight is third-party / content / platform.

What the sweep established this cycle (so the calls are evidenced, not assumed):

- **Every template-rendered `<img>` carries an `alt` attribute.** A regex sweep for `<img` without `alt=` across all `*.liquid` returns **zero** matches; `product-media.liquid` emits `alt="{{ media.alt | escape }}"` (lines 33, 75). So `A11Y-1`'s 2 missing-alt images on `/products/the-miss-honey-pillow` — the **only** page the 178-page crawl flags — are not template. That page renders `{{ product.description }}` raw (`sections/main-product.liquid:175`); the two bare `<img>` live in the admin rich-text description Jenna wrote. **Content-owned, not code.**
- **The "Hazel Boutique" ×5 duplicate meta description (`SEO-2`) is partly code-authorable.** The 5 pages are `/` (index), `/blogs/news` (blog), and `/pages/divider`, `/pages/gift-certificates`, `/pages/swym-share-wishlist` (page type, blank `page.content`). They fall through the theme's custom meta-description chain (`layout/theme.liquid:26-44`) to the bare `shop.name` fallback because **no branch handles `blog`, and content-less `page` types have nothing to fall back to.** Collections already get a unique fallback there (line 32). Mirroring that pattern for `blog` and content-less `page` gives 4 of the 5 a unique, factual description. Home (`index`) needs an admin homepage SEO description — brand-visible copy Jenna owns, not invented in code.
- **The §F "multiple H1 = 1 / skipped heading = 1" flags are not reproducible from the authoritative heading dump.** All 178 rows in the crawl's `seo-headings` table show exactly one H1 and no skipped level (verified programmatically). These are SiteOne summary-count borderline, not a code target — and they carry no finding ID in `02-evaluation.md`, so they're context, not a system.
- **Security response headers stay platform-controlled.** `<meta name="referrer">` is in `main` (`layout/theme.liquid:8`); it does not set the response header SiteOne measures, and `Permissions-Policy` has no meta form. `SEC-1`/`SEC-2` are not theme-authorable.

So the leverage is narrow but — unlike the last cycle, which had only the already-merged cart-upsell slice — there is **one clean, safe, first-party code lever this cycle**: the meta-description fallback. It ships. Everything else is content, platform, third-party, or a measurement artifact.

---

## Systems

### SYS-1 · Meta-description uniqueness — code fallback + product/home content
- **Findings:** SEO-2
- **The system:** 8 duplicated meta descriptions. Two causes. (a) **Code:** the "Hazel Boutique" ×5 group is 5 pages hitting the theme's bare `shop.name` fallback (`layout/theme.liquid:26-44`) — `/blogs/news` (no `blog` branch), three content-less `/pages/*`, and `/` (index). Four of these are fixable in the theme by mirroring the collection fallback already in that block. (b) **Content:** the remaining 7 duplicated descriptions (EVI11 vintage ×5, ornaments ×2, tanks ×2, earrings ×2, joggers ×2, necklaces ×2, jackets ×2) are identical **admin `product.description` copy** shared across product families — Shopify emits them verbatim; only unique copy fixes them. Plus the home page needs an admin homepage SEO description.
- **Effort:** 2/5 — the code slice is one self-contained edit to an already-custom block in `layout/theme.liquid` (no core-file risk, mirrors an existing pattern), owner: code/Hobbes. The content slice (unique product descriptions + home SEO) is separate work owned by Britni/Jenna (`CONTEXT.md`).
- **Impact:** 3/5 — Priority 2 (full SEO checklist). Measurable: the code slice de-duplicates 4 pages immediately; the finding is a snippet-quality nuance, not an indexability blocker, so not a 5.
- **Priority:** 3/2 = **1.5** — **ships the code slice this cycle**

### SYS-2 · Image alt — content gap + decorative artifact
- **Findings:** A11Y-1, SEO-1
- **The system:** The image-alt domain, spanning A11Y and SEO. Two distinct sub-cases, both established from source. (a) **A11Y-1 — real content gap:** 2 `<img>` without alt on `/products/the-miss-honey-pillow`, the only page the crawl flags. Template images all carry `alt` (sweep = zero gaps), so these are embedded in the admin product description (`{{ product.description }}`). Fixing them means adding alt in the admin — **content, owner: Jenna/Britni**. (b) **SEO-1 — measurement artifact:** the golden-path flag is the decorative cursor follower (`mouse_image`, `layout/theme.liquid:491-498`), correctly `alt="" aria-hidden="true"`. Adding descriptive alt would *harm* a11y — **won't-fix**.
- **Effort:** 2/5 — A11Y-1 is admin content on one product (small), owner Jenna/Britni; pinning the exact two images needs the rendered page/admin (a browser task at review). SEO-1 needs no action.
- **Impact:** 2/5 — Priority 1, but the golden path already passes a11y fully (axe 0, score 100). A11Y-1 is one off-path product page; SEO-1 closes nothing real.
- **Priority:** 2/2 = **1.0** — A11Y-1 → content handoff; SEO-1 → won't-fix

### SYS-3 · Performance — lab gap, field passing
- **Findings:** PERF-1, PERF-2, PERF-3, PERF-4, PERF-5, PERF-6, PERF-7, PERF-8, PERF-9, PERF-10, PERF-11, PERF-12, PERF-13, PERF-14, PERF-15, PERF-16, PERF-17, PERF-18
- **The system:** The whole performance domain. Lab fails on mobile (41–53) but **the field passes** on every golden page (§C). The weight is not first-party theme code: third-party scripts (`shopify.widget.js`, `protect.widget.js`/`protect.core.js` = Route Insurance, `da-restock.js`, Instafeed, GA, Meta Pixel — PERF-3/4/6/13/16), content images incl. HEIC source files needing re-export (PERF-2/5), platform-controlled minify/cache/duplicate-JS (PERF-4/13/14/16), render-blocking core `base.css` (PERF-12, a critical-path change that risks FOUC if done blind), layout shifts whose lab values are wildly inflated vs the passing field (PERF-9/10/11), and main-thread / reflow / dependency-tree / slowest-URL items (PERF-7/8/17/18) originating in third-party and platform code. The two highest-leverage moves stay owner-gated: **remove Route Insurance** (`DEVELOPMENT.md` flags it) and **re-export the HEIC images**. The one first-party code slice a prior cycle carved — the cart-drawer upsell image — is **already merged in `main`**. No first-party code gap remains this cycle.
- **Effort:** 5/5 — integration removal + coordination, content re-exports at scale, platform assets, core/critical-path risk. Owners: Mason (Route removal, platform), Britni/Jenna (image re-export). Not closeable in a GitHub-only run.
- **Impact:** 2/5 — Priority 3, but the **field already passes**, so the lab gap costs little for real users. Rated 2 on the field-vs-lab reality.
- **Priority:** 2/5 = **0.4** — full handoff

### SYS-4 · Security response headers — platform
- **Findings:** SEC-1, SEC-2
- **The system:** Referrer-Policy and Permissions-Policy response headers absent (SEC-1); CDN assets carry `Access-Control-Allow-Origin: *` (SEC-2). On Shopify the storefront **cannot set arbitrary response headers from the theme** — platform-controlled. The code-authorable partial (`<meta name="referrer">`) is **already in `main`** and does not set the response header measured; `Permissions-Policy` has no meta form. The CDN `ACAO: *` is expected and benign for public static assets.
- **Effort:** 4/5 — platform config, owner: Mason / Shopify. Not theme-authorable to the measured target.
- **Impact:** 2/5 — security isn't a named Top-3 priority, and the CORS item is benign.
- **Priority:** 2/4 = **0.5** — platform handoff

### SYS-5 · Best-practices, console & inline SVG — third-party / benign
- **Findings:** BP-1, BP-2, BP-3, BP-4, BP-5
- **The system:** Console errors are third-party/network — `ERR_BLOCKED_BY_CLIENT` (visitor ad blocker), 400/403 from embeds, a `shop.app` CSP frame-ancestors notice (BP-1) — none first-party. Inspector issues (BP-2) need the rendered DOM. Duplicate inline SVG (BP-3, `icon-plus` ×12) is one centralised snippet (`snippets/icon-plus.liquid`) inlined per call site; the source is already DRY, and a `<use>`/sprite refactor is invasive across the Dawn fork for a `0 critical` cosmetic count. WebP/AVIF "support" (BP-4/5) is Shopify CDN content-negotiation, not a theme setting.
- **Effort:** 3/5 — mixed: third-party (no action), rendered-DOM-gated, or platform. Owner: Mason at review for the SVG partial if ever pursued.
- **Impact:** 1/5 — Best Practices isn't a Top-3 priority; benign or third-party.
- **Priority:** 1/3 = **0.3** — handoff / won't-chase

---

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Meta-description uniqueness | 3 | 2 | **1.5** | One safe theme edit de-duplicates 4 pages; mirrors an existing fallback — **ships this cycle** |
| 2 | SYS-2 · Image alt | 2 | 2 | 1.0 | A11Y-1 = product-description content (Jenna); SEO-1 = decorative artifact (won't-fix) |
| 3 | SYS-4 · Security response headers | 2 | 4 | 0.5 | Platform-controlled; referrer meta already in code — Mason/Shopify |
| 4 | SYS-3 · Performance (lab gap, field passing) | 2 | 5 | 0.4 | Field passes; cart-upsell slice already in `main`, rest owner-gated |
| 5 | SYS-5 · Best-practices / console / inline SVG | 1 | 3 | 0.3 | Third-party / benign / rendered-DOM-gated |

Every one of the 28 findings lands in exactly one system: SEO-2 → SYS-1; A11Y-1, SEO-1 → SYS-2; PERF-1…18 → SYS-3; SEC-1, SEC-2 → SYS-4; BP-1…5 → SYS-5. None dropped, none invented. (The §F multiple-H1 / skipped-heading / aria-label counts carry no finding ID in `02-evaluation.md` and are unreproducible from the authoritative heading dump / off the golden path — context, not systems.)

## The handoff

Execution draws the budget line on this order. Unlike the last three re-measurement cycles, there is a real first-party code lever this cycle — **SYS-1's meta-description fallback** — so execution ships that slice and hands off the rest: SYS-1's content half (product descriptions + home SEO), SYS-2 (A11Y-1 product-description alt as content; SEO-1 won't-fix), SYS-3 (integration + content + platform), SYS-4 (platform), SYS-5 (third-party/benign). The code batch is thin because that is the truth of the site — the a11y/SEO priorities are met on the golden path, perf passes for real users, and the residue needs hands a GitHub-only cycle doesn't have — not because buildable work was left on the table.
