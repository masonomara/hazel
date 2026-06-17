# Hobbes & Baseline — system audit

A full read of the `hobbes/` system and the 2026-06-11 baseline as it actually exists in the repo, not as it was meant to exist. The point is to improve the system, so this leans on what broke. Every claim cites a file and line so you can check it.

**Audited:** 2026-06-17 · **Scope:** `CLAUDE.md`, `hobbes/{MISSION,DEVELOPMENT,CONTEXT,CHANGELOG,BASELINE}.md`, `hobbes/scorecards/{TEMPLATE,2026-06-11-baseline}.md`, plus git history of `hobbes/`.

---

## TL;DR

The **design is strong; the execution of the first cycle is incomplete and internally inconsistent.** The operator guide (`BASELINE.md`) is genuinely good — clear tools, fixed targets, the lab-vs-field distinction hammered home. But the one cycle that ran produced ~1.3 of its 3 required deliverables, the scorecard contradicts the narrative docs on the headline Home number, the field-vs-lab rule the guide preaches was not honored in the artifact, and the rename history (Tigertail→Hobbes, three filename conventions) left dangling references throughout. None of this is fatal. All of it is fixable with a tightening pass.

The single biggest issue: **by the system's own rule ("a page is never green on automated numbers alone"), the baseline cannot certify a single page as passing** — because the manual accessibility pass and the SEO checklist were never recorded.

---

## 1. What worked

- **The context architecture is coherent.** `CLAUDE.md` defines the agent; `hobbes/` holds standing context; the "read on demand, don't `@import`" rule (`CLAUDE.md` Maintenance) is correct and the reasoning is sound — `@import` costs the same context as inlining, so on-demand reads keep the session lean. This is a real design decision, not decoration.
- **`BASELINE.md` is the strongest file in the system.** The tool list is specific and correct, the targets are fixed and unambiguous (lines 74–85), the lab-vs-field warning is repeated three times (lines 10, 35, 66), and the site-type adaptations (lines 93–118) show real thought about archetypes. The "handoff" rule — Hobbes produces the scorecard, a human signs the manual rows, no page green on automated numbers alone (line 68) — is exactly right.
- **`MISSION.md` baseline→target framing works.** Every priority carries a number and a target (lines 15–17). "If there is no number, there is no priority" (line 13) is the kind of rule that prevents vague work. The numbers did get filled after the baseline.
- **The CHANGELOG `RESULTS:` discipline works, and we have proof.** The Shop Pay entry (CHANGELOG line 22) is the system functioning as designed: a feature shipped, got measured over ~80k sessions, was judged a net negative (orders via Shop Pay 9.5%→6.7%, reached-checkout −15%), and is now being sunset. That is the whole point of "every feature carries a RESULTS line." It caught a loser.
- **The golden path got locked with exact URLs** (scorecard line 5), which is what makes future cycles comparable. Good.

---

## 2. What didn't work — the gaps

### 2.1 The findings doc was never created (highest priority)
`findings-YYYY-MM-DD.md` is the deliverable that turns numbers into action — *page → what's failing → the fix → effort (S/M/L)* (`BASELINE.md` line 90). It is referenced **three times** as if it exists:
- `MISSION.md:21` — "`findings-2026-06-11.md`"
- `MISSION.md:40` — "axe failures listed in … `findings-2026-06-11.md`"
- `CHANGELOG.md:26` — "Scorecard and findings in … `findings-2026-06-11.md`"

It exists in **no commit, ever** (checked full git history of `hobbes/scorecards/`). The findings got scattered into `MISSION.md` priorities instead — but without the fix and the S/M/L effort sizing the format requires. So the most actionable artifact in the method is missing, and three docs point at a file that isn't there.

<!-- i felt the process so far was not good enough to create a good consistent findings doc. We will get to this later after we refine the baseline collection process -->

### 2.2 The lab-vs-field rule the guide preaches was not honored in the scorecard
`BASELINE.md` warns three times that lab INP is fake and field rows must be marked "field" (lines 10, 35, 66); `TEMPLATE.md:22` says "Mark field-data rows 'field'." In the filled scorecard (section B, lines 24–31) **not one row is marked "field."** The numbers are a silent mix of lab Lighthouse and CrUX field data with no way to tell which is which — the exact failure the methodology exists to prevent.

### 2.3 The scorecard contradicts MISSION and CHANGELOG on the headline Home number
This is the one that should bother you most, because it means a number is wrong and we don't know which:

| Metric | Scorecard B | MISSION.md:17 | CHANGELOG.md:26 |
|---|---|---|---|
| Home mobile **LCP** | **1.6s** | **7.5s** | **7.5s** |
| Home mobile **CLS** | 0.08 | 0.11 | 0.11 |

The two narrative docs agree on 7.5s; the scorecard says 1.6s. A Home-mobile **Performance score of 64** (scorecard line 13) with **Speed Index 5.2s** is consistent with a ~7.5s LCP, **not** 1.6s. So the scorecard's 1.6s is almost certainly a field number dropped into a lab row — which is 2.3 biting us in practice. One of these artifacts is lying about the headline performance problem.

<!-- this needs to be fixed. MISSION.md does not exit to show numbers, it exists to show overarchnng goals and missions.

beign verbose can be good, but a concise summary is better. here are the orginal MISSION and CHANGELOG docs, let me know fi i shodul change anythign from teh originals and how I can modify the ones in this codebase to make sure that are true to the originals and do not contradict thes corecard as the search of truth. remember, changelog and missiona re high-level:


MISSION:

# Mission

This is the map you steer by. When you weigh an idea, weigh it against what is written here. If I ask for something that cuts against the mission, say so before you build it.

## The mission

The one thing this agent optimizes for:

> [State the single outcome above everything else. One sentence. Plain.]

## Top priorities

Each priority is written as **baseline → target** so "done" is not a matter of opinion. If there is no number, there is no priority — find the number first.

1. [metric: baseline → target]
2. [metric: baseline → target]
3. [metric: baseline → target]

## Active builds

- **[Project]** — [status. what it is for. the next useful action.]
- **[Project]** — [status. what it is for. the next useful action.]

## Needs work

- **[Project]** — [why it matters, or why it is failing.]

## Back burner

- **[Project]** — [why it waits.]

## Sunset candidates

- **[Project or commitment]** — [why it may need to die.]

## Debt

- [Operational debt, project sprawl, stale repos, messy docs, unused automations, unfinished loops.]




CHANGELOG:

# Changelog

The running record of shipped work. One change per entry, numbered in order, newest at the bottom of **Entries**.

**Format:** `YYYY-MM-DD — NNN type/name: what changed.`

**Types:** `feature` · `cleanup` · `fix` · `content` · `config` (extend as needed)

**Rule:** every `feature` carries a `RESULTS:` line with a measured outcome. Define the metric first. If you cannot measure it, it is not shipped.

Filled baseline scorecards live in `hobbes/scorecards/`.

---

## Examples — delete once you have real entries

**2026-08-06 — 001 feature/custom-embroidery:** Built a custom-embroidery add-on that lets customers personalize products on the product page. An "add custom embroidery" button opens a modal with live preview and a thread-color picker, a configurable fee, and a customization that carries through the drawer, cart line items, and the order, editable and removable throughout. Pulls product and variant colors from metafields (`hex_color`, `display_color`), hides the thread-color variant from the standard picker and surfaces it in the modal, and is fully configurable from theme settings. RESULTS: 60 orders on the three mock necks, 3 customizations.

**2026-08-06 — 002 cleanup/collections:** Audited three collections and tagged missing products — Hazel Minis, Mock Necks, Perfume — as `hazelmini`, `mockneck`, `perfume`.

**2026-08-06 — 003 cleanup/sizing-guide:** Added four size charts (hoodie, mock neck, barrel pants, joggers), added the oversized-fit note at the top, removed all Australian size references.

---

## Entries


-->

### 2.4 Manual accessibility pass (Scorecard C) — entirely blank
Every cell for Keyboard / Focus visible / Screen reader / Contrast fails / Alt coverage is empty across all six rows (scorecard lines 37–42). Group C (`BASELINE.md` lines 46–54) was not done. This is partially **acknowledged** (`MISSION.md:15,40` say the manual pass is "not yet run"), so it's a known hole, not a hidden one. But the consequence is hard: per `BASELINE.md:68`, **no page can be marked "pass"** until those rows are signed. The baseline is, by its own definition, provisional.

### 2.5 SEO checklist (Scorecard D) — entirely blank, yet the work was clearly done
Section D is empty in every cell (scorecard lines 46–55). But `MISSION.md:16` lists **specific** SEO findings: missing meta descriptions on Home + Collection, brand-only Home title, no Home `og:image`, Product `image-alt`, Home double-`h1`. So Group D **was performed** — the results just never got transcribed into the scorecard. The data lives in the narrative and not in the structured artifact. Same disease as 2.1: findings gathered, deliverable not filled.


<!-- this shoudl be properly filled in. can you describe how I did the work so we can start to plan how we can have an agent do it for me? -->

### 2.6 Best Practices is measured but orphaned
Scorecard A records Best Practices for all six combos (97/92/96/96/92/**76**). The target is ≥95 (`BASELINE.md:78`). Three combos **fail**, and Product desktop at **76** is the **worst single score on the entire board** — yet there is **no MISSION priority** tracking Best Practices. The three priorities are a11y, SEO, performance; Best Practices fell through the floor. The worst number we have is the one nobody owns.

<!-- see the mission i left above, the mission is suppsoed to cover the top 3 missions. by coincidence they match up wih the PSI names (accessibility, performance, SEO). best practices is not missing from the mission -->

### 2.7 CHANGELOG numbers don't match the scorecard
The CHANGELOG entry (008) summarizes numbers that disagree with the file it cites:

| Claim | CHANGELOG.md:26 | Scorecard A/B |
|---|---|---|
| Perf mobile range | 58–78 | **45**–73 |
| Perf desktop range | 84–94 | 73–**89** |
| Best Practices range | 69–73 | **76–97** |
| Home mobile LCP | 7.5s | 1.6s (see 2.4) |

The Best Practices range is the egregious one: CHANGELOG says 69–73, scorecard says 76–97 — they don't even overlap. A changelog that misreports its own scorecard is worse than no summary.

<!-- scorecard is source of truth, plase adjust -->

### 2.8 Minor drift
- **Template placeholder left in:** scorecard line 1 still reads "# Baseline scorecard — YYYY-MM" — the header was never filled.

<!-- fix this please -->

- **TTFB column added off-spec:** scorecard B carries a TTFB column (line 24); `TEMPLATE.md` has none, and `BASELINE.md:104` reserves TTFB for **non-Shopify** sites ("server response time that Shopify hides"). Hazel is Shopify. Harmless extra data, but it's drift — the template and the filled file have diverged.

<!-- fix this please -->

- **WAVE contradiction:** `MISSION.md:15,40` say the "WAVE scan … not yet run," but Scorecard C has WAVE error counts filled (59 / 134 / 13). Either WAVE ran and MISSION is stale, or those counts came from somewhere else (likely Lighthouse/axe, since the "axe failures" in MISSION are axe-core rule names that Lighthouse surfaces). Reconcile which tool actually produced those numbers.

<!-- investiagte the process and let me know. again, main focus is trying to automate the abseline collection. -->

---

## 3. Expected vs. unexpected in the baseline

**What we expected and got:** category scores for all 6 combos, the golden path locked with exact URLs, MISSION priorities filled with real numbers, a dated scorecard in `hobbes/scorecards/`.

**What we didn't expect (and is a problem):** the entire manual-a11y and SEO-checklist halves of the scorecard blank; the findings doc absent; the scorecard internally contradicting MISSION/CHANGELOG on Home LCP; no field/lab marking.

**What we didn't expect (and is useful signal):**
- **Product desktop Best Practices = 76.** The real outlier on the board, completely untracked. Worth a look — desktop-specific BP failures on a product page often mean console errors, deprecated APIs, or insecure requests from an app.
- **Collection WAVE errors = 134** vs Product's **13.** A 10× spread. The collection template is doing something structurally worse than the product template, a11y-wise (likely repeated per-card violations × many cards). That points the a11y work at the collection grid first.
- **CWV field pass on Product + Collection** (LCP ~1s, INP 79–95ms) **while their lab Perf scores are mediocre** (Product mobile 45). Real users are fine; the lab is pessimistic. That's the lab-vs-field gap working exactly as the guide says — and an argument for fixing PSI access so field data leads.

---

## 4. Better / worse than expected

**Better than expected**
- The operator guide is more thorough than the rest of the system — it reads like it was written by someone who has actually run these tools.
- The RESULTS discipline already paid off once (Shop Pay caught and killed).
- Real-user performance on the two pages with field data is genuinely good.

**Worse than expected**
- The deliverables are ~40% complete (1 partial scorecard, 0 findings docs, MISSION updated). The method promises three artifacts; the cycle produced a fraction.
- The artifacts disagree with each other on numbers that matter. A baseline's whole job is to be the trustworthy reference; this one needs a footnote on every headline figure.
- The baseline can't certify a single page "pass" — which means the next cycle has nothing clean to regress against.

---

## 5. Root-cause read (the calls, not the facts)

These are my judgments, separated from the cited facts above:

1. **The system is over-specified relative to what one cycle executes.** Three deliverables, a 22-step run, six manual a11y sub-checks. Under real pressure (PSI quota dead, time short) the execution collapsed to "fill the easy automated cells, narrate the rest into MISSION." The method needs a defined **minimum viable baseline** vs. **full baseline**, so a partial run is honest about being partial instead of looking complete.

2. **The scorecard is an afterthought, not the working surface.** SEO and some a11y findings clearly got gathered — they're specific in MISSION — but never landed in the structured file. Data flowed into prose and stopped. The scorecard has to be where you *work*, with MISSION quoting *from* it, or it will always be the thing that gets skipped.

3. **The format doesn't *force* the field/lab rule.** The guide teaches it beautifully and then hands you a table with no field rows and no source column. A rule that depends on the operator remembering it will be dropped under load — and was. Make the template enforce it structurally.

4. **Renames didn't sweep their references.** Tigertail→Hobbes and the filename churn left ghosts because nothing made "rename → fix every pointer" a step. Cheap to fix, cheap to prevent.

5. **The PSI dependency is a single point of failure.** PSI is "the primary measurement tool" (`BASELINE.md:9`) and it was unreachable (no API key / zero quota). The fallback (local Lighthouse) worked but is explicitly non-comparable to PSI (~10–15 pts off) and gives no field data — so the field story got patched in from CrUX permalinks and then mixed into lab rows. Get a PSI API key before the next cycle, or commit to local-only and stop pretending PSI is primary.

<!-- this is a fine single point of failure -->

---

## 6. Recommended edits to the system

Concrete, in rough priority order. I have **not** made any of these yet — they're proposals.

1. **Create `findings-2026-06-11.md`** in the required *page → failing → fix → effort* format, back-filling from the findings already in MISSION — or, if findings-in-MISSION is the real workflow, **delete the findings-doc requirement** from `BASELINE.md` and the three references. Don't keep pointing at a file that isn't there.
2. **Add a "Source" column (lab/field) to Scorecard B in `TEMPLATE.md`**, or split it into a lab table and a field table. Make the rule impossible to skip. Then fix the Home LCP row (2.4) once you know which number is real.
3. **Add Best Practices to MISSION priorities** (or write one line in MISSION saying why it's deliberately excluded). Product desktop 76 needs an owner.
4. **Make the scorecard the source of truth.** MISSION and CHANGELOG should quote numbers *from* the filled scorecard, never carry their own. Reconcile the 2.8 mismatches by deciding the scorecard wins.
5. **Decide TTFB:** either add the column to `TEMPLATE.md` for everyone, or drop it from the Shopify scorecard per `BASELINE.md:104`. Template and filled file should not diverge.
6. **Reconcile the WAVE contradiction** (2.11): state plainly whether WAVE ran and what produced the 59/134/13 counts.
7. **Define a "minimum viable baseline"** in `BASELINE.md`: which cells are mandatory for a baseline to count vs. which can be marked "deferred — human pass pending," so a partial cycle is labeled honestly and a page is never silently treated as passing.

<!-- i woudl like for baseline to be able to be comepltely filled in by ai. I am currently working to figure out everythign an ai can do to create the abseline, and then waht eneds to be done manually I will do at. i think the "waht ai can do" is a perfect MVP baseline, and then the manual checks like keyboard touches is the "above and beyond baseline  -->

8. **Resolve the PSI dependency:** get an API key, or rewrite `BASELINE.md` to make local Lighthouse the standard for this client and drop the "PSI is primary" framing that didn't survive contact.
