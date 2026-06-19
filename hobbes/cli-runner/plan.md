# Plan — Hobbes CLI → Cloud Runner

Build the layer that turns the five hand-run Python tools + five stage templates into a **configurable, locally-installable CLI** that runs the Hobbes cycle on command, and a **cloud runner** that runs it automatically (weekly) and on a button-press, opening PRs for human review and pinging when something needs eyes.

Authored after reading the codebase in depth and researching the runner + notification surface (web + the `claude-api` skill). Code snippets are grounded in the actual tool interfaces.

---

## 1. The codebase as it stands (what we're building on)

Verified by reading the source this session:

- **Five tools, all pure Python stdlib** (`json`, `urllib`, `http.server`, `subprocess`, `concurrent.futures`, `pathlib` …). **No pip dependencies** — this massively simplifies CI (no `requirements.txt`, no venv resolution).
- **The cycle is a filesystem state machine.** Every stage reads the prior artifact and writes its own into `hobbes/scorecards/<YYYY-MM-DD>/`:
  `baseline.md` → `findings.md` → `plan.md` → `execution.md` → (publish). `findings.py` already auto-discovers the newest cycle folder (`latest_run_dir()`). An orchestrator never holds state — it reads the folder and knows the stage.
- **Tool interfaces (stable, already CLI-shaped):** every tool takes `--run-dir DIR` and writes there; `baseline.py` threads `--run-dir` + `--fresh`/`--resume`/`--no-crawl`/`--full` into `psi.py` → `seo.py` → `crawl.py`.
- **The two deterministic boundaries that block multi-site / cloud — hardcoded config:**
  - `psi.py` → `DEFAULT_URLS` (the golden path) + reads `$PSI_API_KEY` or `hobbes/tools/.psi-key`.
  - `seo.py` → its **own** duplicate `DEFAULT_URLS`.
  - `crawl.py` → imports `DEFAULT_URLS` from `psi.py`; **requires the `siteone-crawler` binary on `PATH`** (`brew install` locally; in CI it's a release-binary download — SiteOne is now Rust, zero runtime deps).
  - `baseline.py` → `CONFIG = {client, site, platform, run_by}`.
- **Stages & ownership** (from the templates): baseline/findings = deterministic tools; plan/execute = agent (judgment); **publish = human-gated** (only Mason publishes the live theme — the hard line).
- **Stack constraints** (`DEVELOPMENT.md`): Shopify Advanced, Liquid + vanilla JS, **no build toolchain**, manual browser verify; Theme Check (a local Liquid linter) and the live publish are the **human's**. **Hobbes itself writes only to GitHub** — it never deploys to, authenticates against, or runs a CLI for Shopify.

**Implication:** the deterministic half (baseline/findings/diff) is cheap, network-only, LLM-free, and trivially CI-able once config is extracted. The agent half (plan/execute) needs an LLM + repo write. Publish stays human. That split drives the whole architecture.

---

## 2. Research summary

### 2a. Claude Code in CI — the agent half
`anthropics/claude-code-action@v1` is GA. It supports (a) `@claude` mentions in PRs/issues, (b) auto-run on PR events, and **(c) scheduled automation via `cron` triggers** — the documented use case is "weekly maintenance." Headless Claude Code (`claude -p "<prompt>"`) runs non-interactively for exactly this. Setup via `/install-github-app`. So the plan/execute stages can run in GitHub Actions: read `findings.md` + `PLAN-TEMPLATE.md`/`EXECUTE-TEMPLATE.md`, do the work, open a PR. ([Claude Code GitHub Actions docs](https://code.claude.com/docs/en/github-actions), [claude-code-action](https://github.com/anthropics/claude-code-action))

### 2b. Managed Agents + Scheduled Deployments — the Anthropic-hosted alternative
Anthropic hosts the agent loop and a per-session container. You create an **Agent** (model + system prompt + tools incl. the **GitHub MCP** for PR creation), an **Environment**, and a **scheduled Deployment** (cron → one session per firing; `deployments.run()` = a manual "button" that works even while paused). The session **mounts the client's GitHub repo**, runs the Python tools via `bash` in the container, pushes a branch, opens a PR via the GitHub MCP `create_pull_request` tool. Credentials live in a **vault** (PSI key as an `environment_variable` credential substituted at egress; GitHub MCP OAuth). It's **beta**. (`claude-api` skill: `shared/managed-agents-scheduled-deployments.md`, `…-environments.md`, `…-tools.md`)

### 2c. Notifications — Managed Agents webhooks
Anthropic POSTs **HMAC-signed** thin events to an HTTPS endpoint you register in Console: `session.status_run_started`, `session.status_idled`, `session.status_terminated`, `session.outcome_evaluation_ended`, `vault_credential.refresh_failed`. Verify with `client.beta.webhooks.unwrap()` (reads `ANTHROPIC_WEBHOOK_SIGNING_KEY`); dedupe on `event.id`; auto-disables after ~20 failed deliveries. Each scheduled/manual firing also writes a `deployment_run` record (success → `session_id`; failure → `error.type`) you can poll with `has_error=true`. (`claude-api` skill: `shared/managed-agents-webhooks.md`)

### 2d. SiteOne crawler in CI
Now rewritten in **Rust, zero runtime dependencies**, cross-platform Linux x64/arm64 release binaries on GitHub. A public Docker image is *planned, not yet shipped* — so in CI today we **download the Linux release binary** and put it on `PATH` (which is all `crawl.py` needs: `shutil.which("siteone-crawler")`). It also has a native CI quality-gate (`--ci-min-score`, exit 10) we don't need since `crawl.py` consumes the JSON. ([SiteOne releases](https://github.com/janreges/siteone-crawler/releases))

---

## 3. Architecture decision

**Build inward-out, exactly as scoped earlier: local CLI substrate → GitHub Actions runner → (optional) Managed Agents.** The answer to "MCP vs locally-downloadable" is: **locally-downloadable + configure-in-the-codebase is the MVP**; Managed Agents/MCP is the graduate path.

```
  hobbes CLI (local, per-repo config)        ← the substrate. Same command the runner calls.
        │
        ├─ deterministic patrol  ─────────────→  GitHub Actions cron  (cheap, no LLM, weekly)
        │   baseline → findings → diff                 → opens "Cycle YYYY-MM-DD" PR + Slack ping
        │
        ├─ agent work loop  ──────────────────→  Claude Code Action  (workflow_dispatch / @claude / chained)
        │   plan → execute                             → opens fix-branch PR for review
        │
        └─ publish  ──────────────────────────→  HUMAN, OUTSIDE HOBBES  (Hobbes ends at the merged PR; the human takes the change to Shopify themselves)
```

**Why GitHub Actions as the primary runner, not Managed Agents:**
- It lives **in the client repo** — matches the plop-in distribution model (each client repo = the engine + filled instance + one workflow file). Per-site config for free.
- The deterministic half is **pennies** (pure stdlib Python + a binary download, no LLM) and read-only — safe to run unattended weekly.
- Native PRs, native GitHub notifications, full filesystem control, you own the runner. Multi-site = the same workflow in N repos (or a matrix).
- The same `hobbes` CLI runs whether you type it locally or a cron calls it — **local-first gives remote-for-free.**

**When to graduate to Managed Agents:** if you want Anthropic to host the loop, richer lifecycle webhooks, and the GitHub-MCP PR flow without maintaining CI — and you've accepted beta. Documented in Phase 6, not built first.

**The cycle has never run end-to-end once** (execute/publish never fired). That gates heavy runner investment — Phase 1 (local CLI) must prove one full manual cycle before Phase 2/3 automate it.

---

## 4. How notifications work (the deep dive)

The mental model: **the PR is the notification.** Everything else is a thin "go look" ping. Three layers, cheapest first:

**Layer 1 — GitHub-native (free, zero custom code).**
- **PR creation** → GitHub emails/pushes reviewers (web, email, mobile app). The cycle PR ("Baseline 2026-XX-XX: 3 regressions") and the fix PR are the primary signal.
- **PR/issue comments** — `claude-code-action` posts a progress/result comment you get notified on.
- **Actions run status** — failure emails (per your notification settings), the commit status check, the Actions tab.
- **`$GITHUB_STEP_SUMMARY`** — write markdown to this file and it renders as a rich summary on the run page (e.g. paste the diff table there).
- **Slack GitHub app** — subscribe a channel to the repo's PRs/Actions; zero code.

**Layer 2 — Slack incoming webhook (proactive "cycle done / regression" ping).** One secret (`SLACK_WEBHOOK_URL`), a `curl` step. This is the "tell me in Slack when a baseline finishes or a target regressed" channel:
```yaml
- name: Notify Slack
  if: always()
  run: |
    curl -fsS -X POST -H 'Content-type: application/json' "$SLACK_WEBHOOK_URL" \
      --data "{\"text\": \"Hobbes cycle for *${{ env.CLIENT }}* — ${{ job.status }}. ${{ env.DIFF_SUMMARY }}\nPR: ${{ env.PR_URL }}\"}"
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```
(or `slackapi/slack-github-action` for richer Block Kit.)

**Layer 3 — Managed Agents webhooks (only if you go Phase 6).** Anthropic HMAC-signs `session.status_idled` / `…_terminated` / `…_run_started` to your HTTPS endpoint; you `unwrap()` → verify → fetch session → forward to Slack/email. Plus `deployment_runs.list(has_error=true)` to catch scheduled-run failures (`environment_archived`, `vault_not_found`, …).

**Recommended notification set for the MVP:** PR (Layer 1) + one Slack webhook (Layer 2). That covers "a cycle finished, here's what changed, here's the PR" and "the run failed." Add Layer 3 only with Managed Agents.

---

## 5. The build — phases with code

### Phase 0 — Per-repo config (the prerequisite)

One `hobbes.toml` at the repo's hobbes root, replacing every hardcoded constant. Engine reads it; instance fills it.

```toml
# hobbes/hobbes.toml
[client]
name     = "Hazel Boutique"
site     = "https://hazelboutique.com"
platform = "Shopify Advanced"
run_by   = "Mason"

[golden_path]            # was psi.py DEFAULT_URLS + seo.py DEFAULT_URLS (duplicated)
home       = "https://hazelboutique.com/"
collection = "https://hazelboutique.com/collections/all-hazel-brand"
product    = "https://hazelboutique.com/products/the-capri-collection-baby-pink"

[secrets]
psi_key_env  = "PSI_API_KEY"            # env var first; falls back to the path below
psi_key_file = "hobbes/tools/.psi-key"  # a path, never the secret

[cycle]
branch_prefix = "hobbes/"
effort_budget = 10                       # the execute-stage selection dial
```

A tiny loader all tools import (stdlib `tomllib`, Python 3.11+):
```python
# hobbes/tools/config.py
import tomllib, functools
from pathlib import Path
HOBBES = Path(__file__).resolve().parent.parent

@functools.lru_cache
def cfg():
    return tomllib.loads((HOBBES / "hobbes.toml").read_text())

def golden_path():
    g = cfg()["golden_path"]
    return [("Home", g["home"]), ("Collection", g["collection"]), ("Product", g["product"])]
```
Then `psi.py` / `seo.py`: `from config import golden_path; DEFAULT_URLS = golden_path()`. `baseline.py`: `CONFIG = cfg()["client"]`. **This unifies the two duplicate `DEFAULT_URLS` lists — a real bug-vector removed.**

### Phase 1 — The `hobbes` CLI + `diff.py`

A thin dispatcher (stdlib `argparse`) over the tools + the state machine. `hobbes/cli.py`:
```python
# usage: python -m hobbes.cli <command>
#   cycle      baseline + findings + diff      ← the deterministic patrol (weekly button)
#   baseline / findings / diff                 ← individual deterministic steps
#   status     read newest scorecards/<date>/, print which stage it's at
#   plan / execute   ← spawn the agent (Phase 3); locally just print the prompt + inputs
import subprocess, sys
from pathlib import Path
from datetime import date
TOOLS = Path(__file__).resolve().parent / "tools"

def run(tool, *args): subprocess.run([sys.executable, str(TOOLS / tool), *args], check=True)

def cmd_cycle(args):
    rundir = TOOLS.parent / "scorecards" / date.today().isoformat()
    run("baseline.py", "--fresh", "--run-dir", str(rundir))   # baseline.py threads to psi/seo/crawl
    run("findings.py", "--run-dir", str(rundir))
    run("diff.py", "--run-dir", str(rundir))                   # vs the previous cycle folder
```

**`diff.py`** — the patrol's payoff, the tool we scoped two turns ago. Reads the two most-recent `baseline.md` scorecards and compares deterministically: section A scores, section C field, section F counts. Flags **regressions** (slipped vs prior — `BASELINE.md`'s own definition) and improvements, plus findings-count deltas by domain. Writes `diff.md` and prints a one-line summary for the Slack ping / PR title. It reads only the system's own artifacts, so it's codebase-agnostic.

### Phase 2 — GitHub Actions deterministic patrol

`.github/workflows/hobbes-cycle.yml`:
```yaml
name: Hobbes cycle
on:
  schedule: [{ cron: "0 13 * * 1" }]      # Mondays 13:00 UTC
  workflow_dispatch:                       # the manual "button"
jobs:
  patrol:
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - name: Install SiteOne crawler        # Rust binary, zero deps
        run: |
          curl -fsSL -o /tmp/siteone.tar.gz \
            https://github.com/janreges/siteone-crawler/releases/latest/download/siteone-crawler-linux-x64.tar.gz
          sudo tar -xzf /tmp/siteone.tar.gz -C /usr/local/bin siteone-crawler
      - name: Run cycle                      # pure stdlib — no pip install
        env: { PSI_API_KEY: ${{ secrets.PSI_API_KEY }} }
        run: python -m hobbes.cli cycle
      - name: Open cycle PR
        uses: peter-evans/create-pull-request@v6
        with:
          branch: hobbes/cycle-${{ github.run_id }}
          title: "Baseline ${{ env.CYCLE_DATE }} — ${{ env.DIFF_SUMMARY }}"
          body-path: hobbes/scorecards/${{ env.CYCLE_DATE }}/diff.md
      # + the Slack notify step from §4
```
The PR carries the new scorecard + `diff.md`; merging it records the cycle in git. If `diff.md` shows regressions or new findings, that's the cue to run the agent loop.

### Phase 3 — Agent stages in CI (plan/execute)

A separate, **manually/comment-triggered** workflow (not auto — it writes code) using `claude-code-action`:
```yaml
name: Hobbes execute
on:
  workflow_dispatch: { inputs: { budget: { default: "10" } } }
jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Run the Hobbes plan + execute stages on the latest cycle.
            Read hobbes/scorecards/PLAN-TEMPLATE.md and EXECUTE-TEMPLATE.md and follow them.
            Effort budget: ${{ inputs.budget }}. Open a PR for review. Do NOT publish.
```
Claude Code reads `findings.md` + the templates, writes `plan.md`/`execution.md`, makes the theme-code changes on a branch, and **opens a PR. Its only write target is GitHub** — it runs no Shopify CLI and never publishes. Verification (Theme Check, browser — per `DEVELOPMENT.md`) and the live publish are the human's, at PR review and beyond, entirely outside the runner.

### Phase 4 — Notifications
Wire the Slack webhook (§4 Layer 2) into both workflows; rely on PRs + GitHub for Layer 1. One secret: `SLACK_WEBHOOK_URL`.

### Phase 5 — Secrets
GH repo secrets, all GitHub-scoped: `PSI_API_KEY` (a read-only Google PageSpeed key, not Shopify), `ANTHROPIC_API_KEY`, `SLACK_WEBHOOK_URL`. **No Shopify credentials anywhere** — Hobbes never authenticates against or deploys to Shopify. The merged PR is the entire handoff; the human takes it to Shopify on their own, outside the system.

### Phase 6 (optional, later) — Managed Agents path
Define the Hobbes agent (system = identity + stage prompts; tools = `agent_toolset_20260401` + GitHub MCP) and a **scheduled deployment** (cron). `deployments.run()` is the remote button; webhooks (§4 Layer 3) are the notifications. Build only after Phases 1–3 prove out and if you want Anthropic to host the loop.

---

## 6. Risks / walls (carried from the earlier analysis, now with mitigations)

| Wall | Severity | Mitigation |
|---|---|---|
| Config still hardcoded (2 duplicate `DEFAULT_URLS`) | low, must-do | Phase 0 `hobbes.toml` + `config.py` |
| Agent stages unattended (reliability/cost/off-rails) | high | Keep plan/execute **manual-trigger only**; PR-gated; budget cap; never auto-fire across sites |
| Hobbes touching Shopify | n/a by design | Hobbes only writes to GitHub (branches/PRs). All Shopify work — preview, verify, publish — is the human's, outside the system. No Shopify CLI, no Shopify secrets |
| SiteOne binary in CI (no Docker image yet) | low | Download the Rust release binary to `PATH` (Phase 2) |
| Cycle collision (weekly fires while last PR open) | medium | Date-stamped branches + `create-pull-request` upserts; one open cycle PR at a time |
| Cost ×6 sites ×weekly | medium | Deterministic patrol is ~free; gate the agent stages behind human trigger |
| Cross-cycle finding-ID drift in `diff.py` | medium | Diff `baseline.md` numbers (positional, stable) for regressions; findings by domain count, not ID |

---

## 7. Todo

### Phase 0 — Config (prerequisite)
- [ ] Write `hobbes/hobbes.toml` for Hazel (client, golden_path, secrets, cycle).
- [ ] Add `hobbes/tools/config.py` (`tomllib` loader, `cfg()`, `golden_path()`).
- [ ] Repoint `psi.py` `DEFAULT_URLS` → `golden_path()`; read key via `cfg()["secrets"]`.
- [ ] Repoint `seo.py` `DEFAULT_URLS` → `golden_path()` (kill the duplicate list).
- [ ] Repoint `baseline.py` `CONFIG` → `cfg()["client"]`.
- [ ] Run a full local baseline+findings to confirm config parity (numbers unchanged).

### Phase 1 — CLI + diff + first real cycle
- [ ] Write `hobbes/cli.py` (`cycle`, `baseline`, `findings`, `diff`, `status`).
- [ ] Write `hobbes/tools/diff.py` (compare two `baseline.md`s → regressions/improvements + findings-count deltas → `diff.md` + one-line summary).
- [ ] `python -m hobbes.cli cycle` locally end-to-end; confirm `diff.md`.
- [ ] **Run one full real cycle** (execute the a11y batch → open the PR → human merges + publishes to Shopify outside Hobbes → re-baseline → confirm a finding closed). *Gates Phase 2/3.*

### Phase 2 — Deterministic patrol in CI
- [ ] `.github/workflows/hobbes-cycle.yml` (cron + `workflow_dispatch`).
- [ ] SiteOne binary download step; verify `crawl.py` finds it.
- [ ] `PSI_API_KEY` secret; confirm a green scheduled run.
- [ ] Cycle-PR step (`peter-evans/create-pull-request`) with `diff.md` as the body.

### Phase 3 — Agent stages in CI
- [ ] `.github/workflows/hobbes-execute.yml` (`workflow_dispatch`, budget input).
- [ ] `/install-github-app`; `ANTHROPIC_API_KEY` secret.
- [ ] Prompt wires `PLAN-TEMPLATE.md` + `EXECUTE-TEMPLATE.md`; assert it opens a PR and never publishes.
- [ ] Dry-run on the a11y batch; review the PR.

### Phase 4–5 — Notifications + secrets
- [ ] `SLACK_WEBHOOK_URL` secret + notify step in both workflows.
- [ ] `$GITHUB_STEP_SUMMARY` ← `diff.md`.

### Phase 6 — Managed Agents (optional, later)
- [ ] Author the Hobbes agent YAML (system + GitHub MCP) and a scheduled deployment.
- [ ] Webhook endpoint (`unwrap()` verify → Slack); `deployment_runs` failure poll.

### Distribution (after Hazel proves out)
- [ ] Extract engine (`tools/`, templates, `cli.py`, workflows) from instance (`hobbes.toml`, MISSION/DEV/CONTEXT, scorecards); pick submodule vs installer.
- [ ] Drop the engine + workflow into a second client repo; fill its `hobbes.toml`; confirm a green cycle.

---

## Sources
- Claude Code GitHub Actions — https://code.claude.com/docs/en/github-actions · https://github.com/anthropics/claude-code-action
- SiteOne crawler releases — https://github.com/janreges/siteone-crawler/releases
- Managed Agents (scheduled deployments, webhooks, GitHub MCP, vaults) — `claude-api` skill: `shared/managed-agents-*.md`
