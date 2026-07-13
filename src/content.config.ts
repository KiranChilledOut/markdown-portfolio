import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Front-matter schemas, validated at build time. A bad file fails the build
// with a clear Zod error rather than shipping a broken page.

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./content/projects" }),
  schema: z.object({
    title: z.string(),
    summary: z.string().default(""),
    tech: z.array(z.string()).default([]),
    cover: z.string().nullable().default(null),
    category: z
      .union([
        z.literal("AI"),
        z.literal("Cloud"),
        z.literal("Security"),
        z.literal("IoT"),
        z.literal("DevOps"),
        z.literal("Web"),
        z.literal("Data"),
        z.string(),
      ])
      .default("Project"),
    status: z.union([z.literal("Active"), z.literal("Shipped"), z.literal("Experiment"), z.literal("Archived"), z.string()]).default("Active"),
    date: z.coerce.date().optional(),
    order: z.number().default(0),
    draft: z.boolean().default(false),
    links: z
      .object({
        // Accept empty string / null as "no link" (authors write live: "" when
        // there's no demo). Coerce to undefined so the card hides it cleanly.
        github: z.union([z.string().url(), z.literal(""), z.null()]).optional(),
        live: z.union([z.string().url(), z.literal(""), z.null()]).optional(),
      })
      .default({}),
  }),
});

const tutorials = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./content/tutorials" }),
  schema: z.object({
    title: z.string(),
    summary: z.string().default(""),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date().optional(),
    order: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./content/blog" }),
  schema: z.object({
    title: z.string(),
    summary: z.string().default(""),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date().optional(),
    cover: z.string().nullable().default(null),
    draft: z.boolean().default(false),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./content/pages" }),
  schema: z.object({
    title: z.string(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { projects, tutorials, blog, pages };
