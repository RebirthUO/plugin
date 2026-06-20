---
name: "uo-aos-item-properties"
description: "Use when working with the Age of Shadows (AoS) item property system in ModernUO/RebirthUO servers - AosAttribute, AosWeaponAttribute, AosArmorAttribute, AosSkillBonuses, AosElementAttributes, the BaseAttributes storage pattern, and the GetProperties OPL rows for magical items. Use when adding a new property, debugging a property that does not show in tooltip, wiring a property into combat/spell/resist formulas, or extending the property system per Stygian Abyss (SA) parity."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO AOS Item Properties

## Overview

The AoS item property system is the in-game answer to "this weapon has +30 spell damage and 20% fire area effect". The whole machinery lives in two files: the `BaseAttributes` storage class in `Projects/UOContent/Misc/AOS.cs` and the static `AOS` helper for damage, resistance, and status queries. Every property the client shows in the tooltip is a bitmasked value stored in a sparse `int[]` and surfaced through typed enums.

This skill covers the five property containers, the `BaseAttributes` bit storage model, the static `GetValue(Mobile, attribute)` aggregation that combat/spell/AI use, and the OPL rows that every typed `GetProperties` must add. It is the bridge between the raw `Item` entity (covered in `uo-items-foundation`) and the gameplay formulas (covered in `AOS.Damage`).

The reference implementation is `Projects/UOContent/Misc/AOS.cs` (1607 lines). The plan that defines the remaining UOGuide item properties is `docs/superpowers/plans/2026-06-02-item-properties-completion.md`.

## When to Use

- Adding a new `AosAttribute`, `AosWeaponAttribute`, or `AosArmorAttribute` value.
- Wiring a property into combat (e.g. `HitCurse`, `HitManaDrain`).
- Adding SA-era defensive/caster properties not in the original AoS set.
- Fixing a property that does not appear in the tooltip (OPL row missing).
- Building an item generation routine that rolls properties from a `BaseAttributes`.
- Tracing why a property applies to a player when equipped, but not to their summoned pet.

Don't use for:

- The base Item entity (use `uo-items-foundation`).
- Crafting/recipe plumbing (use `uo-crafting-recipes-resources`).
- Pre-AoS pre-magical items (the system is gated by `Core.AOS`).

## The Five Property Containers

All five live in `Projects/UOContent/Misc/AOS.cs` and inherit from `BaseAttributes`. Each is a typed wrapper over a sparse int array of stored values, addressed by an enum bitmask.

| Container | Backing enum | Used by | Reference |
|---|---|---|---|
| `AosAttributes` | `AosAttribute` | Weapons, armor, clothing, jewelry, spellbooks, all magical items | `AOS.cs:284-310` (enum), `AOS.cs:327-655` (class) |
| `AosWeaponAttributes` | `AosWeaponAttribute` | Weapons only | `AOS.cs:658-685` (enum), `AOS.cs:688-927` (class) |
| `AosArmorAttributes` | `AosArmorAttribute` | Armor, shields, clothing | `AOS.cs:928-935` (enum), `AOS.cs:937-1028` (class) |
| `AosSkillBonuses` | (SkillName/value pairs, slot-indexed) | Armor, jewelry | `AOS.cs:1030-1311` (class) |
| `AosElementAttributes` | `AosElementAttribute` | Weapons (damage type splits) | `AOS.cs:1313-1391` (class) |

Interfaces used to dispatch generic access:

- `IAosItem` exposes `AosAttributes Attributes { get; }` (`AOS.cs:312-315`).
- `IAosWeaponAttributesItem` exposes `AosWeaponAttributes WeaponAttributes { get; }` (`AOS.cs:317-320`).
- `IAosArmorAttributesItem` exposes `AosArmorAttributes ArmorAttributes { get; }` (`AOS.cs:322-325`).

`BaseWeapon`, `BaseArmor`, `BaseClothing`, and `BaseJewel` all implement one or more of these interfaces. The static `GetValue` aggregator in each container walks `m.Items` (the equipped layers) and sums the bitmask value across all matching items, which is the model used by combat and spell formulas.

## BaseAttributes Storage Model

`BaseAttributes` is declared at `AOS.cs:1393-...`:

```csharp
[PropertyObject]
[SerializationGenerator(0)]
public abstract partial class BaseAttributes
{
    [SerializableField(0, setter: "private")]
    private uint _names;

    [EncodedInt]
    [SerializableField(1, setter: "private")]
    private int[] _values;
    ...
}
```

Two fields implement the storage:

- `_names` is a `uint` bitmask of which properties are set. Each enum value is a single bit.
- `_values` is a sparse `int[]` holding values in the order of the bits that are set, addressed by `GetIndex(bitmask)`.

This is a compact representation: items with no properties take a few bytes; items with many properties grow `_values` but never re-hash or re-index on read. `IsEmpty => _names == 0` is the cheap "no properties" check.

`GetValue(int bitmask)` (`AOS.cs:1425-1447`) returns 0 when `!Core.AOS` - the entire system is gated by the era flag. This means setting a property on a pre-AoS server is a no-op and `GetProperties` rows can short-circuit to `0`.

`SetValue(int bitmask, int value)` (`AOS.cs:1449-...`) is more complex: it triggers a side effect for `AosArmorAttribute.DurabilityBonus` and `AosWeaponAttribute.DurabilityBonus` by calling `UnscaleDurability()` on the owner. Any new property with a `SetValue` side effect must follow this pattern, because the durability hook is part of the contract that `BaseArmor`/`BaseWeapon` rely on.

The `(Item owner, BaseAttributes other)` copy constructor (`AOS.cs:1410-1416`) duplicates the storage; it is the path used by clone/copy generation routines and by gem-of-sacrifice-style item rebuilds.

## Adding a New Property

The implementation plan in `docs/superpowers/plans/2026-06-02-item-properties-completion.md` defines the canonical pattern. It is a five-step process:

1. **Extend the bit enum.** Add a new value to `AosAttribute`, `AosWeaponAttribute`, or `AosArmorAttribute`. Use the next free high bit. Example for weapon attributes (`docs/superpowers/plans/2026-06-02-item-properties-completion.md:428-431`):

   ```csharp
   HitCurse = 0x02000000,
   HitFatigue = 0x04000000,
   HitManaDrain = 0x08000000
   ```

2. **Add a typed property wrapper** in the matching container (`AosAttributes`, `AosWeaponAttributes`, `AosArmorAttributes`):

   ```csharp
   [CommandProperty(AccessLevel.GameMaster)]
   public int HitCurse
   {
       get => this[AosWeaponAttribute.HitCurse];
       set => this[AosWeaponAttribute.HitCurse] = value;
   }
   ```

   This is the user-facing API and the `[CommandProperty]` path for `i.props`.

3. **Wire `GetProperties(IPropertyList list)` in the relevant base class.** Append a row with a cliloc or with the `ItemPropertyDisplay` helper. For percentage-based hit effects, `ItemPropertyDisplay.AddPercent` is the right helper (`docs/superpowers/plans/2026-06-02-item-properties-completion.md:451-465`).

4. **Add a static aggregation in the container** (`GetValue(Mobile m, AosAttribute attribute)` etc.) so that combat and spell formulas can read the value from the equipped item set. The aggregation walks `m.Items` and sums across all matching items.

5. **Implement the gameplay effect.** For weapon hit effects, the `BaseWeapon` hit pipeline calls `CheckHitEffect(attacker, defender, attribute, bonus)` and dispatches. New effect bodies are simple mutations: `CurseSpell.DoCurse`, `defender.Stam = Math.Max(0, defender.Stam - Utility.RandomMinMax(10, 20))`, etc. (`docs/superpowers/plans/2026-06-02-item-properties-completion.md:481-497`).

The plan's task list at `docs/superpowers/plans/2026-06-02-item-properties-completion.md:14-26` orders the work: shared test infrastructure first, then low-risk partial properties, then missing classic hit effects, then negative property storage, then engine transfer flags, then SA-specific weapon and defensive properties, then loot/runic/artifact wiring.

## Existing AoS Attribute Reference

`AosAttribute` (`AOS.cs:284-310`) is the cross-type container. Each value is a 21-bit bit slot, giving 24 attributes today with headroom up to 31.

| Value | Bit | Effect (where applied) |
|---|---:|---|
| `RegenHits` | `0x00000001` | Hits regen per tick |
| `RegenStam` | `0x00000002` | Stamina regen per tick |
| `RegenMana` | `0x00000004` | Mana regen per tick |
| `DefendChance` | `0x00000008` | Increase Defense Chance |
| `AttackChance` | `0x00000010` | Increase Hit Chance |
| `BonusStr` | `0x00000020` | +Str while equipped (see `AosAttributes.AddStatBonuses` at `AOS.cs:618-644`) |
| `BonusDex` | `0x00000040` | +Dex while equipped |
| `BonusInt` | `0x00000080` | +Int while equipped |
| `BonusHits` | `0x00000100` | +Max Hits |
| `BonusStam` | `0x00000200` | +Max Stamina |
| `BonusMana` | `0x00000400` | +Max Mana |
| `WeaponDamage` | `0x00000800` | % increase to weapon damage |
| `WeaponSpeed` | `0x00001000` | % swing speed |
| `SpellDamage` | `0x00002000` | % increase to spell damage |
| `CastRecovery` | `0x00004000` | Faster cast recovery |
| `CastSpeed` | `0x00008000` | Faster casting |
| `LowerManaCost` | `0x00010000` | LMC% |
| `LowerRegCost` | `0x00020000` | LRC% |
| `ReflectPhysical` | `0x00040000` | Reflect physical damage (used in `AOS.Damage` at `AOS.cs:204-232`) |
| `EnhancePotions` | `0x00080000` | Boost potion effect (e.g. `InvisibilityPotion` duration) |
| `Luck` | `0x00100000` | Luck modifier (negative triggers `Unlucky` OPL row) |
| `SpellChanneling` | `0x00200000` | Cast spells without un-equipping |
| `NightSight` | `0x00400000` | Permanent night sight |
| `IncreasedKarmaLoss` | `0x00800000` | Higher karma loss on kills |

The static `GetValue(Mobile m, AosAttribute attribute)` aggregator (`AOS.cs:570-614`) walks the equipped items and sums the values for that attribute across all matching types (weapons, armor, clothing, `IAosItem`).

## Existing Weapon Attribute Reference

`AosWeaponAttribute` (`AOS.cs:658-685`) holds weapon-only effects. Each value is a 26-bit bit slot. Existing values are LowerStatReq, SelfRepair, the three HitLeech family, HitLowerAttack/Defend, the hit spells (Magic Arrow, Harm, Fireball, Lightning, Dispel), the area hit effects (Cold/Fire/Poison/Energy/Physical Area), the five resist bonuses, UseBestSkill, MageWeapon, and DurabilityBonus.

The plan in `docs/superpowers/plans/2026-06-02-item-properties-completion.md` adds `HitCurse`, `HitFatigue`, `HitManaDrain` at the next free high bits (`0x02000000`, `0x04000000`, `0x08000000`).

## Existing Armor Attribute Reference

`AosArmorAttribute` (`AOS.cs:928-935`) is intentionally small: LowerStatReq, SelfRepair, MageArmor, DurabilityBonus. SA-era additions (Soul Charge, Reactive Paralyze, etc.) are tracked as future work in the item-properties plan.

## Skill Bonuses

`AosSkillBonuses` (`AOS.cs:1030-...`) is a five-slot modifier system used by armor and jewelry. Each slot holds a `SkillName` and a `double` bonus. The class exposes `Skill_1_Name`/`Skill_1_Value` through `Skill_5_Name`/`Skill_5_Value` for `[CommandProperty]` access. `AddTo(Mobile m)` and `Remove()` install/uninstall the `SkillMod` objects; the storage uses `1 << index` bitmasks (slot 0 = bit 1, slot 1 = bit 2, etc.) so the standard `GetValue/SetValue` pattern still works.

`GetProperties(IPropertyList list)` (`AOS.cs:1112-1121`) emits cliloc 1060451+i for each set slot, formatted with the localized skill label and bonus.

## Element Attributes

`AosElementAttributes` (`AOS.cs:1325-1391`) is the damage-type split for weapons. The seven values are Physical, Fire, Cold, Poison, Energy, Chaos, Direct. The `AosElementAttribute` enum (`AOS.cs:1313-1323`) covers each. `AOS.Damage(m, from, damage, phys, fire, cold, pois, nrgy, chaos, direct, keepAlive, archer, deathStrike)` uses these as percentages of base damage.

## AOS.Damage and Property Aggregation

`AOS.Damage` is the core damage pipeline (`AOS.cs:37-246`). The signature is intentionally wide to cover every variant. The pre-AoS path calls `m.Damage(damage, from)` and returns. The AoS path:

1. Calls `Fix(ref phys)`, `Fix(ref fire)`, etc. to clamp negative values to 0.
2. For ML and `chaos > 0`, randomly distributes the chaos portion across the five elemental types (`AOS.cs:76-106`).
3. For each element, computes `damage * element% * (100 - res%)` against `m.PhysicalResistance` / `m.FireResistance` / etc. (`AOS.cs:120-130`).
4. For ML, adds `damage * direct / 100` and the quiver's damage increase (`AOS.cs:134-142`).
5. Reads `AosAttributes.GetValue(m, AosAttribute.ReflectPhysical)` and adds reflected damage back to the attacker (`AOS.cs:204-232`).

`AOS.GetStatus(from, index)` (`AOS.cs:258-280`) returns a 15-slot status window the client uses for the AOS-equipped attributes view; the data here is used by the MobileStatus packet and the AOS-equipped-overlay.

## Common Recipes

### Auditing Named Artifact Property Parity

When a named artifact must match an external item table, test the concrete artifact class directly before editing it. Cover both normal item stats and AoS containers: base weapon damage/speed/skill/damage split, `Attributes`, `WeaponAttributes`, `ArmorAttributes`, `ClothingAttributes`, `SkillBonuses`, slayers, and resist overrides. Do not assume the base item class already matches the artifact row; named artifacts may need artifact-level `AosMinDamage`, `AosMaxDamage`, or `MlSpeed` overrides when the source row differs from the inherited normal weapon.

See `references/tot-artifact-property-parity.md` for the Treasures of Tokuno table-driven test pattern, RebirthUO test commands, and pitfalls discovered while fixing ToT artifact stats.

### Generating a Magical Item with Property Rolls

```csharp
var weapon = new Katana();
weapon.Attributes.WeaponDamage = 45;
weapon.Attributes.AttackChance = 15;
weapon.WeaponAttributes.HitFireball = 50;
weapon.WeaponAttributes.HitLeechHits = 25;
weapon.Slayer = SlayerName.Silver; // optional
```

This is the standard pattern: a generation routine constructs the item, then mutates the typed `Attributes`/`WeaponAttributes`/`ArmorAttributes` properties directly. `BaseAttributes.SetValue` fires durability unscaling if needed and updates `_names`/`_values` in one call.

### Reading the Effective Value on a Mobile

```csharp
var total = AosAttributes.GetValue(mobile, AosAttribute.SpellDamage);
// or weapon/armor specific
var weaponLeech = AosWeaponAttributes.GetValue(mobile, AosWeaponAttribute.HitLeechHits);
```

Combat and spell code in `BaseWeapon.OnHit`, `AOS.Damage`, and `Spell` damage paths all use this pattern. Adding a new attribute without a `GetValue` aggregation means combat code can never read the value.

### Wiring a Custom Property into OPL

For properties with a cliloc:

```csharp
if ((prop = WeaponAttributes.HitFireball) != 0)
{
    list.Add(1060422 + offset, $"{prop}"); // appropriate cliloc, arguments go through {}
}
```

For properties without a cliloc (the new partial-property set), use the `ItemPropertyDisplay` helper:

```csharp
if (Attributes.Luck < 0)
{
    ItemPropertyDisplay.AddName(list, "Unlucky");
}
```

Remember `CLAUDE.md:14`: PropertyList string literals must be holes. Use `$"{}"` form inside the cliloc arg, never bare concatenation.

### Adding a Hit-Effect Property

The `BaseWeapon` hit pipeline routes through `CheckHitEffect`. To wire a new effect:

```csharp
if (CheckHitEffect(attacker, defender, AosWeaponAttribute.HitCurse, propertyBonus))
{
    CurseSpell.DoCurse(attacker, defender);
}
```

The `CheckHitEffect` helper takes the property value as a percentage chance and applies the per-property-bonus scalar used by `CheckHitEffect` and the various other hit effects. New effects need to be added next to the existing block in `BaseWeapon.OnHit` to keep the order stable.

## Pitfalls

1. **Forgetting the `Core.AOS` gate.** `BaseAttributes.GetValue` returns 0 when `!Core.AOS`, so reading a property value on a pre-AoS server is safe. But writing code that *computes* OPL rows without checking the era can leak property text into pre-AoS tooltips. Guard the OPL side with `if (!Core.AOS) return;` or skip the relevant `if` blocks in `GetProperties`.
2. **Setting `_values` directly.** Never poke into `_values` from outside `BaseAttributes`. Always go through `SetValue(int bitmask, int value)`. The setter is the only place that triggers the durability `UnscaleDurability` side effect and updates `_names`.
3. **Adding a new bit value to a `[Flags]` enum without picking the next high bit.** The bit allocation is dense and intentional. If a contributor adds a low bit, they collide with an existing value. New bits go at the top of the enum (next high bit) and the change is recorded in the plan.
4. **Forgetting `ReflectPhysical` consumption in combat.** `AOS.Damage` reads `ReflectPhysical` once and applies it before `m.Damage`. New reflect-style effects (e.g. SA `Blood Oath`-style reflect) need a parallel code path in `AOS.Damage` or a `BaseCreature` hook.
5. **Adding a new SA attribute without considering pre-SA shards.** SA attributes that affect formulas need an `if (Core.SA)` or `if (Core.ML)` gate in the consumer. Stygian Abyss introduced several property types that should not affect pre-SA combat.
6. **Overlapping property definitions.** If two different properties can apply to the same slot (e.g. `LowerStatReq` on both `AosAttributes` and `AosArmorAttributes`), the static `GetValue` aggregator must dispatch through the right interface. `AosArmorAttributes.GetValue` and `AosAttributes.GetValue` both exist and must be called from the right code path.
7. **Wrong OPL row order.** The client expects properties in a documented order: name, hue, amount, weight, equipped layer, resists, then `AosAttributes` (alphabetical by cliloc), then `AosWeaponAttributes`/`AosArmorAttributes`, then `AosSkillBonuses`, then `AosElementAttributes`. Moving properties around confuses tooling and breaks player muscle memory.
8. **Skipping `InvalidateProperties` after a mutation.** `SetValue` does not auto-invalidate the OPL for items in-world. After programmatic property changes, call `weapon.InvalidateProperties()` to re-render the tooltip.
9. **Assuming `SkillBonuses.GetProperties` covers negative bonuses.** It only emits `GetValues` slots that pass the truthiness check. Negative skill bonuses still show in tooltip, but a future fix may hide them. Always verify with `CapturingPropertyList` (`docs/superpowers/plans/2026-06-02-item-properties-completion.md:78-147`).

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New bit value uses the next free high bit of the enum.
- [ ] `[CommandProperty(AccessLevel.GameMaster)]` wrapper is added to the container.
- [ ] `BaseWeapon`/`BaseArmor`/`BaseClothing`/`BaseJewel` `GetProperties` emits a new OPL row for the property.
- [ ] Static `GetValue(Mobile, attribute)` aggregation includes the new property on the right `if` branch (weapon/armor/clothing/IAosItem).
- [ ] `CapturingPropertyList` test covers the OPL output for at least one new property and one non-AoS era control.
- [ ] No `_values` direct access from outside `BaseAttributes`.
- [ ] `InvalidateProperties()` is called after programmatic mutations in any test or generation routine.
- [ ] `OnAfterDelete` does not need updating for new attributes (storage is owned by `BaseAttributes`), but verify `DurabilityBonus` still works for armor/weapon via the `SetValue` hook.
- [ ] For new hit effects, the combat effect body is gated by `Core.AOS` (or stricter era) at the dispatch site, not just inside the aggregator.

## Related Skills

- `uo-items-foundation` - the base classes (`BaseWeapon`, `BaseArmor`, ...) that own these property containers; also hosts the cross-cutting reading recipe at `uo-items-foundation/references/analyzing-modernuo-subsystems.md` (use it before analyzing other UO subsystems).
- `uo-crafting-recipes-resources` - generation routines that produce these magical items.
- `modernuo-property-lists` - OPL mechanics and cliloc lookup.
- `modernuo-era-expansion` - `Core.AOS`/`Core.SE`/`Core.ML`/`Core.SA` gating for properties.
- `docs/superpowers/plans/2026-06-02-item-properties-completion.md` - the open work tracker for property parity.
