# Execution — 2026-07-03-A

Site: https://hazelboutique.com/ · Cycle: 2026-07-03-A · Branch: `hobbes-cycle-2026-07-03` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is **feasibility, not points**. This is a GitHub-only run (no browser, no Shopify CLI) and a re-measurement cycle: Accessibility is 100 / axe 0 and SEO 100 across the whole golden path, and the prior cycle's cart-upsell perf slice is already merged in `main`. Walking `03-plan.md` top-down, exactly one system has a slice that is both **code-authorable and currently wrong in `main`**: SYS-1's meta-description fallback.

| Rank | System | Effort | In batch? | Why |
|---|---|---|---|---|
| 1 | SYS-1 · Meta-description uniqueness | 2 | ◐ (code slice) | Theme meta-description chain has no `blog` branch and no fallback for content-less `page` types → 4 pages emit the bare shop name. Fixable in one file. The product-description duplicates + home SEO are content (Jenna/Britni). |
| 2 | SYS-2 · Image alt | 2 | ⛔ | A11Y-1 = 2 imgs in a product's admin description (content, Jenna); SEO-1 = decorative cursor follower, correct in source (won't-fix) |
| 3 | SYS-4 · Security response headers | 4 | ⛔ | Platform-controlled response headers; referrer meta already in `main` — Mason/Shopify |
| 4 | SYS-3 · Performance | 5 | ⛔ | Field passes; cart-upsell slice already in `main`; rest is Route removal / HEIC re-export / platform / core render-blocking CSS — owner-gated |
| 5 | SYS-5 · Best-practices / console / inline SVG | 3 | ⛔ | Third-party / benign / DRY-source / rendered-DOM-gated |

Effort spent: **2** (the SYS-1 code slice). Left for later cycles / human owners: SYS-1's content half, SYS-2 (A11Y-1 content; SEO-1 won't-fix), SYS-3, SYS-4, SYS-5 — every one owner-, platform-, browser-, or content-gated. The thin code batch is the truth of the site, not caution: I swept every `<img>` in the theme (zero missing `alt`), the meta-description chain (found the one real gap), the heading dump (all 178 pages clean), and the referrer/perf code (already in `main`). One first-party code gap exists this cycle, and it ships. I am not padding the batch with risky blind work (forcing `alt=""` on content images, a base.css critical-path change, an inline-SVG sprite refactor) — those are bucket-3 by the template's own test.

## 2. Implementation (against the real source)

### SYS-1 slice — per-page-type meta-description fallback · SEO-2 (code half)

The theme carries a **custom** meta-description chain (Dawn ships only `page_description`) at `layout/theme.liquid:26-44`. It gave collections a unique fallback but left two holes that dumped pages onto the bare `shop.name`:

1. **No `blog` branch** — `/blogs/news` fell straight through to `shop.description | default: shop.name` → "Hazel Boutique".
2. **No fallback for content-less `page` types** — `/pages/divider`, `/pages/gift-certificates`, `/pages/swym-share-wishlist` have blank `page.content`, so `page.content | strip_html` was blank and they too hit the shop-name fallback.

Pinned from `raw/crawl.json` (the 5-way "Hazel Boutique" duplicate): `/`, `/blogs/news`, `/pages/divider`, `/pages/gift-certificates`, `/pages/swym-share-wishlist`.

Fix — mirror the collection pattern already in the block (line 32) for `blog` and content-less `page`:

```liquid
        elsif request.page_type == 'article'
          assign meta_description = article.excerpt_or_content | strip_html | truncate: 160
        elsif request.page_type == 'blog'
          assign meta_description = blog.title | append: ' from ' | append: shop.name | append: '.'
        elsif request.page_type == 'page'
          assign meta_description = page.content | strip_html | truncate: 160
          if meta_description == blank
            assign meta_description = page.title | append: ' at ' | append: shop.name | append: '.'
          endif
        endif
```

**Why this is correct and complete:**
- **De-duplicates 4 of the 5.** `/blogs/news` → "News from Hazel Boutique." · `/pages/divider` → "divider at Hazel Boutique." · `/pages/gift-certificates` → "Gift Certificates at Hazel Boutique." · `/pages/swym-share-wishlist` → "Wishlist at Hazel Boutique." Each is factual and unique — no invented brand copy.
- **Zero golden-path regression risk.** The change only fires for pages whose description was already blank (the bare shop-name fallback). Home is `page_type == 'index'` — no branch touches it, so it is **unchanged** (still "Hazel Boutique" until Jenna sets the admin homepage SEO description). Collection and Product golden pages already have real descriptions, so they never reach this code. No golden page's meta description changes.
- **Upgrade-safe.** It edits an already-custom Hazel block, not Dawn core; it adds two `elsif`/`if` branches in the existing `{%- liquid -%}` tag. `blog` and `page` objects are in scope on their respective page types. `escape` on output is unchanged (line 47).
- **Home (`index`) is deliberately not code-fixed.** A homepage meta description is brand-visible marketing copy Jenna owns (admin: Online Store → Preferences). Inventing one in code would be worse than her copy and brand-visible without sign-off — handed off, not guessed.

**Pattern sweep done.** I checked the whole meta chain, not just the flagged pages: `snippets/meta-tags.liquid` derives `og_description` from the same `meta_description` I now populate, so the Open Graph / Twitter descriptions inherit the fix for free. No other template emits `<meta name="description">` except `templates/gift_card.liquid` and `layout/password.liquid`, both of which set their own correct values.

### Verification run (no browser, no Shopify CLI in CI)
- **Source confirmation:** grep for `<meta name="description"` and the `meta_description` assignment chain confirms `layout/theme.liquid` is the single source for the storefront description; the 5 duplicate URLs map to exactly the two holes fixed.
- **No-regression check:** the added branches only assign when the prior value is blank; no existing branch's output changes. Golden pages (Home index / Collection / Product) do not reach the new code.
- **Checker:** Theme Check is the stack's checker (`DEVELOPMENT.md`) but isn't installed in this runner. Adding two `elsif`/`if` branches to an existing `{%- liquid -%}` assignment cannot introduce a new offense. Theme Check + the browser/source pass are the human's at review.

## 3. Todo

- [x] Pin the "Hazel Boutique" ×5 duplicate to the 5 exact URLs and their page types (`raw/crawl.json`)
- [x] Confirm the theme meta-description chain is the source and locate the two fallback holes (`layout/theme.liquid:26-44`)
- [x] SYS-1 slice · add a `blog` branch + content-less `page` title fallback (`layout/theme.liquid`) — SEO-2 code half
- [x] Confirm SEO-1 mouse image is correctly decorative (`alt="" aria-hidden`) in `main` — won't-fix, documented
- [x] Confirm A11Y-1 pillow imgs are product-description content, not template (sweep: zero template `<img>` without `alt`) — content handoff
- [x] Confirm cart-upsell perf slice + referrer meta already in `main` — no code action
- [x] Confirm the §F multiple-H1 / skipped-heading flags are clean in the authoritative heading dump — no code target
- [x] Write `03-plan.md` / `04-execute.md`, open one PR carrying cycle data + the code change

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1 slice — the theme meta-description fallback now gives blog and content-less page types a unique, factual description (`layout/theme.liquid`), de-duplicating 4 of the 5 "Hazel Boutique" pages.

**Bucket 2 — written, needs confirmation at the review's SEO re-baseline:**
- SYS-1 slice: after publish, confirm `/blogs/news`, `/pages/divider`, `/pages/gift-certificates`, `/pages/swym-share-wishlist` each emit a unique `<meta name="description">` (view-source or the re-crawl), that the "Hazel Boutique" duplicate count drops from 5 to 1, and that no golden page's description changed. No browser interaction needed — a source/crawl check.

**Bucket 3 — handed to a human (see PR to-dos):**
- SYS-1 (content half): set the homepage SEO meta description in admin (fixes `/`), and write unique `product.description` copy for the duplicated families — EVI11 vintage ×5, ornaments ×2, tanks ×2, earrings ×2, joggers ×2, necklaces ×2, jackets ×2 — Britni/Jenna.
- SYS-2 (A11Y-1): add alt text to the 2 images embedded in the `/products/the-miss-honey-pillow` admin product description — Jenna/Britni. SEO-1 (cursor follower) is won't-fix (correctly decorative).
- SYS-3 (Performance): Route Insurance removal (`DEVELOPMENT.md` flags it) + HEIC image re-export + platform minify/cache/duplicate-JS + core render-blocking `base.css` — Mason (platform/integration) + Britni/Jenna (image re-export). Field already passes for real users.
- SYS-4 (security headers): set Referrer-Policy / Permissions-Policy at the platform if/where Shopify allows — Mason. CORS `*` on CDN assets is benign.
- SYS-5 (best-practices / console / inline SVG): third-party console noise and CDN format negotiation need no theme change; the `icon-plus` sprite refactor is deferred as invasive for a cosmetic `0-critical` count — Mason if ever pursued.

Execution ends here — branch pushed, PR open. Merge, preview, mobile+desktop check, go-live, and the `published` label are Mason's at the publish stage. The measured after lands in the review's before/after comment once the change is live.
