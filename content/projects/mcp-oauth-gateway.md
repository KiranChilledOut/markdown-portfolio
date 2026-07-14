---
title: "MCP Server Platform — Identity-Gated MCP behind a Shared API Gateway"
summary: "A reusable pattern for publishing Model Context Protocol servers behind a shared API-management gateway with per-team, group-gated OAuth 2.0 — connectable from real MCP clients (Claude Desktop, Claude Code, Cursor, VS Code) with no per-client secret and no manual token."
tech: [Model Context Protocol, TypeScript, Node.js, Azure API Management, Entra ID, OAuth 2.0, OIDC, PKCE, AzAPI, Azure Container Apps, Terraform]
cover: null
date: 2026-07-13
order: 4
draft: false
category: "AI"
status: "Shipped"
links: {}
---

A reusable way to take a team's **Model Context Protocol** server from source to a
live, internet-reachable endpoint that any MCP client can connect to — **gated by
enterprise identity**, with no per-client secret and no manual token. The hard
part wasn't the transport; it was making standards-based MCP OAuth work against a
real enterprise identity provider and the bridge clients people actually use. I
took it from "works in a demo" to "works, and keeps working."

## What I built

- **Native MCP publishing on a shared API gateway** — each team's containerized
  MCP server (TypeScript, Streamable HTTP) is registered as a first-class MCP
  server through infrastructure-as-code, reached privately over the platform
  network. No per-team gateway.
- **Per-team, group-gated OAuth.** Enterprise identity *is* the access decision:
  add a user to the team's security group and they're in; the gateway enforces it
  on every request.
- **Seamless, standards-based discovery** so compliant MCP clients connect with
  zero manual configuration.
- **Real-client support** — proven with the bridge clients Claude Desktop, Claude
  Code, Cursor and VS Code use, including **durable token refresh** across a full
  working session.
- **Staging and production slices** so a build can be exercised through the real
  gateway and identity gate before it's promoted.
- **CI/CD** that builds and ships images from source to staging to production.

## At a glance

```text
 MCP client ─▶ API gateway  (identity-gated)  ─▶  team's MCP server
                    │
                    ▼  standards-based OAuth discovery → enterprise identity provider
```

## Why it was hard

Standards-based MCP auth looks simple until it meets a strict enterprise identity
provider and a bridge-based client. I diagnosed and resolved several deep
OAuth 2.0 / OIDC interoperability failures — spanning resource-indicator
handling, token-refresh identity, and tenant consent policy — from first
principles, reading the protocol specs rather than guessing. The result is a
pattern that "just works" for the end user: sign in once, and every MCP tool
appears.

## Skills

Model Context Protocol · OAuth 2.0 / OIDC / PKCE internals · API-gateway policy &
native-MCP publishing · Entra ID app-registration, app-role & group-based access
design · protocol debugging from first principles · Infrastructure as Code ·
CI/CD for containerized apps.
