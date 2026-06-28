#!/usr/bin/env bash
# Extract a clean, distributable template from this portfolio repo.
#
# Copies the app code (site_pages/, portfolio_site/, manage.py, requirements,
# scripts, .github, docs, templates) but STRIPS the author's personal content
# (content/, site.yml, resume.pdf, old/, .venv*) and replaces them with
# generic example files. The result is a forkable "portfolio-template" repo.
#
# Usage:
#   scripts/extract_template.sh /path/to/output-dir
#
# Safe to re-run: the output dir is wiped first.

set -euo pipefail

OUT="${1:-}"
if [ -z "$OUT" ]; then
  echo "Usage: scripts/extract_template.sh /path/to/output-dir" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ "$OUT" = "$SRC" ] || [ "$(cd "$OUT" 2>/dev/null && pwd)" = "$SRC" ]; then
  echo "Refusing to extract into the source repo." >&2
  exit 2
fi

echo "Extracting portfolio template -> $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"

# --- Copy the app code (whitelist, so nothing personal sneaks in) -------------
# NOTE: do NOT copy the whole `docs/` dir — it contains the author's internal
# design spec (docs/superpowers/). Docs are copied selectively below.
for item in manage.py requirements.txt requirements.lock.txt \
            portfolio_site site_pages scripts .github; do
  if [ -e "$SRC/$item" ]; then
    mkdir -p "$OUT/$(dirname "$item")"
    cp -R "$SRC/$item" "$OUT/$item"
  fi
done
# Docs: tutorial (real source file) + markdown-basics (canonical beginner guide).
# The author's docs/superpowers/ is deliberately excluded.
mkdir -p "$OUT/docs"
cp "$SRC/docs/tutorial.md" "$OUT/docs/tutorial.md"
# Drop any compiled bytecode that rode along.
find "$OUT" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
# Strip the author's real résumé PDF if it rode along in site_pages/static —
# the template ships only a placeholder note, never someone's actual résumé.
rm -f "$OUT/site_pages/static/site_pages/resume.pdf" \
      "$OUT/site_pages/static/site_pages/resume_bak.pdf"
cp "$SRC/.gitignore" "$OUT/.gitignore"

# --- Template-appropriate tests (assert against example content, not the
# --- author's real data) -----------------------------------------------------
cat > "$OUT/site_pages/tests.py" <<'PY'
"""Tests for the portfolio content engine + schema.

These assert against the example content shipped in content.example/ (copied
into content/), so they pass in a fresh fork. Extend them as you add content.
"""
from django.test import TestCase

from site_pages import loader, schema
from site_pages.context_processors import SAFE_FALLBACK, load_site_config


class LoaderTests(TestCase):
    def test_blog_collection_has_seed_post(self):
        posts = loader.load_collection("blog")
        self.assertTrue(any(p["slug"] == "hello-world" for p in posts))

    def test_records_have_rendered_html(self):
        post = loader.load_one("blog", "hello-world")
        self.assertIn("content_html", post)
        # body renders to at least one HTML block element
        self.assertTrue("<p>" in post["content_html"] or "<h1" in post["content_html"])

    def test_draft_excluded_from_collection(self):
        draft = loader.CONTENT_DIR / "blog" / "_draft_test.md"
        try:
            draft.write_text(
                "---\ntitle: Hidden\nsummary: x\ndate: 2026-01-01\ndraft: true\n---\nbody\n",
                encoding="utf-8",
            )
            loader.cache.clear()
            self.assertFalse(any(p["slug"] == "_draft_test" for p in loader.load_collection("blog")))
            from django.http import Http404
            with self.assertRaises(Http404):
                loader.load_one("blog", "_draft_test")
        finally:
            draft.unlink(missing_ok=True)
            loader.cache.clear()

    def test_missing_slug_404s(self):
        from django.http import Http404
        with self.assertRaises(Http404):
            loader.load_one("blog", "no-such-post")


class SchemaTests(TestCase):
    def test_json_resume_has_basics(self):
        doc = schema.build_json_resume()
        self.assertIn("basics", doc)
        self.assertIn("name", doc["basics"])

    def test_portfolio_json_endpoint(self):
        r = self.client.get("/.well-known/portfolio.json")
        self.assertEqual(r.status_code, 200)
        self.assertIn("application/json", r["Content-Type"])

    def test_jsonld_embedded_in_page(self):
        self.assertContains(self.client.get("/"), "application/ld+json")


class ContextProcessorTests(TestCase):
    def test_site_config_loads(self):
        cfg = load_site_config()
        self.assertIn("name", cfg)

    def test_fallback_on_missing_config(self):
        from django.test import override_settings
        with override_settings(SITE_CONFIG="/no/such/site.yml"):
            self.assertEqual(load_site_config(), SAFE_FALLBACK)
PY

# --- Strip personal content; add examples ------------------------------------
# Author's real content and identity are NOT copied. Example skeleton instead.
mkdir -p "$OUT/content/projects" "$OUT/content/tutorials" \
         "$OUT/content/blog" "$OUT/content/pages" \
         "$OUT/content.example/projects" "$OUT/content.example/tutorials" \
         "$OUT/content.example/blog" "$OUT/content.example/pages"

# site.yml.example (placeholders)
cat > "$OUT/site.yml.example" <<'YAML'
# site.yml — the ONLY file you edit to make this site yours.
# Copy this to site.yml and fill in your details. Change it, push, done.

name: "Your Name"
label: "Your tagline here"
location: "Your City"                          # omit the line to hide location
email: null                                    # set an address to surface it; null hides it
base_url: "https://yourname.pythonanywhere.com"

links:
  github: "https://github.com/your-handle"
  linkedin: "https://www.linkedin.com/in/your-handle/"

resume:
  path: "site_pages/resume.pdf"                # put your PDF at site_pages/static/site_pages/resume.pdf
  download_name: "Your-Name-Resume.pdf"

brand: "•"                                     # nav mark (any emoji/text)
theme:
  default: "auto"                              # "light" | "dark" | "auto"

# Which sections show in the nav, in this order. Remove a line to hide that
# section from your site. Set a custom label to rename it (e.g. Blog -> Writing).
sections:
  - { kind: projects,  label: "Projects" }
  - { kind: tutorials, label: "Tutorials" }
  - { kind: blog,      label: "Blog" }
  - { kind: about,     label: "About" }
YAML

# Example content files (one per section), so the site isn't empty on first run.
cat > "$OUT/content.example/projects/hello-world.md" <<'MD'
---
title: "Hello World Project"
summary: "Replace this with a one-line description of your project."
tech: [Python, Django]
date: 2026-01-01
order: 1
draft: false
links:
  github: https://github.com/your-handle/your-repo
  live: https://your-live-demo.example
---

# My Project

Write your project description in markdown. Anything you put here renders on the
project page, including code:

```python
def hello():
    return "world"
```

Delete this example file and add your own under `content/projects/`.
MD

cat > "$OUT/content.example/tutorials/getting-started.md" <<'MD'
---
title: "Getting Started"
summary: "A first tutorial to show how content works."
tags: [intro]
date: 2026-01-01
order: 1
draft: false
---

This is a tutorial. Each tutorial is one markdown file in `content/tutorials/`.

## Steps

1. Write the file.
2. `git push`.
3. It's live.
MD

cat > "$OUT/content.example/blog/hello-world.md" <<'MD'
---
title: "Hello, World"
summary: "Your first blog post."
tags: [meta]
date: 2026-01-01
draft: false
---

Welcome to your blog. Replace this with your first real post.
MD

cat > "$OUT/content.example/pages/about.md" <<'MD'
---
title: "About"
draft: false
---

# About me

Write your bio in markdown here.
MD

# Seed the live content/ from content.example/ so the site works immediately.
cp -R "$OUT/content.example/." "$OUT/content/"

# Placeholder resume note (author must drop a real PDF in)
cat > "$OUT/site_pages/static/site_pages/README_RESUME.txt" <<'TXT'
Put your résumé PDF here as resume.pdf (or update resume.path in site.yml to
point elsewhere). The /resume/ route will serve it as a download with the
filename from resume.download_name.
TXT

# Beginner README + Markdown basics: copy the canonical versions from
# template_assets/ (kept in sync with the source repo) instead of heredoc-ing,
# so re-running the extractor never regresses the docs.
cp "$SRC/template_assets/README.md" "$OUT/README.md"
mkdir -p "$OUT/docs"
cp "$SRC/template_assets/docs/markdown-basics.md" "$OUT/docs/markdown-basics.md"

echo "Template extracted to: $OUT"
echo "Next: cd $OUT && git init && git add -A && git commit -m 'initial template'"
