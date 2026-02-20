# Hazel Boutique — Implementation Plan

This plan addresses every item in `goals.md`. Each task includes the exact files to change, what to do, and code snippets where relevant.

---

## Task 1: Fix Pages Out of Place

**Problem:** Sizing Guide, Our Story, and Store Locations are "out of place." Based on research, the issue is that these pages are linked via hardcoded URLs in the mobile drawer and header rather than through the Shopify menu system, making them unmanageable. Additionally, the default `page.json` template has its main section **disabled** — any page using that template renders blank.

### 1A. Enable the default page template

**File:** `templates/page.json`

The `main` section is currently disabled. Enable it so pages using the default template actually render their content.

```json
// BEFORE
"main": {
  "type": "main-page",
  "disabled": true,
  "settings": {
    "padding_top": 28,
    "padding_bottom": 28
  }
}

// AFTER — remove the "disabled" line
"main": {
  "type": "main-page",
  "settings": {
    "padding_top": 28,
    "padding_bottom": 28
  }
}
```

### 1B. Verify page handles match hardcoded links

The mobile drawer and header link to these exact URLs. Each page must exist in Shopify admin with the correct handle and assigned template.

**Step-by-step for each page:**

**Our Story:**

1. Go to **Shopify Admin > Online Store > Pages**
2. Find the page titled "Our Story" (or similar)
3. Click the page to edit it. Scroll to the bottom of the editor and look at the **URL handle** — it must be `our-story` (so the URL is `/pages/our-story`)
4. If the handle is different, click it to edit and change it to `our-story`
5. In the right sidebar under **Template**, select `page.about` from the dropdown
6. Save

**Store Locations:**

1. In **Pages**, find the "Store Locations" page
2. Confirm the URL handle is `store-locations`
3. Set the template to `page` (the default page template — we're enabling it in Task 1A)
4. Save

**Contact Us:**

1. In **Pages**, find the "Contact Us" page
2. Confirm the URL handle is `contact-us`
3. Set the template to `page.contact`
4. Save

**Sizing Guide:**

1. In **Pages**, find the "Sizing Guide" (or "Sizing") page
2. Confirm the URL handle is `sizing`
3. Set the template to `page.contact` (this gives it the same narrow centered layout as the contact page)
4. Save

**If any page doesn't exist yet**, create it: click **Add Page** at the top right, enter the title, add body content, set the handle, assign the template, and save.

### 1C. Add these pages to the Shopify navigation menu

**Step-by-step:**

1. Go to **Shopify Admin > Online Store > Navigation**
2. Click on `navbar-menu` (the main site navigation)
3. Look at the existing menu items. If Our Story, Store Locations, Contact Us, and Sizing Guide are not present as menu items, add them:
   - Click **Add menu item**
   - Name: `Our Story` / Link: search for "Our Story" in the Pages dropdown and select it
   - Repeat for Store Locations, Contact Us, and Sizing Guide
   - Drag them to the desired position in the menu hierarchy (these likely belong as top-level items or under an "Info" / "About" parent)
4. Click **Save**
5. Now update the footer menus. Go back to **Navigation** and click on `footer-quick-links`
6. Add links to Our Story, Store Locations, Contact Us, Sizing Guide, and Returns (once created) if they aren't already there
7. Save
8. Repeat for any other footer menus (`footer-socials`, `footer-categories-1`, `footer-categories-2`) if those pages belong in multiple footer columns

---

## Task 2: Update Contact Information

**Problem:** Contact info needs to be consolidated onto the Contact Us page. The updated address is:

```
1709 Rt 34
Suite 3
Farmingdale, NJ 07719
```

### 2A. Update the Contact Us page content

**Step-by-step:**

1. Go to **Shopify Admin > Online Store > Pages**
2. Click on the **"Contact Us"** page to edit it
3. In the rich-text body editor, replace the existing content with the consolidated contact information. Use this structure:

```
Hazel Boutique

1709 Rt 34
Suite 3
Farmingdale, NJ 07719

Phone: [your phone number]
Email: [your email address]

Hours:
Monday – Friday: [hours]
Saturday: [hours]
Sunday: [hours]
```

4. For the email address, highlight the email text, click the link icon in the toolbar, and make it a `mailto:` link (e.g., `mailto:hello@hazelboutique.com`)
5. If you want the email link to have an underline, add the CSS class `rteEmailLink` to it (the template already has CSS for that class)
6. Make sure the template is set to `page.contact` in the right sidebar
7. Save

**After saving:** Remove any duplicate contact information from other pages (e.g., if the Store Locations page or Our Story page also lists an old address or phone number, edit those pages to remove it). The goal is one canonical source of contact info on this page.

### 2B. Enable the contact form

**File:** `templates/page.contact.json`

The contact form section is currently disabled. Enable it so customers can submit inquiries directly.

```json
// BEFORE
"form": {
  "type": "contact-form",
  "disabled": true,
  "settings": {
    "heading": "",
    "heading_size": "h1",
    "color_scheme": "",
    "padding_top": 36,
    "padding_bottom": 36
  }
}

// AFTER — remove "disabled", add a heading
"form": {
  "type": "contact-form",
  "settings": {
    "heading": "Send Us a Message",
    "heading_size": "h1",
    "color_scheme": "",
    "padding_top": 36,
    "padding_bottom": 36
  }
}
```

### 2C. Update the Store Locations page

**Step-by-step:**

1. Go to **Shopify Admin > Online Store > Pages**
2. Click on the **"Store Locations"** page
3. Update the body content with the new address:

```
Hazel Boutique
1709 Rt 34, Suite 3
Farmingdale, NJ 07719
```

4. If you want to embed a Google Maps link or iframe, add it here as well. To add a Google Maps link: include an `<a>` tag linking to `https://maps.google.com/?q=1709+Rt+34+Suite+3+Farmingdale+NJ+07719`
5. Make sure the template is set to `page` (the default page template)
6. Save

### 2D. Check for stale address references

**Step-by-step:**

1. In **Shopify Admin > Online Store > Pages**, open each page one at a time and search the body content (Ctrl+F / Cmd+F in your browser) for any old address text. If found, either remove it or update it to the new address
2. Check the footer: Go to **Online Store > Navigation** and look at each footer menu. If any menu item links to an old address or maps URL, update the link
3. Check **Settings > Store details** (top-level Shopify admin settings) — update the store address there as well, since it feeds into order confirmations, shipping labels, and the `shop.address` Liquid object

---

## Task 3: Build Returns System

**Problem:** Hazel Boutique wants a customer-facing returns flow where customers enter an order number (and email), see eligible items, and can initiate a return with a printable slip. 21-day return window.

### Approach

Build a dedicated returns page template with a two-step form:

1. **Step 1 — Lookup:** Customer enters order number + email. A `{% form 'contact' %}` sends this to the store. Simultaneously, JavaScript shows a printable return slip with the store's return address and instructions.
2. **Step 2 — Return Slip:** A styled, printable return slip appears with the order number, return address, and 21-day policy. Customer prints it and includes it in their return package.

This is theme-only (no app required). The store reviews return requests via the Shopify contact form email notifications and processes refunds manually in admin.

### 3A. Create the returns page template

**New file:** `templates/page.returns.json`

```json
{
  "sections": {
    "main": {
      "type": "main-page",
      "settings": {
        "padding_top": 36,
        "padding_bottom": 0
      }
    },
    "returns-form": {
      "type": "returns-form",
      "settings": {
        "heading": "Start a Return",
        "return_address_line_1": "1709 Rt 34",
        "return_address_line_2": "Suite 3",
        "return_address_city_state_zip": "Farmingdale, NJ 07719",
        "return_window_days": 21,
        "color_scheme": "scheme-1",
        "padding_top": 0,
        "padding_bottom": 36
      }
    }
  },
  "order": ["main", "returns-form"]
}
```

### 3B. Create the returns form section

**New file:** `sections/returns-form.liquid`

```liquid
{{ 'section-contact-form.css' | asset_url | stylesheet_tag }}

{%- style -%}
  .section-{{ section.id }}-padding {
    padding-top: {{ section.settings.padding_top | times: 0.75 | round: 0 }}px;
    padding-bottom: {{ section.settings.padding_bottom | times: 0.75 | round: 0 }}px;
  }
  @media screen and (min-width: 750px) {
    .section-{{ section.id }}-padding {
      padding-top: {{ section.settings.padding_top }}px;
      padding-bottom: {{ section.settings.padding_bottom }}px;
    }
  }

  .returns-form { max-width: 580px; margin: 0 auto; }
  .returns-form .field { margin-bottom: 16px; }
  .returns-slip { display: none; max-width: 580px; margin: 0 auto; padding: 40px; border: 2px dashed var(--color-foreground); }
  .returns-slip.active { display: block; }
  .returns-slip__header { text-align: center; margin-bottom: 24px; }
  .returns-slip__address { margin-bottom: 24px; line-height: 1.6; }
  .returns-slip__order { margin-bottom: 24px; }
  .returns-slip__policy { font-size: 14px; opacity: 0.7; margin-bottom: 24px; }
  .returns-slip__cut-line { border-top: 1px dashed var(--color-foreground); padding-top: 16px; margin-top: 24px; text-align: center; font-size: 13px; opacity: 0.5; }

  @media print {
    .returns-form, .site-header, .site-footer,
    header, footer, .announcement-bar, .header-wrapper,
    .section-header, .footer, #shopify-section-header,
    #shopify-section-footer, #shopify-section-announcement-bar,
    .returns-slip__no-print { display: none !important; }
    .returns-slip { display: block !important; border: 2px dashed #000; }
    .returns-slip.active { display: block !important; }
  }
{%- endstyle -%}

<div class="color-{{ section.settings.color_scheme }} gradient">
  <div class="page-width page-width--narrow section-{{ section.id }}-padding">

    {%- if section.settings.heading != blank -%}
      <h2 class="title title-wrapper--no-top-margin {{ section.settings.heading_size }}">
        {{ section.settings.heading }}
      </h2>
    {%- endif -%}

    <!-- STEP 1: Return Request Form -->
    <div class="returns-form" id="ReturnsForm">
      <p style="margin-bottom: 24px;">
        Enter your order number and email address below. We'll generate a return slip you can print and include in your package.
      </p>

      {%- form 'contact', id: 'ReturnsContactForm', class: 'isolate' -%}
        {%- if form.posted_successfully? -%}
          <h2 class="form-status form-status-list form__message" tabindex="-1" autofocus>
            {% render 'icon-success' %}
            Your return request has been submitted. Please print the return slip below.
          </h2>
        {%- elsif form.errors -%}
          <div class="form__message">
            <h2 class="form-status caption-large text-body" role="alert" tabindex="-1" autofocus>
              {% render 'icon-error' %}
              {{ 'templates.contact.form.error_heading' | t }}
            </h2>
          </div>
        {%- endif -%}

        <!-- Hidden field to tag this as a return request -->
        <input type="hidden" name="contact[subject]" value="Return Request">
        <input type="hidden" name="contact[tags]" value="return-request">

        <div class="field">
          <input
            class="field__input"
            type="text"
            id="ReturnsForm-order"
            name="contact[Order Number]"
            required
            placeholder="Order Number (e.g. #1001)"
          >
          <label class="field__label" for="ReturnsForm-order">Order Number</label>
        </div>

        <div class="field">
          <input
            class="field__input"
            type="email"
            id="ReturnsForm-email"
            name="contact[email]"
            required
            autocomplete="email"
            spellcheck="false"
            autocapitalize="off"
            value="{% if customer %}{{ customer.email }}{% endif %}"
            placeholder="Email Address"
          >
          <label class="field__label" for="ReturnsForm-email">Email Address</label>
        </div>

        <div class="field">
          <textarea
            rows="5"
            id="ReturnsForm-reason"
            class="text-area field__input"
            name="contact[Return Reason]"
            placeholder="Which item(s) are you returning and why?"
          >{{- form.body -}}</textarea>
          <label class="form__label field__label" for="ReturnsForm-reason">Items &amp; Reason for Return</label>
        </div>

        <div class="contact__button" style="display: flex; gap: 12px; flex-wrap: wrap;">
          <button type="submit" class="button">Submit Return Request</button>
          <button type="button" class="button button--secondary" id="GenerateReturnSlip">
            Generate Return Slip
          </button>
        </div>
      {%- endform -%}
    </div>

    <!-- STEP 2: Printable Return Slip -->
    <div class="returns-slip" id="ReturnSlip">
      <div class="returns-slip__header">
        <h2>Return Slip</h2>
        <p><strong>{{ shop.name }}</strong></p>
      </div>

      <div class="returns-slip__order">
        <p><strong>Order Number:</strong> <span id="SlipOrderNumber">—</span></p>
        <p><strong>Email:</strong> <span id="SlipEmail">—</span></p>
        <p><strong>Date Generated:</strong> <span id="SlipDate">—</span></p>
      </div>

      <div class="returns-slip__address">
        <p><strong>Return to:</strong></p>
        <p>
          {{ shop.name }}<br>
          {{ section.settings.return_address_line_1 }}<br>
          {%- if section.settings.return_address_line_2 != blank -%}
            {{ section.settings.return_address_line_2 }}<br>
          {%- endif -%}
          {{ section.settings.return_address_city_state_zip }}
        </p>
      </div>

      <div class="returns-slip__items">
        <p><strong>Item(s) Being Returned:</strong></p>
        <p id="SlipItems" style="white-space: pre-line;">—</p>
      </div>

      <div class="returns-slip__policy">
        <p>Items must be returned within <strong>{{ section.settings.return_window_days }} days</strong> of delivery in original condition with tags attached. Please include this slip in your return package.</p>
      </div>

      <div class="returns-slip__cut-line">
        ✂ Cut along this line and include in your package
      </div>

      <div class="returns-slip__no-print" style="margin-top: 24px; text-align: center;">
        <button type="button" class="button" onclick="window.print()">Print Return Slip</button>
      </div>
    </div>

  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('GenerateReturnSlip');
    const slip = document.getElementById('ReturnSlip');
    const form = document.getElementById('ReturnsForm');

    if (generateBtn) {
      generateBtn.addEventListener('click', function () {
        const orderInput = document.getElementById('ReturnsForm-order');
        const emailInput = document.getElementById('ReturnsForm-email');
        const reasonInput = document.getElementById('ReturnsForm-reason');

        if (!orderInput.value.trim()) {
          orderInput.focus();
          orderInput.reportValidity();
          return;
        }

        if (!emailInput.value.trim() || !emailInput.validity.valid) {
          emailInput.focus();
          emailInput.reportValidity();
          return;
        }

        document.getElementById('SlipOrderNumber').textContent = orderInput.value.trim();
        document.getElementById('SlipEmail').textContent = emailInput.value.trim();
        document.getElementById('SlipDate').textContent = new Date().toLocaleDateString('en-US', {
          year: 'numeric', month: 'long', day: 'numeric'
        });
        document.getElementById('SlipItems').textContent = reasonInput.value.trim() || 'See order details';

        slip.classList.add('active');
        slip.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }
  });
</script>

{% schema %}
{
  "name": "Returns Form",
  "tag": "section",
  "class": "section",
  "settings": [
    {
      "type": "inline_richtext",
      "id": "heading",
      "default": "Start a Return",
      "label": "Heading"
    },
    {
      "type": "select",
      "id": "heading_size",
      "options": [
        { "value": "h2", "label": "Small" },
        { "value": "h1", "label": "Medium" },
        { "value": "h0", "label": "Large" }
      ],
      "default": "h1",
      "label": "Heading size"
    },
    {
      "type": "text",
      "id": "return_address_line_1",
      "label": "Return Address Line 1",
      "default": "1709 Rt 34"
    },
    {
      "type": "text",
      "id": "return_address_line_2",
      "label": "Return Address Line 2",
      "default": "Suite 3"
    },
    {
      "type": "text",
      "id": "return_address_city_state_zip",
      "label": "City, State, ZIP",
      "default": "Farmingdale, NJ 07719"
    },
    {
      "type": "range",
      "id": "return_window_days",
      "min": 7,
      "max": 90,
      "step": 1,
      "default": 21,
      "label": "Return Window (days)"
    },
    {
      "type": "color_scheme",
      "id": "color_scheme",
      "label": "Color scheme",
      "default": "scheme-1"
    },
    {
      "type": "range",
      "id": "padding_top",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "label": "Top padding",
      "default": 36
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "label": "Bottom padding",
      "default": 36
    }
  ],
  "presets": [
    {
      "name": "Returns Form"
    }
  ]
}
{% endschema %}
```

### 3C. Create the returns page in Shopify Admin

**Step-by-step:**

1. Go to **Shopify Admin > Online Store > Pages**
2. Click **Add Page** (top right)
3. **Title:** `Returns`
4. **Body content** — paste in your returns policy. Here's a suggested starting point (edit to match your actual policy):

```
Returns & Exchanges

We want you to love your purchase. If something isn't right, we're here to help.

Return Policy:
- Items may be returned within 21 days of delivery
- Items must be in original, unworn condition with all tags attached
- Sale items are final sale and cannot be returned
- Shipping costs are non-refundable

How to Start a Return:
Use the form below to submit your return request. Enter your order number and email address, then click "Generate Return Slip" to create a printable slip to include in your package.

Ship your return to:
Hazel Boutique
1709 Rt 34, Suite 3
Farmingdale, NJ 07719

Once we receive and inspect your return, we'll process your refund within 5-7 business days.

Questions? Contact us at [your email] or visit our Contact Us page.
```

5. Scroll down in the editor. Click **URL handle** and confirm it is `returns` (it should auto-generate from the title)
6. In the right sidebar under **Theme template**, select `page.returns` from the dropdown (this template will exist after we create the `templates/page.returns.json` and `sections/returns-form.liquid` files in Tasks 3A and 3B)
7. Set **Visibility** to `Visible`
8. Click **Save**

### 3D. Add returns link to navigation

**File:** `snippets/header-drawer.liquid`

Add a "Returns" link to the hardcoded utility links in the mobile drawer (after "Sizing Guide"):

```liquid
<!-- Add after the Sizing Guide <li> (around line 335) -->
<li class="mobile-facets__item list-menu__item">
  <a href="/pages/returns" class="mobile-facets__open">
    <span>Returns</span>
  </a>
</li>
```

**Also add to the footer and main navigation:**

1. Go to **Shopify Admin > Online Store > Navigation**
2. Click on `footer-quick-links`
3. Click **Add menu item**, name it `Returns`, and link it to the "Returns" page
4. Save
5. Go back to **Navigation**, click on `navbar-menu`
6. If there's an "Info" or "Help" parent item, add "Returns" as a child item under it. Otherwise, add it as a top-level item
7. Save

---

## Task 4: Update Shop Categories

**Problem:** Need to add "Mock necks" and "Perfume" categories, and move "Hazel Mini" (Mini Cherub) under Bottoms.

All of these are **Shopify Admin tasks**, not theme code changes:

### 4A. Create "Mock Necks" collection

**Step-by-step:**

1. Go to **Shopify Admin > Products > Collections**
2. Click **Create collection** (top right)
3. **Title:** `Mock Necks`
4. **Description:** Optional — add a short description like "Stylish mock neck tops and sweaters"
5. Under **Collection type**, select **Automated**
6. Set the condition: **Product tag** → **is equal to** → `mock neck`
7. Click **Save**
8. Now tag the relevant products: Go to **Products > All products**
9. Find each mock neck product. Click into it, scroll to the **Tags** field in the right sidebar, type `mock neck`, and press Enter to add the tag
10. Save each product. They will auto-populate into the Mock Necks collection
11. If you want a collection image: Go back to **Collections > Mock Necks**, scroll down to **Collection image**, and upload a photo
12. If you want a custom title image (like other collections use): Go to **Settings > Metafields > Collections**, find the `custom_title` metafield, and upload a styled title image for this collection

### 4B. Create "Perfume" collection

**Step-by-step:**

1. Go to **Shopify Admin > Products > Collections**
2. Click **Create collection**
3. **Title:** `Perfume`
4. Under **Collection type**, select **Automated**
5. Set the condition: **Product tag** → **is equal to** → `perfume`
6. Click **Save**
7. Go to **Products > All products** and find the two perfume products
8. Click into each one, add the tag `perfume` in the Tags field, and save
9. They will auto-populate into the Perfume collection
10. Optionally add a collection image

### 4C. Move "Hazel Mini" (Mini Cherub) under Bottoms

**Step-by-step:**

1. Go to **Shopify Admin > Products > Collections**
2. Find the **"Bottoms"** collection and click into it
3. Check how it's set up:
   - If it says **"Automated"** at the top, look at the conditions (e.g., "Product tag is equal to `bottoms`"). Note the tag name
   - If it says **"Manual"**, you'll add products directly
4. Go to **Products > All products**
5. Search for **"Mini Cherub"**
6. Click into the product
7. **If Bottoms is automated:** In the **Tags** field (right sidebar), add the tag that matches the Bottoms collection condition (e.g., `bottoms`). Save
8. **If Bottoms is manual:** Go back to **Collections > Bottoms**, scroll to the Products section, click **Browse**, search for "Mini Cherub", select it, and click **Add**
9. Verify: Go to **Collections > Bottoms** and confirm Mini Cherub now appears in the product list
10. If "Hazel Mini" exists as its own separate collection and is no longer needed, you can either leave it (it won't hurt anything) or delete it from **Collections**

### 4D. Update navigation menus

**Step-by-step:**

1. Go to **Shopify Admin > Online Store > Navigation**
2. Click on **`navbar-menu`** (the main header navigation)
3. Find the **"Clothing"** menu item. Click the arrow/handle to expand it and see its children
4. Click **Add menu item** inside the Clothing submenu
5. Name: `Mock Necks` / Link: search for "Mock Necks" in the Collections dropdown and select it
6. Drag it to the desired position among the other Clothing subcategories
7. Now find the **"Accessories"** menu item and expand it
8. Click **Add menu item** inside the Accessories submenu
9. Name: `Perfume` / Link: search for "Perfume" in the Collections dropdown and select it
10. Click **Save**
11. Verify on the live site: hover over "Clothing" in the header nav and confirm "Mock Necks" appears. Hover over "Accessories" and confirm "Perfume" appears
12. **Mega menu images (optional):** If you want the new collections to show promotional images in the dropdown menus, go to **Online Store > Themes > Customize**, navigate to the header section settings, and configure the mega menu position slots with images for the new collections

---

## Task 5: Fix "Follow us on Instagram" Label

**Problem:** The Instagram label/link on the homepage needs fixing.

There are two ways to fix this — via the theme editor (easiest) or via the template JSON file:

**Option A — Fix via Theme Editor (recommended):**

1. Go to **Shopify Admin > Online Store > Themes**
2. Click **Customize** on the live theme
3. You should be on the **Homepage**. Scroll down to the "Follow us on Instagram" section
4. Click on the section to select it, then click the **heading block** in the left sidebar
5. Fix the heading text to read exactly: `Follow us on Instagram`
6. Click the **text block** below it
7. Make sure the text contains a working link: highlight `@hazelboutique`, click the link icon, and set the URL to `https://www.instagram.com/hazel_boutique`
8. Click **Save** in the top right

**Option B — Fix via code:**

**File:** `templates/index.json`

The rich text section (`rich_text_niFCNN`) renders the Instagram heading. The heading and text blocks should look like this:

```json
{
  "type": "heading",
  "settings": {
    "heading": "Follow us on Instagram"
  }
}
```

```json
{
  "type": "text",
  "settings": {
    "text": "<p><a href=\"https://www.instagram.com/hazel_boutique\" target=\"_blank\" title=\"Hazel Boutique on Instagram\">@hazelboutique</a></p>"
  }
}
```

Verify the current content and correct any typos or broken links. The `@hazelboutique` handle should link to `https://www.instagram.com/hazel_boutique`.

---

## Task 6: Accessibility Review

**Problem:** Review accessibility across the site and forward findings.

The research uncovered significant accessibility issues. Here are the fixes, prioritized:

### 6A. CRITICAL — Remove `aria-hidden="true"` from `visually-hidden` elements

This is the single highest-impact fix. The pattern `class="visually-hidden" aria-hidden="true"` appears 100+ times across the theme. It hides content from screen readers that was designed to be screen-reader-only.

**Files to fix (global find-and-replace):**

Every `.liquid` file containing `class="visually-hidden" aria-hidden="true"` needs the `aria-hidden="true"` removed. Key files:

- `sections/header.liquid`
- `sections/footer.liquid`
- `sections/contact-form.liquid`
- `snippets/card-product.liquid`
- `snippets/header-drawer.liquid`
- `snippets/header-dropdown-menu.liquid`
- `snippets/price.liquid`
- `snippets/facets.liquid`
- And many others

**Find:**

```html
class="visually-hidden" aria-hidden="true"
```

**Replace with:**

```html
class="visually-hidden"
```

Run this across all `.liquid` files in the theme.

### 6B. CRITICAL — Fix nested `<h3>` in product cards

**File:** `snippets/card-product.liquid` (around lines 124-135)

```html
<!-- BEFORE -->
<h3 class="card__heading">
  <h3 class="full-unstyled-link">{{ card_product.title | escape }}</h3>
</h3>

<!-- AFTER -->
<h3 class="card__heading">
  <span class="full-unstyled-link"> {{ card_product.title | escape }} </span>
</h3>
```

### 6C. CRITICAL — Fix `aria-labelledby` on product card links

**File:** `snippets/card-product.liquid` (around line 43)

```html
<!-- BEFORE -->
<a aria-labelledby="{{ card_product.title | escape }}"

<!-- AFTER — use an element ID, not text -->
<a aria-labelledby="CardLink-{{ card_product.id }}-{{ section_id }}"
```

Ensure the referenced ID exists on the product title element.

### 6D. CRITICAL — Add alt text to recently viewed product images

**File:** `sections/footer.liquid` (around lines 141-142)

```javascript
// BEFORE
<img src='${item.productImg}' loading="lazy" width="1200"/>
<img src='${item.productImgTwo}' loading="lazy" width="1200"/>

// AFTER
<img src='${item.productImg}' alt='${item.productTitle}' loading="lazy" width="1200"/>
<img src='${item.productImgTwo}' alt='${item.productTitle}' loading="lazy" width="1200"/>
```

### 6E. MAJOR — Fix duplicate IDs in header

**File:** `sections/header.liquid`

The two header instances (`masonHeaderModifierOne` and `masonHeaderModifierTwo`) generate duplicate `id` attributes. Add a suffix to the second header's IDs:

```liquid
<!-- In the second header block (masonHeaderModifierTwo), suffix all IDs -->
<!-- Example: change id="cart-icon-bubble" to id="cart-icon-bubble-secondary" -->
```

### 6F. MAJOR — Fix `<a>` inside `<summary>` in dropdown menu

**File:** `snippets/header-dropdown-menu.liquid` (around lines 15-36)

```html
<!-- BEFORE -->
<summary id="HeaderMenu-{{ link.handle }}-header-dropdown-menu">
  <a
    id="HeaderMenu-{{ link.handle }}-header-dropdown-menu"
    href="{{ link.url }}"
  >
    {{ link.title | escape }}
  </a>
</summary>

<!-- AFTER — remove the <a>, make summary handle both click and navigation -->
<summary
  id="HeaderMenu-{{ link.handle }}-header-dropdown-menu"
  data-href="{{ link.url }}"
>
  <span class="header__menu-item-title">{{ link.title | escape }}</span>
</summary>
```

Then handle the link navigation via JavaScript (the hover-open behavior already exists in header.liquid).

### 6G. MAJOR — Fix invalid `<div>` inside `<ul>` in dropdown menu

**File:** `snippets/header-dropdown-menu.liquid` (around line 43)

```html
<!-- BEFORE -->
<ul role="list">
  <div class="hazelMegaMenuLinkList">
    <li>...</li>
  </div>
</ul>

<!-- AFTER — move the wrapper div outside the ul, or change to a valid child -->
<div class="hazelMegaMenuLinkList">
  <ul role="list">
    <li>...</li>
  </ul>
</div>
```

### 6H. MAJOR — Add labels to color swatch dots

**File:** `snippets/card-product.liquid` (around lines 263-269)

```html
<!-- BEFORE -->
<div
  style="height: 14px; width: 14px; border-radius:100px; background-color:..."
>
  &nbsp;
</div>

<!-- AFTER — add aria-label and role -->
<div
  style="height: 14px; width: 14px; border-radius:100px; background-color:..."
  role="img"
  aria-label="{{ value | split: ' ' | last }} color swatch"
></div>
```

### 6I. MINOR — Add `aria-label` to distinguish header landmarks

**File:** `sections/header.liquid`

```html
<!-- First header -->
<header aria-label="Primary navigation" class="... masonHeaderModifierOne ...">
  <!-- Second header -->
  <header
    aria-label="Secondary navigation"
    class="... masonHeaderModifierTwo ..."
  ></header>
</header>
```

### 6J. MINOR — Add `aria-hidden="true"` to decorative cursor follower

**File:** `layout/theme.liquid` (around line 421)

```html
<!-- BEFORE -->
<div id="follower"></div>

<!-- AFTER -->
<div id="follower" aria-hidden="true"></div>
```

---

## Task 7: Miscellaneous Fixes

### 7A. Fix CSS typo in header

**File:** `sections/header.liquid` (line 41)

```css
/* BEFORE */
900spx

/* AFTER */
900px
```

### 7B. Fix the `<span href>` in product card

**File:** `snippets/card-product.liquid` (around lines 193-200)

```html
<!-- BEFORE -->
<span
  href="{{ card_product.url }}"
  id="CardLink-..."
  class="full-unstyled-link"
>
  <!-- AFTER — change to <a> since it has an href -->
  <a
    href="{{ card_product.url }}"
    id="CardLink-{{ card_product.id }}-{{ section_id }}"
    class="full-unstyled-link"
  >
    {{ card_product.title | escape }}
  </a></span
>
```

### 7C. Clean up console.log statements

**File:** `sections/footer.liquid` — Remove `console.log` calls from the recently viewed products JavaScript.

**File:** `snippets/cart-drawer.liquid` — Remove `console.log` calls from the upsell JavaScript.

### 7D. Remove `nutTestTest` debug class

**File:** `snippets/header-dropdown-menu-helper.liquid`

```html
<!-- BEFORE -->
<nav class="nutTestTest ...">
  <!-- AFTER -->
  <nav class="header-dropdown-menu-helper ..."></nav>
</nav>
```

---

## Implementation Order

Recommended sequence, grouped by risk and dependency:

### Phase 1 — Low risk, high impact (do first)

1. Enable default `page.json` template (Task 1A)
2. Enable contact form on contact page (Task 2B)
3. Fix CSS typo (Task 7A)
4. Remove `aria-hidden` from `visually-hidden` elements (Task 6A)
5. Fix nested h3 in product cards (Task 6B)
6. Clean up console.logs (Task 7C)
7. Remove debug class (Task 7D)

### Phase 2 — Medium complexity

1. Fix Instagram label (Task 5)
2. Fix `aria-labelledby` and `<span href>` in product cards (Tasks 6C, 7B)
3. Add alt text to recently viewed images (Task 6D)
4. Fix duplicate header IDs (Task 6E)
5. Add accessibility labels to swatches and landmarks (Tasks 6H, 6I, 6J)

### Phase 3 — New features

1. Create returns form section and template (Tasks 3A, 3B)
2. Add returns link to mobile drawer (Task 3D)

### Phase 4 — Shopify Admin tasks (no code, done in browser)

These are all done in the Shopify Admin dashboard at `hazelboutique.myshopify.com/admin`. No code editor needed.

**Pages:**

1. Verify page handles and templates for Our Story, Store Locations, Contact Us, Sizing Guide (Task 1B)
2. Update the Contact Us page body with new address, email, phone, hours (Task 2A)
3. Update the Store Locations page body with new address (Task 2C)
4. Check all other pages for stale address references (Task 2D)
5. Create the Returns page, assign the `page.returns` template (Task 3C)

**Collections:**

6. Create "Mock Necks" automated collection with `mock neck` tag condition (Task 4A)
7. Tag all mock neck products with `mock neck` (Task 4A)
8. Create "Perfume" automated collection with `perfume` tag condition (Task 4B)
9. Tag the two perfume products with `perfume` (Task 4B)
10. Add Mini Cherub to the Bottoms collection (Task 4C)

**Navigation:**

11. Edit `navbar-menu`: add Mock Necks under Clothing, Perfume under Accessories (Task 4D)
12. Edit `navbar-menu`: add pages (Our Story, Store Locations, Contact Us, Sizing Guide, Returns) if not already present (Task 1C)
13. Edit `footer-quick-links`: add Returns link (Task 3D)
14. Verify all footer menus have the right links (Task 1C)

**Store settings:**

15. Update store address in **Settings > Store details** to the new address (Task 2D)

### Phase 5 — Structural HTML fixes (test carefully)

1. Fix `<a>` inside `<summary>` in mega menu (Task 6F)
2. Fix `<div>` inside `<ul>` in mega menu (Task 6G)

---

## Files Changed Summary

| File                                             | Tasks              | Type                     |
| ------------------------------------------------ | ------------------ | ------------------------ |
| `templates/page.json`                            | 1A                 | Edit (remove disabled)   |
| `templates/page.contact.json`                    | 2B                 | Edit (enable form)       |
| `templates/page.returns.json`                    | 3A                 | **New file**             |
| `sections/returns-form.liquid`                   | 3B                 | **New file**             |
| `sections/header.liquid`                         | 6E, 6I, 7A         | Edit                     |
| `sections/footer.liquid`                         | 6D, 7C             | Edit                     |
| `sections/contact-form.liquid`                   | 6A                 | Edit                     |
| `snippets/card-product.liquid`                   | 6A, 6B, 6C, 6H, 7B | Edit                     |
| `snippets/header-drawer.liquid`                  | 3D, 6A             | Edit                     |
| `snippets/header-dropdown-menu.liquid`           | 6A, 6F, 6G         | Edit                     |
| `snippets/header-dropdown-menu-helper.liquid`    | 7D                 | Edit                     |
| `snippets/cart-drawer.liquid`                    | 7C                 | Edit                     |
| `snippets/price.liquid`                          | 6A                 | Edit                     |
| `snippets/facets.liquid`                         | 6A                 | Edit                     |
| `layout/theme.liquid`                            | 6J                 | Edit                     |
| `templates/index.json`                           | 5                  | Edit (if needed)         |
| All other `.liquid` files with `visually-hidden` | 6A                 | Edit (bulk find-replace) |

---

## Todo List

### Phase 1 — Low risk, high impact

Code changes — simple edits, safe to do first.

- [x] **1.1** Enable default page template — remove `"disabled": true` from `templates/page.json` (Task 1A)
- [x] **1.2** Enable contact form — remove `"disabled": true` from `templates/page.contact.json`, set heading to "Send Us a Message" (Task 2B)
- [x] **1.3** Fix CSS typo — change `900spx` to `900px` in `sections/header.liquid` line 41 (Task 7A)
- [x] **1.4** Remove `aria-hidden="true"` from all `visually-hidden` elements — bulk find-and-replace `class="visually-hidden" aria-hidden="true"` with `class="visually-hidden"` across all `.liquid` files (Task 6A)
- [x] **1.5** Fix nested `<h3>` — change inner `<h3>` to `<span>` in `snippets/card-product.liquid` around line 124 (Task 6B)
- [x] **1.6** Remove `console.log` statements from `sections/footer.liquid` recently-viewed JS (Task 7C)
- [x] **1.7** Remove `console.log` statements from `snippets/cart-drawer.liquid` upsell JS (Task 7C)
- [x] **1.8** Rename `nutTestTest` class to `header-dropdown-menu-helper` in `snippets/header-dropdown-menu-helper.liquid` (Task 7D)

### Phase 2 — Medium complexity

Code changes — require more care, affect visible UI.

- [x] **2.1** Fix Instagram heading and link in `templates/index.json` rich text section `rich_text_niFCNN` — or fix via theme editor (Task 5)
- [x] **2.2** Fix `aria-labelledby` on product card — change from text value to element ID in `snippets/card-product.liquid` line 43 (Task 6C)
- [x] **2.3** Fix `<span href>` — change to `<a href>` in `snippets/card-product.liquid` around line 193 (Task 7B)
- [x] **2.4** Add `alt` attribute to recently-viewed product images in `sections/footer.liquid` JS template literals (Task 6D)
- [x] **2.5** Fix duplicate IDs in second header — suffix all IDs in `masonHeaderModifierTwo` block of `sections/header.liquid` (Task 6E)
- [x] **2.6** Add `role="img"` and `aria-label` to color swatch dots in `snippets/card-product.liquid` around line 263 (Task 6H)
- [x] **2.7** Add `aria-label="Primary navigation"` to first `<header>` and `aria-label="Secondary navigation"` to second `<header>` in `sections/header.liquid` (Task 6I)
- [x] **2.8** Add `aria-hidden="true"` to `#follower` div in `layout/theme.liquid` line 421 (Task 6J)

### Phase 3 — New features

New files and code additions.

- [ ] **3.1** Create `templates/page.returns.json` with `main-page` and `returns-form` sections (Task 3A)
- [ ] **3.2** Create `sections/returns-form.liquid` with the return request form, return slip generator, and print styles (Task 3B)
- [ ] **3.3** Add "Returns" link to mobile drawer in `snippets/header-drawer.liquid` after the Sizing Guide link (Task 3D)

### Phase 4 — Shopify Admin tasks (manual, in browser)

All done at `hazelboutique.myshopify.com/admin`. No code editor needed.

**Pages:**

- [x] **4.1** Go to **Online Store > Pages**, open "Our Story" — confirm handle is `our-story`, template is `page.about`. Save **Confirmed `https://hazelboutique.com/pages/our-story`**
- [x] **4.2** Open "Store Locations" — confirm handle is `store-locations`, template is `page`. Update body with new address (1709 Rt 34, Suite 3, Farmingdale, NJ 07719). Save
**Confirmed `https://hazelboutique.com/pages/store-locations`, actual store locations havent changed, jsut the shipping warehouse**
- [x] **4.3** Open "Contact Us" — confirm handle is `contact-us`, template is `page.contact`. Replace body with consolidated contact info: new address, email, phone, hours. Save **Confirmed `https://hazelboutique.com/pages/contact-us`** Can you walk me through more what Jenna/Hazel girls want to see on this page
- [ ] **4.4** Open "Sizing Guide" (or "Sizing") — confirm handle is `sizing`, template is `page.contact`. Save
- [ ] **4.5** Create any of the above pages if they don't exist yet (Add Page, set title, handle, template, body content)
- [ ] **4.6** Create new "Returns" page — title: "Returns", handle: `returns`, template: `page.returns`, paste returns policy text into body. Save and publish
- [ ] **4.7** Open every other page in the Pages list — search each body for old address text. Remove or update any stale references

**Collections:**

- [ ] **4.8** Go to **Products > Collections > Create collection** — title: "Mock Necks", type: Automated, condition: Product tag is equal to `mock neck`. Save
- [ ] **4.9** Go to **Products > All products** — find each mock neck product, add tag `mock neck`, save each one
- [ ] **4.10** Go to **Products > Collections > Create collection** — title: "Perfume", type: Automated, condition: Product tag is equal to `perfume`. Save
- [ ] **4.11** Find the two perfume products, add tag `perfume`, save each one
- [ ] **4.12** Find the "Bottoms" collection, check whether it's automated (note the tag) or manual
- [ ] **4.13** Find the "Mini Cherub" product — if Bottoms is automated, add the matching tag; if manual, add Mini Cherub to the Bottoms collection directly. Save
- [ ] **4.14** Optionally upload collection images for Mock Necks and Perfume

**Navigation:**

- [ ] **4.15** Go to **Online Store > Navigation**, open `navbar-menu`
- [ ] **4.16** Expand "Clothing" submenu — add "Mock Necks" linked to the Mock Necks collection. Drag to desired position. Save
- [ ] **4.17** Expand "Accessories" submenu — add "Perfume" linked to the Perfume collection. Save
- [ ] **4.18** Check if Our Story, Store Locations, Contact Us, Sizing Guide, Returns are in the main menu. Add any that are missing
- [ ] **4.19** Save `navbar-menu`
- [ ] **4.20** Open `footer-quick-links` — add "Returns" linked to the Returns page. Save
- [ ] **4.21** Review all four footer menus (`footer-quick-links`, `footer-socials`, `footer-categories-1`, `footer-categories-2`) — confirm links are correct and none point to dead pages. Save any changes

**Store settings:**

- [ ] **4.22** Go to **Settings > Store details** — update the store address to 1709 Rt 34, Suite 3, Farmingdale, NJ 07719. Save

**Verification:**

- [ ] **4.23** Visit the live site — click every link in the header nav and confirm each page loads (not blank, not 404)
- [ ] **4.24** Open the mobile menu (hamburger) — click each link in the utility section and confirm pages load
- [ ] **4.25** Visit `/pages/returns` — confirm the returns form renders and the "Generate Return Slip" button works
- [ ] **4.26** Hover over "Clothing" in the desktop nav — confirm "Mock Necks" appears
- [ ] **4.27** Hover over "Accessories" in the desktop nav — confirm "Perfume" appears
- [ ] **4.28** Visit the Bottoms collection — confirm Mini Cherub appears in the product grid
- [ ] **4.29** Check the footer — confirm all four link columns render correct links including Returns

### Phase 5 — Structural HTML fixes (test carefully)

These change interactive navigation behavior. Test thoroughly on desktop and mobile after each change.

- [ ] **5.1** Remove `<a>` from inside `<summary>` in `snippets/header-dropdown-menu.liquid` — replace with `<span>`, add `data-href` attribute to `<summary>`, handle navigation via JS (Task 6F)
- [ ] **5.2** Move `<div class="hazelMegaMenuLinkList">` outside the `<ul>` in `snippets/header-dropdown-menu.liquid` — wrap `<ul>` inside the `<div>` instead (Task 6G)
- [ ] **5.3** Test desktop nav: hover over each menu item, confirm dropdowns open, confirm clicking a parent item navigates to its page
- [ ] **5.4** Test mobile nav: open drawer, navigate through all menu levels, confirm back buttons work
- [ ] **5.5** Test keyboard nav: Tab through the header menu items, confirm Enter opens dropdowns, Escape closes them
