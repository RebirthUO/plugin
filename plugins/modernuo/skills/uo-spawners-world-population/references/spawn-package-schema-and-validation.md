# Spawn Package Schema and Validation

Use this reference when editing `Distribution/Data/Spawns/**/*.json`, DTOs, discovery metadata, bounds, or profile/facet package selection.

## Data flow

Current JSON uses plain DTO records under `Projects/UOContent/Engines/Spawners/Json/`:

- `SpawnerDto.cs` defines shared fields and concrete `SpawnerDataDto`, `RegionSpawnerDto`, and `ProximitySpawnerDto` records.
- `SpawnerJsonSerializer.cs` owns serializer options and discoverable-type behavior.
- `Point3DArrayConverter.cs` owns compact location representation.
- `BaseSpawner.Dto.cs`, `Spawner.Dto.cs`, `RegionSpawner.Dto.cs`, and `ProximitySpawner.Dto.cs` map between durable data and runtime objects.

The intended boundary is:

```text
JSON bytes -> DTO graph -> validate map/type/shape -> construct one spawner -> apply DTO -> place in world
```

Do not move world registration into JSON conversion. `ToSpawner()` deletes its newly constructed item if applying DTO state throws; preserve that failure containment.

## Shared fields to inspect

The active DTO includes identity/name, location/map, count, minimum/maximum delay, team, walking range, entries, spawn-location mode, attempt limits, and a compact home-range form. Concrete types add either explicit bounds, a region name, or proximity trigger fields.

Before editing a pack:

1. Confirm the concrete JSON discriminator matches a discoverable DTO.
2. Confirm GUID uniqueness within the selected import set.
3. Resolve every `map`, region name, and entry type in the configured runtime assemblies.
4. Check count, entry amounts/weights, delays, ranges, bounds, and attempt limits for valid values.
5. Check location and bounds against the intended facet, terrain, Z range, and enclosing region.
6. Confirm the package is selected by the target era/profile; a valid file that is never imported is not implemented content.

Exact defaults and casing belong to current serializer code and representative files, not memory.

## Package families

Current data is split under folders such as:

- `Distribution/Data/Spawns/shared/<facet>/`
- `Distribution/Data/Spawns/uoml/<facet>/`
- `Distribution/Data/Spawns/post-uoml/<facet>/`

Treat folder names as implementation package labels, not proof of official expansion ownership. Trace the configured loader/import invocation to show which patterns are active and in what order. When packages overlap, document replacement identity and whether later imports intentionally supersede earlier data.

## Entry and reachability checks

- Type existence alone is insufficient: constructor/constructibility, expansion gating, map placement, and entry amount must make it spawnable.
- A creature's own home/range or AI rules do not repair an invalid spawner bound.
- `RegionSpawner` requires a region that resolves on the same map. A same-named region on another facet is not equivalent.
- `ProximitySpawner` requires negative tests outside trigger range and after reset/reload.
- Vendor, resource, dungeon, and encounter-adjacent packs may need domain-specific review in addition to schema checks.

## Focused tests

Use the current suite under `Projects/UOContent.Tests/Tests/Engines/Spawners/Json/`:

- `AllSpawnFilesLoadTests.cs`
- `SpawnerDiscoveryValidationTests.cs`
- `SpawnerDtoRoundTripTests.cs`
- `SpawnerCompactWriterTests.cs`
- `BoundsEquivalenceTests.cs`
- `ExportImportFileTests.cs`
- `ImportCleanupTests.cs`
- `LegacyHomeRangeTests.cs`
- `MigratedDataLoadTests.cs`

Also run `SectorSpawnCacheTests.cs` when placement/cache behavior changes. Add explicit profile-selection tests when a file moves between package families; parsing every JSON file does not prove runtime reachability.

## Review output

Report the files/patterns selected, DTO type per record, unresolved types/regions/maps, overlap/replacement behavior, pre-era and target-era reachability, test evidence, and any placement claims requiring a client/in-game check.
