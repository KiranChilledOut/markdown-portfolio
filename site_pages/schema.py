"""Open schema generator: JSON Resume + Schema.org Person.

Produces two machine-readable representations of the portfolio, both derived
from the same inputs -- the parsed identity config (``site.yml``) and the
content records loaded from ``content/`` by :mod:`site_pages.loader`:

1. A **JSON Resume** document (https://jsonresume.org/spec/) served at
   ``/.well-known/portfolio.json``. Spec-strict for ``basics`` and ``projects``;
   blog posts and tutorials have no native JSON Resume home, so they're exposed
   under a clearly-namespaced ``_extensions`` block (leading underscore marks it
   as non-spec; spec-strict consumers ignore it).
2. A **Schema.org ``Person``** JSON-LD blob, embedded inline in the page
   ``<head>`` for crawlers.

Both generators are pure functions of their inputs, which makes them trivial to
test and reuse.
"""
from __future__ import annotations

from typing import Any

from . import loader
from .context_processors import load_site_config

# Map site.yml link keys (and the networks agents care about) to JSON Resume
# ``basics.profiles[].network`` labels. Any link not in the map is kept with a
# title-cased key so nothing is silently dropped.
_NETWORK_LABELS = {
    "github": "GitHub",
    "linkedin": "LinkedIn",
    "twitter": "Twitter",
    "mastodon": "Mastodon",
    "website": "Website",
    "youtube": "YouTube",
}


def _network_label(key: str) -> str:
    return _NETWORK_LABELS.get(key, key.replace("_", " ").title())


def build_json_resume(site: dict | None = None) -> dict[str, Any]:
    """Build a JSON Resume document from site identity + content records.

    ``site`` defaults to the parsed ``site.yml``. Pass an explicit dict in tests
    to avoid touching the filesystem.
    """
    site = site if site is not None else load_site_config()
    links = site.get("links") or {}

    basics: dict[str, Any] = {
        "name": site.get("name") or "",
        "label": site.get("label") or "",
    }
    if site.get("email"):
        basics["email"] = site["email"]
    if site.get("base_url"):
        basics["url"] = site["base_url"]
    if site.get("location"):
        basics["location"] = {"address": site["location"]}
    profiles = [{"network": _network_label(k), "url": v} for k, v in links.items() if v]
    if profiles:
        basics["profiles"] = profiles

    # Projects map cleanly onto the JSON Resume "projects" section.
    projects = [_project_to_resume(p) for p in loader.load_collection("projects")]
    doc: dict[str, Any] = {"basics": basics}
    if projects:
        doc["projects"] = projects

    # Blog + tutorials have no JSON Resume home; expose under a namespaced
    # extension so the doc stays spec-strict but the writing is still readable.
    posts = _summaries(loader.load_collection("blog"))
    tutorials = _summaries(loader.load_collection("tutorials"))
    if posts or tutorials:
        doc["_extensions"] = {
            "schema": "https://portfolio-template.dev/extensions/v1",
            "posts": posts,
            "tutorials": tutorials,
        }
    return doc


def _project_to_resume(p: dict) -> dict[str, Any]:
    """Map one portfolio project record to a JSON Resume ``projects`` entry."""
    entry: dict[str, Any] = {
        "name": p.get("title") or p["slug"],
        "summary": p.get("summary") or "",
        "slug": p["slug"],
    }
    if p.get("tech"):
        entry["keywords"] = list(p["tech"])
    links = p.get("links") or {}
    if links.get("github"):
        entry["repo"] = links["github"]
    if links.get("live"):
        entry["url"] = links["live"]
    if p.get("date"):
        entry["startDate"] = p["date"].isoformat()
    return entry


def _summaries(records: list[dict]) -> list[dict[str, Any]]:
    """Reduce a collection to the lightweight fields useful for indexing."""
    out = []
    for r in records:
        entry: dict[str, Any] = {
            "slug": r["slug"],
            "title": r.get("title") or r["slug"],
            "summary": r.get("summary") or "",
        }
        if r.get("date"):
            entry["date"] = r["date"].isoformat()
        if r.get("tags"):
            entry["tags"] = list(r["tags"])
        out.append(entry)
    return out


def build_person_jsonld(site: dict | None = None) -> dict[str, Any]:
    """Build a Schema.org ``Person`` JSON-LD object for crawlers."""
    site = site if site is not None else load_site_config()
    person: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": site.get("name") or "",
    }
    if site.get("base_url"):
        person["url"] = site["base_url"]
    if site.get("email"):
        person["email"] = site["email"]
    same_as = [v for v in (site.get("links") or {}).values() if v]
    if same_as:
        person["sameAs"] = same_as

    # knowsAbout = union of all project tech + post/tutorial tags.
    knows: set[str] = set()
    for p in loader.load_collection("projects"):
        knows.update(p.get("tech") or [])
    for kind in ("blog", "tutorials"):
        for r in loader.load_collection(kind):
            knows.update(r.get("tags") or [])
    if knows:
        person["knowsAbout"] = sorted(knows)
    return person
