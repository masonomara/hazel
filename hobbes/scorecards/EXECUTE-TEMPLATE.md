# Execution — YYYY-MM-DD

Site: [url] · Cycle: [YYYY-MM-DD] · Branch: [feature-branch] · Driven by Hobbes from `plan.md`.

This is the **doing** stage — where the system stops describing and starts building. It takes the plan's ordered systems, selects a batch that fits an effort budget, researches and writes a code-level implementation plan against the **real codebase**, implements it, and then **stops and pushes the branch for human review**.

It is the most agent-driven stage, and the only one that writes to the repo — so it is the most tightly bounded. Two hard limits: it spends **only the effort budget**, and it **never publishes**. Merging the branch and publishing the live theme are a human's call (CLAUDE.md hard line; only Mason publishes, never without sign-off). Execution ends at "push for review" — not one step past it.

## Where this sits

`baseline` (numbers) → `findings` (problems) → `plan` (systems, ordered by leverage) → **`execute` (build the top of the order)** → `publish` (release it). Execution's terminal is a branch pushed and a PR open for review — it hands that to **`publish`**, which owns the human gate, the merge, and the go-live. Execution builds and verifies; it never crosses the line to live itself.

## 1. Select the batch — the effort budget

The plan already ordered every system by leverage. Execution just draws a line on that list at the point the budget runs out.

- **Set a budget** `B` — the effort points spent this cycle. It's the dial for how much to bite off: a small `B` ships one tight PR, a large `B` takes on more.
- **Walk `plan.md`'s order top-down**, summing each system's effort. Draw the line where the next system won't fit in the remaining budget. The systems above the line are the batch.
- **Stay greedy on leverage.** The plan ordered by it; respect that. Don't fragment a coupled block to squeeze in points. If a later system fits the remainder *and* stands cleanly on its own, you may pull it up — but don't shoehorn, and don't break a coherent batch.
- **Record** the budget, the selected systems, effort spent, and what's deferred to a later cycle.

> Worked example (`B = 10` against the 2026-06-18 plan): SYS-1 (2) + SYS-2 (2) + SYS-3 (3) + SYS-4 (2) = **9**; SYS-5 (3) won't fit the remaining 1. Batch = the four accessibility systems. The budget cleanly carves off the entire mission-priority-1 block — a coherent, shippable first PR.

## 2. Research & write the implementation plan

> Study **[selected systems]** in great detail. Understand the intricacies of each. **[selected systems]** need to be improved. Create a detailed plan document outlining how to achieve this. Use **web search** and the **context7 MCP** to research — framework/library docs (Shopify, Liquid, Dawn where covered) via context7, app-specific config and current specifics via web. Include code snippets. **Read the actual source files before suggesting any change — base the plan on the real codebase, not assumptions.** Add a detailed todo list to the plan, with all the phases and individual tasks necessary to complete it.

Write the plan to `execution.md` in the cycle folder. Each task names the system / finding ID it closes, so the diff back to `findings.md` stays traceable.

## 3. Implement

> When the plan is complete, implement it all. When you finish a task or phase, **mark it completed in `execution.md`**. Do not stop until every task and phase in the batch is done. Do not add unnecessary comments or doc-blocks. Honor the project's type discipline, and continuously run the project's checker so you don't introduce new issues.

## Quality gates — from `DEVELOPMENT.md`, not hardcoded

The "done means" bar belongs to the stack, and it lives in `DEVELOPMENT.md` — read it. The gate is **"the project's checker stays green,"** whatever that checker is. For this theme (Liquid + vanilla JS, Dawn fork, **no build toolchain, no TypeScript**):

- **Run `shopify theme check` continuously** — this is the theme's checker (the role "typecheck" plays elsewhere). Keep it clean; no new errors.
- **Browser-verify every change on mobile + desktop.** No new console errors.
- **Keep the fork upgrade-safe** — self-contained snippets, Hazel overrides in the appended `base.css` section, minimal Dawn-core edits. Do not hand-edit `settings_data.json`.
- **No regression** against the `baseline.md` targets.
- **No unnecessary comments**; match the surrounding file's style.

> The seed prompt's "no any/unknown types · run typecheck" is TypeScript language. This codebase has none — so it maps to: honor whatever type discipline the stack has (here, none) and run whatever checker it has (here, `shopify theme check`). Don't carry a gate the stack can't run; substitute the real one from `DEVELOPMENT.md`.

## 4. Stop + hand off

When the batch is implemented and the gates pass: **stop.** Do not merge, and do not publish the live theme — that's the `publish` stage, and a human owns it. Push the feature branch and open the PR for review with a short summary: what shipped, which finding IDs it closes, what was verified, and anything left for a human (content at scale, an app-removal decision, sign-off). That open PR **is** the handoff to `publish` — execution is done. The cycle closes only after publish takes it live.

## Pointers

- `plan.md` — the ordered systems this batch is drawn from.
- `findings.md` / `baseline.md` — what each task closes, and the targets to hold.
- `DEVELOPMENT.md` — the stack and the real "done means" gates.
- `CONTEXT.md` — who owns the non-code work (content, app decisions, sign-off).
