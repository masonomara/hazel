# Mission

This is the map you steer by. When you weigh an idea, weigh it against what is written here. If I ask for something that cuts against the mission, say so before you build it.

## The mission

The one thing this agent optimizes for:

> A fast accessible and discoverable Hazel Storefront that is clean and consistent enough to let the product do the work.

## Top priorities

Each priority is written as **baseline → target** so "done" is not a matter of opinion. If there is no number, there is no priority — find the number first.

1. **Accessibility:** baseline **Lighthouse a11y 88–97** (Product 88, Collection 93–94, Home 97 — none at 100); axe failures: `image-alt` + `button-name` (Product, w10 each), `color-contrast` (Collection), `frame-title` (all pages), `heading-order` (Collection), `label-content-name-mismatch` (Home/Collection). WAVE + the manual keyboard/screen-reader pass not yet run. → Lighthouse Accessibility 100 and 0 WAVE errors/contrast errors on all three core pages. *(baseline 2026-06-11, PSI)*
2. **SEO & discoverability:** baseline **Lighthouse SEO 92** on every page; gaps: missing meta descriptions (Home + Collection), brand-only Home title, no Home `og:image`, Product `image-alt`, Home double-`h1`. → Lighthouse SEO ≥ 95 and the full SEO checklist passing on all three core pages. *(baseline 2026-06-11)*
3. **Performance:** baseline **real-user CWV pass** on Product + Collection (CrUX: LCP ~1s, INP 79–95ms, CLS 0–0.01); **Lighthouse Perf mobile 58–78 / desktop 84–94**. Home has no field data and the worst lab numbers (mobile LCP 7.5s, CLS 0.11). → Lighthouse Performance ≥ 90 and Core Web Vitals all "good" on all three core pages, mobile + desktop. Focus: Home (the only page without a real-user verdict) and mobile lab headroom. *(baseline 2026-06-11, lab = PSI)*

## Active builds

- **Hazel storefront** - cleaned up and running better (base theme fork stripped, fonts and tokens set, mobile fixed). Step 0 baseline captured 2026-06-11 (`hobbes/scorecards/2026-06-11-baseline.md` + `2026-06-11-findings.md`); the three priorities now carry real numbers. Next: work the findings shortlist — product alt/button-name, the missing meta descriptions, the dual-header double-H1, and Home mobile performance.

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

- **Accessibility issues** - now measured (baseline 2026-06-11): a11y 88–97, axe failures listed in priority 1 and `2026-06-11-findings.md`. Still owed: WAVE scan + the manual keyboard/screen-reader/contrast pass before any page is signed off.
- **Baseline method** - now standardized on the PSI API via `hobbes/tools/psi.py` (key at `hobbes/tools/.psi-key`): it pulls lab and CrUX field data separately and labels them, flags incomplete runs, caches calls, and writes a `psi-results.md` artifact. Re-baseline each cycle with the same tool so numbers stay comparable. PSI's mobile throttle is fixed, so a heavy page like Home mobile can return "incomplete" — that's a real slow-page signal, not a tool gap. (Home now *does* have CrUX field data — LCP 1.58s / INP 104ms / CLS 0.08 — so its real-user verdict is no longer missing; refresh the recorded numbers on the next clean cycle.)
- **Lingering nav/template cleanup** and unconfirmed sitewide asset loading.
- **Ongoing theme-cleanup backlog** - chip away as hours allow.
