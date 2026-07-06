# Item-Property Review: Casting Focus Notes

Use this reference when reviewing or implementing RebirthUO issues for the `Casting Focus` magic item property or related caster-interrupt defensive SA properties.

## Source-backed facts from #12 review

Authoritative/source-backed anchors used:

- UO.com Magic Item Properties table: `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
  - Property: `Casting Focus`
  - Intensity: `1-3`
  - Imbue Weight: `No`
  - Found on: `(R)(L)Armor`
  - Cap: `12%`
  - Description: `A chance to resist interruptions while casting spells`
- Parent/Epic policy from RebirthUO #2: implement property mechanics first; decide loot/runic/imbuing/artifact distribution separately.

## Local client cliloc anchors

Local Classic / 7.0.114.2 client data confirmed:

- `1113696` = `Casting Focus ~1_val~%`
- `1113690` = `You regain your focus and continue casting the spell.`
- `1152389` = `This property provides a chance to resist any interruptions while casting spells.  It has a cumulative cap of 12%.  The inscription skill can also grant up to a 5% additional bonus which can exceed the item cap.`

The client cliloc text adds an implementation-critical detail not present in the UO.com table: Inscription can add up to `+5%` and may exceed the `12%` item cap.

## Repo anchors checked

- `Distribution/Data/expansions.json` defines `Stygian Abyss` with `SA: true`; use `Core.SA` as the safe default gate.
- `Projects/UOContent/Misc/AOS.cs` has the existing `SaWeaponAttribute` / `SaWeaponAttributes` pattern for SA-specific item-property storage and aggregation.
- `Projects/UOContent/Misc/AOS.cs` shows `AosArmorAttributes` is still the small AoS set (`LowerStatReq`, `SelfRepair`, `MageArmor`, `DurabilityBonus`); do not overload it casually for a broader SA absorption/caster-defense family.
- `Projects/UOContent/Misc/AOS.cs` `BaseAttributes` owns compact `uint _names` + sparse `int[] _values` storage and invalidation side effects.
- `Projects/UOContent/Items/Armor/BaseArmor.cs` has the primary armor attribute container and tooltip surface.
- `Projects/UOContent/Items/Clothing/BaseClothing.cs` has a similar clothing attribute/tooltip surface; include clothing only if the implementation explicitly treats it as part of the intended Armor family and tests it.
- `Projects/UOContent/Spells/Base/Spell.cs` `OnCasterHurt()` is the correct interrupt hook; the implementation should prevent `Disturb(DisturbType.Hurt)` only when the Casting Focus roll succeeds.
- `Projects/UOContent/Items/Skill Items/Tools/BaseRunicTool.cs` and `Projects/UOContent/Misc/LootPack.cs` are distribution anchors, but should not be modified for a mechanics-only ticket.
- `Projects/UOContent.Tests/Tests/Items/Weapons/SaWeaponAttributesTests.cs` provides local patterns for SA gate, tooltip, `PredictableRandom`, and effect tests.

## Recommended review decision

Casting Focus can be marked implementierungsreif when the ticket scope is mechanics-only and distribution is explicitly out of scope:

- Storage + tooltip + gameplay effect are clear.
- Safe era gate is `Core.SA`.
- Tooltip cliloc is known (`1113696`).
- Success message cliloc is known (`1113690`).
- Formula/test values are specific enough.

## Recommended implementation shape

- Add a small SA absorption / caster-defense property container, initially with `CastingFocus` only. Avoid mass-adding inactive Damage Eater / Resonance / Soul Charge bits unless their tickets are in scope.
- Add the container to `BaseArmor` first; optionally add clothing only with explicit scope and tests.
- Tooltip: `Core.SA` gated `list.Add(1113696, prop)`.
- Gameplay: in `Spell.OnCasterHurt()`, preserve the existing Protection behavior. Only when damage would otherwise disturb the spell, roll Casting Focus and, on success, send `1113690` and keep casting.
- Distribution: do not update loot, runic, reforging, imbuing, or artifacts in the first mechanics PR.

## Formula/test values

Use these as expected values in review comments or tests:

- `itemChance = min(12, SumEquippedCastingFocus)`
- Suggested Inscription bonus from client text and ServUO comparison: `inscribeBonus = Inscribe >= 50.0 ? min(5, fixedInscribe / 200) : 0`
- Expected values:
  - `49.9` Inscription -> `+0`
  - `50.0` Inscription -> `+2`
  - `99.9` Inscription -> `+4`
  - `100.0+` Inscription -> `+5`
  - Max item + GM Inscription chance: `12 + 5 = 17%`

## Pitfalls

- Do not let Casting Focus prevent damage; it only resists the cast interruption.
- Do not let it block equip/use/movement/new-cast disturbances without a separate source.
- Do not leak the tooltip or effect before `Core.SA`.
- Do not silently enable economy distribution; that changes loot value and PvP/PvM caster survivability and needs a separate review.
- ServUO is useful comparative implementation evidence, not canonical UO truth. Label it as comparison when cited.