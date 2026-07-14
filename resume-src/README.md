# Résumé source

The résumé PDF (`public/resume.pdf`, embedded on the `/resume` page) is generated
from `resume.html` here — so it's editable and version-controlled, not a mystery
binary.

## Update it

1. **Edit content** in [`resume.html`](./resume.html). It's plain HTML — the
   `Experience`, `Core Skills`, `Certifications`, `Education` blocks are obvious;
   change text, add/remove a `<div class="job">…</div>` or a `<li>`.
2. **Regenerate the PDF:**
   ```bash
   npm run resume        # → renders resume.html to public/resume.pdf
   ```
3. **Publish:** commit `public/resume.pdf` (and `resume.html`) and push — the
   GitHub Actions build redeploys the site with the new résumé.

## How it works

`npm run resume` runs [`build-resume.sh`](./build-resume.sh), which renders
`resume.html` with a headless Chrome/Chromium already on your machine (Google
Chrome, Edge, a `chromium` on `PATH`, or the Playwright cache) — no extra
dependencies. Layout is print-tuned via the `@page` / print CSS in `resume.html`
(A4, one page).

## Files

| File | Purpose |
|---|---|
| `resume.html` | The résumé — **edit this** |
| `build-resume.sh` | Renderer (invoked by `npm run resume`) |
| `resume-previous.pdf` | Backup of the prior PDF (safe to delete) |
| `preview.png` | Last screenshot preview (safe to delete) |

Output → `../public/resume.pdf`.
