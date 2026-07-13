// Project-card meta helpers: deterministic category colors/icons and
// status badge styling. Keep everything self-contained — no external fonts
// or icon packs required.

const DEFAULT_CATEGORY = "Project";

export type CategoryKey =
  | "ai"
  | "cloud"
  | "security"
  | "iot"
  | "devops"
  | "web"
  | "data"
  | "default";

const CATEGORY_MAP: Record<string, CategoryKey> = {
  ai: "ai",
  "machine learning": "ai",
  ml: "ai",
  llm: "ai",
  agent: "ai",
  agents: "ai",
  cloud: "cloud",
  azure: "cloud",
  aws: "cloud",
  gcp: "cloud",
  infrastructure: "cloud",
  platform: "cloud",
  security: "security",
  "zero trust": "security",
  identity: "security",
  entra: "security",
  iot: "iot",
  embedded: "iot",
  hardware: "iot",
  devops: "devops",
  automation: "devops",
  cicd: "devops",
  ci: "devops",
  web: "web",
  frontend: "web",
  api: "web",
  data: "data",
  database: "data",
};

const ICONS: Record<CategoryKey, string> = {
  ai: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.387-1 1.732V7h1a7 7 0 1 1 0 14H8A7 7 0 1 1 9 7h1V5.732A2.001 2.001 0 0 1 12 2z"/><path d="M9 13h6M10 10h4M10 16h4"/></svg>`,
  cloud: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19c0-3.037-2.463-5.5-5.5-5.5S6.5 15.963 6.5 19M17.5 19H19a4 4 0 0 0 .243-7.98C18.98 7.04 15.39 4 11.5 4 7.115 4 3.47 7.128 3.043 11.294A5.5 5.5 0 0 0 6.5 19h1"/></svg>`,
  security: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`,
  iot: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="18" rx="3"/><path d="M12 18h.01"/><path d="M9 21h6"/></svg>`,
  devops: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>`,
  web: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
  data: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>`,
  default: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>`,
};

export function categoryKey(input?: string): CategoryKey {
  if (!input) return "default";
  const key = CATEGORY_MAP[input.trim().toLowerCase()] || "default";
  return key;
}

export function categoryClass(input?: string): string {
  return `cat-${categoryKey(input)}`;
}

export function categoryIcon(input?: string): string {
  return ICONS[categoryKey(input)];
}

export function statusClass(input?: string): string {
  const key = (input || "").trim().toLowerCase();
  // Normalize common synonyms.
  if (key === "shipped" || key === "done" || key === "completed") return "status-shipped";
  if (key === "active" || key === "building" || key === "in progress") return "status-active";
  if (key === "experiment" || key === "experimental" || key === "prototype") return "status-experiment";
  if (key === "archived" || key === "maintenance") return "status-archived";
  return "status-default";
}
