# Plan — 2026-06-30-A

Site: https://hazelboutique.com/ · Cycle: 2026-06-30-A · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

This groups the cycle's **28 findings** into systems, rates each (effort against `DEVELOPMENT.md`/`CONTEXT.md`, impact against `MISSION.md`), and orders by leverage. The facts are the findings; the effort/impact calls are mine.

## The state this cycle measures — read before rating

This is another re-measurement cycle, and **both priority gaps are met on the golden path.** Same shape as 2026-06-26-B, with that cycle's collection-LCP fix now merged in `main`.

- **Accessibility = 100 on all six golden runs, axe failing audits = 0 everywhere** (§A, §D). Priority 1 is met on the golden path. What's left is off-path crawl residue (`A11Y-1`) and the standing manual §G sign-off.
- **SEO = 100 on all six runs, full golden checklist passes except image-alt** (§A, §E). The one image `seo.py` still flags on all three golden pages is `IMG_3438.png?v=…&width=32` — the 32px cursor follower at `layout/theme.liquid:491-498`, which already carries `alt="" aria-hidden="true" width="32" height="32"`. I read the source: it is **correctly decorative**. SiteOne's sitewide alt count is clean (`Missing image alt attributes: 0 warning / 1741 ok`, `raw/crawl.json`). So image-alt is a measurement artifact, not a gap.
- **Performance fails in the lab (mobile 40–47) but the field passes.** CrUX is "good" on LCP/INP/CLS for all three golden pages (§C: Home LCP 1.756s/INP 106/CLS 0.09 · Collection 0.721s/77/0.01 · Product 1.128s/104/0.0, all ✓). Per the plan rubric, a lab gap where real users already pass is low impact. The pass bar is still lab ≥ 90, but the weight is overwhelmingly third-party / content / platform, not first-party theme code — and the one clean first-party perf lever the last cycle found (collection LCP hint) is already in `main`.

So the leverage this cycle is narrow and honest. I dropped to `raw/` and swept the codebase to pin what is **both code-authorable in a GitHub-only run and currently wrong in `main`**. One thing qualifies: a first-party cart-drawer upsell image pulled at full resolution and rendered without intrinsic dimensions. Everything else is owner-gated (content, integration, platform, rendered-DOM) or a measurement artifact.

What the sweep established (so the deferrals are evidenced, not assumed):
- **Icon-only controls** across `sections/`, `snippets/`, `blocks/` all carry an accessible name (aria-label / visually-hidden text) — pagination, share, quantity steppers, drawer close, header drawer. The single `A11Y-1` "unnamed links/buttons" warning is **not** in first-party theme controls; off the golden path (axe golden = 0); unlocated by the crawl (the accessibility table is counts-only — `_detail` holds only best-practices and security). Pinning it needs the rendered DOM.
- **Referrer hardening is already in code** — `layout/theme.liquid:8` already carries `<meta name="referrer" content="strict-origin-when-cross-origin">`. The `SEC-1` response-header target is platform-controlled regardless, and `Permissions-Policy` cannot be set from a meta tag at all.
- **`icon-plus` is already centralised** in one snippet (`snippets/icon-plus.liquid`) rendered at six call sites. `BP-3`'s "duplicate inline SVG" is the *rendered* HTML inlining that snippet per use; the source is already DRY. A `<symbol>`/`<use>` sprite refactor is invasive across the Dawn fork for a `0 critical` cosmetic count — not a safe blind ship.
- **The full-resolution image waste is real but small.** Live JS-injected first-party images: the footer "Recently viewed" carousel (`sections/footer.liquid:35`) already constrains to `image_url: width: 600` and sits in a `.ratio` wrapper that reserves layout. The orphaned `snippets/recent-viewed-product-js.liquid` is entirely wrapped in `{% comment %}` — dead code, renders nothing. The **cart-drawer upsell** (`snippets/cart-drawer.liquid:35`) was the lone exception: `src="${product.images[0]}"` is the full original image dropped into a box rendered at 25% drawer width, with no `width`/`height`. That is the one code-authorable slice.

---

## Systems

### SYS-1 · Performance — lab gap, field passing
- **Findings:** PERF-1, PERF-2, PERF-3, PERF-4, PERF-5, PERF-6, PERF-7, PERF-8, PERF-9, PERF-10, PERF-11, PERF-12, PERF-13, PERF-14, PERF-15, PERF-16, PERF-17, PERF-18
- **The system:** The whole performance domain. Lab fails on mobile (40–47) but **the field passes** on every golden page (§C). The weight is not first-party theme code: third-party scripts (`shopify.widget.js`, `protect.widget.js`/`protect.core.js` = Route Insurance, `da-restock.js`, Instafeed, GA, Meta Pixel, Fera — PERF-3/4/6/11/13/16), content images incl. HEIC source files that need re-export (`image_*.heic` — PERF-2/5), platform-controlled minify/cache/duplicate-JS (PERF-4/13/14/16), render-blocking core `base.css` (PERF-12, a critical-path change that risks FOUC if done blind), layout shifts whose lab values are wildly inflated vs the passing field (PERF-8/10), and main-thread / reflow / dependency-tree / slowest-URL items (PERF-7/9/17/18) originating in third-party and platform code. The two highest-leverage moves are owner-gated: **remove Route Insurance** (`DEVELOPMENT.md` flags it for removal — an app uninstall, not theme code) and **re-export the HEIC images** to web formats (content/admin). The one first-party slice that is code-authorable and was wrong in `main` is the **cart-drawer upsell image** (`snippets/cart-drawer.liquid:35`): full-resolution `product.images[0]` into a 25%-width box, no intrinsic dimensions — the image-delivery (PERF-2) and layout-shift (PERF-8/10) *class*, in code we own. (PSI measures an empty cart, so this never appears in the golden-path evidence; the benefit lands for real users who have items in cart — i.e. exactly where the field measures.) That slice ships this cycle; the rest hands off.
- **Effort:** 5/5 — long, spans an integration removal + coordination, content re-exports at scale, platform-controlled assets, and core/critical-path risk. Owners: Mason (Route removal, app/platform), Britni/Jenna (image re-export). Not closeable in a GitHub-only run. (The carved cart-upsell slice alone is a 1 — two-line, self-contained, additive.)
- **Impact:** 2/5 — Priority 3, but the **field already passes**, so the lab gap costs little in practice. Rated 2 on the field-vs-lab reality even though the lab number looks alarming.
- **Priority:** 2/5 = **0.4**

### SYS-2 · Duplicate meta descriptions — content
- **Findings:** SEO-2
- **The system:** 5 duplicated descriptions (SEO-2): the shop-name fallback "Hazel Boutique" ×5 on description-less pages, and templated/identical copy on the EVI11 vintage line and bracelet pairs. The duplicates are **admin copy**, not template logic — Shopify emits the per-resource description from the admin, falling back to the shop name where none exists. The fix is writing unique descriptions, not changing code.
- **Effort:** 3/5 — content at scale, owner: Britni / Jenna (`CONTEXT.md`). No code path a blind change improves without risking worse generic copy. Not authorable in a GitHub-only run.
- **Impact:** 2/5 — Priority 2, but SEO is already 100 and duplicate descriptions are a snippet-quality nuance, not an indexability blocker.
- **Priority:** 2/3 = **0.7**

### SYS-3 · Image-alt residue — decorative artifact (won't-fix)
- **Findings:** SEO-1
- **The system:** `seo.py` counts an empty `alt` as missing. The only image still flagged on all three golden pages is `IMG_3438.png?v=…&width=32` — the 32px cursor follower at `layout/theme.liquid:491-498`, already `alt="" aria-hidden="true" width="32" height="32"` and **correctly decorative**. Adding descriptive alt would *harm* a11y. SiteOne's sitewide alt count is clean (0 warning / 1741 ok, `raw/crawl.json`), confirming no broader code-owned alt gap.
- **Effort:** 1/5 — no code action; it is a measurement artifact. (Closeable only by teaching `seo.py` to ignore `aria-hidden` empty-alt images — tool work, out of this cycle's scope.)
- **Impact:** 1/5 — SEO is already 100; this closes nothing real.
- **Priority:** 1/1 = **1.0** (won't-fix — no storefront change)

### SYS-4 · Sitewide a11y crawl residue — off golden path
- **Findings:** A11Y-1
- **The system:** SiteOne flags 10 "HTML structural" warnings and 1 "unnamed links/buttons" across 179 pages (`raw/crawl.json` accessibility table). These are **off the golden path** — axe via PSI reads 0 on all six golden runs and a11y scores 100, so none sit on Home/Collection/Product. The captured data gives **counts only — no element or URL pinned** (the crawl's `_detail` holds only best-practices and security; the accessibility rows are summaries). I swept every icon-only `<button>`/`<a>` in first-party theme code and all carry an accessible name, so the one unnamed control is most likely a third-party embed or an off-path template the crawl reached but the capture didn't locate. Pinning it, or a duplicated id, needs the **rendered DOM** a GitHub-only run doesn't have; fixing duplicate IDs blind across a shared snippet risks breaking working ARIA wiring for a count axe doesn't even flag.
- **Effort:** 3/5 — bucket 3: needs the rendered DOM to know which element/file to change, owner: Mason at review. Low code risk once located, but it can't be located from source alone.
- **Impact:** 2/5 — Priority 1, but the golden path already passes a11y fully; this is residual off-path hygiene, not a user-facing golden gap.
- **Priority:** 2/3 = **0.7**

### SYS-5 · Security response headers — platform
- **Findings:** SEC-1, SEC-2
- **The system:** Referrer-Policy and Permissions-Policy response headers are absent (SEC-1), and CDN assets carry `Access-Control-Allow-Origin: *` (SEC-2). On Shopify the storefront **cannot set arbitrary response headers from the theme** — these are platform-controlled. The code-authorable partial hardening (`<meta name="referrer">`) is **already in `main`** (`layout/theme.liquid:8`), and it does not set the *response header* SiteOne measures; `Permissions-Policy` has no meta-tag form at all. The CDN `ACAO: *` is expected and benign for public static assets.
- **Effort:** 4/5 — platform config, owner: Mason / Shopify platform. Not theme-authorable to the measured target.
- **Impact:** 2/5 — security isn't a named Top-3 priority, and the CORS item is benign. Real but low against the mission.
- **Priority:** 2/4 = **0.5**

### SYS-6 · Best-practices, console & inline SVG — third-party / benign
- **Findings:** BP-1, BP-2, BP-3, BP-4, BP-5
- **The system:** Console errors are third-party/network — `ERR_BLOCKED_BY_CLIENT` (the visitor's ad blocker), Monorail 400/429 (Shopify analytics rate-limit), 400s from embeds (BP-1) — none first-party. Inspector issues (BP-2) need the rendered DOM. Duplicate inline SVG (BP-3, `icon-plus` ×9) is one centralised snippet inlined per call site; the source is already DRY and converting to a `<use>`/sprite is invasive across the Dawn fork and risks breaking icons sitewide for a `0 critical` cosmetic count. WebP/AVIF "support" (BP-4/5) is Shopify CDN content-negotiation, not a theme setting.
- **Effort:** 3/5 — mixed: third-party (no action), rendered-DOM-gated, or platform. Owner: Mason at review for the SVG partial if ever pursued.
- **Impact:** 1/5 — Best Practices isn't a Top-3 priority; these are benign or third-party. Lowest mission weight.
- **Priority:** 1/3 = **0.3**

---

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-3 · Image-alt residue | 1 | 1 | **1.0** | Won't-fix — decorative cursor follower, confirmed correct in source |
| 2 | SYS-2 · Duplicate meta descriptions | 2 | 3 | 0.7 | Content at scale — Britni/Jenna |
| 3 | SYS-4 · Sitewide a11y crawl residue | 2 | 3 | 0.7 | Off-path; needs rendered DOM to pin — Mason at review |
| 4 | SYS-5 · Security response headers | 2 | 4 | 0.5 | Platform-controlled; referrer meta already in code — Mason/Shopify |
| 5 | SYS-1 · Performance (lab gap, field passing) | 2 | 5 | 0.4 | Field passes; one first-party code slice (cart-upsell image) ships, rest owner-gated |
| 6 | SYS-6 · Best-practices / console / inline SVG | 1 | 3 | 0.3 | Third-party / benign / rendered-DOM-gated |

Every one of the 28 findings lands in exactly one system: PERF-1…18 → SYS-1; SEO-2 → SYS-2; SEO-1 → SYS-3; A11Y-1 → SYS-4; SEC-1/SEC-2 → SYS-5; BP-1…5 → SYS-6. None dropped, none invented.

## The handoff

Execution draws the budget line on this order. The leverage ranking puts the won't-fix and the owner-gated systems at the top because the priority work is already met on the golden path — the ordering is honest, not a queue of buildable work. The **only** thing both code-authorable in a GitHub-only run and currently wrong in `main` is the cart-drawer upsell image inside SYS-1, so execution ships that slice and hands off SYS-2 (content), SYS-4 (rendered-DOM a11y), SYS-5 (platform), the rest of SYS-1 (integration + content + platform), and SYS-6 (third-party/benign) as PR to-dos with owners. The thin code batch is the truth of the site, not caution: the a11y/SEO priorities are in `main`, perf passes for real users, and the remainder needs hands a GitHub-only cycle doesn't have.
</content>
</invoke>
