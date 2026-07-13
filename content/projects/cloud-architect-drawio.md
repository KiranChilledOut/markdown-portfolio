---
title: "Cloud Architect — draw.io Diagramming Skill"
summary: "An agent skill that teaches Claude Code, Codex CLI, and other AI coding tools to produce consistent, icon-accurate cloud architecture diagrams in draw.io — automatically."
tech: [Python, draw.io, Agent Skills, MCP]
cover: null
date: 2026-06-27
order: 3
draft: false
category: "DevOps"
status: "Shipped"
links:
  github: https://github.com/KiranChilledOut/Cloud-Architect-DrawIo-Diagramming
  live: ""
---

A portable **Agent Skill** that teaches AI coding agents to draw professional
cloud architecture diagrams in draw.io/diagrams.net — the way an architect
would, not as a messy one-off sketch.

## What it does

Drop the skill folder into Claude Code, Codex CLI, OpenCode, or Warp, and the
agent gains a structured playbook for diagramming. Ask it to diagram a system
and you get a clean, consistent, icon-accurate draw.io file back.

## What I built

- **A catalog of 1,686 verified cloud icons** — 648 Azure + 1,038 AWS — with a
  hard validation gate: the agent is *refused* permission to use any icon path
  it hasn't confirmed exists, so diagrams never render as broken placeholders.
- **Context-aware layout selection.** Auth flows get swimlanes, CI/CD pipelines
  get left-to-right stages, network topologies get thick borders and grouping —
  the shape follows the content, not a single generic style.
- **Anti-overlap layout rules** so boxes, connectors, and labels never collide.
- **Consistent color coding** — blue for the happy path / go, red for blocked,
  amber for secrets — applied the same way every time.
- **Flow animation on connectors** for review walkthroughs.
- **Tool-agnostic packaging** — one folder works across multiple agent
  platforms via standard skill directories, no per-tool glue code.
- Built against the **draw.io MCP server** so the agent emits real diagram XML
  that opens directly in diagrams.net.

## Why

"Quick, draw me the architecture" — the eight words that have ruined more
Friday afternoons than any outage. Every team recreates the same messy,
inconsistent diagram by hand. This turns that request into a fast, reproducible,
icon-correct output any teammate can produce to the same standard, no design
skill required.
