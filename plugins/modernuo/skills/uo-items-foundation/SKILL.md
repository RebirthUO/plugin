---
name: uo-items-foundation
description: Use when creating, debugging, or reviewing a ModernUO-based Item type, construction, ownership/parent movement, equipment hooks, OPL, decay, LootType, deletion, duplication, or serialization. Do not use for AoS property mechanics, craft registration, or loot probability except at the item lifecycle boundary.
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
    - ultima-online
    - modernuo
    - items
    - serialization
    - properties
    related_skills:
    - uo-aos-item-properties
    - uo-loot-generation-artifacts
    - modernuo-serialization
    - modernuo-property-lists
version: 1.0.0
author: Crome696
---
# UO Items Foundation

## Boundary

Own the persistent item entity lifecycle and selection of the correct content base class. Route magical property semantics to `uo-aos-item-properties`, generated drop policy to `uo-loot-generation-artifacts`, and generator/migration details to `modernuo-serialization`.

## Core Workflow

1. Classify the item: generic, weapon/ranged, armor/shield, clothing, jewel, container/quiver, consumable, reagent/food, scroll/book, or addon. State era, acquisition, transfer/death behavior, and persistence needs.
2. Read repository guidance, the chosen base class, adjacent concrete items, property-list conventions, serializer migrations, and focused tests. Prefer content-layer extension; engine `Projects/Server` changes require an explicit cross-cutting need.
3. Define the lifecycle before code: construct -> spawn/add -> parent/container/equip -> use/move/trade/death -> dupe/save/load -> decay/delete. Identify timers, references, mods, and cleanup for every transition.
4. Follow local generator conventions: `partial`, constructible factory where required, dense persistent fields, versioned migration, default/legacy initialization, and symmetric dupe/delete behavior. Runtime timer tokens are rebuilt, not serialized.
5. Build OPL through `base.GetProperties` first, established clilocs/handlers, correct row ordering, and invalidation after state changes. Do not assume `LootType.Blessed` blocks all trade or transfer paths.
6. Keep hot paths single-threaded and spatial: no global world iteration, ad-hoc threads/tasks/locks, or leaked timers/references.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Provide the chosen base class and rationale, lifecycle/persistence table, OPL and transfer/death behavior, compatibility risks, changed files, and exact verification results.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for the detailed item anatomy, base-class table, OPL/LootType/decay examples, and fixture notes.
- Read [analyzing-modernuo-subsystems.md](references/analyzing-modernuo-subsystems.md) only when turning another subsystem into durable skill guidance.
- Run [validate_cromesdk_skill.py](scripts/validate_cromesdk_skill.py) only for a CromeSDK-marked skill package; it is not an item-runtime validator.

## Verification

- Build and run focused item/serialization/OPL/lifecycle tests in the initialized UOContent collection.
- Cover constructibility, defaults, equip/unequip or parent transitions, OPL/invalidation, transfer/death behavior, dupe, current and legacy save paths, and delete cleanup.
- Search for global world scans and persistent timer tokens.
- Self-check that every added mod/timer/reference has a symmetric removal path.
