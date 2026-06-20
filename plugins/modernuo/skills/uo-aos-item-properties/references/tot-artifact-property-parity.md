# Treasures of Tokuno Artifact Property Parity

Session-derived reference for future RebirthUO/ModernUO work on Samurai Empire / Treasures of Tokuno artifact properties.

## Trigger

Use this when auditing or fixing named artifact items whose AoS properties, skill bonuses, resistances, damage types, or base weapon stats need to match an external source table such as UO.com.

## Source order

For this project's UO domain work, use:

1. UO.com
2. UOGuide
3. Stratics

Cite the source directly in tests or docs near the claim when practical.

Primary ToT page used in this slice:

- `https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-treasure-of-tokuno/`

## Pattern that worked

1. Add table-driven tests before changing artifacts.
2. Split tests by property family:
   - base weapon stats: min/max damage, speed, str requirement, skill, damage-type split
   - magical weapon props: `Attributes`, `WeaponAttributes`, slayers, skill bonuses
   - wearables/spellbooks: resists, `Attributes`, `ArmorAttributes`, `ClothingAttributes`, `SkillBonuses`
3. Instantiate concrete artifact classes directly and assert the public item API, not private fields.
4. Dispose/delete items in `finally` blocks to avoid test pollution.
5. Run the focused test first, then the broader Samurai/Tokuno filter.

Example focused command from RebirthUO/service:

```bash
export MODERNUO_TEST_DATA_DIR='C:\Users\Jsiem\Documents\GitHub\RebirthUO\connector\client'
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --filter 'FullyQualifiedName~TreasuresOfTokunoArtifactPropertyTests'
```

Broader focused filter that passed in the session:

```bash
export MODERNUO_TEST_DATA_DIR='C:\Users\Jsiem\Documents\GitHub\RebirthUO\connector\client'
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --filter 'FullyQualifiedName~TreasuresOfTokuno|FullyQualifiedName~SamuraiEmpire|FullyQualifiedName~Tokuno'
```

## Important pitfall

Named artifacts can inherit incorrect base weapon stats from the normal weapon class. Do not assume the base weapon class (`Sai`, `Nunchaku`, `Yumi`, `NoDachi`, etc.) already matches the artifact row.

For ToT artifacts, the fix was artifact-level overrides such as:

- `public override int AosMinDamage => ...;`
- `public override int AosMaxDamage => ...;`
- `public override float MlSpeed => ...;` for Yumi-based artifacts whose artifact speed differs from the inherited base.

This caught mismatches for Demon Forks, Dragon Nunchaku, Exiler, Hanzo's Bow, Peasant's Bokuto, Pilfered Dancer Fans, The Destroyer, Darkened Sky, Sword of the Stampede, Swords of Prosperity, The Horselord, and Wind's Edge.

## Assertion helpers

Useful helper pattern:

```csharp
private static void AssertSkillBonus(AosSkillBonuses bonuses, int index, SkillName expectedSkill, double expectedValue)
{
    Assert.True(bonuses.GetValues(index, out var skill, out var value));
    Assert.Equal(expectedSkill, skill);
    Assert.Equal(expectedValue, value);
}
```

For concrete items, prefer helpers that delete in `finally`:

```csharp
private static void AssertWeaponProperties(BaseWeapon weapon, Action<BaseWeapon> assertions)
{
    try
    {
        assertions(weapon);
    }
    finally
    {
        weapon.Delete();
    }
}
```

## What not to persist as a rule

Do not encode `tiledata.mul` absence as a durable failure. The durable lesson is the setup fix: export `MODERNUO_TEST_DATA_DIR` to the local client data directory before running UOContent tests that load TileData.
