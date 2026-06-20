#!/usr/bin/env python3
"""
config.py — the single source of per-client config for every tool.

Replaces the hardcoded DEFAULT_URLS (psi.py + the old duplicate in seo.py) and
the CONFIG dict (baseline.py) with one `hobbes.toml`. Secrets never live in the
toml — it names where to find them, and psi_key() resolves env var, then file.
"""

import tomllib
from datetime import datetime
from functools import lru_cache
from os import environ
from pathlib import Path
from zoneinfo import ZoneInfo

HOBBES = Path(__file__).resolve().parent.parent   # .../<repo>/hobbes
REPO = HOBBES.parent                                # .../<repo>
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


def golden_path():
    """The locked golden path as [(label, url)] — same shape the tools expect."""
    g = cfg()["golden_path"]
    return [("Home", g["home"]), ("Collection", g["collection"]), ("Product", g["product"])]


def client_meta():
    """The [client] block: name / site / platform / run_by."""
    return cfg()["client"]


def effort_budget():
    """Effort points an execute batch may spend — single source for the CLI and CI."""
    return int(cfg().get("cycle", {}).get("effort_budget", 10))


def psi_key():
    """The PageSpeed key from the named env var, else the repo-relative file, else None."""
    s = cfg()["secrets"]
    key = environ.get(s["psi_key_env"], "").strip()
    if key:
        return key
    f = REPO / s["psi_key_file"]
    if f.exists():
        raw = f.read_text().strip()
        return raw.split("=", 1)[1].strip() if "=" in raw else raw
    return None
