# Publish — YYYY-MM-DD

Site: [url] · Cycle: [YYYY-MM-DD] · Branch / PR: [link] · Released by [human].

This is the **release** stage — the only stage that touches the live site. Execution built and verified the work on a branch and opened a PR; publish takes that reviewed work **live**. Because going live is irreversible and outward-facing, this stage is **human-owned**: Hobbes assists, but a human reviews, signs off, and publishes. The CLAUDE.md hard line lives here.

## Where this sits

`baseline` → `findings` → `plan` → `execute` (branch + PR ready) → **`publish` (PR review → sign-off → merge → go live)** → **`review` (automatic, post-publish: re-baseline the live site and comment the before/after on the PR)** → loop back to `baseline` for the next cycle.

## The hard line — read before anything

Publish crosses the things Hobbes may **not** do alone (CLAUDE.md): publish externally, change the live site, merge nontrivial work to `main`. So Hobbes's role here is bounded, on purpose:

- **Hobbes may:** summarize the PR, answer review comments, make requested code changes (looping back through the `execute` gates), and draft the `CHANGELOG.md` entry. **Hobbes writes only to GitHub — it never runs the deploy** (no platform CLI, no live push, no publish).
- **Only a human may, and only on explicit sign-off:** merge to `main`, and **publish/deploy the live site. Only the designated human (per `CONTEXT.md`) publishes — never without sign-off.** Hobbes never runs the live publish itself, and never assumes a past approval carries to this release.

If you are unsure whether a step is over the line, it is. Stop and hand it back.

## The steps

1. **Review.** Open the PR for the human. Summarize what shipped, the finding IDs it closes, what was verified (the stack's checker clean, mobile + desktop), and what's deferred to a human (content at scale, a third-party/integration removal decision). Address review comments — any code change loops back through the `execute` quality gates before it's re-offered.

2. **Sign-off.** The code owner signs off on the code. Where the change is **brand-visible** (layout, type, motion, anything a visitor sees), the brand owner signs off too — they own brand and final sign-off (`CONTEXT.md`). Don't merge brand-visible work without their nod.

3. **Merge.** On sign-off, merge the branch to `main` — the source of truth.

4. **Preview on staging (the human owner, in the platform — outside Hobbes).** Deploy to an **unpublished / preview environment** — never straight to live. Coordinate any platform-generated config so the platform's editor and the deploy don't clobber each other (per `DEVELOPMENT.md`). Verify mobile + desktop on the preview.

5. **Go live — human only.** **The designated human publishes/deploys the live site.** Hobbes does not run this step. Immediately after, verify the live site on mobile + desktop, then **add the `published` label to the PR** — that label is the explicit "it's live now" signal that fires the `review` phase. (Adding it before the change is actually live would measure the old site.)

6. **Close the loop.** Draft the `CHANGELOG.md` entry — what shipped, why, the finding IDs closed, and the result. (`MISSION.md` is human-owned — Hobbes never edits it; a closed gap is recorded by the scorecard and `06-review.md`, not by rewriting the mission.) Adding the `published` label in step 5 fires the **`review` phase** (`.github/workflows/hobbes-review.yml`): `publish-review.py` re-captures the live site into the cycle's `raw-review/`, `review.py` diffs it against the cycle's pre-publish `01-baseline.md`, and the result (`06-review.md`) is **commented on the PR**. Read it by latency — alt/heading/meta crawl counts and lab a11y/SEO scores move immediately; **field/CrUX is a 28-day average and won't show for weeks** (the next regular cycle confirms it). A finding isn't "done" because it was coded — it's done when the baseline shows it gone.

## Pointers

- `execute.md` / the PR — what's being released.
- `DEVELOPMENT.md` — the deploy mechanics (the platform CLI, preview-first, only the designated human publishes, don't break the live site).
- `CONTEXT.md` — who signs off (the code owner on code, the brand owner on brand-visible).
- `CHANGELOG.md` — the entry publish drafts to close the loop. (`MISSION.md` is human-owned: Hobbes reads it, never writes it.)
