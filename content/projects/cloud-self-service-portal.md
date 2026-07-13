---
title: "Cloud Self-Service IT Portal"
summary: "An internal web portal that lets employees request access, run automations, and manage cloud identity and resources through a self-service UI backed by a cloud identity provider."
tech: [Django, FastAPI, Python, MSAL, Microsoft Graph API, PostgreSQL, Azure DevOps REST API, Jira Service Desk, DRF, Docker, Gunicorn, Pandas]
cover: null
date: 2026-06-28
order: 6
draft: false
category: "Cloud"
status: "Shipped"
links: {}
---

An internal portal that turns manual, ticket-driven IT and cloud-admin work
into auditable, permission-gated self-service workflows — giving end users
direct access to access requests and automations while reducing toil.

## What I built

- **Unified web stack** serving a Django app alongside a FastAPI API (mounted
  under a sub-path) behind a single ASGI entrypoint, with API-key auth for
  programmatic access that users generate in the UI.
- **OAuth2/MSAL authentication layer** against the cloud identity provider,
  with token lifecycle middleware that validates, refreshes, and persists
  tokens, plus group-membership sync middleware.
- **A group- and per-view permission system** with admin overrides, so each
  portal feature is gated by identity-group membership and enforced centrally
  through a permission-check helper.
- **Self-service views** covering identity-graph queries, identity-app updates,
  role-assignment analysis, access-package reporting, and an admin center —
  many backed by background jobs with progress tracking and CSV exports.
- **Integrations** with the IT ticketing system (create service requests,
  discover request types, map field metadata, encrypted credential storage) and
  with the DevOps pipeline platform (trigger and monitor pipelines via REST).
- **Custom management commands** for token refresh/cleanup and for generating
  role-assignment and access-package reports as queued background jobs with
  dual-CSV output.
- **Containerized deployment** (slim Python image, gunicorn/uvicorn, WhiteNoise
  for static files) with dev/staging/production settings tiers.

## Skills

Full-stack web architecture & ASGI integration · Identity & access management
(OAuth2/MSAL, group-based RBAC) · cloud API integration (Graph, DevOps
pipelines) · background job design with progress tracking & reporting ·
containerization & multi-environment configuration.
