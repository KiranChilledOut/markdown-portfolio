// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// GitHub Pages serves from a project path (https://<user>.github.io/<repo>/)
// UNLESS the repo is named <user>.github.io or a custom domain is set.
// We derive `site` and `base` from the repo slug so the same config works
// for forks without manual edits.
//
// Override locally with the SITE_URL and BASE env vars if needed.
const [owner = "kiranchilledout", repo = "markdown-portfolio"] =
  (process.env.GITHUB_REPOSITORY || "").split("/");
const isUserPages = repo.endsWith(".github.io");
const SITE = process.env.SITE_URL ?? `https://${owner.toLowerCase()}.github.io`;
const BASE = process.env.BASE ?? (isUserPages ? "/" : `/${repo}/`);

// https://astro.build/config
export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: "ignore",
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      // Dual themes so code blocks flip with the site's light/dark theme.
      // The dark theme is the "live" render; the light theme is applied
      // automatically when <html data-theme="light"> matches.
      themes: {
        light: "github-light",
        dark: "github-dark-default",
      },
      wrap: true,
    },
  },
});
