---
title: "Getting Started with the Site"
summary: "Fork this site, make it yours, and ship it to GitHub Pages."
tags: [meta, astro, github-pages]
date: 2026-06-29
order: 1
draft: false
---

This is a static site built with [Astro](https://astro.build). Content lives in
plain Markdown files, the build turns them into HTML, and GitHub Pages serves
the result. Everything you need to run it lives in this one repository.

This walkthrough takes you from an empty fork to a live site at
`https://yourname.github.io/personal_portfolio/`.

## 0. What you need

- A [GitHub](https://github.com) account.
- [Node.js](https://nodejs.org) 20 or newer (for running the build locally).
- A terminal with `git`.

That's it. No database, no server to run in production, no account on a hosting
platform.

## 1. Fork the repo

Open the repository on GitHub and click **Fork** in the top right. This copies
the whole project — code, content, and the GitHub Pages deploy workflow — into
your own account.

## 2. Clone your fork

```bash
git clone https://github.com/<your-name>/personal_portfolio.git
cd personal_portfolio
npm install
```

`npm install` pulls Astro and the sitemap integration. It runs once.

## 3. Make it yours: open `site.yml`

The single file that drives the whole site is [`site.yml`](../../) at the repo
root. Identity, links, brand mark, the focus chips on the home page, the tech
badges, the nav sections — all of it is in there.

Edit the top block first:

```yaml
name: "Your Name"
label: "Your one-line tagline"
role: "Your Role"
location: "Your City"        # omit the line to hide it
email: you@example.com
base_url: "https://yourname.github.io/personal_portfolio/"

links:
  github: "https://github.com/your-name"
  linkedin: "https://www.linkedin.com/in/your-handle/"
  website: "https://your-site.example.com"
```

Set `base_url` to where the site will live (see step 7). Everything else —
`focus`, `tech`, `principles`, `time_on`, `exploring`, `sections` — is optional.
Omit any block and the home page simply hides that section.

## 4. Run it locally

```bash
npm run dev
```

Open http://localhost:4321/personal_portfolio/ and you should see the site with
your identity. Edits to `site.yml` or any Markdown file hot-reload instantly.
Stop the server with `Ctrl+C` when you're done.

## 5. Add a project

Drop a Markdown file under `content/projects/`. The filename becomes the URL:

```markdown
---
title: "My First Project"
summary: "One-line summary shown on the project card."
tech: [Python, Terraform, Azure]
order: 1
date: 2026-06-29
draft: false
links:
  github: https://github.com/your-name/your-repo
  live: https://your-demo.example.com
---

Describe the project in plain Markdown. What it is, why you built it,
what you learned. The body supports headings, lists, links, and
syntax-highlighted code blocks:

```python
def ship() -> None:
    print("done")
```
```

Save it as `content/projects/my-first-project.md` and it appears at
`/projects/my-first-project/`. Set `draft: true` to hide it from the listings
while you're still working.

## 6. Add a blog post

Same shape, different folder. `content/blog/first-post.md`:

```yaml
---
title: "First Post"
summary: "A short note."
tags: [meta]
date: 2026-06-29
draft: false
---
```

Then write the body in Markdown below the front matter.

## 7. Set your Pages URL, then push

GitHub Pages will serve the site at `https://<your-name>.github.io/<repo-name>/`
unless your repo is named `<your-name>.github.io` (then it's the user root).
The `base` path is derived from the repo name automatically in
`astro.config.mjs`, so a fork named `personal_portfolio` "just works".

Make sure `base_url` in `site.yml` matches that final URL, then commit and
push:

```bash
git add -A
git commit -m "Make the site mine"
git push
```

## 8. Turn on GitHub Pages

1. In your fork, go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.

That's the only configuration step. The included workflow
(`.github/workflows/deploy.yml`) builds the site on every push and publishes it
straight to Pages — no extra secrets, no runners to configure.

## 9. Wait for the build, then visit

Push a commit and the **Actions** tab shows a deploy run. A minute or two
later the Pages section shows a green check and a URL. Open it.

## What just happened

- You forked a static site generator.
- You pointed `site.yml` at your identity and links.
- You added Markdown files for your content.
- You pushed, and a GitHub Action built and published the static HTML.

From here on, the workflow is short: edit a file (or `site.yml`), `git push`,
wait a minute. The filesystem is the source of truth, and `git push` is the
publish button.
