---
title: "Multi-Tenant Agent Platform — Reference Architecture"
summary: "An opinionated, production-grade blueprint extending a Microsoft Foundry agent workshop into a multi-tenant agentic platform: thin orchestration delegating to APIM-gated, MCP-isolated tool domains."
tech: [Microsoft Foundry, Azure AI Foundry, Azure OpenAI, Azure API Management, Azure App Service, Azure Key Vault, Entra ID, MCP, Terraform, Azure DevOps, Docker, FastAPI]
cover: null
date: 2026-06-28
order: 8
draft: false
category: "Cloud"
status: "Experiment"
links: {}
---

Started from an open-source, multilingual Microsoft Foundry agent workshop
(published on a public workshop site) and extended it into an opinionated,
production-ready blueprint for running secure, multi-tenant agent platforms —
where Foundry stays a thin orchestration layer and tool/inference domains are
isolated behind API-Management-gated MCP servers.

> The base workshop was authored by community contributors; the work shown here
> is the production reference architecture and sample agent I designed and
> built on top of it.

## What I built

- **Built the working sample agent** — a pizza-ordering bot on Azure AI Foundry
  wiring together system prompts, RAG over a vector store of documents, a
  custom function tool, and a remote MCP server — implementing every chapter
  pattern the workshop teaches.
- **Authored a production reference architecture** that generalizes the
  workshop's single-agent pattern into a multi-tenant platform: thin Foundry
  orchestration (routing + synthesis only) delegating heavy LLM inference to an
  external token-factory/inference service via MCP tools.
- **Designed the MCP gateway layer on Azure API Management**: per-domain MCP
  App Services fronted by APIM with Entra OAuth/JWT validation, mTLS, per-team
  rate limiting, path-based authorization scoped to Entra groups, and
  distributed-tracing/correlation headers — authored as inline APIM policy XML.
- **Wrote reusable Terraform IaC modules** for the MCP gateway (APIM), shared
  MCP servers (Linux Web App for Containers with managed identity, VNet
  integration, Key Vault access, IP restrictions), platform core, shared
  services, and self-service team provisioning — with dev/staging/prod
  environments and remote state.
- **Built the Python MCP server framework**: a FastAPI + SSE base class
  implementing the JSON-RPC MCP protocol (initialize / tools-list / tools-call),
  plus a working domain server with HR-system adapters, LLM-driven field
  comparison, and document generation uploaded to Blob storage.
- **Authored a thin client** wrapping the external inference provider
  (AsyncOpenAI-compatible, Key Vault-resolved credentials) and container
  build/deploy pipelines (Docker build-push to ACR, then Terraform plan/apply
  per environment).
- **Created a presentation and architecture diagrams** showcasing how Microsoft
  Foundry can be used to build agents, drawing on the workshop structure.

## Skills

Agentic platform architecture · MCP tool/domain isolation · Terraform IaC &
module design · Azure API Management policy authoring (security, rate limiting,
auth) · developer presentations & reference blueprints.
