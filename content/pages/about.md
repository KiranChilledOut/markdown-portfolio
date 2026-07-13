---
title: "About"
summary: "Who I am and what this site is."
draft: false
---

# About

I'm **Kiran Raj Rajendran** — an engineer who enjoys turning fuzzy problems into
working software. This site is where I keep my projects, tutorials, and writing
in one place.

## What you'll find here

- **Projects** — things I've built, with links to source and live demos.
- **Tutorials** — focused write-ups on problems I've worked through.
- **Blog** — looser notes and essays.
- **Résumé** — [download it here](/resume/).

## How this site is made

It's a static site built with [Astro](https://astro.build). Every page is a
Markdown file in git with a small YAML header. A GitHub Action builds the HTML
on every push and [GitHub Pages](https://pages.github.com) serves it. No
database for content, no browser editor, no server to keep running — just
files.

```text
content/
  projects/<slug>.md
  tutorials/<slug>.md
  blog/<slug>.md
  pages/about.md
```

Site-wide identity and nav live in one file at the repo root in `site.yml`.
Want to fork your own? Start with the
[Getting Started](/personal_portfolio/tutorials/getting-started/) tutorial.

Want to get in touch? Find me on [GitHub](https://github.com/KiranChilledOut),
[LinkedIn](https://www.linkedin.com/in/kiran-raj-37b85b5b/), or
[SillyJoint](https://www.sillyjoint.com).
