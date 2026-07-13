---
title: "Hello, World"
summary: "First post on the rebuilt site — static, markdown-first, shipped on GitHub Pages."
tags: [meta]
date: 2026-06-29
draft: false
---

Welcome to the rebuilt portfolio. This is the first post on a site that no
longer needs a server.

## The shift

The previous version was a small web app that rendered pages on request and
stored its writing in a database behind a browser editor. It worked, but the
content wasn't versioned with the code, wasn't easy to move, and didn't read
like *writing*. So I rebuilt it:

- Every post, project, tutorial, and page is a plain Markdown file.
- Each file has a small YAML header for metadata.
- `git push` is the publish button — a GitHub Action builds and a static
  host serves.

## A code block, for proof

```typescript
// Build-time content loader: every Markdown file becomes a typed entry.
import { getCollection } from "astro:content";

const posts = (await getCollection("blog"))
  .filter((p) => !p.data.draft)
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
```

If that block is coloured, the pipeline works end to end. There's more to come.
