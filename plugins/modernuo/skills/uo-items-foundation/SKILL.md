---
name: uo-items-foundation
description: Use when creating, debugging, or reviewing ModernUO Item construction, ownership/movement, equipment, OPL, decay, LootType, death/corpse allocation, stealing, blessing, insurance, deletion, duplication, or serialization. Excludes AoS properties, craft registration, and loot probability beyond lifecycle.
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
    - uo-living-world-review
    - modernuo-serialization
    - modernuo-property-lists
version: 1.1.0
author: Crome696
---
# UO Items Foundation

## Boundary

Own the persistent item lifecycle and base-class choice, including ownership transitions through death, corpses, stealing, blessing, and insurance. Route magical properties, drop policy, and migrations to their specialist skills.

## Core Workflow

1. Classify the item: generic, weapon/ranged, armor/shield, clothing, jewel, container/quiver, consumable, reagent/food, scroll/book, or addon. State era, acquisition, actor, transfer/death/theft/insurance behavior, and persistence needs.
2. Read the base class, siblings, OPL conventions, relevant death/corpse/insurance consumers, migrations, and tests. Prefer content-layer extension; engine changes require a cross-cutting need.
3. Define construct -> parent/equip -> use/move/trade/steal/death/corpse -> dupe/save/load -> decay/delete. Record ownership, currency, timers, references, mods, and cleanup.
4. Follow local generator conventions: `partial`, constructible factory where required, dense persistent fields, versioned migration, default/legacy initialization, and symmetric dupe/delete behavior. Runtime timer tokens are rebuilt, not serialized.
5. Build OPL through `base.GetProperties` first, established clilocs/handlers, correct row ordering, and invalidation after state changes. Do not assume `LootType.Blessed` blocks all trade or transfer paths.
6. Keep hot paths single-threaded and spatial: no global world iteration, ad-hoc threads/tasks/locks, or leaked timers/references.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Provide base-class rationale, lifecycle/persistence and item-disposition tables, OPL/ownership/currency effects, compatibility/exploit risks, changed files, and exact verification results.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for the detailed item anatomy, base-class table, OPL/LootType/decay examples, and fixture notes.
- Read [item-loss-stealing-insurance.md](references/item-loss-stealing-insurance.md) for death allocation, corpse rights, stealing, blessing, insurance, criminality, and exploit checks.
- Read [analyzing-modernuo-subsystems.md](references/analyzing-modernuo-subsystems.md) only when turning another subsystem into durable skill guidance.
- Run [validate_cromesdk_skill.py](scripts/validate_cromesdk_skill.py) only for a CromeSDK-marked skill package; it is not an item-runtime validator.

## Verification

- Build and run focused item/serialization/OPL/lifecycle tests in the initialized UOContent collection.
- Cover constructibility, defaults, equip/unequip or parent transitions, OPL/invalidation, transfer/death behavior, dupe, current and legacy save paths, and delete cleanup. For item loss, cover corpse/backpack/equipment disposition, protected/unprotected states, currency changes, criminality, and stale/repeated interactions.
- Search for global world scans and persistent timer tokens.
- Self-check that every added mod/timer/reference has a symmetric removal path.
