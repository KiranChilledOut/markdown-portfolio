import type { APIRoute } from "astro";
import { SITE } from "../../config";
import { buildJsonResume } from "../../lib/schema";

export const GET: APIRoute = async () => {
  const doc = await buildJsonResume(SITE);
  return new Response(JSON.stringify(doc, null, 2), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=300",
    },
  });
};
