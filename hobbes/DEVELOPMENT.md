# Development

The stack and the rules of the build. Hobbes reads this in full before touching code. Keep it true to the repo — if the build changes, this changes the same day.

## Stack

- **Platform:** Shopify, **Advanced plan** (not Plus — this gates features like Cart Transform Functions). Store `hazelboutiquenj.myshopify.com` → `hazelboutique.com`.
- **Framework & language:** Liquid + vanilla JavaScript (native Custom Elements / Web Components, no framework) + plain CSS. Fork of Shopify **Dawn v13.0.1**. No build toolchain — no npm, no bundler, no preprocessor.
- **Key integrations:** Judge.me (reviews), Instafeed (Instagram feed), DA Restock (back-in-stock), Route Insurance (shipping protection — flagged for removal), AccessEase (a11y audit, admin-only). Meta Pixel for purchase events (TikTok + Instagram). Cart is a **drawer** on the Shopify AJAX Cart API with a PubSub event bus (`assets/pubsub.js`).
- **Hosting / deploy:** Shopify-hosted. Source in this Git repo (`github.com/masonomara/hazel.git`); ships to the store theme via the Shopify CLI (bidirectional — admin/editor edits get pulled back down). Fonts and images on the store CDN (`cdn.shopify.com/s/files/1/0051/3264/8566/`).

## Build & run

- **Install:** Nothing to install for the theme itself. Requires the Shopify CLI: `npm i -g @shopify/cli @shopify/theme` (or `brew install shopify-cli`), then `shopify auth login`.
- **Run locally:** `shopify theme dev` — hot-reloading local preview bound to the live store's data.
- **Test:** None automated. Verify by hand in the browser (mobile + desktop) and via the web-baseline cycle (`/web-baseline`).
- **Lint / format:** `shopify theme check` (Theme Check). No `.theme-check.yml` committed, so it runs Shopify's default checks.
- **Deploy:** `shopify theme push` to a theme on the store. Push to an **unpublished / dev theme and preview first**; only Mason publishes the live theme, and never without sign-off. `config/settings_data.json` is admin-generated and the editor can overwrite it — coordinate so code pushes and editor edits do not clobber each other.

## Development rules

- **Branch + PR.** Feature branch (current: `embroidery`) → PR to `main`. `main` is the source of truth; do not commit nontrivial work straight to it.
- **Match Dawn and the surrounding file.** Custom Elements for JS behavior, the `properties[...]` line-item-property pattern for product-form data, CSS custom properties for design tokens. Custom Hazel CSS is appended after Dawn's base in `assets/base.css` (~line 3600+) — keep overrides there.
- **Do not hand-edit:** `config/settings_data.json` (admin-generated), anything under `.shopify/` (gitignored), or Dawn base styles in place — override in the appended Hazel section instead. Minimize core-theme edits: prefer a self-contained snippet rendered from one insertion point (the embroidery build holds to a single render line) to keep the fork upgrade-safe.
- **Secrets:** none in the repo. App and store credentials live in the Shopify admin and the CLI's own auth — never hard-code tokens, API keys, or app secrets. (The store id in CDN URLs is public and fine.)
- **Done means:** verified in the browser on mobile + desktop, no new console errors, Theme Check shows no new errors, and no regression against the web-baseline targets.
