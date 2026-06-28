# Tutorial: Fork → Live Portfolio on PythonAnywhere

This walks a person who can write markdown (but maybe not Django) from a fresh
fork to a live site in about 30 minutes. Skim the headings; do the bolded steps.

## 0. What you need

- A GitHub account.
- A [PythonAnywhere](https://www.pythonanywhere.com) account (the free tier
  works; a paid tier removes the daily CPU cap and supports custom domains).
- Your résumé as a PDF.

You do **not** need to know Django. You edit markdown files and one YAML config.

## 1. Make the repo yours

- Click **Use this template** on the template repo (or fork it). Name it
  whatever you like, e.g. `my-portfolio`.
- Clone it locally:
  ```bash
  git clone https://github.com/<you>/my-portfolio.git
  cd my-portfolio
  ```

## 2. Edit `site.yml`

Copy the example to your real config:
```bash
cp site.yml.example site.yml
```
Open `site.yml` and change `name`, `label`, `links`, `base_url`, and
`resume.download_name` to yours. That one file is your identity across the whole
site — the nav, footer, résumé button, and the machine-readable schema all read
from it.

## 3. Write your content

Everything you publish is a markdown file under `content/`. See
`content.example/` for the format. Each file has a small YAML header (the
"front matter") then the body:

```markdown
---
title: "My Awesome Project"
summary: "One-line description for the card."
tech: [Python, React]
date: 2026-06-01
draft: false
links:
  github: https://github.com/you/awesome
  live: https://awesome.example
---
# My Awesome Project

The body of your project page. Code blocks are highlighted:

```python
print("hi")
```
```

- `content/projects/<slug>.md`  → `/projects/<slug>/`
- `content/tutorials/<slug>.md` → `/tutorials/<slug>/`
- `content/blog/<slug>.md`      → `/blog/<slug>/`
- `content/pages/about.md`      → `/about/`

Set `draft: true` to hide a file while you work on it. The filename (without
`.md`) is the URL slug.

## 4. Add your résumé

Drop your PDF at:
```
site_pages/static/site_pages/resume.pdf
```
The `/resume/` link downloads it with the filename from `site.yml`
(`resume.download_name`).

## 5. Run it locally (optional but recommended)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export DJANGO_DEBUG=1 DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput
.venv/bin/python manage.py runserver
```
Open http://127.0.0.1:8000. Edit markdown, save, reload — changes appear with no
restart.

## 6. Set up PythonAnywhere (one time)

1. **Push to GitHub**: `git push` your `site.yml` + `content/` + résumé.
2. On PythonAnywhere: **Dashboard → Git → Add a Git project**. Enter your repo
   URL; it clones into `/home/<your-pa-username>/my-portfolio`.
3. **Web tab → Add a new web app → Manual configuration → Python 3.12**.
4. **Source code** path: `/home/<your-pa-username>/my-portfolio`.
5. **Working directory**: same path.
6. Create a virtualenv in a **Bash console**:
   ```bash
   cd ~/my-portfolio
   python3.12 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
   Set the **Virtualenv** path on the Web tab to
   `/home/<your-pa-username>/my-portfolio/.venv`.
7. **WSGI file** (Web tab → edit the WSGI file). Replace its contents with:
   ```python
   import os, sys
   path = "/home/<your-pa-username>/my-portfolio"
   if path not in sys.path: sys.path.append(path)
   os.environ["DJANGO_SETTINGS_MODULE"] = "portfolio_site.settings"
   os.environ["DJANGO_SECRET_KEY"] = "<make a long random string>"
   os.environ["DJANGO_DEBUG"] = "0"
   os.environ["DJANGO_ALLOWED_HOSTS"] = "<your-pa-username>.pythonanywhere.com"
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
8. **Static files mapping** (Web tab): add
   - URL `/static/` → directory `/home/<your-pa-username>/my-portfolio/staticfiles`
   - URL `/media/` → directory `/home/<your-pa-username>/my-portfolio/media`
9. In a **Bash console**, run:
   ```bash
   cd ~/my-portfolio
   .venv/bin/python manage.py migrate
   .venv/bin/python manage.py collectstatic --noinput
   ```
10. **Reload** the web app on the Web tab. Visit
    `https://<your-pa-username>.pythonanywhere.com`. 🎉

## 7. Turn on auto-deploy (every `git push` goes live)

1. On PythonAnywhere: **Account → API token → Create**. Copy it.
2. In your GitHub repo: **Settings → Secrets and variables → Actions → New
   repository secret**. Add four:
   - `PA_USERNAME` — your PythonAnywhere username
   - `PA_API_TOKEN` — the token from step 1
   - `PA_DOMAIN` — `<your-pa-username>.pythonanywhere.com`
   - `PA_REPO_PATH` — `/home/<your-pa-username>/my-portfolio`
3. Push to `main` (or `master`). The **Deploy to PythonAnywhere** action runs
   the test suite, then pulls code, runs migrations + collectstatic, and reloads
   the web app — all via the PythonAnywhere API, no SSH keys.

From now on: edit a markdown file → `git push` → it's live.

## Troubleshooting

- **500 error after deploy:** check the Web tab **Log files → Error log**. Most
  often a missing `DJANGO_SECRET_KEY` or wrong `DJANGO_ALLOWED_HOSTS`.
- **Styles/JS missing:** you forgot `collectstatic` or the static-files mapping.
- **Action skipped deploy:** the `PA_API_TOKEN` secret isn't set, so it
  intentionally skips (forks stay safe). Add the secrets per step 7.
- **Manual fallback if the action flakes:** open a PythonAnywhere Bash console,
  `cd ~/my-portfolio && git pull && .venv/bin/python manage.py migrate &&
  .venv/bin/python manage.py collectstatic --noinput`, then **Reload** the web
  app. Never leaves you stranded.

## What you get for free

- A markdown-driven Django site (no framework knowledge needed to publish).
- `/.well-known/portfolio.json` — a [JSON Resume](https://jsonresume.org/) doc
  describing you and your projects, plus Schema.org `Person` data in each page.
  Agents and tools can read who you are and what you've built.
- Dark/light theme, syntax highlighting, responsive nav.
- A test suite + deploy pipeline so you can't easily ship something broken.
