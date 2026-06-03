# Custom Embroidery — Recon Findings & Proposed Plan

_Step 1 deliverable. No code changed yet. Reconciled against the live repo (the repo wins over any doc)._

> **Status:** Client answered the four blocking questions (see §7). Plan is **Advanced (not Plus)** and the embroiderable products **have size variants**, so the pricing mechanism is now **locked to Option A** (companion fee product). One loose end: the client named **four** products but listed **three** URLs — need the 4th (see §7).

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

**⚠️ One open item:** the client said **four** products but listed only **three** URLs. Need the **4th product URL/handle** before enabling. (Doesn't block building — enablement is per-product via the metafield/tag — but the 4th product won't show the button until it's flagged.)

> Because all four answers point the same way (not Plus + existing variants + flat $20), **no further confirmation is needed to start coding** once the 4th product handle is supplied (or the client confirms three is correct). The pricing decision is locked in §8.

---

## 8. Pricing mechanism — LOCKED: Option A (companion fee product)

Decision, per `research-one.md` §3 and the §7 answers:

- Plan is **Advanced (not Plus)** → Option C (Cart Transform `lineUpdate`) is unavailable (Plus-only). ❌
- Products **already have 4 size variants each** → Option B ("No/Yes (+$20)" variant) would double them to **8 variants per product**, each needing inventory. Rejected as too messy. ❌
- → **Option A — companion "Embroidery fee" product.** ✅

**How Option A works here:**
- Create one hidden product **"Custom Embroidery"** priced at **$20.00** (one variant). Inventory tracking **off** (or "continue selling"); hidden from search, sitemap, and all collections so it can't be found/bought on its own; correct tax category.
- When the customer saves embroidery text and adds the mockneck to cart, also add **1× the $20 fee variant** in the **same** `/cart/add.js` `items:[...]` call, linked to the embroidered line via a private `_embroidery_for` key (idempotency + cleanup), then refresh the cart drawer via bundled section rendering.
- Keep the fee line's **quantity equal to** the embroidered line's quantity (since the fee is **$20 per item**). If the embroidered line is removed or embroidery is cleared, remove the fee line via `/cart/change.js`. Guard against double-adding on Edit/re-save.

**Fee amount source:** flat **$20**, encoded in the fee product's price (the source of truth for the charge). The on-page summary text "(+$20.00)" reads from a `custom.embroidery_price` metafield if present, else falls back to a single configured value/theme setting — display only; the actual charge is the fee product's price.

**Per-product gate:** `custom.embroidery_enabled` boolean metafield (preferred), with an `embroidery` **tag** as fallback. Enable it on the 3–4 Sunday Brunch Mockneck products.

**New setup artifacts this requires (admin, not code):**
1. The hidden **"Custom Embroidery" $20 product** → note its **variant id** for the snippet (`settings.embroidery_fee_variant_id` theme setting, or hardcoded constant).
2. The **`custom.embroidery_enabled`** boolean metafield definition, set `true` on the embroiderable products.
3. (Optional) **`custom.embroidery_price`** metafield for the display amount.

---

## 9. Proposed implementation shape (for approval)

1. **Gate** (1 line in `sections/main-product.liquid`, right after the `buy_buttons` render at line 449):
   ```liquid
   {%- if product.metafields.custom.embroidery_enabled -%}
     {% render 'embroidery', product: product, section_id: section.id %}
   {%- endif -%}
   ```
   — the **only** core-theme-file edit; documented here for re-applying after Dawn updates.
2. **`snippets/embroidery.liquid`** (new, self-contained): hidden `properties[Embroidery]` input bound with `form="product-form-{{ section.id }}"`, `disabled` until non-empty text is saved; the "Custom Embroidery" trigger button styled with Dawn's `button button--secondary`; a native `<dialog>` modal with a textarea + char counter + Save/Remove; an on-page summary showing the text + **(+$20.00)**. Section-scoped vanilla JS, `textContent`-only preview (no `innerHTML`), `maxlength="50"` + clamp on save.
3. **Pricing wiring — Option A:** intercept the product form submit when `Embroidery` is set; add the mockneck (with `properties[Embroidery]`) **and** the **$20 fee variant** (with `_embroidery_for` link key + matching qty) in one `/cart/add.js` call; refresh the drawer via section rendering. Add listeners to keep fee qty in sync with the embroidered line and to remove the fee when the line is removed or embroidery cleared; idempotent on re-save.
4. **No cart-snippet edits** (already render properties).
5. Match Dawn CSS tokens/button classes; prefer an `assets/` file if I add non-trivial CSS/JS (the theme keeps JS in `assets/`).

**Before coding I'll pull live docs via Context7** (Ajax Cart API, Liquid `line_item`/`properties`, and — if Plus — the Cart Transform Function API) and reconcile against these files.

---

## Open items (no longer blocking — can start coding)

The four blocking questions are **answered** (§7); pricing is **locked to Option A** (§8). Remaining loose ends, none of which block building the snippet:

1. **4th product handle** — client named four products but listed three URLs. Needed only to enable the button on that product (per-product gate). Three confirmed: dusty-blue, seagull, white.
2. **Admin setup** (client or me, before go-live): create the hidden **$20 "Custom Embroidery"** fee product and capture its **variant id**; add the **`custom.embroidery_enabled`** boolean metafield and set it on the embroiderable products.
3. **Edge confirmations** to raise with client during build (defaults assumed): the $20 fee is taxed like a normal product and may be touched by cart discounts (Option A); one embroidery string per line at qty > 1 (per-unit text at qty 2+ is out of scope for v1).

**Next step (on approval):** pull live Context7 docs (Ajax Cart API + Liquid `properties`), then implement per §9.

---

## 10. Implementation TODO — phased task list

Option A, Dawn v13.0.1. `[ ]` = not started. Phases are roughly sequential, but **Phase 0 (admin) and Phase 1 (docs)** can run in parallel before any theme code. **Nothing here is implemented yet.**

### Phase 0 — Admin setup & inputs (Shopify admin; client or me — no theme code)
_These produce the IDs/flags the code depends on. Build can start before they're all done, but go-live can't._

- [ ] **0.1** Get the **4th product handle** from client (or confirm only 3: dusty-blue, seagull, white).
- [ ] **0.2** Create the hidden fee product **"Custom Embroidery"**, price **$20.00**, single variant.
  - [ ] Inventory tracking **off** (or "continue selling when out of stock").
  - [ ] Sales channels / visibility: **hidden from Online Store search, sitemap, and all collections** (unpublish from search; don't add to any collection).
  - [ ] Set the correct **tax category** (taxable like apparel, per client).
  - [ ] Minimal/locked product template so it can't be meaningfully bought standalone.
- [ ] **0.3** **Capture the fee variant id** (numeric). Decide where it lives: a theme setting `settings.embroidery_fee_variant_id` (preferred — editable) vs. a constant in the snippet.
- [ ] **0.4** Create metafield definition **`custom.embroidery_enabled`** (boolean, product). Set **true** on the embroiderable products.
- [ ] **0.5** _(Optional)_ Create **`custom.embroidery_price`** (money) for the on-page display amount; else use a single configured fallback ($20).
- [ ] **0.6** Confirm with client: fee is **taxable** and **discountable** (Option A behavior); **one embroidery string per line** at qty > 1 (v1 scope).

### Phase 1 — Docs & reconciliation (no code)
- [ ] **1.1** Context7 `resolve-library-id` + `get-library-docs`: **Shopify Ajax Cart API** (`/cart/add.js`, `/cart/change.js`, `items:[...]`, bundled **section rendering**).
- [ ] **1.2** Context7: **Liquid `line_item` / `properties`** reference (confirm private `_` behavior, display rules).
- [ ] **1.3** Reconcile docs against live files: re-confirm `product-form-{{ section.id }}`, `product-form.js` `FormData(this.form)` serialization, and the cart property loops (drawer + cart page). Repo wins.
- [ ] **1.4** Identify the exact **section-rendering sections** to request on add (cart-drawer / cart-icon-bubble) and how Dawn's `cart` JS expects the response (check `assets/cart.js` / `cart-drawer.js` / `pubsub.js`).

### Phase 2 — Theme setting & enablement gate
- [ ] **2.1** _(If using a setting for the variant id)_ Add `embroidery_fee_variant_id` (+ optional default price/length) to `config/settings_schema.json` under a new "Custom Embroidery" group.
- [ ] **2.2** Add the **single core-theme edit**: the gated `{% render 'embroidery' %}` line in `sections/main-product.liquid` right after the `buy_buttons` render (~line 449). Gate on `custom.embroidery_enabled` with `tags contains 'embroidery'` fallback.
- [ ] **2.3** Document this exact edit (file + anchor + snippet) in this doc's "Theme-update re-apply" note (Phase 7) so it survives Dawn updates.

### Phase 3 — `snippets/embroidery.liquid` (UI + text capture)
- [ ] **3.1** Snippet scaffold + `{% comment %}` expected params (`product`, `section_id`); read `max_len` (default 50), `fee` (default $20), `fee_variant_id` into `data-*` attrs.
- [ ] **3.2** Hidden input `name="properties[Embroidery]"`, `form="product-form-{{ section_id }}"`, **`disabled`** until non-empty text saved, unique id per section.
- [ ] **3.3** Trigger **"Custom Embroidery"** button (Dawn `button button--secondary`, `type="button"`) beside Add to Cart.
- [ ] **3.4** Native **`<dialog>`** modal: labeled `<textarea maxlength="50">`, live char counter, **Save** / **Remove** buttons, fee shown in heading.
- [ ] **3.5** On-page **summary** (`Embroidery: "…" (+$20.00)` + Edit) — hidden until saved; uses `textContent`, never `innerHTML`.
- [ ] **3.6** Section-scoped vanilla JS (IIFE over `[data-embroidery]`): open/edit/close, counter, `applyValue()` (trim → enable+set input + show summary, or clear → disable+hide), clamp to 50 on save, re-disable when cleared.
- [ ] **3.7** Accessibility: `<dialog>` focus trap + Esc, labeled field, backdrop-click close, return focus to trigger.
- [ ] **3.8** Optionally consider stripping/flagging characters the machine can't stitch (emoji/control chars) — confirm scope with client; default = allow, just clamp length.

### Phase 4 — Pricing wiring (Option A: companion fee product + sync)
- [ ] **4.1** Intercept the product form **submit** when `properties[Embroidery]` is non-empty (without breaking normal adds for non-embroidery / non-set cases). Coordinate with `product-form.js` (don't double-submit).
- [ ] **4.2** Build one **`/cart/add.js`** call with `items: [ {mockneck variant, qty, properties:{Embroidery}}, {fee variant, qty: same, properties:{_embroidery_for: <key>}} ]`. Use `window.Shopify.routes.root`.
- [ ] **4.3** **Refresh the cart drawer** via bundled **section rendering** (request the cart sections; update DOM; publish the cart-update PubSub event Dawn uses).
- [ ] **4.4** **Linking key** strategy: derive a stable `_embroidery_for` value (e.g. mockneck variant id + a nonce) so the fee line maps 1:1 to its embroidered line, and two same-variant lines with different text don't collide.
- [ ] **4.5** **Qty sync:** listen for embroidered-line qty changes (cart drawer/page) → `/cart/change.js` to set the fee line qty equal. Cover the quantity inputs in both drawer and `main-cart-items`.
- [ ] **4.6** **Cleanup:** when the embroidered line is removed (or qty→0), remove its linked fee line. When embroidery is cleared pre-add, add no fee.
- [ ] **4.7** **Idempotency:** re-Save/Edit must not add a second fee line; match on `_embroidery_for`.
- [ ] **4.8** **Edge:** variant switch on PDP keeps the bound text; ensure the add uses the currently-selected mockneck variant id.

### Phase 5 — Styling (native look)
- [ ] **5.1** Match Dawn CSS tokens/`button` classes; spacing consistent with `.product-form__buttons`.
- [ ] **5.2** Put non-trivial CSS/JS in `assets/` (theme convention) rather than inline if it grows; otherwise scoped inline in the snippet is acceptable for v1. Decide and note.
- [ ] **5.3** Mobile layout for button + modal; dialog max-width/scroll on small screens.

### Phase 6 — Cart display (verify only; expect no edits)
- [ ] **6.1** Confirm `cart-drawer.liquid` + `main-cart-items.liquid` render `Embroidery` and **skip** the `_embroidery_for` key and blanks (already true per §4 — verify live).
- [ ] **6.2** Only if a surface strips it, add a minimal properties loop. (Not expected.)

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
