# Execution — 2026-06-30-A

Site: https://hazelboutique.com/ · Cycle: 2026-06-30-A · Branch: `hobbes-cycle-2026-06-30` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is **feasibility, not points**. This is a GitHub-only run (no browser, no Shopify CLI) and a re-measurement cycle: Accessibility is 100 / axe 0 and SEO 100 across the whole golden path, the prior cycle's collection-LCP fix is already merged in `main`, and the referrer hardening is already in `main`. The only system with a slice that is both **code-authorable and currently wrong in `main`** is SYS-1 — the cart-drawer upsell image.

| System | Effort | In batch? | Why |
|---|---|---|---|
| SYS-1 · Performance — lab gap, field passing | 5 | ◐ (code slice only) | Cart-drawer upsell image (full-res src, no dimensions) is the one first-party code-authorable spot wrong in `main`. The rest — Route Insurance removal, HEIC re-export, platform minify/cache, core render-blocking CSS — is owner-gated. |
| SYS-2 · Duplicate meta descriptions | 3 | ⛔ | Content at scale (admin copy) — Britni/Jenna |
| SYS-3 · Image-alt residue | 1 | ⛔ | Won't-fix — decorative cursor follower, confirmed correct in source |
| SYS-4 · Sitewide a11y crawl residue | 3 | ⛔ | Off-path; counts-only data; needs rendered DOM to pin — Mason at review |
| SYS-5 · Security headers | 4 | ⛔ | Platform-controlled response headers; referrer meta already in `main` — Mason/Shopify |
| SYS-6 · Best-practices / console / inline SVG | 3 | ⛔ | Third-party / benign / rendered-DOM-gated |

Effort spent: **1** (the SYS-1 cart-upsell slice). Left for later cycles / human owners: the bulk of SYS-1 (Route removal, HEIC re-export, platform), SYS-2, SYS-4, SYS-5, SYS-6 — every one owner-, platform-, or browser-gated — and SYS-3 (won't-fix). The small batch is honest, not lazy: I swept the whole codebase for the named patterns (icon-only controls without an accessible name, unsized/full-res JS-injected images, referrer hardening, inline-SVG duplication) and there is exactly one code-owned gap left wrong in `main`. I am not inventing risky work (blind duplicate-id edits, a base.css critical-path change, an inline-SVG sprite refactor) to pad the batch — those are bucket-3 by the template's own test and would risk the live store.

## 2. Implementation (against the real source)

### SYS-1 slice — cart-drawer upsell image: size the source, lock the dimensions · first-party slice of PERF-2 / PERF-8 / PERF-10

The cart drawer injects a "Wear it with:" upsell after `DOMContentLoaded` when the cart has items (`snippets/cart-drawer.liquid`, `renderUpsell`). The image was:

```liquid
<img class="cartUpsell__image" src="${product.images[0]}" alt="${product.title}" />
```

Two problems in code we own:
1. **`product.images[0]` is the full-resolution original** from `recommendations/products.json`, dropped into a box the CSS renders at `width: 25%` with `aspect-ratio: 4 / 5` (`assets/base.css:6740`). A full-size product JPEG to paint a ~100px thumbnail — pure image-delivery waste (the PERF-2 class), paid by exactly the users the field (CrUX) measures.
2. **No intrinsic `width`/`height`.** The CSS `aspect-ratio` reserves the box once styles load, but the element gives the browser no ratio of its own — the layout-shift class (PERF-8/PERF-10).

Fix — build a CDN-sized URL and lock the ratio:

```liquid
      const rawImage = product.images && product.images[0];
      const image = rawImage ? `${rawImage}${rawImage.includes('?') ? '&' : '?'}width=400` : '';
```

```liquid
    <img class="cartUpsell__image" src="${image}" alt="${product.title}" width="400" height="500" loading="lazy" />
```

**Why this is correct and complete:**
- `&width=400` rides Shopify's CDN image transform. The displayed box is 25% of a ~440px drawer (~110px), so 400px covers retina with headroom — a large download shrinks to a thumbnail-appropriate one. The `includes('?')` guard keeps the URL valid whether or not the source carries a query string (products.json URLs always carry `?v=`, but the guard costs nothing and is robust).
- `width="400" height="500"` is the 4:5 ratio the CSS already enforces, so it changes no rendered layout — it only gives the browser the ratio before `base.css` loads. `object-fit: cover` (already on `.cartUpsell__image`) keeps the crop correct.
- `loading="lazy"` is harmless here (the node is injected post-parse into a `visibility:hidden` drawer) and signals intent.
- `alt="${product.title}"` is unchanged — already meaningful.
- **Pattern sweep done, not just the flagged file.** I checked every live JS-injected first-party image: the footer "Recently viewed" carousel (`sections/footer.liquid:35`) already constrains to `image_url: width: 600` inside a `.ratio` wrapper that reserves layout — no change needed; the `snippets/recent-viewed-product-js.liquid` duplicate is entirely wrapped in `{% comment %}` (dead/orphaned) — renders nothing, left untouched. The cart-drawer upsell was the only live exception.

### Verification run (no browser, no Shopify CLI in CI)
- **Source confirmation:** grep of `<img` across `snippets/`, `sections/`, `blocks/` shows the cart-drawer upsell was the only live first-party JS-injected image lacking both a width-constrained source and intrinsic dimensions. Footer recently-viewed is already sized; the orphaned snippet is commented out.
- **No-regression check:** the change is contained to `renderUpsell` in `snippets/cart-drawer.liquid` and only runs when `cart.items.size > 0`. Empty cart (the PSI condition) emits nothing — no golden-path baseline can regress from it. The new `image` const is local to the function.
- **Checker:** Theme Check is the stack's checker (`DEVELOPMENT.md`) but isn't installed in this runner. Adding a sized `src` and `width`/`height`/`loading` attributes to an existing `<img>` inside a JS template string cannot introduce a new offense. Theme Check + the browser pass are the human's at review.

## 3. Todo

- [x] SYS-1 slice · build a CDN-sized upsell image URL (`&width=400`) in `renderUpsell` (`snippets/cart-drawer.liquid`) — PERF-2 class
- [x] SYS-1 slice · add intrinsic `width="400" height="500"` + `loading="lazy"` to the upsell `<img>` — PERF-8/PERF-10 class
- [x] Sweep live JS-injected first-party images (footer recently-viewed, orphaned snippet) — confirm cart upsell was the only gap
- [x] Confirm SYS-3 cursor follower is correctly decorative (`alt="" aria-hidden` + dimensions) in `layout/theme.liquid` — won't-fix, documented
- [x] Confirm referrer meta already present (`layout/theme.liquid:8`) — SYS-5 code portion already in `main`
- [x] Sweep icon-only controls for missing accessible names (SYS-4) — all first-party controls labeled; unnamed control is off-path / unlocated
- [x] Write `03-plan.md` / `04-execute.md`, open one PR carrying cycle data + the code change

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1 slice — the cart-drawer upsell image now requests a CDN-sized source and carries intrinsic dimensions (`snippets/cart-drawer.liquid`).

**Bucket 2 — written, needs browser confirmation at review:**
- SYS-1 slice: add an item to the cart, open the drawer, confirm the "Wear it with:" upsell renders, the thumbnail loads from a `…&width=400` URL (smaller download), the image isn't distorted (`object-fit: cover` holds), and no new console error. The fix only runs with a non-empty cart, so PSI's empty-cart golden run won't show it — confirm in the drawer directly.

**Bucket 3 — handed to a human (see PR to-dos):**
- SYS-1 (rest of Performance): Route Insurance removal (`DEVELOPMENT.md` flags it) + HEIC image re-export + platform minify/cache/duplicate-JS + core render-blocking `base.css` — Mason (platform/integration) + Britni/Jenna (image re-export). Field already passes for real users.
- SYS-2 (duplicate meta descriptions): write unique admin descriptions for the EVI11 vintage line, bracelet pairs, and the description-less pages falling back to "Hazel Boutique" — Britni/Jenna.
- SYS-4 (sitewide a11y residue): pin the 1 unnamed control + 10 HTML-structural warnings from the rendered DOM and fix in place — Mason at review.
- SYS-5 (security headers): set Referrer-Policy / Permissions-Policy at the platform if/where Shopify allows — Mason. CORS `*` on CDN assets is benign.
- SYS-6 (best-practices / console / inline SVG): third-party console noise and CDN format negotiation need no theme change; the `icon-plus` sprite refactor is deferred as invasive for a cosmetic count — Mason if ever pursued.

Execution ends here — branch pushed, PR open. Merge, preview, mobile+desktop check, go-live, and the `published` label are Mason's at the publish stage. The measured after lands in the review's before/after comment once the change is live.
</content>
