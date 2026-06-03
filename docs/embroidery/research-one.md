# Custom Embroidery (with Upcharge) — Solution Research

**Client:** Hazel Boutique (`hazelboutique.com` → `hazelboutiquenj.myshopify.com`)
**Platform:** Shopify (confirmed)
**Goal:** A "Custom Embroidery" button beside *Add to Cart* on selected products. Clicking it opens a modal with a single free-text field. The entered text must appear (1) on the product page, (2) in the cart, and (3) on the order in the Shopify admin / shipping docs. Adding embroidery must apply an **upcharge** (extra fee). **Text only** — no fonts, no live preview, no image upload.

---

## TL;DR Recommendation

Two concerns, two mechanisms:

**1. Capturing & displaying the text → Shopify line item properties (native, no app).**
A line item property (`properties[Embroidery]`) added to the product form flows **automatically** to the cart, checkout, the order in admin, packing slips, and order emails. The button + modal is just a UI layer that writes the text into a hidden `properties[Embroidery]` input bound to the add-to-cart form, so it rides through the AJAX cart. Gate it per-product with a metafield (recommended) or a tag.

**2. The upcharge → depends on the store's Shopify plan.** Line item properties do **not** change price, and the clean native way to raise a line's own price (Shopify Functions **Cart Transform `lineUpdate`**) is **Shopify Plus–only**. So:
- **Not on Plus (most likely): add a companion "Embroidery fee" product** to the cart alongside the item, linked + quantity-synced via JS. Works on every plan. This is what personalization apps (Customily, Teeinblue, Easify "Add-on Product") do under the hood.
- **On Plus: use a Cart Transform `lineUpdate` function** to surcharge the embroidered line directly — cleanest UX, no extra cart line, but requires a custom app + Function.

**Step 0 for the agent: determine the store's Shopify plan** (Settings → Plan, or ask the client). It decides the pricing path.

**Implementation shape:** a self-contained theme snippet (`snippets/embroidery.liquid`) rendered near the buy buttons, a per-product metafield for enablement (and optionally the price), plus the chosen pricing mechanism. Right weight for one store and a few products. (A Theme App Extension is the scalable alternative — see §8.)

Do **not** prefix the property key with an underscore. In Shopify, `properties[_Foo]` is a *private* property hidden from the storefront. The client wants it visible everywhere, so use a plain key like `Embroidery`. (Underscore keys are still useful for *internal* linking metadata on the fee line — see §3.)

---

## 1. How line item properties work (the core mechanism)

Any input inside (or bound to) the add-to-cart form whose `name` is `properties[Something]` becomes a line item property:

```html
<input type="text" name="properties[Embroidery]" value="Hello">
```

What you get for free once it's in the cart:

| Surface | Visible automatically? | Notes |
|---|---|---|
| Cart page / cart drawer | Yes (Dawn & most OS 2.0 themes) | Themes loop over `item.properties` and render them under the line title. Blank values and keys starting with `_` are skipped. |
| Checkout | Yes | Shown under the line item. |
| Order in Shopify admin | Yes | Listed under each line item's details. |
| Default packing slip | Yes | Shopify's default order/packing-slip templates print line item properties. |
| Order confirmation email | Yes | Default notification templates include line item properties. |
| Third-party shipping/fulfillment apps | Usually, sometimes needs config | Most read line item properties; a few need a setting toggled to print them on labels/slips. Verify with the client's tooling. |

Authoritative behavior (Shopify Ajax Cart API reference):
- Properties travel with the line through `/cart/add.js`, `/cart/change.js`, etc.
- Two otherwise-identical units with **different** properties stay **separate line items** — good, so two shirts with different embroidery don't collapse into qty 2.
- Underscore-prefixed keys (`_foo`) are *private* — present in Liquid/Ajax/admin but hidden on the storefront unless the theme renders them.

---

## 2. The one real gotcha for the text: the AJAX cart

Modern themes (Dawn and descendants) add to cart via **AJAX**. A custom input only rides along if it's part of the serialized form.

### Method A — bind the input to the product form via the `form` attribute (recommended for the text)

```liquid
{%- assign product_form_id = 'product-form-' | append: section.id -%}
<input
  type="hidden"
  name="properties[Embroidery]"
  id="embroidery-value-{{ section.id }}"
  form="{{ product_form_id }}"
  value=""
  disabled>
```

The `form="..."` attribute makes the browser serialize this input as part of that form, so Dawn's AJAX add-to-cart picks it up with **no** changes to `product-form.js`. Upgrade-safe and community-blessed.

> **Critical — the form id is theme-specific. Detect it; don't assume.**
> - **Dawn** (and most forks): `product-form-{{ section.id }}`
> - **Horizon** (Shopify's newest default theme): `BuyButtons-ProductForm-{{ section.id }}`
> - Verify by inspecting the rendered `<product-form>` / `<form>` id in `sections/main-product.liquid` (or the buy-buttons block). The integration hinges on this id.

> **Keep empty values out of orders.** The `disabled` attribute means the input isn't submitted until the modal JS enables it (only when non-empty text is saved). So a product where nobody opens the modal attaches no blank `Embroidery` property.

### Method B — POST to `/cart/add.js` yourself (used by the fee approach in §3, Option A)

```js
fetch(window.Shopify.routes.root + 'cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    items: [{ id: variantId, quantity: 1, properties: { Embroidery: text } }]
  })
});
```

Use `window.Shopify.routes.root` (not a hardcoded path) for localized/multi-region stores. Method B means you also own refreshing the cart drawer (use the Ajax API's bundled **section rendering** to re-render the cart sections).

---

## 3. The upcharge — three mechanisms; pick by plan

**Why this is separate work:** Shopify won't let the storefront change a product's price arbitrarily. The only way to alter a line's *own* price programmatically — Cart Transform `lineUpdate` — is **restricted to Shopify Plus (and development) stores** (confirmed in the Cart Transform API docs). So first establish the plan, then pick:

### Option A — Companion "Embroidery fee" product  *(works on every plan — recommended default)*
- Create a product, e.g. **"Custom Embroidery"** priced at the upcharge (say $10). Turn inventory tracking off (or "continue selling"); hide it from search, the sitemap, and all collections; give it a minimal/locked template so it can't be bought meaningfully on its own.
- When the customer saves embroidery text and adds to cart, **also add 1× the fee product**, linked to the embroidered line.
- **Link + sync with private (`_`) properties**, e.g. on the fee line `_embroidery_for: <parent line key or variant id>`; mirror the readable text if useful. Keep fee quantity equal to the embroidered line's quantity. If the embroidered line is removed or embroidery is cleared, remove the fee line via `/cart/change.js`.
- **Pros:** any plan; simple concept; native checkout/taxes. **Cons:** shows as a separate cart line; you own the link/sync/idempotency logic; affects item counts.

### Option B — "Embroidery (+$X)" variant/option  *(works on every plan — best for low-variant products)*
- Add an option to the product, e.g. **Embroidery: No / Yes (+$10)**; the "Yes" variant carries the higher price.
- Hide the option in the theme and drive it from the modal: saving text selects the "Yes" variant and sets `properties[Embroidery]`; clearing reverts to "No".
- **Pros:** any plan; single line item; native price. **Cons:** multiplies variants (every size/color × Yes/No), so only clean for products with few/no existing variants; fixed per-product amount; needs inventory handling on the new variants.

### Option C — Shopify Functions Cart Transform `lineUpdate`  *(Shopify Plus only — cleanest UX)*
- A custom app deploys a Cart Transform function that detects the `Embroidery` property on a line and raises **that line's** price by the upcharge — no extra line, no variant.
- **Pros:** cleanest; the embroidered item simply costs more; one line; no sync logic. **Cons:** **Plus only**; requires building/deploying a custom app + Function; known to not combine with selling plans.

**Decision:** Not Plus → **Option A** for arbitrary products, or **Option B** if the embroiderable products have few/no variants. Plus → **Option C**.

**Where to set the amount:** a product metafield `custom.embroidery_price` (varies per product) or a single global value. Option A encodes it in the fee product's price; Option B in the variant delta; Option C reads the metafield in the function. Default assumption: a **flat fee per embroidered item**, scaling with that line's quantity. Confirm flat-vs-per-character and per-item-vs-per-order with the client.

---

## 4. Recommended architecture

```
Product page (only on embroidery-enabled products)
├── [Add to Cart]  [Custom Embroidery]      ← button beside ATC
├── <p> Embroidery: "Hello" (+$10) (Edit)   ← on-page summary after save (shows fee)
├── <dialog> modal: textarea + char count + Save / Remove
├── <input type="hidden" name="properties[Embroidery]" form="product-form-…" disabled>
└── pricing mechanism (per §3):
        A) on save → add companion fee product, link + sync to the embroidered line
        B) on save → switch product form to the "Yes (+$X)" variant
        C) on save → property present; Cart Transform raises the line price at checkout
                                   │
                                   ▼
        Cart → Checkout → Order (admin) → Packing slip → Emails   (text auto; total reflects upcharge)
```

**Per-product enablement — metafield (preferred):**
- `custom.embroidery_enabled` (boolean) to turn the feature on per product; optionally `custom.embroidery_price` (money/decimal) and `custom.embroidery_max_length` (integer).

```liquid
{%- if product.metafields.custom.embroidery_enabled -%}
  {% render 'embroidery', product: product, section_id: section.id %}
{%- endif -%}
```

**Tag fallback (simplest):** `{%- if product.tags contains 'embroidery' -%} … {%- endif -%}`

Recommend the metafield: explicit, keeps tags clean, and carries the price/length config.

---

## 5. Reference implementation sketch

> Sketch only — match the live theme's markup, classes, form id, and JS conventions. Read the real files first (see the kickoff prompt). The fee wiring below assumes **Option A**; for Option B swap "add fee product" for "select the +$X variant"; for Option C drop client-side fee logic and build the function instead.

**`snippets/embroidery.liquid`**

```liquid
{%- comment -%} expects: product, section_id {%- endcomment -%}
{%- assign product_form_id = 'product-form-' | append: section_id -%}
{%- assign max_len = product.metafields.custom.embroidery_max_length.value | default: 50 -%}
{%- assign fee = product.metafields.custom.embroidery_price.value | default: 10 -%}

<div class="embroidery"
     data-embroidery
     data-max="{{ max_len }}"
     data-fee="{{ fee }}"
     data-fee-variant-id="{{ settings.embroidery_fee_variant_id }}">  {# Option A: the fee product's variant id #}

  {# Bound to the product form, disabled until the customer saves text #}
  <input type="hidden"
         name="properties[Embroidery]"
         id="embroidery-value-{{ section_id }}"
         form="{{ product_form_id }}"
         value="" disabled data-embroidery-field>

  <button type="button" class="button button--secondary" data-embroidery-open>
    Custom Embroidery
  </button>

  <p class="embroidery__summary" data-embroidery-summary hidden>
    Embroidery: “<span data-embroidery-text></span>” (+{{ fee | money }})
    <button type="button" class="link" data-embroidery-edit>Edit</button>
  </p>

  <dialog class="embroidery__modal" data-embroidery-modal aria-label="Add custom embroidery">
    <div class="embroidery__modal-inner">
      <h2>Custom embroidery <small>(+{{ fee | money }})</small></h2>
      <label for="embroidery-input-{{ section_id }}">Your text</label>
      <textarea id="embroidery-input-{{ section_id }}" rows="2"
                maxlength="{{ max_len }}" data-embroidery-input></textarea>
      <p class="embroidery__count"><span data-embroidery-count>0</span>/{{ max_len }}</p>
      <div class="embroidery__actions">
        <button type="button" class="button button--secondary" data-embroidery-remove>Remove</button>
        <button type="button" class="button" data-embroidery-save>Save</button>
      </div>
    </div>
  </dialog>
</div>

<script>
  (function () {
    document.querySelectorAll('[data-embroidery]').forEach(function (root) {
      var field   = root.querySelector('[data-embroidery-field]');
      var openBtn = root.querySelector('[data-embroidery-open]');
      var editBtn = root.querySelector('[data-embroidery-edit]');
      var modal   = root.querySelector('[data-embroidery-modal]');
      var input   = root.querySelector('[data-embroidery-input]');
      var saveBtn = root.querySelector('[data-embroidery-save]');
      var rmBtn   = root.querySelector('[data-embroidery-remove]');
      var summary = root.querySelector('[data-embroidery-summary]');
      var textEl  = root.querySelector('[data-embroidery-text]');
      var countEl = root.querySelector('[data-embroidery-count]');
      var maxLen  = parseInt(root.getAttribute('data-max'), 10) || 50;

      function openModal() { input.value = field.value || ''; updateCount(); modal.showModal(); input.focus(); }
      function updateCount() { countEl.textContent = (input.value || '').length; }

      function applyValue(val) {
        val = (val || '').trim();
        if (val) {
          field.value = val;
          field.disabled = false;          // serializes the property with the form
          textEl.textContent = val;        // textContent, never innerHTML (XSS-safe)
          summary.hidden = false;
        } else {
          field.value = ''; field.disabled = true; summary.hidden = true;
        }
        // NOTE: the actual fee handling (Option A add-fee / Option B variant swap) is wired
        // at add-to-cart time so the fee tracks the real line. See §3 + §5 notes below.
      }

      openBtn.addEventListener('click', openModal);
      if (editBtn) editBtn.addEventListener('click', openModal);
      input.addEventListener('input', updateCount);
      saveBtn.addEventListener('click', function () {
        if (input.value.length > maxLen) input.value = input.value.slice(0, maxLen);
        applyValue(input.value); modal.close();
      });
      rmBtn.addEventListener('click', function () { applyValue(''); input.value = ''; modal.close(); });
      modal.addEventListener('click', function (e) { if (e.target === modal) modal.close(); });
    });
  })();
</script>
```

**Fee wiring (Option A) — the important part.** Because the fee is a *second* line item, do it at add-to-cart, not on modal save, so it tracks the real line:
- Intercept the product form's submit when `Embroidery` is set. Add **both** the product (with `properties[Embroidery]`) **and** the fee variant (with a private `_embroidery_for` linking key + matching qty) in a single `/cart/add.js` `items: [...]` call, then refresh the cart drawer via bundled **section rendering**. Doing both in one call keeps them adjacent and avoids a flash of the item without its fee.
- After add, register listeners so that changing the embroidered line's qty updates the fee qty (`/cart/change.js`), and removing the line (or clearing embroidery) removes the fee. Guard against double-adding the fee on Edit/re-save (idempotency by the `_embroidery_for` key).
- Configure the fee product: tracking off, hidden from search/sitemap/collections, clear title ("Custom Embroidery"), correct tax category.

**Fee wiring (Option B).** On save, set the product form's selected variant to the "Yes (+$X)" variant id (and keep `properties[Embroidery]`); on remove, revert to the base variant. No extra line, no sync logic — but only practical when the variant explosion is acceptable.

**Cart display:** Dawn renders properties already — verify `snippets/cart-drawer.liquid` and `sections/main-cart-items.liquid` loop `item.properties` and skip blanks / `_`-prefixed keys. Only add the loop if a non-Dawn theme strips it.

---

## 6. Edge cases & things to get right

- **Find the Shopify plan first** — it picks the pricing path (Option C is Plus-only).
- **Theme + form id detection** — confirm the real `<product-form>`/form id and that the bound input serializes. Test in the live theme.
- **Empty values** — `disabled`-until-saved keeps blank properties off orders.
- **XSS / escaping** — Liquid auto-escapes `{{ property.last }}`; in JS use `textContent`, never `innerHTML`; never `| raw` the embroidery text.
- **Length / charset** — enforce `maxlength` and clamp on save; consider stripping characters the embroidery machine can't stitch (emoji/control chars). Confirm the real limit with the client.
- **Fee ↔ line sync (Option A)** — fee qty must follow the embroidered line; remove the fee when the line is removed or embroidery cleared; never double-add on re-save; hide the fee product from standalone purchase/search.
- **Taxes & discounts (Option A/B)** — the fee is a real product/variant, so it's taxed and may be hit by cart discounts; confirm desired behavior with the client.
- **Quantity > 1** — one embroidery string per line. Different text per unit at qty 2+ is a bigger feature (force qty 1 when embroidery is set, or split adds) — confirm scope; out of scope for v1.
- **Same product, different embroidery** — stays as separate line items automatically.
- **Variant switching** — the bound hidden input persists across variant changes (tied to the form, not the variant) — desired.
- **Accessibility** — native `<dialog>` (focus trap + Esc), labeled field, return focus to the trigger on close.
- **Theme updates** — snippet + one render line in `main-product.liquid` is low-risk and version-controlled; document the edit so it can be re-applied. Fully update-proof option = app block (§8).

---

## 7. Existing solutions to learn from / remix

**Patterns & tutorials (free, code-level):**
- Shopify **Ajax Cart API reference** — `add.js`/`change.js`, `properties`, private `_` keys, section rendering: `https://shopify.dev/docs/api/ajax/reference/cart`
- Shopify **Cart Transform Function API** — `lineUpdate` price override and its **Plus-only** restriction: `https://shopify.dev/docs/api/functions/latest/cart-transform`
- **Shopify UI Elements Generator** — generates line-item-property inputs: `https://ui-elements-generator.myshopify.com/pages/line-item-property`
- **Pogodan** — line item properties in Dawn without editing theme code (the `form="..."` binding + the **Horizon** form-id variant): `https://www.pogodan.com/blogs/shopify-diy/adding-line-item-properties-in-dawn-without-editing-the-theme-code`
- **CarsonBain gist** — full personalization template walkthrough: `https://gist.github.com/CarsonBain/8f206795a23514916405353c0c30e3fb`
- **Rob Johnson** — line item properties implementation & how they persist to the order: `https://www.robkjohnson.com/posts/shopify-line-item-properties-implementation/`
- **Shopify Community** — "Line item properties in Dawn Theme" (the canonical AJAX thread; Dawn PR #509 improved native support).

**Upcharge patterns specifically (study the mechanism, build custom):**
- **Customily — "How to charge extra for personalizations"** — the companion-fee-**product** pattern (Option A) in detail: `https://help.customily.com/hc/en-us/articles/15743447086363`
- **Teeinblue — "Addon Charge"** — the **variant**-per-price-tier pattern (Option B): `https://support.teeinblue.com/en/article/upsell-your-product-design-with-addon-charge-additional-charge-1at62af/`
- **Easify — "Add extra charges for custom product options"** — contrasts **Add-on Price** vs **Add-on Product** (maps to Option C-style vs Option A): `https://easifyapps.com/blog/adding-extra-charges-for-custom-product-options-shopify/`

**Apps to study for UX (don't install — mirror the flow):** Infinite Options (Shop Circle), Easify Product Options, Tepo, Variant + Product Options. For fee-only mechanics: Magical Product Fees, Dotstore/Easify extra-fees apps (most use the companion-product trick under the hood).

How to remix: take the **field + form-binding** mechanism from the tutorials, the **fee mechanism** from Customily/Teeinblue (per plan), wrap both in the **button-opens-modal** UX the client asked for, and drop everything unneeded (fonts, previews, uploads).

---

## 8. Out of scope for v1 (flag to client)

- **Per-unit embroidery at qty > 1** — see §6.
- **Per-character / tiered pricing** — v1 assumes a flat per-item fee; tiered pricing means a variable fee (Option A: variable fee quantity or multiple fee variants; Option C: compute in the function).
- **App / Theme App Extension version** — if the client wants this to survive theme swaps with zero re-editing, be merchant-configurable from an app UI, or be reused across stores, build it as a **Theme App Extension (app block)** instead of a snippet. (And note: Option C *requires* an app anyway, since Functions deploy via an app.) For a single store + a few products, the snippet approach is pragmatic.

---

## 9. Using Context7 during implementation

Pull **live** docs via the Context7 MCP rather than relying on memory (Shopify theme/Function APIs change). Resolve and read:
- Shopify **Ajax Cart API** (`add.js`/`change.js`, `properties`, section rendering).
- Shopify **Cart Transform Function API** (if the store is Plus and you go with Option C) — `lineUpdate`, plan gating, schema.
- Shopify **Liquid `line_item` / `properties`** reference.
- The **specific theme** (Dawn or Horizon) source, to match the real product-form id, buy-button markup, and cart-rendering snippets.

Workflow: Context7 `resolve-library-id` for "Shopify Dawn theme", "Shopify Liquid Ajax cart", "Shopify Functions cart transform", "Shopify line item properties", then `get-library-docs` on the resolved id(s). The live theme/repo is the source of truth over any doc.

---

## 10. Testing checklist

Text capture & display:
- [ ] Button shows **only** on embroidery-enabled products; never elsewhere.
- [ ] Modal opens, accepts text, enforces max length + char count.
- [ ] Save → text appears on the product page; Remove/empty → summary hides, no property attached.
- [ ] Add to cart: text appears in cart drawer **and** cart page.
- [ ] Two of the same product with different text = two separate line items.
- [ ] A product without embroidery set adds with **no** blank `Embroidery` property.
- [ ] Checkout, admin order, packing slip, and order email all show the text.
- [ ] Variant switch keeps the text; quantity behaves as agreed.

Upcharge:
- [ ] Saving embroidery applies the upcharge; cart subtotal/total reflect it.
- [ ] Clearing embroidery (or removing the item) removes the upcharge.
- [ ] Changing the embroidered line's quantity keeps the fee in sync (Option A).
- [ ] No double-charge on Edit/re-save (Option A idempotency).
- [ ] Fee product can't be found/bought on its own (Option A): hidden from search/sitemap/collections.
- [ ] Upcharge is correct at checkout and on the admin order total; taxes/discounts behave as the client expects.
- [ ] (Option C) Function only runs on Plus; verify behavior on the actual plan before shipping.

General:
- [ ] Works on mobile; modal is keyboard- and screen-reader-accessible (Esc closes, focus returns).
- [ ] Re-test after any theme update; re-apply the render line if needed.
