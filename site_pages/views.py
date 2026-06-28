"""Views for the markdown-driven portfolio site.

All content comes from on-disk markdown files via :mod:`site_pages.loader`.
There is one view per "kind" plus a home view and a resume download.
"""
from __future__ import annotations

from django.conf import settings
from django.http import FileResponse, Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from . import loader, schema
from .context_processors import load_site_config

# How many recent projects to feature on the home page.
HOME_FEATURED_PROJECTS = 4


def _list_context(kind: str, title: str) -> dict:
    """Build the common context for a listing page."""
    items = loader.load_collection(kind)
    return {
        "title": title,
        "kind": kind,
        "items": items,
        "empty": not items,
    }


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    """Landing page: hero + a few featured items from each enabled section."""
    site_cfg = load_site_config()
    sections = site_cfg.get("sections", [])
    # Build {(kind): recent_items} for the content sections that are enabled.
    featured: dict[str, list[dict]] = {}
    for s in sections:
        kind = s.get("kind")
        if s.get("is_content") and kind:
            limit = HOME_FEATURED_PROJECTS if kind == "projects" else 4
            featured[kind] = loader.load_collection(kind)[:limit]
    # First enabled content section -> the hero "view X" button target.
    first_content = next((s for s in sections if s.get("is_content")), None)
    return render(
        request,
        "site_pages/home.html",
        {
            "title": "Home",
            "featured": featured,
            "first_content": first_content,
        },
    )


@require_GET
def project_list(request: HttpRequest) -> HttpResponse:
    return render(request, "site_pages/project_list.html", _list_context("projects", "Projects"))


@require_GET
def project_detail(request: HttpRequest, slug: str) -> HttpResponse:
    project = loader.load_one("projects", slug)
    return render(
        request,
        "site_pages/project_detail.html",
        {"project": project, "title": project["title"], "back_url": reverse("site_pages:project_list"), "back_label": "projects"},
    )


@require_GET
def tutorial_list(request: HttpRequest) -> HttpResponse:
    return render(request, "site_pages/tutorial_list.html", _list_context("tutorials", "Tutorials"))


@require_GET
def tutorial_detail(request: HttpRequest, slug: str) -> HttpResponse:
    tutorial = loader.load_one("tutorials", slug)
    return render(
        request,
        "site_pages/tutorial_detail.html",
        {"tutorial": tutorial, "title": tutorial["title"], "back_url": reverse("site_pages:tutorial_list"), "back_label": "tutorials"},
    )


@require_GET
def blog_list(request: HttpRequest) -> HttpResponse:
    return render(request, "site_pages/blog_list.html", _list_context("blog", "Blog"))


@require_GET
def blog_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = loader.load_one("blog", slug)
    return render(
        request,
        "site_pages/blog_detail.html",
        {"post": post, "title": post["title"], "back_url": reverse("site_pages:blog_list"), "back_label": "blog"},
    )


@require_GET
def page(request: HttpRequest, slug: str) -> HttpResponse:
    """Generic markdown page, e.g. the About page at content/pages/about.md."""
    record = loader.load_one("pages", slug)
    return render(request, "site_pages/page.html", {"page": record, "title": record["title"]})


@require_GET
def about(request: HttpRequest) -> HttpResponse:
    return page(request, slug="about")


@require_GET
def resume(request: HttpRequest) -> HttpResponse:
    """Stream the resume PDF as a download (inline-preview fallback in browser).

    The file is served from static storage; ``static()`` resolves to the
    collectstatic path in production. We open it directly off the static dir
    so PythonAnywhere serves a guaranteed-current copy.
    """
    site_cfg = load_site_config()
    resume_cfg = site_cfg.get("resume") or {}
    relative = resume_cfg.get("path") or "site_pages/resume.pdf"
    filename = resume_cfg.get("download_name") or "resume.pdf"
    candidates = [
        # Local dev / collected static
        settings.STATIC_ROOT / relative,
        # The app's own static source (works without collectstatic in DEBUG)
        settings.BASE_DIR / "site_pages" / "static" / relative,
    ]
    for path in candidates:
        if path.exists():
            return FileResponse(
                path.open("rb"),
                content_type="application/pdf",
                as_attachment=True,
                filename=filename,
            )
    raise Http404(
        f"Resume PDF not found; add it at the path in site.yml resume.path ({relative})"
    )


@require_GET
@cache_page(60 * 5)  # 5 minutes; content changes invalid via loader mtime cache anyway
def portfolio_json(request: HttpRequest) -> JsonResponse:
    """Serve the JSON Resume document at /.well-known/portfolio.json.

    Spec-strict for ``basics`` and ``projects``; blog/tutorials exposed under a
    namespaced ``_extensions`` block. Consumed by agents/readers/tooling.
    """
    doc = schema.build_json_resume()
    resp = JsonResponse(doc, json_dumps_params={"indent": 2})
    resp["Cache-Control"] = "public, max-age=300"
    return resp


@require_GET
def error_404(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "site_pages/404.html", {"title": "Not found"}, status=404)
