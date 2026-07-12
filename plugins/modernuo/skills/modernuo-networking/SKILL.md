---
name: modernuo-networking
description: >
  Use when creating or modifying ModernUO packet encoders, incoming handlers,
  NetState sends, SpanWriter/SpanReader protocol code, or client message fan-out.
  Do not use for ordinary gameplay text alone; route formatting concerns to
  modernuo-string-handling.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, networking, packets, spanwriter, protocol]
    related_skills:
      - modernuo-code-audit
      - modernuo-threading
      - modernuo-performance-hot-paths
      - modernuo-string-handling
      - modernuo-test-workflow
      - migrate-packets
---

# ModernUO Networking and Packets

## Boundary

Own packet layout, registration, validation, send eligibility, and protocol-safe
buffer use. Preserve client compatibility and game-thread ownership. Prefer the
existing `Mobile`, `Item`, and `NetState` message APIs over hand-built packets
when the task is only player-facing text.

## Workflow

1. Find the protocol specification and nearest current packet implementation.
   Record packet/subcommand ID, fixed or variable length, endianness, encoding,
   client/expansion gate, and authorization assumptions.
2. For outgoing packets, expose a `NetState` send helper and a deterministic
   `Create*` encoder. Check `CannotSendPackets()` before building or sending.
3. Use `stackalloc` for small bounded packets and `SpanWriter`/the repository pool
   for variable or larger payloads. Initialize the packet and finalize variable
   lengths exactly once.
4. Register incoming handlers in `Configure()` with the correct length and
   in-game gate. Validate remaining input, entity lookup, state, permissions,
   range/ownership, and value bounds before mutation.
5. Compare encoded bytes and handler behavior with a neighboring packet; add a
   focused round-trip, byte-layout, or handler test when practical.

## Guardrails

- UO packet integers are big-endian unless the protocol explicitly requires a
  `WriteLE`/`Read*LE` variant.
- Never trust client serials, lengths, indexes, strings, or enum values. A
  successful read is not authorization.
- Fixed buffers must match the declared length; variable packets must write the
  actual packet length after the payload.
- Avoid `new byte[]` in repeated sends and avoid pre-building strings when a
  handler-aware message API can format at the call site.
- Do not move game-state mutation to network worker threads. Follow the existing
  incoming dispatch boundary and `modernuo-threading` rules.
- Preserve safe string decoders and control-character filtering where the
  neighboring handler uses them.

## Output Contract

Return the packet contract (ID/sub-ID, direction, length, fields, endianness,
encoding, gates), changed paths, validation decisions, and verification evidence.
For review findings, include the affected byte offset or input field and the
client/security consequence.

## Verification

- Exact byte layout and declared length match the protocol.
- Truncated, oversized, invalid-serial, unauthorized, and disconnected cases fail
  safely where relevant.
- Existing client/era behavior and neighboring packet tests remain green.
- State whether validation used tests, captured bytes, a client smoke check, or
  static reasoning only.

## Reference Routing

- Read [packet and message patterns](references/packet-patterns.md) when choosing
  writer/reader methods, allocation strategy, or message fan-out helpers.
- Read `dev-docs/networking-packets.md` for the current repository API surface.
- Load `modernuo-string-handling` for interpolated text and
  `modernuo-threading` for dispatch ownership.
