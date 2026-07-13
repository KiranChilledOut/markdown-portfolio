---
title: "SillyJointTunnel"
summary: "Per-window remote display for macOS over Tailscale — stream a single Mac app window to a phone on the same tailnet with full keyboard/mouse control, built on a vendored RustDesk fork."
tech: [Rust, RustDesk, Tailscale, macOS ScreenCaptureKit, Swift, Flutter/Dart, Protobuf, WebSocket, CGEvent, Python]
cover: null
date: 2026-06-28
order: 7
draft: false
category: "IoT"
status: "Active"
links: {}
---

A standalone personal project that turns a Mac into a single, controllable app
window reachable from a phone over a zero-config private network — delivering
remote control with RustDesk-grade encryption and transport while keeping the
attack surface confined to the owner's tailnet.

## What I built

- **Vendored a RustDesk fork (v1.4.7)** as a submodule and built a Swift FFI
  bridge that reuses its video pipeline, end-to-end encryption, and transport
  rather than reinventing them — with no-op C stubs so the host compiles
  standalone during development.
- **Per-window capture on the Mac host** using ScreenCaptureKit, backed by an
  `AppEnumerator` that diffs `NSWorkspace` state against `CGWindow` listings
  with an icon cache and a guard for spurious/title-bar-only windows.
- **A ControlServer WebSocket** (RFC 6455 framing on a fixed port) with 32-byte
  token auth checked in constant time, per-IP rate limiting (failed-auth
  throttle + drop), heartbeat/drop, tailnet-only bind (never `0.0.0.0`), and
  per-connection source-CIDR checks.
- **An `InputInjector`** using `CGEvent` for keyboard and mouse, with modifier
  bitmasks, held-keys teardown, and coordinate math with clamp/scale to map
  phone gestures onto the captured window.
- **A protobuf protocol** with codegen across Swift/Dart/Python, including
  `oneof` enforcement and forward-compatible unknown-field skipping — verified
  by round-trip tests across all three languages.
- **A Flutter client** (Android-first, also desktop/iOS) with parallel tailnet
  discovery, secure-token storage, a multi-state Host Picker with QR/manual
  pairing, an App Picker, and a Stream View with a sticky-modifier dev
  keyboard, gesture layer, and a spec-compliant reconnect schedule.
- **A pragmatic transport pivot:** after profiling, replaced per-frame
  GPU-context allocation with a reusable one, and switched the streaming
  channel from base64-in-JSON to raw JPEG binary WebSocket frames when the full
  RustDesk media-toolchain build proved impractical to ship.

## Skills

Cross-platform systems integration (Swift host + Flutter client + Rust/RustDesk
bridge) · real-time video pipeline & binary protocol design · network security
hardening (auth, rate limiting, source validation, tailnet-only bind) ·
vendoring & fork maintenance · test-driven development across Swift, Python,
and Flutter.
