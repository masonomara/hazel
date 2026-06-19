# Runner setup — once per client

One-time wiring to turn the Hobbes cycle into an automated cloud runner. Do this once per client repo. Both stages run from GitHub Actions — the deterministic patrol (`baseline → findings → diff`) and the Claude-Code execute stage — and **Hobbes writes only to GitHub**; every Shopify action stays human.

## 1. API keys — where each one goes

**Secrets never live in the repo.** `hobbes.toml` only *names* where to look (`psi_key_env`, `psi_key_file`); the actual values go in two places — GitHub for the cloud runner, a git-ignored file for local runs.

| Key | What it is | Where to get it | **Cloud** (GitHub) | **Local** |
|---|---|---|---|---|
| `PSI_API_KEY` | Google PageSpeed Insights API key | Google Cloud Console → enable the *PageSpeed Insights API* → Credentials → API key (restrict it to that API) | repo secret | `hobbes/tools/.psi-key` (git-ignored) |
| `ANTHROPIC_API_KEY` | Claude API key (drives the execute action) | console.anthropic.com → API keys | repo secret | not needed — local Claude Code uses your own login |

**Cloud:** repo → **Settings → Secrets and variables → Actions → New repository secret** → add both by the exact names above. The workflows inject them as env vars; `config.py` reads `$PSI_API_KEY` first, then the file.

**Local:** `echo 'YOUR_PSI_KEY' > hobbes/tools/.psi-key` (the file is git-ignored). Claude Code uses your existing local auth — no key file.

That's the whole secret surface: two keys, both GitHub-scoped. No Shopify credentials anywhere — Hobbes never touches Shopify.

## 2. Claude Code GitHub app

From Claude Code, run **`/install-github-app`** — it installs the GitHub app and wires the `ANTHROPIC_API_KEY` secret used by `.github/workflows/hobbes-execute.yml`.

## 3. Fix the branch-prefix collision (if present)

A branch literally named `hobbes` blocks the `hobbes/` prefix the cycle workflow uses for its PR branches (`hobbes/cycle-<date>`) and `branch_prefix` in `hobbes.toml`. Either delete it (`git push origin :hobbes`) or change the prefix to a non-colliding name.

## 4. Merge the workflows to the default branch

GitHub only runs `schedule` and `workflow_dispatch` workflows from the **default branch**. The workflow files must be on `main` before the patrol can fire.

## 5. First run

- **Actions → "Hobbes cycle" → Run workflow** (`workflow_dispatch`). Confirm: a green run, a "Baseline …" cycle PR, and the GitHub email.
- After that, the weekly cron keeps the patrol fresh. Run **"Hobbes execute"** (`workflow_dispatch`, with an effort budget) on demand for agent work — it opens a fix PR for review.

## Recurring vs one-time

| Step | Cadence |
|---|---|
| 1–4 above | **once** per client |
| Review + publish PRs | **every cycle** (the human gate) |
| Rotate a key | only on exposure |
