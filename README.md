# Markdown Portfolio — your own website, free, on GitHub Pages

A personal site built with [Astro](https://astro.build), authored in Markdown,
and deployed automatically to [GitHub Pages](https://pages.github.com). No
server to run, no Python, no databases — just text files in Git.

You don't need to know how to code. If you can type, you can have a personal
website with your projects, writing, and résumé — hosted free on GitHub. This
template does the hard part; you just write.

> **What is this?** A ready-made website. You write simple text files (in a
> format called *Markdown*) describing your projects and posts, and the
> website turns them into nice-looking pages automatically. When you `git
> push`, your site rebuilds and goes live within a minute.

---

## What your site will have

- A **home page** with your name, taglines, tech badges, and links.
- A **Projects** section — each project you write becomes a page.
- A **Tutorials** section — each tutorial becomes a page.
- A **Blog** — each post becomes a page.
- An **About** page — your bio.
- A **Résumé** download link.
- A dark/light theme and phone-friendly layout, already built in.
- A machine-readable identity page at `/.well-known/portfolio.json`
  (JSON Resume + Schema.org) for tooling.

---

## What you need before you start

1. A free **GitHub** account (github.com).
2. Your **résumé as a PDF file** (optional but recommended).

That's it. You do **not** need to install Node, Astro, or anything else to
write content — every page is just a Markdown file in your repo. GitHub builds
and publishes the site for you on every push.

> New to Markdown (the simple text format you'll write in)? Read
> **[docs/markdown-basics.md](docs/markdown-basics.md)** first — it takes 5
> minutes and shows you everything you'll need.

---

## Step-by-step: from zero to live website

### Step 1 — Get your own copy of this template

1. Make sure you're signed in to **GitHub**.
2. On this repository's page, click the green **"Use this template"** button
   (near the top right), then **"Create a new repository"**.
3. Name it something like `my-portfolio`. Leave it **Public** (so your website
   can be seen). Click **Create repository**.

You now have your own copy. GitHub shows you a list of files.

> Your site will be served from `https://<your-username>.github.io/<repo>/`.
> If your repo is named `<your-username>.github.io`, the URL drops the repo
> segment (`https://<your-username>.github.io/`) and you get a "clean" root.

### Step 2 — Tell the site who you are

1. In your new repository, find the file `site.yml.example` and click it.
2. Click the **pencil icon** ✏️ to edit.
3. Change it to your details — name, links, optional focus/tech/etc. The
   comments inside explain every field.

4. **Rename** `site.yml.example` to `site.yml` (GitHub can't rename in place).
   Easiest way:
   - Click **"Add file" → "Create new file"**
   - Type the name `site.yml`
   - Paste your edited content
   - Commit
   - Go back and delete `site.yml.example`

> `site.yml` is the *only* file that holds your identity — your name, links,
> colour brand mark, résumé filename, and which menu sections to show all
> come from here. You will not need to touch any other config.

### Step 3 — Write your content (the fun part)

Each page on your site is **one text file**. They live in the `content/`
folder, split into four sub-folders:

| Folder | Becomes | Example file |
|---|---|---|
| `content/projects/` | a Project page | `my-first-app.md` |
| `content/tutorials/` | a Tutorial page | `baking-bread.md` |
| `content/blog/` | a Blog post | `hello-world.md` |
| `content/pages/` | a standalone page | `about.md` |

To add your own:

1. Click into a folder, e.g. `content/projects/`.
2. **"Add file" → "Create new file"**.
3. Type a name ending in `.md` (e.g. `my-website.md`) — it becomes part of
   the web address.
4. Paste a template like:

   ```markdown
   ---
   title: "My First Website"
   summary: "A small site I built to learn HTML."
   tech: [HTML, CSS]
   category: Web
   date: 2026-06-01
   draft: false
   ---

   # My First Website

   I built this to learn how the web works. Here's what I did:

   - Designed the layout
   - Wrote the pages
   - Put it online

   It was fun!
   ```

5. **Commit changes** (the green button).

> The lines between the `---` dashes are the page's settings (front matter) —
> title, date, category, etc. Everything below them is your content, in
> Markdown. **[docs/markdown-basics.md](docs/markdown-basics.md)** covers
> headings, links, lists, images, and code blocks.
>
> To **hide** a page while it's still a draft, set `draft: true` in its
> settings. It won't show up on the site until you change it back to `false`.

### Step 4 — Add your résumé

1. In your repository, click into `public/`.
2. **"Add file" → "Upload files"** and upload your résumé PDF.
3. **Important:** it must be named exactly `resume.pdf` (overwrite the
   placeholder file).
4. **Commit changes**.

The **Résumé** button on the homepage now downloads your file.

> Prefer to keep your résumé as editable source and generate the PDF with one
> command? See **"Résumé — edit as HTML, generate the PDF"** below.

### Step 5 — Enable GitHub Pages

In your repo on GitHub:

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**
   (not "Deploy from a branch").
3. That's it — no branch to pick. The included workflow (`.github/workflows/deploy.yml`)
   does the rest.

> If the option is greyed out, your repo might be inside an organisation
> that has Pages disabled at the org level — ask an org admin to enable it.

### Step 6 — Watch your site go live

1. Open the **Actions** tab in your repo. The first deploy run starts
   automatically a few seconds after Step 5.
2. Wait for the green tick on **build** *and* **deploy**.
3. The deploy job prints the public URL, something like:

   ```
   https://<your-username>.github.io/<your-repo>/
   ```

4. Open it. If you see the homepage chrome with sections, your site is live.

> First deploy takes about 1–2 minutes. Subsequent deploys for content edits
> only take ~30 seconds.

### Step 7 — Make future updates effortless

Once set up, adding a new project or post is just:

1. Add or edit a `.md` file on GitHub (Step 3).
2. **Commit**.

The action fires on every push to `main`/`master`. Within a minute your edits
are live — no other commands, no extra infrastructure.

---

## Where things live (quick reference)

| You want to change... | Edit this |
|---|---|
| Your name, links, brand mark, résumé filename | `site.yml` |
| Which sections show in the menu (Projects/Blog/etc.) | `site.yml` → `sections:` |
| A project page | a file in `content/projects/` |
| A blog post | a file in `content/blog/` |
| A tutorial | a file in `content/tutorials/` |
| Your About page | `content/pages/about.md` |
| Your résumé | `resume-src/resume.html` → `npm run resume` (or just upload `public/resume.pdf`) |
| The site's design, colours, or layout | `src/styles/main.css` and the components in `src/components/` |

### Show or hide sections

In `site.yml`, find the `sections:` list — each line is one menu item.
**Delete a line to remove that section** from the menu and home page
(everything in that folder is still on disk, just not linked). **Change its
`label` to rename it** (e.g. `Blog` → `Writing`).

```yaml
sections:
  - { kind: projects,  label: "Projects" }
  - { kind: blog,      label: "Writing" }   # renamed
  - { kind: about,     label: "About" }
  # tutorials removed — that whole section is now gone from the menu and home page
```

### Custom domain

1. Add a `CNAME` file at the repo root containing the bare domain
   (e.g. `your-name.com`).
2. Point your DNS at GitHub Pages: an apex `A` record to GitHub's four Pages
   IPs, or a `www` `CNAME` to `<your-username>.github.io`.
3. In **Settings → Pages**, type the domain under **Custom domain**; tick
   **Enforce HTTPS** once the certificate provisions (a few minutes).

---

## Run it locally (optional)

You only need this step if you want to preview drafts before pushing. Most
people never need it.

```bash
git clone https://github.com/<you>/<your-repo>.git
cd <your-repo>
npm install
npm run dev          # http://localhost:4321/<your-repo>/
```

`npm run build` produces the static site in `dist/`. The GitHub Actions
workflow runs exactly the same build, so if it works locally it will work
on Pages.

---

## Résumé — edit as HTML, generate the PDF (optional)

Instead of hand-exporting a PDF from another tool every time, this repo keeps the
résumé as an **editable source file** and renders the PDF for you — so it's
version-controlled and quick to update.

- **Source:** [`resume-src/resume.html`](resume-src/resume.html) — plain HTML; the
  *Experience*, *Core Skills*, *Certifications* and *Education* blocks are easy to
  edit (change text, add a job `<div>` or an `<li>`).
- **Generate:**
  ```bash
  npm run resume
  ```
  Renders `resume.html` → `public/resume.pdf`. It uses a Chrome/Chromium you
  already have (Google Chrome, Edge, a `chromium` on `PATH`, or the Playwright
  cache) — **no extra dependencies**.
- **Publish:** commit `public/resume.pdf` (and `resume-src/resume.html`) and push —
  the site redeploys with the new résumé, and the homepage **Résumé** button serves it.

Full details are in **[resume-src/README.md](resume-src/README.md)**.

> Prefer to just drop in a finished PDF from elsewhere? That still works —
> overwrite `public/resume.pdf` (Step 4) and ignore this section.

---

## Need help?

- **"How do I write the text?"** → [docs/markdown-basics.md](docs/markdown-basics.md)
- **"How do I enable Pages?"** → Step 5 above
- **"Something went wrong on deploy"** → open the failed run in the
  Actions tab; the log shows the exact line that failed. 90% of deploy
  failures are a malformed `site.yml` (quote or indent error) — paste the
  contents into a YAML validator to find it.

Good luck — your site is closer than you think. ✦
