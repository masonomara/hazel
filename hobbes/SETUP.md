# Setup — once per client

How to stand Hobbes up. First fill the per-client config (`hobbes.toml`, below); then set up **local** (run the deterministic cycle on a laptop) and/or **cloud** (the automated GitHub runner). Local alone is enough to capture a baseline by hand; the cloud runner adds the weekly patrol and the agent fix-PR. Hobbes writes only to GitHub (branches, PRs, comments); every Shopify action stays human.

## Configure the client (`hobbes.toml`)

The per-client config every tool reads. Fill it once:

- **Identify the client.** Set the `[client]` block — name, site, platform, who runs it. (The fuller picture — goals, people, constraints — lives in `hobbes/context/CONTEXT.md`.)
- **Lock the golden path.** Pick 3–4 important pages with exact URLs — typically home, collection, product — and set them in `[golden_path]`. Reuse the same URLs every cycle so results stay comparable.
- **Method is PSI.** The cycle runs the PageSpeed Insights API the same way every cycle, so numbers stay comparable. Local Lighthouse is the fallback only for URLs PSI can't reach (theme draft, localhost, staging) — never mix PSI and local scores in one baseline. (Full method in `hobbes/BASELINE.md`.)

## Local setup — the engine on your machine

To run `python3 hobbes/cli.py cycle` (baseline → findings → diff) on a laptop:

- **Python ≥ 3.11** — stdlib only (`tomllib`); nothing to pip-install.
- **SiteOne crawler** on `PATH` — the whole-site crawl. macOS: `brew install janreges/tap/siteone-crawler` (or the desktop GUI app).
- **PSI key** — at `hobbes/tools/.psi-key` (git-ignored), or the `$PSI_API_KEY` env var. Get one: Google Cloud Console → enable *PageSpeed Insights API* → Credentials → API key.
- **First run:** `python3 hobbes/cli.py cycle` → a dated `hobbes/scorecards/<date>/` folder. `python3 hobbes/cli.py status` shows which stage it reached.

The agent stages (plan / execute) can run as local Claude Code instead of the cloud action — no secret needed; it uses your login.

## GitHub setup at a glance

Five one-time steps. Each prevents a real, specific failure — the right-hand column is the error you get if you skip it.

| # | Where | What | Error it prevents |
|---|---|---|---|
| 1 | Settings → Secrets and variables → Actions | Add secrets **`PSI_API_KEY`** + **`CLAUDE_CODE_OAUTH_TOKEN`** | PSI exits "No PSI key"; execute can't auth |
| 2 | github.com/apps/claude | **Install the Claude GitHub App** on this repo | `401 — Claude Code is not installed on this repository` |
| 3 | Settings → Actions → General → Workflow permissions | Check **"Allow GitHub Actions to create and approve pull requests"** | `GitHub Actions is not permitted to create or approve pull requests` |
| 4 | terminal | **`gh label create published`** | the `review` phase never fires |
| 5 | git | **Merge the workflow files to the default branch** | schedule / dispatch / label triggers never run |

Details below.

## 1. Two repo secrets

**Secrets never live in the repo.** `hobbes.toml` only *names* where to look; the values go in GitHub (cloud) and a git-ignored file (local).

| Secret | What it is | Where to get it | Cloud (GitHub) | Local |
|---|---|---|---|---|
| `PSI_API_KEY` | Google PageSpeed Insights key | Google Cloud Console → enable *PageSpeed Insights API* → Credentials → API key | repo secret | `hobbes/tools/.psi-key` (git-ignored) |
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code **subscription** token (Pro/Max) — drives `execute`. **Not** a pay-per-token API key | run **`claude setup-token`** locally, copy the token | repo secret | not needed (local Claude Code uses your login) |

**Settings → Secrets and variables → Actions → New repository secret**, add both by the exact names. A headless runner has no Claude login, so `execute` needs the subscription token stored as a secret — but it's your subscription, **never an Anthropic API key**. The deterministic stages (`cycle`, `review`) use no Claude at all — only PSI.

## 2. Install the Claude GitHub App  *(execute auth)*

`execute` runs `claude-code-action`, which authenticates its GitHub work by exchanging an **OIDC token** for the **Claude GitHub App's** token. The app must be installed on the repo or that exchange returns `401 — Claude Code is not installed on this repository`.

1. Open **https://github.com/apps/claude** → **Install** (or **Configure** if already on your account).
2. **Only select repositories** → tick **this repo** → **Install**.
3. Verify: **github.com/settings/installations** → **Claude** → Configure → the repo is in its list.

(`/install-github-app` from Claude Code does the same thing. The matching `id-token: write` permission is already in `hobbes-execute.yml` — no action needed.)

## 3. Let Actions open pull requests

Both `cycle` and `execute` open PRs with the built-in `GITHUB_TOKEN`, which a repo policy blocks by default.

**Settings → Actions → General → Workflow permissions** → check **"Allow GitHub Actions to create and approve pull requests"** → **Save.** (Leave the read/write radio as-is; the workflows declare their own `permissions:`.) Skip it and you get `GitHub Actions is not permitted to create or approve pull requests` *after* a full run — wasted minutes.

## 4. Create the `published` label

The `review` phase fires when you add a **`published`** label to a merged PR — your explicit "it's live now" signal (merge ≠ live, and it varies per client). Create it once:

```
gh label create published --description "Theme is live — fire the Hobbes review" --color 0e8a16
```

Per release: merge the fix PR → publish the theme live in Shopify → **add `published` to the PR**. The review re-baselines the **live** site and comments the before/after. Label it *only after* it's actually live, or you measure the old site.

## 5. Workflows on the default branch

GitHub runs `schedule` / `workflow_dispatch` workflows only from the **default branch** — merge the `.github/workflows/hobbes-*.yml` files to `main` before anything can fire.

> **Gotcha:** a `pull_request` event (the `published` label) runs the workflow **and tool code from that PR's own branch**, frozen at branch-creation. So fix the engine *before* opening a fix PR. If you patch the engine after a PR exists, re-run its review with the manual escape hatch: **Actions → "Hobbes review" → Run workflow**, input the PR number — that runs `main`'s current code.

## 6. First run

- **Actions → "Hobbes cycle" → Run workflow.** Confirm a green run, a "Baseline …" cycle PR, and the GitHub email. (Needs only step 1's `PSI_API_KEY` + step 3 + step 5 — no Claude.)
- Then **Actions → "Hobbes execute" → Run workflow** (blank budget = the `hobbes.toml` default) → a fix PR. (Needs steps 1, 2, 3, 5.)
- The weekly cron keeps the patrol fresh after that.

## Already wired in the workflow YAML — you don't touch these

The engine handles these; they're listed so you know they're covered:

- `permissions: contents/pull-requests/id-token: write` on each workflow.
- `execute`: `claude_args --allowedTools Edit,Read,Write,Glob,Grep,Bash` + `GH_TOKEN` (so the agent can edit, commit, and open the PR).
- SiteOne crawler install resolves the versioned release asset from the API (the asset name carries the version).

## Recurring vs one-time

| Step | Cadence |
|---|---|
| Client config + local + GitHub setup above | **once** per client |
| Add the `published` label after each go-live | **every release** (fires the review) |
| Review + publish PRs | **every cycle** (the human gate) |
| Rotate a key | only on exposure |
