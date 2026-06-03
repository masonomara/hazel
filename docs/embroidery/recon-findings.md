# Custom Embroidery — Recon Findings & Proposed Plan

_Step 1 deliverable. No code changed yet. Reconciled against the live repo (the repo wins over any doc)._

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

## 7. Items I CANNOT determine from the repo — need the client

These block the pricing decision and final config. **Please confirm before I code:**

1. **Shopify plan** (Settings → Plan). This picks the pricing mechanism — Cart Transform price changes (Option C) are **Shopify Plus-only**. My default assumption below is **not Plus**.
2. **Which products are embroiderable, and do they already have many variants** (size/color)? This decides Option A vs Option B. The repo doesn't identify embroidery products, and I can't query the live store from here.
3. **Fee amount**, and: **flat per item vs per character**, and **per embroidered item vs per order**. Research default = flat fee per embroidered item, scaling with that line's quantity.
4. **Real embroidery character limit** from the embroiderer (default 50 if unknown).

<!-- 1. shopify plan in "advanced" - not plus. -->
<!-- 2. i have four products that need to be embroiderable: https://hazelboutique.com/products/the-sunday-brunch-mockneck-dusty-blue, https://hazelboutique.com/products/the-sunday-brunch-mockneck-seagull, and https://hazelboutique.com/products/the-sunday-brunch-mockneck-white. -->
<!-- 3. $20 per embroidery per item -->
<!-- 4. default 50 characters -->

---

## 8. Proposed pricing mechanism (pending plan confirmation)

Per `research-one.md` §3:

- **If NOT Plus (assumed default) → Option A: companion "Embroidery fee" product.**
  Add a hidden "Custom Embroidery" product (priced at the fee) to the cart alongside the embroidered item in one `/cart/add.js` `items:[...]` call, linked via a private `_embroidery_for` key and quantity-synced via JS. Works on every plan. This is the default for arbitrary products with existing variants.
  - _Switch to **Option B** (an "Embroidery: No / Yes (+$X)" variant) instead **iff** the embroiderable products have few/no existing variants — single line item, no sync logic, but it multiplies variants across every size/color._
- **If Plus → Option C: Cart Transform `lineUpdate` function** in a custom app — surcharges the embroidered line directly, no extra line. Cleanest, but requires building/deploying an app + Function.

**Fee amount source:** `custom.embroidery_price` metafield (per-product), falling back to a single configured value. **Per-product gate:** `custom.embroidery_enabled` boolean metafield (preferred), with a `embroidery` tag as fallback.

---

## 9. Proposed implementation shape (for approval)

1. **Gate** (1 line in `sections/main-product.liquid`, right after the `buy_buttons` render at line 449):
   ```liquid
   {%- if product.metafields.custom.embroidery_enabled -%}
     {% render 'embroidery', product: product, section_id: section.id %}
   {%- endif -%}
   ```
   — the **only** core-theme-file edit; documented here for re-applying after Dawn updates.
2. **`snippets/embroidery.liquid`** (new, self-contained): hidden `properties[Embroidery]` input bound with `form="product-form-{{ section.id }}"`, `disabled` until non-empty text is saved; the "Custom Embroidery" trigger button styled with Dawn's `button button--secondary`; a native `<dialog>` modal with a textarea + char counter + Save/Remove; an on-page summary showing the text + fee. Section-scoped vanilla JS, `textContent`-only preview (no `innerHTML`), clamp to max length.
3. **Pricing wiring** per the confirmed option (A: add+sync fee variant via Ajax + section rendering; B: variant swap; C: scaffold the Function).
4. **No cart-snippet edits** (already render properties).
5. Match Dawn CSS tokens/button classes; prefer an `assets/` file if I add non-trivial CSS/JS (the theme keeps JS in `assets/`).

**Before coding I'll pull live docs via Context7** (Ajax Cart API, Liquid `line_item`/`properties`, and — if Plus — the Cart Transform Function API) and reconcile against these files.

---

## Blocking questions (need answers to proceed)

1. What **Shopify plan** is the store on (Plus or not)?
2. Which products get embroidery, and **do they already have size/color variants**?
3. **Fee amount**, and is it **flat per item** (scaling with qty) or per character / per order?
4. **Character limit** for the embroidery text?
