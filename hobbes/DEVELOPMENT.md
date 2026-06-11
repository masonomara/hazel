# Development

The stack and the rules of the build. Hobbes reads this in full before touching code. Keep it true to the repo — if the build changes, this changes the same day.

## Stack

- **Platform:** [Shopify / WooCommerce / Next / Nuxt / Remix / other]
- **Framework & language:** [e.g. Liquid + JS; React/TS; etc.]
- **Key integrations:** [payments, search, analytics, CRM, anything that shapes the code]
- **Hosting / deploy:** [where it runs, how it ships]

## Build & run

- **Install:** [exact command]
- **Run locally:** [exact command]
- **Test:** [exact command, or "none yet"]
- **Lint / format:** [exact command, or "none yet"]
- **Deploy:** [how a change reaches production, and who is allowed to trigger it]

## Development rules

- [Convention: branching, commits, PRs.]
- [Convention: code style, file layout, naming.]
- [Convention: what must never be edited directly — generated files, vendored code, locked theme sections.]
- [Convention: how secrets and env vars are handled. Never hard-code them.]
- [Convention: what counts as "done" — tests pass, baseline holds, no new regressions.]
