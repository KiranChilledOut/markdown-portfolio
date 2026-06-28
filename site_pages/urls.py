"""URL routes for the markdown-driven portfolio site."""
from django.urls import path

from . import views

app_name = "site_pages"

urlpatterns = [
    path("", views.home, name="home"),
    # Machine-readable identity — JSON Resume schema
    path(".well-known/portfolio.json", views.portfolio_json, name="portfolio_json"),
    # Projects
    path("projects/", views.project_list, name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    # Tutorials
    path("tutorials/", views.tutorial_list, name="tutorial_list"),
    path("tutorials/<slug:slug>/", views.tutorial_detail, name="tutorial_detail"),
    # Blog
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    # Misc pages
    path("about/", views.about, name="about"),
    path("resume/", views.resume, name="resume"),
]
