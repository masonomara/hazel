# Execution — YYYY-MM-DD

Site: [url] · Cycle: [YYYY-MM-DD] · Branch: [feature-branch] · Driven by Hobbes from `plan.md`.

This is the **doing** stage — where the system stops describing and starts building. It takes the plan's ordered systems, selects a batch that fits an effort budget, researches and writes a code-level implementation plan against the **real codebase**, implements it, and then **stops and pushes the branch for human review**.

It is the most agent-driven stage, and the only one that writes to the repo — so it is the most tightly bounded. Two hard limits: it spends **only the effort budget**, and it **never publishes**. Merging the branch and publishing the live theme are a human's call (CLAUDE.md hard line; only Mason publishes, never without sign-off). Execution ends at "push for review" — not one step past it.

## Where this sits

`baseline` (numbers) → `findings` (problems) → `plan` (systems, ordered by leverage) → **`execute` (build the top of the order)** → `publish` (release it). Execution's terminal is a branch pushed and a PR open for review — it hands that to **`publish`**, which owns the human gate, the merge, and the go-live. Execution builds and verifies; it never crosses the line to live itself.

## 1. Select the batch — the effort budget

The plan already ordered every system by leverage. Execution just draws a line on that list at the point the budget runs out.

- **Set a budget** `B` — the effort points spent this cycle. The default lives in `hobbes.toml` (`[cycle] effort_budget`, currently **20**) and is overridable per run via the execute workflow input. It's the dial for how much to bite off: a small `B` ships one tight PR, a large `B` takes on more. Bias toward more — a thin batch under-uses the run.
- **Walk `plan.md`'s order top-down**, summing each system's effort. Draw the line where the next system won't fit in the remaining budget. The systems above the line are the batch.
- **Stay greedy on leverage.** The plan ordered by it; respect that. Don't fragment a coupled block to squeeze in points. If a later system fits the remainder *and* stands cleanly on its own, you may pull it up — but don't shoehorn, and don't break a coherent batch.
- **Record** the budget, the selected systems, effort spent, and what's deferred to a later cycle.

> Worked example (`B = 20` against the 2026-06-18 plan): SYS-1 (2) + SYS-2 (2) + SYS-3 (3) + SYS-4 (2) + SYS-5 (3) + SYS-6 (3) + SYS-7 (4) = **19**; SYS-8 (3) won't fit the remaining 1. Batch = the top **seven** systems — the whole a11y block *plus* page metadata, image delivery, and third-party JS. The code-side of every mission priority moves in one PR; the parts that need a human (content at scale, an app-removal call) are flagged for the human, not skipped silently.

## 2. Research & write the implementation plan

> Study **[selected systems]** in great detail. Understand the intricacies of each. **[selected systems]** need to be improved. Create a detailed plan document outlining how to achieve this. Use **web search** and the **context7 MCP** to research — framework/library docs (Shopify, Liquid, Dawn where covered) via context7, app-specific config and current specifics via web. Include code snippets. **Read the actual source files before suggesting any change — base the plan on the real codebase, not assumptions.** Add a detailed todo list to the plan, with all the phases and individual tasks necessary to complete it.

Write the plan to `execution.md` in the cycle folder. Each task names the system / finding ID it closes, so the diff back to `findings.md` stays traceable.

## 3. Implement

> When the plan is complete, implement it all. When you finish a task or phase, **mark it completed in `execution.md`**. Do not stop until every task and phase in the batch is done. Do not add unnecessary comments or doc-blocks. Honor the project's type discipline, and continuously run the project's checker so you don't introduce new issues.

**Clear the whole batch — don't quietly ship a subset.** The budget already bounded the work; once selected, every system in the batch gets implemented this run. A coherent code change you simply didn't get to is not a deferral; finish it. (Past runs under-delivered by stopping at two systems out of caution — don't.)

**Author what you can; defer only what you genuinely can't — three buckets, not two:**

1. **Ship it.** Self-contained code you can both write *and* reason about from the source — write it.
2. **Author it, flag it for review.** Code you can write from the source but **can't verify without a browser** (a layout/CSS tweak, a DOM-affecting change, an a11y attribute whose effect needs axe). Do **not** defer these — the review gate *is* where browser verification happens. Author the best-effort fix and flag it in `execution.md` and the PR as **"needs browser confirmation at review,"** naming exactly what to check (e.g. "confirm 0 `label-content-name-mismatch` on Home mobile; confirm the hero doesn't shift"). Lean toward authoring — a flagged best-effort fix a human verifies beats a finding that sits untouched for cycles.
3. **Hand to a human.** Genuinely not authorable in a GitHub-only, no-browser run: content at scale (copy, image re-exports, per-product alt), app-config / paid-app decisions, platform-bound items with no theme mechanism, sign-offs, and code that needs the **rendered DOM to even know what to change** (not just to verify it) or carries real regression risk authored blind (e.g. pulling `base.css` off the critical path). Name each in `execution.md` and the PR with its reason **and its owner**.

The test between bucket 2 and bucket 3: *can you write a correct, self-contained change from the source alone?* If yes → author it and flag for verification (2). If you'd be guessing at what to change without seeing the rendered page → hand it off (3). When in doubt, prefer 2 over 3.

**Fix the pattern, not just the flagged instance — sweep the whole codebase.** Findings are measured on the **3 golden-path pages** (PSI) plus a crawl sample, so they name only the instances that surfaced *there*. A pattern finding — missing `alt`, an icon-only button with no accessible name, an unlabeled link, an unsized `<img>`, a heading-level slip — almost always recurs in theme files the measurement never touched. Before you call a pattern finding done, **grep the entire theme for every instance of it and fix them all in one pass.** "Image-alt" is not `card-product.liquid` — it's *every* `<img>` the theme renders (product/collection cards, footer recently-viewed, cart-drawer upsell, hero, every snippet). Chasing only the flagged file ships a nibble, re-surfaces the same finding next cycle from a different page, and never converges. **One pattern → one exhaustive sweep → done**, so the finding can't come back from a corner you skipped.

## Quality gates — from `DEVELOPMENT.md`, not hardcoded

The "done means" bar belongs to the stack, and it lives in `DEVELOPMENT.md` — read it. The gate is **"no *new* offenses from this change,"** not "zero offenses" — a real repo carries pre-existing ones (this theme already has a Theme Check error in `icon-shop-pay.liquid`), so a zero-offense gate would block every PR forever. Diff the checker output against the base, not against zero. For this theme (Liquid + vanilla JS, Dawn fork, **no build toolchain, no TypeScript**):

- **Run `shopify theme check` continuously** — the theme's checker (the role "typecheck" plays elsewhere). The bar is **no new offenses in the files you touched**; pre-existing ones elsewhere are out of scope.
- **Browser verification is the human's, at review** — the agent can't run a browser in CI. It authors against the source; the mobile + desktop check and "no new console errors" happen at review, and every bucket-2 change is flagged for exactly that.
- **Keep the fork upgrade-safe** — self-contained snippets, Hazel overrides in the appended `base.css` section, minimal Dawn-core edits. Do not hand-edit `settings_data.json`.
- **No regression** against the `baseline.md` targets.
- **No unnecessary comments**; match the surrounding file's style.

> The seed prompt's "no any/unknown types · run typecheck" is TypeScript language. This codebase has none — so it maps to: honor whatever type discipline the stack has (here, none) and run whatever checker it has (here, `shopify theme check`). Don't carry a gate the stack can't run; substitute the real one from `DEVELOPMENT.md`.

## 4. Stop + hand off — with the baseline before/after in the PR

When the batch is implemented and the gates pass: **stop.** Do not merge, and do not publish the live theme — that's the `publish` stage, and a human owns it. Push the feature branch and open the PR. The PR body must carry the **baseline before/after**, not just a prose summary:

- **Before** — for every finding the batch closes, its *current measured value* pulled from this cycle's `baseline.md` / `findings.md` (e.g. "a11y 88 mobile", "73 pages missing meta description"), plus the target it should hit. This is the pre-fix state, captured before the PR opens.
- **After (measured) comes post-publish, by necessity.** PSI and the crawl only measure the **live** site, and the fix isn't live until a human publishes — so the true after is not knowable at PR time. It lands in the **review's before/after comment** once the change is live (the review re-baselines the live site and diffs against this cycle's baseline); the 28-day CrUX field part confirms in a later review still. Do not fabricate an after from local guesses or unpublished previews.
- **What shipped** — the systems implemented this run, each naming the finding/system IDs it closes.
- **Human to-do — the actions only a person can take, as a checkbox list grouped by owner.** Execution writes only code; everything else the cycle surfaced lands here so the PR is a complete handoff, not a code drop with the rest lost. Write each as `- [ ]` so it can be ticked off, and give each item *the action · the owner · the finding/system it closes*. Always cover:
  - **Publish** (every PR, owner: Mason) — merge → push to a dev theme → verify mobile + desktop → publish live → add the `published` label. (Steps in `PUBLISH-TEMPLATE.md`.)
  - **Browser-confirm** (Mason, at review) — every **bucket-2** change authored-but-unverified, with exactly what to check.
  - **Content** (Jenna / Britni) — the specific copy to write, images to re-export, alt to author, admin settings to change.
  - **App / platform** (Brenda / Jenna / Mason) — app-config changes, paid-app decisions, and platform-bound items (e.g. a Shopify-support request).

That open PR **is** the handoff to `publish` — execution is done. The cycle closes only after publish takes it live and the next baseline confirms the after.

## Pointers

- `plan.md` — the ordered systems this batch is drawn from.
- `findings.md` / `baseline.md` — what each task closes, and the targets to hold.
- `DEVELOPMENT.md` — the stack and the real "done means" gates.
- `CONTEXT.md` — who owns the non-code work (content, app decisions, sign-off).
