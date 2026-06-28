# Markdown Portfolio — make your own website in an afternoon

You don't need to know how to code. If you can type, you can have a personal
website with your projects, writing, and résumé — hosted free on
PythonAnywhere. This template does the hard part; you just write.

> **What is this?** A ready-made website. You write simple text files (in a
> format called *Markdown*) describing your projects and posts, and the website
> turns them into nice-looking pages automatically. No design, no coding.

---

## What your site will have

- A **home page** with your name and links.
- A **Projects** section — each project you write becomes a page.
- A **Tutorials** section — each tutorial becomes a page.
- A **Blog** — each post becomes a page.
- An **About** page — your bio.
- A **Résumé** download button.
- A dark/light theme and phone-friendly layout, already built in.

---

## What you need before you start

1. A free **GitHub** account (github.com).
2. A free **PythonAnywhere** account (pythonanywhere.com).
3. Your **résumé as a PDF file**.

That's it. You do **not** need to install or understand Python, Django, or any
programming. Everything happens through GitHub and PythonAnywhere's website.

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

### Step 2 — Tell the site who you are

1. In your new repository, find the file `site.yml.example` and click it.
2. Click the **pencil icon** ✏️ to edit.
3. Change it to your details. For example:

   ```yaml
   name: "Jane Doe"
   label: "Aspiring designer and maker"
   location: "London"
   email: jane@example.com
   base_url: "https://yourusername.pythonanywhere.com"

   links:
     github: "https://github.com/your-handle"
     linkedin: "https://www.linkedin.com/in/your-handle/"

   resume:
     path: "site_pages/resume.pdf"
     download_name: "Jane-Doe-Resume.pdf"

   brand: "✦"
   theme:
     default: "auto"
   ```

4. **Rename the file** to `site.yml` (remove the `.example`). GitHub can't
   rename in-place, so: click **"Add file" → "Create new file"**, type
   `site.yml` as the name, paste your edited content, and **Commit**. Then go
   back and delete `site.yml.example`.

   > Tip: `site.yml` is the *only* file that holds your identity — your name,
   > links, and résumé filename all come from here.

### Step 3 — Write your content (the fun part)

Each page on your site is **one text file**. They live in the `content/`
folder, split into four sub-folders:

| Folder | Becomes | Example file |
|---|---|---|
| `content/projects/` | a Project page | `my-first-app.md` |
| `content/tutorials/` | a Tutorial page | `baking-bread.md` |
| `content/blog/` | a Blog post | `hello-world.md` |
| `content/pages/` | a standalone page | `about.md` |

The folder already has **example files** you can copy. To add your own:

1. Click into a folder, e.g. `content/projects/`.
2. **"Add file" → "Create new file"**.
3. Type a name ending in `.md` (e.g. `my-website.md`). The name becomes part of
   the web address.
4. Paste a template like this:

   ```markdown
   ---
   title: "My First Website"
   summary: "A small site I built to learn HTML."
   tech: [HTML, CSS]
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

> The lines between the `---` dashes at the top are the page's "settings"
> (title, date, etc.). Everything below them is your content, written in
> Markdown. See **[docs/markdown-basics.md](docs/markdown-basics.md)** for how
> to make headings, links, lists, and images.

> To **hide** a page while you're still writing it, set `draft: true` in its
> settings. It won't show up until you change it back to `false`.

### Step 4 — Add your résumé

1. In your repository, go to
   `site_pages/static/site_pages/`.
2. **"Add file" → "Upload files"** and upload your résumé PDF.
3. **Important:** it must be named exactly `resume.pdf`.
4. **Commit changes**.

The **Résumé** button on your site will download this file.

### Step 5 — Preview it on your computer (optional but recommended)

Skip to Step 6 if you'd rather just put it live directly. To preview first:

1. Click the green **"Code"** button on your repo and **Download ZIP**.
2. Unzip it.
3. You'll need to run a few commands — if commands are new to you, follow
   **[docs/tutorial.md](docs/tutorial.md)**, which has pictures-level detail for
   the local preview.

### Step 6 — Put it on the internet (PythonAnywhere)

This is the only technical part, and it's a one-time setup.
**[docs/tutorial.md](docs/tutorial.md)** walks through it screenshot-by-
screenshot. The short version:

1. Sign in to **pythonanywhere.com** (free).
2. Tell it about your GitHub repo (it copies your files over).
3. Create a "web app" pointing at those files.
4. Paste a short settings snippet (given in the tutorial) and click **Reload**.

You'll get an address like `https://yourusername.pythonanywhere.com` — that's
your live website.

### Step 7 — Make future updates effortless

Once set up, adding a new project or post is just:

1. Add or edit a `.md` file on GitHub (Steps 3).
2. *(If you turned on auto-deploy in the tutorial — Step 7 of the tutorial:
   nothing else to do. The site updates itself within a minute.)*

If you didn't set up auto-deploy, the tutorial's "Troubleshooting" section shows
the two-click manual refresh.

---

## Where things live (quick reference)

| You want to change... | Edit this |
|---|---|
| Your name, links, résumé filename | `site.yml` |
| Which sections show in the menu (Projects/Blog/etc.) | `site.yml` → `sections:` |
| A project page | a file in `content/projects/` |
| A blog post | a file in `content/blog/` |
| A tutorial | a file in `content/tutorials/` |
| Your About page | `content/pages/about.md` |
| Your résumé PDF | `site_pages/static/site_pages/resume.pdf` |

### Show or hide sections

Not everyone wants a Tutorials or Blog section. In `site.yml`, find the
`sections:` list — each line is one menu item. **Delete a line to remove that
section** from your site, or change its `label` to rename it (e.g. `Blog` →
`Writing`). The example ships all four; keep only the ones you want:

```yaml
sections:
  - { kind: projects,  label: "Projects" }
  - { kind: blog,      label: "Writing" }   # renamed
  - { kind: about,     label: "About" }
  # tutorials removed — that whole section is now gone from the menu and home page
```

Don't touch the `portfolio_site/` or `site_pages/` code folders unless you want
to customize the design — you never need to for normal use.

---

## Need help?

- **"How do I write the text?"** → [docs/markdown-basics.md](docs/markdown-basics.md)
- **"How do I get it online?"** → [docs/tutorial.md](docs/tutorial.md)
- **"Something went wrong"** → the "Troubleshooting" section at the bottom of
  [docs/tutorial.md](docs/tutorial.md)

Good luck — your site is closer than you think. ✦
