"""Django settings for the portfolio_site project.

A file-based, markdown-first personal site deployed on PythonAnywhere.
Content (projects, tutorials, blog posts, pages) lives as ``.md`` files under
``content/`` -- there are no content models. See ``site_pages/loader.py``.

Environment variables (set these on PythonAnywhere / in the WSGI file):
  DJANGO_SECRET_KEY     required in production (any long random string)
  DJANGO_DEBUG          "1" to enable debug; off otherwise
  DJANGO_ALLOWED_HOSTS  comma-separated, e.g. "yourname.pythonanywhere.com,localhost"
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
# Security
# --------------------------------------------------------------------------- #
def _env_bool(name: str, default: bool) -> bool:
    return os.environ.get(name, "").lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    # A throwaway dev key -- production MUST set DJANGO_SECRET_KEY in env.
    "django-insecure-dev-only-change-me-via-DJANGO_SECRET_KEY",
)

DEBUG = _env_bool("DJANGO_DEBUG", False)

_allowed = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1",
)
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]

# PythonAnywhere serves over https; trust the forwarded proto header.
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# PA is always https in front of the WSGI app; redirect any stray http hits.
SECURE_SSL_REDIRECT = not DEBUG

# Allow the production domain for form posts (admin login). Extend via env if
# you add a custom domain.
_pa_hosts = [f"https://{h}" for h in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = _pa_hosts + ["http://localhost", "http://127.0.0.1"]


# --------------------------------------------------------------------------- #
# Applications
# --------------------------------------------------------------------------- #
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "site_pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "site_pages.context_processors.site",
                "site_pages.context_processors.person_jsonld",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_site.wsgi.application"


# --------------------------------------------------------------------------- #
# Database (only Django bookkeeping -- sessions/auth/admin; no content here)
# --------------------------------------------------------------------------- #
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --------------------------------------------------------------------------- #
# Password validation
# --------------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------- #
# Internationalization
# --------------------------------------------------------------------------- #
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------- #
# Static & media files
# --------------------------------------------------------------------------- #
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").is_dir() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------------------------------- #
# Markdown content engine
# --------------------------------------------------------------------------- #
# Extensions applied when rendering content bodies. ``codehilite`` (Pygments)
# class matches the stylesheet rule ``.highlight`` in site_pages/static/.../main.css.
MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.fenced_code",
    "markdown.extensions.codehilite",
    "markdown.extensions.toc",
    "markdown.extensions.tables",
    "markdown.extensions.attr_list",
    "markdown.extensions.md_in_html",
]
MARKDOWN_EXTENSION_CONFIGS = {
    "markdown.extensions.codehilite": {
        "css_class": "highlight",
        "guess_lang": False,
    },
}

# Path to content directory (one .md file per page). Overridable for tests.
CONTENT_DIR = BASE_DIR / "content"

# Path to the site identity config (name, links, resume, branding). Read by the
# site_pages context processor and the schema generator.
SITE_CONFIG = BASE_DIR / "site.yml"

# When True, draft content is visible in listings and on direct requests.
# Flip via env locally: DJANGO_SHOW_DRAFTS=1
SHOW_DRAFTS = _env_bool("DJANGO_SHOW_DRAFTS", DEBUG)

# Default upload location for the resume and any author-supplied PDFs.
RESUME_RELATIVE_PATH = "site_pages/resume.pdf"


# --------------------------------------------------------------------------- #
# Security headers (production hardening; check with `manage.py check --deploy`)
# --------------------------------------------------------------------------- #
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
