# Hazel Boutique — Implementation Plan

Ordered from simplest to most complex. Each item is self-contained — work can be picked up in any order within a tier. Code snippets reference the actual codebase.

---

## Tier 1 — Shopify Admin Only (No Code)

These require zero theme changes. Do them first.

---

### 1. Shop Navigation Categories **COMPLETE**

**What:** Add Mock Necks under Clothing, add Perfume under Accessories, move Hazel Mini (Mini Cherub) under Bottoms within Clothing.

**Where:** Shopify Admin → Navigation → Main Menu

**Steps:**
1. Go to **Online Store → Navigation → Main Menu**
2. Open the **Clothing** dropdown item → add **Mock Necks** as a child link pointing to its collection
3. Open the **Accessories** dropdown item → add **Perfume** as a child link pointing to its collection
4. Open **Clothing → Bottoms** → add **Hazel Mini / Mini Cherub** as a child link
5. Save

**No code changes needed.**

---

### 2. Hide Route Insurance Product from Store **COMPLETE**

**What:** Route's Package Protection product appears in product listings and possibly recommendations. It should not be customer-facing.

**Where:** Shopify Admin → Products → Package Protection by Route

**Steps:**
1. Go to **Products** → search "Route" or "Package Protection"
2. Open the product → change **Status** to **Unlisted** (not Draft — Draft prevents cart injection and breaks the widget entirely)
3. Save

**Note:** Unlisted is Route's officially documented approach. The product is hidden from storefront search and collections but remains purchasable via cart/checkout so the widget functions normally. If using third-party search/recommendations apps (Rebuy, Klaviyo, Boost, etc.) that ignore Unlisted status, add a vendor filter: `Product vendor is not equal to "Route"` in that app's settings.

**The `.route-div` placeholder in `snippets/cart-drawer.liquid:654` and `sections/main-cart-footer.liquid:80` is already empty** — Route injects its widget into that div via its app embed. The div itself is harmless but can be removed once Route is fully disabled if needed.

**CSS fallback** (add to Shopify admin → Online Store → Themes → Edit Code → `assets/base.css` bottom, only if product still appears):
```css
/* Hide Route widget if still injected */
.route-div { display: none !important; }
```

---

### 3. Returns Email Verification **COMPLETE**

**What:** Confirm that return requests route to shop@hazelboutique.com.

**Where:** Shopify Admin → Settings → Notifications

**Steps:**
1. Go to **Settings → Notifications**
2. Check all customer-facing email notification templates (especially **Order confirmation**, **Refund confirmation**) and confirm the sender/reply-to is shop@hazelboutique.com
3. Also check **Settings → General → Store contact information** — the contact email here is what Shopify uses as the default reply-to for customer emails

**No code changes.** The returns form lives in the contact page as page content (not as the `contact-form` section, which is currently disabled in `templates/page.contact.json`).

---

### 4. Enable Express Checkout Payment Methods **COMPLETE**

**What:** Enable Apple Pay, Google Pay, and Shop Pay buttons in Shopify admin — these are the "dynamic checkout" buttons currently commented out in the theme.

**Where:** Shopify Admin → Settings → Payments

**Steps:**
1. Go to **Settings → Payments** and verify Shop Pay, Apple Pay, and Google Pay are activated under "Accelerated checkouts"
2. These are already configured in the theme code — see Tier 2 item #10 for uncommenting the button

---

---

## Tier 2 — Simple Code Changes

These are 1–20 line changes with immediate visible impact.

---

### 5. Fix Header Breakpoint Typo

**What:** A typo `900spx` in the header CSS prevents the correct desktop/mobile breakpoint from applying, which may cause the hamburger drawer to show at desktop widths when it shouldn't.

**File:** `sections/header.liquid:41`

**Current:**
```liquid
@media screen and (min-width: 900spx) {
  header-drawer {
    display: none;
  }
}
```

**Fix:**
```liquid
@media screen and (min-width: 900px) {
  header-drawer {
    display: none;
  }
}
```

**Risk:** None. This is a pure typo fix restoring intended behavior.

---

### 6. Fix DA Restock Moment.js URL

**What:** The Moment.js script URL has a leading space that causes a 404 on every product page with the DA Restock widget.

**File:** `snippets/da-restock.liquid:17`

**Current:**
```liquid
<script type="text/JavaScript" src=" https://MomentJS.com/downloads/moment.js"></script>
```

**Fix:**
```liquid
<script type="text/JavaScript" src="https://MomentJS.com/downloads/moment.js"></script>
```

**Note:** Also consider whether MomentJS.com is the correct CDN — the standard CDN is `https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.30.1/moment.min.js`. Verify this works with DA Restock before deploying.

---

### 7. Hide "Press Play" Video Overlay Button on Mobile

**What:** The play button overlay on product videos (`deferred-media__poster-button`) is broken on mobile. The fix is to hide it on mobile so videos load without requiring the tap interaction.

**How it works:** `snippets/product-media.liquid:54–77` renders a `<button class="deferred-media__poster">` with the play icon. On desktop this works fine. On mobile the button doesn't trigger the deferred video load correctly.

**Option A — CSS only (recommended, low risk):** Add to the bottom of `assets/component-deferred-media.css`:

```css
@media screen and (max-width: 749px) {
  .product__media-item .deferred-media__poster-button {
    display: none;
  }
  /* Make the full poster area tappable instead */
  .product__media-item .deferred-media__poster {
    pointer-events: auto;
  }
}
```

**Option B — Remove the button entirely from the snippet** (more invasive, affects all media). Not recommended until Option A is tested.

**File to edit:** `assets/component-deferred-media.css` — add at the bottom.

---

### 8. Remove Product Count from Collection Pages

**What:** Goals note says "Remove product count display from the product page." In the codebase this is the **"X products"** text shown in the vertical sort bar on collection pages.

**File:** `sections/main-collection-product-grid.liquid:69–88`

**Current block:**
```liquid
<div class="product-count-vertical light" role="status">
  <h2 class="product-count__text text-body">
    <span id="ProductCountDesktop">
      {%- if collection.results_count -%}
        {{ 'templates.search.results_with_count' | t: terms: collection.terms, count: collection.results_count }}
      {%- elsif collection.products_count == collection.all_products_count -%}
        {{ 'products.facets.product_count_simple' | t: count: collection.products_count }}
      {%- else -%}
        {{ 'products.facets.product_count' | t: product_count: collection.products_count, count: collection.all_products_count }}
      {%- endif -%}
    </span>
  </h2>
  {%- render 'loading-spinner' -%}
</div>
```

**Option A — CSS hide (reversible, zero risk):** Add to `assets/base.css`:
```css
.product-count-vertical,
.product-count__text {
  display: none !important;
}
```

**Option B — Remove from Liquid** (cleaner): Delete lines 69–88 from `sections/main-collection-product-grid.liquid`. Note that `facets.js` also updates `#ProductCountDesktop` via JS — removing the element is safe since the JS update would simply fail silently.

There is also a product count in the horizontal filter bar inside `snippets/facets.liquid`. If that also shows, add the CSS rule above (Option A covers both).

---

### 9. Update Contact Page Email

**What:** The contact email on the contact page needs to change from the old Gmail address to shop@hazelboutique.com.

**Where:** This is page content stored in Shopify admin, not in theme files.

**Steps:**
1. Go to **Online Store → Pages** → find the Contact Us page
2. Edit the rich text content and replace the Gmail address with shop@hazelboutique.com
3. The contact *form* submission email (where Shopify sends the inquiry) is controlled by **Settings → Notifications → Contact form**

**No code changes needed** unless the email is hardcoded somewhere. Quick verification:
```bash
grep -r "gmail\|Gmail" sections/ snippets/ templates/ --include="*.liquid"
```
If nothing returns, it's page content only.

---

### 10. Enable Dynamic Checkout Buttons (Apple Pay / Shop Pay / Google Pay)

**What:** The dynamic checkout buttons are implemented in the theme but currently commented out. Uncommenting them enables Apple Pay, Google Pay, and Shop Pay to appear on the product page below the add-to-cart button.

**File:** `snippets/buy-buttons.liquid:96–100`

**Current (commented out):**
```liquid
{% comment %}
  {%- if show_dynamic_checkout -%}
    {{ form | payment_button }}
  {%- endif -%}
{% endcomment %}
```

**Fix — uncomment:**
```liquid
{%- if show_dynamic_checkout -%}
  {{ form | payment_button }}
{%- endif -%}
```

**Additionally**, for the cart page/drawer, `{{ content_for_additional_checkout_buttons }}` should be present. Check `snippets/cart-drawer.liquid` and `sections/main-cart-footer.liquid` for this tag and add if missing:

```liquid
{%- if additional_checkout_buttons -%}
  <div class="cart__dynamic-checkout-buttons additional-checkout-buttons">
    {{ content_for_additional_checkout_buttons }}
  </div>
{%- endif -%}
```

**Prerequisites:**
1. Confirm Tier 1 item #4 is done (payment methods enabled in admin)
2. On the product page in the theme editor, go to the **buy_buttons** block and verify "Show dynamic checkout buttons" is toggled on — this controls the `block.settings.show_dynamic_checkout` flag that `show_dynamic_checkout` depends on (it's already `true` in `templates/product.json:43`)
3. Test on Safari/iOS for Apple Pay, and on Chrome for Google Pay

---

---

## Tier 3 — Content and Moderate Code Changes

---

### 11. Sizing Guide Page **COMPLETE**

**What:** Update the sizing guide to:
- Add an "All Hazel styles are an oversized fit — models wear sizes L–2XL" note at the top
- Remove any reference to Australian sizes
- Include the four updated size charts from `docs/goals.md`

**Where:** Shopify Admin → Online Store → Pages → find the Sizing / Size Guide page

**Steps:**
1. Open the sizing page in the page editor
2. Add this note at the top of the content:
   > *All Hazel styles are an oversized fit. Models are wearing sizes L–2XL.*
3. Delete any mentions of Australian sizes (AU 6, AU 8, etc.)
4. Paste in the four size charts from `docs/goals.md`:

**Hoodie** *(Oversized fit with dropped shoulders and relaxed body)*

| Size | Chest (in) | Length (in) | Sleeve (in) |
|------|-----------|-------------|-------------|
| S    | 48        | 27          | 23          |
| M    | 52        | 28          | 24          |
| L    | 56        | 29          | 25          |
| XL   | 60        | 30          | 26          |
| 2XL  | 64        | 31          | 27          |

**Mockneck** *(Relaxed oversized fit with structured mock neckline and dropped shoulders)*

| Size  | Chest (in) | Length (in) | Sleeve (in) |
|-------|-----------|-------------|-------------|
| M/L   | 50        | 27          | 24          |
| L/XL  | 56        | 28.5        | 25          |
| 1X/2X | 62        | 30          | 26          |
| 2X/3X | 68        | 31.5        | 27          |

**Barrel Pant** *(Loose curved-leg silhouette with oversized drape)*

| Size | Waist (in) | Hip (in) | Inseam (in) |
|------|-----------|---------|-------------|
| S    | 26–28     | 46      | 29          |
| M    | 28–32     | 50      | 30          |
| L    | 32–36     | 54      | 31          |
| XL   | 36–40     | 58      | 32          |
| 2XL  | 40–44     | 62      | 33          |

**Jogger** *(Relaxed through the leg with elastic ankle cuff)*

| Size | Waist (in) | Hip (in) | Inseam (in) |
|------|-----------|---------|-------------|
| S    | 26–28     | 44      | 30          |
| M    | 28–32     | 48      | 31          |
| L    | 32–36     | 52      | 32          |
| XL   | 36–40     | 56      | 33          |
| 2XL  | 40–44     | 60      | 34          |

5. If the page uses images for the size charts, replace or supplement with these reference images from `/docs/`: `size-chart-hoodie.png`, `size-chart-mockneck.png`, `size-chart-barrel-pant.png`, `size-chart-jogger.png`

---

### 12. Font Audit and Pragmatica Fix **COMPLETE**

**What:** Pragmatica and PragmaticaCondensed are currently falling back to system sans-serif because Shopify disabled those CDN files on 2026-03-30. The goals.md notes "all premium licensed fonts are confirmed in place" — this conflicts with what's in the code. Needs resolution before any font work.

**File:** `layout/theme.liquid:255–326`

**Current state (abridged):**
```liquid
{%- comment -%} Change on 2026-03-30 by Shopify {%- endcomment -%}
{%- comment -%} These fonts have been disabled {%- endcomment -%}
/* Pragmatica - Book */
{%- comment -%}
@font-face { ... src: url('https://cdn.shopify.com/...Pragmatica-Book.woff2') ... }
{%- endcomment -%}
{%- comment -%} Begin replacement {%- endcomment -%}
@font-face {
  font-family: 'Pragmatica';
  src: local('Arial'), local('Helvetica Neue'), local('Helvetica'), local('sans-serif');
}
```

**Resolution steps:**
1. **Confirm with owner** whether the CDN files still exist under the store's own CDN (not the shared Shopify CDN). The original URLs reference store ID `1/0051/3264/8566` — if these files were uploaded to that store's own files, they may still be accessible
2. **Test the original URLs** from `theme.liquid:260–295` directly in a browser. If they 404, the files are gone
3. **If files are gone:** Re-upload the font files (`.woff2`, `.woff`, `.ttf`) to **Settings → Files** in the Shopify admin. Get fresh CDN URLs and restore the `@font-face` declarations in the commented-out block
4. **If files are accessible:** Simply uncomment the original `@font-face` declarations (lines ~258–296) and remove the replacement block (lines ~298–326)

**The restored `@font-face` block should look like:**
```css
/* Pragmatica - Book */
@font-face {
  font-display: swap;
  font-family: 'Pragmatica';
  font-style: normal;
  font-weight: 400;
  src: url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/Pragmatica-Book.woff2?v=1713569839') format('woff2'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/Pragmatica-Book.woff?v=1713569839') format('woff'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/Pragmatica-Book.ttf?v=1713569839') format('truetype');
}
/* Pragmatica - Light */
@font-face {
  font-display: swap;
  font-family: "Pragmatica";
  font-style: normal;
  font-weight: 400;
  src: url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaLight.woff2?v=1713569839') format('woff2'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaLight.woff?v=1713569839') format('woff'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaLight.ttf?v=1713569839') format('truetype');
}
/* PragmaticaCondensed - Book */
@font-face {
  font-display: swap;
  font-family: 'PragmaticaCondensed';
  font-style: normal;
  font-weight: 400;
  src: url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Book.woff2?v=1713569839') format('woff2'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Book.woff?v=1713569839') format('woff'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Book.ttf?v=1713569839') format('truetype');
}
/* PragmaticaCondensed - Light */
@font-face {
  font-display: swap;
  font-family: "PragmaticaCondensed";
  font-style: normal;
  font-weight: 400;
  src: url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Light.woff2?v=1713569839') format('woff2'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Light.woff?v=1713569839') format('woff'),
       url('https://cdn.shopify.com/s/files/1/0051/3264/8566/files/PragmaticaCond-Light.ttf?v=1713569839') format('truetype');
}
```

---

### 13. Meta Pixel Audit

**What:** Verify that the Shopify Meta Pixel fires correctly for purchase events on both TikTok and Instagram integrations.

**Tools needed:** Meta Events Manager, TikTok Pixel Helper Chrome extension, Meta Pixel Helper Chrome extension.

**Steps:**

**Step 1 — Check what pixels are installed:**
1. Go to **Online Store → Preferences** in Shopify admin — check if the Facebook/Meta channel is connected
2. Go to **Online Store → Themes → Customize → App Embeds** — verify Meta Pixel and TikTok Pixel app embeds are enabled (not just installed)

**Step 2 — Verify Meta Pixel (Facebook/Instagram):**
1. Go to **Meta Business Suite → Events Manager** → select your pixel
2. Click **Test Events** → enter the store URL → open in new tab
3. Place a test order using Shopify's **bogus gateway** (no real payment needed; enable under Settings → Payments → Test mode)
4. Back in Events Manager, confirm a `Purchase` event appears in the real-time feed within 60 seconds
5. If missing: check that the pixel ID in Shopify matches what's in Events Manager. Also verify the Conversions API (server-side) is connected — this is required since browser blocking is widespread

**Step 3 — Verify TikTok Pixel:**
1. Install **TikTok Pixel Helper** Chrome extension
2. Browse the store and place a test order — the extension shows which events fire in real time
3. Note: TikTok renamed `CompletePayment` to `Purchase` in May 2025. If using a legacy integration, confirm the event name mapping is correct in the TikTok Ads Manager → Events → Web Events

**Step 4 — 2026 Shopify update:**
Shopify now monitors whether pixels are contributing measurable signals. Pixels with no attribution over days/weeks may be paused automatically. Confirm in the Shopify admin that both pixels show "Active" status.

**Common fixes:**
- If events are missing: disconnect and reconnect the Meta Sales Channel / TikTok for Business app
- If purchase events are tracking but not matching ad conversions: enable **Conversions API** for server-side tracking to supplement browser-side pixel events

---

### 14. Restore Missing Pages (Our Story & Store Locations)

**What:** The "Our Story" and "Store Locations" pages appear broken or inaccessible. There are internal links to `/pages/our-story` and `/pages/store-locations` throughout the theme.

**Where they're referenced:**
- `sections/header.liquid:169` — "Store Locations" link hardcoded in header: `href="/pages/store-locations"`
- `templates/index.json` — multicolumn block links: `"link":"shopify://pages/our-story"` and `"link":"shopify://pages/store-locations"`
- `sections/main-page.liquid:17–61` — "our-story" handle has a special layout

**Steps:**

**Step 1 — Verify pages exist:**
1. Go to **Online Store → Pages** → check if pages with handles `our-story` and `store-locations` exist
2. If they exist but are hidden: check the page's visibility/status

**Step 2 — If "Our Story" page is missing:**
1. Create a new page titled "Our Story" — Shopify will auto-generate the handle `our-story`
2. The `sections/main-page.liquid` has a special layout for this handle (hero image, decorative title) — it will automatically apply when the page handle matches
3. Note: The hero image URL is hardcoded in the section:
   ```liquid
   {%- if page.handle == 'our-story' -%}
     <header class="main--about--imageContainer">
       <img src="https://cdn.shopify.com/s/files/1/0051/3264/8566/files/IMG_1248_Facetune_21-08-2022-19-55-54_copy.webp?v=1716319263" ...>
   ```
   Verify this image is still accessible. If not, replace the URL with a new upload.

**Step 3 — If "Store Locations" page is missing:**
1. Create a new page titled "Store Locations" — handle will be `store-locations`
2. Add store location content (addresses, hours, maps embed if desired) in the page editor

**Step 4 — Add pages to navigation:**
1. Go to **Navigation → Main Menu** → confirm both pages appear as menu items, or add them

---

---

## Tier 4 — Accessibility Audit

This is ongoing work, not a one-time task. Structure it as a monthly sprint.

---

### 15. Accessibility Audit

**What:** Full review using AccessEase (installed as Shopify app), plus a manual walkthrough. Target: WCAG 2.1 AA — required under the European Accessibility Act (enforceable since June 2025).

**Phase 1 — Automated scan (1–2 hours):**
1. Run AccessEase audit from the Shopify admin — this flags contrast failures, missing alt text, unlabeled inputs
2. Export findings as a CSV or list
3. Prioritize by: (a) checkout flow first, (b) product pages, (c) navigation, (d) content pages

**Phase 2 — Known issues to fix now (from Dawn-specific research):**

**Issue 1: Dropdown menus don't announce expanded state** (WCAG 4.1.2)

The header mega menu uses `mouseover`/`mouseout` to toggle `open` attribute. The `aria-expanded` attribute needs syncing.

`sections/header.liquid:633–647` — the existing script sets `aria-expanded` on `mouseover`:
```js
item.addEventListener("mouseover", () => {
  item.setAttribute("open", true);
  item.querySelector("summary").setAttribute("aria-expanded", "true");
  item.addEventListener("mouseout", () => {
    item.removeAttribute("open");
    item.querySelector("summary").setAttribute("aria-expanded", "false");
  });
});
```
This is already partially implemented. Verify screen readers announce the expanded state by testing with VoiceOver (Mac) or NVDA (Windows).

**Issue 2: Icon-only buttons lack accessible names** (WCAG 1.1.1, 4.1.2)

Search button, cart button, and hamburger have visually hidden `<span class="visually-hidden">` text — this is already correct in the codebase. Verify they're not empty in the actual rendered HTML.

**Issue 3: Cart count bubble accessibility**

The cart count uses a custom `(0)` parenthesis style. The screen reader text is present:
```liquid
<span class="visually-hidden">{{ 'sections.header.cart_count' | t: count: cart.item_count }}</span>
```
Verify the translation string exists: check `locales/en.default.json` for `sections.header.cart_count`.

**Issue 4: Color contrast — sale badges and disabled buttons** (WCAG 1.4.3)

Dawn's default orange sale badge (`rgb(238, 148, 65)`) on white fails 4.5:1 ratio. Fix in `assets/base.css`:
```css
/* Improve sale badge contrast */
.badge--sale {
  background-color: #b8480a; /* ~5.5:1 on white */
}
```

**Issue 5: Form labels vs. placeholders** (WCAG 3.3.2)

The contact form in `sections/contact-form.liquid` uses floating labels — these have proper `<label>` elements paired with `for` attributes. The pattern is already accessible. Verify any custom forms on static pages follow the same pattern.

**Issue 6: Focus indicator visibility** (WCAG 2.4.7)

Dawn ships with `:focus-visible` styles. The custom CSS in `assets/base.css` doesn't override these. Do a keyboard-tab walkthrough to verify focus rings are visible on all interactive elements, especially the custom header elements (`headerLeftMenu`, `masonHeaderModifierTwo`).

**Phase 3 — Manual keyboard test checklist:**
- [ ] Tab through header navigation — every menu item reachable, mega menus open/close
- [ ] Cart drawer opens, items focusable, close button works with Enter/Escape
- [ ] Product variant picker navigable with arrow keys
- [ ] Add to cart button reachable and activatable with Enter
- [ ] Search modal: focus traps inside, Escape closes it
- [ ] Skip to content link at top of every page (already implemented in `layout/theme.liquid:446`)

**Phase 4 — Screen reader test:**
- Test with VoiceOver on iPhone Safari (primary customer device)
- Key flows to test: homepage → collection → product → add to cart → checkout

---

---

## Summary Checklist

| # | Task | Where | Effort | Priority |
|---|------|--------|--------|----------|
| 1 | Shop categories update | Shopify Admin Nav | 10 min | Immediate |
| 2 | Hide Route product | Shopify Admin Products | 5 min | Immediate |
| 3 | Returns email check | Shopify Admin Notifications | 10 min | Immediate |
| 4 | Enable express checkout in admin | Shopify Admin Payments | 5 min | Immediate |
| 5 | Fix header `900spx` typo | `sections/header.liquid:41` | 1 line | Quick |
| 6 | Fix DA Restock Moment.js URL | `snippets/da-restock.liquid:17` | 1 line | Quick |
| 7 | Hide video play button on mobile | `assets/component-deferred-media.css` | 5 lines | Quick |
| 8 | Remove product count display | `sections/main-collection-product-grid.liquid:69–88` | 2 lines CSS | Quick |
| 9 | Update contact email | Shopify Admin Pages | 2 min | Immediate |
| 10 | Enable dynamic checkout buttons | `snippets/buy-buttons.liquid:96–100` | Uncomment 3 lines | Low-effort, high-impact |
| 11 | Update sizing guide page | Shopify Admin Pages | 30 min | Immediate |
| 12 | Font audit & Pragmatica fix | `layout/theme.liquid:255–326` | 1–2 hrs | High visual impact |
| 13 | Meta Pixel audit | Events Manager + admin | 1–2 hrs | Immediate |
| 14 | Restore Our Story & Store Locations | Shopify Admin Pages + Nav | 1–2 hrs | Immediate |
| 15 | Accessibility audit (Phase 1–4) | Multiple files | Ongoing monthly | Continuous |
