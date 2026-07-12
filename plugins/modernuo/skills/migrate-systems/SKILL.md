---
name: migrate-systems
description: Use when converting a multi-file RunUO engine or system with interdependent entities, persistence, commands, gumps, packets, configuration, or lifecycle hooks. Covers dependency mapping, staged conversion, integration order, and rollback. Do not use for a single isolated class or subsystem.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, systems, engines, lifecycle]
    related_skills:
      - migrate-foundation
      - migrate-persistence
      - migrate-serialization
      - migrate-commands-events
      - modernuo-configuration
      - modernuo-events
      - modernuo-lifecycle-cleanup
      - modernuo-code-audit
---

# RunUO to ModernUO Multi-File System Migration

## Boundary

Coordinate a system migration whose parts cannot be safely converted in isolation. Delegate mechanics to narrower skills; this skill owns sequencing, integration, and completeness.

## Workflow

1. Apply [migrate-foundation](../migrate-foundation/SKILL.md). Produce a file/symbol inventory and dependency graph covering data types, saved state, entities, UI, commands, packets, configuration, events, timers, tests, and entry points.
2. Mark external contracts: saved type names/versions, configuration keys, command names/access, packet IDs, data files, player-visible behavior, and era gates.
3. Choose vertical slices with a rollback boundary. Prefer this order where dependencies allow: data types; persistence; entities; runtime services; UI/commands/packets; startup integration.
4. For each slice, load only its relevant `migrate-*` and `modernuo-*` skills, inspect local precedent, implement, and verify before continuing.
5. Reconcile cross-references, registration order, idempotent startup/cleanup, and old-save migration after all slices compile.
6. Run focused tests per slice, then owning-project integration, save/restart, enable/disable, and failure-path checks.

## Safety gates

- Do not perform a big-bang rewrite without an inventory and staged validation.
- Preserve external IDs, names, config defaults, and persistence contracts unless explicitly changed.
- Do not double-register old and new entry points.
- Separate baseline failures from migration failures and keep unrelated files out of scope.

## Verification/self-check

Reconcile the final diff against the dependency inventory and external contracts, then run slice-level and owning-system integration/save-restart tests. Explain every unconverted or deferred dependency.

## Output contract

Return the dependency graph/inventory, ordered slices and owners, contract/compatibility decisions, changed files, validation matrix, rollback boundary, and remaining blockers. Explain every excluded source file or subsystem.

## Reference routing

- Route each dependency to its matching sibling migration skill.
- Read [modernuo-configuration](../modernuo-configuration/SKILL.md), [modernuo-events](../modernuo-events/SKILL.md), or [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) only when those surfaces exist.
