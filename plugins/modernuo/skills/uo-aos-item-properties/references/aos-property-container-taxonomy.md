# AoS Property Container Taxonomy Notes

Session-derived guidance for choosing storage containers when later-era item properties (SA/HS/TOL) are added to the AoS magic-property system.

## Core decision

Treat **AoS as the item-property system**, not as only the set of properties introduced in the Age of Shadows publish. Later expansions add properties and behavior, but they usually still live conceptually inside the AoS magic-item-property architecture.

Avoid making container names mirror expansions (`SaWeaponAttributes`, `HsWeaponAttributes`, `TolWeaponAttributes`) unless the property family is truly expansion-specific and cannot be described by item family or mechanic. Era belongs primarily in:

- tooltip/OPL gates,
- gameplay/effect gates,
- effective-value aggregators,
- loot/runic/imbuing distribution policy,
- tests.

## Recommended container shape

Use family/role names, not era names:

- Existing core containers remain `AosAttributes`, `AosWeaponAttributes`, `AosArmorAttributes`, `AosSkillBonuses`, `AosElementAttributes`.
- If `AosWeaponAttribute` bit capacity is too tight, prefer a neutral overflow/family container such as `AosExtendedWeaponAttributes` or `ExtendedWeaponAttributes` over `SaWeaponAttributes`.
- If absorption/eater/casting-interrupt properties need their own family, prefer `AosAbsorptionAttributes` or `AbsorptionAttributes` over `SaAbsorptionAttributes`.

Each property still has its own introduction gate, e.g. SA properties gated by `Core.SA`, TOL properties by `Core.TOL`, HS properties by `Core.HS`.

## Why not put everything in `AosWeaponAttribute`?

The existing `BaseAttributes` storage uses a `uint _names` bitmask and sparse `int[] _values`. With the classic AoS weapon properties plus additions such as `Massive`, the safe high bits are limited. Forcing all SA/TOL weapon properties into `AosWeaponAttribute` can quickly require either:

- using the awkward `0x80000000` signed-int edge,
- widening the storage model (`uint` to `ulong`) with migration risk,
- or adding another container later anyway.

A neutral extended weapon container is a conservative compromise: it preserves AoS-as-system semantics while avoiding risky storage widening.

## Practical review checklist

When reviewing a property-container change:

1. Ask whether the container name describes a mechanic/family or just an expansion label.
2. Keep storage, tooltip, gameplay, aggregation, and distribution decisions separate.
3. Ensure every added persistent container is copied in `OnAfterDuped`, initialized in constructors and legacy deserialize paths, and covered by generated migration content.
4. Add `ShouldSerialize*` save flags for sparse containers unless the serializer pattern intentionally omits them.
5. Test pre-era no-op behavior at the consumer/tooltip level, not only storage reads.
6. Do not enable loot/runic/imbuing rolls as a side effect of adding storage.

## Suggested placement examples

| Property/family | Preferred storage | Gate |
|---|---|---|
| Classic HCI/DCI/SSI/SDI/LMC/LRC/etc. | `AosAttributes` | `Core.AOS` |
| Classic hit spells/areas/leeches/UBWS/MageWeapon | `AosWeaponAttributes` | `Core.AOS` |
| `Brittle`, `Prized` | `AosAttributes` as common negative/special properties | `Core.SA` / `Core.HS` per property |
| `Massive` | `AosWeaponAttributes` / `AosArmorAttributes` if bit space and semantics fit | `Core.HS` |
| `Soul Charge` | `AosArmorAttributes`, shield-only consumer | `Core.SA` |
| SA weapon procs (`HitCurse`, `HitFatigue`, `HitManaDrain`, `BloodDrinker`, `Splintering`, `BattleLust`) | neutral extended weapon property container | `Core.SA` |
| TOL weapon procs (`Sparks`, `Swarm`) | same neutral extended weapon property container | `Core.TOL` |
| Eaters / Casting Focus | neutral absorption property container | `Core.SA` |
