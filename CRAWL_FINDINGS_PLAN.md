# Plan — SiteOne crawl → fresh baseline → first findings doc

**Status:** Phases 1–4 complete (`crawl.py` built, wired into `baseline.py`, fresh full run done, `2026-06-17-findings.md` drafted). Phase 5 (backport spec to `BASELINE.md`) intentionally deferred.
**Goal:** add whole-site crawl coverage to the automated baseline, run one clean full capture, and draft the first real findings doc — letting the findings *spec* fall out of a working example before it's backported to `BASELINE.md`.

**Grounding:** based on the actual code as of this writing — `hobbes/tools/{psi,seo,baseline}.py`, `hobbes/scorecards/TEMPLATE.md`, and the installed `siteone-crawler` binary (`--output-json-file` confirmed).

---

## Design decisions already settled

- **Crawl feeds two places:** summary **counts → Scorecard Section E** (site-level); per-URL **detail → findings**. Scorecard stays quantitative; findings holds the fixes.
- **Root crawl, not sitemap.** Broken links are only found by following links on pages; the sitemap lists only good URLs.
- **Findings structure:** flat table with an **`Area`** tag (a11y / seo / perf / best-practices / links) — *not* grouped by the 3 missions, so Best Practices and broken links have a home (avoids the run-1 orphaning).
- **Date is `2026-06-17`**, from today's clean artifacts — never `2026-06-11` (that's run-1's contradictory data).
- **Lean spec:** drop `severity` as a column (grouping + "Start here" cover it; rank by target−baseline where free) and drop stable `id`s for v1 (Issue+Scope is the natural key; add IDs when cycle-2 regression needs them).
- **Auto/judgment boundary:** tools auto-fill `Issue / Area / Scope / Source`; agent+human fill `Fix / Effort` and the "Start here" ranking.
- **Findings spec is NOT backported to BASELINE.md yet** — only after the working doc proves out.

## Open item to confirm before Phase 3
- [x] **Live-crawl rate** — confirmed by Mason. `--max-reqs-per-sec=5 --workers=3 --timeout=10 --max-visited-urls=2000`, root crawl.

---

## Phase 1 — Build `crawl.py` (mirror `seo.py`'s shape)

- [x] **1.1 Probe the JSON schema first (don't guess field names).** Done — bounded crawl to `/tmp/probe.json`.
- [x] **1.2 Inspect `/tmp/probe.json`** — done. Real schema: `results[].status` (HTTP code, string); `tables['seo'].rows[]` = per-URL `{urlPathAndQuery, title, description, h1}` (empty string = missing); `tables['404'].rows[]` = `{url, statusCode, sourceUqId}`; `tables['redirects'].rows[]` = `{url, targetUrl, statusCode}`; `tables['non-unique-titles'/'non-unique-descriptions'].rows[]` = `{count, title|description}`.
- [x] **1.3 Scaffold `crawl.py`** — stdlib only, root from `psi.DEFAULT_URLS[0]`, gentle `LIMITS`, `--fresh`/`--resume`/`--out`.
- [x] **1.4 Implement the crawl call** — `subprocess` to `siteone-crawler` with JSON output + gentle flags; cached `crawl.json`, reused on `--resume`, re-crawled on `--fresh`/default.
- [x] **1.5 Implement the parser** — broken links (`tables['404']`), redirects, missing/duplicate titles, missing descriptions, missing H1; counts + per-URL lists.
- [x] **1.6 Implement the artifact** `crawl-results.md` — `## Site-wide (crawl) — Section E counts` table + `## Detail — for findings`.
- [x] **1.7 Error handling** — binary missing → brew-install message; crawl failure / no output → non-zero exit.
- [x] **1.8 Test** — ran against probe data (`--resume`): 2 pages, 2 missing descriptions, 1 missing H1, reconciles with `seo` table.
- [x] **1.9** `python3 -m py_compile hobbes/tools/crawl.py` — passes.

## Phase 2 — Wire crawl into `baseline.py`

- [x] **2.1** Added `run_tool("crawl.py", passthrough)` after the `seo.py` call.
- [x] **2.2** Reads `crawl-results.md`; extracts the count table via `between(crawl, "| Site-wide (crawl) | Count |", "## Detail")`.
- [x] **2.3** Appends that count table **under Section E** (after seo's site-level table) — no competing `##` header.
- [x] **2.4** Crawl **detail stays out** of the scorecard — only the count table is merged; detail remains in `crawl-results.md` for findings.
- [x] **2.5** Added `--no-crawl` flag.
- [x] **2.6** Docstring + MVP note updated (psi → A–D, seo → E per-page, crawl → E site-wide counts). Also fixed `crawl.py` fresh-logic to mirror psi/seo so `--resume` reuses the cached crawl.
- [x] **2.7** Tested `baseline.py --resume` — scorecard assembles with the crawl count table in E, F blank.
- [x] **2.8** `python3 -m py_compile hobbes/tools/baseline.py` — passes.

## Phase 3 — One full fresh run

- [x] **3.1** Live-crawl rate confirmed by Mason.
- [x] **3.2** Ran `baseline.py` fresh — psi (converged after a couple retries) + seo + gentle crawl of 51 pages. Exit 0.
- [x] **3.3** Verified `2026-06-17-baseline.md`: header filled; A–F present; crawl counts in E; `⚠`/`✗cut` + footnotes preserved (this run: Home **and** Product mobile `✗cut`); F blank.
- [x] **3.4** Crawl counts reconcile with detail: 1 broken link (`/policies/` 404), 32 missing meta descriptions, 1 missing H1 (`/`), 0 dupes — consistent with the per-page seo results.

## Phase 4 — Draft `2026-06-17-findings.md` (authored from the artifacts)

- [x] **4.1** Big DRAFT/backport note at the top.
- [x] **4.2** Flat findings table — `Issue | Area | Scope | Source | Fix | Effort | Status`.
- [x] **4.3** Auto cells (`Issue/Area/Scope/Source`) lifted from the three artifacts.
- [x] **4.4** Judgment cells (`Fix/Effort`) filled per row.
- [x] **4.5** Dedup — the 32 missing descriptions collapsed to one template-level finding (URL list lives in `crawl-results.md`), not 32 rows; broken link kept as the one instance.
- [x] **4.6** Built **① Start here** — top 5, ranked by target-gap (SEO site-wide, frame-title all-pages, Product a11y, Home head fixes, never-idle perf).
- [x] **4.7** Built **③ Deferred — human-pending** — F manual a11y, never-idle root-cause diagnosis, alt-text quality.
- [x] **4.8** Wrote `hobbes/scorecards/2026-06-17-findings.md`.

## Phase 5 — Backport the proven spec (LATER, out of scope this round)

- [ ] **5.1** (deferred) Once the draft proves the structure, write the findings spec into `BASELINE.md` and add a findings `TEMPLATE`. Not now.
