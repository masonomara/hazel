# Changelog

<!-- Human-owned record. At the publish stage Hobbes drafts a new entry for the human to
     review and approve (see hobbes/templates/PUBLISH-TEMPLATE.md); past entries are history
     and are never rewritten. Per-cycle numbers live in the scorecard, not here. -->

The running record of shipped work. One change per entry, numbered in order, newest at the bottom of **Entries**.

**Format:** `YYYY-MM-DD — NNN type/name: what changed.`

**Types:** `feature` · `cleanup` · `fix` · `content` · `config` (extend as needed)

**Rule:** every `feature` carries a `RESULTS:` line with a measured outcome. Define the metric first. If you cannot measure it, it is not shipped.

Filled baseline scorecards live in `hobbes/scorecards/`.

---

## Examples — delete once you have real entries

**2026-08-06 — 001 feature/custom-embroidery:** Built a custom-embroidery add-on that lets customers personalize products on the product page. An "add custom embroidery" button opens a modal with live preview and a thread-color picker, a configurable fee, and a customization that carries through the drawer, cart line items, and the order, editable and removable throughout. Pulls product and variant colors from metafields (`hex_color`, `display_color`), hides the thread-color variant from the standard picker and surfaces it in the modal, and is fully configurable from theme settings. RESULTS: 60 orders on the three mock necks, 3 customizations.

**2026-08-06 — 002 cleanup/collections:** Audited three collections and tagged missing products — Hazel Minis, Mock Necks, Perfume — as `hazelmini`, `mockneck`, `perfume`.

**2026-08-06 — 003 cleanup/sizing-guide:** Added four size charts (hoodie, mock neck, barrel pants, joggers), added the oversized-fit note at the top, removed all Australian size references.

---

## Entries
