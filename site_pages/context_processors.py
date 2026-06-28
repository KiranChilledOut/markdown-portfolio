"""Context processor exposing site identity (``site.yml``) to every template.

The templates read name/links/resume/brand from ``SITE`` rather than hard-coding
them, so the same codebase serves many people — identity lives in one config
file. Parsing is cached by file mtime (mirrors :mod:`site_pages.loader`), so
editing ``site.yml`` invalidates the cache on the next request with no restart.

If the config is missing or broken, a safe fallback is returned so a misconfig
never takes the whole site down.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import yaml
from django.conf import settings

log = logging.getLogger(__name__)

# Safe, generic identity used when site.yml is absent or unparseable. The site
# stays up; the admin sees a warning in the logs.
SAFE_FALLBACK: dict = {
    "name": "Your Name",
    "label": "",
    "location": None,
    "email": None,
    "base_url": "",
    "links": {},
    "resume": {"path": "site_pages/resume.pdf", "download_name": "resume.pdf"},
    "brand": "•",
    "theme": {"default": "auto"},
}

# Sections that appear in the nav (kind -> url name). Order in the list = order
# in the nav. ``about`` is special (single page, not a content collection).
DEFAULT_SECTIONS = [
    {"kind": "projects", "label": "Projects"},
    {"kind": "tutorials", "label": "Tutorials"},
    {"kind": "blog", "label": "Blog"},
    {"kind": "about", "label": "About"},
]
_SECTION_URL_NAMES = {
    "projects": "site_pages:project_list",
    "tutorials": "site_pages:tutorial_list",
    "blog": "site_pages:blog_list",
    "about": "site_pages:about",
}
# Content kinds (drives home "featured" + schema), excluding the about page.
_CONTENT_KINDS = ("projects", "tutorials", "blog")


def _config_path() -> Path:
    return Path(getattr(settings, "SITE_CONFIG", Path(settings.BASE_DIR) / "site.yml"))


@lru_cache(maxsize=8)
def _load_cached(mtime: int, path_str: str) -> dict:
    """Load + parse site.yml. Cached by mtime; stale mtime = fresh read."""
    try:
        text = Path(path_str).read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
    except FileNotFoundError:
        log.warning("site.yml not found at %s; using identity fallback", path_str)
        return dict(SAFE_FALLBACK)
    except yaml.YAMLError as exc:
        log.warning("site.yml is unparseable (%s); using identity fallback", exc)
        return dict(SAFE_FALLBACK)

    if not isinstance(data, dict):
        log.warning("site.yml top level must be a mapping; using identity fallback")
        return dict(SAFE_FALLBACK)

    # Merge over the fallback so every key templates can rely on is present.
    merged = dict(SAFE_FALLBACK)
    merged.update(data)
    merged.setdefault("links", {})
    merged.setdefault("resume", SAFE_FALLBACK["resume"])
    merged.setdefault("theme", SAFE_FALLBACK["theme"])
    # Resolve the sections config into a nav-friendly list with url + content
    # kind flags. Falls back to DEFAULT_SECTIONS when absent or malformed.
    merged["sections"] = _resolve_sections(merged.get("sections"))
    return merged


def _resolve_sections(raw) -> list[dict]:
    """Turn the ``sections:`` list from site.yml into nav-ready entries.

    Each entry gets: kind, label, url (reversed), and is_content (bool — a
    content collection vs the about page). Unknown kinds are dropped with a
    warning; an empty/missing list yields the four default sections so a
    missing config never hides everything.
    """
    from django.urls import NoReverseMatch, reverse  # local import avoids load cycle

    if not isinstance(raw, list) or not raw:
        raw = DEFAULT_SECTIONS

    resolved = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        kind = entry.get("kind")
        if kind not in _SECTION_URL_NAMES:
            log.warning("Unknown section kind %r in site.yml; skipping", kind)
            continue
        label = entry.get("label") or kind.title()
        try:
            url = reverse(_SECTION_URL_NAMES[kind])
        except NoReverseMatch:
            continue
        resolved.append({
            "kind": kind,
            "label": label,
            "url": url,
            "is_content": kind in _CONTENT_KINDS,
        })
    if not resolved:
        # Every entry was bad — fall back rather than show an empty nav.
        return _resolve_sections(DEFAULT_SECTIONS)
    return resolved


def load_site_config() -> dict:
    """Return the parsed site.yml identity, mtime-cached."""
    path = _config_path()
    try:
        mtime = int(path.stat().st_mtime)
    except OSError:
        return dict(SAFE_FALLBACK)
    return _load_cached(mtime, str(path))


def site(request):  # noqa: ANN001  (Django calls with a HttpRequest)
    """Template context processor: injects the parsed site.yml as ``SITE``."""
    return {"SITE": load_site_config()}


def person_jsonld(request):  # noqa: ANN001
    """Inject Schema.org Person JSON-LD (for crawlers) into every page."""
    from . import schema  # local import avoids circular at module load
    import json

    blob = schema.build_person_jsonld()
    return {"PERSON_JSONLD": json.dumps(blob, ensure_ascii=False)}
