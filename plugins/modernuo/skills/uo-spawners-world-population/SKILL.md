---
name: uo-spawners-world-population
description: Use when adding, migrating, importing, exporting, debugging, or auditing ModernUO BaseSpawner implementations or Distribution/Data/Spawns JSON packs, including entries, bounds, timing, counts, era/facet selection, persistence, cleanup, and sector-cache behavior. Do not use for creature design, region policy, encounter controllers, loot, or calendar scheduling.
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
      - spawners
      - world-population
      - json
    related_skills:
      - uo-world-facets-regions
      - modernuo-content-patterns
      - modernuo-serialization
      - modernuo-performance-hot-paths
      - modernuo-test-workflow
version: 1.0.0
author: RebirthUO
---
# UO Spawners and World Population

## Boundary

Own spawner runtime machinery and world-population packages: concrete spawner selection, entry resolution, placement bounds, delays/counts, import/export, persistence, replacement, cleanup, and spatial cache behavior. Route the spawned mobile or item definition to `modernuo-content-patterns`, spatial policy to `uo-world-facets-regions`, and wave/boss progression to its encounter owner.

## Core Workflow

1. State the target era/profile, facet, package, spawner type, entries and weights/counts, placement mode/bounds, delays, home/walking range, and expected import or runtime behavior.
2. Inspect `Engines/Spawners`, the active JSON pack, profile/package loader, migrations, and focused tests. Confirm every entry type resolves in the configured assemblies and every map/region exists.
3. Trace data to runtime: JSON -> discoverable DTO -> validated concrete spawner -> world placement -> entry construction -> spawn-position search -> sector cache -> respawn/remove -> save/load/delete.
4. Preserve identity and cleanup. Treat GUIDs as replacement identity, reject invalid maps before world mutation, delete partially built entities on failure, and prove re-import does not leave duplicate spawners or children.
5. Keep hot paths spatial and bounded. Use map/sector queries and existing spawn-attempt limits; do not scan the full world or add blocking work to timer ticks.
6. Add or update round-trip, import cleanup, bounds, type discovery, migration, cache, and profile-reachability tests before relying on in-game observation.

## Evidence boundary

Establish expected official world population through `uo-official-evidence`. Repository code and data prove implementation state only; community spawn maps and emulator packs may aid discovery but cannot establish official composition, timing, density, or coordinates.

## Output Contract

Return a package/entry matrix, JSON-to-runtime lifecycle trace, era/facet reachability status, identity and cleanup analysis, migration/import rollback risks, changed source/data/tests, exact automated results, and remaining in-game checks.

## Reference Routing

- Read [spawner-runtime-lifecycle.md](references/spawner-runtime-lifecycle.md) for class roles, ownership, timing, cache, persistence, and cleanup.
- Read [spawn-package-schema-and-validation.md](references/spawn-package-schema-and-validation.md) when editing JSON packs, DTOs, type discovery, bounds, or profile reachability.
- Read [import-export-migration.md](references/import-export-migration.md) for command behavior, replacement identity, legacy formats, migrations, and rollback.

## Verification

- Run focused spawner JSON, round-trip, discovery, import cleanup, bounds, migration, and sector-cache tests.
- Cover valid and invalid maps/types, empty packs, duplicate locations/GUIDs, all concrete DTO types, pre-era/target-era package selection, save/load, re-import, delete, and child cleanup.
- Validate startup/package loading when reachability changes and perform a bounded in-game check for placement, respawn, walking/home range, and removal.
- Self-check that no content-only change became an engine-wide scan and no encounter controller was modeled as an ordinary spawner.
