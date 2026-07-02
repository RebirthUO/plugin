# Samurai Empire Craft Metadata Test Pattern

Use this when resolving Samurai Empire craft coverage tickets or any ModernUO/RebirthUO craft parity issue that asks for recipe `skill/resource/category/output/era gate` coverage.

## Key lesson

Do not source-grep `Def*.cs` as the assertion mechanism. Build table-driven tests through the runtime `CraftItem` objects exposed by each `CraftSystem`.

`CraftItem` exposes the fields needed for low-level recipe coverage:

- `ItemType` — output type
- `GroupNameNumber` — craft gump group/category cliloc
- `NameNumber` — item/row cliloc
- `RequiredExpansion` — era gate, e.g. `Expansion.SE`
- `Skills` — required skill rows (`SkillToMake`, `MinSkill`, `MaxSkill`)
- `Resources` — required resource rows (`ItemType`, `Amount`)
- `UseAllRes` — ammo/bulk-resource behavior such as arrows, bolts, and Fukiya Darts

## Test shape

1. Ensure the craft system is initialized under the expansion gate you need. Preserve and restore `Core.Expansion` around initialization when changing it.
2. Get the row with `CraftSystem.CraftItems.SearchFor(typeof(TargetItem))`.
3. Assert row identity and gate:
   - `Assert.NotNull(craftItem)`
   - `Assert.Equal(typeof(TargetItem), craftItem.ItemType)`
   - `Assert.Equal(expectedGroup, craftItem.GroupNameNumber)`
   - `Assert.Equal(expectedName, craftItem.NameNumber)`
   - `Assert.Equal(Expansion.SE, craftItem.RequiredExpansion)`
4. Assert every expected `CraftSkill` row, not just the main skill. This matters for mixed-skill rows like `Tessen`.
5. Assert every expected `CraftRes` row, including secondary resources such as cloth/logs/flour/ginseng.
6. Assert `UseAllRes` when the source row calls `SetUseAllRes(index, true)`, e.g. `FukiyaDarts`.

## Helpers worth extracting in tests

```csharp
private static CraftItem AssertCraftItem(CraftSystem system, Type itemType, int group, int name)
{
    var craftItem = system.CraftItems.SearchFor(itemType);
    Assert.NotNull(craftItem);
    Assert.Equal(itemType, craftItem.ItemType);
    Assert.Equal(group, craftItem.GroupNameNumber);
    Assert.Equal(name, craftItem.NameNumber);
    Assert.Equal(Expansion.SE, craftItem.RequiredExpansion);
    return craftItem;
}

private static void AssertCraftSkill(CraftItem craftItem, SkillName skill, double minSkill, double maxSkill)
{
    for (var i = 0; i < craftItem.Skills.Count; i++)
    {
        var row = craftItem.Skills[i];
        if (row.SkillToMake == skill)
        {
            Assert.Equal(minSkill, row.MinSkill);
            Assert.Equal(maxSkill, row.MaxSkill);
            return;
        }
    }

    Assert.Fail($"{craftItem.ItemType.Name} should require {skill}.");
}

private static void AssertCraftResource(CraftItem craftItem, Type resourceType, int amount)
{
    for (var i = 0; i < craftItem.Resources.Count; i++)
    {
        var row = craftItem.Resources[i];
        if (row.ItemType == resourceType)
        {
            Assert.Equal(amount, row.Amount);
            return;
        }
    }

    Assert.Fail($"{craftItem.ItemType.Name} should require {resourceType.Name}.");
}
```

## SE rows observed during issue #76-#100 discovery

Useful anchors from `Def*` craft systems:

- Tabi: `NinjaTabi` group `1015288`, name `1030210`, Tailoring `70.0-95.0`, `Cloth x10`; `SamuraiTabi` group `1015288`, name `1030209`, Tailoring `20.0-45.0`, `Cloth x6`.
- Carpentry: `Bokuto` name `1030227`, `70.0-95.0`, `Log x6`; `Fukiya` name `1030229`, `60.0-85.0`, `Log x6`; `Tetsubo` name `1030225`, `80.0-140.3`, `Log x10`.
- Bowcraft: `FukiyaDarts` group `1044565`, name `1030246`, Fletching `50.0-90.0`, `Log x1`, `UseAllRes = true`; `Yumi` group `1044566`, name `1030224`, Fletching `90.0-130.0`, `Log x10`.
- Tinkering: `Nunchaku` group `1044042`, name `1030158`, Tinkering `70.0-120.0`, `IronIngot x3`, plus `Log x8`.
- Ninja tools: `SmokeBomb` Alchemy `90.0-120.0`, `Eggs x1`, plus `Ginseng x3`; `EggBomb` Cooking `90.0-120.0`, `Eggs x1`, plus `SackFlour x3`.
- Blacksmith Samurai armor: `PlateMempo` group `1011078`, name `1030180`, Blacksmith `80.0-130.0`, `IronIngot x18`; `PlateDo` group `1011078`, name `1030184`, `87.0-137.0`, `IronIngot x28`; `PlateHiroSode` group `1011078`, name `1030187`, `80.0-130.0`, `IronIngot x16`; `PlateSuneate` group `1011078`, name `1030195`, `65.0-115.0`, `IronIngot x20`; `PlateHaidate` group `1011078`, name `1030200`, `65.0-115.0`, `IronIngot x20`.
- Blacksmith Samurai helmets: `ChainHatsuburi` group `1011079`, name `1030175`, Blacksmith `30.0-80.0`, `IronIngot x20`; `PlateHatsuburi` name `1030176`, `45.0-95.0`, `IronIngot x20`; `HeavyPlateJingasa` name `1030178`, `45.0-95.0`, `IronIngot x20`; `LightPlateJingasa` name `1030188`, `45.0-95.0`, `IronIngot x20`; `SmallPlateJingasa` name `1030191`, `45.0-95.0`, `IronIngot x20`; `DecorativePlateKabuto` name `1030179`, `90.0-140.0`, `IronIngot x25`; `PlateBattleKabuto` name `1030192`, `90.0-140.0`, `IronIngot x25`; `StandardPlateKabuto` name `1030196`, `90.0-140.0`, `IronIngot x25`.
- Blacksmith SE weapons/tools: `NoDachi` group `1011081`, name `1030221`, Blacksmith `75.0-125.0`, `IronIngot x18`; `Wakizashi` name `1030223`, `50.0-100.0`, `IronIngot x8`; `Lajatang` name `1030226`, `80.0-130.0`, `IronIngot x25`; `Daisho` name `1030228`, `60.0-110.0`, `IronIngot x15`; `Tekagi` name `1030230`, `55.0-105.0`, `IronIngot x12`; `Shuriken` name `1030231`, `45.0-95.0`, `IronIngot x5`; `Kama` name `1030232`, `40.0-90.0`, `IronIngot x14`; `Sai` name `1030234`, `50.0-100.0`, `IronIngot x12`; `Tessen` group `1011084`, name `1030222`, Blacksmith `85.0-135.0`, Tailoring `50.0-55.0`, `IronIngot x16`, `Cloth x10`.

Verify exact line values against the active branch before committing; the table above is a discovery aid, not a substitute for reading the target source.

## Test isolation pitfall: static CraftSystem, Core.Expansion, and Recipe.Recipes

Craft systems are process-global (`DefTailoring.CraftSystem`, `DefBlacksmithy.CraftSystem`, etc.) and many UOContent tests share the same process. Do not write a focused craft metadata test that temporarily sets `Core.Expansion = Expansion.SE`, calls `Def*.Initialize()`, and then restores only `Core.Expansion`: that leaves the static `CraftSystem` rebuilt for the SE-only recipe set and can create order-dependent failures in ML/EJ craft tests that only initialize when `CraftSystem == null`.

Recipe-bearing systems add a second global-state hazard: `Recipe.Recipes` is a single static registry and `Recipe` throws `Attempting to create recipe with preexisting ID` on duplicate IDs. Reinitializing `DefBlacksmithy`, `DefCarpentry`, `DefTinkering`, etc. under ML/EJ in a test `finally` can collide with IDs already registered by earlier initializations. If a test truly needs expansion-scoped craft reinitialization, snapshot/restore `Core.Expansion`, the affected `Def*.CraftSystem` static, `Recipe.Recipes`, and `Recipe.LargestRecipeID` (or use an explicit test-only reset helper) instead of just calling `Def*.Initialize()` again.

Preferred pattern for SE row metadata tickets:

- If the normal test fixture/default expansion is EJ/current and therefore includes SE rows, do **not** force `Core.Expansion = Expansion.SE`; initialize the craft system only when it is null, then assert each row's `RequiredExpansion == Expansion.SE`.
- Be careful with expected craft-gump categories that are era-conditional in production source. For example, `DefCarpentry` uses `Core.ML ? 1044566 : 1044295` for Bokuto/Fukiya/Tetsubo, so an EJ/default-fixture test should expect `1044566` unless it deliberately snapshots and rebuilds the craft system under SE-only.
- If a test truly must rebuild a craft system under a lower expansion, restore both `Core.Expansion` and the affected static craft system state. Be careful: blindly reinitializing a recipe-bearing system under ML/EJ can throw `Attempting to create recipe with preexisting ID` unless the recipe registry is also safely restored/reset.
- Add a wider regression slice when fixing static-state concerns, e.g. the focused test plus adjacent craft gump/recipe tests, not only the new test class.

Example safe shape when EJ/current is already active:

```csharp
if (DefTailoring.CraftSystem == null)
{
    DefTailoring.Initialize();
}

var craftItem = DefTailoring.CraftSystem.CraftItems.SearchFor(typeof(NinjaTabi));
Assert.NotNull(craftItem);
Assert.Equal(Expansion.SE, craftItem.RequiredExpansion);
```

## Batch PR wave lessons

When several SE craft tickets share one test file (for example `TokunoCraftRecipeFieldTests.cs`), still keep the GitHub work isolated per issue/PR unless the user explicitly asks to combine. Use one worktree per issue, make only the rows needed for that issue, and run the same validation loop in that worktree before pushing:

```text
git diff --check
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --filter "FullyQualifiedName~TokunoCraftRecipeFieldTests" --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
```

For successful craft-metadata-only PRs, the PR body should explicitly say there is no gameplay behavior change and list the exact runtime metadata asserted: output type, group/name clilocs, expansion gate, skills, resources, and `UseAllRes` where applicable.
