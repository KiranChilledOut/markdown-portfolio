---
title: "Voice-Driven Agent Orchestration Platform"
summary: "A personal, voice-controlled, immersive 3D platform that orchestrates coding agents — you speak, the right agent wakes in a game-like world, runs real work, and speaks the result back."
tech: [FastAPI, Python, SQLAlchemy 2.0 async, Alembic, Claude Agent SDK, faster-whisper, TTS, Milvus, Langfuse, Prometheus, React, TypeScript, Vite, Three.js, Zustand, Docker Compose]
cover: null
date: 2026-06-28
order: 9
draft: false
category: "AI"
status: "Active"
links: {}
---

A single command-and-speak interface that turns spoken intent into real,
agent-executed work with spoken results — a full-stack, voice-native,
AI-orchestration experience built end to end.

## What I built

- **An async backend orchestrator** (FastAPI + SQLAlchemy async + Alembic) that
  spawns coding-agent subprocesses and streams their results back in real time,
  with an event/streaming layer and structured logging (correlation IDs, secret
  scrubbing).
- **A complete voice pipeline:** microphone capture, voice-activity detection,
  local speech-to-text, wake/activation logic, turn/barge-in handling, and
  text-to-speech playback — all wired through a session state machine.
- **An agent runtime and lifecycle layer** with a generic skill-file format,
  agent templates, and implementations (code-review, learning, analysis-only
  trading, infrastructure), orchestrated by the Claude Agent SDK against a local
  token forwarder.
- **An immersive React + Vite + TypeScript + Three.js front end:** a
  boot/enter-gate sequence, a 3D world scene with agents as entities,
  waveform/push-to-talk controls, live transcript, results stream, and tabbed
  settings — all driven over REST and WebSockets.
- **A spec-driven build ledger** with test-driven-development gates, a
  coverage-enforced CI gate (ruff + mypy strict + pytest), and
  contract/snapshot/load (Locust) test suites.
- **Observability and ops surfaces:** Prometheus metrics, tracing, a vector
  store for agent memory/feedback, a CLI, and production deploy compose files.
- **A self-healing supervisor loop and resume-from-ledger design** so long
  autonomous build/run sessions survive crashes and context resets.

## Skills

Async system & agent-orchestration design · voice/real-time pipeline
engineering (STT/TTS/VAD/WebSockets) · immersive 3D front-end (React +
Three.js) · spec-driven, test-first autonomous development · observability and
resumable long-running systems.
