# Plan — 2026-06-26-A

Site: https://hazelboutique.com/ · Cycle: 2026-06-26-A · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

This groups the cycle's **29 findings** into systems, rates each (effort against `DEVELOPMENT.md`/`CONTEXT.md`, impact against `MISSION.md`), and orders by leverage. The facts are the findings; the effort/impact calls are mine.

## The state this cycle measures

Read the baseline before rating anything: **this is largely a re-measurement cycle, and the priority gaps are mostly closed.**

- **A11Y = 100 on all six golden runs, axe failing audits = 0 everywhere** (§A, §D). The code-owned a11y work shipped in the two 2026-06-25 cycles (PRs #27, #31) is holding in `main`. Priority 1 is effectively met on the golden path; what remains is off-path crawl warnings and the standing manual §G sign-off.
- **SEO = 100 on all six runs, full golden checklist passes except image-alt** (§A, §E). Priority 2 is met but for one row.
- **Performance fails in the lab (mobile 50–57) but the field passes** — CrUX is "good" on LCP/INP/CLS for Home, Collection, and Product (§C). Per the plan rubric, a lab-only perf gap where real users already pass is low impact.

So the leverage this cycle is narrow and honest: **one code-authorable SEO gap**, then a stack of owner-gated work (content, integration, platform, browser) that a GitHub-only run can't close.

---

## Systems

### SYS-1 · Cart-drawer collection image — empty alt
- **Findings:** SEO-1 (code portion)
- **The system:** `seo.py` counts an empty `alt` as missing (`02-evaluation.md` SEO-1; tool logic `hobbes/tools/seo.py:111-113`). Two images flag on every golden page because both are sitewide elements rendered in `layout/theme.liquid` and the cart drawer:
  - **`cart_drawer_collection_image_two`** (`IMG_2024-05-08-170032.jpg`, 1500w) renders through `snippets/card-collection.liquid:71` as `alt="{{ placeholder_image.alt | escape }}"`. The image's admin alt field is blank → `alt=""` → flagged. This is a **real gap** (SiteOne's sitewide alt count is clean at 1738 ok / 0 warning because it tolerates empty alt — but the empty alt is still poor SEO/a11y). One template fallback to the collection title closes it for the image and every other `card-collection` placeholder render in one place.
  - **`mouse_image`** (`IMG_3438.png`, 32px cursor follower) renders at `layout/theme.liquid:491-498` and *already* carries `alt="" aria-hidden="true"` — **correctly decorative**. seo.py flags it only because it counts empty alt. Adding descriptive alt would be wrong a11y. **Won't-fix: measurement artifact, leave as-is.** (Same conclusion the 2026-06-25-B cycle reached.)
- **Effort:** 1/5 — code, one line in `snippets/card-collection.liquid`, self-contained, upgrade-safe, owner: Mason. Byte-identical pattern to PR #27's card-product/multicolumn alt fallbacks. No browser needed to write; needs a browser only to confirm the alt now reads present.
- **Impact:** 3/5 — advances Priority 2 (SEO checklist: the only failing golden row), and improves real a11y on the cart drawer. Clears the one *code-owned* half of SEO-1 on all three golden pages. Capped at 3, not 5, because the other flagged image is a won't-fix artifact and SEO is already at 100 — this closes a checklist row, not a score gap.
- **Priority:** 3/1 = **3.0**

### SYS-2 · Duplicate meta descriptions — content
- **Findings:** SEO-2
- **The system:** 5 duplicated descriptions (`02-evaluation.md` SEO-2): the shop-name fallback "Hazel Boutique" ×5 on description-less pages, and templated/identical product copy on the EVI11 vintage line and bracelet pairs. The duplicates are **admin copy**, not template logic — Shopify emits the per-resource description set in the admin, falling back to the shop name only where none exists. The fix is writing unique descriptions, not changing code.
- **Effort:** 3/5 — content at scale, owner: Britni / Jenna (`CONTEXT.md`). No code path that a blind change improves without risking worse generic descriptions. Not authorable in a GitHub-only run.
- **Impact:** 2/5 — Priority 2, but SEO is already 100 and duplicate descriptions are a snippet-quality nuance, not an indexability blocker. Small real-user effect.
- **Priority:** 2/3 = **0.7**

### SYS-3 · Sitewide a11y crawl residue — off golden path
- **Findings:** A11Y-1
- **The system:** SiteOne flags 10 "HTML structural" warnings and 1 "unnamed link/button" across 179 pages (`02-evaluation.md` A11Y-1; `raw/crawl.json` accessibility table — counts only, no element pinned). These are **off the golden path** — axe via PSI reads 0 on all six golden runs and a11y scores 100, so none of these sit on Home/Collection/Product. They are counts without a located element; pinning the one unnamed link or the structural warnings needs the **rendered DOM**, which a GitHub-only run doesn't have.
- **Effort:** 3/5 — bucket 3: needs the rendered DOM to even know which element/file to change, owner: Mason at review. Low code risk once located, but it can't be located from source alone.
- **Impact:** 2/5 — Priority 1, but the golden path already passes a11y fully; this is residual off-path hygiene, not a user-facing golden gap.
- **Priority:** 2/3 = **0.7**

### SYS-4 · Performance — third-party / content / platform
- **Findings:** PERF-1 … PERF-18
- **The system:** The whole performance domain. The lab score fails on mobile (50–57) but **the field passes** — CrUX LCP/INP/CLS are all "good" on every golden page (§C). The weight is overwhelmingly **not first-party theme code**: third-party scripts (`shopify.widget.js`, `protect.widget.js`/`protect.core.js` = Route Insurance, `da-restock.js`, Instafeed, GA, Meta Pixel — PERF-3/4/6/12), HEIC source images that need re-export (`image_*.heic` — PERF-2/5), platform CSS/JS minification and caching the theme doesn't control (PERF-3/9/14/15), and render-delay/LCP-discovery items (PERF-11/16) that need the rendered DOM to target safely. The two highest-leverage moves are both owner-gated: **remove Route Insurance** (`DEVELOPMENT.md` flags it for removal — an app uninstall, not theme code) and **re-export the HEIC images** to web formats (content/admin). `fetchpriority=high` on the LCP image (PERF-16) is the one arguably code-authorable item, but choosing the LCP element blind risks promoting the wrong asset on a live store.
- **Effort:** 5/5 — long, spans an integration removal + coordination, content re-exports at scale, platform-controlled assets, and browser-gated targeting. Owners: Mason (Route removal, app/platform), Britni/Jenna (image re-export). Not closeable in a GitHub-only run.
- **Impact:** 2/5 — Priority 3, but **the field already passes for real users**, so the lab gap costs little in practice. Rated 2, not higher, on the field-vs-lab reality even though the lab number looks alarming.
- **Priority:** 2/5 = **0.4**

### SYS-5 · Security response headers — platform
- **Findings:** SEC-1, SEC-2
- **The system:** Referrer-Policy and Permissions-Policy headers are absent (SEC-1) and CDN assets carry `Access-Control-Allow-Origin: *` (SEC-2). On Shopify the storefront **cannot set arbitrary response headers from the theme** — these are platform-controlled. A `<meta name="referrer">` tag is a partial code-authorable hardening, but it does **not** set the response header SiteOne measures, and on a live revenue store it touches analytics/pixel referrer attribution — so it's a Mason decision, not a blind GitHub-only ship. The CDN `ACAO: *` is expected and benign for public static assets.
- **Effort:** 4/5 — platform config, owner: Mason / Shopify platform. Not theme-authorable to the measured target.
- **Impact:** 2/5 — security isn't a named Top-3 priority, and the CORS item is benign. Real but low against the mission.
- **Priority:** 2/4 = **0.5**

### SYS-6 · Best-practices & console notices — third-party / benign
- **Findings:** BP-1, BP-2, BP-3, BP-4, BP-5, BP-6
- **The system:** Console errors are third-party/network — `ERR_BLOCKED_BY_CLIENT` (the visitor's ad blocker), Monorail 400/429 (Shopify analytics rate-limit), 400s from embeds (BP-1) — none first-party. Inspector issues (BP-2) need the rendered DOM. Invalid/duplicate inline SVG (BP-3 ×10, BP-4 ×1) are sitewide warnings from a shared icon partial or third-party-injected markup, with no element pinned and `0 critical` — changing inline SVG blind across 179 pages risks breaking icons for a cosmetic best-practice count. WebP/AVIF "support" (BP-5/6) is Shopify CDN content-negotiation, not a theme setting.
- **Effort:** 3/5 — mixed: third-party (no action), rendered-DOM-gated, or platform. Owner: Mason at review for the SVG partial if pursued.
- **Impact:** 1/5 — Best Practices isn't a Top-3 priority; these are benign or third-party. Lowest mission weight.
- **Priority:** 1/3 = **0.3**

---

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Cart-drawer collection image alt | 3 | 1 | **3.0** | Only code-authorable gap; one-line title fallback closes the last failing golden SEO row, mirrors PR #27 |
| 2 | SYS-2 · Duplicate meta descriptions | 2 | 3 | 0.7 | Content at scale — Britni/Jenna |
| 3 | SYS-3 · Sitewide a11y crawl residue | 2 | 3 | 0.7 | Off-path, needs rendered DOM to pin — Mason |
| 4 | SYS-5 · Security response headers | 2 | 4 | 0.5 | Platform-controlled — Mason/Shopify |
| 5 | SYS-4 · Performance | 2 | 5 | 0.4 | Field passes; Route removal + HEIC re-export — Mason + content |
| 6 | SYS-6 · Best-practices / console notices | 1 | 3 | 0.3 | Third-party / benign — mostly no action |

Every one of the 29 findings lands in exactly one system: SEO-1 → SYS-1; SEO-2 → SYS-2; A11Y-1 → SYS-3; PERF-1…18 → SYS-4; SEC-1/SEC-2 → SYS-5; BP-1…6 → SYS-6. None dropped, none invented.

## The handoff

Execution draws the budget line on this order. Only **SYS-1** is code-authorable in a GitHub-only run; SYS-2 through SYS-6 are owner-gated (content, integration, platform, rendered-DOM) and hand off as PR to-dos. The thin code batch is honest, not lazy — the a11y/SEO priority work is already in `main` and the rest needs hands a GitHub-only cycle doesn't have.
