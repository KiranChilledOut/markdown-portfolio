---
title: "Entra Access Package Manager"
summary: "A Terraform-driven platform for managing Microsoft Entra ID access packages at scale across multiple catalogs, with approval/review workflows and Slack/Logic App request notifications."
tech: [Terraform, Microsoft Entra ID, Azure, PowerShell, Microsoft Graph API, Azure Logic Apps, Slack API, GitLab CI]
cover: null
date: 2026-06-28
order: 5
draft: false
category: "Security"
status: "Shipped"
links: {}
---

A platform for provisioning, approving, and reviewing Microsoft Entra ID
entitlement-management access packages through version-controlled tfvars and
merge requests instead of manual portal clicks — dramatically cutting HCL
boilerplate while keeping cross-cutting notifications and access reviews
consistent.

## What I built

- **Built a reusable Terraform module** that turns each access package from
  ~160 lines of repeated flat HCL into ~12 lines of declarative data, modeled
  on a single typed per-catalog tfvars "request form" (display name,
  description, groups/apps, approver UPNs).
- **Migrated two large catalogs** from flat HCL (the largest ~13,600 lines)
  into the modular pattern, using hundreds of `moved {}` blocks to remap state
  addresses so no live resources were destroyed or recreated.
- **Designed an "outliers" pattern** so packages with state quirks the module
  shouldn't accommodate stay in flat HCL — enabling incremental, low-risk
  migration instead of a big-bang rewrite.
- **Automated Entra custom-extension wiring** (Slack / Logic App notifications)
  that the `azuread` provider can't model, via a PowerShell script run through
  `terraform_data` + `local-exec` calling Microsoft Graph — made idempotent and
  non-destructive (faithful read-modify-write of policy), quiet-planned with
  `triggers_replace`.
- **Standardized three assignment policies per package** (12hr / 4-week /
  indefinite) with ordered approvers and quarterly access reviews, configurable
  per catalog while keeping module defaults backward-compatible.
- **Wrote a custom Claude Code skill** that enforces a tfvars-only edit boundary
  (refusing to touch module/HCL wiring), routes requests to the right
  per-catalog schema, and documents the add/modify/backfill/remove/extend
  flows.

## Skills

IaC module design and refactor · Terraform state migration (moved blocks,
drift avoidance) · Microsoft Entra ID entitlement management & approval
workflows · Microsoft Graph API automation · CI/CD guardrails & safe-change
boundaries.
