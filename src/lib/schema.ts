// JSON Resume + Schema.org Person builders. Port of site_pages/schema.py.
// Pure functions of (site identity, content collections).

import type { SiteConfig } from "../config";
import { getCollection } from "astro:content";

const NETWORK_LABELS: Record<string, string> = {
  github: "GitHub",
  linkedin: "LinkedIn",
  twitter: "Twitter",
  mastodon: "Mastodon",
  website: "Website",
  youtube: "YouTube",
};

function networkLabel(key: string): string {
  return NETWORK_LABELS[key] || key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

interface CollectionEntryLike {
  id: string;
  data: Record<string, unknown>;
}

function isDraft(entry: { data: { draft?: boolean } }): boolean {
  return entry.data.draft === true;
}

function summaryFields(entries: CollectionEntryLike[]): Record<string, unknown>[] {
  return entries.map((e) => {
    const d = e.data;
    const out: Record<string, unknown> = {
      slug: e.id,
      title: d.title || e.id,
      summary: d.summary || "",
    };
    if (d.date) out.date = new Date(d.date as string).toISOString().slice(0, 10);
    if (Array.isArray(d.tags) && d.tags.length) out.tags = d.tags;
    return out;
  });
}

async function loadAll(name: "projects" | "tutorials" | "blog"): Promise<CollectionEntryLike[]> {
  // getCollection is async in Astro v7 content layer.
  const showDrafts = import.meta.env.SHOW_DRAFTS === "true" || import.meta.env.DEV;
  const all = (await getCollection(name)) as unknown as CollectionEntryLike[];
  return showDrafts ? all : all.filter((e) => !isDraft(e as unknown as { data: { draft?: boolean } }));
}

export async function buildJsonResume(site: SiteConfig): Promise<Record<string, unknown>> {
  const basics: Record<string, unknown> = {
    name: site.name || "",
    label: site.label || "",
  };
  if (site.email) basics.email = site.email;
  if (site.base_url) basics.url = site.base_url;
  if (site.location) basics.location = { address: site.location };
  const profiles = Object.entries(site.links)
    .filter(([, v]) => v)
    .map(([k, v]) => ({ network: networkLabel(k), url: v }));
  if (profiles.length) basics.profiles = profiles;

  const projects = (await loadAll("projects"))
    .sort((a, b) => {
      const da = a.data.date ? new Date(a.data.date as string).getTime() : 0;
      const db = b.data.date ? new Date(b.data.date as string).getTime() : 0;
      return db - da;
    })
    .map((p) => {
      const d = p.data;
      const links = (d.links || {}) as { github?: string; live?: string };
      const entry: Record<string, unknown> = {
        name: d.title || p.id,
        summary: d.summary || "",
        slug: p.id,
      };
      if (Array.isArray(d.tech) && d.tech.length) entry.keywords = d.tech;
      if (links.github) entry.repo = links.github;
      if (links.live) entry.url = links.live;
      if (d.date) entry.startDate = new Date(d.date as string).toISOString().slice(0, 10);
      return entry;
    });

  const doc: Record<string, unknown> = { basics };
  if (projects.length) doc.projects = projects;

  const posts = summaryFields(await loadAll("blog"));
  const tutorials = summaryFields(await loadAll("tutorials"));
  if (posts.length || tutorials.length) {
    doc._extensions = {
      schema: "https://portfolio-template.dev/extensions/v1",
      posts,
      tutorials,
    };
  }
  return doc;
}

export async function personJsonLd(site: SiteConfig): Promise<Record<string, unknown>> {
  const person: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: site.name || "",
  };
  if (site.base_url) person.url = site.base_url;
  if (site.email) person.email = site.email;
  const sameAs = Object.values(site.links).filter(Boolean);
  if (sameAs.length) person.sameAs = sameAs;

  const knows = new Set<string>();
  for (const p of await loadAll("projects")) {
    if (Array.isArray(p.data.tech)) p.data.tech.forEach((t: string) => knows.add(t));
  }
  for (const kind of ["blog", "tutorials"] as const) {
    for (const r of await loadAll(kind)) {
      if (Array.isArray(r.data.tags)) r.data.tags.forEach((t: string) => knows.add(t));
    }
  }
  if (knows.size) person.knowsAbout = Array.from(knows).sort();
  return person;
}
