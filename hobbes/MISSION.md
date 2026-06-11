# Mission

This is the map you steer by. When you weigh an idea, weigh it against what is written here. If I ask for something that cuts against the mission, say so before you build it.

## The mission

The one thing this agent optimizes for:

> A fast accessible and discoverable Hazel Storefront that is clean and consistent enough to let the product do the work.

## Top priorities

Each priority is written as **baseline → target** so "done" is not a matter of opinion. If there is no number, there is no priority — find the number first.

1. **Accessibility:** baseline TBD → Lighthouse Accessibility 100 and 0 WAVE errors/contrast errors on all three core pages.
2. **SEO & discoverability:** baseline TBD → Lighthouse SEO ≥ 95 and the full SEO checklist passing on all three core pages.
3. **Performance:** baseline TBD → Lighthouse Performance ≥ 90 and Core Web Vitals all "good" on all three core pages, mobile + desktop.

## Active builds

- **Hazel storefront** - cleaned up and running better (base theme fork stripped, fonts and tokens set, mobile fixed). Next: run the Step 0 baseline capture so the three priorities get real numbers.

## Needs work

- **Motion & consistency** ("move well") - Jenna likes the style, but the site doesn't move well or hold together yet; wants more animation. This is the real gap, and what the priority work should protect.
- **Page & navigation cleanup** - lingering template and nav items.
- **Image & asset loading** - confirm consistent loading site-wide.

## Back burner

- **Mobile app** - unscoped. Park until the problem it solves is defined.
- **Automation research** - back-in-stock notifications, inventory management, customer flows, recommendations. Research first; bring recommendations before implementing anything.

## Sunset candidates

- **Express pay** - Enabled Shop Pay express checkout on every page for one-tap checkout. RESULTS: After about 80,000 sessions the share of orders completed with Shop Pay declined from 9.5% to 6.7% and the reached checkout rate went down 15%. Small sample size but nothing suggest sthe SHop Pay buttons helped with checkout. 

## Debt

- **Accessibility issues** - known but unmeasured; Step 0 turns them from vague debt into measured priorities.
- **No baseline / test harness yet** - fixed by Step 0; the captured numbers become the reusable baselines.
- **Lingering nav/template cleanup** and unconfirmed sitewide asset loading.
- **Ongoing theme-cleanup backlog** - chip away as hours allow.
