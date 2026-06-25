# Plan — YYYY-MM-DD

Site: [url] · Cycle: [YYYY-MM-DD] · Authored by Hobbes from `02-evaluation.md` + `01-baseline.md` + `raw/`.

This is the **plan** — where the system goes from deterministic extraction to judgment. Baseline and findings are tool-built and repeat exactly; the plan is Hobbes thinking. It sits between two documents and is not either of them:

- `02-evaluation.md` is the **problem catalog** — every problem, deterministic, no fix and no weighting. The plan **groups** those problems into systems and **rates** them.
- **Execution** (next stage) does the work, top-down through the order the plan sets. The plan does not write the fix line-by-line — it understands each system well enough to estimate effort and impact and tell execution where to start.

Two runs of the plan may differ — judgment isn't deterministic, and that's correct. The one hard rule: **invent nothing.** Every system maps to real finding IDs from this cycle. Facts (the findings) stay apart from the calls (your effort/impact ratings), and you own the calls.

## Inputs — read all, in depth, before grouping

- **`02-evaluation.md`** — the problems to group. Every system cites its finding IDs.
- **`01-baseline.md`** — the numbers, targets, and the **field-vs-lab** reality (e.g. §C CrUX may already pass where lab fails — that changes impact).
- **`raw/`** — go deeper on any finding when grouping or effort needs more than the catalog shows.
- **`MISSION.md`** — what **impact** is rated against: the priorities (in their stated order), the mission line, and "Needs work". This file decides *what matters*.
- **`DEVELOPMENT.md`** — what **effort** and **feasibility** are rated against on the *stack* side: whether a fix is authorable in the code we control at all or lives in content / third-party / platform the cycle can't reach, how hard it is given the stack's constraints (core-file risk, generated config, the browser gate, any upgrade-safety rule), and the "done means" bar each system must clear.
- **`CONTEXT.md`** — what **effort** and **feasibility** are rated against on the *people* side: which kind of work each fix needs (code · content/admin · integration or platform config · sign-off) and **who** `CONTEXT.md` names for it, plus the hard constraints that gate it (platform limits, the brand bar and whose sign-off brand-visible work needs, accessibility as a standing requirement). This is what "the resources we have" *means*.

> **The three files map cleanly onto the two scores.** **Impact ← `MISSION.md`** (what matters). **Effort & feasibility ← `DEVELOPMENT.md` + `CONTEXT.md`** (what it costs — the stack's reality and the people behind it). Read all three; a plan that rates impact without the mission, or effort without the stack and the people, is guessing.

## The method — four phases

Read findings, raw, and baseline in depth first. Understand each problem deeply — what it does and all its specifics — before grouping anything. Then:

1. **Group.** Cluster the findings into **systems** — by same problem, similar problem, cascading dependency, related or coupled cause. A system is the set of findings one body of work would address together. **Systems cut across the finding domains** — a missing-alt system spans A11Y *and* SEO; a heading system spans A11Y *and* SEO with one cascading root. Understand each system deeply: the shared root cause, and what a single fix would clear. Cite the finding IDs.

2. **Effort.** For each system, estimate the effort to fix it — a subjective **1–5** rated against **`DEVELOPMENT.md`** (the stack) and **`CONTEXT.md`** (the people), weighing: whether it's authorable in the code we control at all or lives in content / third-party / platform the cycle can't reach (`DEVELOPMENT.md`); how hard given the stack's constraints — core-file risk, generated config, the browser gate, any upgrade-safety rule (`DEVELOPMENT.md`); **which kind of work it needs and who owns it** — code · content/admin · integration or platform config · sign-off, each mapped to the person `CONTEXT.md` names (`CONTEXT.md`); how complicated it is; and how much we already know vs. still have to investigate. When a hard constraint *gates* a system — not code-authorable, breaks an upgrade-safety rule, needs brand sign-off — name it: it sets the owner and can sink the system to won't-chase regardless of its raw score.

3. **Impact.** For each system, estimate the impact of fixing it — a subjective **1–5**, weighed against `MISSION.md`: which priority it advances, whether it serves the mission directly, and how many findings / pages one fix clears. Weigh the field-vs-lab reality — a perf fix matters less to real users where CrUX already passes.

4. **Order.** Rank the systems by priority score and pass the ordered list to execution — highest-leverage work first.

## Scoring

The two scores read from different files — keep them apart so a cheap fix can't inflate its impact and a mission-critical one can't hide its cost.

- **Impact (1–5)** — against `MISSION.md`. `5` = clears a Priority-1 gap (whatever `MISSION.md` ranks first), or a cross-cutting root whose single fix cascades across many findings/pages. `3` = a real golden-path gap advancing a non-top priority. `1` = cosmetic, platform-bound, or already fine for real users (field passes).
- **Effort (1–5, cost)** — against `DEVELOPMENT.md` (the stack: code-authorable? how hard given the stack's constraints? browser-gated?) and `CONTEXT.md` (which kind of work, who owns it, what access, whose sign-off). `5` = long, needs scarce resources (client content at scale, an integration removal + coordination, or a risky core change), and complex. `1` = a token tweak or a single self-contained change shipped in minutes. Name the resource — a system that needs *the client to write dozens of product descriptions* is a different cost than one a developer fixes in code.
- **Priority = Impact ÷ Effort** — leverage. High impact, low cost, first.

> Formula note: the brief said *impact × effort*. Taken literally that ranks the **hardest** work first — a 5×5 monster above a 5×1 quick win — which buries exactly the quick wins you'd want to ship first. So this scores leverage as Impact ÷ Effort. If you truly want the product, it's a one-character flip; the recommendation is leverage.

## Output — the shape of `plan.md`

One block per system, then the ordered table.

```
### SYS-<n> · <system name>
- **Findings:** <A11Y-6, A11Y-7, SEO-3 — the IDs this system covers>
- **The system:** <what binds them — shared root cause, the cascade, what one fix clears>
- **Effort:** <n>/5 — <time · which resource (code / content / integration or platform config / sign-off) · complexity · confidence>
- **Impact:** <n>/5 — <mission priority served · findings & pages cleared · field-vs-lab caveat>
- **Priority:** <impact>/<effort> = <x.x>
```

Then:

```
## Order (highest leverage first)

| Rank | System | Impact | Effort | Priority | Do-first because |
|---|---|---|---|---|---|
| 1 | SYS-3 · … | 5 | 1 | 5.0 | clears 3 a11y findings sitewide, one snippet |
| 2 | … | | | | |
```

Every finding in the cycle lands in exactly one system — none dropped, none invented. If a finding is genuinely not worth acting on (platform-bound, benign), it still gets a system (or a "won't-fix" note with the reason), so coverage is visible, never silent.

## The handoff

The ordered table is what execution consumes. It works the systems top-down, proving each against the BASELINE targets and the `DEVELOPMENT.md` "done means" bar before moving on. After publish, the review re-baselines the live site and diffs against this cycle's baseline — closed findings and any regressions tell you whether the plan worked.

## Pointers

- `02-evaluation.md` — the problems this plan groups (cite the IDs).
- `01-baseline.md` — the numbers and field-vs-lab context.
- `MISSION.md` — what **impact** is rated against (the priorities and the mission line).
- `DEVELOPMENT.md` — the **stack** behind every effort/feasibility call: code-authorable vs not, core/upgrade-safety risk, the "done means" bar.
- `CONTEXT.md` — the **people, access, and hard constraints** behind every effort estimate and every gated system.
