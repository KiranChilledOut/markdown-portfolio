---
title: "Claude & Codex → Nebius Proxy"
summary: "A streaming proxy that lets Claude Code and OpenAI Codex CLI run against Nebius-hosted models, with web search, model routing, and cost observability built in."
tech: [Python, SSE streaming, Docker, Nebius, Tavily]
cover: null
date: 2026-06-27
order: 2
draft: false
category: "AI"
status: "Shipped"
links:
  github: https://github.com/KiranChilledOut/claude-codex-nebius-proxy
  live: ""
---

A bridge that lets both **Claude Code** and **OpenAI Codex CLI** use **Nebius**
AI infrastructure as the backend — with the extras the lightweight routers leave
out.

## What it does

The proxy accepts requests in two different wire formats — Anthropic's
`/v1/messages` and OpenAI's `/v1/responses` — translates each into
OpenAI-compatible calls against Nebius, and converts the responses back. Both
CLIs talk to one local endpoint and hit the same Nebius backend.

## What I built

- **Format translation, both directions.** Incoming Anthropic/OpenAI requests
  are normalized to a common internal shape, routed to Nebius, and the streamed
  response is rendered back into whichever format the calling CLI expects.
- **SSE streaming end-to-end** so token streaming and tool calls feel native in
  both clients.
- **Automatic model routing** across big / middle / small / vision categories,
  picked per request based on payload rather than hard-coded.
- **Server-side web search via Tavily** — when the model emits a `web_search`
  tool call, the proxy executes it, feeds results back, and continues.
- **Token-saving housekeeping handling** that short-circuits low-value Claude
  Code requests (title generation, network probes) locally instead of sending
  them upstream.
- **Tool-call JSON repair and deduplication**, plus **context auto-truncation**
  that preserves tool-result dependencies so truncation doesn't break a chain.
- **Observability dashboard** (`localhost:8083/dashboard`) showing per-request
  usage, latency, cost, and which model each request landed on.
- **A guided TUI installer** that checks prerequisites, tests API keys, offers
  live model dropdowns, writes config, and runs smoke tests — so setup is one
  command.

## Why

I wanted Nebius-hosted models as a drop-in behind both CLIs without going
through Anthropic or OpenAI directly, and the existing routers (claude-code-
router, LiteLLM) didn't include search, request optimization, or cost tracking
out of the box. So I bundled them.
