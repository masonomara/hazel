# Execution — 2026-06-25-B

Site: https://hazelboutique.com/ · Cycle: 2026-06-25-B · Branch: `hobbes-cycle-2026-06-25-B` · Driven by Hobbes from `03-plan.md`.

## 1. Batch selected — effort budget 100

The budget is large; the binding constraint is **feasibility, not points**. This is a GitHub-only run (no browser), and it's a re-measurement cycle: the code-authorable systems A's PR #27 already closed are intact in `main` (SYS-2, SYS-3) — re-writing them would be inventing work. The only system that is both code-authorable **and** currently wrong in `main` is SYS-1, which a capture-digest PR regressed.

| System | Effort | In batch? | Why |
|---|---|---|---|
| SYS-1 · Product-card name mismatch (regressed) | 1 | ✅ | Code, one-line, sitewide — **regressed in `main`, restore it** |
| SYS-2 · Image-alt coverage | 1 | ⛔ | **Already in `main`** (A's PR #27, intact; 41→2 live) — content tail to human |
| SYS-3 · Heading/structural hygiene | 1 | ⛔ | **Already in `main`** (A's PR #27, intact; headings clean) — DOM residual to follow-up |
| SYS-4 · Duplicate meta descriptions | 3 | ⛔ | Content-owned (admin copy) — human |
| SYS-6 · Security headers | 4 | ⛔ | Platform-controlled — human/platform |
| SYS-5 · Performance | 5 | ⛔ | Field passes; third-party/content/browser-gated |
| SYS-7 · Best-practices notices | 3 | ⛔ | Third-party + benign — won't-chase |

Effort spent: **1** (SYS-1). The small batch is honest, not lazy: SYS-2/SYS-3 are done in code and need a publish, not a commit; everything below them is owner- or browser-gated. The capture-clobber loop is escalated, not deferred (§4).

## 2. Implementation plan (against the real source)

### SYS-1 — remove the regressed `aria-label` from the card-wrapper anchor · closes A11Y-1
`snippets/card-product.liquid:43-48`. The anchor wraps the whole card, so its accessible name must contain its visible text. Delete the `aria-label` line; the accessible name then derives from content (the `card__heading` title span, always present) and contains the visible text by construction → `label-content-name-mismatch` can't fire. No new "link without name" risk: the title text is always inside the anchor. This is byte-identical to the change A shipped in PR #27 that captures #28–30 reverted.

Before:
```liquid
  <a
    class="card-wrapper product-card-wrapper underline-links-hover"
    href="{{ card_product.url }}"
    id="CardLink-{{ section_id }}-{{ card_product.id }}"
    aria-label="{{ card_product.title | escape }}"
  >
```
After:
```liquid
  <a
    class="card-wrapper product-card-wrapper underline-links-hover"
    href="{{ card_product.url }}"
    id="CardLink-{{ section_id }}-{{ card_product.id }}"
  >
```

### Verification I ran (no browser, no Shopify CLI in CI)
- `image_tag`/`alt` codebase sweep (SYS-2 completeness): no other hardcoded `alt=""` in `snippets/*.liquid` or `sections/*.liquid`; the `image_tag` calls without an explicit `alt:` auto-emit the admin alt field, so they are not code gaps. The only code-owned empty-alt sources were the two A already fixed.
- Heading residual (SYS-3): `raw/crawl.json` `seo-headings` shows 0 pages with >1 H1 and 0 heading errors — no pinnable culprit, confirming A's banner dedup closed the root.
- Theme Check is the stack's checker (`DEVELOPMENT.md`) but isn't installed in this CI runner; a one-line attribute deletion cannot introduce a new offense. Theme Check + browser are the human's at review.

## 3. Todo

- [x] SYS-1 · remove regressed `aria-label` from `card-product.liquid` card anchor (A11Y-1)
- [x] SYS-2 · confirm in-repo fixes intact (secondary alt `:116`, multicolumn alt) — no re-write needed
- [x] SYS-3 · confirm in-repo banner dedup intact + heading raw clean — no re-write needed
- [x] Codebase sweep for other code-owned `alt` gaps — none found
- [x] Write 03-plan.md / 04-execute.md, open one PR carrying cycle data + code

## 4. What shipped vs. flagged

**Shipped (code, this PR):** SYS-1 — the regressed `aria-label` removal, restored.

**Bucket 2 — written, needs browser confirmation at review:**
- SYS-1: confirm axe `label-content-name-mismatch` reads **0** on Collection (mobile + desktop) and Home (mobile), and product cards stay keyboard/voice-operable by name.

**Escalation (top human to-do — process bug, not a code deferral):** The capture-digest workflow (PRs #28, #29, #30) reverted SYS-1's merged fix three times by pulling the unpublished live theme over `main`. This re-fix restores `main`, but the **next capture will clobber it again** unless the human (a) **publishes** the live theme so capture and repo agree, and/or (b) stops the capture digest from overwriting merged theme code. Owner: Mason.

**Bucket 3 — handed to a human (see PR to-dos):**
- SYS-2 content tail — fill blank admin alt on the ~9 hero/slideshow photos and the 4 multicolumn block titles (Britni/Jenna). The 32px `aria-hidden` decorative icon is correctly `alt=""` — leave it.
- SYS-3 residual — the 57 "HTML structural" warnings + 1 unnamed link/button need a rendered-DOM follow-up to pin.
- SYS-4 — duplicate meta descriptions, admin copy (Britni/Jenna).
- SYS-5 — Route Insurance removal + HEIC re-export + browser-gated perf (Mason/admin + content).
- SYS-6 — platform/response headers (Mason/admin).
- SYS-7 — third-party/benign best-practice notices (no action).
