# Spawner Import, Export, and Migration

Use this reference for staff commands, replacement semantics, legacy formats, serializer migrations, and rollback planning.

## Command surfaces

Inspect current implementations under `Projects/UOContent/Engines/Spawners/Commands/`:

- `ImportSpawnersCommand.cs`
- `ExportSpawnersCommand.cs`
- `EditSpawnerCommand.cs`
- `RespawnCommand.cs`
- `ShowSpawnerBordersCommand.cs`
- `SpawnPropsCommand.cs`

Import accepts globbed files and currently recognizes JSON plus legacy XML and Nerun-style map inputs. Legacy readers are compatibility paths; export and new reviewed data should use the current JSON DTO representation unless project instructions say otherwise.

## JSON import behavior

Current JSON import follows these safety steps:

1. Deserialize the whole file into DTOs before constructing world objects.
2. Reject missing or internal maps.
3. Construct one concrete spawner through `dto.ToSpawner()`, which deletes a partial item when DTO application throws.
4. At the target map/location, delete existing spawners of the same concrete type.
5. Move the new spawner into the world and respawn it.
6. If its GUID replaces a previously indexed spawner, delete the previous instance.
7. Delete the new spawner if placement/respawn/indexing throws.

This is failure-contained per record, not a transaction for the complete file set. Earlier records can remain applied when a later record fails. Plan rollback accordingly.

## Identity and collision rules

- Location/type replacement and GUID replacement are separate collision paths; test both together and independently.
- Reusing a GUID intentionally means replacement. Accidental GUID reuse can delete a valid spawner elsewhere.
- A new GUID at an existing location may still replace the same concrete spawner type.
- Different concrete spawner types at one location are not automatically equivalent or mutually exclusive.
- Re-import must reconcile existing children according to current delete behavior; prove no child, timer, or cache entry survives unintentionally.

Do not promise atomic import unless the implementation is changed and tested to provide it.

## Export and round-trip

For export changes, verify:

- every concrete spawner maps to the correct DTO discriminator;
- mandatory fields remain emitted even when values equal defaults;
- optional defaults round-trip without semantic drift;
- compact `homeRange` and explicit bounds remain equivalent where intended;
- region/proximity-only fields are neither dropped nor emitted on the wrong type;
- ordering/formatting changes do not hide behavioral diffs.

Use round-trip tests for semantics, not raw text equality alone.

## Serializer migrations

Spawner migrations live under:

- `Projects/UOContent/Engines/Spawners/BaseSpawner.Migrations.cs`
- `Projects/UOContent/Migrations/Server.Engines.Spawners.*.json`

When durable fields change:

1. Identify source versions and all concrete subclasses.
2. Define defaults for old saves separately from defaults for new JSON.
3. Preserve GUID, entry ownership, location/map, timing, and running state unless the migration explicitly changes them.
4. Regenerate required migration schemas/artifacts using repository tooling.
5. Test current save/load and each supported legacy path.

## Safe rollout

Before import, capture:

- exact glob expansion and file order;
- active spawner count/identity for the affected area;
- expected replacements and retained children;
- backup/export or world-save rollback boundary;
- commands and permissions used.

After import, compare generated/failure counts, inspect error logs, search for duplicate location/GUID identities, validate sector lookup, and sample spawn/cleanup behavior. Never run a broad production import as a validation experiment.
