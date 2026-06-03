# Custom Embroidery — Recon Findings & Proposed Plan

_Step 1 deliverable. No code changed yet. Reconciled against the live repo (the repo wins over any doc)._

> **Status:** Client answered the four blocking questions (see §7). Plan is **Advanced (not Plus)** and the embroiderable products **have size variants**, so the pricing mechanism is now **locked to Option A** (companion fee product). Product count resolved: **three** products (dusty-blue, seagull, white) — no 4th. Fee product built; **fee variant id = `53563251753274`**; 3 products tagged `embroidery`. **Phases 0 and 1 complete** — ready for Phase 2 (build).

---

## 1. Theme name + version

**Dawn v13.0.1** (Shopify's official Dawn, forked/customized for Hazel Boutique).
Confirmed in `config/settings_schema.json` → `theme_info`: `"theme_name": "Dawn", "theme_version": "13.0.1"`.

- No build system — pure Liquid/CSS/vanilla JS, deployed via Shopify CLI.
- Cart type: **drawer** (`sections/cart-drawer.liquid`), AJAX cart + PubSub pattern.

This is **not** Horizon, so we use the **Dawn** form-id convention.

---

## 2. The product form (the binding target) — CONFIRMED

The add-to-cart form id is **`product-form-{{ section.id }}`** (Dawn standard). Evidence:

- `sections/main-product.liquid:81` → `assign product_form_id = 'product-form-' | append: section.id`
- `snippets/buy-buttons.liquid:47-53` → `{%- form 'product', product, id: product_form_id, ... -%}` — so the rendered `<form>` gets `id="product-form-<sectionId>"`.
- The form is wrapped in a `<product-form>` custom element (`buy-buttons.liquid:27`).

**AJAX serialization is safe.** `assets/product-form.js:36` does `const formData = new FormData(this.form)`. The `FormData(form)` constructor includes **all** form-associated elements — including inputs placed outside the `<form>` but bound via the HTML `form="..."` attribute. So **Method A** from the research (a hidden `properties[Embroidery]` input with `form="product-form-{{ section.id }}"`) will ride along with the AJAX add **with zero changes to `product-form.js`**. This is the upgrade-safe path.

---

## 3. Where Add to Cart is rendered (where the button goes)

- The `buy_buttons` block is rendered at `sections/main-product.liquid:442-449` (`{%- render 'buy-buttons' ... -%}`).
- Inside `snippets/buy-buttons.liquid`:
  - ATC button: `<button id="ProductSubmitButton-{{ section_id }}" name="add">` at `buy-buttons.liquid:78-95`, inside `<div class="product-form__buttons">`.
  - Dynamic checkout / payment button follows it.

**Proposed insertion point:** render the embroidery snippet from `main-product.liquid` **right after the `buy-buttons` render (after line 449)**, gated by the enablement metafield/tag. This keeps the **only** core-theme edit to a single render line, exactly as the constraints require. (Putting it in the section rather than inside `buy-buttons.liquid` keeps the section/buy-buttons separation clean and the form binding works regardless via the `form=` attribute.)

---

## 4. Cart rendering of line item properties — ALREADY HANDLED, no edits needed

Both cart surfaces already loop properties and skip blanks + private (`_`) keys:

- `snippets/cart-drawer.liquid:317-319`:
  ```liquid
  {%- for property in item.properties -%}
    {%- assign property_first_char = property.first | slice: 0 -%}
    {%- if property.last != blank and property_first_char != '_' -%}
  ```
- `sections/main-cart-items.liquid:142-144`: identical pattern.

So `properties[Embroidery]` will display in the drawer **and** the cart page automatically, blank values won't show, and `_embroidery_for` (private link key for Option A) is correctly hidden. **No cart-snippet edits required.**

Checkout, admin order, packing slips, and order emails get line item properties natively.

---

## 5. Existing personalization / options / fee code — none conflicting

- Only existing line-item-property usage is `snippets/gift-card-recipient-form.liquid` (Shopify's native gift-card recipient feature — unrelated, no conflict).
- No embroidery code/assets exist yet (`grep -i embroider` → nothing).
- No third-party options/fee/personalization app code, no `upcharge`/`add-on`/`companion` references.
- No native `<dialog>`/`showModal` usage in the theme today — Dawn uses its own `modal-dialog` custom element elsewhere; our native `<dialog>` won't collide.
- Third-party apps in the theme (from project notes): Judge.me, Instafeed, DA Restock, Route Insurance, AccessEase. None touch the product form or line item properties. **No conflicts.**

---

## 6. Metafields currently defined

`.shopify/metafields.json` (definitions snapshot) shows product metafields: `reviews.rating`, `reviews.rating_count`, and Shopify discovery boosts/recommendations. **No `custom.embroidery_*` metafields exist yet** — they'll need to be created in the admin (Settings → Custom data → Products) as part of setup:

- `custom.embroidery_enabled` (boolean) — per-product gate.
- `custom.embroidery_price` (money or decimal) — the fee amount (optional; can fall back to a single configured value).
- `custom.embroidery_max_length` (integer) — char limit (optional; default ~50).

---

## 7. Client answers — RESOLVED

The four items I couldn't get from the repo, now answered by the client (notes in the doc):

| # | Question | Answer | Impact |
|---|---|---|---|
| 1 | **Shopify plan** | **Advanced** (not Plus) | Option C (Cart Transform) is **out** — it's Plus-only. Pricing must be Option A or B. |
| 2 | **Embroiderable products + variants** | Three "Sunday Brunch Mockneck" products (Dusty Blue, Seagull, White), each **$78 with 4 size variants** (S/M, M/L, L/XL, XL/XXL) — verified live via the `.js` endpoints | Existing size variants → **Option A**. Option B would explode to 4 sizes × (No/Yes) = **8 variants** per product, each needing its own inventory. Ruled out. |
| 3 | **Fee amount / structure** | **$20, flat, per embroidered item**, scaling with that line's quantity | Fee = **$20** encoded in the Option A fee product's price; fee line qty syncs to the embroidered line qty. |
| 4 | **Character limit** | **50** | `maxlength="50"` + clamp on save. No per-product override needed (so `custom.embroidery_max_length` is optional). |

**Verified variant structure** (live `https://hazelboutique.com/products/<handle>.js`):
- `the-sunday-brunch-mockneck-dusty-blue` — option **Size**; 4 variants (S/M, M/L, L/XL, XL/XXL); $78.
- `the-sunday-brunch-mockneck-seagull` — same: 4 size variants; $78.
- `the-sunday-brunch-mockneck-white` — same: 4 size variants; $78.

**Resolved:** client confirmed **three** products only — no 4th. All three are tagged `embroidery` (the live gate).

> All answers point the same way (not Plus + existing variants + flat $20). Pricing is locked in §8; **Phase 0 + Phase 1 are complete** (see §10) and the build (Phase 2+) can proceed.

---

## 8. Pricing mechanism — ⚠️ SUPERSEDED → see §14 (switched to Option B)

> **DIRECTION CHANGE (Phase 7 testing):** the client requires **the embroidered item's own price to adjust** (PDP + cart line read $98), not a separate fee line. Option A (below) cannot do that — Shopify forbids storefront line-price changes; only a higher-priced **variant (Option B)** or Plus-only Cart Transform (C) can. Plan is Advanced → **we pivot to Option B.** The Option A analysis below is kept for history; the live plan is **§14**.

### 8 (historical). Option A (companion fee product)

Decision, per `research-one.md` §3 and the §7 answers:

- Plan is **Advanced (not Plus)** → Option C (Cart Transform `lineUpdate`) is unavailable (Plus-only). ❌
- Products **already have 4 size variants each** → Option B ("No/Yes (+$20)" variant) would double them to **8 variants per product**, each needing inventory. Rejected as too messy. ❌
- → **Option A — companion "Embroidery fee" product.** ✅

**How Option A works here:**
- Create one hidden product **"Custom Embroidery"** priced at **$20.00** (one variant). Inventory tracking **off** (or "continue selling"); hidden from search, sitemap, and all collections so it can't be found/bought on its own; correct tax category.
- When the customer saves embroidery text and adds the mockneck to cart, also add **1× the $20 fee variant** in the **same** `/cart/add.js` `items:[...]` call, linked to the embroidered line via a private `_embroidery_for` key (idempotency + cleanup), then refresh the cart drawer via bundled section rendering.
- Keep the fee line's **quantity equal to** the embroidered line's quantity (since the fee is **$20 per item**). If the embroidered line is removed or embroidery is cleared, remove the fee line via `/cart/change.js`. Guard against double-adding on Edit/re-save.

**Fee amount source:** flat **$20**, encoded in the fee product's price (the source of truth for the charge). The on-page "(+$20.00)" label is **display only**, driven by a single configured value/theme setting (the `custom.embroidery_price` metafield was intentionally skipped — flat $20, no per-product variance).

**Per-product gate (LIVE):** product **tag `embroidery`** — already applied to the 3 mocknecks. The Phase-2 gate keys off this tag (and will also accept `custom.embroidery_enabled` if ever introduced).

**Setup artifacts (admin) — DONE:**
1. ✅ Hidden **"Custom Embroidery" $20 product** — handle `custom-embroidery`, **variant id `53563251753274`** (goes into theme setting `settings.embroidery_fee_variant_id`).
2. ✅ Gate via **`embroidery` tag** on the 3 products (no metafield needed).
3. — Display-price metafield: **skipped** (flat $20).

---

## 9. Proposed implementation shape (for approval)

1. **Gate** (1 line in `sections/main-product.liquid`, right after the `buy_buttons` render at line 449), keyed off the **live `embroidery` tag**:
   ```liquid
   {%- if product.tags contains 'embroidery' or product.metafields.custom.embroidery_enabled -%}
     {% render 'embroidery', product: product, section_id: section.id %}
   {%- endif -%}
   ```
   — the **only** core-theme-file edit; documented here for re-applying after Dawn updates.
2. **`snippets/embroidery.liquid`** (new, self-contained): hidden `properties[Embroidery]` input bound with `form="product-form-{{ section.id }}"`, `disabled` until non-empty text is saved; the "Custom Embroidery" trigger button styled with Dawn's `button button--secondary`; a native `<dialog>` modal with a textarea + char counter + Save/Remove; an on-page summary showing the text + **(+$20.00)**. Section-scoped vanilla JS, `textContent`-only preview (no `innerHTML`), `maxlength="50"` + clamp on save.
3. **Pricing wiring — Option A:** capture-phase intercept of the product form submit when `Embroidery` is set; add the mockneck (with `properties[Embroidery]`) **and** the **$20 fee variant `53563251753274`** (with `_embroidery_for` link key + matching qty) in one `/cart/add.js` call; refresh the drawer via `cart-drawer.renderContents`. Add a `cartUpdate` listener to keep fee qty in sync with the embroidered line and to remove the fee when the line is removed or embroidery cleared; idempotent on re-save.
4. **No cart-snippet edits** (already render properties).
5. Match Dawn CSS tokens/button classes; prefer an `assets/` file if I add non-trivial CSS/JS (the theme keeps JS in `assets/`).

**Live docs pulled (Phase 1, done):** Ajax Cart API + Liquid `properties` via Context7, reconciled against the theme JS — full contract in §11.

---

## Open items

All Phase 0/1 prerequisites are **resolved** (§7, §10). Nothing blocks the build. Remaining items are downstream:

1. ✅ Product scope — three products (dusty-blue, seagull, white), tagged `embroidery`.
2. ✅ Admin setup — fee product + variant id `53563251753274` done; gate via tag.
3. **Edge confirmations** still at v1 defaults (raise during build if needed): the $20 fee is taxed like a normal product and may be touched by cart discounts (Option A); one embroidery string per line at qty > 1 (per-unit text at qty 2+ is out of scope for v1).

**Next step:** Phase 2 — add the `embroidery_fee_variant_id` theme setting (= `53563251753274`) + the single gated render line in `sections/main-product.liquid`. Then Phases 3–7.

---

## 10. Implementation TODO — phased task list

Option A, Dawn v13.0.1. `[ ]` = not started. Phases are roughly sequential, but **Phase 0 (admin) and Phase 1 (docs)** can run in parallel before any theme code. **Nothing here is implemented yet.**

### Phase 0 — Admin setup & inputs (Shopify admin; client or me — no theme code)
_These produce the IDs/flags the code depends on. Build can start before they're all done, but go-live can't._

> **✅ Status: COMPLETE.** Fee product built ($20, variant `53563251753274`), 3 products tagged `embroidery`, tax set, display metafield skipped (flat $20). Nothing here blocks the build.

- [x] **0.1** ✅ **Resolved — three products only** (dusty-blue, seagull, white); no 4th.
- [x] **0.2** ✅ **Done by client.** Fee product **"Custom Embroidery"** ($20.00, handle `custom-embroidery`, product id `10321682399546`): inventory tracking **off**; **"unlisted"** (out of search/collections, still purchasable by direct URL — required for the Ajax add; `available: true` verified); correct **tax category**; simple/locked template.
- [x] **0.3** ✅ **Captured — fee variant id = `53563251753274`** (verified live via `custom-embroidery.js`). Goes into theme setting `settings.embroidery_fee_variant_id` (built in Phase 2.1).
- [x] **0.4** ✅ **Done by client — `embroidery` tag added to the 3 products.** The Phase-2 gate keys off this tag (and also accepts `custom.embroidery_enabled` if ever used).
- [x] **0.5** ✅ **Intentionally skipped.** Flat $20 across all products → no per-product display variance, so no metafield. Snippet uses a single configured `$20` (wired to the Phase-2 theme setting).
- [x] **0.6** ✅ **Tax category set** by client (taxable). Discountability + "one embroidery string per line at qty > 1" left at **v1 defaults** unless the client says otherwise.

### Phase 1 — Docs & reconciliation (no code) ✅ COMPLETE
_Full findings in §11._
- [x] **1.1** Context7 (`/websites/shopify_dev_storefronts_themes`): **Ajax Cart API** confirmed — `/cart/add.js` accepts a JSON `{ items: [...] }` array (multi-line add in one call) plus `sections` + `sections_url` for bundled section rendering; `/cart/change.js` takes `line`/`id` + `quantity` (+ `sections`).
- [x] **1.2** Context7: **line item properties** = inputs named `properties[Name]` on the product form; reconfirmed. Private `_`-prefixed keys persist to the order but are hidden on the storefront (already relied on by the cart loops — §4).
- [x] **1.3** Reconciled against live files (repo wins): `product-form-{{ section.id }}` form id (✓ buy-buttons.liquid:47), `product-form.js:36` `new FormData(this.form)` serializes `form=`-bound inputs (✓ Method A safe), cart property loops skip blanks + `_` keys (✓ cart-drawer.liquid:317, main-cart-items.liquid:142).
- [x] **1.4** Section-rendering contract mapped: dual-add requests `sections: ['cart-drawer','cart-icon-bubble']` + `sections_url`, then `document.querySelector('cart-drawer').renderContents(response)` (cart-drawer.js:86) renders + opens the drawer. Qty sync/cleanup hooks off `PUB_SUB_EVENTS.cartUpdate` (`"cart-update"`, constants.js:4) published by `cart.js` `updateQuantity`. Helpers: `fetchConfig('json')` (global.js:228), `window.routes.cart_add_url`/`cart_change_url` (theme.liquid:447-449), `window.Shopify.routes.root`.

### Phase 2 — Theme setting & enablement gate ✅ COMPLETE
_Theme check: 209 files, 5 offenses / 1 error / 4 warnings — unchanged from baseline (no new issues). Edits confined to settings_schema.json, main-product.liquid, and the new snippet._
- [x] **2.1** ✅ Added a **"Custom Embroidery"** settings group to `config/settings_schema.json`: `embroidery_fee_variant_id` (text, default `53563251753274`), `embroidery_price` (number, default `20` — display label only), `embroidery_max_length` (number, default `50`). Valid JSON confirmed (23 groups).
- [x] **2.2** ✅ Added the **single core-theme edit** in `sections/main-product.liquid` (after the `buy_buttons` render, before `.product__installment`): gated `{% render 'embroidery' %}` on `product.tags contains 'embroidery' or product.metafields.custom.embroidery_enabled`. See §13 for the exact diff.
- [x] **2.3** ✅ Documented the exact edit in the **Theme-update re-apply note (§13)** for re-applying after Dawn updates.
- [x] **2.x** ✅ _Supporting:_ created a **minimal valid `snippets/embroidery.liquid`** (params → `data-*`, bound `properties[Embroidery]` hidden input, trigger button) so the render target resolves and theme check stays green. **Modal + summary + JS + a11y are still Phase 3** (boxes below remain open).

### Phase 3 — `snippets/embroidery.liquid` (UI + text capture) ✅ COMPLETE
_JS in `assets/embroidery.js` (deferred, theme convention), config via `data-*`. `node --check` passes; theme check unchanged from baseline (no new offenses)._
- [x] **3.1** ✅ Snippet scaffold + Accepts comment (`product`, `section_id`); reads `max_len` (50), `fee` (20), `fee_variant_id`, plus `fee_money = fee | times: 100 | money` for the label, into `data-*` attrs.
- [x] **3.2** ✅ Hidden `name="properties[Embroidery]"`, `form="product-form-{{ section_id }}"`, **`disabled`** until saved, id `embroidery-value-{{ section_id }}`.
- [x] **3.3** ✅ Trigger **"Custom Embroidery"** button (`button button--secondary`, `type="button"`), rendered beside Add to Cart.
- [x] **3.4** ✅ Native **`<dialog>`** modal: labeled `<textarea maxlength="{{ max_len }}">`, live `0/50` counter, **Save** / **Remove**, fee in the heading.
- [x] **3.5** ✅ On-page **summary** (`Embroidery: "…" (+$20.00)` + Edit), `hidden` until saved; populated via `textContent` only (no `innerHTML`).
- [x] **3.6** ✅ Section-scoped IIFE over `[data-embroidery]` (per-root `data-embroidery-init` guard): open/edit/close, counter, `applyValue()` (trim+clamp → enable field + show summary + hide open btn, or clear → disable field + hide summary + show open btn), clamp to `maxLen` on save, re-disable on clear.
- [x] **3.7** ✅ A11y: native `<dialog>` (`showModal()` focus trap + Esc), labeled field, backdrop-click close, focus returns to the visible control on close (open btn after Remove, Edit link after Save).
- [x] **3.8** ✅ Default scope — allow all characters, **clamp length only** (no machine-charset stripping). Easy to add later if the embroiderer needs it; flagged for client confirmation, not blocking.

> **Intermediate state after Phase 3:** saving text enables the bound input, so a native Add to Cart already carries `properties[Embroidery]` to cart/checkout/admin. **The $20 fee is NOT wired yet — that's Phase 4** (capture-phase intercept + dual-add + qty sync).

### Phase 4 — Pricing wiring (Option A: companion fee product + sync) ✅ COMPLETE
_All in `assets/embroidery.js`. `node --check` passes; theme check unchanged from baseline. No core-theme JS patched — interception is a capture-phase listener._
- [x] **4.1** ✅ **Capture-phase `submit` listener on `document`** (`onCaptureSubmit`, installed once via `window.__embroiderySetup`). Looks up the form-bound `[data-embroidery-field]` by the form's id; if absent/disabled/empty it returns and Dawn handles the add normally. When embroidery is set, `preventDefault()` + `stopImmediatePropagation()` blocks Dawn's own form listener (which runs in the target phase, after capture) — no `product-form.js` edit, no double-submit.
- [x] **4.2** ✅ One `/cart/add.js` (`window.routes.cart_add_url`) with `items: [ {id: mockneck, qty, properties:{Embroidery, _embroidery_key}}, {id: fee 53563251753274, qty: same, properties:{_embroidery_for}} ]`. `id`/`quantity` read via `new FormData(form)` (correct because Dawn's quantity input is bound by `form=`, not nested — confirmed main-product.liquid:253).
- [x] **4.3** ✅ Refresh via `cart.renderContents(response)` (drawer/notification element), requesting `sections = cart.getSectionsToRender().map(id)` + `sections_url`; then `publish(cartUpdate, {source:'product-form', cartData})` — mirrors Dawn's own add flow.
- [x] **4.4** ✅ Link key = `<variantId>:<base36 time + rand>`. Embroidered line carries `_embroidery_key`; fee line carries `_embroidery_for` = same key. 1:1, and two same-variant lines with different text get distinct keys (separate fee lines).
- [x] **4.5** ✅ Qty sync via `subscribe(cartUpdate, onCartUpdate)` → `reconcile(cart)` matches each embroidered line to its fee by key and, on quantity mismatch, `/cart/change.js` sets fee qty = item qty. Works for drawer **and** cart page (both publish `cartUpdate`). Re-entrancy guarded by a `syncing` flag + a private `embroidery-sync` source that the handler ignores.
- [x] **4.6** ✅ Cleanup in the same `reconcile`: a fee whose embroidered line is gone is removed (`change.js` qty 0). Clearing embroidery before add → field disabled → no fee added.
- [x] **4.7** ✅ Idempotent: the fee is only ever added in the single dual-add; `reconcile` **only adjusts/removes**, never adds — so re-Save/Edit and repeated cart updates can't create a second fee.
- [x] **4.8** ✅ Variant switch: the bound field persists (tied to form id); the add reads the **currently selected** variant from `FormData(form).get('id')` at submit time.

> **Known v1 limitation (flag to client):** the fee is a normal cart line, so a customer *could* manually delete only the "Custom Embroidery" line and keep the item — `reconcile` never re-adds (by design, for idempotency), so that item would ship without the surcharge. Hardening (hide the fee line's remove control) requires editing cart snippets, which the project constraints say to avoid. Acceptable for v1; revisit if it becomes a problem.
>
> **Intermediate state after Phase 4:** functionally complete — text + $20 fee flow to cart/checkout/admin, qty stays in sync, removal cleans up. Remaining: **Phase 5 styling** (native look; modal is currently unstyled native `<dialog>`) and **Phase 6–7 verification**.

### Phase 5 — Styling (native look) ✅ COMPLETE
_New `assets/embroidery.css`, loaded via `{{ 'embroidery.css' | asset_url | stylesheet_tag }}` in the snippet. Theme check unchanged from baseline._
- [x] **5.1** ✅ Uses Dawn tokens: `rgb(var(--color-foreground))`/`--color-background`, `--inputs-radius`/`--inputs-border-width`/`--inputs-border-opacity`, `--font-heading-family`/`--font-body-family`, and the native focus ring `outline: 0.2rem solid rgba(var(--color-foreground), 0.5)`. Trigger button uses real Dawn classes `button button--secondary button--full-width` so it stacks under Add to Cart like the native buy buttons (`margin-top: 1rem`). Modal inherits the section's color scheme via CSS vars.
- [x] **5.2** ✅ Both CSS and JS live in `assets/` (`embroidery.css`, `embroidery.js`) per theme convention — nothing non-trivial left inline; the snippet only loads them.
- [x] **5.3** ✅ Mobile: dialog `width: 90vw` (→ `94vw` ≤480px), `max-width: 46rem`, `max-height: 90vh` + `overflow: auto` for scroll; action buttons stack full-width (`column-reverse`) on small screens.

### Phase 6 — Cart display (verify only; expect no edits) ✅ COMPLETE — NO EDITS
- [x] **6.1** ✅ Verified both loops (`cart-drawer.liquid:317-338`, `main-cart-items.liquid:142-158`): `{%- if property.last != blank and property_first_char != '_' -%}` renders non-blank, non-`_` keys as `<dt>{{ property.first }}:</dt><dd>{{ property.last }}</dd>`. So `Embroidery` shows on the drawer **and** cart page; `_embroidery_key` (item) and `_embroidery_for` (fee) are hidden. `{{ property.last }}` is Liquid-auto-escaped → XSS-safe. (Both loops also special-case `/uploads/` file links — irrelevant to free-text embroidery.)
- [x] **6.2** ✅ Not needed — no surface strips the property; **zero cart-snippet edits**, satisfying the "don't touch cart rendering unless necessary" constraint.

> Static template verification only (reading the Liquid). Live render across drawer/cart/checkout/admin is exercised in **Phase 7** (needs a theme preview).

### Phase 7 — Testing (per `research-one.md` §10) & handoff
**Text capture & display**
- [ ] **7.1** Button shows **only** on enabled products; nowhere else.
- [ ] **7.2** Modal opens, accepts text, enforces 50-char max + counter; Save shows summary; Remove/empty hides it and attaches **no** property.
- [ ] **7.3** Add to cart: text in **drawer** and **cart page**; checkout, **admin order**, packing slip, order email all show it.
- [ ] **7.4** Two same products w/ different text = **two separate lines**; non-embroidery product adds **no blank** property.
- [ ] **7.5** Variant switch keeps text; qty behaves as agreed.

**Upcharge**
- [ ] **7.6** Saving embroidery adds **$20**; cart subtotal/total reflect it; correct at checkout and on **admin order total**.
- [ ] **7.7** Clearing embroidery or removing the item **removes** the fee.
- [ ] **7.8** Changing embroidered-line qty keeps fee qty **in sync**.
- [ ] **7.9** **No double-charge** on Edit/re-save (idempotency).
- [ ] **7.10** Fee product **can't be found/bought** on its own (search/sitemap/collections).
- [ ] **7.11** Taxes/discounts on the fee behave as client expects.

**General / handoff**
- [ ] **7.12** Works on mobile; modal keyboard- + screen-reader-accessible (Esc closes, focus returns).
- [ ] **7.13** Commit on a feature branch; keep edits minimal/version-controlled.
- [ ] **7.14** Write the **"theme-update re-apply" note**: the one `main-product.liquid` render line + how to re-add after a Dawn update.
- [ ] **7.15** Client walkthrough: how to enable a new product (set `custom.embroidery_enabled`), and the fee-product/variant-id dependency.

---

## 11. Phase 1 findings — live docs + Dawn JS reconciliation (the integration contract)

Source of truth = the live theme JS (reconciled with Context7 `/websites/shopify_dev_storefronts_themes`). This is everything Phase 3–4 will build against.

### 11.1 Add-to-cart flow (Dawn `assets/product-form.js`)
- `product-form.js:36` builds `new FormData(this.form)` on submit → a hidden input with `form="product-form-{{ section.id }}"` **is serialized even though it lives outside the `<form>`**. Method A confirmed; no `product-form.js` edit needed for the text.
- It appends `sections` (from `cart.getSectionsToRender()`) + `sections_url`, POSTs to `routes.cart_add_url`, then `this.cart.renderContents(response)` (drawer) on success.
- The native handler adds **one** variant (the FormData). For Option A's single dual-add I'll **intercept** the form's `submit` in the **capture phase** and `preventDefault()` + `stopImmediatePropagation()` when `properties[Embroidery]` is set+enabled — this blocks Dawn's bubble-phase handler **without monkey-patching `product-form.js`** (upgrade-safe), then I run my own dual-add.

### 11.2 Dual-add (Ajax Cart API)
- `POST {{ routes.cart_add_url }}` with `fetchConfig('json')` headers and a JSON body:
  ```js
  { items: [
      { id: <mockneckVariantId>, quantity: q, properties: { Embroidery: text } },
      { id: <feeVariantId>,      quantity: q, properties: { _embroidery_for: <linkKey> } }
    ],
    sections: ['cart-drawer', 'cart-icon-bubble'],
    sections_url: window.location.pathname }
  ```
- One call keeps the two lines adjacent and avoids a flash of the item without its fee.
- On success: `document.querySelector('cart-drawer').renderContents(response)` — `cart-drawer.js:86` reads `response.sections['cart-drawer']` + `['cart-icon-bubble']`, swaps them in, and opens the drawer. (Falls back to `cart-notification` when the theme isn't in drawer mode — here it's drawer.)

### 11.3 Quantity sync + cleanup (Dawn `assets/cart.js`)
- Line qty changes go through `CartItems.updateQuantity()` → `POST routes.cart_change_url` `{ line, quantity, sections, sections_url }`, then it `publish(PUB_SUB_EVENTS.cartUpdate, { source: 'cart-items', cartData })`.
- **Hook:** `subscribe(PUB_SUB_EVENTS.cartUpdate, …)`. On each update, read `cartData` (or fetch `/cart.js`), then for every line with `properties.Embroidery`, ensure its linked fee line (`properties._embroidery_for === linkKey`) has **matching quantity**; if the embroidered line is gone, `change.js` the fee line to `quantity: 0`. **Re-entrancy guard** required (my own `change.js` triggers another `cartUpdate`).
- `PUB_SUB_EVENTS.cartUpdate === "cart-update"` (constants.js:4). `fetchConfig('json')` = `{ method:'POST', headers:{'Content-Type':'application/json', Accept:'application/json'} }` (global.js:228). Routes: `window.routes.{cart_add_url,cart_change_url,cart_url}` (theme.liquid:447-451); `window.Shopify.routes.root` for locale-safe paths.

### 11.4 Linking key (`_embroidery_for`)
- Must map a fee line 1:1 to its embroidered line and survive two same-variant lines with different text. Plan: a value combining the mockneck variant id + a short nonce generated at add time, stored on **both** lines (readable on the embroidered line as `_embroidery_for` too, or matched by the fee line's key → embroidered line key). Private `_` prefix keeps it off the storefront (cart loops skip it) but on the order for our logic. Idempotency on re-Save/Edit = match existing fee line by this key instead of adding a second.

### 11.5 Cart display — no edits (confirmed §4)
- `cart-drawer.liquid:317-319` and `main-cart-items.liquid:142-144` already loop `item.properties`, render non-blank, skip `_`-prefixed. `Embroidery` shows; `_embroidery_for` stays hidden. Checkout/admin/packing-slip/email are native.

---

## 12. Phase 0 admin runbook (turn-key — execute in Shopify admin)

⛔ **I can't run these from the theme repo** (no Admin API token/session; the theme CLI has no product/metafield-create command; and it's a production store). Hand to the client or run with an Admin API token + go-ahead.

> **Progress:** 12.1 (fee product) ✅ done. 12.2 (variant id `53563251753274`) ✅ captured. **Only 12.3 remains** (enable the 3 products); 12.4 optional.

### 12.1 Create the fee product
1. **Admin → Products → Add product.**
2. **Title:** `Custom Embroidery`. **Description:** short (e.g. "Personalization fee for embroidered items — added automatically.").
3. **Pricing → Price:** `20.00`. Leave "Charge tax on this product" **as the client wants** (default: taxed like apparel).
4. **Inventory:** **uncheck** "Track quantity" (or check "Continue selling when out of stock"). Clear/zero SKU is fine.
5. **Shipping:** uncheck "This is a physical product" (the fee ships nothing).
6. **Search engine listing / visibility:**
   - **Sales channels:** keep Online Store published (the Ajax add needs it purchasable) **but**…
   - **Theme template:** assign a **minimal/locked template** (e.g. duplicate `product.json` → `product.embroidery-fee.json` stripped to nothing meaningful) so the PDP can't be used to buy it standalone.
   - **Exclude from search & sitemap:** add a tag or use an SEO/noindex setting; **do not add it to any collection**; if the store has a "hidden" pattern, follow it. (Goal: not findable/browsable.)
7. **Save.**

### 12.2 Capture the fee variant id
- Open the product → the single variant → copy the numeric **Variant ID** from the URL (`.../variants/<ID>`), or fetch `https://hazelboutique.com/products/custom-embroidery.js` and read `variants[0].id`.
- This value goes into the theme setting `settings.embroidery_fee_variant_id` (added in Phase 2.1). **Send it to me.**

### 12.3 Enable the 3 products (← the one remaining Phase 0 step)
Pick **either** path; the Phase-2 gate accepts both.
- **Simplest — tag:** on each of the 3 mocknecks (dusty-blue, seagull, white), add the product **tag `embroidery`**. Done.
- **Cleaner — metafield:** **Admin → Settings → Custom data → Products → Add definition** → Name `Embroidery enabled`, key `custom.embroidery_enabled`, Type **True/False**. Save, then set it **true** on each of the 3 products.

### 12.4 (Optional) Display-price metafield
- Same flow: **Name** `Embroidery price`, key `custom.embroidery_price`, **Type Money** (or Decimal), set to `20.00` per product. Only drives the on-page "(+$20.00)" label; the real charge is the fee product's price. If skipped, the snippet falls back to a configured `20`.

### 12.5 Hand back to me
Provide: (a) the **fee variant id** (12.2) — ✅ done (`53563251753274`), (b) ~~4th product handle~~ — ✅ three only, (c) tax/discount preference (0.6) — ✅ tax set. Phases 2–7 can complete end-to-end.

---

## 13. Theme-update re-apply note (core-theme edits — FINAL, Option B)

Self-contained files: `snippets/embroidery.liquid`, `assets/embroidery.js`, `assets/embroidery.css`, and the `config/settings_schema.json` "Custom Embroidery" group (these survive Dawn updates). **Three** edits touch Dawn core files — re-apply them after any Dawn update that overwrites those files:

**Edit 1 — `sections/main-product.liquid`** (the gated render). Inside the `{%- when 'buy_buttons' -%}` block, after `{%- render 'buy-buttons' … -%}`, before `<p class="product__installment caption">`:
```liquid
                {%- if product.tags contains 'embroidery' or product.metafields.custom.embroidery_enabled -%}
                  {% render 'embroidery', product: product, section_id: section.id %}
                {%- endif -%}
```

**Edit 2 — `snippets/cart-drawer.liquid`** and **Edit 3 — `sections/main-cart-items.liquid`** (hide the `Embroidery` variant option in the cart). In each `{%- for option in item.options_with_values -%}` loop, wrap the `<div class="product-option">` in:
```liquid
{%- assign embroidery_option_name = settings.embroidery_option_name | default: 'Embroidery' -%}
{%- for option in item.options_with_values -%}
  {%- unless option.name == embroidery_option_name -%}
    … existing option markup …
  {%- endunless -%}
{%- endfor -%}
```

**Dependencies (not in core files):**
- `config/settings_schema.json` → "Custom Embroidery" group: `embroidery_option_name` (`Embroidery`), `embroidery_yes_value` (`Embroidered`), `embroidery_no_value` (`Standard`), `embroidery_price` (20, display), `embroidery_max_length` (50).
- Products gated by the **`embroidery` tag** (or `custom.embroidery_enabled`), each with an **`Embroidery` product option** (`Standard` / `Embroidered`); `Embroidered` variants priced +$20 and continue-selling.
- (Option A's fee product `custom-embroidery` is **obsolete** — delete/unpublish it.)

**Verify after re-applying:** `shopify theme check` at baseline; button renders only on tagged products; Save→$98 / Remove→$78; cart shows only `Embroidery: <text>` (no `Embroidery: Standard/Embroidered` row).

---

## 14. ACTIVE PLAN — Option B (variant-priced embroidery)

**Why:** client requires the embroidered item's **own price** to increase (PDP + cart line = $98). Only a higher-priced variant achieves this on a non-Plus plan. Replaces Option A.

### 14.1 Mechanism
- Each embroiderable product gains an **`Embroidery` option** with values **`No` / `Yes`**. The `Yes` variants are priced **+$20** (so $78 → **$98**); `No` variants stay $78.
- The option selector is **hidden** in the theme. The modal drives it: **Save** → set the hidden `Embroidery` option input to **Yes** and dispatch the native `change` (Dawn re-selects the same-size `Yes` variant, updates the PDP price to $98 and the form's variant id); **Remove** → set back to **No** (price reverts to $78).
- The embroidery **text still rides** as `properties[Embroidery]` (Phase 3 input unchanged). Add to cart is **Dawn's native add** — no interception, no fee line, no qty-sync.
- **No hardcoded variant IDs** — Dawn maps the selected options (`Size` + `Embroidery`) to the right variant. The JS only needs the **option name** (`Embroidery`) and the **Yes value** (`Yes`), both configurable.

### 14.2 What carries over (no change)
- Phase 3 snippet UI (button, `<dialog>`, summary, char counter) and the `properties[Embroidery]` bound input.
- Phase 5 CSS. Phase 6 cart display (properties already render; `_` keys hidden — note Option B no longer uses `_embroidery_*` keys at all).
- `embroidery` **tag** gate; `embroidery_max_length` (50), `embroidery_price` (20, display label only).

### 14.3 What's removed / replaced
- **Remove** the Option A JS in `assets/embroidery.js`: capture-phase submit intercept, dual-add, `reconcile`/qty-sync, fee logic. Replace with variant-switch logic (set option → dispatch `change`; sync modal state from the current variant on load).
- **Remove** `embroidery_fee_variant_id` setting; **add** `embroidery_option_name` (default `Embroidery`) and `embroidery_yes_value` (default `Yes`).
- **Retire** the `custom-embroidery` fee product (delete or leave unpublished — no longer added to cart).
- Hide the `Embroidery` option selector in the product form (CSS, scoped to the option block).

### 14.4 Admin prerequisites (client — live store; I can't do these from here)
For **each** of the 3 products (dusty-blue, seagull, white):
1. Add a product **option `Embroidery`** with values **`No`** and **`Yes`** (existing size variants become the `No` set).
2. Set every **`Yes` variant price = $98.00** (the `No` variants stay $78.00).
3. Set the `Yes` variants' **inventory policy** per the decision below.
4. Ensure **`No`** is the **default/first** value so the PDP loads at $78.

### 14.5 Decisions needed before coding
- **Inventory on the `Yes` variants:** untracked, or "continue selling when out of stock"? (Recommend **untracked** so embroidery availability isn't separately capped.)
- **Option/value labels:** keep `Embroidery: No / Yes`? (The variant title — e.g. `S/M / Yes` — will appear in cart/checkout/admin alongside the `Embroidery: <text>` property. Alternative labels like `No / Embroidered` read nicer on the order; your call.)
- Confirm the **+$20** delta ($98) is correct for all three.

### 14.6 Revised task list
- [ ] **B0** ⛔ _Pending (client, live store)._ Add the `Embroidery` option (`No`/`Yes`) + price `Yes` variants $98 + inventory, on all 3 products (14.4). Theme code ships first (degrades gracefully until this lands), then B0 activates the price switch on next page load — no redeploy needed.
- [x] **B1** ✅ Settings: removed `embroidery_fee_variant_id`; added `embroidery_option_name` (default `Embroidery`), `embroidery_yes_value` (`Yes`), `embroidery_no_value` (`No`). Kept `embroidery_price` (20, display) + `embroidery_max_length` (50).
- [x] **B2** ✅ Snippet: dropped `data-fee-variant-id`; added `data-section-id`, `data-option-name`, `data-yes-value`, `data-no-value`. Fee label still from `embroidery_price` (display only). Modal + `properties[Embroidery]` input unchanged.
- [x] **B3** ✅ CSS: `embroidery.css` hides the option block via `.product-form__input:has(select[name="options[Embroidery]"]), …:has(input[name="Embroidery"])` (FOUC-safe); JS also hides it as a guaranteed/configurable fallback.
- [x] **B4** ✅ JS rewritten (`assets/embroidery.js`): **all Option A wiring removed** (no submit intercept, no dual-add, no fee, no qty-sync). On Save → set the hidden `Embroidery` option to `Yes` + dispatch native `change` (Dawn re-selects the `$98` variant, updates `[name="id"]` + price element); on Remove → set `No`. Verified via global.js that `renderProductInfo` only swaps price/sku/inventory/button (not the embroidery DOM), and `updateOptions()` reads hidden `select, fieldset` (so a `display:none` option still works). Add to cart is Dawn-native. Modal/counter/clamp/a11y retained. Degrades gracefully when the option is absent (text still captured, no price change, no errors). `node --check` + `shopify theme check` clean (baseline unchanged).
- [ ] **B5** ⛔ _Pending verification (needs B0 + a preview)._ PDP price 78→98 on Save and 98→78 on Remove; cart line = $98; text shows; two same-size + different text = 2 lines; size switch keeps embroidery state.

### 14.8 Cart display fix + checkout caveat (Option B side effect)
Because the price now lives in an `Embroidery: No/Yes` **variant option**, the cart line would otherwise show that option *and* the `Embroidery` text property — two "Embroidery:" rows.
- **Fixed (theme):** `sections/main-cart-items.liquid` and `snippets/cart-drawer.liquid` now **skip the option** whose name == `settings.embroidery_option_name` (default `Embroidery`) in the `options_with_values` loop. Result: the cart shows only `Embroidery: <text>` (the property); normal purchases no longer show `Embroidery: No`. (These are 2 additional core-theme edits — add to the re-apply note alongside the §13 render line.)
- **⚠️ Caveat (not fixable on non-Plus):** the **Shopify checkout page and the admin order** display the **variant title**, which for Option B includes the option value — `S/M / Yes` for embroidered, `S/M / No` for standard. This can't be hidden from the hosted checkout without Shopify Plus checkout customization. For fulfillment `/ Yes` is actually a useful "this one is embroidered" flag; `/ No` on standard orders is minor noise.
  - **Chosen:** option values are **`Standard` / `Embroidered`** (so checkout/order read `S/M / Standard` and `S/M / Embroidered`). Theme settings updated to match: `embroidery_no_value = "Standard"`, `embroidery_yes_value = "Embroidered"` (option name stays `Embroidery`). Admin values must match these strings exactly (case-sensitive).

### 14.7 Testing checklist deltas (supersedes §10 Phase 7 "Upcharge")
- [ ] Saving embroidery raises the **PDP price** to $98; Remove reverts to $78.
- [ ] Cart/checkout/admin show the **line at $98** (no separate fee line) **plus** the `Embroidery: <text>` property.
- [ ] Changing **size** while embroidery is on keeps it on (stays on a `Yes` variant of the new size).
- [ ] `Yes` variants aren't separately purchasable in a broken way (option hidden; inventory per decision).
