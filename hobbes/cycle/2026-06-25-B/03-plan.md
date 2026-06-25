# Plan — 2026-06-25-B

Site: https://hazelboutique.com/ · Cycle: 2026-06-25-B · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

The findings are the facts. The systems, effort, and impact below are Hobbes' calls. Every system maps to real finding IDs from this cycle; nothing is invented.

## The frame that decides this cycle

This is a **re-measurement** cycle, and reading it as a fresh problem set would be wrong. Cycle **2026-06-25-A** (PR #27, merged) already shipped the three code-authorable fixes this baseline re-surfaces: the card-anchor `aria-label` removal (A11Y-1), the image-alt sweep (SEO-1), and the doubled "Collection:" H1 (the A11Y-2 heading root). The B baseline was captured against the **live, not-yet-published** store, so it re-reads the same findings A already closed in code.

Two things separate signal from noise here:

1. **One of A's fixes regressed in the repo.** Three "Hobbes capture digest" PRs (#28, #29, #30) each re-touched **only** `snippets/card-product.liquid` and re-introduced `aria-label="{{ card_product.title | escape }}"` — the exact line A deleted. The capture pulls the live theme down (the bidirectional Shopify CLI, per `DEVELOPMENT.md`), and the live theme still carries the bug because A's fix isn't published. Net: **`main` currently ships the A11Y-1 bug again.** That is the one real, code-authorable action this cycle — restore the fix.

2. **A's other fixes are intact and landing.** Current `main` still has the secondary-image alt fallback (`card-product.liquid:116`), the multicolumn alt fallback (`multicolumn.liquid:110/118`), and the de-duplicated banner span (`main-collection-banner.liquid`, single occurrence). And the live data moved: B's `SEO-1` shows Collection missing-alt **41 → 2** and the crawl's per-page heading data is clean (0 multi-H1, 0 heading errors). Those two systems need **no new code** — they're code-complete, awaiting the human's publish.

So the honest batch is small and I won't pad it: **re-apply SYS-1**, and **escalate the capture-clobber loop** — because re-applying a fix that three consecutive captures have already reverted is worthless unless the publish happens and/or the capture stops pulling unpublished code back down.

The rest (perf, security headers, duplicate descriptions, best-practice notices, the unpinnable heading/aria residual) is content-, platform-, integration-, or rendered-DOM-gated, exactly as A scoped it. CrUX field data (§C) still **passes on all three golden pages** — real users aren't waiting — so the lab-perf findings stay low-impact throttle artifacts.

## The systems

### SYS-1 · Product-card link — accessible-name mismatch (REGRESSED, re-fix)
- **Findings:** A11Y-1 (label-content-name-mismatch, 55 nodes).
- **The system:** `snippets/card-product.liquid:47`. The whole card is one `<a>` carrying `aria-label="{{ card_product.title | escape }}"`. The anchor wraps the title **and** price **and** swatches, so its visible inner text is "Title $48.00 …" while its accessible name is just "Title" — WCAG 2.5.3 (Label in Name) fails. One shared snippet renders every product card sitewide, so the 55 flagged nodes across Home/Collection are one root. **A deleted this line in PR #27; captures #28–30 put it back.** Fix (again): drop the `aria-label`. The accessible name then computes from content (the `card__heading` title span, always present), which contains the visible text by construction, so the rule can't fire and the link never loses its name.
- **Effort:** 1/5 — one-line delete in a shared snippet, code (Mason) · trivial · high confidence. Browser/screen-reader confirm at review (bucket 2). **Gated by a process bug:** worthless unless the publish lands and/or the capture digest stops re-pulling unpublished theme code over merged fixes (escalation below).
- **Impact:** 5/5 — Priority 1 (accessibility). Clears the only axe failure on the golden path (BASELINE §D), 55 nodes, every card-bearing page sitewide.
- **Priority:** 5/1 = 5.0

### SYS-2 · Image-alt coverage sweep (code-complete in repo — awaiting publish)
- **Findings:** SEO-1 (golden Home 15/44, Collection 2/89, Product 2/25 images with empty alt).
- **The system:** A's code fixes are present in `main` and **landing live** — Collection's missing-alt fell **41 → 2** since cycle A. The secondary hover image (`card-product.liquid:116`) and multicolumn card images (`multicolumn.liquid:110/118`) both now derive alt from `image.alt | default: <title>`. The Home residual of 15 (verified from `raw/*.seo.json`) is: 4 `multicolumn-card__image` (book/store/email/tape — covered by the in-repo fallback, will resolve on publish if the block titles are set, else admin), ~9 hero/slideshow content photos with blank admin alt (`motion-reduce`, w≥1536 — **content-owned**, a heading-based code fallback would be poor alt), and **1 `aria-hidden="true"` 32px decorative icon** (`IMG_3438.png`) where `alt=""` is **correct**. No new code-authorable `<img>` source remains — the codebase sweep found no other hardcoded `alt=""` and no `image_tag` gap (`image_tag` auto-emits the admin alt).
- **Effort:** 1/5 (code) — **already shipped in A; nothing to re-write.** Residual is content at small scale (admin alt fields, Britni/Jenna), owner-gated.
- **Impact:** 4/5 — Priority 2 (SEO "All images have alt") + Priority 1 (a11y). The code already clears the bulk; the row fully flips only when the admin alts are filled.
- **Priority:** 4/1 = 4.0 — **no code this cycle; content tail is a human to-do.**

### SYS-3 · Sitewide heading / structural hygiene (code-complete in repo — awaiting publish)
- **Findings:** A11Y-2 (sitewide: 57 HTML-structural warnings + 1 unnamed link/button; §F multiple-H1 ×1, skipped-heading ×1).
- **The system:** A's PR #27 deleted the duplicated visually-hidden "Collection:" span in `main-collection-banner.liquid` (now a single occurrence in `main`), killing the "Collection: Collection: <title>" doubling. B confirms it: the crawl's per-page heading table shows **0 pages with >1 H1 and 0 heading errors** — the §F "1/1" rollup has **no pinnable per-page culprit** in `raw/crawl.json`. The remaining A11Y-2 items — 57 "HTML structural" warnings and **1 unnamed link/button** — are SiteOne aggregate prevalence with no per-URL element in this JSON; pinning them needs the **rendered DOM**, so they're a DOM-equipped follow-up, not a blind guess.
- **Effort:** 1/5 (code) — **already shipped in A; nothing to re-write.** The residual is rendered-DOM-gated.
- **Impact:** 3/5 — Priority 2 (heading/structure hygiene). The collection-H1 root is closed in code.
- **Priority:** 3/1 = 3.0 — **no code this cycle; residual is a DOM follow-up.**

### SYS-4 · Duplicate meta descriptions
- **Findings:** SEO-2 ("Hazel Boutique" ×5; templated product/collection copy ×4, ×4, ×2, ×2).
- **The system:** Two causes, neither code-fixable. (a) "Hazel Boutique" ×5 = system/utility pages (home, password, cart, search-class) with no natural description falling to `shop.description`; the theme fallback chain in `layout/theme.liquid` is already correct, so there's no code bug. (b) The repeated product/collection blurbs (EVI11 vintage one-of-a-kinds, candle spec sheet, bracelet copy) are identical **merchant copy in Shopify admin**. Content-owned (Britni/Jenna).
- **Effort:** 3/5 — content at scale, admin, owner-gated. No code, not authorable in this repo.
- **Impact:** 2/5 — Priority 2, but Lighthouse SEO is already 100 and most duplicates are one-of-a-kind vintage items where unique copy is genuinely hard.
- **Priority:** 2/3 = 0.67 — **human to-do, not code.**

### SYS-5 · Performance — lab below target, field already passing
- **Findings:** PERF-1 … PERF-19 (lab scores 42–68, image delivery, cache lifetimes, payload, JS/CSS execution & unused, reflow, render-blocking, LCP discovery, legacy/dup/minify, layout shifts, slowest URLs).
- **The system:** **§C CrUX passes on all three pages — LCP, INP, CLS all "good."** The lab failures are PSI's mobile throttle (Moto G4 / slow-4G / 4× CPU); the 12.7 s LCP is the `✗cut` artifact, not real. The weight is third-party + content, not theme code: `shopify.widget.js` (559 KB, Shop), `protect.widget.js`/`protect.core.js` (Route Insurance — **flagged for removal** in `DEVELOPMENT.md`), `da-restock.js`, Judge.me, Instafeed, GA, freeshippingbar, popup; plus merchant-uploaded **HEIC** hero images (`image_*.heic`, 183 KB+) to re-export. The few first-party levers (fetchpriority on the LCP image PERF-17, deferring `base.css` PERF-11, the desktop lab CLS) need the **rendered page** to target safely and would risk regression written blind — a browser-equipped perf cycle.
- **Effort:** 5/5 — integration removal + coordination (Route Insurance, Mason/admin), content re-export (HEIC → WebP/JPG, Britni/Jenna), residual code browser-gated. Scarce, multi-owner.
- **Impact:** 2/5 — real users already pass (§C). Highest-value concrete move is the Route Insurance removal already on the books.
- **Priority:** 2/5 = 0.4 — **human/integration to-do + defer risky code to a browser cycle.**

### SYS-6 · Missing security response headers
- **Findings:** SEC-1 (Referrer-Policy, Permissions-Policy absent — 2 of 4), SEC-2 (Access-Control-Allow-Origin: \* on assets).
- **The system:** Response headers on a Shopify-hosted storefront are largely platform-controlled — the theme can't set arbitrary response headers, and CSP/HSTS are already present (host-set). SEC-2's `ACAO: *` is on public CDN assets, which is normal, not a credentialed-endpoint risk. Confirm what Advanced actually exposes (admin/checkout settings or an app) before treating as fixable.
- **Effort:** 4/5 — platform/integration, admin (Mason). Not theme-code-authorable.
- **Impact:** 2/5 — hardening headers, no user-facing or mission-priority gain; SEC-2 benign on assets.
- **Priority:** 2/4 = 0.5 — **human/platform to-do.**

### SYS-7 · Best-practices & structural notices
- **Findings:** BP-1 (console errors), BP-2 (inspector issues), BP-3 (invalid inline SVG ×10), BP-4 (duplicate inline SVG ×1), BP-5 (WebP), BP-6 (AVIF).
- **The system:** BP-1/BP-2 are third-party/client-side: `ERR_BLOCKED_BY_CLIENT` (ad blockers), 400/403 from embeds, a `shop.app` frame-ancestors CSP (Shopify) — not first-party bugs. BP-3/BP-4 are "0 critical" warnings (icons inlined per use — minor DOM bloat; the `<use>` refactor is core-theme churn against the upgrade-safety rule). BP-5/BP-6 are informational format-support notices, not defects. Best-Practices score is already 92–96.
- **Effort:** 3/5 — mostly third-party (can't fix) or low-value warnings against the upgrade-safety rule.
- **Impact:** 1/5 — cosmetic/benign.
- **Priority:** 1/3 = 0.33 — **won't-chase this cycle; flagged for visibility.**

## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-1 · Product-card name mismatch (regressed) | 5 | 1 | 5.0 | The one live code regression — restore the deleted `aria-label`, 55 nodes sitewide |
| 2 | SYS-2 · Image-alt coverage | 4 | 1 | 4.0 | **Code already in repo** (41→2 live); content tail to human |
| 3 | SYS-3 · Heading/structural hygiene | 3 | 1 | 3.0 | **Code already in repo** (headings clean); DOM residual to follow-up |
| 4 | SYS-4 · Duplicate meta descriptions | 2 | 3 | 0.67 | Content-owned; theme fallback correct → human |
| 5 | SYS-6 · Security headers | 2 | 4 | 0.5 | Platform-controlled → human/platform |
| 6 | SYS-5 · Performance | 2 | 5 | 0.4 | Field passes; third-party/content/browser-gated → human + defer |
| 7 | SYS-7 · Best-practices notices | 1 | 3 | 0.33 | Third-party + benign → won't-chase |

## The handoff

Execution takes the **code-authorable, no-browser-safe** top of this order. This cycle that is exactly **SYS-1** — re-applying the regressed `aria-label` removal — because SYS-2 and SYS-3 are already code-complete in `main` (A's PR #27, intact) and need only the human's publish, not a re-write. The batch is deliberately one system: padding it with rewrites of already-shipped code would be the "look of work where there is none" the stance forbids.

The decisive non-code item is an **escalation, not a deferral**: the capture-digest workflow (PRs #28–30) has reverted SYS-1's merged fix three times by pulling the unpublished live theme back over `main`. Re-applying it is correct (it restores `main` to truth) but will be clobbered again by the next capture unless the human (a) publishes A's/this fix to the live theme so capture and repo agree, and/or (b) stops the capture digest from overwriting merged theme code. That goes in the PR as the top human to-do.

SYS-4/5/6/7 and the A11Y-2 DOM residual are content-, platform-, integration-, or rendered-DOM-gated; they're written up as owner-tagged human to-dos, not dropped. After publish, the review re-baselines the live site and diffs §D (axe), §E (alt coverage), and §F (headings) against this cycle.
