# Hazel Boutique Theme — Deep Research Report

## 1. Theme Identity

**Base theme:** Shopify Dawn v13.0.1 (Shopify's first-party open-source theme).
**Store:** Hazel Boutique — a physical + online retail boutique in Farmingdale, NJ (1709 Rt 34, Suite 3, 07719).
**Domain:** hazelboutique.com
**Developer attribution:** Site credit links to opnsrcsolutions.com throughout the footer and mobile drawer.

This is not a premium third-party theme. It is stock Dawn with moderate-to-heavy customizations concentrated in the header, hero, footer, cart drawer, product cards, and CSS layer. The core architecture, section schemas, JS web components, and template structure are all recognizable Dawn patterns.

---

## 2. File Inventory

| Directory | Files | Purpose |
|-----------|-------|---------|
| `assets/` | 102 | JS (32), CSS (66), images (4) |
| `config/` | 3 | settings_data, settings_schema, markets |
| `layout/` | 2 | theme.liquid, password.liquid |
| `locales/` | 52 | 26 languages, each with storefront + schema JSON |
| `sections/` | 55 | 2 JSON section groups, 53 Liquid sections |
| `snippets/` | 75 | Reusable Liquid partials (39 unique functional, 36 icons) |
| `templates/` | 21 | 14 JSON templates, 7 customer templates, 1 Liquid gift card |
| `docs/` | 2 | goals.md, this file |
| **Total** | **310** | |

---

## 3. Architecture

### 3.1 Layout System

Two layouts exist:
- **`theme.liquid`** — Main storefront layout. Wraps every page except the password gate. Contains the `<head>` with CSS custom properties, font loading, and conditional script loading; `<body>` with header section group, `<main>`, footer section group, and global JS route/string objects.
- **`password.liquid`** — Stripped-down layout for the password-protected state. No custom fonts, no cursor follower, no cart drawer.

The body uses `display: grid; grid-template-rows: auto auto 1fr auto` for announcement bar + header + main + footer.

### 3.2 Section Groups

Two section groups control the global chrome:
- **`header-group.json`** — Announcement bar + header. Announcement bar uses custom CSS for PragmaticaCondensed font. Header uses `navbar-menu`, logo top-center, dropdown menus, always-sticky.
- **`footer-group.json`** — Footer with 4 link list blocks (quick links, socials, two category columns), newsletter enabled, policies shown. Instafeed app block present but disabled.

### 3.3 Template Composition

| Template | Active Sections | Notable Config |
|----------|----------------|----------------|
| **Homepage** (`index.json`) | 6 active / 5 disabled | Hero slideshow, 2 featured collections, rich text + Instafeed, multicolumn icon nav |
| **Product** (`product.json`) | 4 | Main product with Judge.me badges, complementary products ("Complete the look"), rich text review heading, Judge.me widget, related products |
| **Collection** (`collection.json`) | 2 | Banner + product grid, 48 products/page, horizontal filtering |
| **Cart** (`cart.json`) | 2 | Standard items + footer |
| **Blog** (`blog.json`) | 1 | Collage layout, no author |
| **Article** (`article.json`) | 1 | Image + title + share + content, no author |
| **Search** (`search.json`) | 1 | 4-column grid, adapt image ratio |
| **Page** (`page.json`) | 1 (disabled) | Main section disabled — pages using this template render empty |
| **About** (`page.about.json`) | 1 | Standard page content |
| **Contact** (`page.contact.json`) | 2 (1 disabled) | Page content active, contact form disabled |
| **Customer templates** (7) | 1 each | All stock Dawn defaults |
| **Gift card** (`gift_card.liquid`) | N/A | Self-contained Liquid template, no layout |

### 3.4 JavaScript Architecture

**Pattern:** Web Components (Custom Elements v1). No framework. 38 custom elements total.

**Event system:** Hand-rolled pub/sub (`pubsub.js`) with 4 events:
- `cart-update` — After any cart modification
- `quantity-update` — When quantity boundaries change
- `variant-change` — After variant switch with fetched HTML
- `cart-error` — When add-to-cart fails

**Key inheritance chains:**
- `SliderComponent` → `SlideshowComponent` (hero, slideshow, product gallery)
- `MenuDrawer` → `HeaderDrawer` (mobile nav)
- `ModalDialog` → `ProductModal` / `QuickAddModal`
- `DetailsModal` → `PasswordModal`
- `DetailsDisclosure` → `HeaderMenu` / `ShareButton`
- `DeferredMedia` → `ProductModel` (3D viewer)
- `CartItems` → `CartDrawerItems`
- `SearchForm` → `MainSearch` / `PredictiveSearch`

**Cross-cutting patterns:**
- Section Rendering API for all cart/product mutations (fetch pre-rendered HTML, parse with DOMParser, surgical DOM replacement)
- `trapFocus()` / `removeTrapFocus()` used consistently across modals and drawers
- Pub/sub subscriptions stored and cleaned up in `disconnectedCallback()`
- Duplicate registration guards (`if (!customElements.get(...))`) on secondary components

**Core JS files (loaded globally):**
- `global.js` — Utility functions, 10 core custom elements, polyfills
- `pubsub.js` — Event bus
- `constants.js` — Event name constants, debounce timer

**Lazy-loaded JS (per-feature):**
- `cart-drawer.js`, `cart.js`, `cart-notification.js`
- `product-form.js`, `product-info.js`, `product-modal.js`, `product-model.js`
- `media-gallery.js`, `magnify.js`
- `facets.js`, `predictive-search.js`, `search-form.js`, `main-search.js`
- `quick-add.js`, `quick-order-list.js`
- `animations.js` (currently disabled via settings)
- `details-disclosure.js`, `details-modal.js`
- `localization-form.js`, `pickup-availability.js`, `price-per-item.js`
- `quantity-popover.js`, `recipient-form.js`, `share.js`, `show-more.js`
- `theme-editor.js` (Shopify editor integration)
- `customer.js` (account address management)
- `password-modal.js`

### 3.5 CSS Architecture

**`base.css`** is the primary stylesheet (~4000+ lines). Structure:
1. CSS custom properties layer — Design token inheritance for cards, containers, media
2. Base reset & typography — Font scale system with responsive breakpoints at 750px
3. Animation timing tokens — Duration variables and easing curves
4. Focus ring system — Three variants (default, inset, none) with `:focus-visible` support
5. Flexbox grid system — CSS variable-driven gutters, 1-4 columns, tablet overrides
6. Component styles — All custom elements
7. Hazel customizations (~lines 3738+) — Brand-specific overrides, heavily using `!important`

**66 component CSS files** loaded conditionally per-section (e.g., `component-card.css`, `section-main-product.css`).

---

## 4. Brand Customizations (Deviations from Stock Dawn)

### 4.1 Typography

Five custom `@font-face` declarations hardcoded in `theme.liquid`:
- **Pragmatica** Book (400) and Light (300)
- **PragmaticaCondensed** Book (400) and Light (300)
- **Millionare** Script (400) — decorative/script typeface
- **Lustria** Regular (400) — serif accent typeface

`'Pragmatica'` is prepended to both `--font-body-family` and `--font-heading-family`, overriding whatever the Shopify font picker selects. The Shopify picker is set to `sans-serif` (system font) as a fallback.

PragmaticaCondensed is used extensively in navigation, the announcement bar, drawer menus, product card swatches, and UI text. Specific uses are called out via inline CSS in `header-group.json` and class-based rules in `base.css`.

**Font URLs are hardcoded to Shopify CDN paths** tied to store ID `1/0051/3264/8566`. These will break if the store is migrated to a different Shopify instance.

### 4.2 Color Palette

5 color schemes defined:
| Scheme | Background | Text | Use |
|--------|-----------|------|-----|
| scheme-1 (primary) | `#fcf9f3` warm cream | Black | Main brand color, most sections |
| scheme-2 | `#eeece7` warm gray | Black | Multicolumn footer section |
| scheme-3 | `#242833` dark blue-gray | White | Dark accent |
| scheme-4 | `#121212` near-black | White | Dark accent |
| scheme-5 | `#334fb4` blue | White | Accent |

The overall aesthetic is warm, cream-toned, upscale boutique. Sharp corners on buttons (0 radius), flat borderless inputs, 18px rounded product cards.

### 4.3 Custom Cursor ("Mouse Buddy")

A custom element `#follower` (32x32px circle) follows the mouse cursor with eased animation (`requestAnimationFrame`, ease factor 0.2). Uses a configurable image from `settings.mouse_image`. Hidden below 750px viewport. Z-index is `99000000000`. Has `pointer-events: none`.

A separate custom cursor system using strawberry images (`strawberryHazel.png`, `strawberryHazelHover.png`) exists in commented-out CSS in `base.css`.

### 4.4 Custom Hero Section

**`sections/hero.liquid`** — Entirely custom, not in Dawn. Dual rendering:
- **Mobile:** `slideshow-component` web component for swipeable slides
- **Desktop:** Static multi-panel flex/grid layout (all slides visible simultaneously)

Each slide supports: static image, Shopify-hosted video, or YouTube embed. All slides are wrapped in `<a>` tags (full-slide clickable links). Text overlay (`.textyText`) renders title and zero-padded index (01, 02, 03) via `.rteMidge` span.

Hardcoded Hazel Boutique script logo images render after the hero:
- Desktop: `script-logo.png`
- Mobile: `hazel-mobile-logo.png`

### 4.5 Dual-Header Architecture

**`sections/header.liquid`** renders two complete headers side by side:
1. **`masonHeaderModifierOne`** — Primary sticky header. Contains: drawer toggle, search icon, hardcoded "Store Locations" link, logo, `header-dropdown-menu` snippet, localization selectors, cart icon.
2. **`masonHeaderModifierTwo`** — Secondary header. Contains: logo, `header-dropdown-menu-helper` snippet (flat links, no dropdowns), search, cart.

The `.header--homepage` class creates a transparent header on the index template that transitions to solid on scroll. Account icon is deliberately commented out. Cart count shows `(0)` with parenthesis when empty instead of hiding.

Inline JavaScript adds `mouseover`/`mouseout` event listeners for hover-open dropdown behavior on `<details>` elements.

**CSS typo:** Line 41 of header.liquid has `900spx` instead of `900px`.

### 4.6 Custom Mega Menu

7 configurable mega menu position slots in the header schema (`mega_menu_position_one` through `_seven`), each with:
- A title confirmation text
- Two image/link/text pairs (a and b)

Creates a visual mega menu where each dropdown can show up to 2 promotional collection images alongside the standard link list. Pre-configured with specific products: Cherub Crewneck, Tami's Garden Robe, Bold Move Cardigan, Lover Shorts.

The CSS uses flex column layout with wrapping, 180px max-height, 20px column gap. Caret dropdown indicators are globally hidden (`.header__menu-item .icon-caret { display: none !important; }`).

### 4.7 Custom Product Card System

**`snippets/card-product.liquid`** — The most heavily customized snippet.

**Badge system with colored dots:**
- "Hazel Exclusive" — pink dot (`#e5b5b1`), triggered by tag `hazel brand` or `Hazel Brand`
- "Online Exclusive" — blue dot (`#bfd9e0`), triggered by tag `online exclusive` or `Online Exclusive`
- "Sold Out" — red dot (`#DB4357`)
- "Sale" — green dot (`#557f45`)

**Color swatches on cards:** Shows up to 3 colored circles below the price with a "+" indicator for additional colors. Uses `custom.hex_color` variant metafield, falling back to parsing the color name's last word. Font: PragmaticaCondensed.

**Fixed 3:4 portrait aspect ratio** (`--ratio-percent: 133%`) on all product cards.

**Entire card wrapped in `<a>` tag** — the whole card is clickable, unlike Dawn's default where only the title links.

### 4.8 Custom Cart Drawer Features

**"Wear it with" upsell system:** Custom JavaScript fetches Shopify product recommendations (complementary first, then related as fallback) for the first cart item. Displays a styled upsell card with image, title, price, and "View Product" link. Uses `cartUpsell__` CSS class prefix.

A second upsell system in `cart.js` (`checkUpsells()`) searches for matching products by color name (parsed from the product title after ` - `) and fetches from `/search?q={color} -{handle}&type=product&view=wear-with`. Uses cookie-based dismissal (`hide_wear_with`).

**Empty cart shows collection suggestions:** Renders one or two collection cards using `settings.cart_drawer_collection` and `settings.cart_drawer_collection_two` with custom placeholder images. Currently configured with "fine-collection" and "all-sale".

**Route shipping protection:** `<div class="route-div"></div>` placeholder (edited 7/1/2024) in both the cart drawer and cart footer.

**Dynamic checkout buttons are commented out** in `snippets/buy-buttons.liquid` — Shopify Pay, Apple Pay, Google Pay are disabled. Only the standard "Add to Cart" button renders.

### 4.9 Custom Footer Features

**Recently Viewed Products:** Custom vanilla JavaScript using `localStorage`:
- `setRecentlyViewedPdp()` — On product pages, stores product data (title, images, price, URL) in localStorage, capped at 4 products
- `getRecentPdp()` — Reads localStorage and dynamically injects HTML product cards into a `.product-grid-recently-viewed` grid

Note: A separate `snippets/recent-viewed-product-js.liquid` exists but is entirely wrapped in `{% comment %}` tags (disabled). The active implementation lives in `sections/footer.liquid`.

Hardcoded Hazel logo images (desktop and mobile variants) shown on non-index pages.
Newsletter button text is "Sign Up" instead of Dawn's default arrow icon.
"Site Credit" link to opnsrcsolutions.com appended after policy links.
Custom `image` block type added to the footer schema for image blocks with width and alignment settings.

### 4.10 Custom Mobile Drawer

**`snippets/header-drawer.liquid`:**
- Hamburger button includes visible text "Menu"
- Standard Dawn utility links (account, localization, social) are entirely commented out
- Replaced with hardcoded links: Our Story, Store Locations, Contact Us, Sizing Guide, Instagram, Facebook, TikTok
- Footer in drawer includes policies, copyright, and site credit to opnsrcsolutions.com

### 4.11 Collection Banner with Metafield Images

**`sections/main-collection-banner.liquid`** supports custom collection title images via metafield `collection.metafields.collection.custom_title`. When present, renders an `<img>` (45px height) instead of a text `<h1>`. This allows each collection to have a styled/branded title image.

### 4.12 Pagination Customizations

**`snippets/pagination.liquid`:**
- New Arrivals collection suppresses pagination entirely (if URL contains `new-arrivals`, renders empty div)
- Page numbers are zero-padded to 2 digits (01, 02, 03...)

### 4.13 Collection List Customization

**`sections/collection-list.liquid`** adds two custom block fields:
- `collection_image_alt` (image picker) — alternate image for the collection card
- `collection_title_alt` (inline richtext) — alternate title text

### 4.14 GlobalE Integration

`cart.js` checks for a `GlobalE_Data` cookie to detect international customers and hides the GWP (gift-with-purchase) wrapper for non-US visitors.

---

## 5. Third-Party App Integrations

| App | Status | Location |
|-----|--------|----------|
| **Judge.me Reviews** | Active | Product page — preview badge (above vendor) + full review widget |
| **Instafeed** (Instagram) | Active on homepage, disabled in footer | Homepage via `apps` section |
| **Fera Reviews** | Active (config) | Settings blocks |
| **Wishlist Plus** | Active (config) | Settings blocks |
| **AccessEase** (accessibility) | Active (config) | Settings blocks |
| **Route Shipping Protection** | Active | Cart drawer + cart footer placeholder divs |
| **DA Restock** (back-in-stock) | Active | Product pages via `snippets/da-restock.liquid` — uses shop metafields, loads Moment.js from CDN |
| **Hextom Shipping Bar** | Disabled | Config block |
| **Shopify Inbox** | Disabled | Config block — custom greeting "Welcome to Hazel Boutique..." |

---

## 6. Settings Configuration

### Layout
- Page width: **1600px** (maximum)
- Section spacing: **0** (no spacing between sections)
- Grid spacing: 24px both directions

### Animations
- Scroll reveal: **disabled**
- Hover effects: **none**

### Buttons & Inputs
- Button radius: 0 (sharp corners), 1px border at 100% opacity, no shadow
- Inputs: 0 border, 0 radius, 0 shadow (completely flat/borderless)

### Cards
- Product cards: 18px corner radius, standard style, left-aligned, no padding/border/shadow
- Collection & blog cards: 0 corner radius, standard style, no shadows

### Badges
- Positioned top-left, 0 corner radius (square)

### Cart
- Type: **drawer** (not page or notification)
- Two featured collections in drawer: `fine-collection` and `all-sale` with custom images

### Search
- Predictive search: enabled
- Vendor and price display: off

### Localization
- Markets: **none configured** (single-market setup)
- 26 locale files present but no multi-market configuration
- Currency code display: disabled

### Social Links
- All empty in settings — social links are hardcoded in the mobile drawer instead

---

## 7. Identified Issues & Technical Debt

### Bugs
1. **CSS typo in header.liquid (line 41):** `900spx` should be `900px`
2. **Nested `<h3>` tags** in `card-product.liquid` — invalid HTML
3. **Homepage hero slides 2 and 3** retain Dawn placeholder text ("Tell your brand's story through images") — never customized
4. **"New Arrivals" featured collection** pulls from `all-products` instead of `new-arrivals-1`, though the "View More" link correctly points to the latter
5. **Default `page.json` template has its main section disabled** — any page using the default template renders empty (only header/footer)

### Code Quality
6. **`console.log` statements** present in cart drawer upsell JS and recently viewed products JS
7. **`nutTestTest` debug class** in `header-dropdown-menu-helper.liquid`
8. **IE11 compatibility code** in cart drawer (lines 684-703) — unnecessary
9. **Duplicate badge rendering** in `card-product.liquid` (once in `.card__inner`, once in outer `.card__content`)
10. **Moment.js loaded from CDN** by DA Restock — significant external dependency for simple date formatting

### Fragility
11. **All custom font URLs hardcoded** to Shopify CDN paths tied to store ID `1/0051/3264/8566` — will break on store migration
12. **All CDN logo URLs hardcoded** (hero script logos, footer logos) — same migration risk
13. **Hardcoded page links** in mobile drawer (Our Story, Store Locations, Contact Us, Sizing Guide) and header (Store Locations) — will break if page handles change
14. **Hardcoded social media URLs** in mobile drawer — not configurable from theme editor

### Disabled/Dead Code
15. **Dynamic checkout buttons** (Shopify Pay / Apple Pay / Google Pay) commented out in `buy-buttons.liquid`
16. **`recent-viewed-product-js.liquid` snippet** entirely wrapped in `{% comment %}` (duplicate of footer's active implementation)
17. **Customer account links** commented out in both the header and mobile drawer
18. **5 homepage sections disabled** (image-with-text, image banner, 2 collection lists, another image banner)
19. **Contact form section disabled** on contact page template
20. **Strawberry cursor CSS** commented out in `base.css`

### Consistency Gaps
21. **Collection pages** use portrait images; **search results** use adapt ratio. Secondary images show on collections but not search.
22. **Image ratio mismatch** — product cards force 3:4 via `--ratio-percent: 133%`, but some sections set "adapt" or "square" ratios

---

## 8. Pending Work (from goals.md)

### Accessibility
- Forward accessibility info, review site, send accessibility contact

### Pages Out of Place
- Sizing Guide, Our Story, Store Locations — reported as broken, mislabeled, or improperly linked

### Contact Information
- Consolidate onto a dedicated "Contact Us" page
- Remove from wherever it currently lives elsewhere

### Returns System
- Build a customer-facing returns flow:
  - Customer enters order number (+ possibly email)
  - System shows eligible items
  - Customer can initiate return
  - Generates a return slip/label to print
  - 21-day return window
- Update returns page with new physical address
- "Generate Returns" needs to look like a button

### Shop Categories
- Add "Mock necks" as a category
- Add "Perfume" under Accessories (only two perfumes)
- Move "Hazel Mini" (Mini Cherub) under Bottoms in Clothing

### Misc Fixes
- Fix "Follow us on Instagram" label
- Fix missing pages
- Update physical address to: 1709 Rt 34, Suite 3, Farmingdale, NJ 07719

---

## 9. Custom Element Registry (Complete)

| Tag Name | Class | Extends | File |
|----------|-------|---------|------|
| `quantity-input` | `QuantityInput` | `HTMLElement` | `global.js` |
| `menu-drawer` | `MenuDrawer` | `HTMLElement` | `global.js` |
| `header-drawer` | `HeaderDrawer` | `MenuDrawer` | `global.js` |
| `modal-dialog` | `ModalDialog` | `HTMLElement` | `global.js` |
| `modal-opener` | `ModalOpener` | `HTMLElement` | `global.js` |
| `deferred-media` | `DeferredMedia` | `HTMLElement` | `global.js` |
| `slider-component` | `SliderComponent` | `HTMLElement` | `global.js` |
| `slideshow-component` | `SlideshowComponent` | `SliderComponent` | `global.js` |
| `variant-selects` | `VariantSelects` | `HTMLElement` | `global.js` |
| `product-recommendations` | `ProductRecommendations` | `HTMLElement` | `global.js` |
| `cart-drawer` | `CartDrawer` | `HTMLElement` | `cart-drawer.js` |
| `cart-drawer-items` | `CartDrawerItems` | `CartItems` | `cart-drawer.js` |
| `cart-notification` | `CartNotification` | `HTMLElement` | `cart-notification.js` |
| `cart-remove-button` | `CartRemoveButton` | `HTMLElement` | `cart.js` |
| `cart-items` | `CartItems` | `HTMLElement` | `cart.js` |
| `cart-note` | `CartNote` | `HTMLElement` | `cart.js` |
| `details-disclosure` | `DetailsDisclosure` | `HTMLElement` | `details-disclosure.js` |
| `header-menu` | `HeaderMenu` | `DetailsDisclosure` | `details-disclosure.js` |
| `details-modal` | `DetailsModal` | `HTMLElement` | `details-modal.js` |
| `facet-filters-form` | `FacetFiltersForm` | `HTMLElement` | `facets.js` |
| `price-range` | `PriceRange` | `HTMLElement` | `facets.js` |
| `facet-remove` | `FacetRemove` | `HTMLElement` | `facets.js` |
| `localization-form` | `LocalizationForm` | `HTMLElement` | `localization-form.js` |
| `main-search` | `MainSearch` | `SearchForm` | `main-search.js` |
| `media-gallery` | `MediaGallery` | `HTMLElement` | `media-gallery.js` |
| `password-modal` | `PasswordModal` | `DetailsModal` | `password-modal.js` |
| `pickup-availability` | `PickupAvailability` | `HTMLElement` | `pickup-availability.js` |
| `pickup-availability-drawer` | `PickupAvailabilityDrawer` | `HTMLElement` | `pickup-availability.js` |
| `predictive-search` | `PredictiveSearch` | `SearchForm` | `predictive-search.js` |
| `price-per-item` | `PricePerItem` | `HTMLElement` | `price-per-item.js` |
| `product-form` | `ProductForm` | `HTMLElement` | `product-form.js` |
| `product-info` | `ProductInfo` | `HTMLElement` | `product-info.js` |
| `product-modal` | `ProductModal` | `ModalDialog` | `product-modal.js` |
| `product-model` | `ProductModel` | `DeferredMedia` | `product-model.js` |
| `quantity-popover` | `QuantityPopover` | `HTMLElement` | `quantity-popover.js` |
| `quick-add-modal` | `QuickAddModal` | `ModalDialog` | `quick-add.js` |
| `quick-order-list` | `QuickOrderList` | `HTMLElement` | `quick-order-list.js` |
| `quick-order-list-remove-button` | `QuickOrderListRemoveButton` | `HTMLElement` | `quick-order-list.js` |
| `quick-order-list-remove-all-button` | `QuickOrderListRemoveAllButton` | `HTMLElement` | `quick-order-list.js` |
| `recipient-form` | `RecipientForm` | `HTMLElement` | `recipient-form.js` |
| `search-form` | `SearchForm` | `HTMLElement` | `search-form.js` |
| `share-button` | `ShareButton` | `DetailsDisclosure` | `share.js` |
| `show-more-button` | `ShowMoreButton` | `HTMLElement` | `show-more.js` |

---

## 10. Metafield Dependencies

| Namespace | Key | Type | Used By |
|-----------|-----|------|---------|
| `custom` | `hex_color` | Variant metafield | Product card swatches, variant option swatches |
| `collection` | `custom_title` | Collection metafield (image) | Collection banner title images |
| `da-restock` | Various | Shop + product metafields | Back-in-stock notification configuration |

---

## 11. Key File Reference

**Custom/heavily modified (where the Hazel-specific work lives):**
- `layout/theme.liquid` — Custom fonts, mouse buddy, Pragmatica override
- `sections/hero.liquid` — Entirely custom hero section
- `sections/header.liquid` — Dual-header architecture, custom mega menu
- `sections/footer.liquid` — Recently viewed products, hardcoded logos, site credit
- `sections/main-collection-banner.liquid` — Metafield title images
- `sections/collection-list.liquid` — Alt image/title fields
- `sections/main-cart-footer.liquid` — Route shipping protection
- `snippets/card-product.liquid` — Custom badges, color swatches, fixed aspect ratio
- `snippets/cart-drawer.liquid` — "Wear it with" upsell, empty cart collections, Route div
- `snippets/buy-buttons.liquid` — Dynamic checkout commented out
- `snippets/header-drawer.liquid` — Hardcoded nav links, "Menu" text
- `snippets/header-dropdown-menu.liquid` — Visual mega menu with collection images
- `snippets/header-dropdown-menu-helper.liquid` — Flat secondary nav
- `snippets/header-search.liquid` — "Search" text label
- `snippets/pagination.liquid` — New Arrivals suppression, zero-padded numbers
- `snippets/product-variant-options.liquid` — Color swatches on button pickers
- `snippets/da-restock.liquid` — Third-party back-in-stock integration
- `assets/base.css` — Brand CSS overrides (lines ~3738+)
- `assets/cart.js` — "Wear With" upsell, GlobalE integration
- `config/settings_schema.json` — Mouse Buddy field, cart drawer collection fields

**Stock Dawn (unmodified or minimally modified):**
- All customer templates, 404, password, gift card
- Most section files (collage, collapsible-content, contact-form, custom-liquid, email-signup-banner, featured-blog, image-banner, image-with-text, multicolumn, multirow, newsletter, rich-text, slideshow, video, quick-order-list, related-products, predictive-search, pickup-availability)
- All icon snippets
- All JS files except `cart.js`
- All locale files
