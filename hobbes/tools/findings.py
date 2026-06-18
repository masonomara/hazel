#!/usr/bin/env python3
"""
findings.py — the problem catalog. Reads a cycle's raw artifacts and emits a
dense, deterministic findings.md: every problem, with verbatim evidence, for an
agent. Step after baseline.py (which captures) and before the plan (which groups,
fixes, and rates effort/impact). See hobbes/scorecards/FINDINGS-TEMPLATE.md.

WHY DETERMINISTIC: findings get rebuilt every cycle. Same raw → same findings,
IDs and all. Everything here is extracted and sorted, never written fresh per
run. The fix, the effort, the impact, and the source-file root cause are NOT
here on purpose — those are judgment, and judgment lives in the plan.

Sources, all under the cycle's raw/:
  raw/*.psi.json   — PSI/Lighthouse per golden page × mobile/desktop (A11Y, PERF, BP)
  raw/*.seo.json   — page HTML per golden page (SEO specifics, re-parsed)
  raw/crawl.json   — SiteOne whole-site crawl (sitewide SEO/A11Y/SEC/BP counts + detail)

USAGE:
  python3 hobbes/tools/findings.py                 # newest cycle folder with raw/
  python3 hobbes/tools/findings.py --run-dir DIR   # a specific cycle folder
  python3 hobbes/tools/findings.py --out PATH      # write elsewhere
"""

import json
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOBBES = TOOLS.parent
sys.path.insert(0, str(TOOLS))
# Reuse the capture tools' logic so findings can't drift from the scorecard.
from psi import DEFAULT_URLS, cache_path as psi_cache
from seo import Page, head_ok, OG_REQUIRED
from crawl import table_rows, count_for, rollup_texts, header_set

GOLDEN = {url: label for label, url in DEFAULT_URLS}
STRATS = ("mobile", "desktop")

# ── static knowledge overlay: id -> (what it is, why it matters / where it lives) ──
# The deterministic "how it works deeply". Site-specific root cause stays for the plan.
A11Y_KNOW = {
    "button-name": ("A <button> has no accessible name.",
                    "A screen reader announces it as just 'button'. In Dawn this hits icon-only buttons — media zoom toggles, quantity steppers, drawer close icons — that need aria-label or visually-hidden text."),
    "image-alt": ("An <img> has no alt attribute.",
                  "A screen reader skips it or reads the filename. On Shopify these are product/card images; alt comes from the image's alt set in admin or the theme's <img> tag."),
    "link-name": ("A link has no discernible text.",
                  "Announced as 'link' with no destination. Usually icon/image links missing aria-label."),
    "frame-title": ("An <iframe> has no title attribute.",
                    "Announced with no purpose. Often a third-party embed (Mailchimp popup, video, map) we don't author directly — fix in the embed config or wrap it."),
    "label-content-name-mismatch": ("A control's visible text isn't contained in its accessible name.",
                                     "Voice-control users can't activate it by its visible label. Common on slideshow/hero slide links and pagination, where an aria-label omits the visible text."),
    "color-contrast": ("Text/background contrast is below WCAG AA.",
                       "Low-vision users can't read it. Often sale/sold-out price text, placeholder grey, or button text on hover — a token/CSS value, not markup."),
    "heading-order": ("Headings skip a level (e.g. h3 with no h2).",
                      "Breaks the document outline a screen reader navigates by. In Dawn, card titles (h3/h5) under a section with no h2 are the usual cause."),
}
BP_KNOW = {
    "errors-in-console": ("JavaScript errors logged to the browser console.",
                          "Each is a script failing at runtime — broken behavior, often from an app embed or a theme script. Read the messages; they name the file."),
    "deprecations": ("Use of a deprecated browser API.",
                     "Will break in a future browser version. Usually inside a third-party script."),
    "image-aspect-ratio": ("An image is displayed at a ratio that doesn't match its file.",
                           "Looks stretched/squashed; can also shift layout. A width/height or CSS sizing mismatch."),
    "inspector-issues": ("Issues Chrome's Issues panel flagged (cookies, mixed content, etc.).",
                         "Browser-level warnings; open the raw audit for the specifics."),
}


def latest_run_dir():
    base = HOBBES / "scorecards"
    cands = sorted((d for d in base.glob("[0-9]" * 4 + "-*")
                    if (d / "raw").is_dir()), reverse=True)
    if not cands:
        sys.exit(f"✗ no cycle folder with raw/ under {base}")
    return cands[0]


def trunc(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def kb(n):
    return f"{round((n or 0) / 1024)} KB"


def ms(n):
    return f"{round(n or 0)} ms"


def short_url(u):
    if not u:
        return ""
    p = urllib.parse.urlparse(u)
    tail = (p.path or "/").split("/")[-1] or p.path
    return trunc((tail + (("?" + p.query) if p.query else "")) or u, 60)


# ── loaders ──────────────────────────────────────────────────────────────────
def load_psi(raw):
    out = {}
    for label, url in DEFAULT_URLS:
        for strat in STRATS:
            f = psi_cache(raw, url, strat)
            if f.exists():
                lh = json.loads(f.read_text()).get("lighthouseResult", {})
                out[(label, strat)] = lh
    return out


def load_seo(raw):
    out = {}
    for label, url in DEFAULT_URLS:
        slug = "".join(c if c.isalnum() else "_" for c in url)[:80]
        f = raw / f"{slug}.seo.json"
        if f.exists():
            out[label] = json.loads(f.read_text()).get("html", "")
    return out


def load_crawl(raw):
    f = raw / "crawl.json"
    return json.loads(f.read_text()) if f.exists() else None


class RichPage(Page):
    """seo.py's Page, plus the specifics findings needs: image srcs and heading text."""

    def __init__(self):
        super().__init__()
        self.img_list = []        # (src, alt-or-None)
        self.heading_list = []    # [level, text]
        self._cur_h = None

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        a = dict(attrs)
        if tag == "img":
            self.img_list.append((a.get("src", ""), a.get("alt")))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_h = [int(tag[1]), ""]
            self.heading_list.append(self._cur_h)

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_h = None

    def handle_data(self, data):
        super().handle_data(data)
        if self._cur_h is not None:
            self._cur_h[1] += data


def parse_page(html):
    p = RichPage()
    p.feed(html or "")
    return p


# ── domain extractors: each returns a list of finding dicts ──────────────────
def F(title, what, why, source, target, measured, golden, site, evidence):
    return dict(title=title, what=what, why=why, source=source, target=target,
                measured=measured, golden=golden, site=site, evidence=evidence)


def a11y_findings(psi, crawl):
    agg = {}   # rule -> {pages:set, nodes:{selector:snippet}, title}
    for (label, strat), lh in psi.items():
        cat = lh.get("categories", {}).get("accessibility", {})
        au = lh.get("audits", {})
        for ref in cat.get("auditRefs", []):
            a = au.get(ref["id"], {})
            if a.get("scoreDisplayMode") == "binary" and a.get("score") == 0:
                e = agg.setdefault(ref["id"], {"pages": set(), "nodes": {}, "title": a.get("title", "")})
                e["pages"].add(f"{label} — {strat}")
                for it in a.get("details", {}).get("items", []):
                    nd = it.get("node", {}) or {}
                    sel = nd.get("selector") or ""
                    if sel:
                        e["nodes"][sel] = (nd.get("snippet") or "").strip()
    out = []
    for rule in sorted(agg, key=lambda r: (-len(agg[r]["nodes"]), r)):
        e = agg[rule]
        what, why = A11Y_KNOW.get(rule, (e["title"] or rule, "Failing axe-core accessibility check."))
        nodes = sorted(e["nodes"].items())
        ev = []
        for sel, snip in nodes[:3]:
            ev.append(f"`{trunc(sel, 100)}`")
            if snip:
                ev.append(f"  ↳ {trunc(snip, 120)}")
        if len(nodes) > 3:
            ev.append(f"(+{len(nodes) - 3} more node(s) — see raw/*.psi.json)")
        out.append(F(
            f"{rule} — {len(nodes)} node(s)", what, why,
            f"PSI Lighthouse · accessibility · `{rule}`",
            "0 failing a11y audits (BASELINE §D)", f"{len(nodes)} node(s), {len(e['pages'])} run(s)",
            ", ".join(sorted(e["pages"])), "", ev))
    # sitewide prevalence (crawl rollup) — coarse page-level flags
    texts = rollup_texts(crawl)
    n = len(table_rows(crawl.get("tables", {}), "seo"))
    no_alt, no_aria, no_roles = (count_for(texts, "without image alt"),
                                 count_for(texts, "without aria"),
                                 count_for(texts, "without role"))
    if no_alt or no_aria or no_roles:
        out.append(F(
            "Sitewide a11y prevalence",
            "How widespread the golden-path a11y gaps are across all pages.",
            "SiteOne's blunt page-level flags — one missing-alt image flags the whole page. They show prevalence, not per-node detail; the PSI rules above are authoritative for the golden path.",
            "SiteOne crawl · summary rollup",
            "0 pages (BASELINE §F)", f"alt {no_alt}, aria {no_aria}, roles {no_roles} of {n}",
            "", f"{n} pages crawled",
            [f"{no_alt} page(s) with an image missing alt",
             f"{no_aria} page(s) flagged without aria labels",
             f"{no_roles} page(s) flagged without role attributes"]))
    return out


def seo_findings(seo_html, crawl):
    tables = crawl.get("tables", {})
    texts = rollup_texts(crawl)
    seo_rows = table_rows(tables, "seo")
    n = len(seo_rows)
    parsed = {lbl: parse_page(html) for lbl, html in seo_html.items()}
    out = []

    # 1 — missing meta descriptions
    miss_desc = sorted((r.get("urlPathAndQuery") or "/") for r in seo_rows
                       if not (r.get("description") or "").strip())
    g_desc = [lbl for lbl, p in parsed.items() if not p.metas.get("description", "").strip()]
    if miss_desc or g_desc:
        out.append(F(
            "Missing meta descriptions",
            "Pages with no <meta name=description>.",
            "Google then invents the SERP snippet from page text — usually worse copy, lower click-through. On Shopify, collection/policy/system pages have none unless the theme or admin sets one.",
            "SiteOne crawl · seo table  ·  seo.py · golden path",
            "Every page (BASELINE §E + §F)", f"{len(miss_desc)} of {n} sitewide; golden: {', '.join(g_desc) or 'none'}",
            ", ".join(g_desc), f"{len(miss_desc)} / {n}",
            [p for p in miss_desc] or ["(none sitewide)"]))

    # 2 — heading structure (single-h1 + order)
    multi_h1 = count_for(texts, "multiple <h1>")
    skipped = count_for(texts, "skipped heading")
    head_rows = sorted((r for r in table_rows(tables, "seo-headings")
                        if int(r.get("headingsErrorsCount") or 0) > 0),
                       key=lambda r: (-int(r.get("headingsErrorsCount") or 0), r.get("urlPathAndQuery") or ""))
    ev = []
    for lbl, p in parsed.items():
        if p.h1 != 1 or not head_ok(p.headings):
            tree = " → ".join(f"h{lv}" for lv in p.headings[:12]) + ("…" if len(p.headings) > 12 else "")
            ev.append(f"golden {lbl}: {p.h1} h1, order {'ok' if head_ok(p.headings) else 'BROKEN'} — {tree}")
    for r in head_rows[:8]:
        levels = re.findall(r"<h([1-6])", r.get("headings") or "")
        tree = " → ".join(f"h{lv}" for lv in levels[:12]) + ("…" if len(levels) > 12 else "")
        ev.append(f"{r.get('urlPathAndQuery')}: {r.get('headingsErrorsCount')} error(s) — {tree}")
    if len(head_rows) > 8:
        ev.append(f"(+{len(head_rows) - 8} more page(s) with heading errors)")
    if ev:
        out.append(F(
            "Heading structure (single H1 + order)",
            "Pages with no/multiple H1 or a skipped heading level.",
            "Headings are the outline assistive tech and search engines read. A skipped level (h1→h3) or a second h1 breaks that outline. In Dawn, section/card heading levels (h2/h3/h5) drift when sections are reordered or a banner ships an h1.",
            "SiteOne crawl · seo-headings  ·  seo.py · golden path",
            "Single H1 + ordered headings, all pages (BASELINE §E/§F)",
            f"{multi_h1} multi-H1, {skipped} skipped-level of {n}",
            ", ".join(lbl for lbl, p in parsed.items() if p.h1 != 1 or not head_ok(p.headings)),
            f"{len(head_rows)} / {n} pages with heading errors", ev))

    # 3 — image alt coverage (golden specifics; node detail is in A11Y)
    ev, g_alt = [], []
    for lbl, p in parsed.items():
        missing = [src for src, alt in p.img_list if alt is None or not (alt or "").strip()]
        if missing:
            g_alt.append(lbl)
            ev.append(f"golden {lbl}: {len(missing)} of {len(p.img_list)} img(s) missing alt")
            for src in missing[:3]:
                ev.append(f"  ↳ {short_url(src)}")
            if len(missing) > 3:
                ev.append(f"  (+{len(missing) - 3} more on this page)")
    if ev:
        out.append(F(
            "Image alt coverage",
            "Images on the page with no alt attribute (coverage, not quality).",
            "Same gap as the A11Y image-alt rule, seen from the SEO side. Coverage only — whether the alt that exists is meaningful is the manual pass. Product/card images get alt from the admin image alt or the theme <img>.",
            "seo.py · golden path",
            "All images have alt (BASELINE §E)", f"golden pages failing: {', '.join(g_alt)}",
            ", ".join(g_alt), "", ev))

    # 4 — Open Graph / Twitter
    og_rows = table_rows(tables, "open-graph")
    og_miss = sorted((r.get("urlPathAndQuery") or "/") for r in og_rows
                     if not (r.get("ogTitle") or "").strip() or not (r.get("ogImage") or "").strip())
    ev = []
    for lbl, p in parsed.items():
        gone = [r.replace("og:", "") for r in OG_REQUIRED if not p.metas.get(r)]
        if gone:
            ev.append(f"golden {lbl}: missing {', '.join(gone)}")
    if ev or og_miss:
        ev += [f"sitewide: {len(og_miss)} of {n} page(s) missing og:title or og:image"]
        out.append(F(
            "Open Graph / Twitter tags",
            "Pages missing og:title/og:image (and the rest of the OG/Twitter set).",
            "These control the link preview when the page is shared (social, iMessage, etc.). Missing them = an ugly or blank share card. Set in the theme <head>; Dawn ships them but custom templates can drop them.",
            "seo.py · golden path  ·  SiteOne crawl · open-graph",
            "OG/Twitter present, all pages", f"{len(og_miss)} of {n} sitewide",
            ", ".join(lbl for lbl, p in parsed.items()
                      if any(not p.metas.get(r) for r in OG_REQUIRED)),
            f"{len(og_miss)} / {n}", ev))

    # 5 — duplicate titles
    dups = [r for r in table_rows(tables, "non-unique-titles") if (r.get("title") or "").strip()]
    if dups:
        out.append(F(
            "Duplicate page titles",
            "Two or more pages share an identical <title>.",
            "Search engines can't tell the pages apart and may pick the wrong one to rank. Usually two collections/pages built from the same title source.",
            "SiteOne crawl · non-unique-titles",
            "0 duplicate titles (BASELINE §F)", f"{len(dups)} duplicated title(s)",
            "", "", [f'"{trunc(r.get("title"), 70)}" ×{r.get("count")}' for r in dups]))

    # 6 — broken links
    broken = table_rows(tables, "404")
    if broken:
        out.append(F(
            "Broken links (4xx/5xx)",
            "A linked URL returns an error status.",
            "Dead end for users and crawlers; wastes crawl budget and leaks link equity. Fix the link or restore/redirect the target.",
            "SiteOne crawl · 404 table",
            "0 broken links (BASELINE §F)", f"{len(broken)} broken",
            "", "", [f"{r.get('url')} ({r.get('statusCode')})" for r in broken]))
    return out


# Performance opportunity audits: friendly name + candidate ids (first present wins).
PERF_AUDITS = [
    ("Total byte weight", ["total-byte-weight"]),
    ("Unused JavaScript", ["unused-javascript"]),
    ("JS bootup (parse/compile/exec)", ["bootup-time"]),
    ("Main-thread work", ["mainthread-work-breakdown"]),
    ("Render-blocking resources", ["render-blocking-resources"]),
    ("Responsive / modern images", ["uses-responsive-images", "modern-image-formats", "uses-optimized-images"]),
    ("Legacy JavaScript", ["legacy-javascript"]),
]


def _item_url(it):
    s = it.get("source")
    if isinstance(s, dict):
        s = s.get("url")
    return it.get("url") or s or it.get("groupLabel") or it.get("group") or ""


def _item_bytes(it):
    return it.get("wastedBytes") or it.get("totalBytes") or it.get("transferSize") or 0


def _item_ms(it):
    return it.get("wastedMs") or it.get("duration") or it.get("blockingTime") or it.get("total") or 0


def perf_findings(psi):
    out = []
    # overview: lab + field per page×device
    ev = []
    for label, url in DEFAULT_URLS:
        for strat in STRATS:
            lh = psi.get((label, strat))
            if not lh:
                continue
            au = lh.get("audits", {})

            def num(aid, div=1000, nd=2):
                v = au.get(aid, {}).get("numericValue")
                return round(v / div, nd) if v is not None else "—"
            perf = lh.get("categories", {}).get("performance", {}).get("score")
            perf = round(perf * 100) if perf is not None else "—"
            warns = lh.get("runWarnings") or []
            cut = " ✗cut" if any("loaded too slowly" in w.lower() for w in warns) else ""
            ev.append(f"{label} — {strat}: perf {perf}{cut} · LCP {num('largest-contentful-paint')}s · "
                      f"TBT {num('total-blocking-time', 1, 0)}ms · SI {num('speed-index')}s · "
                      f"CLS {num('cumulative-layout-shift', 1, 3)}")
    # field verdict (CrUX) per page — pulled from the full PSI doc would need loadingExperience;
    # the scorecard §C already carries it. Note it here as context.
    out.append(F(
        "Lab performance below target (mobile)",
        "Lighthouse Performance score and the lab metrics behind it, per page × device.",
        "PSI's mobile run is a fixed heavy throttle (Moto G4 / slow-4G / 4× CPU), so mobile scores run far below desktop and a heavy page can be cut before network-idle (LCP marked ✗cut — treat that LCP as unknown, not as the failure). Cross-check the real-user verdict in baseline.md §C: CrUX may already pass even where lab fails. The MISSION target is still lab ≥ 90.",
        "PSI Lighthouse · performance",
        "Performance ≥ 90, mobile + desktop (MISSION 3)", "mobile 46–72, desktop 68–72 (see §A)",
        "all golden pages, mobile", "", ev))

    # opportunity audits — aggregate across the 3 mobile runs (where perf hurts)
    for name, ids in PERF_AUDITS:
        merged = {}   # url -> (bytes, ms)
        used = None
        for label, url in DEFAULT_URLS:
            lh = psi.get((label, "mobile"))
            if not lh:
                continue
            au = lh.get("audits", {})
            for aid in ids:
                a = au.get(aid)
                items = a.get("details", {}).get("items") if a else None
                if items:
                    used = aid
                    for it in items:
                        k = _item_url(it) or "(unknown)"
                        b, m = _item_bytes(it), _item_ms(it)
                        pb, pm = merged.get(k, (0, 0))
                        merged[k] = (max(pb, b), max(pm, m))
                    break
        if not merged:
            continue
        rows = sorted(merged.items(), key=lambda kv: (-(kv[1][0]), -(kv[1][1]), kv[0]))
        ev = []
        for k, (b, m) in rows[:8]:
            parts = [short_url(k)]
            if b:
                parts.append(kb(b))
            if m:
                parts.append(ms(m))
            ev.append(" · ".join(parts))
        if len(rows) > 8:
            ev.append(f"(+{len(rows) - 8} more — see raw/*.psi.json)")
        tot_b = sum(b for _, (b, _) in rows)
        tot_m = sum(m for _, (_, m) in rows)
        measured = (f"{kb(tot_b)} across {len(rows)}" if tot_b else f"{ms(tot_m)} across {len(rows)}")
        out.append(F(
            name, f"PSI opportunity/diagnostic: {name.lower()}.",
            "Each entry is a real resource Lighthouse flagged on the mobile run — the JS/CSS/image bytes and main-thread time dragging the score. These are the levers behind the low mobile Performance number.",
            f"PSI Lighthouse · `{used}` (mobile runs)",
            "Performance ≥ 90 (MISSION 3)", measured,
            "golden pages, mobile", "", ev))
    return out


def sec_findings(crawl):
    tables = crawl.get("tables", {})
    texts = rollup_texts(crawl)
    out = []
    want = [("Strict-Transport-Security", "HSTS"), ("Content-Security-Policy", "CSP"),
            ("Referrer-Policy", "Referrer-Policy"), ("Permissions-Policy", "Permissions-Policy")]
    recs = {r.get("header"): r for r in table_rows(tables, "security")}
    ev = []
    for hdr, short in want:
        if not header_set(tables, hdr):
            r = recs.get(hdr, {})
            ev.append(f"{short}: not set — {trunc(r.get('recommendation', ''), 110)}")
    if ev:
        out.append(F(
            "Missing security response headers",
            "Standard hardening headers absent from responses.",
            "These reduce XSS, clickjacking, and referrer-leak exposure. On Shopify (hosted, Advanced plan) the platform sets some headers and limits what a theme can add — CSP/HSTS especially may be platform-controlled. Confirm what's actually settable before treating each as fully fixable.",
            "SiteOne crawl · security table",
            "All present (BASELINE §F)", f"{len(ev)} of {len(want)} missing",
            "", "all responses", ev))
    # CORS wildcard, if flagged
    cors = recs.get("Access-Control-Allow-Origin")
    if cors and (int(cors.get("critical") or 0) + int(cors.get("warning") or 0)) > 0:
        out.append(F(
            "Access-Control-Allow-Origin: *",
            "A response allows any origin to read it.",
            "Usually fine for public CDN assets, a risk if it's on anything credentialed. Check which responses carry it.",
            "SiteOne crawl · security table",
            "No over-permissive CORS", "flagged",
            "", "flagged responses", [trunc(cors.get("recommendation", ""), 140)]))
    # Brotli
    no_brotli = count_for(texts, "brotli")
    if no_brotli:
        n = len(table_rows(tables, "seo"))
        out.append(F(
            "No Brotli compression",
            "Responses aren't served with Brotli.",
            "Brotli beats gzip on text (HTML/CSS/JS), trimming transfer bytes. On Shopify this is largely platform-controlled — likely not theme-fixable; record as a platform note unless proven otherwise.",
            "SiteOne crawl · summary rollup",
            "Brotli on (BASELINE §F)", f"{no_brotli} of {n} pages",
            "", f"{no_brotli} / {n}", [f"{no_brotli} page(s) served without Brotli"]))
    return out


def bp_findings(psi, crawl):
    out = []
    # PSI best-practices failures aggregated across runs
    agg = {}
    for (label, strat), lh in psi.items():
        cat = lh.get("categories", {}).get("best-practices", {})
        au = lh.get("audits", {})
        for ref in cat.get("auditRefs", []):
            a = au.get(ref["id"], {})
            if a.get("score") is not None and a.get("score") < 1 and a.get("scoreDisplayMode") in ("binary", "numeric", "metricSavings"):
                e = agg.setdefault(ref["id"], {"pages": set(), "title": a.get("title", ""), "items": {}})
                e["pages"].add(f"{label} — {strat}")
                for it in a.get("details", {}).get("items", []):
                    desc = it.get("description") or it.get("reason") or _item_url(it) or ""
                    if desc:
                        e["items"][trunc(desc, 120)] = True
    for aid in sorted(agg, key=lambda a: (-len(agg[a]["pages"]), a)):
        e = agg[aid]
        what, why = BP_KNOW.get(aid, (e["title"] or aid, "Lighthouse best-practice failure."))
        ev = list(e["items"])[:4]
        if len(e["items"]) > 4:
            ev.append(f"(+{len(e['items']) - 4} more)")
        out.append(F(
            f"{aid}", what, why,
            f"PSI Lighthouse · best-practices · `{aid}`",
            "Best Practices ≥ 95 (MISSION)", f"on {len(e['pages'])} run(s)",
            ", ".join(sorted(e["pages"])), "", ev or ["(see raw/*.psi.json)"]))
    # crawl structural
    texts = rollup_texts(crawl)
    n = len(table_rows(crawl.get("tables", {}), "seo"))
    for needle, title, why in [
        ("invalid inline svg", "Invalid inline SVG",
         "Malformed inline SVG markup — can render wrong or bloat the DOM. Usually a theme snippet or app-injected icon."),
        ("duplicated inline svg", "Duplicated inline SVG",
         "The same SVG inlined many times instead of defined once and referenced (<use>). Minor HTML bloat; common in Dawn — low priority."),
        ("non-clickable", "Non-clickable phone number",
         "A phone number shown as text with no tel: link. On mobile it can't be tapped to call."),
    ]:
        c = count_for(texts, needle)
        if c:
            out.append(F(
                title, f"{c} page(s) flagged: {needle}.", why,
                "SiteOne crawl · summary rollup",
                "0 pages (BASELINE §F)", f"{c} of {n}",
                "", f"{c} / {n}", [f"{c} page(s) flagged — see crawl.html"]))
    return out


# ── render ───────────────────────────────────────────────────────────────────
def render_finding(fid, f):
    L = [f"### {fid} · {f['title']}",
         f"- **What / why:** {f['what']} {f['why']}",
         f"- **Source:** {f['source']}",
         f"- **Target → measured:** {f['target']} → {f['measured']}"]
    scope = []
    if f["golden"]:
        scope.append(f"golden path: {f['golden']}")
    if f["site"]:
        scope.append(f"sitewide: {f['site']}")
    if scope:
        L.append(f"- **Scope:** {' · '.join(scope)}")
    L.append("- **Evidence:**")
    L += [f"  - {line}" for line in f["evidence"]]
    return L


DOMAINS = [
    ("A11Y", "Accessibility", "MISSION priority 1"),
    ("SEO", "SEO & discoverability", "MISSION priority 2"),
    ("PERF", "Performance", "MISSION priority 3"),
    ("SEC", "Security", ""),
    ("BP", "Best practices / structure", ""),
]


def main():
    args = sys.argv[1:]
    rd = Path(args[args.index("--run-dir") + 1]) if "--run-dir" in args else latest_run_dir()
    out = Path(args[args.index("--out") + 1]) if "--out" in args else rd / "findings.md"
    raw = rd / "raw"
    if not raw.is_dir():
        sys.exit(f"✗ no raw/ in {rd}")

    psi = load_psi(raw)
    seo_html = load_seo(raw)
    crawl = load_crawl(raw)
    if crawl is None:
        sys.exit(f"✗ no crawl.json in {raw}")

    sections = {
        "A11Y": a11y_findings(psi, crawl),
        "SEO": seo_findings(seo_html, crawl),
        "PERF": perf_findings(psi),
        "SEC": sec_findings(crawl),
        "BP": bp_findings(psi, crawl),
    }

    site = urllib.parse.urlparse(DEFAULT_URLS[0][1])
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(len(v) for v in sections.values())
    L = [
        f"# Findings — {rd.name}",
        "",
        f"Site: {site.scheme}://{site.netloc}/ · Generated {stamp} by `hobbes/tools/findings.py` from `raw/`.",
        "",
        f"The problem catalog — dense, deterministic, agent-facing. {total} findings. "
        "Numbers and scorecard in `baseline.md`; the fix, effort, and impact are the **plan's** job, not this file's. "
        "See `hobbes/scorecards/FINDINGS-TEMPLATE.md`.",
    ]
    for key, name, note in DOMAINS:
        items = sections[key]
        L += ["", f"## {key} — {name}" + (f"  ({note})" if note else "")]
        if not items:
            L += ["", "— all checks pass."]
            continue
        for i, f in enumerate(items, 1):
            L += [""]
            L += render_finding(f"{key}-{i}", f)
    report = "\n".join(L) + "\n"
    out.write_text(report)
    print(report)
    print(f"→ {total} findings written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
