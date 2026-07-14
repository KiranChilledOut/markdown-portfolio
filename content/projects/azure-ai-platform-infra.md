---
title: "Azure AI Platform — Self-Service Infrastructure as Code"
summary: "A multi-stack Terraform landing zone that turns a one-line manifest entry into an isolated, least-privilege Azure environment — hub-and-spoke networking, a two-identity authorization model, and self-service onboarding behind a human-reviewed merge gate."
tech: [Terraform, Azure, azuread, AzAPI, Azure API Management, Azure Container Apps, Azure Firewall, Application Gateway, Private DNS, Azure Key Vault, Private Endpoints, TeamCity CI, GitLab, Bash]
cover: null
date: 2026-07-13
order: 4
draft: false
category: "Cloud"
status: "Shipped"
links: {}
---

An internal Azure platform that turns a **one-line manifest entry into a fully
isolated, least-privilege cloud environment** — provisioned end to end through
infrastructure-as-code, behind a human-reviewed merge gate. Product teams get a
fast, self-service environment; the platform keeps consistent guardrails,
network segmentation, and identity isolation without anyone hand-crafting cloud
resources.

## What I built

- **Designed a multi-stack Terraform landing zone** (hub-and-spoke) with a
  **two-identity authorization model** that structurally separates who *provisions*
  an environment from who runs *day-two* changes — so a team can never escalate
  its own access.
- **Built the shared platform hub** — API management, a container-app platform,
  Key Vault, and hub networking with firewall egress control, a WAF gateway,
  private DNS, and private endpoints for data-plane isolation.
- **Delivered manifest-driven onboarding and symmetric decommissioning** — one
  JSON entry renders a per-team stack and opens a single reviewed merge request;
  teardown is safe and archived for clean re-onboarding.
- **Automated the full CI/CD lifecycle** — plan/apply orchestration and MR gating,
  with change detection scoped per stack so the right pipeline runs as the right
  identity.
- **Hardened security end-to-end** — least-privilege identities, private data
  planes, and a strict *no-secrets-in-git* posture.
- **Audited the estate at scale** — ran a multi-agent review across the platform
  and turned the findings into a prioritized, safe-rollout hardening roadmap.

## At a glance

```text
 manifest entry ─▶ CI renders a per-team stack ─▶ reviewed MR ─▶ isolated environment
                                                                 own network · identity · RBAC
                                                                 egress via the shared hub
```

## Why it was hard

Multi-stack remote state with a shared module catalog; a deliberate identity
split enforced in code; deterministic, collision-free network allocation across
teams; preview-only Azure resources managed as code; and idempotent lifecycle
automation that recovers cleanly from partial failures — all kept auditable and
drift-free.

## Skills

Infrastructure as Code · Azure enterprise landing-zone & least-privilege identity
design · multi-stack Terraform state & module architecture · hub-and-spoke
network segmentation · CI/CD lifecycle automation · security hardening & secret
management.
