#!/usr/bin/env python3
"""
config.py — the single source of per-client config for every tool.

Replaces the hardcoded DEFAULT_URLS (psi.py + the old duplicate in seo.py) and
the CONFIG dict (baseline.py) with one `hobbes.toml`. Secrets never live in the
toml — psi_key() reads $PSI_API_KEY (a repo secret in CI).
"""

import tomllib
from datetime import datetime
from functools import lru_cache
from os import environ
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

HOBBES = Path(__file__).resolve().parent.parent   # .../<repo>/hobbes
_TOML = HOBBES / "hobbes.toml"
_DEFAULT_TZ = "America/Chicago"


def _tz():
    """The cycle's pinned timezone — one source, so a local run (any machine TZ)
    and CI (UTC) always land on the same calendar day. Set [cycle].timezone."""
    return ZoneInfo(cfg().get("cycle", {}).get("timezone", _DEFAULT_TZ))


def today():
    """Cycle-folder date in the pinned timezone — never off-by-one between local and CI."""
    return datetime.now(_tz()).strftime("%Y-%m-%d")


def stamp():
    """Human timestamp for digests — pinned timezone, labelled (e.g. 'CDT'), one source."""
    return datetime.now(_tz()).strftime("%Y-%m-%d %H:%M %Z")


@lru_cache(maxsize=1)
def cfg():
    return tomllib.loads(_TOML.read_text())


def _page_label(url):
    """A short, client-agnostic page label derived from the URL: the first path
    directory (e.g. '/collections'), or '/' for the site root. No hardcoded page
    names, so the same code labels any site — a storefront, a blog, an app — from
    its own URLs."""
    seg = urlsplit(url).path.strip("/").split("/")[0]
    return f"/{seg}" if seg else "/"


def golden_path():
    """The locked golden path as [(label, url)], in config order. Each [[golden_path]]
    entry has a url and an optional label; when label is omitted it's derived from the
    url (see _page_label). No fixed keys or page types — client- and platform-agnostic
    for any number of pages."""
    return [(p.get("label") or _page_label(p["url"]), p["url"]) for p in cfg()["golden_path"]]


def client_meta():
    """The [client] block: name / site / platform / run_by."""
    return cfg()["client"]


def effort_budget():
    """Effort points an execute batch may spend — single source for the CLI and CI."""
    return int(cfg().get("cycle", {}).get("effort_budget", 10))


def sample_path():
    """The high-volume URL substring the crawler subsamples (e.g. '/products/' on a
    storefront, '/blog/' on a content site), from [cycle].sample_path. None when unset
    — the crawler then takes every page, no subsampling. Client-agnostic: the pattern
    lives in config, not in the code."""
    return cfg().get("cycle", {}).get("sample_path") or None


def psi_key():
    """The PageSpeed key from $PSI_API_KEY, else None. CI injects it from the repo secret."""
    return environ.get("PSI_API_KEY", "").strip() or None
