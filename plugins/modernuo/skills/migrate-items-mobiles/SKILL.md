---
name: migrate-items-mobiles
description: Use when converting RunUO Item, Mobile, or BaseCreature subclasses to ModernUO and coordinating their serialization, construction, timers, properties, ownership, and deletion lifecycle. Do not use for a subsystem-only migration or for designing brand-new content from scratch.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, items, mobiles, lifecycle]
    related_skills:
      - migrate-foundation
      - migrate-serialization
      - migrate-timers
      - migrate-property-lists
      - modernuo-content-patterns
      - modernuo-serialization
      - modernuo-lifecycle-cleanup
      - modernuo-code-audit
---

# RunUO to ModernUO Item and Mobile Migration

## Boundary

Own whole-entity migration for existing items, mobiles, and creatures. Route isolated save, timer, tooltip, or gump work to the narrower migration skill.

## Workflow

1. Apply [migrate-foundation](../migrate-foundation/SKILL.md) and inventory constructors, serialized fields/order, command properties, timers, owned entities, deletion hooks, property lists, context menus, loot, and era gates.
2. Choose the exact [serialization mode](../migrate-serialization/SKILL.md). Preserve old type identity and old-save reads before deleting manual methods or `Serial` constructors.
3. Convert the class to local generated-serialization conventions, including `partial`, `[Constructible]` where appropriate, and generated setters for persistent mutations.
4. Route runtime timers through [migrate-timers](../migrate-timers/SKILL.md); restore only runtime state after deserialization and cancel/clear owned state on deletion.
5. Convert tooltips with [migrate-property-lists](../migrate-property-lists/SKILL.md), context menus to the local pooled-list signature, and legacy names/corpse names to current overrides when supported.
6. Preserve AI, fight mode, stats, skills, loot, taming, access, and era behavior unless the request changes them.
7. Generate schemas when required, build the owning project, and test construct/add, save-load, property display, timer cleanup, and delete paths.

## Safety gates

- Mutate generated persistent properties, not backing fields, so dirty tracking runs.
- Never serialize `TimerExecutionToken` or other runtime-only handles.
- Do not start world-dependent restoration before the appropriate post-load phase.
- Do not change loot, economy, combat, or era behavior as incidental modernization.
- Verify base-call ordering in deletion hooks against the local hierarchy.

## Verification/self-check

Trace every saved field and owned runtime resource, run schema/build plus construct/save-load/delete tests, and compare player-visible stats/loot/behavior with the source contract.

## Output contract

Return the migrated entity files, serialization/identity decision, lifecycle ownership map, behavior-preservation notes, schema changes, verification evidence, and any old-save or era risk.

## Reference routing

- Use [modernuo-content-patterns](../modernuo-content-patterns/SKILL.md) only for local entity conventions and [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) for ambiguous ownership.
