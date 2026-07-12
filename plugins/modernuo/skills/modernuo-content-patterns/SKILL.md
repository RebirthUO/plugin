---
name: modernuo-content-patterns
description: Use when implementing new ModernUO items, mobiles, creatures, spells, skill handlers, loot, context menus, or other UOContent types. Routes shared patterns; specialist spawner, vendor, pet, and faction behavior stays with its domain skill. Do not use for taxonomy, parity, or RunUO migration.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, content, uocontent, gameplay, hub]
    related_skills:
      - modernuo-code-audit
      - modernuo-serialization
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-performance-hot-paths
      - modernuo-era-expansion
      - modernuo-property-lists
      - modernuo-gump-system
      - modernuo-commands-targeting
      - modernuo-events
      - modernuo-test-workflow
      - uo-spawners-world-population
      - uo-vendors-commerce
      - uo-pets-taming-stables
      - uo-factions-towns-sigils
---

# ModernUO Content Patterns

## Boundary

This is the implementation hub for new UOContent types. Use `modernuo-content-taxonomy` for classification/parity, `migrate-*` for conversion, and domain skills for spawner, vendor, pet, or Factions state.

## Workflow

1. Establish the target era/profile, player-visible behavior, authoritative evidence, non-goals, side effects, and owning content domain. If era changes behavior, stop until it is specified.
2. Inspect the nearest current sibling implementation, its base types, registration, tests, schemas, localization, and data files. Do not guess constructor or hook signatures.
3. Select the smallest shape from [content-shapes.md](references/content-shapes.md). Type construction stays here; specialist system behavior routes outward.
4. Implement the behavior with local conventions: generated serialization for durable entities, `[Constructible]` where staff construction is intended, explicit ownership/cleanup, and bounded game-loop work.
5. Preserve economy, loot, combat, housing, PvP/PvM, and client-presentation boundaries; do not add adjacent features incidentally.
6. Add behavior-level tests for success, rejection, era gates, lifecycle, persistence, and exploit boundaries. Generate schemas when required.
7. Run [modernuo-code-audit](../modernuo-code-audit/SKILL.md), focused tests, and the owning project; distinguish automated evidence from manual in-game/client checks.

## Core safety gates

- Persistent state uses generated setters/dirty tracking; runtime timers and temporary effects are not serialized.
- Every timer, event subscription, owned entity, and held reference has an owner and cleanup path.
- Loot and stat values require era/source support; no placeholder balance values are presented as parity.
- Property-list arguments, clilocs, gump responses, commands, and targets follow their dedicated safety rules.
- Hot paths avoid full-world scans, blocking work, and unmeasured allocation.

## Verification/self-check

Map each acceptance criterion and non-goal to code/tests, run schema/build/focused/owning checks after the final edit, and audit lifecycle, era, and economy/client side effects. Label remaining manual checks honestly.

## Output contract

Return changed content/registration/test/schema paths, source and era decisions, behavior and non-goal summary, lifecycle/persistence map, verification commands/results, and residual manual or parity checks.

## Reference routing

- Always read [content-shapes.md](references/content-shapes.md) for the selected type.
- For a temporary weapon enchantment, read [weapon-buff-spell-pattern.md](references/weapon-buff-spell-pattern.md).
- Route spawner, vendor, controlled-pet, and Factions state to their named `uo-*` domain skills.
- Load [modernuo-serialization](../modernuo-serialization/SKILL.md), [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md), [modernuo-gump-system](../modernuo-gump-system/SKILL.md), or other domain skills only when their surface exists.
