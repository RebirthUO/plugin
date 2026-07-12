# Spawner Runtime Lifecycle

Use this reference for `BaseSpawner` behavior, concrete spawner selection, spawned-entity ownership, persistence, and spatial-cache work. Re-read the active branch before relying on a member name or default.

## Source map

| Surface | Current anchors | Responsibility |
|---|---|---|
| Base runtime | `Projects/UOContent/Engines/Spawners/BaseSpawner.cs` | Shared identity, entries, delays, counts, running state, spawn/remove, ownership, and serialization hooks |
| Standard placement | `Projects/UOContent/Engines/Spawners/Spawner.cs` | Explicit bounds/home range and ordinary timed population |
| Region placement | `Projects/UOContent/Engines/Spawners/RegionSpawner.cs` | Placement constrained to a resolved `BaseRegion` |
| Proximity activation | `Projects/UOContent/Engines/Spawners/ProximitySpawner.cs` | Trigger-range activation, optional message, and instant behavior |
| Entries | `Projects/UOContent/Engines/Spawners/SpawnerEntry.cs` | Spawn type, amount/weight, construction, and child tracking |
| Position search | `Projects/UOContent/Engines/Spawners/SpawnPositionState.cs` | Bounded candidate selection and validity checks |
| Spatial cache | `Projects/UOContent/Engines/Spawners/SectorSpawnCache.cs` | Sector-indexed spawner lookup and invalidation |
| Staff control | `Projects/UOContent/Engines/Spawners/SpawnerGump.cs`, `SpawnerControllerGump.cs`, `SpawnPropsGump.cs` | Inspection and mutation; not the source of runtime invariants |

## Lifecycle trace

1. A concrete spawner is constructed from a DTO, staff command, or deserialization.
2. Configuration establishes GUID, map/location or region/bounds, entries, target count, delays, and movement/home behavior.
3. World placement registers the spawner item and any sector-cache participation.
4. Running/timer logic compares owned live children with configured demand and selects an eligible entry.
5. Position search produces a bounded candidate accepted by map, terrain, occupancy, and spawner policy.
6. The child is constructed and placed, then associated with its owning spawner/entry.
7. Death, deletion, explicit removal, respawn, re-import, or spawner deletion must reconcile child tracking and cache state.
8. Save/load restores durable configuration and identity; runtime timer/cache tokens are rebuilt.

Trace the actual callbacks in the active branch. Do not infer cleanup from a collection disappearing: prove the child, timer, cache entry, and owner reference all converge.

## Invariants

- `Count` is aggregate demand; each `SpawnerEntry` also constrains how much of its type may exist. Verify weighted selection separately from maximum population.
- A child belongs to one spawner identity at a time. Reassignment, deletion, and import replacement must not leave stale ownership.
- `Map.Internal`, unresolved regions, missing types, impossible bounds, or exhausted position attempts must fail without leaking a world item.
- Pausing a spawner and deleting one are different states. Define whether existing children remain, are removed, or are adopted before changing behavior.
- Runtime timers and cache membership are derived state. Persist configuration and identity, then rebuild transient scheduling/indexes.
- Moving or deleting a spawner must update spatial registration. A cache lookup returning an old location is a correctness and performance bug.

## Hot-path checks

- Keep spawn checks on the game loop and use map/sector APIs; never enumerate `World.Items` or `World.Mobiles` per tick.
- Respect existing maximum spawn attempts. An impossible location must terminate predictably.
- Avoid repeated reflection/type discovery during ordinary ticks; resolve or cache through established infrastructure.
- Do not deserialize arbitrary JSON directly into live `Item` instances. The DTO boundary exists so malformed data can fail before world registration.

## Failure review

For every change, ask:

1. Can construction throw after a live item is registered?
2. Can a child be added before owner tracking succeeds?
3. Can a child die/delete without reducing the tracked live count?
4. Can re-import replace a spawner while preserving its old children or cache entry accidentally?
5. Can save/load duplicate scheduling, children, or GUID identity?
6. Can a region/map unload or era gate leave an unreachable active spawner?

## Verification anchors

Use focused tests under `Projects/UOContent.Tests/Tests/Engines/Spawners/` and server map spawnability tests under `Projects/Server.Tests/Tests/Maps/`. Cover lifecycle behavior with deterministic clocks/randomness where available, then perform a small in-game placement/respawn/removal check.
