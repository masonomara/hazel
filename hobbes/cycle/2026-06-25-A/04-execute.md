# Execution — 2026-06-25

Site: https://hazelboutique.com/ · Cycle: 2026-06-25-A · Branch: `hobbes-cycle-2026-06-25` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is feasibility, not points. This is a GitHub-only run with no browser, so the batch is every **code-authorable, no-browser-safe** system at the top of the order. All three ship in one PR.

| System | Effort | In batch? | Why |
|---|---|---|---|
| SYS-1 · Product-card name mismatch | 1 | ✅ | Code, one-line, sitewide |
| SYS-3 · Heading/structural hygiene | 1 | ✅ | Code, one file |
| SYS-2 · Image-alt coverage | 2 | ✅ | Code (secondary + multicolumn); content tail flagged |
| SYS-4 · Duplicate meta descriptions | 3 | ⛔ | Content-owned (admin copy) — human to-do |
| SYS-6 · Security headers | 4 | ⛔ | Platform-controlled — human/platform |
| SYS-5 · Performance | 5 | ⛔ | Field passes; third-party/content/browser-gated |
| SYS-7 · Best-practices notices | 3 | ⛔ | Third-party + benign — won't-chase |

Effort spent: 4 (SYS-1 + SYS-3 + SYS-2). Left for later cycles: SYS-4/5/6/7, all owner- or browser-gated, handed off as PR to-dos.

## 2. Implementation plan (against the real source)

### SYS-1 — remove `aria-label` from the card-wrapper anchor · closes A11Y-1
`snippets/card-product.liquid:43-48`. The anchor wraps the whole card, so its accessible name must contain its visible text. Delete the `aria-label` line; the accessible name then derives from content (the `card__heading` title span, always present) and contains the visible text by construction → label-content-name-mismatch can't fire. No new "link without name" risk: the title text is always inside the anchor.

```liquid
<a
  class="card-wrapper product-card-wrapper underline-links-hover"
  href="{{ card_product.url }}"
  id="CardLink-{{ section_id }}-{{ card_product.id }}"
>
```

### SYS-2 — fill empty alts in code · closes the code portion of SEO-1
1. Secondary hover image, `snippets/card-product.liquid:116` — mirror the primary:
   ```liquid
   alt="{{ card_product.media[1].alt | default: card_product.title | escape }}"
   ```
2. Multicolumn card image, `sections/multicolumn.liquid:110-117` — add an alt fallback to the card title:
   ```liquid
   {%- assign multicolumn_image_alt = block.settings.image.alt | default: block.settings.title | strip_html | escape -%}
   {{ block.settings.image | image_url: width: 3200 | image_tag: widths: '...', sizes: sizes, class: 'multicolumn-card__image', alt: multicolumn_image_alt }}
   ```
The 32px `aria-hidden` decorative icon and admin-uploaded product images are deliberately **not** touched (correct as-is / content-owned).

### SYS-3 — remove the duplicated "Collection:" span · closes the code portion of A11Y-2
`sections/main-collection-banner.liquid:15-29`. Line 16 already renders the visually-hidden `{{ 'sections.collection_template.title' | t }}: ` prefix for both branches; line 26 renders it a second time inside the `else`. Delete the duplicate at line 26 so the H1 text stops doubling to "Collection: Collection: <title>".

## 3. Todo

- [x] SYS-1 · remove `aria-label` from `card-product.liquid` card anchor (A11Y-1)
- [x] SYS-2 · secondary hover image alt fallback in `card-product.liquid` (SEO-1)
- [x] SYS-2 · multicolumn image alt fallback in `multicolumn.liquid` (SEO-1)
- [x] SYS-3 · remove duplicate "Collection:" span in `main-collection-banner.liquid` (A11Y-2)
- [x] Theme Check on touched files — no new offenses
- [x] Write 03-plan.md / 04-execute.md, open one PR carrying cycle data + code

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1, SYS-2 (code portion), SYS-3.

**Bucket 2 — written, needs browser confirmation at review:**
- SYS-1: confirm axe `label-content-name-mismatch` reads **0** on Collection (mobile + desktop) and Home (mobile), and product cards are still keyboard/voice-operable by name.
- SYS-2: confirm the secondary card image and multicolumn images now report alt present; confirm the screen-reader name of the card link is acceptable given the title already appears (mild redundancy — manual §G sign-off).
- SYS-3: confirm every collection page H1 still shows the title and reads "Collection: <title>" once (no visual change expected).

**Bucket 3 — handed to a human (see PR to-dos):** SYS-4 (content), SYS-5 (Route Insurance removal + HEIC re-export + browser-gated perf), SYS-6 (platform headers), SYS-7 (third-party/benign), and the A11Y-2 residual single-page heading/unnamed-link items needing a rendered-DOM follow-up.
