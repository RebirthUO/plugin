---
name: uo-world-facets-regions
description: Use when adding, debugging, or auditing ModernUO-based maps/facets, Region definitions/lifecycle hooks, overlap priority, travel restrictions, guarded/dungeon/champion/house zones, spatial queries, or spawn-package reachability. Do not use for combat, spells, housing, or encounters except at their explicit region boundary.
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
    - facets
    - regions
    - world
    related_skills:
    - modernuo-regions
    - uo-housing-houses-multis
    - uo-champions-cannedevil-treasures
    - uo-official-evidence
version: 1.0.0
author: Crome696
---
# UO World, Facets, and Regions

## Boundary

Own map registration/spatial indexing, JSON-driven region construction, overlap/priority, lifecycle hooks, travel/resource/harm/entry policies, and spawn-package placement/reachability. Route house aggregate behavior, champion controllers, combat formulas, and spell effects to their owning skills.

## Core Workflow

1. State ruleset/era, local map/facet, coordinates/area/Z range, region type/priority, affected hooks, travel/resource/combat policy, and canonical versus custom intent.
2. Inspect current map definitions, region JSON/schema/deserializer, concrete `Region` subclass, parent/overlaps, `SpellHelper` travel matrix, spawn data/loader, registration lifecycle, and focused tests. Verify the map exists locally; product vocabulary is not implementation.
3. Trace construction and runtime: data -> expansion filter -> typed region -> registration/sector lookup -> enter/exit/priority selection -> hook -> deregistration/reload. For spawns, trace data -> type resolution -> placement -> timer/persistence -> cleanup.
4. Put local policy in the narrow region hook and delegate shared travel checks to the central matrix. Return/block using established APIs; do not scatter `Map ==` checks or throw from normal veto hooks.
5. Use `Map.GetItemsInRange<T>` / `GetMobilesInRange<T>` and pooled patterns where required; never scan `World.Items`/`World.Mobiles` in spatial gameplay.
6. Check overlap priority, parent behavior, Min/Max expansion, dynamic cleanup, and data reachability. A region class without a loaded definition is incomplete.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return a map/region/overlap diagram or table, hook/travel matrix, JSON/spawn anchors, era/reachability status, lifecycle/performance risks, changed files, and exact validation results.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for detailed facet, sector, hook, travel, JSON, champion/faction/dungeon, spawn, and example notes. Re-check facet counts, region counts, travel claims, and schema casing in current code/data.

## Verification

- Parse/load data and run focused region/travel/spawn tests plus a startup validation when appropriate.
- Cover inside/outside/boundary/Z, overlap priority, allowed/blocked travel and harmful/entry cases, pre-era/target-era loading, enter/exit, reload/delete cleanup, and type resolution.
- Confirm no global spatial scans and no orphan registrations/spawns.
- Self-check that a facet-wide rule was not used where a nested region owns the policy.
