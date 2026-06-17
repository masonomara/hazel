# Baseline scorecard — YYYY-MM-DD

Client: [name] · Site: [url] · Platform: [platform] · Run by: [name] · Date: [YYYY-MM-DD]

Golden path: [page 1 url] · [page 2 url] · [page 3 url]

Copy this file to `YYYY-MM-DD-baseline.md` (date first, ISO 8601 — the `[date]-[name].md` convention) and fill every cell with a raw number or pass/fail. Compare to the Targets in `hobbes/BASELINE.md`. The filled file **is** the baseline.

Sections A, B1, and B2 are filled by Hobbes from `hobbes/tools/psi.py` (PSI API) — paste from its `psi-results.md` artifact. Sections C and D are the human's to sign.

## A. Lighthouse scores (LAB — PSI server)

`python3 hobbes/tools/psi.py`. Mobile uses PSI's fixed throttle (Moto G4 / slow 4G); desktop is unthrottled. A ⚠ on a row = PSI flagged the run incomplete (page too slow to finish in the time limit); the category scores stand, but treat late metrics (esp. LCP) on that row as unreliable and re-run `--fresh` if the score looks unstable.

| Page / Device | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home — mobile |  |  |  |  |
| Home — desktop |  |  |  |  |
| Collection — mobile |  |  |  |  |
| Collection — desktop |  |  |  |  |
| Product — mobile |  |  |  |  |
| Product — desktop |  |  |  |  |

## B1. Lab metrics (LAB — not real INP; TBT is the lab stand-in)

Lab only. Real INP and the real-user verdict are in B2 — never put a field number in this table.

| Page / Device | LCP (s) | CLS | FCP (s) | TTFB (s) | TBT (ms) | Speed Index (s) |
|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |

## B2. Field data (CrUX 28-day, per page — the only real INP)

Real users, per page (not per device). "origin agg." = the page lacks page-level CrUX so PSI returned the whole-site average — note it, don't treat it as the page's own number.

| Page | LCP (s) | INP (ms) | CLS | Overall |
|---|---|---|---|---|
| Home |  |  |  |  |
| Collection |  |  |  |  |
| Product |  |  |  |  |

## C. Accessibility detail

| Page / Device | WAVE errors | WAVE contrast errors | Keyboard pass | Focus visible | Screen reader pass | Contrast fails | Alt coverage |
|---|---|---|---|---|---|---|---|
| Home — mobile |  |  |  |  |  |  |  |
| Home — desktop |  |  |  |  |  |  |  |
| Collection — mobile |  |  |  |  |  |  |  |
| Collection — desktop |  |  |  |  |  |  |  |
| Product — mobile |  |  |  |  |  |  |  |
| Product — desktop |  |  |  |  |  |  |  |

## D. SEO checklist

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

## E. Site level (once per site)

| Item | Present |
|---|---|
| `sitemap.xml` |  |
| `robots.txt` |  |
