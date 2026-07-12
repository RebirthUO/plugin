---
name: modernuo-regions
description: >
  Use when creating or changing ModernUO static or dynamic regions, dungeon or
  town sub-zones, travel/housing/spawn rules, region JSON, parent inheritance,
  or region lifecycle. Do not use for range-query geometry alone; route that to
  modernuo-spatial-range-geometry.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, regions, facets, spatial-rules, travel]
    related_skills:
      - modernuo-code-audit
      - modernuo-performance-hot-paths
      - modernuo-content-patterns
      - modernuo-serialization
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-era-expansion
      - uo-world-facets-regions
      - modernuo-spatial-range-geometry
---

# ModernUO Regions

## Boundary

Own spatial rule inheritance, JSON/type registration, travel and housing policy,
dynamic register/unregister behavior, and world-load restoration. Exact AoE/range
math belongs to `modernuo-spatial-range-geometry`; object cleanup details belong
to `modernuo-lifecycle-cleanup`.

## Workflow

1. Record the map, bounds, Z semantics, parent region, base class, priority,
   affected hooks, era gate, and staff behavior.
2. Prefer an existing region type. For JSON-defined regions, verify type
   registration and schema shape; for dynamic regions, derive the parent from
   `Region.Find(location, map)` unless isolation is intentional.
3. Override only the behavior that differs and preserve parent delegation/base
   calls unless the rule intentionally blocks it.
4. For item/controller regions, centralize replacement: unregister the old
   region, validate owner/map, create and register one replacement.
5. Invoke replacement on location/map/enable changes and unregister on deletion.
   Restore only after the required world/map/parent state is available.
6. Test inside/outside boundaries, parent inheritance, travel/housing policy,
   movement/recreation, deletion, and save/load.

## Guardrails

- Choose the semantic base: `BaseRegion` for general rules, `DungeonRegion` for
  dungeon defaults, `GuardedRegion`/`TownRegion` for guards, and existing
  no-travel/no-housing variants when they already express the rule.
- Dynamic regions must never double-register or leave the old instance active.
- Use deferred `[AfterDeserialization(false)]` for cross-world dependencies;
  add a zero-delay timer only when the current repository pattern requires a
  further tick boundary.
- Travel/spell restrictions normally preserve the established staff bypass.
- `Region.Find(point, map)` is suitable for gameplay; `Region.Find(name, map)` is
  a linear lookup for startup/config/admin paths.
- Housing, travel, spawn, combat, and facet changes are gameplay changes; keep
  their source/era decision explicit.

## Output Contract

Return the region type/base, map/area/parent, changed hooks, lifecycle table,
player/staff behavior, era/source decision, and verification. Review findings
must identify whether the risk is a ghost region, lost parent rule, hot lookup,
or incorrect spatial policy.

## Verification

- Boundary tiles and parent inheritance behave as intended.
- Register/unregister is exactly once across move, map change, disable, delete,
  and load.
- Travel, housing, spawn, and staff cases are tested independently where changed.
- Focused tests/build and any in-game smoke check are reported separately.

## Reference Routing

- Read [dynamic and JSON region patterns](references/dynamic-region-patterns.md)
  when selecting a base, parent, lifecycle hook, or JSON registration.
- Load `modernuo-lifecycle-cleanup` for owned-resource cleanup,
  `modernuo-serialization` for load hooks, and `uo-world-facets-regions` for UO
  world/era policy.
- Read `dev-docs/regions.md` for the current hook and type inventory.
