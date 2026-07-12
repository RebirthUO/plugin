---
name: migrate-foundation
description: Use when starting any RunUO-to-ModernUO migration or applying cross-cutting namespace, naming, logging, time, pooling, threading, and performance conventions. Load before specialized migrate-* skills. Do not use alone for serialization, timers, gumps, packets, persistence, or other subsystem migrations.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, foundation, csharp]
    related_skills:
      - migrate-serialization
      - migrate-items-mobiles
      - migrate-timers
      - migrate-gumps
      - migrate-packets
      - migrate-property-lists
      - migrate-commands-events
      - migrate-persistence
      - migrate-systems
      - modernuo-code-audit
      - modernuo-serialization
      - modernuo-lifecycle-cleanup
      - modernuo-threading
      - modernuo-performance-hot-paths
---

# RunUO to ModernUO Migration Foundation

## Boundary

This is the required cross-cutting pass for RunUO migrations. It establishes local conventions and routes subsystem work; it does not replace a specialized migration skill.

## Workflow

1. Inventory source files, type names, namespaces, registrations, serialized state, timers, persistence, UI, packets, and cross-file dependencies.
2. Inspect the nearest current ModernUO implementation before changing an API. Record which specialized skills apply.
3. Apply only proven cross-cutting changes: file-scoped namespaces where locally standard, `[Constructable]` to `[Constructible]`, new private fields as `_camelCase`, structured logging, and `Core.Now` for server-time semantics.
4. In game-loop code, replace global world scans with map/sector queries and avoid new locks, tasks, threads, concurrent collections, or general `ArrayPool<T>`; route infrastructure concurrency to [modernuo-threading](../modernuo-threading/SKILL.md).
5. Classify hot, warm, and cold paths before replacing collections or LINQ. Prefer local precedent and measurement; do not mechanically rewrite cold code.
6. Apply subsystem migrations, then run [modernuo-code-audit](../modernuo-code-audit/SKILL.md) and the repository's focused build/test workflow.

## Required migration chain

Use, in order:

1. this foundation;
2. [migrate-serialization](../migrate-serialization/SKILL.md) when saved state or old-save identity exists;
3. each applicable subsystem `migrate-*` skill;
4. the corresponding `modernuo-*` runtime skill;
5. code audit and focused verification.

## Safety gates

- Do not rename untouched legacy fields merely for style.
- Do not delete `Serial` constructors or manual serialization until the serialization mode and old-save path are proven.
- Do not remove synchronization from server infrastructure without tracing its thread ownership.
- Preserve type identity with aliases when old saves encode a moved or renamed type.
- Treat era-dependent mechanics as unresolved until the target era/profile is known.

## Verification/self-check

Account for every inventory item and selected/omitted chain step, then run the scoped build/tests and code audit. Re-read the diff for incidental behavior changes and unsupported API assumptions.

## Output contract

Return a migration inventory, selected chain with skip reasons, changed files, compatibility decisions, build/test evidence, and residual risks. A completed migration must account for every saved field, registration, timer, owned reference, and user-visible behavior in scope.

## Reference routing

- Read the relevant sibling `migrate-*` skill only when its subsystem appears.
- Use [modernuo-performance-hot-paths](../modernuo-performance-hot-paths/SKILL.md) for allocation or query decisions and [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) for ownership cleanup.
