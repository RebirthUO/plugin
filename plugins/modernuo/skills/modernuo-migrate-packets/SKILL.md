---
name: modernuo-migrate-packets
description: Migrate an existing known RunUO packet contract, PacketWriter or PacketReader code, or packet-handler registration to span-based APIs verified in a specific ModernUO repository revision. Use for outgoing buffers, incoming readers, registration, framing, bounds, and packet text. Do not design new protocols or infer wire details.
---

# RunUO to ModernUO Packet Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require the complete source packet and callers, an authoritative wire contract or known-good fixture/capture, one explicit ModernUO repository and revision, supported clients, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and applicable build/test facilities. Verify local writer, reader, initialization, send, and registration APIs before editing.

Return `BLOCKED_INPUT` for missing scope, `BLOCKED_EVIDENCE` for ambiguous ID, framing, lengths, widths, endianness, encoding, terminators, reserved bytes, or client gates, and `VALIDATION_FAILED` for failed required checks. Never guess protocol bytes and never edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Trace packet ID, fixed/variable framing, every field offset/width, callers, registration, and client gates.
2. Implement outgoing creation/send and incoming registration/reading using only APIs proven at the target revision.
3. Validate declared and remaining lengths before reads; validate user-controlled indices, strings, and entity references.
4. Preserve reserved bytes and use bounded text operations with the proven encoding and terminator rules. Packet encoding remains owned here; do not delegate wire-format decisions to a general string skill.
5. Keep game-state work on the event loop; use [modernuo-threading](../modernuo-threading/SKILL.md) when ownership crosses threads.
6. Compare complete emitted and consumed byte layouts with the fixture/capture. Test minimum, maximum, malformed/truncated, cannot-send, and every supported client gate.

## Result contract

This skill owns the top-level result; embed string/threading outputs as evidence and propagate their blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with byte map `Offset | Width | Meaning | Encoding | Evidence`; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires byte-for-byte proof and every applicable negative path.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map sibling blockers and embed ready evidence. Use confidence `high` only for direct wire/revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, packet/client scope, fixture, and mode; `# Checklist` covers every wire and negative-path category; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, missing captures, recovery input, or `None`.

Recheck every ID, length, offset, width, encoding, terminator, reserved byte, and client gate against cited evidence. Keep official gameplay claims separate from repository and protocol evidence.
