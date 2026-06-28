"""File-based markdown content engine.

Content lives under ``content/`` at the project root, one ``.md`` file per
page/post/project/tutorial. Each file begins with YAML front matter delimited
by ``---`` lines, followed by a markdown body. This module parses the files,
renders the markdown body to HTML (cached per-file by mtime so ``git pull``
invalidates the cache automatically) and exposes a small read-only API to
the views.

There is no database involvement for content -- the filesystem is the source
of truth.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import markdown
import yaml
from django.conf import settings
from django.core.cache import cache
from django.http import Http404

# Kinds we know how to serve. Maps a URL-friendly kind to a content subdir.
KINDS = ("projects", "tutorials", "blog", "pages")

CONTENT_DIR: Path = Path(getattr(settings, "CONTENT_DIR", Path(settings.BASE_DIR) / "content"))

# Default sort order per kind: blog/projects newest first, tutorials by order.
_SORT_DESC = {"blog", "projects"}

# Markdown extensions + config are declared in settings so they can be tuned
# without touching this module (see portfolio_site/settings.py).
_EXTENSIONS = getattr(settings, "MARKDOWN_EXTENSIONS", ["markdown.extensions.extra"])
_EXTENSION_CONFIGS = getattr(settings, "MARKDOWN_EXTENSION_CONFIGS", {})


class ContentError(Exception):
    """Raised when a content file is malformed."""


def _split_front_matter(text: str) -> tuple[dict, str]:
    """Split a markdown file into (front_matter_dict, body).

    Front matter is an optional YAML block enclosed by ``---`` delimiters at
    the very top of the file. If absent, an empty dict is returned.
    """
    if not text.startswith("---"):
        return {}, text

    # Split on the closing ``---`` that ends the front matter block. Use
    # splitlines-style logic so any line-ending works.
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        # Try CRLF / trailing-newline variants.
        parts = text.split("---\r\n", 2)
    if len(parts) < 3:
        raise ContentError("Front matter block was not closed with a '---' line")

    meta_yaml = parts[1]
    body = parts[2]
    meta = yaml.safe_load(meta_yaml) or {}
    if not isinstance(meta, dict):
        raise ContentError("Front matter must be a YAML mapping")
    return meta, body


def _render_body(body: str) -> str:
    """Render a markdown string to HTML."""
    md = markdown.Markdown(
        extensions=_EXTENSIONS,
        extension_configs=_EXTENSION_CONFIGS,
        output_format="html5",
    )
    return md.convert(body)


def _parse_file(path: Path, slug: str) -> dict:
    """Read, parse and (cached by mtime) render a single content file."""
    try:
        mtime = int(path.stat().st_mtime)
    except FileNotFoundError as exc:
        raise Http404(f"No content for slug '{slug}'") from exc

    cache_key = f"site_pages:md:{path}:{mtime}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    text = path.read_text(encoding="utf-8")
    meta, body = _split_front_matter(text)

    # Normalise common fields so templates can rely on them.
    meta.setdefault("title", slug.replace("-", " ").title())
    meta.setdefault("summary", "")
    meta.setdefault("draft", False)
    meta.setdefault("tags", [])
    if isinstance(meta.get("date"), date):
        meta["date"] = meta["date"]
    elif isinstance(meta.get("date"), str):
        meta["date"] = date.fromisoformat(meta["date"])
    else:
        meta["date"] = None

    rendered = _render_body(body)
    record = {
        "slug": slug,
        "meta": meta,
        "title": meta["title"],
        "summary": meta["summary"],
        "date": meta["date"],
        "tags": meta.get("tags", []),
        "tech": meta.get("tech", []),
        "cover": meta.get("cover"),
        "order": meta.get("order", 0),
        "links": meta.get("links", {}) or {},
        "draft": bool(meta.get("draft", False)),
        "content_html": rendered,
    }
    cache.set(cache_key, record, None)  # mtime in key invalidates on edit
    return record


def _kind_dir(kind: str) -> Path:
    if kind not in KINDS:
        raise ValueError(f"Unknown content kind: {kind!r}")
    return CONTENT_DIR / kind


def load_one(kind: str, slug: str) -> dict:
    """Return the rendered record for ``content/<kind>/<slug>.md``.

    Raises ``Http404`` when the file is missing or marked as a draft.
    """
    path = _kind_dir(kind) / f"{slug}.md"
    record = _parse_file(path, slug)
    if record["draft"] and not getattr(settings, "SHOW_DRAFTS", False):
        raise Http404("Draft content is not published")
    return record


def load_collection(kind: str, include_drafts: bool = False) -> list[dict]:
    """Return all published records for a kind, sorted appropriately.

    Drafts are excluded unless ``include_drafts`` is True or the
    ``SHOW_DRAFTS`` setting is enabled.
    """
    directory = _kind_dir(kind)
    if not directory.is_dir():
        return []

    show_drafts = include_drafts or getattr(settings, "SHOW_DRAFTS", False)
    records = []
    for path in sorted(directory.glob("*.md")):
        slug = path.stem
        try:
            record = _parse_file(path, slug)
        except ContentError:
            # Skip broken files rather than 500-ing the whole list.
            continue
        if record["draft"] and not show_drafts:
            continue
        records.append(record)

    if kind in _SORT_DESC:
        records.sort(key=lambda r: (r["date"] or date.min), reverse=True)
    else:
        records.sort(key=lambda r: r.get("order", 0))
    return records


def load_page(slug: str) -> dict:
    """Convenience wrapper for ``content/pages/<slug>.md``."""
    return load_one("pages", slug)
