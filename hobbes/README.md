# Hobbes

A **web-baseline + agentic-fix system**: it measures a live site, catalogs what's wrong, plans the highest-leverage fixes, writes them as a pull request, and — once a human publishes — re-measures to prove the impact. It runs in GitHub Actions on a Claude Code subscription and **writes only to GitHub** (branches, PRs, comments); every deploy/go-live action stays human.

This folder is the system. Start here:

| Read | When |
|---|---|
| [`guides/SYSTEM.md`](guides/SYSTEM.md) | **The map** — the pipeline, how the data flows, every file's role, the design decisions. Read this to understand how Hobbes works. |
| [`guides/SETUP.md`](guides/SETUP.md) | **Stand it up** — per-client config + local and cloud wiring. Once per client. |
| [`guides/BASELINE.md`](guides/BASELINE.md) | **Run a cycle** — the tools, the run, the targets, the deliverables. Every cycle. |
| [`../CLAUDE.md`](../CLAUDE.md) | **Who Hobbes is** — identity, stance, and the hard line. Identical across all clients. |

**Standing context** (per-client, read on demand): [`context/MISSION.md`](context/MISSION.md) · [`context/DEVELOPMENT.md`](context/DEVELOPMENT.md) · [`context/CONTEXT.md`](context/CONTEXT.md) · [`context/CHANGELOG.md`](context/CHANGELOG.md). Config lives in [`hobbes.toml`](hobbes.toml).
