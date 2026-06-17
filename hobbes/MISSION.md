# Mission

This is the map you steer by. When you weigh an idea, weigh it against what is written here. If I ask for something that cuts against the mission, say so before you build it.

## The mission

The one thing this agent optimizes for:

> A fast accessible and discoverable Hazel Storefront that is clean and consistent enough to let the product do the work.

## Top priorities

Each priority is a **baseline → target** so "done" is not a matter of opinion. The baseline lives in the latest scorecard (`hobbes/scorecards/`) — the source of truth — not here; this file holds the target and points there. If a priority has no number in the scorecard, it is not a priority yet — baseline it first.

1. **Accessibility** → Lighthouse Accessibility 100 and 0 WAVE errors / contrast errors, all core pages.
2. **SEO & discoverability** → Lighthouse SEO ≥ 95 and the full SEO checklist passing, all core pages.
3. **Performance** → Lighthouse Performance ≥ 90 and Core Web Vitals all "good", all core pages, mobile + desktop.

## Active builds

- **Hazel storefront** - cleaned up and running better (base theme fork stripped, fonts and tokens set, mobile fixed). Step 0 baseline captured 2026-06-11 — numbers in the scorecard (`hobbes/scorecards/2026-06-11-baseline.md`), gaps in the findings doc (`2026-06-11-findings.md`). Next: work the findings shortlist — a11y alt/button-name, the missing meta descriptions, the double-`h1`, and Home mobile lab perf.

## Needs work

- **Motion & consistency** ("move well") - Jenna likes the style, but the site doesn't move well or hold together yet; wants more animation. This is the real gap, and what the priority work should protect.
- **Page & navigation cleanup** - lingering template and nav items.
- **Image & asset loading** - confirm consistent loading site-wide.

## Back burner

- **Mobile app** - unscoped. Park until the problem it solves is defined.
- **Automation research** - back-in-stock notifications, inventory management, customer flows, recommendations. Research first; bring recommendations before implementing anything.

## Sunset candidates

- *(none active)*

## Debt

- **Accessibility issues** - now measured (baseline 2026-06-11); the failures live in the scorecard and findings doc (`2026-06-11-findings.md`). Still owed: WAVE scan + the manual keyboard/screen-reader/contrast pass before any page is signed off.
- **Baseline method** - now standardized on the PSI API via `hobbes/tools/psi.py` (key at `hobbes/tools/.psi-key`): it pulls lab and CrUX field data separately and labels them, flags incomplete runs, caches calls, and writes a `psi-results.md` artifact. Re-baseline each cycle with the same tool so numbers stay comparable. PSI's mobile throttle is fixed, so a heavy page like Home mobile can return "incomplete" — that's a real slow-page signal, not a tool gap. (Home now *does* have CrUX field data, so its real-user verdict is no longer missing — the numbers are in the scorecard; refresh them on the next clean cycle.)
- **Lingering nav/template cleanup** and unconfirmed sitewide asset loading.
- **Ongoing theme-cleanup backlog** - chip away as hours allow.
