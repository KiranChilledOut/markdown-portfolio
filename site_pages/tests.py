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
