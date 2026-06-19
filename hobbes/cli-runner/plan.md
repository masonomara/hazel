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

### 2b. Managed Agents — the Anthropic-hosted option (PARKED, not built)
Anthropic can host the whole agent loop: an **Agent** (system prompt + tools incl. the **GitHub MCP**), an **Environment**, and a **scheduled Deployment** (cron → one session per firing; `deployments.run()` is a manual button) that mounts the repo, runs the tools in `bash`, and opens a PR via the GitHub MCP. Lifecycle **webhooks** notify; credentials sit in a **vault** and never enter the container. It's a genuinely appealing fit — **but it is the Anthropic *API* surface, not Claude Code, and it's beta**, so it's deliberately out of the build (see §3 and Phase 6). Captured here only so we don't lose the thread. (`claude-api` skill: `shared/managed-agents-*.md`)

### 2c. SiteOne crawler in CI
Now rewritten in **Rust, zero runtime dependencies**, cross-platform Linux x64/arm64 release binaries on GitHub. A public Docker image is *planned, not yet shipped* — so in CI today we **download the Linux release binary** and put it on `PATH` (which is all `crawl.py` needs: `shutil.which("siteone-crawler")`). It also has a native CI quality-gate (`--ci-min-score`, exit 10) we don't need since `crawl.py` consumes the JSON. ([SiteOne releases](https://github.com/janreges/siteone-crawler/releases))

---

## 3. Architecture decision

**Build inward-out: local CLI substrate → GitHub Actions runner.** The answer to "MCP vs locally-downloadable" is: **locally-downloadable + configure-in-the-codebase is the MVP.**

**One hard rule: the build uses Claude Code exclusively.** The agent stages (plan/execute) run through `claude-code-action` in GitHub Actions — **no raw Anthropic API anywhere.** The deterministic stages are plain Python (no LLM at all). Managed Agents is the *API* surface, not Claude Code, so it is **parked, not built** (Phase 6).

```
  hobbes CLI (local, per-repo config)        ← the substrate. Same command the runner calls.
        │
        ├─ deterministic patrol  ─────────────→  GitHub Actions cron  (cheap, no LLM, weekly)
        │   baseline → findings → diff                 → opens "Cycle YYYY-MM-DD" PR (GitHub emails you)
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

**Managed Agents stays parked — but the door stays open.** It's appealing (Anthropic-hosted loop, scheduled deployments, GitHub-MCP PRs), but it's the API surface and it's beta, so it's not in the build. Nothing in Phases 0–5 blocks adopting it later: the same `hobbes` CLI, `hobbes.toml`, templates, and GitHub repo carry over unchanged (Phase 6).

**The cycle has never run end-to-end once** (execute/publish never fired). That gates heavy runner investment — Phase 1 (local CLI) must prove one full manual cycle before Phase 2/3 automate it.

---

## 4. How notifications work

**The PR is the notification, and GitHub email is the delivery.** No Slack, no webhook endpoint, no custom code — GitHub's built-in notifications are more than enough. The whole surface:

- **PR creation** → GitHub emails you (plus web + mobile-app notifications). The cycle PR ("Baseline 2026-XX-XX — 3 regressions") and the fix PR are the primary signal: open the email, read the diff, review.
- **PR / issue comments** — `claude-code-action` posts a progress/result comment; you're emailed on it.
- **Actions run status** — a failed scheduled run emails you (per your GitHub notification settings) and shows a red check in the Actions tab.
- **`$GITHUB_STEP_SUMMARY`** — the cycle writes `diff.md` here, so the run page shows the regressions / closed-findings table inline; the PR body carries it too.

That's it: **GitHub PRs + GitHub emails.** Zero extra secrets, zero extra services.

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

**`diff.py`** — the patrol's payoff, the tool we scoped two turns ago. Reads the two most-recent `baseline.md` scorecards and compares deterministically: section A scores, section C field, section F counts. Flags **regressions** (slipped vs prior — `BASELINE.md`'s own definition) and improvements, plus findings-count deltas by domain. Writes `diff.md` and prints a one-line summary for the PR title / step summary. It reads only the system's own artifacts, so it's codebase-agnostic.

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
      # GitHub emails you on PR creation — that's the notification (§4)
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
Nothing to wire. Have the cycle write `diff.md` into `$GITHUB_STEP_SUMMARY` and the PR body; GitHub emails do the rest (§4). No Slack, no third service.

### Phase 5 — Secrets (GitHub secrets, never the TOML)
**The call: secrets live in GitHub repo secrets, not in `hobbes.toml`.** `hobbes.toml` is committed, so it holds only the *name/location* of a secret (`psi_key_env = "PSI_API_KEY"`, `psi_key_file = "hobbes/tools/.psi-key"`), never a value. Actual values:
- **Cloud (GitHub Actions):** GitHub repo secrets — `PSI_API_KEY`, `ANTHROPIC_API_KEY` — injected as env vars. That's the whole set.
- **Local:** a gitignored `hobbes/tools/.psi-key` (already ignored) or a shell env var; Claude Code uses your existing local auth.

No Shopify credentials, no Slack, no other service. The merged PR is the entire handoff.

### Phase 6 (PARKED — explicitly *not* part of the Claude-Code-only build) — Managed Agents
A future option worth keeping on the table — but deliberately deferred, because it's a **different surface: the Anthropic API (hosted agent loop), not Claude Code.** Per the §3 "Claude Code only" rule, we don't build it now. **Parking it costs nothing — Phases 0–5 don't block it:** the same `hobbes` CLI, `hobbes.toml`, templates, and GitHub repo work unchanged whether the agent stages are driven by `claude-code-action` (now) or a Managed Agents scheduled deployment (later).

What it would add when/if adopted: Anthropic hosts the loop + a per-session container; a **scheduled deployment** (cron) fires a session per run with `deployments.run()` as the manual button; the session mounts the repo, runs the tools, opens a PR via the **GitHub MCP**; lifecycle **webhooks** + `deployment_runs` notify. **Is it safe?** The credential model is sound — vault tokens never enter the sandbox; a git proxy injects the GitHub token only after a request leaves the container. The real caveats: it's **beta**, Anthropic-hosted (not your CI), and the **API surface, not Claude Code** — which is exactly why it's parked. Revisit once the Claude-Code path is proven *and* Managed Agents is GA.

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

## 7. Todo — detailed task list

**Sequencing & gates.** Phases 0 → 1 are local and come first. **Phase 1 ends with a full real cycle that closes a finding — that gate must pass before Phases 2–3 automate anything.** Phases 2 and 3 are independent of each other once Phase 1 is done. Phase 6 is parked. Distribution (Phase 7) comes after Hazel runs green end-to-end.

### Phase 0 — Config extraction (prerequisite; local) — ✅ DONE
- [x] Confirm the toolchain: Python 3.14 locally (`tomllib` stdlib); recorded in `DEVELOPMENT.md`.
- [x] **Secret hygiene:** `.psi-key` was **tracked + in history** (commit `260cf2b`). Untracked (`git rm --cached`) + added to `.gitignore`. ⚠ **You must rotate the PSI key** — it's exposed in history.
- [x] Wrote `hobbes/hobbes.toml` (`[client]`/`[golden_path]`/`[secrets]`/`[cycle]`).
- [x] Added `hobbes/tools/config.py` (`cfg`, `golden_path`, `client_meta`, `psi_key`).
- [x] `psi.py`: `DEFAULT_URLS = golden_path()`; `load_key()` → `psi_key()`; removed now-unused `import os`.
- [x] `seo.py`: duplicate `DEFAULT_URLS` → `golden_path()`.
- [x] `baseline.py`: `CONFIG = client_meta()`; `CONFIG['client']` → `CONFIG['name']`. (`crawl.py` inherits via `from psi import DEFAULT_URLS` — confirmed.)
- [x] **Parity check:** all 6 tools `py_compile`; `DEFAULT_URLS`/`CONFIG` assert-equal to the originals; `findings.py` re-run on cached raw is **byte-identical** to the committed `2026-06-18`. (Full live `baseline --fresh` parity is left for the next real cycle — it would overwrite the gold standard and isn't needed to prove the wiring.)

### Phase 1 — CLI + cycle-diff + first real cycle (local) — ✅ code done · cycle running · gate ⛔ needs you
- [x] Invocation: `python3 hobbes/cli.py <cmd>` (script form, no package).
- [x] Wrote `hobbes/cli.py`: `cycle` · `baseline` · `findings` · `diff` · `status` · `plan`/`execute` stubs (print template + findings + the GitHub-only instruction). `status` verified.
- [x] Wrote `hobbes/tools/diff.py`:
  - [x] Locates the two most-recent cycle folders with a `baseline.md`.
  - [x] Parses §A scores + §F counts + the findings total. (§C field deferred — CrUX is 28-day, slow-moving; low value to diff.)
  - [x] Flags regressions (score slipped / count grew / more findings) and improvements.
  - [x] Writes `diff.md` + a one-line summary (PR title).
  - [x] First-cycle case **and** a non-comparable-prior guard (it caught the old `⚠`-label format silently reporting "0 changes" — fixed to say so honestly).
- [~] `python3 hobbes/cli.py cycle` end-to-end — **running now** (creates `2026-06-19/`), which also gives a real same-format second cycle to verify the live diff.
- [ ] ⛔ **GATE — one full real cycle** (execute a11y batch → PR → **human merges + publishes to Shopify** → re-baseline → confirm a finding closed). Blocked: the human publish is yours — I can't do it. Everything up to the PR is buildable (Phase 3).

### Phase 2 — Deterministic patrol in GitHub Actions — ✅ file written · secret + run ⛔ need you
- [ ] ⛔ Add repo secret `PSI_API_KEY` (GitHub UI — yours).
- [x] Wrote `.github/workflows/hobbes-cycle.yml`: `schedule` cron + `workflow_dispatch`; `contents`/`pull-requests: write`; `concurrency`; checkout → setup-python 3.12 → SiteOne binary → `cli.py cycle` (PSI key in `env`) → export `CYCLE_DATE`/`DIFF_SUMMARY` + `diff.md` → `$GITHUB_STEP_SUMMARY` → `create-pull-request`.
- [~] Pinned actions to majors (`@v4/@v5/@v6`); SiteOne uses `latest` with a comment to pin once the exact release-asset name is confirmed.
- [x] `crawl.py`'s `shutil.which("siteone-crawler")` finds it locally; the CI download step puts it on `PATH`. (Couldn't run CI to confirm there.)
- [ ] ⛔ Trigger `workflow_dispatch` once (needs the secret + merge to the default branch — yours).

### Phase 3 — Agent stages in GitHub Actions (Claude Code only) — ✅ file written · setup + run ⛔ need you
- [ ] ⛔ Run `/install-github-app` (installs the app + sets `ANTHROPIC_API_KEY`) — yours.
- [x] Wrote `.github/workflows/hobbes-execute.yml`: `workflow_dispatch` only + `budget` input; `contents`/`pull-requests: write`; `anthropics/claude-code-action@v1` with a prompt that follows the PLAN/EXECUTE templates, opens a PR, and **writes only to GitHub — no Shopify CLI, no publish.** (Confirm the action's exact input flag names against its docs.)
- [ ] ⛔ Dry-run on the a11y batch + review the PR (needs the app + CI — yours).

### Phase 4 — Notifications (GitHub-native only) — ✅ wired
- [x] `diff.md` → `$GITHUB_STEP_SUMMARY` + PR body (in `hobbes-cycle.yml`).
- [ ] ⛔ Confirm GitHub email arrives on the cycle / execute PRs (needs a real run — yours).
- [x] No Slack / webhook / third service — by design.

### Phase 5 — Secrets (GitHub, never the TOML) — ✅ done where I can · creation ⛔ yours
- [ ] ⛔ Add `PSI_API_KEY` + `ANTHROPIC_API_KEY` as GitHub repo secrets (yours).
- [x] `hobbes.toml` holds only secret *names/paths* (`psi_key_env`, `psi_key_file`), no values — confirmed.
- [x] `.psi-key` git-ignored + untracked; local runs use it / the env var. (⚠ rotate the key — it's in history.)

### Phase 6 — Managed Agents (PARKED — not built; door open)
- [x] Nothing built. Phases 0–5 are surface-agnostic (CLI / toml / templates / repo unchanged) — MA stays a drop-in.
- [ ] (later — only once the Claude-Code path is proven *and* MA is GA) author the agent + scheduled deployment.

### Phase 7 — Distribution (after Hazel runs green end-to-end) — gated, not started
- [ ] ⛔ Gated on the Phase 1 real-cycle gate (Hazel proving out end-to-end). The engine/instance line is drafted in §3; promotion to the stale `~/Documents/hobbes` seed + a second client repo wait until a cycle closes a finding for real.

### Cross-cutting / docs
- [x] `BASELINE.md` documents `hobbes/cli.py` (cycle/diff/status) + the `hobbes.toml`/`config.py` config; `DEVELOPMENT.md` notes Python ≥ 3.11.
- [ ] Update the stale seed `README.md` (Phase 7) and add a `CHANGELOG.md` line **when the runner actually ships** (merged + first green run) — not yet.

---

## Sources
- Claude Code GitHub Actions — https://code.claude.com/docs/en/github-actions · https://github.com/anthropics/claude-code-action
- SiteOne crawler releases — https://github.com/janreges/siteone-crawler/releases
- Managed Agents (scheduled deployments, webhooks, GitHub MCP, vaults) — `claude-api` skill: `shared/managed-agents-*.md`
