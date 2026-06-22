# Development

<!-- Human-owned. The stack and the rules of the build — kept true to the repo by a human, updated the same day the build changes. Hobbes reads it in full before touching code (the conventions and the "done means" gates) but never maintains it. -->

The stack and the rules of the build. Hobbes reads this in full before it touches code.

## Stack

- **Platform:** [Shopify / WooCommerce / Next / Nuxt / Remix / other]
- **Framework & language:** [e.g. Liquid + vanilla JS; React/TS; etc.]
- **Key integrations:** [payments, search, analytics, CRM — anything that shapes the code]
- **Hosting / deploy:** [where it runs, how it ships]

## Build & run

- **Install:** [exact command]. (Running the Hobbes baseline tools locally has its own prereqs — see `hobbes/SETUP.md`.)
- **Run locally:** [exact command]
- **Test:** [exact command, or "none — verify by hand + the Hobbes baseline cycle (`python3 hobbes/cli.py cycle`)"]
- **Lint / format:** [exact command, or "none yet"]
- **Deploy:** [how a change reaches production, and who may trigger it — only a human takes the live step]

## Development rules

- [Branching, commits, PRs — and that `main` is the source of truth.]
- [Code style, file layout, naming — match the surrounding file.]
- [What must never be edited directly — generated files, vendored code, locked theme sections.]
- [How secrets and env vars are handled. Never hard-code them.]
- **Done means:** [what counts as done — checker clean (no *new* offenses), verified by hand, no regression against the baseline targets in `hobbes/BASELINE.md`].
