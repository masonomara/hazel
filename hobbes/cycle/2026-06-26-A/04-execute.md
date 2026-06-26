# Execution — 2026-06-26-A

Site: https://hazelboutique.com/ · Cycle: 2026-06-26-A · Branch: `hobbes-cycle-2026-06-26` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is **feasibility, not points**. This is a GitHub-only run (no browser, no Shopify CLI) and a re-measurement cycle: A11Y is already 100 / axe 0 and SEO 100 on the whole golden path — the code-owned priority work shipped in PRs #27 and #31 is holding in `main`. The only system that is both **code-authorable and currently wrong in `main`** is SYS-1.

| System | Effort | In batch? | Why |
|---|---|---|---|
| SYS-1 · Cart-drawer collection image alt | 1 | ✅ | Code, one-line, sitewide — last failing golden SEO row |
| SYS-2 · Duplicate meta descriptions | 3 | ⛔ | Content at scale (admin copy) — Britni/Jenna |
| SYS-3 · Sitewide a11y crawl residue | 3 | ⛔ | Off-path; needs rendered DOM to pin — Mason at review |
| SYS-5 · Security headers | 4 | ⛔ | Platform-controlled response headers — Mason/Shopify |
| SYS-4 · Performance | 5 | ⛔ | Field passes; Route removal + HEIC re-export — Mason + content |
| SYS-6 · Best-practices / console notices | 3 | ⛔ | Third-party / benign / rendered-DOM-gated — mostly no action |

Effort spent: **1** (SYS-1). Left for later cycles / human owners: SYS-2 through SYS-6, every one owner-, platform-, or browser-gated. The small batch is honest, not lazy — there is exactly one code-owned gap left wrong in `main`, and I'm not inventing work by re-touching code that's already correct.

## 2. Implementation (against the real source)

### SYS-1 — title fallback for the placeholder collection-card alt · closes the code portion of SEO-1

`snippets/card-collection.liquid:71`. The placeholder-image branch (lines 51–77) renders the image passed as `placeholder_image`, with the alt sourced straight from the admin field:

Before:
```liquid
alt="{{ placeholder_image.alt | escape }}"
```
After:
```liquid
alt="{{ placeholder_image.alt | default: card_collection.title | escape }}"
```

**Why this is correct and complete:**
- The flagged image `cart_drawer_collection_image_two` (`IMG_2024-05-08-170032.jpg`) is rendered here via the cart drawer (`snippets/cart-drawer.liquid:115-120`), which passes both `card_collection: settings.cart_drawer_collection_two` and `placeholder_image: settings.cart_drawer_collection_image_two`. Its admin alt is blank → the old code emitted `alt=""` → seo.py counts it missing (`hobbes/tools/seo.py:111-113` treats empty alt as missing). The fallback now emits the collection's title — a meaningful description of where the promo image links.
- **Pattern, not one-off:** `card-collection.liquid:71` is the *single* placeholder-alt site in the theme (grep-confirmed). `card-collection` is rendered from `cart-drawer`, `collage`, `main-list-collections`, and `collection-list`; fixing line 71 covers every placeholder render in one place. The non-placeholder branch (line 100) already has the same `card_collection.featured_image.alt`-with-fallback shape — this brings the placeholder branch in line with it.
- **Byte-pattern-identical to PR #27**, which used `... .alt | default: <title> | escape` for the card-product secondary image and the multicolumn card. Same idiom, upgrade-safe, one core-light edit.

**Won't-fix (documented, not dropped):** the second flagged image `mouse_image` (`IMG_3438.png`, 32px cursor follower) at `layout/theme.liquid:491-498` already carries `alt="" aria-hidden="true"` and is **correctly decorative**. seo.py flags it only because it counts empty alt; SiteOne's sitewide alt count tolerates it (1738 ok / 0 warning). Adding descriptive alt would *harm* a11y. Leave it.

### Verification run (no browser, no Shopify CLI in CI)
- **Pattern sweep:** `grep` for `placeholder_image.alt` and `alt=""` across `snippets/` + `sections/` — `card-collection.liquid:71` is the only admin-sourced placeholder alt that could resolve blank; no other code-owned empty-alt source on the golden path. The prior cycles already closed card-product (secondary) and multicolumn.
- **SiteOne cross-check:** `raw/crawl.json` accessibility table reads `Missing image alt attributes: 0 warning / 1738 ok` sitewide — confirms no broader code-owned alt gap; SEO-1 is purely the golden-path empty-alt nuance, now closed in code for the cart-drawer image.
- **Checker:** Theme Check is the stack's checker (`DEVELOPMENT.md`) but isn't installed in this runner. A one-line Liquid filter addition to an existing `alt=` attribute cannot introduce a new offense. Theme Check + the browser pass are the human's at review.

## 3. Todo

- [x] SYS-1 · add `default: card_collection.title` fallback to placeholder alt in `card-collection.liquid:71` (SEO-1)
- [x] Codebase sweep for other code-owned empty-alt patterns — none beyond what PRs #27/#31 closed
- [x] Confirm `mouse_image` is correctly decorative (`alt="" aria-hidden`) — won't-fix, documented
- [x] Cross-check SiteOne sitewide alt count (0 warnings) — no broader gap
- [x] Write `03-plan.md` / `04-execute.md`, open one PR carrying cycle data + the code change

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1 — the placeholder collection-card alt fallback in `snippets/card-collection.liquid`.

**Bucket 2 — written, needs browser confirmation at review:**
- SYS-1: open the cart drawer on Home/Collection/Product (mobile + desktop) and confirm the `cart_drawer_collection_image_two` promo now reports a non-empty `alt` (the collection title), and re-run the golden-path SEO check to confirm the image-alt row moves from ✗ toward ✓ (the only residual will be the decorative `mouse_image`, which is correct as-is).

**Bucket 3 — handed to a human (see PR to-dos):** SYS-2 (content meta descriptions), SYS-3 (rendered-DOM a11y residue), SYS-4 (Route Insurance removal + HEIC re-export + browser-gated perf), SYS-5 (platform response headers), SYS-6 (third-party/benign best-practice + console notices).

Execution ends here — branch pushed, PR open. Merge, preview, mobile+desktop check, go-live, and the `published` label are Mason's at the publish stage. The measured after lands in the review's before/after comment once the change is live.
