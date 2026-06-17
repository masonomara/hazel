# Findings — 2026-06-17

> **⚠ DRAFT — the findings format is still shaking out.** This is the first real
> findings doc built from the automated baseline. The structure here (Start here →
> flat `Area`-tagged table → Deferred) is **provisional**. Once it has proven itself
> on a real fix cycle, the proven spec gets **backported into `BASELINE.md`** (plus a
> findings `TEMPLATE`). Until then, treat this format as not-yet-canonical.

Built from the 2026-06-17 MVP baseline: `psi-results.md` (A–D), `seo-results.md` (E
per-page), `crawl-results.md` (E site-wide, 51 pages). **Scope:** golden-path for the
per-template issues; whole-site for the crawl issues. The manual a11y pass (F) is **not
run**, so keyboard/screen-reader/contrast-by-eye findings are pending (see Deferred).

*How to read:* `Issue / Area / Scope / Source` come straight from the tool artifacts;
`Fix / Effort` and the **Start here** ranking are judgment. Severity is ranked by the
target gap where it's free (a11y 88→100, SEO ≥95, perf ≥90).

---

## ① Start here — highest impact per effort

1. **Missing meta descriptions, site-wide (32 pages).** Biggest discoverability gap and a near-template fix — every collection page emits none. *(seo, M)*
2. **`frame-title` on every page.** One unlabeled iframe fails a11y on all 6 surfaces; a single `title` clears it everywhere. *(a11y, S)*
3. **Product a11y: `button-name`×5 + `image-alt`×2.** Clears the worst a11y page (88) with label/alt edits in one template. *(a11y, S)*
4. **Home: double `<h1>` + no `og:image`.** Two quick head/heading fixes on the most-shared page. *(seo, S)*
5. **Investigate the never-idle script.** Home & Product mobile never reach network-idle — lab LCP truncates to ~13s while real users get ~1.6s. Find the always-on script; it also drives mobile TBT (398–432ms). *(perf, M–L)*

---

## ② All findings

| Issue | Area | Scope | Source | Fix | Effort | Status |
|---|---|---|---|---|---|---|
| Missing meta descriptions — 32 pages (26 collections, policies, `/cart`, `/search`, `/`, `/pages/divider`) | seo | site-wide (template) | crawl, E | Emit a templated meta description in the collection template (from collection body/metafield); author unique ones for Home + policy pages | M | open |
| `frame-title` — an iframe with no `title`, on every page | a11y | site-wide | psi D | Add a `title` to the embedded iframe (likely a shared app embed) | S | open |
| `button-name`×5 — icon-only buttons unlabeled | a11y | template (Product) | psi D | Add `aria-label` to the icon buttons in the product template | S | open |
| `image-alt`×2 — images with no alt | a11y | template (Product) | psi D | Add alt text to the flagged product-template images | S | open |
| `label-content-name-mismatch`×3–4 | a11y | template (Home, Collection) | psi D | Make each control's visible label match its accessible name | S | open |
| `color-contrast`×1 | a11y | template (Collection) | psi D | Raise contrast on the flagged Collection text/control to ≥4.5:1 | S | open |
| `heading-order`×1 | a11y | template (Collection) | psi D | Fix the skipped heading level in the collection template | S | open |
| Home has two empty `<h1>` | seo | template (Home) | seo E, crawl | Collapse to one meaningful `<h1>` on Home | S | open |
| Home missing `og:image` | seo | template (Home) | seo E | Add `og:image` to the Home `<head>` so shared links preview | S | open |
| Broken link `/policies/` → 404 | links | instance | crawl | Redirect `/policies/` (or remove the link pointing to it) | S | open |
| Home & Product mobile never reach network-idle; lab LCP `✗cut` (12.9s / 13.0s) vs field LCP ~1–1.6s FAST | perf | site-wide | psi A/B, footnotes | Find the always-on script holding the network open (Judge.me / Instafeed / Route / a poller) and defer/remove it — unblocks lab certification and cuts mobile TBT | M–L | open |
| Best Practices 73 on Product desktop (worst on board; target ≥95) | best-practices | template (Product) | psi A | Audit the product page for console errors, deprecated APIs, or insecure (non-HTTPS) requests from an app | M | open |
| Image alt **coverage** gaps (Home 20/45, Collection 44/88, Product 16/25 missing) | a11y/seo | template | seo E | Add alt to theme/product images; **usefulness** judged in F | M | open |

---

## ③ Deferred — human-pending

These are honest blanks, not oversights — they need a person or hands-on diagnosis:

- **Manual accessibility pass (Section F).** Keyboard, visible focus, logical order, screen reader, contrast-by-eye, reduced motion — not yet run. No page is certified *fully* pass until these are signed.
- **Never-idle root cause.** The finding above points at the symptom and the likely culprits; naming the exact always-on script needs a DevTools/network look on a real session.
- **Alt-text quality.** Coverage counts are in the table; whether the alt that *exists* is meaningful is a human call (part of F).
