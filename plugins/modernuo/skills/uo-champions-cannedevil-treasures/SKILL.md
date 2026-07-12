---
name: uo-champions-cannedevil-treasures
description: Use when adding, debugging, or auditing Champion Spawn/CannedEvil altars, candle progression, champions, Harrower skulls, Doom or Treasures event integration, and facet-specific rewards in a ModernUO-based repository. Do not use for generic combat, region infrastructure, or ordinary loot packs.
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
    - champion-spawns
    - pvm
    - artifacts
    related_skills:
    - uo-world-facets-regions
    - uo-loot-generation-artifacts
    - uo-combat-pipeline
version: 1.0.0
author: Crome696
---
# UO Champions, CannedEvil, and Treasures

## Boundary

Own encounter-controller state, activation/progression, boss transition, participant credit, event-specific rewards, and integration with the enclosing region. Route spatial/travel rules to `uo-world-facets-regions`, generic drop construction to `uo-loot-generation-artifacts`, and damage formulas to `uo-combat-pipeline`.

## Core Workflow

1. Name era, facet, encounter family, canonical parity versus custom policy, and reward scope. Source exact candle/kill/reward claims; do not treat community percentages as code truth without reconciliation.
2. Inspect the active controller under `Engines/CannedEvil`, its spawn-info/type table, generator/spawn data, region binding, serialization, boss death callback, damage-credit logic, and focused tests. For Doom, ToT, or another Treasures event, inspect that engine separately rather than assuming Champion semantics.
3. Trace the state machine end to end: inactive -> activation -> spawn waves -> progress/decay -> champion -> completion/reset. Verify restart behavior and cleanup of spawned mobiles/items/timers.
4. Trace rewards independently: eligible participants, facet gate, skull/power-scroll/artifact/gold paths, backpack-versus-corpse delivery, duplicate prevention, and event enablement. Keep ordinary adds, champion rewards, and event currency distinct.
5. For a new altar/type, wire enum/info, controller, region, placement/generation, expansion gate, boss, reset, and tests. Class existence without generator/data reachability is incomplete.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Produce a state-transition summary, source and repo anchors, facet/reward matrix, lifecycle/economy risks, changed surfaces, and exact validation results. Label inaccessible or conflicting event details `Needs source confirmation`.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for the historical architecture, champion/Star Room/Doom/ToT tables, examples, and pitfalls. Re-check exact coordinates, drop rates, era labels, and event-account restrictions before implementing them.

## Verification

- Build and run focused controller/reward/region tests.
- Cover activation, progress thresholds, decay/backslide, champion spawn/kill/reset, restart serialization, and spawned-entity cleanup.
- Cover participant credit and positive/negative facet reward cases; prove travel/pet restrictions through the region owner.
- Self-check that event-specific rewards were not inserted into a generic loot pack and that a new encounter is reachable in world data.
