# Hobbes

Hobbes is a **web-baseline + agentic-fix system**: it measures a live site, catalogs what's wrong, plans the highest-leverage fixes, writes them as a pull request, and — once a human publishes — re-measures to prove the impact. It runs in GitHub Actions on a Claude Code subscription, and it **writes only to GitHub** (branches, PRs, comments). Every Shopify action — preview, publish, go-live — stays human.

This file is the map of the whole system. For *setup*, see [`SETUP.md`](SETUP.md). For *what Hobbes is and how it behaves*, see [`../CLAUDE.md`](../CLAUDE.md).

---

## The pipeline

Six stages, split across a hard **determinism boundary**: deterministic tools do the measuring and comparing; a Claude agent does the judgment (plan + fix); a human owns going live.

```
   DETERMINISTIC  (Python tools, no LLM — same input → same output)
   ┌─────────────────────────────────────────────┐
   │  baseline ──► findings ──► diff              │   ← cycle workflow (weekly + on-demand)
   └─────────────────────────────────────────────┘
                       │ findings.md
                       ▼
   JUDGMENT  (Claude agent, via claude-code-action)
   ┌─────────────────────────────────────────────┐
   │  plan ──► execute  ──►  fix PR               │   ← execute workflow (on-demand)
   └─────────────────────────────────────────────┘
                       │ you review + merge
                       ▼
   HUMAN
   ┌─────────────────────────────────────────────┐
   │  publish (Shopify go-live)  +  `published`   │   ← you, in Shopify, then a PR label
   └─────────────────────────────────────────────┘
                       │ label fires
                       ▼
   DETERMINISTIC
   ┌─────────────────────────────────────────────┐
   │  review = re-baseline ──► diff ──► PR comment│   ← review workflow (on the label)
   └─────────────────────────────────────────────┘
```

| Stage | Kind | Produces | Runs in |
|---|---|---|---|
| **baseline** | tool | `baseline.md` (+ raw/) — the scorecard | cycle workflow |
| **findings** | tool | `findings.md` — the problem catalog | cycle workflow |
| **diff** | tool | `diff.md` — cycle-over-cycle change | cycle + review workflows |
| **plan** | agent | `plan.md` — systems grouped, rated, ordered by leverage | execute workflow |
| **execute** | agent | `execution.md` + theme-code changes → a **fix PR** | execute workflow |
| **publish** | human | the change live on the store | you, in Shopify |
| **review** | tool | a **before/after comment** on the PR | review workflow (on `published`) |

**Why the boundary matters:** measurement must be reproducible (same raw → same findings, IDs and all), so it's deterministic and rebuilt every cycle. Fixing is judgment (what to group, what it costs, what it's worth, what the root cause is), so it's the agent's. Going live is irreversible and outward-facing, so it's the human's.

---

## Every file in the system

### Standing context — who Hobbes is and what it's steering by
*(Read by the agent; prose, not code.)*

| File | Role |
|---|---|
| [`../CLAUDE.md`](../CLAUDE.md) | Hobbes's identity, stance, and **the hard line** (never publish/merge/spend without sign-off). Identical across all clients. |
| [`context/MISSION.md`](context/MISSION.md) | What this client optimizes for, as **baseline → target** priorities (a11y, SEO, performance). Points at the scorecard for the numbers. |
| [`context/DEVELOPMENT.md`](context/DEVELOPMENT.md) | The stack and the build rules — the "done means" gates. |
| [`context/CONTEXT.md`](context/CONTEXT.md) | The client: goals, users, the people who sign off, where access lives. |
| [`context/CHANGELOG.md`](context/CHANGELOG.md) | What has shipped, why, and to what result. |
| [`context/BASELINE.md`](context/BASELINE.md) | The operator's runbook for driving a baseline cycle by hand. |

### Config — the one source of per-client truth
| File | Lines | Role |
|---|---|---|
| [`hobbes.toml`](hobbes.toml) | 22 | Per-client config: the golden path (home/collection/product URLs), where secrets live (names, not values), branch prefix, **timezone** (pins cycle dates), **effort_budget**. |

### The deterministic engine — `hobbes/tools/`
| File | Lines | Role |
|---|---|---|
| [`tools/config.py`](tools/config.py) | 70 | Single source loaded from `hobbes.toml`: `golden_path()`, `client_meta()`, `psi_key()` (env→file), `effort_budget()`, `today()`/`stamp()` (pinned-tz dates so local + CI never disagree). |
| [`tools/psi.py`](tools/psi.py) | 356 | PageSpeed Insights / Lighthouse capture → scorecard **§A–D** (lab perf/a11y/BP/SEO + CrUX field). Median-of-3, retry-resilient (survives PSI timeouts and truncated reads). |
| [`tools/seo.py`](tools/seo.py) | 315 | Per-page HTML SEO checklist → **§E** (titles, meta, canonical, OG, structured data). |
| [`tools/crawl.py`](tools/crawl.py) | 436 | SiteOne sitemap crawl (stratified sample) → **§F** site-wide SEO/a11y/security counts. |
| [`tools/baseline.py`](tools/baseline.py) | 131 | Orchestrates psi + seo + crawl into one dated cycle folder, then assembles `baseline.md` from `TEMPLATE.md`. Honors `--run-dir`. |
| [`tools/findings.py`](tools/findings.py) | 737 | The **problem catalog**: reads raw/ → `findings.md`, every issue with verbatim evidence + a static knowledge overlay (what it is, why it matters). Deterministic — fix/effort/impact are deliberately left to the plan. |
| [`tools/diff.py`](tools/diff.py) | 215 | Cycle-over-cycle diff, **honest by tier**: Field (CrUX, trustworthy) / Lab (§A, volatile) / **§D axe a11y** / §F counts (coverage-gated). `--prior` pins the comparison. |

### The CLI
| File | Lines | Role |
|---|---|---|
| [`cli.py`](cli.py) | 104 | `cycle` (baseline→findings→diff), the individual steps, `status`, `plan`/`execute` (print the stage prompt), `budget`, `today`. Run as `python3 hobbes/cli.py <cmd>`. |

### Stage contracts — `hobbes/templates/*.md`
| File | Role |
|---|---|
| [`templates/TEMPLATE.md`](templates/TEMPLATE.md) | The baseline scorecard shape — §A–G (A–F tool-filled, G manual a11y for the human). |
| [`templates/FINDINGS-TEMPLATE.md`](templates/FINDINGS-TEMPLATE.md) | The findings contract — dense, evidence-based, deterministic. |
| [`templates/PLAN-TEMPLATE.md`](templates/PLAN-TEMPLATE.md) | The plan contract — group findings into systems → estimate effort → estimate impact → **order by leverage (impact ÷ effort)**. |
| [`templates/EXECUTE-TEMPLATE.md`](templates/EXECUTE-TEMPLATE.md) | The execute contract — select a batch by effort budget, research, implement the **whole** batch, gates ("no *new* Theme Check offenses"), and the PR's before/after. Never publishes. |
| [`templates/PUBLISH-TEMPLATE.md`](templates/PUBLISH-TEMPLATE.md) | The publish contract — human-owned: PR review → sign-off → merge → go-live → `published` label → review. |

### The cloud runner — `.github/workflows/`
| File | Lines | Trigger | Role |
|---|---|---|---|
| [`../.github/workflows/hobbes-cycle.yml`](../.github/workflows/hobbes-cycle.yml) | 60 | cron (Mon 13:00 UTC) + dispatch | The deterministic patrol: `cli.py cycle` → opens a baseline **cycle PR**. No Claude. |
| [`../.github/workflows/hobbes-execute.yml`](../.github/workflows/hobbes-execute.yml) | 55 | dispatch (budget input) | The agent: `claude-code-action` (subscription auth) plans + writes fixes → opens a **fix PR**. |
| [`../.github/workflows/hobbes-review.yml`](../.github/workflows/hobbes-review.yml) | 84 | `published` label + dispatch (PR #) | Post-publish: re-baseline the **live** site, diff vs the pre-publish baseline, comment on the PR. No Claude. |

### Setup — `hobbes/SETUP.md`
| File | Role |
|---|---|
| [`SETUP.md`](SETUP.md) | **Setup, once per client** — local (Python + SiteOne + PSI key + first cycle) and cloud (two secrets, the Claude GitHub App, the "allow Actions to create PRs" toggle, the `published` label, workflows-on-default-branch), each annotated with the error it prevents. |

### Cycle data — `hobbes/scorecards/<YYYY-MM-DD>/`
Each cycle is a folder — the **filesystem is the state machine**. A folder accumulates: `baseline.md` → `findings.md` → `plan.md` → `execution.md` → `diff.md`, beside `raw/` (the `*.psi.json` / `*.seo.json` / `crawl.json` captures, git-ignored), `crawl.html`, and the per-tool digests (`psi-results.md`, `seo-results.md`, `crawl-results.md`). Which files exist tells you which stage the cycle reached (`cli.py status`).

---

## How it runs

**Cloud (the default).** All three workflows run from the **default branch** in GitHub Actions:
- **Measure:** Actions → *Hobbes cycle* → Run (or the Monday cron). → cycle PR.
- **Fix:** Actions → *Hobbes execute* → Run (blank budget = `hobbes.toml` default). → fix PR.
- **Verify:** add the **`published`** label to a merged fix PR (after you publish in Shopify). → before/after comment. Manual re-run: Actions → *Hobbes review* → Run → enter the PR number.

GitHub emails you when a PR opens or a comment posts — that's the notification; you don't watch anything.

**Local.** The deterministic half also runs on a laptop with Python 3.11+ and the SiteOne crawler: `python3 hobbes/cli.py cycle`. The agent half can run as local Claude Code instead of the cloud action (no secret needed — uses your login).

**The operator's weekly loop:** cycle runs Monday → baseline PR in your inbox · run execute when you want work → fix PR · review + merge → publish in Shopify → add `published` → the review posts the impact.

---

## Load-bearing design decisions

- **GitHub-only.** Hobbes touches nothing but GitHub. No Shopify CLI, no Shopify credentials. Going live is always a human in Shopify.
- **Claude Code, not the API.** The execute stage authenticates with a **Claude Code subscription token** (`claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN`), never a pay-per-token API key. The deterministic stages use no Claude at all.
- **The determinism boundary.** Tools measure and compare (reproducible); the agent judges and builds (creative); the human publishes (irreversible). Each thing lives where it belongs.
- **The diff doesn't lie.** It separates the trustworthy field signal from volatile lab noise, gates site-wide counts on crawl coverage (a collapsed crawl can't read as "improvement"), and surfaces the §D a11y findings the agent actually targets — distinguishing a real win from noise from an *unfulfilled claim*.
- **`published` is an explicit signal.** The review fires on a human-added label, not on merge — because "merged" doesn't mean "live," and every client's Shopify is wired differently.
- **Pinned-timezone dates.** Cycle folders are stamped in `[cycle].timezone`, so a local run and a UTC CI runner always land on the same calendar day.
- **Effort budget is a ceiling, not a quota.** Execute fills it with leverage-ordered work and won't shoehorn; a high budget only produces a big PR when there's that much worthwhile work queued.
