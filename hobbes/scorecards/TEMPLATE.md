# Baseline scorecard — YYYY-MM-DD

Client: [name] · Site: [url] · Platform: [platform] · Run by: [name] · Date: [YYYY-MM-DD]

Golden path: [page 1 url] · [page 2 url] · [page 3 url]

Copy this file to `YYYY-MM-DD-baseline.md` (date first, ISO 8601 — the `[date]-[name].md` convention) and fill every cell with a raw number or pass/fail. Compare to the Targets in `hobbes/BASELINE.md`. The filled file **is** the baseline.

Sections A–E are filled by the tools — `psi.py` → A / B / C / D, `seo.py` → E; paste from their `*-results.md` artifacts. Section F (manual a11y) and the alt-text / contrast *quality* judgments are the human's to sign — a page is never marked pass on the automated rows alone.

## A. Lighthouse scores (LAB — PSI server)

`python3 hobbes/tools/psi.py`. Mobile uses PSI's fixed throttle (Moto G4 / slow 4G); desktop is unthrottled. A ⚠ on a row = PSI cut the run at its time limit (the page never reached network-idle): the category scores and early metrics (B) still stand. A `✗cut` Performance score / LCP is the cutoff value, not a real paint — treat it as unknown and investigate why the page never idles rather than re-measuring (local Lighthouse hits the same wall).

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile |  |  |  |  |
| Home — desktop |  |  |  |  |
| Collection — mobile |  |  |  |  |
| Collection — desktop |  |  |  |  |
| Product — mobile |  |  |  |  |
| Product — desktop |  |  |  |  |

## B. Lab metrics (LAB — not real INP; TBT is the lab stand-in)

Lab only. Real INP and the real-user verdict are in C — never put a field number in this table.

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |

## C. Field data (CrUX 28-day, per page — the only real INP)

Real users, per page (not per device). "origin agg." = the page lacks page-level CrUX so PSI returned the whole-site average — note it, don't treat it as the page's own number.

| Page | LCP (s) | INP (ms) | CLS | Overall |
|---|---|---|---|---|
| Home |  |  |  |  |
| Collection |  |  |  |  |
| Product |  |  |  |  |

## D. Accessibility — automated (axe-core via PSI)

Filled by `psi.py` from PSI's accessibility audits (these are axe-core checks — no separate axe/WAVE run needed). `color-contrast` is the contrast-error count, `image-alt` the alt gaps. List each failing rule with its node count.

| Page / Device | Failing axe audits | Details (rule × nodes) |
|---|---|---|
| Home — mobile |  |  |
| Home — desktop |  |  |
| Collection — mobile |  |  |
| Collection — desktop |  |  |
| Product — mobile |  |  |
| Product — desktop |  |  |

## E. SEO checklist

Filled by `seo.py`. Per-page checks, plus the site-level files at the foot (once per site).

| Item | Page 1 | Page 2 | Page 3 |
|---|---|---|---|
| Unique, descriptive title |  |  |  |
| Meta description present |  |  |  |
| Canonical correct |  |  |  |
| Single H1 + ordered headings |  |  |  |
| Valid structured data |  |  |  |
| Open Graph / Twitter tags |  |  |  |
| All images have meaningful alt |  |  |  |
| Indexable (robots OK) |  |  |  |

| Site-level (once per site) | Present |
|---|---|
| `sitemap.xml` |  |
| `robots.txt` |  |

## F. Accessibility — manual (optional; human sign-off, tools cannot judge these)

Optional per cycle — the automated baseline (A–E) stands on its own — but **a page cannot be certified fully pass until these manual rows are signed.** D gives the automated counts; here you judge keyboard flow, screen-reader sense, and whether the alt text that *exists* is meaningful.

| Page / Device | Keyboard | Focus visible | Logical order | Screen reader | Alt meaningful | Contrast (by eye) | Reduced motion |
|---|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |  |
