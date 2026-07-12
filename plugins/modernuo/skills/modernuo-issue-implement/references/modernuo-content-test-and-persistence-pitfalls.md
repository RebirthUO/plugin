# ModernUO Content-Test and Persistence Pitfalls

Reusable lessons from Mysticism/content implementation work.

## Source-generated persistent items

When adding an item with `[SerializationGenerator]`, run the schema generator before the final build/test:

```bash
dotnet tool restore && dotnet tool run ModernUOSchemaGenerator -- ModernUO.slnx
```

Verify that the owning project's `Migrations/` directory contains the expected type/version schema. Include the generated migration in the issue-scoped changeset.

## UOContent test bootstrap

A project-only build can leave distribution data absent from the test output. If a UOContent fixture fails during bootstrap in `AOS`/`SkillsInfo` or reports missing data, build the solution first, then rerun the test project:

```bash
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
MODERNUO_TEST_DATA_DIR='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic' \
  dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj ...
```

Treat this as test-output preparation, not as a product failure; report the actual owning-test result separately.

## Mutating item containers while enumerating

`FindItemsByType<T>()`/ordinary container enumeration is mutation-sensitive. Deleting or moving matched items during iteration can throw:

> Item was modified after enumerator was instantiated. Use Item.EnumerateItems method instead for safe enumerations.

Use the owning container's safe queue and dispose it:

```csharp
using (var items = backpack.EnumerateItemsByType<SpellStone>())
{
    foreach (var item in items)
    {
        item.Delete();
    }
}
```

## Final validation discipline

After every final code or test edit, rebuild the solution and rerun the focused filter. Then rerun the broad owning project when feasible. A previously green run does not validate the current worktree if the last edit happened afterward. Do not commit, push, or report completion while the post-edit focused run is stale or failing.

## Client localization

Do not invent cliloc IDs for new messages. Prefer a verified cliloc from the cited source/repository; otherwise use the project's established plain-message convention until localization evidence is available.
