# Runner setup — once per client

One-time wiring to turn the Hobbes cycle into an automated cloud runner. Do this once per client repo. Both stages run from GitHub Actions — the deterministic patrol (`baseline → findings → diff`) and the Claude-Code execute stage — and **Hobbes writes only to GitHub**; every Shopify action stays human.

## 1. API keys — where each one goes

**Secrets never live in the repo.** `hobbes.toml` only *names* where to look (`psi_key_env`, `psi_key_file`); the actual values go in two places — GitHub for the cloud runner, a git-ignored file for local runs.

| Key | What it is | Where to get it | **Cloud** (GitHub) | **Local** |
|---|---|---|---|---|
| `PSI_API_KEY` | Google PageSpeed Insights API key | Google Cloud Console → enable the *PageSpeed Insights API* → Credentials → API key (restrict it to that API) | repo secret | `hobbes/tools/.psi-key` (git-ignored) |
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code **subscription** token (Pro/Max) — drives the execute action. **Not** a pay-per-token API key | run **`claude setup-token`** locally and copy the token | repo secret | not needed — local Claude Code uses your own login |

**Cloud:** repo → **Settings → Secrets and variables → Actions → New repository secret** → add both by the exact names above. `PSI_API_KEY` is injected as an env var (`config.py` reads it first, then the file); `CLAUDE_CODE_OAUTH_TOKEN` is read by `claude-code-action`. A headless runner has no Claude login, so the execute stage needs this token stored as a secret — but it's your subscription, not the API.

**Local:** `echo 'YOUR_PSI_KEY' > hobbes/tools/.psi-key` (the file is git-ignored). Claude Code uses your existing local auth — no token needed locally.

That's the whole secret surface: two values, both GitHub-scoped. No Anthropic API key, no Shopify credentials anywhere — the deterministic stages (cycle, review) use no Claude at all; only `execute` does, via your Claude Code subscription.

## 2. Claude Code GitHub app

From Claude Code, run **`/install-github-app`** — it installs the GitHub app (repo permissions for the action). Auth itself is the `CLAUDE_CODE_OAUTH_TOKEN` secret from `claude setup-token` above, used by `.github/workflows/hobbes-execute.yml`.

## 3. Fix the branch-prefix collision (if present)

A branch literally named `hobbes` blocks the `hobbes/` prefix the cycle workflow uses for its PR branches (`hobbes/cycle-<date>`) and `branch_prefix` in `hobbes.toml`. Either delete it (`git push origin :hobbes`) or change the prefix to a non-colliding name.

## 4. Merge the workflows to the default branch

GitHub only runs `schedule` and `workflow_dispatch` workflows from the **default branch**. The workflow files must be on `main` before the patrol can fire.

## 5. The review trigger — the `published` label

The `review` phase (`hobbes-review.yml`) fires when you add a **`published`** label to a merged PR — your explicit "it's live now" signal, so the system never has to guess whether merge means live (it varies per client). Create the label once:

```
gh label create published --description "Theme is live — fire the Hobbes review" --color 0e8a16
```

Then the per-release flow is: merge the PR → publish the theme live in Shopify → **add `published` to the PR**. The review re-baselines the live site and comments the before/after. (Label it only *after* it's actually live, or you'll measure the old site.)

## 6. First run

- **Actions → "Hobbes cycle" → Run workflow** (`workflow_dispatch`). Confirm: a green run, a "Baseline …" cycle PR, and the GitHub email.
- After that, the weekly cron keeps the patrol fresh. Run **"Hobbes execute"** (`workflow_dispatch`, with an effort budget) on demand for agent work — it opens a fix PR for review.

## Recurring vs one-time

| Step | Cadence |
|---|---|
| 1–5 above | **once** per client |
| Add the `published` label after each go-live | **every release** (fires the review) |
| Review + publish PRs | **every cycle** (the human gate) |
| Rotate a key | only on exposure |
