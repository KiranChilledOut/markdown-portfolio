---
title: "Portfolio Revamp"
summary: "Re-platformed this site from a Django app on PythonAnywhere to a static Astro build on GitHub Pages."
tech: [Astro, TypeScript, Markdown, GitHub Actions]
cover: null
date: 2026-06-29
order: 1
draft: false
category: "Web"
status: "Active"
links:
  github: https://github.com/KiranChilledOut
  live: https://www.sillyjoint.com
---

A ground-up rebuild of this very site. The previous version was a small web app
that rendered pages at request time and stored its writing in a database behind
a browser editor. This version treats **content as code**: every page is a
Markdown file with YAML front matter, versioned in git, compiled to static HTML
at build time, and served from GitHub Pages.

## What changed

- **Static, not runtime.** Pages are compiled once at build time. Nothing runs
  when a visitor loads the site, so there's no server to keep up, no cold
  starts, and nothing to scale.
- **Git-push deploys.** `git push` triggers a GitHub Action that builds the
  site and publishes it straight to GitHub Pages. No separate hosting account.
- **One source of truth for identity.** `site.yml` at the repo root holds name,
  links, brand, tech badges, focus areas, and nav sections — the templates read
  from it, and so does the JSON Resume / Schema.org output at
  `/.well-known/portfolio.json`.
- **Typed content.** Front matter is validated at build time with Zod, so a
  malformed file fails the build with a clear error instead of shipping a
  broken page.
- **Syntax highlighting** straight out of the Markdown via Shiki, with a light
  and a dark theme that swap with the site theme:

```typescript
// Every collection entry is type-checked against a Zod schema at build time.
import { getCollection } from "astro:content";

const projects = (await getCollection("projects"))
  .sort((a, b) => (a.data.order ?? 0) - (b.data.order ?? 0));
```

## Why file-based?

Content in the database was never versioned, never reviewable, and never
portable. Keeping it as files means the whole site — design *and* writing —
lives in one git repository, forkable by anyone. Editing a post is just
editing a file.
