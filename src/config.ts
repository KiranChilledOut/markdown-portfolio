// Reads site.yml at build time and resolves the nav sections. Single source of
// truth for the site's identity, links, brand, and which sections appear in nav.

import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

export interface SiteLink {
  [network: string]: string;
}

// Optional home-page profile blocks. Strings render as-is;
// BarSeries is a list of { label, level 0..10 } for the focus bars.
export interface BarItem {
  label: string;
  level: number;
}
export interface TechItem {
  name: string;
  slug?: string;     // simple-icons slug; if present, renders a branded logo badge
  logo?: string;
}

export interface SiteConfig {
  name: string;
  label: string;
  role: string | null;
  location: string | null;
  email: string | null;
  base_url: string;
  links: SiteLink;
  resume: { path: string; download_name: string };
  brand: string;
  theme: { default: "light" | "dark" | "auto" };
  sections: Section[];
  // Optional profile blocks (all default to []  / null → section doesn't render).
  focus: string[];
  tech: TechItem[];
  principles: string[];
  time_on: BarItem[];
  exploring: BarItem[];
  currently_building: string[];
  shaped_thinking: string[];
}

export interface Section {
  kind: "projects" | "tutorials" | "blog" | "about";
  label: string;
  url: string;
  isContent: boolean;
}

const DEFAULT_SECTIONS: { kind: Section["kind"]; label: string }[] = [
  { kind: "projects", label: "Projects" },
  { kind: "tutorials", label: "Tutorials" },
  { kind: "blog", label: "Blog" },
  { kind: "about", label: "About" },
];

const URL_BY_KIND: Record<Section["kind"], string> = {
  projects: "/projects/",
  tutorials: "/tutorials/",
  blog: "/blog/",
  about: "/about/",
};

const CONTENT_KINDS: Section["kind"][] = ["projects", "tutorials", "blog"];

const FALLBACK: SiteConfig = {
  name: "Your Name",
  label: "",
  role: null,
  location: null,
  email: null,
  base_url: "",
  links: {},
  resume: { path: "resume.pdf", download_name: "resume.pdf" },
  brand: "•",
  theme: { default: "auto" },
  sections: [],
  focus: [],
  tech: [],
  principles: [],
  time_on: [],
  exploring: [],
  currently_building: [],
  shaped_thinking: [],
};

// Coerce a raw YAML value into the declared shape; a malformed block just
// yields [] so the section silently hides instead of breaking the build.
function asStringArray(v: unknown): string[] {
  return Array.isArray(v) ? v.filter((x) => typeof x === "string") : [];
}
function asBarItemArray(v: unknown): BarItem[] {
  if (!Array.isArray(v)) return [];
  return v
    .map((x) => {
      if (!x || typeof x !== "object") return null;
      const label = (x as { label?: unknown }).label;
      const levelRaw = (x as { level?: unknown }).level;
      const level = Number(levelRaw);
      if (typeof label !== "string") return null;
      return {
        label,
        level: Number.isFinite(level) ? Math.max(0, Math.min(10, level)) : 5,
      };
    })
    .filter((x): x is BarItem => x !== null);
}
function asTechArray(v: unknown): TechItem[] {
  if (!Array.isArray(v)) return [];
  return v
    .map((x) => {
      if (typeof x === "string") return { name: x };
      if (x && typeof x === "object") {
        const name = (x as { name?: unknown }).name;
        if (typeof name !== "string") return null;
        const slug = (x as { slug?: unknown }).slug;
        const logo = (x as { logo?: unknown }).logo;
        return {
          name,
          ...(typeof slug === "string" ? { slug } : {}),
          ...(typeof logo === "string" ? { logo } : {}),
        } as TechItem;
      }
      return null;
    })
    .filter((x): x is TechItem => x !== null);
}

function withBase(url: string, base: string): string {
  // Astro base may or may not have leading/trailing slash; normalize.
  const b = base.startsWith("/") ? base : `/${base}`;
  const prefix = b.endsWith("/") ? b.slice(0, -1) : b;
  return prefix + url;
}

function resolveSections(
  raw: unknown,
  base: string
): Section[] {
  const list = Array.isArray(raw) && raw.length ? raw : DEFAULT_SECTIONS;
  const out: Section[] = [];
  for (const entry of list) {
    if (!entry || typeof entry !== "object") continue;
    const kind = (entry as { kind?: string }).kind as Section["kind"];
    if (!(kind in URL_BY_KIND)) {
      console.warn(`[site.yml] unknown section kind "${kind}"; skipping`);
      continue;
    }
    const label = (entry as { label?: string }).label || kind[0].toUpperCase() + kind.slice(1);
    out.push({
      kind,
      label,
      url: withBase(URL_BY_KIND[kind], base),
      isContent: CONTENT_KINDS.includes(kind),
    });
  }
  return out.length ? out : resolveSections(DEFAULT_SECTIONS, base);
}

let cached: SiteConfig | null = null;

export function loadSiteConfig(): SiteConfig {
  if (cached) return cached;
  const file = path.resolve(process.cwd(), "site.yml");
  let data: Record<string, unknown> = {};
  try {
    const text = fs.readFileSync(file, "utf-8");
    const parsed = yaml.load(text);
    if (parsed && typeof parsed === "object") data = parsed as Record<string, unknown>;
  } catch (e) {
    console.warn(`[site.yml] could not read/parse (${(e as Error).message}); using fallback`);
  }

  const base = import.meta.env.BASE_URL || "/";
  const merged: SiteConfig = {
    name: (data.name as string) || FALLBACK.name,
    label: (data.label as string) || "",
    role: (data.role as string) ?? null,
    location: (data.location as string) ?? null,
    email: (data.email as string) ?? null,
    base_url: (data.base_url as string) || "",
    links: (data.links as SiteLink) || {},
    resume: {
      path: ((data.resume as { path?: string })?.path) || FALLBACK.resume.path,
      download_name:
        ((data.resume as { download_name?: string })?.download_name) ||
        FALLBACK.resume.download_name,
    },
    brand: (data.brand as string) || FALLBACK.brand,
    theme: {
      default: ((data.theme as { default?: string })?.default as SiteConfig["theme"]["default"]) || "auto",
    },
    sections: resolveSections(data.sections, base),
    focus: asStringArray(data.focus),
    tech: asTechArray(data.tech),
    principles: asStringArray(data.principles),
    time_on: asBarItemArray(data.time_on),
    exploring: asBarItemArray(data.exploring),
    currently_building: asStringArray(data.currently_building),
    shaped_thinking: asStringArray(data.shaped_thinking),
  };
  cached = merged;
  return merged;
}

export const SITE = loadSiteConfig();

/** Resolve an absolute site path under the Astro base. */
export function url(pathname: string): string {
  return withBase(pathname, import.meta.env.BASE_URL || "/");
}
