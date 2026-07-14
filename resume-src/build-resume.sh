#!/usr/bin/env bash
# build-resume.sh — render resume-src/resume.html → public/resume.pdf (headless Chrome).
#
# Workflow to UPDATE your résumé:
#   1. edit  resume-src/resume.html   (content is plain HTML — the Experience/Skills/etc. blocks)
#   2. run   npm run resume           (or: bash resume-src/build-resume.sh)
#   3. commit public/resume.pdf (+ resume-src/resume.html) and push → the live site redeploys
#
# No extra dependencies: it uses a Chrome/Chromium you already have (Google Chrome, Edge, a
# chromium on PATH, or the Playwright cache).
set -euo pipefail

# repo root = parent of this script's dir
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/resume-src/resume.html"
OUT="$ROOT/public/resume.pdf"

[ -f "$SRC" ] || { echo "✗ source not found: $SRC" >&2; exit 1; }

# Find a Chromium-family binary.
find_chrome() {
  local c
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "$(command -v google-chrome 2>/dev/null || true)" \
    "$(command -v chromium 2>/dev/null || true)" \
    "$(command -v chromium-browser 2>/dev/null || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return 0; }
  done
  # Playwright's cached chromium (headless shell), newest first
  c=$(ls -dt "$HOME/Library/Caches/ms-playwright"/chromium*/chrome-*/*/Google\ Chrome\ for\ Testing.app/Contents/MacOS/* \
             "$HOME/Library/Caches/ms-playwright"/chromium*/chrome-*/chrome \
             "$HOME/.cache/ms-playwright"/chromium*/chrome-*/chrome 2>/dev/null | head -1 || true)
  [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return 0; }
  return 1
}

CHROME="$(find_chrome)" || { echo "✗ No Chrome/Chromium found. Install Google Chrome, or run 'npx playwright install chromium'." >&2; exit 1; }
echo "• renderer: $CHROME"

# Render. --no-pdf-header-footer drops the default date/URL header; the HTML's @page handles margins.
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$SRC" 2>/dev/null || \
"$CHROME" --headless --disable-gpu --print-to-pdf-no-header \
  --print-to-pdf="$OUT" "file://$SRC" 2>/dev/null

[ -s "$OUT" ] || { echo "✗ render produced no output" >&2; exit 1; }
echo "✓ wrote $OUT"

# Keep the local build output (dist/) in sync if it exists, so `npm run preview` shows the new one.
if [ -f "$ROOT/dist/resume.pdf" ]; then cp "$OUT" "$ROOT/dist/resume.pdf"; echo "✓ synced dist/resume.pdf"; fi
