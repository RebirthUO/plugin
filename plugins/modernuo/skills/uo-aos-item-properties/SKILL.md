---
name: uo-aos-item-properties
description: Use when working with the Age of Shadows (AoS) item property system in ModernUO/RebirthUO servers - AosAttribute, AosWeaponAttribute, AosArmorAttribute, AosSkillBonuses, AosElementAttributes, the BaseAttributes storage pattern, and the GetProperties OPL rows for magical items. Use when adding a new property, debugging a property that does not show in tooltip, wiring a property into combat/spell/resist formulas, or extending the property system per Stygian Abyss (SA) parity.
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
    - aos
    - item-properties
    - parity
    related_skills:
    - uoguide-item-properties
    - modernuo-item-property-parity-check
    - uo-items-foundation
    - uo-combat-pipeline
    - uo-loot-generation-artifacts
version: 1.0.0
author: Crome696
---
# UO AOS Item Properties

## Overview

The AoS item property system is the in-game answer to "this weapon has +30 spell damage and 20% fire area effect". The whole machinery lives in two files: the `BaseAttributes` storage class in `Projects/UOContent/Misc/AOS.cs` and the static `AOS` helper for damage, resistance, and status queries. Every property the client shows in the tooltip is a bitmasked value stored in a sparse `int[]` and surfaced through typed enums.

This skill covers the five property containers, the `BaseAttributes` bit storage model, the static `GetValue(Mobile, attribute)` aggregation that combat/spell/AI use, and the OPL rows that every typed `GetProperties` must add. It is the bridge between the raw `Item` entity (covered in `uo-items-foundation`) and the gameplay formulas (covered in `AOS.Damage`).

The reference implementation is `Projects/UOContent/Misc/AOS.cs`. For Stygian Abyss property introduction, read `references/sa-item-properties-introduction.md` before editing: it records the source hierarchy, RebirthUO anchors, recommended implementation slices, and pitfalls discovered while reviewing SA properties. For negative item properties such as `Antique`, read `references/antique-item-property-review.md`: it captures UO.com wording, ServUO anchors, RebirthUO durability/Powder-of-Fortifying anchors, implementation shape, and economy-side-effect boundaries. For the first SA weapon-hit slice (`HitCurse`, `HitFatigue`, `HitManaDrain`) read `references/sa-weapon-attributes-implementation-notes.md`: it captures the separate `SaWeaponAttributes` container pattern, BaseWeapon migration checklist, effect semantics, and test strategy. That first slice is now present in RebirthUO `live`; when deciding what to implement next, read `references/sa-defensive-properties-next-slices.md` for the recommended follow-up order (`Reactive Paralyze`, then `Soul Charge`, then `Casting Focus`, with Damage Eater/Resonance deferred). For dynamic tooltip-only item properties such as `Last Parry Chance`, read `references/last-parry-chance-runtime-tooltip.md` before adding storage: some official magic-property table rows are runtime display state, not rollable AoS/SA attribute bits. For Publish 96 weapon properties, especially `Sparks`, read `references/sparks-publish96-review.md` before planning storage, tooltip, or gameplay: Sparks is post-ToL/Publish 96 Doom content, not an SA attribute; prefer a modern/extended weapon-property container and keep loot/runic/imbuing distribution as a separate decision. For `Swarm`, read `references/swarm-publish96-review.md`: it captures UO.com/Publish-96 evidence, the practical `Core.TOL` gate, extended weapon storage, cliloc `1157325`, normal-hit-only trigger, physical `AOS.Damage` DoT, fire/torch counterplay, distribution guard, and Hermes post-edit verification script pattern. For `Bone Breaker`, read `references/bone-breaker-publish96-review.md`: it captures UO.com Publish 96 evidence, the practical `Core.TOL` gate, ServUO comparison values (+50 physical damage, 4s stamina drain, 60s immunity), refresh-potion blocking, and test expectations. For `Massive`, read `references/massive-publish86-review.md`: it captures UO.com/UOGuide Publish-86 evidence, the RebirthUO `Core.HS` gate decision, AoS weapon/armor storage, effective Strength Requirement 125 behavior, retained Lower Requirements tooltip policy, and focused tests for weapon/armor/shield equip + tooltip + auto-drop. For Mana Phase / Mana Phasing Orb tickets, read `references/mana-phase-talisman-implementation-notes.md`: it records UO.com, UOGuide, ServUO, and RebirthUO anchors, plus the required parity decision about whether damage caused or damage taken clears the effect.

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

Current repository dispatch notes:

- `IAosItem` exposes `AosAttributes Attributes { get; }` (`AOS.cs:307-310`) and is implemented by many host item types, but the effective-value aggregators do **not** dispatch polymorphically through `IAosItem`.
- There are no current `IAosWeaponAttributesItem` or `IAosArmorAttributesItem` interfaces in `Projects/`.
- `AosAttributes.GetValue(Mobile, AosAttribute)` explicitly scans equipped `BaseWeapon`, `BaseArmor`, `BaseJewel`, `BaseClothing`, `Spellbook`, `BaseQuiver`, and `BaseTalisman`; for `Luck`, it also adds weapon/armor resource luck bonuses (`AOS.cs:496-585`).
- `AosWeaponAttributes.GetValue(Mobile, AosWeaponAttribute)` scans equipped `BaseWeapon` plus the special `ElvenGlasses._weaponAttributes` case (`AOS.cs:851-886`).
- `AosArmorAttributes.GetValue(Mobile, AosArmorAttribute)` scans equipped `BaseArmor` and `BaseClothing` (`AOS.cs:944-979`); local armor/clothing code reads most armor attributes directly instead.

The static `GetValue` aggregator in each container walks `m.Items` (the equipped layers) and sums the bitmask value across the hard-coded matching item types. Learning: adding a new host item with `IAosItem` and a tooltip is not enough; if combat/spells/status must see its properties, update the relevant static aggregator and add a test.

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

When adding a property, use the local source shape plus `references/sa-item-properties-introduction.md` for SA-era scope. Treat storage, tooltip, gameplay effect, and generation as separate work items:

1. **Extend the bit enum.** Add a new value to `AosAttribute`, `AosWeaponAttribute`, or `AosArmorAttribute`. Use the next safe free high bit in the existing storage model. Be especially careful with `0x80000000` because `BaseAttributes` stores a `uint` mask but many callers cast enum values through `int`.

2. **Add a typed property wrapper** in the matching container (`AosAttributes`, `AosWeaponAttributes`, `AosArmorAttributes`):

   ```csharp
   [CommandProperty(AccessLevel.GameMaster)]
   public int HitCurse
   {
       get => this[AosWeaponAttribute.HitCurse];
       set => this[AosWeaponAttribute.HitCurse] = value;
   }
   ```

3. **Wire `GetProperties(IPropertyList list)` in the relevant base class.** Prefer known client clilocs. If a helper such as `ItemPropertyDisplay` or a capturing test utility is not present in the target branch, do not assume it exists — either use established local OPL patterns or add the helper/test infrastructure deliberately.

4. **Add static aggregation only when formulas need equipped totals.** `AosAttributes.GetValue`, `AosWeaponAttributes.GetValue`, and `AosArmorAttributes.GetValue` walk equipped items. Some item-local effects can read the owner item directly; status/combat formulas need aggregators.

5. **Implement the gameplay effect in the owning pipeline.** Weapon hit effects belong in `BaseWeapon.OnHit`; defensive/parry properties belong in `AbsorbDamageAOS`/shield hooks; damage-to-resource properties belong in `AOS.Damage` or a deliberately named helper.

6. **Enable generation separately.** Do not add a new property to `BaseRunicTool`, loot packs, artifacts, or imbuing in the same step unless the task explicitly includes distribution/economy policy. A stored and working property can remain GM/test-only until generation is reviewed.

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

The SA review notes in `references/sa-item-properties-introduction.md` originally recommended `HitCurse`, `HitFatigue`, and `HitManaDrain` as the first low-scope weapon-hit slice; that slice now exists on current RebirthUO `live` as a separate `SaWeaponAttribute` enum and `SaWeaponAttributes : BaseAttributes` container. For additional SA weapon properties, keep using the separate SA container pattern when the property family is broader than original AoS. For the next post-hit-slice priorities, see `references/sa-defensive-properties-next-slices.md`: prefer `Reactive Paralyze` first because it hangs off successful parry/block, then `Soul Charge` in `AOS.Damage`, then `Casting Focus`; defer Damage Eater/Resonance until absorption caps/charges and distribution policy are scoped. Keep new properties GM/test-only until loot/runic/imbuing distribution is explicitly reviewed.

## Existing Armor Attribute Reference

`AosArmorAttribute` (`AOS.cs:928-935`) is intentionally small: LowerStatReq, SelfRepair, MageArmor, DurabilityBonus. For SA-era additions, keep `SoulCharge` and `ReactiveParalyze` as a separate defensive/parry slice, and prefer a separate SA-specific absorption container for Damage Eater / Resonance / Casting Focus if that family is implemented.

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

### Generating Source-Backed Item Property Documentation

When the user asks for "all item properties from the Internet" or similar documentation output, use the extraction recipe in `references/item-properties-internet-extraction.md`. The durable source pattern is UO.com Magic Item Properties as the official table plus UOGuide's Item Properties wikitext API to recover concrete tooltip variants, Stygian Abyss properties, special state properties, and negative properties. Generate one Markdown file per property plus an index, and label the result as source documentation rather than RebirthUO implementation parity.

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

For properties without a cliloc, first check whether the target branch already has a display helper. If not, either add a reusable helper deliberately or use the closest established local OPL pattern. Do not assume `ItemPropertyDisplay` exists on this branch.

```csharp
if (Attributes.Luck < 0)
{
    list.Add($"{"Unlucky"}");
}
```

If a reusable helper exists or is added, route these fallback rows through it so future raw-name properties stay consistent.

Remember `CLAUDE.md:14`: PropertyList string literals must be holes. Use `$"{}"` form inside the cliloc arg, never bare concatenation.

### Adding a Hit-Effect Property

The existing `BaseWeapon.OnHit` pipeline already computes property chances and dispatches hit spell, area, leech, and lower-attack/defense effects. To wire a new SA hit effect, add a `Core.SA`-gated block beside the existing AoS hit-effect block, use the property value as a percentage chance with any active property-bonus scalar, and keep the effect body small and testable.

Example shape:

```csharp
if (Core.SA)
{
    var curseChance = (int)(WeaponAttributes.HitCurse * propertyBonus);

    if (curseChance != 0 && curseChance > Utility.Random(100))
    {
        DoHitCurse(attacker, defender);
    }
}
```

New effects need tests for trigger/no-trigger and a pre-SA no-effect control. Do not add them to loot/runic/imbuing generation in the same change unless distribution policy is part of the task.

## Pitfalls

1. **Forgetting the `Core.AOS` gate.** `BaseAttributes.GetValue` returns 0 when `!Core.AOS`, so reading a property value on a pre-AoS server is safe. But writing code that *computes* OPL rows without checking the era can leak property text into pre-AoS tooltips. Guard the OPL side with `if (!Core.AOS) return;` or skip the relevant `if` blocks in `GetProperties`.
2. **Setting `_values` directly.** Never poke into `_values` from outside `BaseAttributes`. Always go through `SetValue(int bitmask, int value)`. The setter is the only place that triggers the durability `UnscaleDurability` side effect and updates `_names`.
3. **Adding a new bit value to a `[Flags]` enum without picking the next high bit.** The bit allocation is dense and intentional. If a contributor adds a low bit, they collide with an existing value. New bits go at the top of the enum (next high bit) and the change is recorded in the plan.
4. **Forgetting `ReflectPhysical` consumption in combat.** `AOS.Damage` reads `ReflectPhysical` once and applies it before `m.Damage`. New reflect-style effects (e.g. SA `Blood Oath`-style reflect) need a parallel code path in `AOS.Damage` or a `BaseCreature` hook.
5. **Adding a new SA attribute without considering pre-SA shards.** SA attributes that affect formulas need an `if (Core.SA)` or `if (Core.ML)` gate in the consumer. Stygian Abyss introduced several property types that should not affect pre-SA combat.
6. **Overlapping property definitions.** If two different properties can apply to the same concept (e.g. `LowerStatReq` on weapon/armor-specific containers versus common `AosAttributes`), the consumer must read the right container/static aggregator. Current effective-value dispatch is hard-coded by item family, not generic interface dispatch.
7. **Wrong OPL row order.** The client expects properties in a documented order: name, hue, amount, weight, equipped layer, resists, then `AosAttributes` (alphabetical by cliloc), then `AosWeaponAttributes`/`AosArmorAttributes`, then `AosSkillBonuses`, then `AosElementAttributes`. Moving properties around confuses tooling and breaks player muscle memory.
8. **Bypassing `BaseAttributes.SetValue`.** The indexed/typed setters auto-update durability scaling where needed, refresh equipped mobile stats/resistances/deltas, re-apply skill mods, and invalidate item/mobile properties (`AOS.cs:1403-1534`). Direct field mutation or custom side-channel state will skip those side effects; use the container setter unless you intentionally handle every side effect yourself.
9. **Assuming test helpers exist.** Some branches may not have `CapturingPropertyList`, `ItemPropertyDisplay`, or SA absorption containers yet. Search the target branch before following examples; add missing helpers intentionally with tests, or adapt to the existing local patterns.
10. **Using `AosAttributes.AddStatBonuses` without checking the remove key.** Current `AOS.cs` adds stat mods with `$"{GetHashCode()}Str/Dex/Int"` but `RemoveStatBonuses` removes `$"{Owner.Serial}Str/Dex/Int"` (`AOS.cs:590-626`). The helper is used by `BaseQuiver` and `BaseTalisman`; until fixed/tested, prefer the item-local serial-key pattern used by `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, and `Spellbook`, or fix the helper plus a regression test before adding a new helper caller.
11. **Treating storage/tooltip/generation/gameplay as one step.** `BaseRunicTool.ApplyAttributesTo` has separate per-family random property tables for weapons, armor, hats, jewelry, and spellbooks. Adding a stored property and OPL row does not automatically make it roll on loot/runics/artifacts or affect combat; add each surface deliberately and test each one.
12. **Using conceptual documentation as implementation evidence.** For RebirthUO development, inspect local source and product/mechanics sources directly. Do not rely on conceptual docs trees as proof that a mechanic is implemented or that a property should be live.
13. **Forcing every UO.com magic-property row into `BaseAttributes`.** Some table rows are dynamic display state rather than persistent, rollable item properties. `Last Parry Chance` is the canonical example: use runtime state on `BaseShield`/`BaseWeapon`, EJ-gated cliloc `1158861`, and no loot/runic/imbuing rollout unless explicitly scoped. See `references/last-parry-chance-runtime-tooltip.md`.
14. **Treating Mana Phase as a generic talisman roll without a parity decision.** UO.com lists Mana Phase as `Talisman (L)`, while UOGuide and ServUO point to a concrete `ManaPhasingOrb` with charges, 30s cooldown, `BuffIcon.ManaPhase`, and `Spell`/`SpecialMove` mana hooks. Decide whether damage caused or damage taken clears the effect before implementing, and keep loot/runic/imbuing distribution separate. See `references/mana-phase-talisman-implementation-notes.md`.

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New bit value uses the next free high bit of the enum.
- [ ] `[CommandProperty(AccessLevel.GameMaster)]` wrapper is added to the container.
- [ ] `BaseWeapon`/`BaseArmor`/`BaseClothing`/`BaseJewel` `GetProperties` emits a new OPL row for the property.
- [ ] Static `GetValue(Mobile, attribute)` aggregation includes the new property on the right `if` branch (weapon/armor/clothing/IAosItem).
- [ ] `CapturingPropertyList` test covers the OPL output for at least one new property and one non-AoS era control.
- [ ] No `_values` direct access from outside `BaseAttributes`.
- [ ] Programmatic mutations go through typed/indexed `BaseAttributes` setters, or custom state explicitly invalidates properties and updates affected mobile stats/resistances.
- [ ] `OnAfterDelete` does not need updating for new attributes (storage is owned by `BaseAttributes`), but verify `DurabilityBonus` still works for armor/weapon via the `SetValue` hook.
- [ ] For new hit effects, the combat effect body is gated by `Core.SA` (or the correct stricter era) at the dispatch site, not just inside the aggregator.
- [ ] Property distribution is intentional: storage/OPL/effect work does not automatically add loot/runic/imbuing rolls.
- [ ] For SA work, `references/sa-item-properties-introduction.md` was checked for source hierarchy, repo anchors, and phased implementation guidance.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the base classes (`BaseWeapon`, `BaseArmor`, ...) that own these property containers; also hosts the cross-cutting reading recipe at `uo-items-foundation/references/analyzing-modernuo-subsystems.md` (use it before analyzing other UO subsystems).
- `uo-crafting-recipes-resources` - generation routines that produce these magical items.
- `modernuo-property-lists` - OPL mechanics and cliloc lookup.
- `modernuo-era-expansion` - `Core.AOS`/`Core.SE`/`Core.ML`/`Core.SA` gating for properties.
- `references/sa-item-properties-introduction.md` - session-derived SA item property implementation notes: UO.com/ServUO source hierarchy, local RebirthUO anchors, recommended implementation slices, and pitfalls for storage/tooltip/gameplay/generation separation.
