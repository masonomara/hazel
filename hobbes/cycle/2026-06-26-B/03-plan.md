# Plan — 2026-06-26-B

Site: https://hazelboutique.com/ · Cycle: 2026-06-26-B · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

This groups the cycle's **27 findings** into systems, rates each (effort against `DEVELOPMENT.md`/`CONTEXT.md`, impact against `MISSION.md`), and orders by leverage. The facts are the findings; the effort/impact calls are mine.

## The state this cycle measures

Read the baseline before rating anything: **this is a re-measurement cycle, and the two priority gaps are met on the golden path.**

- **A11Y = 100 on all six golden runs, axe failing audits = 0 everywhere** (§A, §D). Priority 1 is met on the golden path. What remains is off-path crawl residue (`A11Y-1`) and the standing manual §G sign-off.
- **SEO = 100 on all six runs, full golden checklist passes except image-alt** (§A, §E). And the one image-alt case is now down to a **single decorative element**: the prior cycle's cart-drawer placeholder-alt fix (PR for 2026-06-26-A) is merged in `main` — `snippets/card-collection.liquid:71` already carries `default: card_collection.title`. The only image `seo.py` still flags is `IMG_3438.png` (the 32px cursor follower), which is correctly `alt="" aria-hidden="true"`. That is a measurement artifact, not a gap.
- **Performance fails in the lab (mobile 42–53) but the field passes** — CrUX is "good" on LCP/INP/CLS for Home, Collection, and Product (§C: Collection field LCP 0.719s, INP 77ms, CLS 0.01). Per the plan rubric, a lab gap where real users already pass is low impact. The pass bar is still lab ≥ 90, but the weight is overwhelmingly third-party / content / platform, not first-party theme code.

So the leverage this cycle is narrow and honest. I dropped to `raw/` to pin the one perf finding that **is** first-party and code-authorable — **PERF-15**, the collection LCP image priority hint — and confirmed the rest is owner-gated (content, integration, platform, rendered-DOM).

What `raw/` confirmed for PERF-15 (`lcp-discovery-insight`, mobile, per page):
- **Home** — LCP = slideshow image; `eagerlyLoaded: true`, `priorityHinted: true`. ✓ already correct.
- **Product** — LCP = main product media; eager + priority-hinted. ✓ already correct.
- **Collection** — LCP = the **first product-card image**; `requestDiscoverable: true` but **`priorityHinted: false`** → "fetchpriority=high should be applied". ✗ — the one real gap. The grid already eager-loads the first two cards (`lazy_load: false`) but `card-product.liquid` emits no `fetchpriority`, so the LCP candidate is never priority-hinted.

---

## Systems

### SYS-1 · Collection LCP image — missing priority hint
- **Findings:** PERF-15
- **The system:** On the collection page the LCP element is the first product-card image (`raw/…all_hazel_brand-mobile.psi.json` → `lcp-discovery-insight`). `sections/main-collection-product-grid.liquid:125-129` already sets `lazy_load: false` for the first two cards (so the request is discoverable), but `snippets/card-product.liquid:80-99` has **no `fetchpriority` path at all** — eager, but never priority-hinted. PSI reports `priorityHinted: false`. One optional `preload` param on the card snippet, set for `forloop.index == 1` in the grid, emits `fetchpriority="high"` on exactly the LCP candidate. Home (slideshow) and Product (main media) are already priority-hinted, so this is the only page that needs it.
- **Effort:** 1/5 — code, two files, self-contained, owner: Mason. New optional param defaults to `false`, so no other `card-product` caller (search, related, featured, collage, recent-viewed) changes behavior. Upgrade-safe (additive, no core override removed). Writable from source; needs a browser/PSI only to confirm the hint reads and the score moves.
- **Impact:** 2/5 — Priority 3 (Performance), and it is the **only** code-authorable perf lever on the golden path. Capped at 2 because the **field already passes** for real users (CrUX Collection LCP 0.719s "good"), so the lab number overstates the real-user cost; one hint alone won't carry collection mobile 45→90. Real, correct, worth shipping — not a score-mover on its own.
- **Priority:** 2/1 = **2.0**

### SYS-2 · Performance — third-party / content / platform
- **Findings:** PERF-1, PERF-2, PERF-3, PERF-4, PERF-5, PERF-6, PERF-7, PERF-8, PERF-9, PERF-10, PERF-11, PERF-12, PERF-13, PERF-14, PERF-16, PERF-17
- **The system:** The rest of the performance domain. Lab fails on mobile (42–53) but **the field passes** on every golden page (§C). The weight is not first-party theme code: third-party scripts (`shopify.widget.js`, `protect.widget.js`/`protect.core.js` = Route Insurance, `da-restock.js`, Instafeed, GA, Meta Pixel, Fera — PERF-3/4/6/11/12), HEIC source images that need re-export (`image_*.heic` — PERF-2/5), platform-controlled minify/cache (PERF-13/14/4), render-blocking core `base.css` (PERF-10, a core/critical-path change that risks FOUC if done blind), and main-thread / reflow / dependency-tree items (PERF-7/8/16) that originate in third-party and platform code. The two highest-leverage moves are owner-gated: **remove Route Insurance** (`DEVELOPMENT.md` flags it for removal — an app uninstall, not theme code) and **re-export the HEIC images** to web formats (content/admin).
- **Effort:** 5/5 — long, spans an integration removal + coordination, content re-exports at scale, platform-controlled assets, and core/critical-path risk. Owners: Mason (Route removal, app/platform), Britni/Jenna (image re-export). Not closeable in a GitHub-only run.
- **Impact:** 2/5 — Priority 3, but the **field already passes**, so the lab gap costs little in practice. Rated 2 on the field-vs-lab reality even though the lab number looks alarming.
- **Priority:** 2/5 = **0.4**

### SYS-3 · Image-alt residue — decorative artifact (won't-fix)
- **Findings:** SEO-1
- **The system:** `seo.py` counts an empty `alt` as missing (`hobbes/tools/seo.py`). The only image still flagged on all three golden pages is `IMG_3438.png?v=…&width=32` — the 32px cursor follower at `layout/theme.liquid`, which already carries `alt="" aria-hidden="true"` and is **correctly decorative**. Adding descriptive alt would *harm* a11y. SiteOne's sitewide alt count is clean (`Missing image alt attributes: 0 warning / 1720 ok`, `raw/crawl.json`), confirming no broader code-owned alt gap. The cart-drawer placeholder image that the 2026-06-26-A cycle flagged is already fixed in `main`.
- **Effort:** 1/5 — no code action; it is a measurement artifact. (Could be closed by teaching `seo.py` to ignore `aria-hidden` empty-alt images, but that is tool work, not storefront work, and out of this cycle's scope.)
- **Impact:** 1/5 — SEO is already 100; this closes nothing real.
- **Priority:** 1/1 = **1.0** (won't-fix — no storefront change)

### SYS-4 · Duplicate meta descriptions — content
- **Findings:** SEO-2
- **The system:** 5 duplicated descriptions (`02-evaluation.md` SEO-2): the shop-name fallback "Hazel Boutique" ×5 on description-less pages, and templated/identical copy on the EVI11 vintage line and bracelet pairs. The duplicates are **admin copy**, not template logic — Shopify emits the per-resource description from the admin, falling back to the shop name where none exists. The fix is writing unique descriptions, not changing code.
- **Effort:** 3/5 — content at scale, owner: Britni / Jenna (`CONTEXT.md`). No code path a blind change improves without risking worse generic copy. Not authorable in a GitHub-only run.
- **Impact:** 2/5 — Priority 2, but SEO is already 100 and duplicate descriptions are a snippet-quality nuance, not an indexability blocker.
- **Priority:** 2/3 = **0.7**

### SYS-5 · Sitewide a11y crawl residue — off golden path
- **Findings:** A11Y-1
- **The system:** SiteOne flags 10 "HTML structural" warnings (the crawl log labels them "duplicate id / broken ARIA references") and 1 "unnamed links/buttons (icon-only without aria-label)" across 176 pages (`raw/crawl.json` accessibility table). These are **off the golden path** — axe via PSI reads 0 on all six golden runs and a11y scores 100, so none sit on Home/Collection/Product. The captured data gives **counts only — no element or URL pinned** (I checked `raw/crawl.json` results and `crawl-report.html`; the structural/unnamed detail is summarised, not located). Pinning the one unnamed control or a duplicated id needs the **rendered DOM**, which a GitHub-only run doesn't have. Fixing duplicate IDs blind across a shared snippet risks breaking working ARIA wiring for a count axe doesn't even flag.
- **Effort:** 3/5 — bucket 3: needs the rendered DOM to know which element/file to change, owner: Mason at review. Low code risk once located, but it can't be located from source alone.
- **Impact:** 2/5 — Priority 1, but the golden path already passes a11y fully; this is residual off-path hygiene, not a user-facing golden gap.
- **Priority:** 2/3 = **0.7**

### SYS-6 · Security response headers — platform
- **Findings:** SEC-1, SEC-2
- **The system:** Referrer-Policy and Permissions-Policy headers are absent, HSTS/CSP not set (SEC-1), and CDN assets carry `Access-Control-Allow-Origin: *` (SEC-2). On Shopify the storefront **cannot set arbitrary response headers from the theme** — these are platform-controlled. A `<meta name="referrer">` tag is a partial code-authorable hardening, but it does **not** set the response header SiteOne measures, and on a live revenue store it touches analytics/pixel referrer attribution — so it's a Mason decision, not a blind GitHub-only ship. The CDN `ACAO: *` is expected and benign for public static assets.
- **Effort:** 4/5 — platform config, owner: Mason / Shopify platform. Not theme-authorable to the measured target.
- **Impact:** 2/5 — security isn't a named Top-3 priority, and the CORS item is benign. Real but low against the mission.
- **Priority:** 2/4 = **0.5**

### SYS-7 · Best-practices, console & inline SVG — third-party / benign
- **Findings:** BP-1, BP-2, BP-3, BP-4, BP-5
- **The system:** Console errors are third-party/network — `ERR_BLOCKED_BY_CLIENT` (the visitor's ad blocker), Monorail 400/429 (Shopify analytics rate-limit), 400s from embeds (BP-1) — none first-party. Inspector issues (BP-2) need the rendered DOM. Duplicate inline SVG (BP-3, the `icon-plus` ×6-8 on product pages) is a shared icon partial inlined per use; converting to a `<use>`/sprite is invasive across the Dawn fork and risks breaking icons sitewide for a `0 critical` cosmetic count — not a safe blind ship. WebP/AVIF "support" (BP-4/5) is Shopify CDN content-negotiation, not a theme setting.
- **Effort:** 3/5 — mixed: third-party (no action), rendered-DOM-gated, or platform. Owner: Mason at review for the SVG partial if pursued.
- **Impact:** 1/5 — Best Practices isn't a Top-3 priority; these are benign or third-party. Lowest mission weight.
- **Priority:** 1/3 = **0.3**

---

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Collection LCP image priority hint | 2 | 1 | **2.0** | Only code-authorable golden-path gap; one optional param hints the collection LCP image |
| 2 | SYS-4 · Duplicate meta descriptions | 2 | 3 | 0.7 | Content at scale — Britni/Jenna |
| 3 | SYS-5 · Sitewide a11y crawl residue | 2 | 3 | 0.7 | Off-path, needs rendered DOM to pin — Mason |
| 4 | SYS-6 · Security response headers | 2 | 4 | 0.5 | Platform-controlled — Mason/Shopify |
| 5 | SYS-2 · Performance (third-party/content/platform) | 2 | 5 | 0.4 | Field passes; Route removal + HEIC re-export — Mason + content |
| 6 | SYS-3 · Image-alt residue | 1 | 1 | 1.0 | Won't-fix — decorative artifact, no storefront change |
| 7 | SYS-7 · Best-practices / console / inline SVG | 1 | 3 | 0.3 | Third-party / benign — mostly no action |

Every one of the 27 findings lands in exactly one system: PERF-15 → SYS-1; PERF-1…14,16,17 → SYS-2; SEO-1 → SYS-3; SEO-2 → SYS-4; A11Y-1 → SYS-5; SEC-1/SEC-2 → SYS-6; BP-1…5 → SYS-7. None dropped, none invented.

## The handoff

Execution draws the budget line on this order. Only **SYS-1** is both code-authorable in a GitHub-only run and currently wrong in `main`. SYS-2 through SYS-7 are owner-gated (content, integration, platform, rendered-DOM) or won't-fix, and hand off as PR to-dos. The thin code batch is honest, not lazy — the a11y/SEO priority work is already in `main`, and the rest needs hands a GitHub-only cycle doesn't have.
