---
name: migrate-packets
description: Use when converting RunUO Packet subclasses, PacketWriter/PacketReader code, or packet-handler registration to ModernUO span-based networking. Covers outgoing buffers, incoming readers, function-pointer registration, and text safety. Do not use for protocol design or unrelated networking changes.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, packets, networking]
    related_skills:
      - migrate-foundation
      - modernuo-networking
      - modernuo-string-handling
      - modernuo-code-audit
      - modernuo-threading
---

# RunUO to ModernUO Packet Migration

## Boundary

Convert an existing, known packet contract. Do not invent IDs, lengths, field widths, endianness, encoding, or client-version rules.

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Trace packet ID, fixed/variable length, every field, callers, registration, and supported client versions.
2. Compare with the current local `SpanWriter`, `SpanReader`, packet initialization, send, and incoming registration APIs.
3. For outgoing packets, replace the class with the repository's static create/send pattern, initialize the exact buffer length, and guard `CannotSendPackets()`.
4. For incoming packets, register the exact ID/length and handler function pointer in the expected startup phase; update the handler to `SpanReader`.
5. Use bounded/safe text readers and writers with the protocol's actual encoding and terminator rules.
6. Test representative minimum, maximum, malformed/truncated, cannot-send, and client-version paths; compare emitted bytes with a known-good fixture or capture.

## Safety gates

- Reject migration when the wire contract is ambiguous; request evidence instead of guessing.
- Preserve fixed vs variable packet framing and all reserved bytes.
- Validate lengths before reads and validate user-controlled indices, strings, and entity references.
- Keep game-state work on the event loop; do not introduce background networking callbacks.

## Verification/self-check

Compare the complete emitted/consumed byte layout with a known-good fixture or capture and exercise malformed/truncated and cannot-send paths. Recheck every ID, length, width, encoding, and client gate.

## Output contract

Return the migrated registration/create/send code, a byte-level field map, call-site changes, fixture or capture evidence, verification results, and any unverified client compatibility.

## Reference routing

- Read [modernuo-networking](../modernuo-networking/SKILL.md) for current local packet APIs.
- Read [modernuo-string-handling](../modernuo-string-handling/SKILL.md) only for packet text encoding/formatting.
