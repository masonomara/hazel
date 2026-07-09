# Shopify × Mailchimp "Alerts" Signup — Persistent Header + Footer

A complete, buildable guide for adding a header trigger that swaps the announcement‑bar
message and opens a popup where a visitor can sign up for alerts by email, phone, or both,
with the identical form mirrored in the persistent footer.

The first half explains how the two platforms actually fit together (so the code makes sense
and stays compliant). The second half is the build. Part 7 is the handoff plan that splits the
work between you (Shopify/Mailchimp admin dashboards) and the theme‑coding agent.

> How to read this document. It is written for a coding agent that works exclusively inside the
> Shopify theme codebase and already understands this theme's structure and visual style. The code
> below is functional scaffolding, not final design. Every snippet carries the behavior, the
> Mailchimp wiring, the accessibility hooks, and the anti‑bot pieces — but the visual styling is left
> deliberately open‑ended. The agent is expected to inspect the theme's own design system and
> components and make the popup, bar, and footer form look native to the store. Wherever you see an
> `AGENT:` note, that is a decision the agent owns. Do not copy the placeholder CSS as‑is.

> Placeholders you'll replace: `us21` (your data‑center), `abc123…` (your account `u` value),
> `1a2b3c4d5e` (your Audience/List ID). All three come from Mailchimp — see "Getting your Mailchimp
> identifiers." The agent receives these from you via the handoff packet in Part 7.

---

## Part 1 — How Mailchimp + Shopify work (the parts that matter here)

### 1.1 The native integration

Mailchimp and Shopify were disconnected from 2019 to 2024 and now have a fully restored,
native integration, installed from the Shopify App Store as *"Mailchimp Email & SMS Marketing"*
(published by Intuit Mailchimp). Once connected it:

- Syncs customers, orders, and products into a single Mailchimp audience you pick during setup.
- Pushes updates in near real time (all fields except discount codes, which sync every few hours).
- Installs the Mailchimp Site Tracking Pixel automatically, feeding on‑site events back for automations.
- Syncs most fields bi‑directionally, with one important exception below.

Key mental model: the integration keeps a Mailchimp *audience* in step with your Shopify
*customer list*. Anyone who lands in either system with marketing consent shows up in the other.
Your popup's job is simply to *create a subscribed contact in that audience* — after which
Mailchimp's normal automations (welcome, abandoned cart, back‑in‑stock, etc.) take over.

### 1.2 How email signup works

- A contact needs an email address and a subscription status. The two you'll use are:
  - `subscribed` — added immediately (single opt‑in).
  - `pending` — Mailchimp emails a confirmation link; they become `subscribed` only after clicking
    (double opt‑in). Whether new signups are single or double opt‑in is an audience‑level setting
    in Mailchimp, not something the form dictates.
- Extra data rides along as merge fields — `EMAIL`, `FNAME`, `LNAME`, `PHONE`, and any custom
  fields, each identified by an uppercase merge tag.
- To fight bots, Mailchimp forms include a honeypot field and support reCAPTCHA (enabled in
  the audience's form settings). Bot signups are a real, recurring pain point that inflates your
  contact count (and bill), so keep the honeypot in and turn reCAPTCHA on.

### 1.3 How SMS/text signup works — read this before you build the phone field

SMS is not just "collect a phone number." It is a separate, regulated marketing channel with
its own consent, and Mailchimp enforces that:

- SMS is a paid add‑on, available on the Essentials plan or higher, and you must submit an
  application and be approved before you can collect SMS opt‑ins or send texts. `MMS` (image/GIF)
  is US/Canada only.
- You buy SMS credits to send, and there are quiet hours, rate limits/throttling, and for
  US sending you register a 10DLC number (or, on Standard+, a short code).
- Geographic limit: you can only text subscribers in the same country as your registered
  sending number.
- Consent is explicit, separate, and recorded. SMS consent is *not* covered by email consent —
  it must be its own, verifiable opt‑in (TCPA in the US). When you use Mailchimp's own SMS field,
  it records the consent timestamp for you and attaches a mandatory legal checkbox that you cannot
  edit or remove.
- Sync direction: SMS subscribers sync Shopify → Mailchimp only (not back), and only once you
  have an approved SMS program.

### 1.4 The trap: `PHONE` merge field ≠ SMS subscription

Mailchimp has two different phone concepts, and confusing them is the most common mistake:

| | `PHONE` merge field | SMS phone number field |
|---|---|---|
| What it is | A data field that just stores a number | An actual opt‑in to marketing texts |
| Requires SMS program? | No | Yes (application + approval) |
| Sends texts? | No | Yes |
| Consent checkbox | Not required | Required, non‑editable |

If you only put a `PHONE` merge field in your form, you have collected a number but no one is
subscribed to SMS — you can't legally text them. To actually enroll SMS subscribers you must use
the real SMS field / SMS subscription status and capture explicit consent.

### 1.5 Three ways to wire a custom form to Mailchimp

| Method | Backend? | Email | SMS opt‑in | Notes |
|---|---|---|---|---|
| A. JSONP to the classic `post-json` endpoint | None | ✅ Great | ⚠️ Not reliable/compliant for true SMS opt‑in | Fastest; keys never involved; email‑only quick start |
| B. Mailchimp‑generated embed markup dropped into your popup | None | ✅ | ✅ (carries the required consent checkbox) | You reuse Mailchimp's exact field + checkbox markup |
| C. Marketing API behind a small server/App Proxy | Yes | ✅ | ✅ (SMS field is supported by the API) | Most control, best error handling, keeps API key server‑side |

Recommendation for this project (email OR phone OR both):

- Email → Method A (JSONP) if you want zero backend, or Method C for robustness.
- Phone/SMS → Method B or C. Never expose a Mailchimp API key in Shopify theme/browser code —
  that's why true SMS goes through generated embed markup (B) or a server (C).

The build below gives you Method A for email + Method C for the server path, and shows exactly
where to paste Method B's generated SMS block if you'd rather not run a server.

---

## Part 2 — Prerequisites checklist

1. Shopify: access to *Online Store → Themes → Edit code* on your live (or a duplicated) theme.
   Duplicate the theme first and build on the copy.
2. Mailchimp: the account and the audience you want signups to land in.
3. If you want real SMS: an Essentials+ plan, a submitted & approved SMS Marketing program,
   and SMS credits. Without approval, ship email now and add the phone field later.
4. Decide single vs double opt‑in in the audience settings, and turn on reCAPTCHA for the form.
5. Getting your Mailchimp identifiers (used by Methods A/B):
   - In Mailchimp: Audience → Signup forms → Embedded forms. Generate any embedded form.
   - In the generated code, the form `action` looks like
     `https://xxxx.us21.list-manage.com/subscribe/post?u=abc123def456…&id=1a2b3c4d5e`.
     - `us21` = data center (also the tail of your API key, `…-us21`).
     - `u=` value = your account id.
     - `id=` value = your audience/list id.
     - The honeypot field name is `b_<u>_<id>` — copy it verbatim from the generated code.

---

## Part 3 — Build the UI (structure is portable; styling is the agent's job)

The plan: one snippet holds the modal, the shared form, and all CSS/JS; it's rendered once in
`theme.liquid`. A tiny section renders the announcement bar with a trigger button. The footer
reuses the same form markup. Clicking the trigger swaps the bar's message and opens the modal.

### 3.0 Agent styling brief (read before touching the snippets)

The behavior, wiring, and accessibility hooks below are fixed. The look is yours to define — the
goal is that a shopper can't tell this feature wasn't shipped with the theme. Before writing any CSS:

1. Learn the theme's design system. Inspect `config/settings_schema.json` and
   `config/settings_data.json` for color schemes, fonts, and global settings; inspect the base
   stylesheet(s) in `assets/` for CSS custom properties (colors, `--page-width`, spacing, radii,
   shadows, focus rings) and the button/field/typography classes. Reuse these tokens rather than
   inventing values.
2. Reuse existing components, don't reinvent them.
   - If the theme ships a modal/drawer/popup primitive (e.g. a custom element like
     `<modal-dialog>` / `details-modal`, or a drawer used by cart/search/quick‑add), strongly prefer
     wrapping the form in that primitive and deleting the placeholder modal markup/JS — as long as you
     preserve the `data-alerts-open`, `data-close`, `data-form-slot`, and the `alerts:open` /
     `alerts:close` events the bar listens for. Reusing the theme's dialog gets you its focus trap,
     scroll‑lock, transitions, and z‑index handling for free.
   - Style the form with the theme's button and input/field classes; style the announcement
     bar with the theme's announcement/utility bar styles and color‑scheme mechanism.
3. Match, don't clash. Typography scale, spacing rhythm, corner radius, motion (respect
   `prefers-reduced-motion`), focus visibility, and dark/light color schemes should all follow the
   theme. The `alerts-*` class names are placeholders — rename or map them to the theme's own classes
   freely, provided the JS hooks (`data-*` attributes and the `is-error` / `is-success` state classes)
   keep working.
4. Follow the theme's JS conventions. If the theme defers scripts, bundles assets, or uses web
   components / a specific event pattern, adapt the inline `<script>` blocks to that convention (e.g.
   move JS into an `assets/*.js` file loaded the way the theme loads others). Keep the logic identical.
5. Responsive + a11y are part of "done." Mobile layout, tap targets, labels, `aria-*`, keyboard
   (Esc to close, focus return) must all match the quality bar of the rest of the theme.

Everywhere an `AGENT:` comment appears in the code, it marks a spot you own. Treat the provided CSS as
scaffolding to be replaced, not a design to preserve.

### 3.1 The shared snippet — `snippets/alerts-signup.liquid`

Create `snippets/alerts-signup.liquid` and paste this. It contains: the modal, the reusable form
(used by both modal and footer), styles, and the JavaScript.

```liquid
{%- comment -%} snippets/alerts-signup.liquid {%- endcomment -%}
{%- comment -%}
  Reusable "Sign up for alerts" form used by the header popup AND the footer.
  Set your Mailchimp identifiers in the data-* attributes on the wrapper below.
{%- endcomment -%}

<template id="alerts-form-template">
  <form class="alerts-form" novalidate>
    <p class="alerts-form__intro">Get alerts by email, text, or both.</p>

    <label class="alerts-field">
      <span>Email</span>
      <input type="email" name="EMAIL" autocomplete="email" placeholder="you@example.com">
    </label>

    <label class="alerts-field">
      <span>Mobile number</span>
      <input type="tel" name="PHONE" autocomplete="tel" placeholder="+1 555 555 5555">
    </label>

    <label class="alerts-consent" data-consent="sms" hidden>
      <input type="checkbox" name="SMS_CONSENT">
      <span>
        I agree to receive recurring automated marketing text messages at the number provided.
        Consent is not a condition of purchase. Msg &amp; data rates may apply. Reply STOP to opt out.
      </span>
    </label>

    <!-- Honeypot: real users never see or fill this. Name MUST be your b_<u>_<id> value. -->
    <div aria-hidden="true" style="position:absolute;left:-5000px;">
      <input type="text" name="b_abc123def456_1a2b3c4d5e" tabindex="-1" value="">
    </div>

    <button type="submit" class="alerts-form__submit">Notify me</button>
    <p class="alerts-form__msg" role="status" aria-live="polite"></p>
  </form>
</template>

<!-- The modal -->
<div id="alerts-modal" class="alerts-modal" hidden aria-hidden="true" role="dialog"
     aria-modal="true" aria-labelledby="alerts-modal-title">
  <div class="alerts-modal__backdrop" data-close></div>
  <div class="alerts-modal__panel" role="document">
    <button class="alerts-modal__close" data-close aria-label="Close">&times;</button>
    <h2 id="alerts-modal-title" class="alerts-modal__title">Sign up for alerts</h2>
    <div class="alerts-modal__body" data-form-slot></div>
  </div>
</div>

<style>
  /* ==========================================================================
     STRUCTURAL / MECHANICAL CSS ONLY — this is NOT the final design.

     AGENT: Own all presentation. Replace and extend everything here with the
     theme's design system: color schemes/CSS custom properties, spacing scale,
     typography, radii, shadows, focus rings, and the theme's existing form,
     field, button, and (if present) modal/drawer components. Prefer reusing the
     theme's own component classes over these `alerts-*` placeholders — you may
     rename/replace class names as long as you keep the data-* hooks and the
     JS-set state classes (`is-error`, `is-success`) working.

     KEEP the mechanics below (they make the modal function and hide the
     honeypot); restyle everything else. Notes inline mark what must stay.
     ========================================================================== */

  /* --- must stay: overlay mechanics --- */
  .alerts-modal[hidden]{display:none;}                       /* keep: hidden state */
  .alerts-modal{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
    z-index:1000;}                                           /* AGENT: z-index must sit above the theme header/announcement bar */
  .alerts-modal__backdrop{position:absolute;inset:0;}        /* AGENT: give this a scrim (e.g. semi-transparent fill) so the modal reads */
  .alerts-modal__panel{position:relative;box-sizing:border-box;width:100%;max-width:420px;}
                                                             /* AGENT: max-width/padding/surface styling are yours to set */
  .alerts-modal__close{position:absolute;cursor:pointer;}    /* AGENT: place & style the close affordance per theme */

  /* --- layout skeleton: restyle freely --- */
  .alerts-form{display:grid;}                                /* AGENT: gap, width, rhythm */
  .alerts-field{display:grid;}                               /* AGENT: label + input styling */
  .alerts-consent{display:grid;grid-template-columns:auto 1fr;align-items:start;}
                                                             /* keep the 2-col checkbox+text layout; style the rest */
  /* .alerts-form__submit / .alerts-form__msg / .alerts-form__intro / .alerts-footer:
     AGENT to style. `.alerts-form__msg.is-error` and `.is-success` are set by JS —
     give them clear error/success treatment consistent with the theme. */
</style>

<script>
(function () {
  // ---- CONFIG: replace with your Mailchimp identifiers ------------------------
  var MC = {
    dc:       'us21',            // data center
    u:        'abc123def456',    // account id (the ?u= value)
    listId:   '1a2b3c4d5e',      // audience id (the &id= value)
    // If you run the server path (Method C), set this to your endpoint and it takes over:
    proxyUrl: ''                 // e.g. '/apps/alerts' (App Proxy) or 'https://your-fn.example.com/subscribe'
  };
  // ----------------------------------------------------------------------------

  var template = document.getElementById('alerts-form-template');
  var modal    = document.getElementById('alerts-modal');
  var lastFocus = null;

  // Build a form instance from the template and wire it up.
  function mountForm(slot) {
    var node = template.content.firstElementChild.cloneNode(true);
    slot.appendChild(node);
    wire(node);
    return node;
  }

  function wire(form) {
    var phone   = form.querySelector('[name="PHONE"]');
    var email   = form.querySelector('[name="EMAIL"]');
    var consent = form.querySelector('[data-consent="sms"]');

    // Reveal the SMS consent checkbox only when a phone number is being entered.
    phone.addEventListener('input', function () {
      consent.hidden = phone.value.trim() === '';
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submit(form, { email: email, phone: phone, consent: consent });
    });
  }

  function setMsg(form, text, kind) {
    var el = form.querySelector('.alerts-form__msg');
    el.textContent = text;
    el.className = 'alerts-form__msg' + (kind ? ' is-' + kind : '');
  }

  function submit(form, f) {
    var emailVal = f.email.value.trim();
    var phoneVal = f.phone.value.trim();

    if (!emailVal && !phoneVal) {
      return setMsg(form, 'Enter an email, a phone number, or both.', 'error');
    }
    if (phoneVal && !f.consent.querySelector('input').checked) {
      return setMsg(form, 'Please agree to receive text messages to continue.', 'error');
    }

    var btn = form.querySelector('.alerts-form__submit');
    btn.disabled = true;
    setMsg(form, 'Submitting…');

    // Method C: server/App Proxy (handles email + real SMS opt-in). Preferred if configured.
    if (MC.proxyUrl) {
      fetch(MC.proxyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: emailVal,
          phone: phoneVal,
          sms_consent: f.consent.querySelector('input').checked,
          fname: '', lname: ''
        })
      })
      .then(function (r) { return r.json(); })
      .then(function (data) { done(form, btn, data.ok, data.message); })
      .catch(function () { done(form, btn, false, 'Something went wrong. Please try again.'); });
      return;
    }

    // Method A: no-backend email via JSONP. (SMS via this path is not compliant — use Method C
    // or paste Mailchimp's generated SMS block; see the guide.)
    if (!emailVal) {
      done(form, btn, false, 'To subscribe by text, ask your developer to enable the server path.');
      return;
    }
    var base = 'https://' + MC.dc + '.list-manage.com/subscribe/post-json'
             + '?u=' + encodeURIComponent(MC.u)
             + '&id=' + encodeURIComponent(MC.listId)
             + '&EMAIL=' + encodeURIComponent(emailVal)
             + (phoneVal ? '&PHONE=' + encodeURIComponent(phoneVal) : '');
    jsonp(base, 'c').then(function (data) {
      done(form, btn, data.result === 'success', stripHtml(data.msg));
    }).catch(function () {
      done(form, btn, false, 'Network error. Please try again.');
    });
  }

  function done(form, btn, ok, message) {
    btn.disabled = false;
    setMsg(form, message || (ok ? 'You\'re on the list!' : 'Please try again.'),
           ok ? 'success' : 'error');
    if (ok) form.reset();
  }

  // Minimal JSONP helper (Mailchimp's post-json uses ?c=<callback>).
  function jsonp(url, cbParam) {
    return new Promise(function (resolve, reject) {
      var cb = 'mc_cb_' + Date.now() + Math.floor(Math.random() * 1e4);
      var s  = document.createElement('script');
      var to = setTimeout(function () { cleanup(); reject(); }, 10000);
      function cleanup() { clearTimeout(to); delete window[cb]; s.remove(); }
      window[cb] = function (data) { cleanup(); resolve(data); };
      s.onerror = function () { cleanup(); reject(); };
      s.src = url + '&' + cbParam + '=' + cb;
      document.body.appendChild(s);
    });
  }
  function stripHtml(str) { var d = document.createElement('div'); d.innerHTML = str || ''; return d.textContent; }

  // ---- Modal open/close + focus handling -------------------------------------
  function openModal() {
    var slot = modal.querySelector('[data-form-slot]');
    if (!slot.children.length) mountForm(slot);   // mount once, lazily
    lastFocus = document.activeElement;
    modal.hidden = false; modal.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('alerts-open');
    var first = modal.querySelector('input, button');
    if (first) first.focus();
    document.body.dispatchEvent(new CustomEvent('alerts:open'));
  }
  function closeModal() {
    modal.hidden = true; modal.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('alerts-open');
    if (lastFocus) lastFocus.focus();
    document.body.dispatchEvent(new CustomEvent('alerts:close'));
  }

  modal.addEventListener('click', function (e) {
    if (e.target.hasAttribute('data-close')) closeModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) closeModal();
  });

  // Any element with data-alerts-open triggers the popup (header button, etc.)
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-alerts-open]');
    if (trigger) { e.preventDefault(); openModal(); }
  });

  // Mount footer form(s) on load.
  document.querySelectorAll('[data-alerts-footer]').forEach(mountForm);

  // Expose for the announcement bar to hook message-swapping.
  window.AlertsSignup = { open: openModal, close: closeModal };
})();
</script>
```

### 3.2 Render the snippet site‑wide

In `layout/theme.liquid`, just before the closing `</body>` tag, add:

```liquid
{% render 'alerts-signup' %}
```

### 3.3 The header trigger + message swap — `sections/alerts-bar.liquid`

Create `sections/alerts-bar.liquid`. It renders a thin bar with your normal message and a button.
Clicking the button swaps the message and opens the modal; closing reverts.

> AGENT: This is a generic bar so the behavior is portable. If the theme already has an
> announcement/utility bar section you'd rather extend, you may instead add the trigger button +
> message‑swap `<script>` into that existing section (see the "keep the existing bar" note after the
> placement steps) and skip this file. Either way, match the theme's bar styling and color‑scheme
> pattern rather than hard‑coding colors — the settings below use a bare fallback only.

```liquid
{%- comment -%} sections/alerts-bar.liquid {%- endcomment -%}
<div class="alerts-bar" data-alerts-bar>
  {%- comment -%}
    AGENT: match the theme's announcement/utility bar. If the theme uses color_scheme settings,
    add a `color_scheme` setting to the schema and apply the theme's scheme class here instead of
    inline colors. Reuse the theme's bar wrapper/inner classes if they exist.
  {%- endcomment -%}
  <div class="alerts-bar__inner">
    <span class="alerts-bar__msg" data-default>{{ section.settings.message | escape }}</span>
    <span class="alerts-bar__msg" data-swapped hidden>{{ section.settings.swapped | escape }}</span>
    <button type="button" class="alerts-bar__btn" data-alerts-open>
      {{ section.settings.button_label | escape }}
    </button>
  </div>
</div>

<style>
  /* STRUCTURAL ONLY. AGENT: style .alerts-bar to look like the theme's announcement bar
     (height, background via color scheme, typography, responsive behavior). Style the
     button using the theme's button/link component. Keep the flex centering skeleton. */
  .alerts-bar__inner{display:flex;align-items:center;justify-content:center;gap:.5rem;}
  .alerts-bar__btn{cursor:pointer;}
</style>

<script>
  (function () {
    var bar = document.currentScript.closest('section') || document;
    var def = bar.querySelector('[data-default]');
    var swp = bar.querySelector('[data-swapped]');
    document.body.addEventListener('alerts:open',  function () { if(def&&swp){def.hidden=true; swp.hidden=false;} });
    document.body.addEventListener('alerts:close', function () { if(def&&swp){def.hidden=false; swp.hidden=true;} });
  })();
</script>

{% schema %}
{
  "name": "Alerts bar",
  "settings": [
    { "type": "text", "id": "message",      "label": "Default message", "default": "Free shipping over $50 🚚" },
    { "type": "text", "id": "swapped",      "label": "Message while popup is open", "default": "Choose how you'd like to hear from us 👇" },
    { "type": "text", "id": "button_label", "label": "Button label", "default": "Get alerts" }
    /* AGENT: add a "color_scheme" setting (and any padding/animation settings) to mirror how the
       theme's own announcement bar is configured, so merchants get a familiar editing experience. */
  ],
  "presets": [{ "name": "Alerts bar" }]
}
{% endschema %}
```

Placing the bar (pick one):

- Online Store 2.0 themes (Dawn and most modern themes): open the Theme editor, and in the
  Header group click Add section → Alerts bar, then drag it above the theme's own header.
  (You can also add it to `sections/header-group.json`.)
- Vintage themes: in `layout/theme.liquid`, add `{% section 'alerts-bar' %}` on the line above
  `{% section 'header' %}`.

> Prefer to keep your theme's existing announcement bar? Instead of a new section, add a Custom
> Liquid block (theme editor) inside the existing announcement bar containing just the
> `<button data-alerts-open>…</button>` and the small swap `<script>`. The button opens the same modal.

### 3.4 The footer form

In `sections/footer.liquid` (or a Custom Liquid block in the footer via the theme editor), drop
a mount point where you want the form:

```liquid
<div class="alerts-footer" data-alerts-footer aria-label="Sign up for alerts"></div>
```

The snippet's JS finds every `[data-alerts-footer]` on load and injects the same form, so the footer
and popup stay identical with zero duplication.

---

## Part 4 — Wiring to Mailchimp

### 4.1 Method A — Email via JSONP (no backend)

Already wired in `alerts-signup.liquid`. Set `MC.dc`, `MC.u`, `MC.listId`, keep `MC.proxyUrl` empty,
and email signups post straight to Mailchimp's `subscribe/post-json` endpoint. Success/error text
comes back in `data.result` / `data.msg`. This is email‑only; the phone path will tell users to use
the server route.

### 4.2 Method B — Compliant SMS with zero backend (generated markup)

Once your SMS program is approved, in Mailchimp generate an Embedded form with the SMS phone
number field enabled. Mailchimp outputs the phone input plus a required, non‑editable legal
consent checkbox. Copy that exact block (input + checkbox + its field `name`s) and replace the
`PHONE` field and the `alerts-consent` label in the template with Mailchimp's generated markup. Point
the form `action` at that generated form. Because the markup is Mailchimp's own, consent is recorded
correctly and the number is enrolled as a subscribed SMS contact.

### 4.3 Method C — Server path via the Marketing API (recommended for SMS + robust email)

Set `MC.proxyUrl` to your endpoint and the client posts JSON to it; the server adds the contact with
the Marketing API, which supports both email and the SMS phone number field. The API key
lives only on the server — never in theme code.

Two ways to host the endpoint:

- Shopify App Proxy — expose it at `/apps/alerts` on your own domain (same‑origin, no CORS). Requires
  a custom Shopify app.
- Serverless function (Cloudflare Worker, Vercel, Netlify, etc.) — simplest; just enable CORS for
  your store domain.

Example Node/serverless handler (email + `PHONE` merge field, single‑ or double‑opt‑in via
`status_if_new`):

```js
// POST { email, phone, sms_consent, fname, lname }
import crypto from 'node:crypto';

const DC      = 'us21';                       // data center
const LIST_ID = '1a2b3c4d5e';                 // audience id
const API_KEY = process.env.MAILCHIMP_API_KEY; // e.g. "xxxx…-us21"  (server env only!)

export default async function handler(req, res) {
  // CORS (skip if using App Proxy / same origin)
  res.setHeader('Access-Control-Allow-Origin', 'https://your-store.myshopify.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const { email = '', phone = '', sms_consent = false, fname = '', lname = '' } = req.body || {};
  if (!email && !phone) return res.status(400).json({ ok: false, message: 'Provide an email or phone.' });
  if (phone && !sms_consent) return res.status(400).json({ ok: false, message: 'SMS consent required.' });

  // Mailchimp keys contacts by md5(lowercased email). If email-less (SMS-only), you must have an
  // approved SMS program and use the SMS-contact flow — verify field names in the live API reference.
  const base = `https://${DC}.api.mailchimp.com/3.0/lists/${LIST_ID}/members`;
  const auth = 'Basic ' + Buffer.from('any:' + API_KEY).toString('base64');

  const merge_fields = {};
  if (fname) merge_fields.FNAME = fname;
  if (lname) merge_fields.LNAME = lname;
  if (phone) merge_fields.PHONE = phone;   // stores the number as data

  try {
    if (email) {
      const hash = crypto.createHash('md5').update(email.toLowerCase()).digest('hex');
      const body = {
        email_address: email,
        status_if_new: 'pending',   // 'pending' = double opt-in; 'subscribed' = single opt-in
        merge_fields
        // For true SMS enrollment, also set the SMS subscription status / SMS phone number here.
        // These fields ARE supported by the Marketing API — confirm exact keys against the current
        // Members endpoint schema for your account before shipping SMS.
      };
      const r = await fetch(`${base}/${hash}`, {
        method: 'PUT',                // add-or-update (idempotent)
        headers: { Authorization: auth, 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await r.json();
      if (!r.ok) return res.status(200).json({ ok: false, message: friendly(data) });
    }
    return res.status(200).json({ ok: true, message: "You're on the list!" });
  } catch (e) {
    return res.status(200).json({ ok: false, message: 'Server error. Please try again.' });
  }
}

function friendly(data) {
  if (data?.title === 'Member Exists') return "You're already subscribed — thanks!";
  return data?.detail || 'Could not subscribe right now.';
}
```

> SMS via API caveat: the SMS phone‑number field is supported by the Marketing API, but the exact
> payload keys for SMS subscription have evolved. Before you ship the phone path, confirm the current
> field names against Mailchimp's live Members endpoint reference for your account, and make sure
> your SMS program is approved. If in doubt, use Method B (generated markup) for the phone field.

---

## Part 5 — Test & troubleshoot

- Use fresh, real‑looking data. Mailchimp rejects obvious fakes like `john@example.com`; test with
  a real address you haven't used in this account.
- Double opt‑in: if the audience is double opt‑in, a first submit returns an "almost finished /
  check your inbox" message, and the contact sits as `pending` until they confirm — that's expected.
- No success message (JSONP): usually a JS conflict or a required, hidden field. Keep the honeypot's
  `name` exactly `b_<u>_<id>`; don't leave any *required* merge field out of the form.
- Bot signups flooding the list: enable reCAPTCHA in the audience form settings (regenerate the
  form afterward), and keep the honeypot.
- CORS errors (Method C serverless): set `Access-Control-Allow-Origin` to your exact store origin,
  or switch to an App Proxy to stay same‑origin.
- Contact appears but no purchase data: that's the native integration's job — confirm the Mailchimp
  app is connected in Shopify and syncing to the same audience your form targets.

---

## Part 6 — Compliance & gotchas (don't skip)

- Email and SMS consent are separate. A single "Notify me" click can cover both only if your
  copy makes the two channels explicit and the SMS consent is its own checkbox with the required
  language. That's why the form reveals the SMS consent box only when a phone number is entered.
- SMS is heavily regulated (TCPA in the US). Keep the consent record, honor STOP/HELP
  keywords (Mailchimp auto‑handles these on an approved program), respect quiet hours, and only
  text subscribers in your registered country.
- Never put an API key in theme or browser code. Anything client‑side (Methods A/B) uses only the
  public `u`/`id`; the secret key stays on the server (Method C).
- One announcement bar per theme. If your theme already has one and you added a separate `alerts-bar`
  section, decide which owns the top slot to avoid stacking two bars.
- Test‑theme first. Duplicate the live theme, build and QA on the copy, then publish.

---

## Part 7 — Handoff plan: who does what

This feature spans two places the agent cannot reach: the Mailchimp admin and the Shopify
admin dashboard. The agent lives only in the theme code. So the work splits cleanly. Do the
Track A dashboard work, assemble the handoff packet, then let the agent run Track B.

Dependency note: the email path can be built and shipped independently and immediately. The
phone/SMS path is blocked until your Mailchimp SMS program is approved (Track A, step 4) —
which can take time. Recommended sequencing: ship email now; enable phone as a fast follow once
approval lands. The agent should build the form so the phone field can be turned on later without a
rewrite (it already is).

### Track A — YOUR tasks (Mailchimp + Shopify admin dashboards)

In Mailchimp

1. Pick the audience these signups will land in (or create one). Everything targets this single
   audience.
2. Grab the three identifiers. Audience → Signup forms → Embedded forms → generate any form, and
   read them off the form's `action` URL: the data center (`us21`), the `u=` account id, and
   the `id=` audience id. Also copy the honeypot field name `b_<u>_<id>` from that generated
   code.
3. Choose opt‑in style. In the audience settings, decide single vs double opt‑in and tell the
   agent (it changes the expected success message and the `status_if_new` value).
4. Turn on reCAPTCHA for the form (audience form settings) to blunt bot signups.
5. (Phone/SMS only — do early, it gates everything SMS): make sure you're on Essentials or
   higher, then submit the SMS Marketing application and get approved, buy SMS credits, and
   complete number registration (10DLC, or a short code on Standard+). Note your sending
   country. Once approved, generate an embedded form with the SMS phone‑number field enabled and
   copy that block including its non‑editable consent checkbox — this is what the agent splices in
   for Method B.
6. (Method C only — the server path): create a Marketing API key, store it as a server
   environment variable (never hand it to the agent for theme code), stand up the endpoint (App
   Proxy or serverless), and give the agent only the endpoint URL.
7. Confirm the native app is connected. Install/verify Mailchimp Email & SMS Marketing in
   Shopify and confirm it's syncing to the same audience you chose in step 1.

In Shopify admin

8. Duplicate the live theme (Online Store → Themes → ⋯ → Duplicate). The agent works on the copy.
9. Give the agent access to that unpublished theme (theme code access, or the GitHub‑connected
   repo / Shopify CLI setup your agent uses). Confirm the agent can Preview it.
10. Provide test data: a real email you haven't used in this account, and (if SMS is live) a
    real mobile number in your sending country.
11. Publish the theme yourself after you've reviewed the agent's Preview and QA. (Publishing is an
    admin action; keep it in your hands.)

The handoff packet to give the agent

> - Data center: `us20`  ·  `u=` account id: `bb68751aca24eb8005a87da31`  ·  Audience `id=`: `7488b9bad0`
> - Honeypot field name: `b_bb68751aca24eb8005a87da31_7488b9bad0`
> - Opt‑in style: `single`
> - Method for email: A (JSONP) or C (server) → if C, endpoint URL: `______`
> - Method for phone: B (paste generated markup) or C (server) or not yet (SMS pending)
> - If Method B: the generated SMS field + consent block (paste it in)
> - Unpublished/dev theme + preview access; test email (and test phone if SMS is live)
> - Desired default bar message, "popup‑open" message, and button label

Here is the embedded form code:

```html
<div id="mc_embed_shell">
      <link href="//cdn-images.mailchimp.com/embedcode/classic-061523.css" rel="stylesheet" type="text/css">
  <style type="text/css">
        #mc_embed_signup{background:#fff; false;clear:left; font:14px Helvetica,Arial,sans-serif; width: 600px;}
        /* Add your own Mailchimp form style overrides in your site stylesheet or in this style block.
           We recommend moving this block and the preceding CSS link to the HEAD of your HTML file. */
</style>
<div id="mc_embed_signup">
    <form action="https://hazelboutique.us20.list-manage.com/subscribe/post?u=bb68751aca24eb8005a87da31&amp;id=7488b9bad0&amp;f_id=000e76eef0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank">
        <div id="mc_embed_signup_scroll"><h2>Subscribe</h2>
            <div class="indicates-required"><span class="asterisk">*</span> indicates required</div>
            <div class="mc-field-group"><label for="mce-EMAIL">Email Address <span class="asterisk">*</span></label><input type="email" name="EMAIL" class="required email" id="mce-EMAIL" required="" value=""></div><div class="mc-field-group"><label for="mce-SMSPHONE">SMS Phone Number <span class="asterisk">*</span></label><div class="" style="display: flex; border: 1px solid rgb(171, 176, 178);"><div style="display: flex;"><span style="padding-left: 0px; padding-right: 4px; align-self: center;"><div style="display: flex; align-content: flex-start; align-items: center; gap: 10px;"><div id="flag-display-SMSPHONE" style="display: flex; align-items: center; gap: 4px; cursor: pointer; padding-left: 8px; position: relative;"><span id="flag-emoji-SMSPHONE">🇺🇸</span><svg xmlns="http://www.w3.org/2000/svg" width="16" height="17" viewBox="0 0 16 17" fill="none"><path d="M8.0096 11.5649C7.9219 11.5649 7.83506 11.5476 7.75407 11.5139C7.67307 11.4803 7.59951 11.431 7.5376 11.3689L3.54293 7.36289C3.48099 7.30091 3.43186 7.22733 3.39836 7.14636C3.36485 7.06539 3.34763 6.97862 3.34766 6.89099C3.34769 6.80336 3.36498 6.7166 3.39854 6.63565C3.4321 6.55471 3.48128 6.48117 3.54326 6.41923C3.60525 6.35729 3.67882 6.30816 3.75979 6.27466C3.84076 6.24115 3.92754 6.22392 4.01517 6.22395C4.10279 6.22398 4.18956 6.24127 4.2705 6.27484C4.35145 6.3084 4.42499 6.35758 4.48693 6.41956L8.01093 9.95289L11.5443 6.42956C11.6694 6.30464 11.8391 6.23457 12.016 6.23476C12.1928 6.23495 12.3623 6.30538 12.4873 6.43056C12.6122 6.55574 12.6823 6.72542 12.6821 6.90227C12.6819 7.07911 12.6114 7.24864 12.4863 7.37356L8.48026 11.3702C8.35532 11.4949 8.18607 11.5649 8.0096 11.5649Z" fill="#21262A"></path></svg><select id="country-select-SMSPHONE" name="SMSPHONE[country]" style="position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 10; border-width: medium; border-style: none; border-color: currentcolor; border-image: initial; background: transparent; font-size: 0px; margin: 0px; padding: 0px; min-width: auto; max-width: none;"><option value="US" selected="">US+1</option></select></div></div></span></div><input type="text" name="SMSPHONE" class="REQ_CSS" id="mce-SMSPHONE" placeholder="+1 000 000 0000" value="" style="border-width: medium; border-style: none; border-color: currentcolor; border-image: initial;"></div><div class="mc-sms-phone-group"><div><input type="checkbox" name="mc-SMSPHONE-ack" id="mc-SMSPHONE-ack" value="true"></div><div class="small-meta"><div id="legal-text-SMSPHONE"><div>Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a target="_blank" href="http://eepurl.com/iwthPw" rel="noopener noreferrer">See terms</a>, <a target="_blank" href="" rel="noopener noreferrer">See Privacy Policy</a></div></div></div></div></div>
        <div id="mce-responses" class="clear">
            <div class="response" id="mce-error-response" style="display: none;"></div>
            <div class="response" id="mce-success-response" style="display: none;"></div>
        </div><div aria-hidden="true" style="position: absolute; left: -5000px;"><input type="text" name="b_bb68751aca24eb8005a87da31_7488b9bad0" tabindex="-1" value=""></div><div class="clear"><input type="submit" name="subscribe" id="mc-embedded-subscribe" class="button" value="Subscribe"></div>
    </div>
</form>
</div>
<script type="text/javascript" src="//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js"></script><script type="text/javascript">(function($) {window.fnames = new Array(); window.ftypes = new Array();fnames[0]='EMAIL';ftypes[0]='email';fnames[6]='SMSPHONE';ftypes[6]='smsphone';fnames[1]='FNAME';ftypes[1]='text';fnames[2]='LNAME';ftypes[2]='text';fnames[3]='ADDRESS';ftypes[3]='address';fnames[4]='PHONE';ftypes[4]='phone';fnames[5]='BIRTHDAY';ftypes[5]='birthday';fnames[7]='SHOPB2BCO';ftypes[7]='text';}(jQuery));var $mcj = jQuery.noConflict(true);
    // SMS Phone Multi-Country Functionality
    if(!window.MC) {
      window.MC = {};
    }
    window.MC.smsPhoneData = {
      defaultCountryCode: 'US',
      programs: [{"countryCode":"US","countryCallingCode":"+1","number":"+17328131627","imgSrc":"https://flagcdn.com/w40/us.png","requiredTemplate":"Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","optionalTemplate":"Hazel Boutique  - By providing your phone number, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","language":"en"}],
      smsProgramDataCountryNames: [{"code":"US","name":"USA"}]
    };

    function getCountryUnicodeFlag(countryCode) {
       return countryCode.toUpperCase().replace(/./g, (char) => String.fromCodePoint(char.charCodeAt(0) + 127397))
    };

    // HTML sanitization function to prevent XSS
    function sanitizeHtml(str) {
      if (typeof str !== 'string') return '';
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');
    }

    // URL sanitization function to prevent javascript: and data: URLs
    function sanitizeUrl(url) {
      if (typeof url !== 'string') return '';
      const trimmedUrl = url.trim().toLowerCase();
      if (trimmedUrl.startsWith('javascript:') || trimmedUrl.startsWith('data:') || trimmedUrl.startsWith('vbscript:')) {
        return '#';
      }
      return url;
    }

    const getBrowserLanguage = () => {
      if (!window?.navigator?.language?.split('-')[1]) {
        return window?.navigator?.language?.toUpperCase();
      }
      return window?.navigator?.language?.split('-')[1];
    };

    
    function getDefaultCountryProgram(defaultCountryCode, smsProgramData) {
      if (!smsProgramData || smsProgramData.length === 0) {
        return null;
      }

      const browserLanguage = getBrowserLanguage();

      if (browserLanguage) {
        const foundProgram = smsProgramData.find(
          (program) => program?.countryCode === browserLanguage,
        );
        if (foundProgram) {
          return foundProgram;
        }
      }

      if (defaultCountryCode) {
        const foundProgram = smsProgramData.find(
          (program) => program?.countryCode === defaultCountryCode,
        );
        if (foundProgram) {
          return foundProgram;
        }
      }

      return smsProgramData[0];
    }

    function updateSmsLegalText(countryCode, fieldName) {
      if (!countryCode || !fieldName) {
        return;
      }
      
      const programs = window?.MC?.smsPhoneData?.programs;
      if (!programs || !Array.isArray(programs)) {
        return;
      }
      
      const program = programs.find(program => program?.countryCode === countryCode);
      if (!program || !program.requiredTemplate) {
        return;
      }
    
      
      var smsConsentHtmlRenderingFixEnabled = true;
      
      const legalTextElement = document.querySelector('#legal-text-' + fieldName);
      if (!legalTextElement) {
        return;
      }
      
      const divRegex = new RegExp('</?[div][^>]*>', 'gi');
      const blockWrapperRegex = new RegExp('</?(?:div|p)[^>]*>', 'gi');
      const fullAnchorRegex = new RegExp('<a.*?</a>', 'g');
      const anchorRegex = new RegExp('<a href="(.*?)" target="(.*?)">(.*?)</a>');
      
      const template = smsConsentHtmlRenderingFixEnabled
        ? program.requiredTemplate
            .replace(/<\/p>\s*<p[^>]*>/gi, ' ')
            .replace(blockWrapperRegex, '')
        : program.requiredTemplate.replace(divRegex, '');
      
      

      legalTextElement.textContent = '';
      const parts = template.split(/(<a href=".*?" target=".*?">.*?<\/a>)/g);
      parts.forEach(function(part) {
        if (!part) {
          return;
        }
        const anchorMatch = part.match(/<a href="(.*?)" target="(.*?)">(.*?)<\/a>/);
        if (anchorMatch) {
          const linkElement = document.createElement('a');
          linkElement.href = sanitizeUrl(anchorMatch[1]);
          linkElement.target = sanitizeHtml(anchorMatch[2]);
          linkElement.textContent = sanitizeHtml(anchorMatch[3]);
          legalTextElement.appendChild(linkElement);
        } else {
          legalTextElement.appendChild(document.createTextNode(part));
        }
      });
          
    }

    function generateDropdownOptions(smsProgramData) {
      if (!smsProgramData || smsProgramData.length === 0) {
        return '';
      }

      var programs = false
        ? smsProgramData.filter(function(p, i, arr) {
            return arr.findIndex(function(q) { return q.countryCode === p.countryCode; }) === i;
          })
        : smsProgramData;
      
      return programs.map(program => {
        const flag = getCountryUnicodeFlag(program.countryCode);
        const countryName = getCountryName(program.countryCode);
        const callingCode = program.countryCallingCode || '';
        // Sanitize all values to prevent XSS
        const sanitizedCountryCode = sanitizeHtml(program.countryCode || '');
        const sanitizedCountryName = sanitizeHtml(countryName || '');
        const sanitizedCallingCode = sanitizeHtml(callingCode || '');
        return '<option value="' + sanitizedCountryCode + '">' + sanitizedCountryName + ' ' + sanitizedCallingCode + '</option>';
      }).join('');
    }

    function getCountryName(countryCode) {
      if (window.MC?.smsPhoneData?.smsProgramDataCountryNames && Array.isArray(window.MC.smsPhoneData.smsProgramDataCountryNames)) {
        for (let i = 0; i < window.MC.smsPhoneData.smsProgramDataCountryNames.length; i++) {
          if (window.MC.smsPhoneData.smsProgramDataCountryNames[i].code === countryCode) {
            return window.MC.smsPhoneData.smsProgramDataCountryNames[i].name;
          }
        }
      }
      return countryCode;
    }

    function getDefaultPlaceholder(countryCode) {
      if (!countryCode || typeof countryCode !== 'string') {
        return '+1 000 000 0000'; // Default US placeholder
      }
      
            var mockPlaceholders = [
        {
          countryCode: 'US',
          placeholder: '+1 000 000 0000',
          helpText: 'Include the US country code +1 before the phone number',
        },
        {
          countryCode: 'GB',
          placeholder: '+44 0000 000000',
          helpText: 'Include the GB country code +44 before the phone number',
        },
        {
          countryCode: 'CA',
          placeholder: '+1 000 000 0000',
          helpText: 'Include the CA country code +1 before the phone number',
        },
        {
          countryCode: 'AU',
          placeholder: '+61 000 000 000',
          helpText: 'Include the AU country code +61 before the phone number',
        },
        {
          countryCode: 'DE',
          placeholder: '+49 000 0000000',
          helpText: 'Fügen Sie vor der Telefonnummer die DE-Ländervorwahl +49 ein',
        },
        {
          countryCode: 'FR',
          placeholder: '+33 0 00 00 00 00',
          helpText: 'Incluez le code pays FR +33 avant le numéro de téléphone',
        },
        {
          countryCode: 'ES',
          placeholder: '+34 000 000 000',
          helpText: 'Incluya el código de país ES +34 antes del número de teléfono',
        },
        {
          countryCode: 'NL',
          placeholder: '+31 0 00000000',
          helpText: 'Voeg de NL-landcode +31 toe vóór het telefoonnummer',
        },
        {
          countryCode: 'BE',
          placeholder: '+32 000 00 00 00',
          helpText: 'Incluez le code pays BE +32 avant le numéro de téléphone',
        },
        {
          countryCode: 'CH',
          placeholder: '+41 00 000 00 00',
          helpText: 'Fügen Sie vor der Telefonnummer die CH-Ländervorwahl +41 ein',
        },
        {
          countryCode: 'AT',
          placeholder: '+43 000 000 0000',
          helpText: 'Fügen Sie vor der Telefonnummer die AT-Ländervorwahl +43 ein',
        },
        {
          countryCode: 'IE',
          placeholder: '+353 00 000 0000',
          helpText: 'Include the IE country code +353 before the phone number',
        },
        {
          countryCode: 'IT',
          placeholder: '+39 000 000 0000',
          helpText: 'Includere il prefisso internazionale IT +39 prima del numero di telefono',
        },
        {
          countryCode: 'NO',
          placeholder: '+47 000 00 000',
          helpText: 'Inkluder NO landskode +47 før telefonnummeret',
        },
        {
          countryCode: 'SE',
          placeholder: '+46 00 000 00 00',
          helpText: 'Inkludera SE landskod +46 före telefonnumret',
        },
        {
          countryCode: 'DK',
          placeholder: '+45 00 00 00 00',
          helpText: 'Inkluder DK landekode +45 før telefonnummeret',
        },
        {
          countryCode: 'FI',
          placeholder: '+358 00 000 0000',
          helpText: 'Sisällytä FI-maakoodi +358 ennen puhelinnumeroa',
        },
        {
          countryCode: 'EE',
          placeholder: '+372 0000 0000',
          helpText: 'Lisage EE riigikood +372 telefoninumbri ette',
        },
        {
          countryCode: 'PL',
          placeholder: '+48 000 000 000',
          helpText: 'Podaj numer kierunkowy PL +48 przed numerem telefonu',
        },
        {
          countryCode: 'SK',
          placeholder: '+421 000 000 000',
          helpText: 'Pred telefónne číslo uveďte kód krajiny SK +421',
        },
        {
          countryCode: 'LV',
          placeholder: '+371 0000 0000',
          helpText: 'Iekļaujiet LV valsts kodu +371 pirms tālruņa numura',
        },
        {
          countryCode: 'LT',
          placeholder: '+370 0000 0000',
          helpText: 'Įtraukite LT šalies kodą +370 prieš telefono numerį',
        },
        {
          countryCode: 'GR',
          placeholder: '+30 000 000 0000',
          helpText: 'Συμπεριλάβετε τον κωδικό χώρας GR +30 πριν από τον αριθμό τηλεφώνου',
        },
        {
          countryCode: 'PT',
          placeholder: '+351 000 000 000',
          helpText: 'Inclua o código de país PT +351 antes do número de telefone',
        },
        {
          countryCode: 'HR',
          placeholder: '+385 00 000 0000',
          helpText: 'Uključite HR pozivni broj države +385 prije telefonskog broja',
        },
        {
          countryCode: 'SI',
          placeholder: '+386 00 000 000',
          helpText: 'Vključite SI kodo države +386 pred telefonsko številko',
        },
        {
          countryCode: 'IS',
          placeholder: '+354 000 0000',
          helpText: 'Láttu IS landsnúmer +354 fylgja á undan símanúmerinu',
        },
        {
          countryCode: 'LU',
          placeholder: '+352 000 000 000',
          helpText: 'Incluez le code pays LU +352 avant le numéro de téléphone',
        },
        {
          countryCode: 'MC',
          placeholder: '+377 00 00 00 00',
          helpText: 'Incluez le code pays MC +377 avant le numéro de téléphone',
        },
        {
          countryCode: 'AD',
          placeholder: '+376 000 000',
          helpText: 'Incloeu el codi de país AD +376 abans del número de telèfon',
        },
        {
          countryCode: 'JE',
          placeholder: '+44 0000 000000',
          helpText: 'Include the JE country code +44 before the phone number',
        },
        {
          countryCode: 'IM',
          placeholder: '+44 0000 000000',
          helpText: 'Include the IM country code +44 before the phone number',
        },
        {
          countryCode: 'GG',
          placeholder: '+44 0000 000000',
          helpText: 'Include the GG country code +44 before the phone number',
        },
        {
          countryCode: 'AL',
          placeholder: '+355 00 000 0000',
          helpText: 'Përfshini kodin e vendit AL +355 para numrit të telefonit',
        },
        {
          countryCode: 'SM',
          placeholder: '+378 0000 000000',
          helpText: 'Includere il prefisso internazionale SM +378 prima del numero di telefono',
        },
        {
          countryCode: 'FO',
          placeholder: '+298 000000',
          helpText: 'Inkluder FO landekode +298 før telefonnummeret',
        },
        {
          countryCode: 'MT',
          placeholder: '+356 0000 0000',
          helpText: 'Include the MT country code +356 before the phone number',
        },
        {
          countryCode: 'LI',
          placeholder: '+423 000 0000',
          helpText: 'Fügen Sie vor der Telefonnummer die LI-Ländervorwahl +423 ein',
        },
        {
          countryCode: 'GI',
          placeholder: '+350 000 00000',
          helpText: 'Include the GI country code +350 before the phone number',
        },
        {
          countryCode: 'MD',
          placeholder: '+373 00 000 000',
          helpText: 'Includeți codul de țară MD +373 înaintea numărului de telefon',
        },
        {
          countryCode: 'HU',
          placeholder: '+36 00 000 0000',
          helpText: 'A telefonszám előtt adja meg a HU országkódot +36',
        },
        {
          countryCode: 'NZ',
          placeholder: '+64 00 000 0000',
          helpText: 'Include the NZ country code +64 before the phone number',
        },
        {
          countryCode: 'ME',
          placeholder: '+382 00 000 000',
          helpText: 'Uključite ME pozivni broj države +382 prije telefonskog broja',
        },
      ];

      const selectedPlaceholder = mockPlaceholders.find(function(item) {
        return item && item.countryCode === countryCode;
      });
      
      return selectedPlaceholder ? selectedPlaceholder.placeholder : mockPlaceholders[0].placeholder;
    }

    function updatePlaceholder(countryCode, fieldName) {
      if (!countryCode || !fieldName) {
        return;
      }
      
      const phoneInput = document.querySelector('#mce-' + fieldName);
      if (!phoneInput) {
        return;
      }
      
      const placeholder = getDefaultPlaceholder(countryCode);
      if (placeholder) {
        phoneInput.placeholder = placeholder;
      }
    }

    function updateCountryCodeInstruction(countryCode, fieldName) {
      updatePlaceholder(countryCode, fieldName);
      
    }

    function getDefaultHelpText(countryCode) {
      var mockPlaceholders = [
        {
          countryCode: 'US',
          placeholder: '+1 000 000 0000',
          helpText: 'Include the US country code +1 before the phone number',
        },
        {
          countryCode: 'GB',
          placeholder: '+44 0000 000000',
          helpText: 'Include the GB country code +44 before the phone number',
        },
        {
          countryCode: 'CA',
          placeholder: '+1 000 000 0000',
          helpText: 'Include the CA country code +1 before the phone number',
        },
        {
          countryCode: 'AU',
          placeholder: '+61 000 000 000',
          helpText: 'Include the AU country code +61 before the phone number',
        },
        {
          countryCode: 'DE',
          placeholder: '+49 000 0000000',
          helpText: 'Fügen Sie vor der Telefonnummer die DE-Ländervorwahl +49 ein',
        },
        {
          countryCode: 'FR',
          placeholder: '+33 0 00 00 00 00',
          helpText: 'Incluez le code pays FR +33 avant le numéro de téléphone',
        },
        {
          countryCode: 'ES',
          placeholder: '+34 000 000 000',
          helpText: 'Incluya el código de país ES +34 antes del número de teléfono',
        },
        {
          countryCode: 'NL',
          placeholder: '+31 0 00000000',
          helpText: 'Voeg de NL-landcode +31 toe vóór het telefoonnummer',
        },
        {
          countryCode: 'BE',
          placeholder: '+32 000 00 00 00',
          helpText: 'Incluez le code pays BE +32 avant le numéro de téléphone',
        },
        {
          countryCode: 'CH',
          placeholder: '+41 00 000 00 00',
          helpText: 'Fügen Sie vor der Telefonnummer die CH-Ländervorwahl +41 ein',
        },
        {
          countryCode: 'AT',
          placeholder: '+43 000 000 0000',
          helpText: 'Fügen Sie vor der Telefonnummer die AT-Ländervorwahl +43 ein',
        },
        {
          countryCode: 'IE',
          placeholder: '+353 00 000 0000',
          helpText: 'Include the IE country code +353 before the phone number',
        },
        {
          countryCode: 'IT',
          placeholder: '+39 000 000 0000',
          helpText: 'Includere il prefisso internazionale IT +39 prima del numero di telefono',
        },
        {
          countryCode: 'NO',
          placeholder: '+47 000 00 000',
          helpText: 'Inkluder NO landskode +47 før telefonnummeret',
        },
        {
          countryCode: 'SE',
          placeholder: '+46 00 000 00 00',
          helpText: 'Inkludera SE landskod +46 före telefonnumret',
        },
        {
          countryCode: 'DK',
          placeholder: '+45 00 00 00 00',
          helpText: 'Inkluder DK landekode +45 før telefonnummeret',
        },
        {
          countryCode: 'FI',
          placeholder: '+358 00 000 0000',
          helpText: 'Sisällytä FI-maakoodi +358 ennen puhelinnumeroa',
        },
        {
          countryCode: 'EE',
          placeholder: '+372 0000 0000',
          helpText: 'Lisage EE riigikood +372 telefoninumbri ette',
        },
        {
          countryCode: 'PL',
          placeholder: '+48 000 000 000',
          helpText: 'Podaj numer kierunkowy PL +48 przed numerem telefonu',
        },
        {
          countryCode: 'SK',
          placeholder: '+421 000 000 000',
          helpText: 'Pred telefónne číslo uveďte kód krajiny SK +421',
        },
        {
          countryCode: 'LV',
          placeholder: '+371 0000 0000',
          helpText: 'Iekļaujiet LV valsts kodu +371 pirms tālruņa numura',
        },
        {
          countryCode: 'LT',
          placeholder: '+370 0000 0000',
          helpText: 'Įtraukite LT šalies kodą +370 prieš telefono numerį',
        },
        {
          countryCode: 'GR',
          placeholder: '+30 000 000 0000',
          helpText: 'Συμπεριλάβετε τον κωδικό χώρας GR +30 πριν από τον αριθμό τηλεφώνου',
        },
        {
          countryCode: 'PT',
          placeholder: '+351 000 000 000',
          helpText: 'Inclua o código de país PT +351 antes do número de telefone',
        },
        {
          countryCode: 'HR',
          placeholder: '+385 00 000 0000',
          helpText: 'Uključite HR pozivni broj države +385 prije telefonskog broja',
        },
        {
          countryCode: 'SI',
          placeholder: '+386 00 000 000',
          helpText: 'Vključite SI kodo države +386 pred telefonsko številko',
        },
        {
          countryCode: 'IS',
          placeholder: '+354 000 0000',
          helpText: 'Láttu IS landsnúmer +354 fylgja á undan símanúmerinu',
        },
        {
          countryCode: 'LU',
          placeholder: '+352 000 000 000',
          helpText: 'Incluez le code pays LU +352 avant le numéro de téléphone',
        },
        {
          countryCode: 'MC',
          placeholder: '+377 00 00 00 00',
          helpText: 'Incluez le code pays MC +377 avant le numéro de téléphone',
        },
        {
          countryCode: 'AD',
          placeholder: '+376 000 000',
          helpText: 'Incloeu el codi de país AD +376 abans del número de telèfon',
        },
        {
          countryCode: 'JE',
          placeholder: '+44 0000 000000',
          helpText: 'Include the JE country code +44 before the phone number',
        },
        {
          countryCode: 'IM',
          placeholder: '+44 0000 000000',
          helpText: 'Include the IM country code +44 before the phone number',
        },
        {
          countryCode: 'GG',
          placeholder: '+44 0000 000000',
          helpText: 'Include the GG country code +44 before the phone number',
        },
        {
          countryCode: 'AL',
          placeholder: '+355 00 000 0000',
          helpText: 'Përfshini kodin e vendit AL +355 para numrit të telefonit',
        },
        {
          countryCode: 'SM',
          placeholder: '+378 0000 000000',
          helpText: 'Includere il prefisso internazionale SM +378 prima del numero di telefono',
        },
        {
          countryCode: 'FO',
          placeholder: '+298 000000',
          helpText: 'Inkluder FO landekode +298 før telefonnummeret',
        },
        {
          countryCode: 'MT',
          placeholder: '+356 0000 0000',
          helpText: 'Include the MT country code +356 before the phone number',
        },
        {
          countryCode: 'LI',
          placeholder: '+423 000 0000',
          helpText: 'Fügen Sie vor der Telefonnummer die LI-Ländervorwahl +423 ein',
        },
        {
          countryCode: 'GI',
          placeholder: '+350 000 00000',
          helpText: 'Include the GI country code +350 before the phone number',
        },
        {
          countryCode: 'MD',
          placeholder: '+373 00 000 000',
          helpText: 'Includeți codul de țară MD +373 înaintea numărului de telefon',
        },
        {
          countryCode: 'HU',
          placeholder: '+36 00 000 0000',
          helpText: 'A telefonszám előtt adja meg a HU országkódot +36',
        },
        {
          countryCode: 'NZ',
          placeholder: '+64 00 000 0000',
          helpText: 'Include the NZ country code +64 before the phone number',
        },
        {
          countryCode: 'ME',
          placeholder: '+382 00 000 000',
          helpText: 'Uključite ME pozivni broj države +382 prije telefonskog broja',
        },
      ];
      
      if (!countryCode || typeof countryCode !== 'string') {
        return mockPlaceholders[0].helpText;
      }
      
      const selectedHelpText = mockPlaceholders.find(function(item) {
          return item && item.countryCode === countryCode;
        });
        
        return selectedHelpText ? selectedHelpText.helpText : mockPlaceholders[0].helpText;
    }

    function setDefaultHelpText(countryCode) {
      const helpTextSpan = document.querySelector('#help-text');
      if (!helpTextSpan) {
        return;
      }

        
    }

    function updateHelpTextCountryCode(countryCode, fieldName) {
      if (!countryCode || !fieldName) {
        return;
      }
      
      setDefaultHelpText(countryCode);
    }

    function initializeSmsPhoneDropdown(fieldName) {
      if (!fieldName || typeof fieldName !== 'string') {
        return;
      }
      
      const dropdown = document.querySelector('#country-select-' + fieldName);
      const displayFlag = document.querySelector('#flag-display-' + fieldName);
      
      if (!dropdown || !displayFlag) {
        return;
      }

      const smsPhoneData = window.MC?.smsPhoneData;
      if (smsPhoneData && smsPhoneData.programs && Array.isArray(smsPhoneData.programs)) {
        dropdown.innerHTML = generateDropdownOptions(smsPhoneData.programs);
      }

      const defaultProgram = getDefaultCountryProgram(smsPhoneData?.defaultCountryCode, smsPhoneData?.programs);
      if (defaultProgram && defaultProgram.countryCode) {
        dropdown.value = defaultProgram.countryCode;
        
        const flagSpan = displayFlag?.querySelector('#flag-emoji-' + fieldName);
        if (flagSpan) {
          flagSpan.textContent = getCountryUnicodeFlag(defaultProgram.countryCode);
          flagSpan.setAttribute('aria-label', sanitizeHtml(defaultProgram.countryCode) + ' flag');
        }
        
        updateSmsLegalText(defaultProgram.countryCode, fieldName);
        updatePlaceholder(defaultProgram.countryCode, fieldName);
        updateCountryCodeInstruction(defaultProgram.countryCode, fieldName);
      }

     
      var smsNotRequiredRemoveCountryCodeEnabled = true;
      var smsField = Object.values({"EMAIL":{"name":"EMAIL","label":"Email Address","helper_text":"","type":"email","required":true,"audience_field_name":"Email Address","merge_id":0,"help_text_enabled":false,"enabled":true,"order":0,"field_type":"merge"},"SMSPHONE":{"name":"SMSPHONE","label":"SMS Phone Number","helper_text":"","type":"smsphone","required":true,"audience_field_name":"SMS Phone Number","legal":{"required":"Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>","optional":"Hazel Boutique  - By providing your phone number, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>"},"smsProgramData":[{"countryCode":"US","countryCallingCode":"+1","number":"+17328131627","imgSrc":"https://flagcdn.com/w40/us.png","requiredTemplate":"Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","optionalTemplate":"Hazel Boutique  - By providing your phone number, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","language":"en"}],"defaultCountryCode":"US","countryNames":[{"code":"US","name":"USA"}],"multiCountryEnabled":true,"formsMultiCountryFastFollowsEnabled":true,"legaleseVersionCaptureAndSaveEnabled":true,"smsNotRequiredRemoveCountryCodeEnabled":true,"landingPagesInputStylesFixEnabled":true,"europeanSmsExpansionEnabled":true,"ageGatingEnabled":false,"phoneformat":"","merge_id":6,"help_text_enabled":false,"enabled":true,"order":1,"field_type":"merge"},"FNAME":{"name":"FNAME","label":"First Name","helper_text":"","type":"text","required":false,"audience_field_name":"First Name","enabled":false,"order":null,"field_type":"merge","merge_id":1},"LNAME":{"name":"LNAME","label":"Last Name","helper_text":"","type":"text","required":false,"audience_field_name":"Last Name","enabled":false,"order":null,"field_type":"merge","merge_id":2},"ADDRESS":{"name":"ADDRESS","label":"Address","helper_text":"","type":"address","required":false,"audience_field_name":"Address","enabled":false,"order":null,"field_type":"merge","merge_id":3,"countries":{"2":"Albania","3":"Algeria","4":"Andorra","5":"Angola","6":"Argentina","7":"Armenia","8":"Australia","9":"Austria","10":"Azerbaijan","11":"Bahamas","12":"Bahrain","13":"Bangladesh","14":"Barbados","15":"Belarus","16":"Belgium","17":"Belize","18":"Benin","19":"Bermuda","20":"Bhutan","21":"Bolivia","22":"Bosnia and Herzegovina","23":"Botswana","24":"Brazil","25":"Bulgaria","26":"Burkina Faso","27":"Burundi","28":"Cambodia","29":"Cameroon","30":"Canada","31":"Cape Verde","32":"Cayman Islands","33":"Central African Republic","34":"Chad","35":"Chile","36":"China","37":"Colombia","38":"Congo","40":"Croatia","41":"Cyprus","42":"Czech Republic","43":"Denmark","44":"Djibouti","45":"Ecuador","46":"Egypt","47":"El Salvador","48":"Equatorial Guinea","49":"Eritrea","50":"Estonia","51":"Ethiopia","52":"Fiji","53":"Finland","54":"France","56":"Gabon","57":"Gambia","58":"Georgia","59":"Germany","60":"Ghana","61":"Greece","63":"Guinea","64":"Guinea-Bissau","65":"Guyana","66":"Honduras","67":"Hong Kong","68":"Hungary","69":"Iceland","70":"India","71":"Indonesia","74":"Ireland","75":"Israel","76":"Italy","78":"Japan","79":"Jordan","80":"Kazakhstan","81":"Kenya","82":"Kuwait","83":"Kyrgyzstan","84":"Lao People's Democratic Republic","85":"Latvia","86":"Lebanon","87":"Lesotho","88":"Liberia","90":"Liechtenstein","91":"Lithuania","92":"Luxembourg","93":"Macedonia","94":"Madagascar","95":"Malawi","96":"Malaysia","97":"Maldives","98":"Mali","99":"Malta","100":"Mauritania","101":"Mexico","102":"Moldova","103":"Monaco","104":"Mongolia","105":"Morocco","106":"Mozambique","107":"Namibia","108":"Nepal","109":"Netherlands","110":"Netherlands Antilles","111":"New Zealand","112":"Nicaragua","113":"Niger","114":"Nigeria","116":"Norway","117":"Oman","118":"Pakistan","119":"Panama","120":"Paraguay","121":"Peru","122":"Philippines","123":"Poland","124":"Portugal","126":"Qatar","127":"Reunion","128":"Romania","129":"Russia","130":"Rwanda","132":"Samoa (Independent)","133":"Saudi Arabia","134":"Senegal","135":"Seychelles","136":"Sierra Leone","137":"Singapore","138":"Slovakia","139":"Slovenia","140":"Somalia","141":"South Africa","142":"South Korea","143":"Spain","144":"Sri Lanka","146":"Suriname","147":"Swaziland","148":"Sweden","149":"Switzerland","152":"Taiwan","153":"Tanzania","154":"Thailand","155":"Togo","156":"Tunisia","157":"Turkiye","158":"Turkmenistan","159":"Uganda","161":"Ukraine","162":"United Arab Emirates","163":"Uruguay","164":"USA","165":"Uzbekistan","166":"Vatican City State (Holy See)","167":"Venezuela","168":"Vietnam","169":"Virgin Islands (British)","170":"Yemen","173":"Zambia","174":"Zimbabwe","175":"Antigua And Barbuda","176":"Anguilla","179":"Aruba","180":"Brunei Darussalam","181":"Bouvet Island","183":"Cook Islands","185":"Christmas Island","187":"Dominican Republic","188":"Western Sahara","189":"Falkland Islands","191":"Faroe Islands","192":"Grenada","193":"French Guiana","194":"Gibraltar","195":"Greenland","196":"Guadeloupe","198":"Guatemala","200":"Haiti","202":"Jamaica","203":"Kiribati","204":"Comoros","205":"Saint Kitts and Nevis","206":"Saint Lucia","207":"Marshall Islands","208":"Macau","210":"Martinique","212":"Mauritius","213":"New Caledonia","214":"Norfolk Island","215":"Nauru","217":"Niue","219":"Papua New Guinea","221":"Pitcairn","222":"Palau","223":"Solomon Islands","225":"Svalbard and Jan Mayen Islands","227":"San Marino","232":"Tonga","233":"Timor-Leste","234":"Trinidad and Tobago","235":"Tuvalu","237":"Saint Vincent and the Grenadines","239":"Vanuatu","241":"Mayotte","242":"Myanmar","255":"Sao Tome and Principe","257":"South Georgia and the South Sandwich Islands","260":"Tajikistan","262":"United Kingdom","268":"Costa Rica","270":"Guernsey","272":"North Korea","274":"Afghanistan","275":"Cote D'Ivoire","276":"Cuba","277":"French Polynesia","278":"Iran","279":"Iraq","281":"Libya","282":"Palestine","285":"Syria","286":"Aaland Islands","287":"Turks & Caicos Islands","288":"Jersey  (Channel Islands)","289":"Dominica","290":"Montenegro","293":"Sudan","294":"Montserrat","298":"Curacao","302":"Sint Maarten","311":"South Sudan","315":"Republic of Kosovo","318":"Congo, Democratic Republic of the","323":"Isle of Man","324":"Saint Martin","325":"Bonaire, Saint Eustatius and Saba","326":"Serbia","327":"Saint Barthelemy"},"defaultcountry":164},"PHONE":{"name":"PHONE","label":"Phone Number","helper_text":"","type":"phone","required":false,"audience_field_name":"Phone Number","phoneformat":"","enabled":false,"order":null,"field_type":"merge","merge_id":4},"BIRTHDAY":{"name":"BIRTHDAY","label":"Birthday","helper_text":"","type":"birthday","required":false,"audience_field_name":"Birthday","dateformat":"MM/DD","enabled":false,"order":null,"field_type":"merge","merge_id":5},"SHOPB2BCO":{"name":"SHOPB2BCO","label":"Shopify B2B Company","helper_text":"","type":"text","required":false,"audience_field_name":"Shopify B2B Company","enabled":false,"order":null,"field_type":"merge","merge_id":7}}).find(function(f) { return f.name === fieldName && f.type === 'smsphone'; });
      var isRequired = smsField ? smsField.required : false;
      var shouldAppendCountryCode = smsNotRequiredRemoveCountryCodeEnabled ? isRequired : true;
      
      var phoneInput = document.querySelector('#mce-' + fieldName);
      if (phoneInput && defaultProgram.countryCallingCode && shouldAppendCountryCode) {
        phoneInput.value = defaultProgram.countryCallingCode;
      }
      


      displayFlag?.addEventListener('click', function(e) {
        dropdown.focus();
      });


      dropdown?.addEventListener('change', function() {
        const selectedCountry = this.value;
        
        if (!selectedCountry || typeof selectedCountry !== 'string') {
          return;
        }
        
        const flagSpan = displayFlag?.querySelector('#flag-emoji-' + fieldName);
        if (flagSpan) {
          flagSpan.textContent = getCountryUnicodeFlag(selectedCountry);
          flagSpan.setAttribute('aria-label', sanitizeHtml(selectedCountry) + ' flag');
        }

         
        const selectedProgram = window.MC?.smsPhoneData?.programs.find(function(program) {
          return program && program.countryCode === selectedCountry;
        });

        var smsNotRequiredRemoveCountryCodeEnabled = true;
        var smsField = Object.values({"EMAIL":{"name":"EMAIL","label":"Email Address","helper_text":"","type":"email","required":true,"audience_field_name":"Email Address","merge_id":0,"help_text_enabled":false,"enabled":true,"order":0,"field_type":"merge"},"SMSPHONE":{"name":"SMSPHONE","label":"SMS Phone Number","helper_text":"","type":"smsphone","required":true,"audience_field_name":"SMS Phone Number","legal":{"required":"Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>","optional":"Hazel Boutique  - By providing your phone number, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>"},"smsProgramData":[{"countryCode":"US","countryCallingCode":"+1","number":"+17328131627","imgSrc":"https://flagcdn.com/w40/us.png","requiredTemplate":"Hazel Boutique  - By providing your phone number and checking the box, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","optionalTemplate":"Hazel Boutique  - By providing your phone number, you agree to receive promotional and marketing messages, notifications, and customer service communications from Hazel Boutique . Message and data rates may apply. Consent is not a condition of purchase. Message frequency varies. Text HELP for help. Text STOP to cancel. <a href=\"http://eepurl.com/iwthPw\" target=\"_blank\">See terms</a>, <a href=\"\" target=\"_blank\">See Privacy Policy</a>","language":"en"}],"defaultCountryCode":"US","countryNames":[{"code":"US","name":"USA"}],"multiCountryEnabled":true,"formsMultiCountryFastFollowsEnabled":true,"legaleseVersionCaptureAndSaveEnabled":true,"smsNotRequiredRemoveCountryCodeEnabled":true,"landingPagesInputStylesFixEnabled":true,"europeanSmsExpansionEnabled":true,"ageGatingEnabled":false,"phoneformat":"","merge_id":6,"help_text_enabled":false,"enabled":true,"order":1,"field_type":"merge"},"FNAME":{"name":"FNAME","label":"First Name","helper_text":"","type":"text","required":false,"audience_field_name":"First Name","enabled":false,"order":null,"field_type":"merge","merge_id":1},"LNAME":{"name":"LNAME","label":"Last Name","helper_text":"","type":"text","required":false,"audience_field_name":"Last Name","enabled":false,"order":null,"field_type":"merge","merge_id":2},"ADDRESS":{"name":"ADDRESS","label":"Address","helper_text":"","type":"address","required":false,"audience_field_name":"Address","enabled":false,"order":null,"field_type":"merge","merge_id":3,"countries":{"2":"Albania","3":"Algeria","4":"Andorra","5":"Angola","6":"Argentina","7":"Armenia","8":"Australia","9":"Austria","10":"Azerbaijan","11":"Bahamas","12":"Bahrain","13":"Bangladesh","14":"Barbados","15":"Belarus","16":"Belgium","17":"Belize","18":"Benin","19":"Bermuda","20":"Bhutan","21":"Bolivia","22":"Bosnia and Herzegovina","23":"Botswana","24":"Brazil","25":"Bulgaria","26":"Burkina Faso","27":"Burundi","28":"Cambodia","29":"Cameroon","30":"Canada","31":"Cape Verde","32":"Cayman Islands","33":"Central African Republic","34":"Chad","35":"Chile","36":"China","37":"Colombia","38":"Congo","40":"Croatia","41":"Cyprus","42":"Czech Republic","43":"Denmark","44":"Djibouti","45":"Ecuador","46":"Egypt","47":"El Salvador","48":"Equatorial Guinea","49":"Eritrea","50":"Estonia","51":"Ethiopia","52":"Fiji","53":"Finland","54":"France","56":"Gabon","57":"Gambia","58":"Georgia","59":"Germany","60":"Ghana","61":"Greece","63":"Guinea","64":"Guinea-Bissau","65":"Guyana","66":"Honduras","67":"Hong Kong","68":"Hungary","69":"Iceland","70":"India","71":"Indonesia","74":"Ireland","75":"Israel","76":"Italy","78":"Japan","79":"Jordan","80":"Kazakhstan","81":"Kenya","82":"Kuwait","83":"Kyrgyzstan","84":"Lao People's Democratic Republic","85":"Latvia","86":"Lebanon","87":"Lesotho","88":"Liberia","90":"Liechtenstein","91":"Lithuania","92":"Luxembourg","93":"Macedonia","94":"Madagascar","95":"Malawi","96":"Malaysia","97":"Maldives","98":"Mali","99":"Malta","100":"Mauritania","101":"Mexico","102":"Moldova","103":"Monaco","104":"Mongolia","105":"Morocco","106":"Mozambique","107":"Namibia","108":"Nepal","109":"Netherlands","110":"Netherlands Antilles","111":"New Zealand","112":"Nicaragua","113":"Niger","114":"Nigeria","116":"Norway","117":"Oman","118":"Pakistan","119":"Panama","120":"Paraguay","121":"Peru","122":"Philippines","123":"Poland","124":"Portugal","126":"Qatar","127":"Reunion","128":"Romania","129":"Russia","130":"Rwanda","132":"Samoa (Independent)","133":"Saudi Arabia","134":"Senegal","135":"Seychelles","136":"Sierra Leone","137":"Singapore","138":"Slovakia","139":"Slovenia","140":"Somalia","141":"South Africa","142":"South Korea","143":"Spain","144":"Sri Lanka","146":"Suriname","147":"Swaziland","148":"Sweden","149":"Switzerland","152":"Taiwan","153":"Tanzania","154":"Thailand","155":"Togo","156":"Tunisia","157":"Turkiye","158":"Turkmenistan","159":"Uganda","161":"Ukraine","162":"United Arab Emirates","163":"Uruguay","164":"USA","165":"Uzbekistan","166":"Vatican City State (Holy See)","167":"Venezuela","168":"Vietnam","169":"Virgin Islands (British)","170":"Yemen","173":"Zambia","174":"Zimbabwe","175":"Antigua And Barbuda","176":"Anguilla","179":"Aruba","180":"Brunei Darussalam","181":"Bouvet Island","183":"Cook Islands","185":"Christmas Island","187":"Dominican Republic","188":"Western Sahara","189":"Falkland Islands","191":"Faroe Islands","192":"Grenada","193":"French Guiana","194":"Gibraltar","195":"Greenland","196":"Guadeloupe","198":"Guatemala","200":"Haiti","202":"Jamaica","203":"Kiribati","204":"Comoros","205":"Saint Kitts and Nevis","206":"Saint Lucia","207":"Marshall Islands","208":"Macau","210":"Martinique","212":"Mauritius","213":"New Caledonia","214":"Norfolk Island","215":"Nauru","217":"Niue","219":"Papua New Guinea","221":"Pitcairn","222":"Palau","223":"Solomon Islands","225":"Svalbard and Jan Mayen Islands","227":"San Marino","232":"Tonga","233":"Timor-Leste","234":"Trinidad and Tobago","235":"Tuvalu","237":"Saint Vincent and the Grenadines","239":"Vanuatu","241":"Mayotte","242":"Myanmar","255":"Sao Tome and Principe","257":"South Georgia and the South Sandwich Islands","260":"Tajikistan","262":"United Kingdom","268":"Costa Rica","270":"Guernsey","272":"North Korea","274":"Afghanistan","275":"Cote D'Ivoire","276":"Cuba","277":"French Polynesia","278":"Iran","279":"Iraq","281":"Libya","282":"Palestine","285":"Syria","286":"Aaland Islands","287":"Turks & Caicos Islands","288":"Jersey  (Channel Islands)","289":"Dominica","290":"Montenegro","293":"Sudan","294":"Montserrat","298":"Curacao","302":"Sint Maarten","311":"South Sudan","315":"Republic of Kosovo","318":"Congo, Democratic Republic of the","323":"Isle of Man","324":"Saint Martin","325":"Bonaire, Saint Eustatius and Saba","326":"Serbia","327":"Saint Barthelemy"},"defaultcountry":164},"PHONE":{"name":"PHONE","label":"Phone Number","helper_text":"","type":"phone","required":false,"audience_field_name":"Phone Number","phoneformat":"","enabled":false,"order":null,"field_type":"merge","merge_id":4},"BIRTHDAY":{"name":"BIRTHDAY","label":"Birthday","helper_text":"","type":"birthday","required":false,"audience_field_name":"Birthday","dateformat":"MM/DD","enabled":false,"order":null,"field_type":"merge","merge_id":5},"SHOPB2BCO":{"name":"SHOPB2BCO","label":"Shopify B2B Company","helper_text":"","type":"text","required":false,"audience_field_name":"Shopify B2B Company","enabled":false,"order":null,"field_type":"merge","merge_id":7}}).find(function(f) { return f.name === fieldName && f.type === 'smsphone'; });
        var isRequired = smsField ? smsField.required : false;
        var shouldAppendCountryCode = smsNotRequiredRemoveCountryCodeEnabled ? isRequired : true;
        
        var phoneInput = document.querySelector('#mce-' + fieldName);
        if (phoneInput && selectedProgram.countryCallingCode && shouldAppendCountryCode) {
          phoneInput.value = selectedProgram.countryCallingCode;
        }
        
        
        updateSmsLegalText(selectedCountry, fieldName);
        updatePlaceholder(selectedCountry, fieldName);
        updateCountryCodeInstruction(selectedCountry, fieldName);
      });
    }

    document.addEventListener('DOMContentLoaded', function() {
      const smsPhoneFields = document.querySelectorAll('[id^="country-select-"]');
      
      smsPhoneFields.forEach(function(dropdown) {
        const fieldName = dropdown?.id.replace('country-select-', '');
        initializeSmsPhoneDropdown(fieldName);
      });
    });
    </script></div>

```

### Track B — AGENT tasks (theme codebase only)

1. Study the theme first. Map its design tokens, color schemes, typography, spacing, button/field
   classes, existing modal/drawer primitive, announcement/utility bar section, and JS/asset
   conventions (per the Agent styling brief, §3.0). Decide what to reuse vs build.
2. Create `snippets/alerts-signup.liquid` from §3.1: keep the behavior, wiring, `data-*` hooks,
   consent logic, and honeypot; restyle everything to the theme. Fill the `MC` config with the
   packet identifiers and honeypot name; set `status_if_new`/messaging to match the opt‑in choice.
   If the theme has its own dialog component, wrap the form in it and drop the placeholder modal.
3. Render it globally — `{% render 'alerts-signup' %}` before `</body>` in `layout/theme.liquid`
   (or the theme's equivalent global include).
4. Header trigger + message swap — add `sections/alerts-bar.liquid` (§3.3) styled like the theme's
   announcement bar with its color‑scheme pattern, or inject the trigger button + swap script
   into the theme's existing announcement bar. Ensure it emits/consumes `alerts:open` / `alerts:close`.
5. Footer — add the `<div data-alerts-footer>` mount in `sections/footer.liquid` where the merchant
   wants it; confirm the same form renders there.
6. Wire the chosen method(s): email via A (JSONP) or C (POST to the endpoint URL); phone via B
   (splice the merchant's generated SMS block, replacing the placeholder phone field + consent) or C.
   Never place an API key in theme code.
7. Polish to theme quality: responsive layout, focus trap + focus return, `Esc` to close,
   `prefers-reduced-motion`, proper labels/`aria`, sensible `z-index` above the header, clear
   error/success states on `.is-error` / `.is-success`.
8. QA against Part 5 on the Preview: real email; verify contact lands in the correct audience;
   confirm double‑opt‑in "check your inbox" message if applicable; no console/JS conflicts; honeypot
   name correct; phone path shows consent only when a number is entered.
9. Hand back with a short note: which theme components were reused vs added, which files changed,
   what settings are now exposed in the theme editor, and any follow‑ups (e.g. "SMS field is stubbed;
   enable once the program is approved and paste the generated block here").

### At‑a‑glance split

| Task | You (admin) | Agent (code) |
|---|---|---|
| Choose audience, opt‑in style, get `dc`/`u`/`id` + honeypot | ✅ | |
| Enable reCAPTCHA; connect native app | ✅ | |
| SMS program: apply, approve, credits, number, generate SMS block | ✅ | |
| Create API key + host endpoint (Method C) | ✅ | |
| Duplicate theme, grant access, provide test data, publish | ✅ | |
| Study theme design system & components | | ✅ |
| Build snippet/section/footer + restyle to theme | | ✅ |
| Wire chosen Mailchimp method(s) in code | | ✅ |
| Accessibility, responsive, QA on preview | | ✅ |

---

### Quick reference — where each piece lives

| Piece | File | Purpose |
|---|---|---|
| Modal + shared form + JS/CSS | `snippets/alerts-signup.liquid` | The reusable engine |
| Render site‑wide | `layout/theme.liquid` (before `</body>`) | Loads the engine on every page |
| Header bar + message swap | `sections/alerts-bar.liquid` | Trigger button + bar |
| Footer form mount | `sections/footer.liquid` | `<div data-alerts-footer>` |
| Server endpoint (optional) | your serverless / App Proxy | Marketing API, keeps key secret |
