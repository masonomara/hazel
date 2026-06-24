# Hobbes

Hobbes is a **web-baseline + agentic-fix system**: it measures a live site, catalogs what's wrong, plans the highest-leverage fixes, writes them as a pull request, and — once a human publishes — re-measures to prove the impact. It runs in GitHub Actions on a Claude Code subscription, and it **writes only to GitHub** (branches, PRs, comments). Every Shopify action — preview, publish, go-live — stays human.

This file is the map of the whole system. For *setup*, see [`SETUP.md`](SETUP.md). For *what Hobbes is and how it behaves*, see [`../CLAUDE.md`](../CLAUDE.md).

---

## The pipeline

Six stages, split across a hard **determinism boundary**: deterministic tools do the measuring and comparing; a Claude agent does the judgment (plan + fix); a human owns going live.

```
   ON-DEMAND — one trigger fires measure + fix together, into ONE PR
   (Actions → "Hobbes cycle"; or `python3 hobbes/cli.py cycle` locally for the data alone)
   ┌────────────────────────────────────────────────────────────────┐
   │  DETERMINISTIC (Python, no LLM)   │   JUDGMENT (Claude agent)    │
   │  baseline ─► findings             │   plan ─► execute            │
   └────────────────────────────────────────────────────────────────┘
                       │ ONE PR: scorecard + findings + the code fix
                       ▼ you review + merge
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
| **baseline** | tool | `01-baseline.md` (+ raw/) — the scorecard | cycle workflow |
| **findings** | tool | `02-evaluation.md` — the problem catalog | cycle workflow |
| **plan** | agent | `plan.md` — systems grouped, rated, ordered by leverage | cycle workflow |
| **execute** | agent | `execution.md` + theme-code changes | cycle workflow |
| **publish** | human | the change live on the store | you, in Shopify |
| **review** | tool (`diff.py`) | a **before/after comment** on the PR | review workflow (on `published`) |

> The first four stages (baseline, findings, plan, execute) run in **one** `Hobbes cycle` workflow and land in **one PR** — the scorecard/findings (data) beside the theme-code fix. The determinism boundary still holds inside that run: the Python tools measure first (reproducibly, no LLM), then the agent judges and fixes. **There is no diff in a cycle** — a cycle measures the current site and has no "after" to compare (this cycle's fix isn't live yet). The before/after is the **review** stage's job, after a publish.

**Why the boundary matters:** measurement must be reproducible (same raw → same findings, IDs and all), so it's deterministic and rebuilt every cycle. Fixing is judgment (what to group, what it costs, what it's worth, what the root cause is), so it's the agent's. Going live is irreversible and outward-facing, so it's the human's.

---

## Follow the data — what reads what, and who emits the content

The stage table above says *what each stage produces*. This is the other axis — the one that's easy to lose: **what each file reads, what it writes, and who consumes that next.** Follow one cycle's data from the live site all the way to the PR comment.

```
  LIVE SITE  (hazelboutique.com — the only source of truth for numbers)
     │
     │  ── CAPTURE: three tools hit the site. Each writes a raw artifact and PRINTS its sections ──
     ├─ psi.py    ─►  raw/*.psi.json     (prints §A–D)
     ├─ seo.py    ─►  raw/*.seo.json     (prints §E)
     └─ crawl.py  ─►  raw/crawl.json     (prints §F + per-URL detail)
                          │                         │
                          │   baseline.py CAPTURES the three tools' stdout ──►  01-baseline.md
                          │   (§A–F sliced from their printed sections + §G from TEMPLATE.md — the ONE digest)
                          │                                                       │
   the RAW artifacts ─────┴──────────────────────►  findings.py  ──►  02-evaluation.md   (the problem catalog)
                                                                                  │   (no diff in a cycle)
     │  ── JUDGMENT: the agent reads the catalog (never the raw) and works against the real code ──
                            02-evaluation.md + MISSION.md ─────────────►  [agent · PLAN-TEMPLATE]  ──►  plan.md
            plan.md + 02-evaluation.md + 01-baseline.md + the theme source ───►  [agent · EXECUTE-TEMPLATE] ─►  execution.md + theme code + PR body
                                                                                  │
                                              ONE PR  ──►  human review + merge  ──►  publish in Shopify  ──►  add `published` label
                                                                                  │
     │  ── VERIFY: the same three tools re-run on the now-LIVE site, then diff'd ──
                          baseline.py ─► findings.py ─► diff.py  ──►  diff.md  ──►  gh pr comment  (the before/after)
```

**Five handoffs worth understanding — this is the "what each file does along the way":**

1. **Two readers, two different diets — one source, no middle file.** Each tool *prints* its rendered sections to stdout and writes its raw JSON to `raw/`. `baseline.py` runs the three as subprocesses and **captures their stdout**, slicing §A–F straight from the printed sections — there is no per-tool `*-results.md` on disk. `findings.py` eats the **raw** artifacts (`raw/*.psi.json`, `raw/crawl.json`) *directly*. `raw/` is git-ignored. This is why `02-evaluation.md` can't be rebuilt from `01-baseline.md`: the catalog needs node-level evidence the scorecard's summary tables threw away.
2. **The catalog can't drift from the scorecard.** `findings.py` doesn't re-implement parsing — it *imports* the same extractors from `psi.py` / `seo.py` / `crawl.py` that produced the numbers. One parser, two outputs, so a finding and its scorecard row can never disagree.
3. **`diff.py` runs only in the review phase — never in a cycle.** A cycle measures the current site; it has no "after" to compare (this cycle's fix isn't even live yet). So the diff lives entirely in the post-publish **review**: it reads two `01-baseline.md` files — the pre-publish baseline and the re-baselined live site — re-parses their tables back into numbers, and compares them tier by tier (field / lab / axe / counts). It touches no raw and only a findings *count*. (This is also where the **28-day CrUX field** impact of a fix finally shows — the review fires too soon after publish for field to move, so it's the *next* review/cycle that confirms it.)
4. **The agent reads `02-evaluation.md`, never `raw/`.** Judgment works off the catalog — an already-fixed, deterministic list of problems — not the megabytes of Lighthouse JSON. The templates (`PLAN`, `EXECUTE`) are the skeleton it must fill; the codebase is what it reads to write the actual fix.
5. **The capture tools run in both phases; the diff doesn't.** `baseline.py` + `findings.py` (driving psi/seo/crawl) run in the cycle (pre-fix) **and** in the review (post-publish, on the now-live site). `diff.py` is the one piece that's review-only — the review re-baselines the live site, rebuilds findings, then diffs against the pre-publish baseline, and that diff *is* the PR comment.

**The determinism boundary, restated as authorship:** every **number** and every **comparison** in this flow is emitted by Python (`baseline.py`, `findings.py`, `diff.py`) — reproducible, unspinnable. Only the **fix narrative and the PR prose** are the agent's, and even those ride a fixed template skeleton. The PR comment (`diff.md`) is 100% Python; the PR body is agent prose constrained by `EXECUTE-TEMPLATE.md`.

### Reads → writes → consumed by

| File | Reads | Writes | Consumed by |
|---|---|---|---|
| `psi.py` | live site (PSI API) | `raw/*.psi.json` + prints §A–D | `baseline.py` (stdout), `findings.py` (raw) |
| `seo.py` | live site (HTML) | `raw/*.seo.json` + prints §E | `baseline.py` (stdout), `findings.py` (raw) |
| `crawl.py` | live site (sitemap crawl) | `raw/crawl.json` + prints §F | `baseline.py` (stdout), `findings.py` (raw) |
| `baseline.py` | the three tools' stdout + `TEMPLATE.md` | `01-baseline.md` (the one digest) | the agent, the human, `diff.py` (review only) |
| `findings.py` | `raw/*.psi.json`, `raw/*.seo.json`, `raw/crawl.json` | `02-evaluation.md` | the agent (plan + execute), `diff.py` (count, review only) |
| `diff.py` | two `01-baseline.md` (pre-publish + live re-baseline) | `diff.md` | the **post-publish PR comment** — **review phase only, not a cycle** |
| agent · `PLAN` | `02-evaluation.md`, `MISSION.md` | `plan.md` | the execute stage |
| agent · `EXECUTE` | `plan.md`, `02-evaluation.md`, `01-baseline.md`, theme source | `execution.md`, theme code, **PR body** | the human (review → publish) |

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

### Config — the one source of per-client truth
| File | Lines | Role |
|---|---|---|
| [`hobbes.toml`](hobbes.toml) | 22 | Per-client config: the golden path (home/collection/product URLs), where secrets live (names, not values), branch prefix, **timezone** (pins cycle dates), **effort_budget**. |

### The deterministic engine — `hobbes/tools/`
| File | Lines | Role |
|---|---|---|
| [`tools/config.py`](tools/config.py) | 70 | Single source loaded from `hobbes.toml`: `golden_path()`, `client_meta()`, `psi_key()` (env→file), `effort_budget()`, `today()`/`stamp()` (pinned-tz dates so local + CI never disagree). |
| [`tools/psi.py`](tools/psi.py) | 358 | PageSpeed Insights / Lighthouse capture → prints scorecard **§A–D** (lab perf/a11y/BP/SEO + CrUX field) to stdout. Median-of-3, retry-resilient (survives PSI timeouts and truncated reads). |
| [`tools/seo.py`](tools/seo.py) | 316 | Per-page HTML SEO checklist → prints **§E** (titles, meta, canonical, OG, structured data). |
| [`tools/crawl.py`](tools/crawl.py) | 437 | SiteOne sitemap crawl (stratified sample) → prints **§F** site-wide SEO/a11y/security counts. |
| [`tools/baseline.py`](tools/baseline.py) | 135 | Runs psi + seo + crawl into one dated cycle folder and **captures their stdout** into the one digest, `01-baseline.md` (stamped from `TEMPLATE.md`). Honors `--run-dir`. |
| [`tools/findings.py`](tools/findings.py) | 737 | The **problem catalog**: reads raw/ → `02-evaluation.md`, every issue with verbatim evidence + a static knowledge overlay (what it is, why it matters). Deterministic — fix/effort/impact are deliberately left to the plan. |
| [`tools/diff.py`](tools/diff.py) | 241 | The **review phase's** before/after (not run in a cycle), **honest by tier**: Field (CrUX, trustworthy) / Lab (§A, volatile) / **§D axe a11y** / §F counts (coverage-gated), rendered as before→after tables. `--prior` pins the comparison. |

### The CLI
| File | Lines | Role |
|---|---|---|
| [`cli.py`](cli.py) | 111 | `cycle` (baseline→findings), the individual steps (incl. `diff` as a manual drift check), `status`, `plan`/`execute` (print the stage prompt), `budget`, `today`. Run as `python3 hobbes/cli.py <cmd>`. |

### Stage contracts — `hobbes/templates/*.md`
| File | Role |
|---|---|
| [`templates/TEMPLATE.md`](templates/TEMPLATE.md) | The baseline scorecard shape — §A–G (A–F tool-filled, G manual a11y for the human). |
| [`templates/FINDINGS-TEMPLATE.md`](templates/FINDINGS-TEMPLATE.md) | The findings contract — dense, evidence-based, deterministic. |
| [`templates/PLAN-TEMPLATE.md`](templates/PLAN-TEMPLATE.md) | The plan contract — group findings into systems → estimate effort → estimate impact → **order by leverage (impact ÷ effort)**. |
| [`templates/EXECUTE-TEMPLATE.md`](templates/EXECUTE-TEMPLATE.md) | The execute contract — select a batch by effort budget, research, implement the **whole** batch, gates ("no *new* Theme Check offenses"), and the PR's before/after. Never publishes. |
| [`templates/PUBLISH-TEMPLATE.md`](templates/PUBLISH-TEMPLATE.md) | The publish contract — human-owned: PR review → sign-off → merge → go-live → `published` label → review. |

### The cloud runner — `.github/workflows/`
| File | Trigger | Role |
|---|---|---|
| [`../.github/workflows/hobbes-cycle.yml`](../.github/workflows/hobbes-cycle.yml) | dispatch (budget input) | The work cycle: `cli.py cycle` measures (deterministic, no LLM), then `claude-code-action` plans + writes the fix → **one PR** carrying the scorecard/findings *and* the code. (No diff — that's the review.) |
| [`../.github/workflows/hobbes-review.yml`](../.github/workflows/hobbes-review.yml) | `published` label + dispatch (PR #) | Post-publish: re-baseline the **live** site, diff vs the pre-publish baseline, comment on the PR. No Claude. |

### Operator guides — `hobbes/`
*(Engine-generic — same across clients; read by the agent and the human operator.)*
| File | Role |
|---|---|
| [`SETUP.md`](SETUP.md) | **Setup, once per client** — local (Python + SiteOne + PSI key + first cycle) and cloud (two secrets, the Claude GitHub App, the "allow Actions to create PRs" toggle, the `published` label, workflows-on-default-branch), each annotated with the error it prevents. |
| [`BASELINE.md`](BASELINE.md) | The operator's runbook for a baseline cycle — the tools, the run, the targets, the deliverables. Read by the agent during a cycle. |

### Cycle data — `hobbes/cycle/<YYYY-MM-DD>/`
Each cycle is a folder — the **filesystem is the state machine**. A folder accumulates: `01-baseline.md` → `02-evaluation.md` → `plan.md` → `execution.md`, beside `raw/` (the `*.psi.json` / `*.seo.json` / `crawl.json` captures — git-ignored, the only build intermediate). The three capture tools print their sections to stdout for `baseline.py` to assemble into the one `01-baseline.md`; they write no per-tool digest of their own. **No `diff.md` lands in a cycle folder** — the diff is the review phase's, written post-publish and posted as a PR comment. Which files exist tells you which stage the cycle reached (`cli.py status`).

---

## How it runs

**Cloud (the default).** Both workflows run from the **default branch** in GitHub Actions:
- **Measure + fix:** Actions → *Hobbes cycle* → Run (blank budget = `hobbes.toml` default). It measures, then plans and writes the fix → **one PR** with the scorecard/findings *and* the code change. Manual trigger only — there is no cron; a cycle fires when you ask for one.
- **Verify:** add the **`published`** label to the merged PR (after you publish in Shopify). → before/after comment. Manual re-run: Actions → *Hobbes review* → Run → enter the PR number.

GitHub emails you when a PR opens or a comment posts — that's the notification; you don't watch anything.

**Local.** The deterministic half runs on a laptop with Python 3.11+ and the SiteOne crawler — `python3 hobbes/cli.py cycle` produces the data (scorecard + findings) only. The agent half (plan + fix) runs as the cloud workflow, or as local Claude Code against the templates (no secret needed — uses your login).

**The operator's loop:** run *Hobbes cycle* when you want work → one PR (data + fix) in your inbox · review + merge → publish in Shopify → add `published` → the review posts the impact.

---

## Load-bearing design decisions

- **GitHub-only.** Hobbes touches nothing but GitHub. No Shopify CLI, no Shopify credentials. Going live is always a human in Shopify.
- **Claude Code, not the API.** The agent stage (plan + fix) authenticates with a **Claude Code subscription token** (`claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN`), never a pay-per-token API key. The deterministic stages use no Claude at all.
- **The determinism boundary.** Tools measure and compare (reproducible); the agent judges and builds (creative); the human publishes (irreversible). Each thing lives where it belongs.
- **Measure and fix fire together, into one PR.** A CI cycle always runs the deterministic measure *and* the agent fix on one trigger, landing the scorecard/findings beside the code change in a single PR — so the fix is always planned against fresh measurements, never a stale cycle folder. There's no measure-only cron; a data-only run is the local `cli.py cycle`.
- **The diff is the review's, not the cycle's.** A cycle measures the current site and has no "after" — this cycle's fix isn't live yet — so it writes no diff. The before/after lives entirely in the **review** phase (post-publish), where `diff.py` re-baselines the live site and compares it to the pre-publish baseline. This also gives the 28-day CrUX field signal time to move, which an at-publish comparison can't.
- **The diff doesn't lie.** When it does run (in review), it separates the trustworthy field signal from volatile lab noise, gates site-wide counts on crawl coverage (a collapsed crawl can't read as "improvement"), and surfaces the §D a11y findings the agent actually targets — distinguishing a real win from noise from an *unfulfilled claim*.
- **`published` is an explicit signal.** The review fires on a human-added label, not on merge — because "merged" doesn't mean "live," and every client's Shopify is wired differently.
- **Pinned-timezone dates.** Cycle folders are stamped in `[cycle].timezone`, so a local run and a UTC CI runner always land on the same calendar day.
- **Effort budget is a ceiling, not a quota.** Execute fills it with leverage-ordered work and won't shoehorn; a high budget only produces a big PR when there's that much worthwhile work queued.
