# Hazel Boutique — Theme Research Report

## Overview

This is a Shopify theme for **Hazel Boutique**, a women's clothing and accessories boutique. The theme is a heavily customized fork of Shopify's official **Dawn theme v13.0.1**. There is no build toolchain in the repository — it deploys directly to Shopify via the Shopify CLI or theme editor.

The store sells: clothing (hoodies, mocknecks, barrel pants, joggers, and more), accessories (perfume pending), home goods, and vintage items under the "EVI11 Twin Vintage" label.

---

## Directory Structure

```
hazel/
├── assets/         104 files — JS, CSS, and image assets
├── config/         Theme settings schema and current data
├── docs/           Work notes and size charts
├── layout/         Global layout (theme.liquid + password.liquid)
├── locales/        54 translation files
├── sections/       56 Liquid section files
├── snippets/       77 reusable Liquid snippets
└── templates/      JSON template files for each page type
```

---

## Tech Stack

- **Language**: Shopify Liquid (templating), vanilla JavaScript (Custom Elements API), plain CSS
- **Base theme**: Dawn v13.0.1 by Shopify
- **No build system** — no webpack, no npm, no preprocessors; everything is vanilla
- **Custom Elements**: Extensively used for interactive components (sticky header, cart drawer, product form, sliders, etc.)
- **PubSub pattern**: `pubsub.js` implements a simple subscribe/publish event bus used for cart state updates across components

---

## Layout: `layout/theme.liquid`

The global HTML shell. Key responsibilities:

- Sets font-face declarations (see Fonts section below)
- Injects CSS custom properties for all design tokens (colors, spacing, radii, shadows, typography scale) from `settings_data.json`
- Outputs `content_for_header` (Shopify app scripts and pixels)
- Renders the cart drawer (when cart type is `drawer`)
- Renders `header-group` sections
- Contains the `#follower` mouse cursor element with easing animation
- Renders `footer-group` sections
- Exposes global JS objects: `window.routes`, `window.cartStrings`, `window.variantStrings`, `window.accessibilityStrings`

### Custom Mouse Follower

A `<div id="follower">` sits inside `<main>` and animates smoothly to the mouse position using `requestAnimationFrame` with an easing factor of `0.2`. The follower image is configurable via a `mouse_image` setting in the theme schema. It is hidden on mobile via CSS (`display: none` below 749px).

---

## Fonts

Four custom font families are declared in `theme.liquid`. Current status:

| Family | Weights | Status | Source |
|---|---|---|---|
| Pragmatica | 400 (Book), 300 (Light) | **Disabled** — fallback to system fonts | Was: Shopify CDN |
| PragmaticaCondensed | 400 (Book), 300 (Light) | **Disabled** — fallback to system fonts | Was: Shopify CDN |
| Millionare | 400 (Script) | Active | Shopify CDN |
| Lustria | 400 (Regular) | Active | Shopify CDN |

**Important**: On 2026-03-30, Shopify disabled the Pragmatica and PragmaticaCondensed fonts (noted in a comment block in `theme.liquid`). The `@font-face` declarations were replaced with `src: local('Arial'), local('Helvetica Neue'), local('Helvetica'), local('sans-serif')`. CSS variables still reference `'Pragmatica'` as the first font family, so system sans-serif is silently substituted everywhere. This is a known open bug in `docs/goals.md`.

---

## Header Architecture

The header is uniquely implemented with **two separate header elements** instead of one.

### `masonHeaderModifierOne`
- The primary header — always in the DOM and initially visible
- Contains: hamburger drawer (mobile), search button, Store Locations link (desktop only), logo, navigation menu, cart icon
- On mobile (<900px): sticky via `shopify-section-header-sticky`
- On desktop (≥900px): sits in normal document flow; hides on scroll-down, reveals on scroll-up via the `StickyHeader` custom element

### `masonHeaderModifierTwo`
- A secondary compact header for desktop only
- Hidden on mobile (<900px) with `display: none`
- On desktop: positioned `fixed` at `top: 0`, starts hidden behind `masonHeaderModifierOne` via `z-index: -2` and negative `margin-top`
- When the user scrolls past the primary header, JavaScript adds `scrolled-past-header` class, which transitions `masonHeaderModifierTwo` to `margin-top: 0` with a 200ms ease-out — creating a "slide down from top" effect
- Contains: logo, navigation menu, search, cart icon (no Store Locations link)

### Navigation Behavior
Desktop navigation uses `<details>`/`<summary>` for dropdown menus, but a custom `<script>` overrides click behavior with `mouseover`/`mouseout` events so menus open on hover.

### Mega Menu Configuration
The header schema supports configuring mega-menu images for up to 7 main menu positions. Each position can have two image+link+text pairs (A and B). These are rendered via `header-mega-menu.liquid` and `header-mega-menu-helper.liquid`.

### Cart Count Style
Cart item count is displayed as `(3)` with parenthesis spans, not as a badge bubble. This applies to both zero and non-zero states.

### Account Button
The account/login button is **commented out** in both header instances.

---

## Homepage (`templates/index.json`)

Active sections in render order:

1. **Hero slideshow** — 3 slides with images from Shopify CDN, linking to new-arrivals and all-clothing collections
2. **Featured Collection "New Arrivals"** — 8 products, 4 columns desktop, 2 mobile, quick-add enabled
3. **Featured Collection "EVI11 TWIN VINTAGE"** — 4 products from the `vintage` collection, custom heading size h1
4. **Rich Text** — "Follow us on Instagram @hazelboutique"
5. **Apps block** — Instafeed Instagram embed
6. **Multicolumn** — 4 columns: Our Story, Store Locations, Customer Love, Size Guide (icon images 64×64px, overridden via custom CSS in the template JSON)

Disabled (not rendered) sections: image-with-text "Field of Dreams Collection", image-banners, collection-lists for clothing/accessories/home and new-arrivals/hazel-brand.

---

## Product Page (`templates/product.json`)

Block render order within `main-product`:

1. **Judge.me preview badge** (app block)
2. **Text** — displays `{{ product.vendor }}`
3. **Title**
4. **Price**
5. **Variant picker** — button style, circle swatches
6. **Buy buttons** — with dynamic checkout (Apple Pay/Shop Pay surface) and gift card recipient form enabled
7. **Complementary products** — "Complete the look", max 10 products, 3 per page, counter pagination, square images, quick-add enabled
8. **Description**

Below the main section:
- Rich text section with "Ratings and Reviews" heading
- Apps block with Judge.me review widget
- Related products section — "You might also love...", 4 products, 4 columns desktop, 2 mobile, portrait images with hover secondary image

Settings: sticky product info column, large media size, cover media fit, columns gallery layout, lightbox zoom, left media position.

---

## Collection Pages

### `sections/main-collection-banner.liquid`
Supports a `collection.metafields.collection.custom_title` field. When set, the collection title is rendered as an `<img>` (an image-based title) instead of text. This allows per-collection custom logotype headers.

### `sections/main-collection-product-grid.liquid`
- Supports filter/sort via `facets.js` (vertical and drawer filter types)
- Pagination via `paginate` tag
- Quick-add enabled
- Products per page configurable in section settings

---

## Custom Page Templates

### `templates/page.contact.json`
Uses `main-page` section + a disabled `contact-form` section. The contact page content comes from the Shopify admin page editor (rich text). The contact form section is disabled — meaning the form shown on the page is embedded directly in the page's rich text content, not rendered from the contact-form section.

### `templates/page.about.json`
Uses `main-page` section only. The "Our Story" page has a special code path in `sections/main-page.liquid`:

```liquid
{% if page.handle == 'our-story' %}
  <!-- Renders a full-width hero image from CDN, a decorative "ABOUT" heading, 
       and a script-logo image -->
{% endif %}
```

The hero image and logo image are hardcoded CDN URLs in the Liquid file — not configurable from the theme editor.

---

## Third-Party App Integrations

| App | Integration Point | Function |
|---|---|---|
| **Judge.me Reviews** | `product.json` blocks | Review badges and widget on product pages |
| **Instafeed** | `templates/index.json` apps block | Instagram feed on homepage |
| **DA Restock** | `snippets/da-restock.liquid` | Back-in-stock notification forms |
| **Route Insurance** | Open bug — needs hiding | Route's shipping protection product appears in cart (unwanted) |
| **AccessEase** | Installed, not in codebase | Accessibility auditing tool in Shopify admin |

### DA Restock (`snippets/da-restock.liquid`)
Reads from shop and product metafields under `da-restock` namespace. Two modes:
- **Always-show mode** (`alwaysShow == 'true'`): Shows form for any product/variant that has no inventory, with an optional "back in stock date" message using Moment.js
- **Per-variant mode**: Hidden `div`s per variant, shown via JS when an unavailable variant is selected
- Collections can be excluded via `collection.metafields['da-restock'].forbidden`
- Loads Moment.js from an external CDN (`MomentJS.com`) — has a leading space in the URL which may cause issues

---

## Recently Viewed Products

`snippets/recent-viewed-product-js.liquid` exists but the **entire snippet is wrapped in a `{% comment %}` block**, meaning it renders nothing. The logic inside:
- Stores up to 4 product URLs, titles, images, and prices in `localStorage.recently_viewed`
- Would render a client-side "Recently viewed" product grid by DOM-injecting HTML
- Was never fully shipped — the `{% comment %}` block makes it completely inert

The footer section (`sections/footer.liquid`) also contains a duplicate copy of the `setRecentlyViewedPdp()` function (not commented out), which does save to localStorage — but no display logic renders the stored data.

---

## CSS Architecture

`assets/base.css` is **7,044 lines** — the largest file in the project. It contains:
- Dawn's original base styles (~first ~3,600 lines)
- All custom Hazel overrides appended after the base (lines ~3,600–7,044)

### Key custom CSS additions:
- **Global typography overrides** (line ~84): `letter-spacing: 0px`, `text-underline-offset: 0.3rem`, `text-decoration-thickness: 1px` on all elements
- **Cursor easter eggs** (line ~89): Commented-out strawberry cursor URLs (`strawberryHazel.png`, `strawberryHazelHover.png`)
- **Sparkle animation** (line ~3617): CSS variable `--sparkle: url("./sparkle.gif")` available for hover animations
- **Header system** (line ~3892+): All custom `masonHeaderModifierOne/Two`, `headerLeftMenu`, `storeLocations` CSS
- **Custom h2 weight override** in product.json for the ratings heading: `font-weight: 400`

---

## JavaScript Architecture

All JS uses native Custom Elements (Web Components API). No framework. Key files:

| File | Purpose |
|---|---|
| `pubsub.js` | Simple event bus with `subscribe(event, cb)` / `publish(event, data)` |
| `global.js` | Focus trap, ARIA utilities, `debounce`, `fetchConfig`, keyboard handling |
| `constants.js` | Shared constants (debounce timers, PubSub event names) |
| `cart.js` | `CartItems` and `CartRemoveButton` custom elements; AJAX cart updates |
| `cart-drawer.js` | `CartDrawer` and `CartDrawerItems` custom elements |
| `product-form.js` | `ProductForm` custom element — handles add-to-cart via Fetch API |
| `product-info.js` | `ProductInfo` — manages variant switching, media gallery sync |
| `animations.js` | `IntersectionObserver`-based scroll reveal animations |
| `predictive-search.js` | `PredictiveSearch` custom element for live search |
| `facets.js` | Collection filter/sort with URL state management |
| `magnify.js` | Product image zoom on hover |
| `details-disclosure.js` | Dropdown menus using `<details>` |
| `details-modal.js` | Modal dialogs (search modal) |

---

## Color Scheme System

Colors are defined as CSS custom properties via `settings_schema.json` color scheme groups. Each scheme exposes RGB component variables (e.g., `--color-background: R,G,B`) rather than full hex values, allowing alpha compositing with `rgba(var(--color-background), 0.5)`.

The theme uses 4+ color schemes. Scheme assignment is per-section via the Shopify theme editor.

---

## Settings Schema Custom Additions

Beyond Dawn defaults, `settings_schema.json` adds:
- **`mouse_image`** (image_picker) — the configurable cursor follower image in the Logo section

---

## Known Issues and Open Work

From `docs/goals.md`, the active issues relevant to the codebase:

| Issue | Location |
|---|---|
| Pragmatica font replaced by system fallback | `layout/theme.liquid` lines ~255–326 |
| Contact email needs update (Gmail → shop@hazelboutique.com) | Shopify admin page content |
| Returns form routing needs verification | Shopify admin / contact form handler |
| PDP "press play" video overlay broken on mobile | `sections/main-product.liquid` or product media blocks |
| Route Insurance product appearing in cart | Cart/checkout settings or app configuration |
| Product count on PDP should be removed | Variant picker or product info blocks |
| Account button commented out | `sections/header.liquid` lines ~301–314 |
| Recently viewed snippet is fully commented out | `snippets/recent-viewed-product-js.liquid` |
| DA Restock loads Moment.js with leading space in URL | `snippets/da-restock.liquid` line 17 |
| Header breakpoint typo: `900spx` | `sections/header.liquid` line 41 |
| Shopify store categories need updating | Shopify admin navigation |

---

## Localization

54 locale files in `locales/`. The country and language selectors in both the announcement bar and header are **disabled by default** in the current settings. The theme supports multi-currency and multi-language but it is not configured for production use.

---

## Size Chart Reference

From `docs/goals.md` — all Hazel brand styles are oversized fit, models wear L–2XL:

- **Hoodie**: S–2XL, chest 48–64", length 27–31", sleeve 23–27"
- **Mockneck**: M/L–2X/3X, chest 50–68", length 27–31.5", sleeve 24–27"
- **Barrel Pant**: S–2XL, waist 26–44", hip 46–62", inseam 29–33"
- **Jogger**: S–2XL, waist 26–44", hip 44–60", inseam 30–34"

Reference images: `docs/size-chart-hoodie.png`, `docs/size-chart-mockneck.png`, `docs/size-chart-barrel-pant.png`, `docs/size-chart-jogger.png`

---

## Design Direction

Per `docs/goals.md`, the target aesthetic is **madewell.com** — clean, confident, product-forward. The theme is being progressively refined toward that standard, with accessibility and performance as continuous priorities.
