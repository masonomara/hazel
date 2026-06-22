# Publish — YYYY-MM-DD

Site: [url] · Cycle: [YYYY-MM-DD] · Branch / PR: [link] · Released by [human].

This is the **release** stage — the only stage that touches the live store. Execution built and verified the work on a branch and opened a PR; publish takes that reviewed work **live**. Because going live is irreversible and outward-facing, this stage is **human-owned**: Hobbes assists, but a human reviews, signs off, and publishes. The CLAUDE.md hard line lives here.

## Where this sits

`baseline` → `findings` → `plan` → `execute` (branch + PR ready) → **`publish` (PR review → sign-off → merge → go live)** → **`review` (automatic, post-publish: re-baseline the live site and comment the before/after on the PR)** → loop back to `baseline` for the next cycle.

## The hard line — read before anything

Publish crosses the things Hobbes may **not** do alone (CLAUDE.md): publish externally, change the live store, merge nontrivial work to `main`. So Hobbes's role here is bounded, on purpose:

- **Hobbes may:** summarize the PR, answer review comments, make requested code changes (looping back through the `execute` gates), and draft the `CHANGELOG.md` entry. **Hobbes writes only to GitHub — it never touches Shopify** (no CLI, no theme push, no publish).
- **Only a human may, and only on explicit sign-off:** merge to `main`, and **publish the live theme. Only Mason publishes the live theme — never without sign-off.** Hobbes never runs the live publish itself, and never assumes a past approval carries to this release.

If you are unsure whether a step is over the line, it is. Stop and hand it back.

## The steps

1. **Review.** Open the PR for the human. Summarize what shipped, the finding IDs it closes, what was verified (theme check clean, mobile + desktop), and what's deferred to a human (content at scale, an app-removal decision). Address review comments — any code change loops back through the `execute` quality gates before it's re-offered.

2. **Sign-off.** Mason signs off on the code. Where the change is **brand-visible** (layout, type, motion, anything a shopper sees), Jenna signs off too — she owns brand and final sign-off (CONTEXT.md). Don't merge brand-visible work without her nod.

3. **Merge.** On sign-off, merge the branch to `main` — the source of truth.

4. **Preview on a dev theme (Mason, in Shopify — outside Hobbes).** Push to an **unpublished / dev theme and preview** — never straight to live. Coordinate `settings_data.json` so the theme editor and the push don't clobber each other (it's admin-generated). Verify mobile + desktop on the preview.

5. **Go live — human only.** **Mason publishes the live theme.** Hobbes does not run this step. Immediately after, verify the live store on mobile + desktop, then **add the `published` label to the PR** — that label is the explicit "it's live now" signal that fires the `review` phase. (Adding it before the change is actually live would measure the old site.)

6. **Close the loop.** Draft the `CHANGELOG.md` entry — what shipped, why, the finding IDs closed, and the result. (`MISSION.md` is human-owned — Hobbes never edits it; a closed gap is recorded by the scorecard and `diff.md`, not by rewriting the mission.) Adding the `published` label in step 5 fires the **`review` phase** (`.github/workflows/hobbes-review.yml`): it re-baselines the live site, diffs against the pre-publish baseline, and **comments the before/after on the PR**. Read it by latency — alt/heading/meta crawl counts and lab a11y/SEO scores move immediately; **field/CrUX is a 28-day average and won't show for weeks** (the next regular cycle confirms it). A finding isn't "done" because it was coded — it's done when the baseline shows it gone.

## Pointers

- `execute.md` / the PR — what's being released.
- `DEVELOPMENT.md` — the deploy mechanics (Shopify CLI, dev-theme-first, only Mason publishes, don't break the live store).
- `CONTEXT.md` — who signs off (Mason on code, Jenna on brand-visible).
- `CHANGELOG.md` — the entry publish drafts to close the loop. (`MISSION.md` is human-owned: Hobbes reads it, never writes it.)
