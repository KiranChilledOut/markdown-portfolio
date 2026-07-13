// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// GitHub Pages serves from a project path (https://<user>.github.io/<repo>/)
// UNLESS the repo is named <user>.github.io or a custom domain is set.
// We derive `base` from the repo name so the same config works for forks.
//
// Override locally with SITE URL + BASE env vars if needed.
const SITE = process.env.SITE_URL ?? "https://kiranraj.github.io";
const repo = process.env.GITHUB_REPOSITORY?.split("/")[1] ?? "personal_portfolio";
const isUserPages = repo.endsWith(".github.io");
const BASE = isUserPages ? "/" : `/${repo}/`;

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
