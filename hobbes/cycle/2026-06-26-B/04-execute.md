# Execution — 2026-06-26-B

Site: https://hazelboutique.com/ · Cycle: 2026-06-26-B · Branch: `hobbes-cycle-2026-06-26` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is **feasibility, not points**. This is a GitHub-only run (no browser, no Shopify CLI) and a re-measurement cycle: A11Y is 100 / axe 0 and SEO 100 across the whole golden path, and the prior cycle's card-collection alt fix is already merged in `main`. The only system that is both **code-authorable and currently wrong in `main`** is SYS-1.

| System | Effort | In batch? | Why |
|---|---|---|---|
| SYS-1 · Collection LCP image priority hint | 1 | ✅ | Code, two files, sitewide param — the one code-authorable golden-path gap (PERF-15) |
| SYS-4 · Duplicate meta descriptions | 3 | ⛔ | Content at scale (admin copy) — Britni/Jenna |
| SYS-5 · Sitewide a11y crawl residue | 3 | ⛔ | Off-path; needs rendered DOM to pin — Mason at review |
| SYS-6 · Security headers | 4 | ⛔ | Platform-controlled response headers — Mason/Shopify |
| SYS-2 · Performance | 5 | ⛔ | Field passes; Route removal + HEIC re-export — Mason + content |
| SYS-3 · Image-alt residue | 1 | ⛔ | Won't-fix — decorative `mouse_image`, no storefront change |
| SYS-7 · Best-practices / console / inline SVG | 3 | ⛔ | Third-party / benign / rendered-DOM-gated — mostly no action |

Effort spent: **1** (SYS-1). Left for later cycles / human owners: SYS-2, SYS-4, SYS-5, SYS-6, SYS-7 — every one owner-, platform-, or browser-gated — and SYS-3 (won't-fix). The small batch is honest, not lazy: there is exactly one code-owned gap left wrong in `main`, and I'm not inventing work by re-touching code that's already correct.

## 2. Implementation (against the real source)

### SYS-1 — priority-hint the collection LCP image · closes PERF-15

The collection page's LCP element is the first product-card image (`raw/…all_hazel_brand-mobile.psi.json` → `lcp-discovery-insight`: `requestDiscoverable: true`, `priorityHinted: false`). The grid already eager-loads the first two cards, but the card snippet had no `fetchpriority` path. Two surgical, additive edits:

**`snippets/card-product.liquid`** — new optional `preload` param, documented in the header comment, emits `fetchpriority="high"` on the featured image:

```liquid
                {% unless lazy_load == false %}
                  loading="lazy"
                {% endunless %}
                {% if preload %}
                  fetchpriority="high"
                {% endif %}
```

**`sections/main-collection-product-grid.liquid`** — set `preload` for the first card only and pass it to the render:

```liquid
              {%- for product in collection.products -%}
                {% assign lazy_load = false %}
                {% assign preload = false %}
                {%- if forloop.index > 2 -%}
                  {%- assign lazy_load = true -%}
                {%- endif -%}
                {%- if forloop.index == 1 -%}
                  {%- assign preload = true -%}
                {%- endif -%}
                ...
                  {% render 'card-product',
                    ...
                    lazy_load: lazy_load,
                    preload: preload,
                    ...
```

**Why this is correct and complete:**
- It targets **exactly one** image — `forloop.index == 1`, the LCP candidate. `fetchpriority="high"` on a single element is the recommended pattern; spraying it across many images defeats the hint.
- `preload` **defaults to false**, so every other `card-product` caller (search, related-products, featured-collection, collage, recent-viewed, main-product) is byte-for-byte unchanged. Notably it does **not** hint related-product cards on the product page, which would compete with the main product image for priority.
- **Home and Product are already correct** (`lcp-discovery-insight` score 1, `priorityHinted: true` on the slideshow and main media). This is the only page that needed the hint — no sweep beyond it is warranted.
- Additive and upgrade-safe: no Dawn core behaviour removed, the eager-load logic that already existed is left intact, the hint simply rides on top.

### Verification run (no browser, no Shopify CLI in CI)
- **Source confirmation:** `lcp-discovery-insight` in `raw/` shows Home/Product already `priorityHinted: true` and Collection `false` — so the fix is scoped to the collection grid only. Grep confirms `card-product.liquid` is the single featured-image render; the new `preload` param flows only from `main-collection-product-grid.liquid`.
- **No-regression check:** `preload` defaults to false; the five other callers don't pass it, so their output is unchanged. The first-two-cards eager logic (`lazy_load`) is untouched.
- **Checker:** Theme Check is the stack's checker (`DEVELOPMENT.md`) but isn't installed in this runner. Adding a conditional `fetchpriority="high"` attribute beside the existing `loading` handling cannot introduce a new offense. Theme Check + the browser/PSI pass are the human's at review.

## 3. Todo

- [x] SYS-1 · add optional `preload` param + `fetchpriority="high"` to `snippets/card-product.liquid` (PERF-15)
- [x] SYS-1 · set `preload` for the first card in `sections/main-collection-product-grid.liquid` and pass to render (PERF-15)
- [x] Confirm Home (slideshow) and Product (main media) are already priority-hinted — no change needed there
- [x] Confirm `preload` defaults false so other `card-product` callers are unchanged
- [x] Confirm `mouse_image` (SEO-1) is correctly decorative (`alt="" aria-hidden`) — won't-fix, documented
- [x] Cross-check SiteOne sitewide alt count (0 warnings / 1720 ok) — no broader code-owned alt gap
- [x] Write `03-plan.md` / `04-execute.md`, open one PR carrying cycle data + the code change

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1 — the collection LCP image priority hint (`snippets/card-product.liquid` + `sections/main-collection-product-grid.liquid`).

**Bucket 2 — written, needs browser/PSI confirmation at review:**
- SYS-1: load the collection page (mobile) and confirm the first product-card `<img>` now carries `fetchpriority="high"`; re-run PSI on `/collections/all-hazel-brand` (mobile) and confirm `lcp-discovery-insight` flips `priorityHinted` to true / the audit passes, with no new CLS from the change. Spot-check that other grids (search, related, featured) render unchanged.

**Bucket 3 — handed to a human (see PR to-dos):** SYS-2 (Route Insurance removal + HEIC re-export + core/critical-path perf), SYS-4 (content meta descriptions), SYS-5 (rendered-DOM a11y residue), SYS-6 (platform response headers), SYS-7 (third-party/benign best-practice + console notices). SYS-3 is a measurement artifact (decorative image) — no storefront action.

Execution ends here — branch pushed, PR open. Merge, preview, mobile+desktop check, go-live, and the `published` label are Mason's at the publish stage. The measured after lands in the review's before/after comment once the change is live.
