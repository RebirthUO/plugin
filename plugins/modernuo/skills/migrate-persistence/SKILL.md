---
name: migrate-persistence
description: Use when replacing RunUO WorldSave/WorldLoad handlers or custom binary files with ModernUO GenericPersistence for global, non-entity system state. Covers schema/version preservation, IGenericWriter/IGenericReader, dirty tracking, and load restoration. Do not use for Item/Mobile fields; use serialization migration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, persistence, saves, lifecycle]
    related_skills:
      - migrate-foundation
      - migrate-serialization
      - modernuo-serialization
      - modernuo-events
      - modernuo-lifecycle-cleanup
      - modernuo-code-audit
---

# RunUO to ModernUO Persistence Migration

## Boundary

Use `GenericPersistence` for global system data that does not belong to an `Item` or `Mobile`. Entity fields belong in [migrate-serialization](../migrate-serialization/SKILL.md).

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Inventory file paths, version markers, field order/types, entity references, mutation sites, missing-file behavior, and startup/save hooks.
2. Inspect a current local `GenericPersistence` implementation and the exact reader/writer APIs.
3. Define a stable persistence name and versioned read/write contract. Preserve the legacy read path or provide an explicit one-time migration when existing saves matter.
4. Replace file management and WorldSave/WorldLoad subscriptions with a registered `GenericPersistence` instance.
5. Write entity references with supported entity methods and read them with typed entity APIs; handle deleted or missing references.
6. Call `MarkDirty()` on every state mutation that must persist. Rebuild runtime-only indexes, timers, and registrations only in the correct post-load phase.
7. Test empty state, legacy load, current round trip, corrupt/unsupported version behavior, deletion/null references, and dirty/no-dirty saves.

## Safety gates

- Never reorder or reinterpret legacy fields without a versioned migration.
- Do not delete legacy files or loaders before a backup/rollback boundary and successful migration test exist.
- Fail safely on unsupported versions; do not silently read misaligned data.
- Keep runtime handles and caches out of serialized state.

## Verification/self-check

Test legacy and current round trips, unsupported/corrupt versions, entity deletion/nulls, and dirty tracking. Re-read the schema in write order and confirm the rollback boundary before removing old code.

## Output contract

Return the persistence class and registration changes, a schema/version table, legacy migration and rollback decision, dirty-tracking audit, verification evidence, and unresolved save-compatibility risks.

## Reference routing

- Read [modernuo-serialization](../modernuo-serialization/SKILL.md) for current reader/writer patterns.
- Read [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) when loaded state owns timers, events, entities, or other runtime resources.
- Consult the official [ModernUO serialization guide](https://modernuo.com/docs/development/serialization/) for a repository-independent cross-check.
