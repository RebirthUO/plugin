# SA Item Properties Introduction Notes

Session-derived implementation notes for introducing Stygian Abyss-era item properties in RebirthUO/ModernUO.

## Trigger

Use this reference when planning or implementing SA-era item properties such as `HitCurse`, `HitFatigue`, `HitManaDrain`, `SoulCharge`, `ReactiveParalyze`, Damage Eater / Resonance / Casting Focus, or later loot-generation negative properties.

## Source hierarchy used

- UO.com Magic Item Properties table: `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
- UO.com Imbuing overview: `https://uo.com/wiki/ultima-online-wiki/skills/imbuing/`
- ServUO current code is useful as comparative implementation evidence, not canonical design: `Scripts/Misc/AOS.cs`, `Scripts/Items/Equipment/Weapons/BaseWeapon.cs`, `Scripts/Items/Equipment/Armor/BaseArmor.cs`, `Scripts/Items/Tools/BaseRunicTool.cs`.
- RebirthUO local source remains the implementation authority for shape/conventions.

## RebirthUO anchors observed

- Era and feature flags:
  - `Projects/Server/ExpansionInfo.cs` defines `Expansion.SA`.
  - `Distribution/Data/expansions.json` has Stygian Abyss at Id 8 with `SA: true`, Ter Mur map-selection flag, Gothic/Rustic housing flags, and MobileStatusVersion 6.
  - `Distribution/Data/map-definitions.json` defines `TerMur`.
- Current AoS property storage:
  - `Projects/UOContent/Misc/AOS.cs` contains `AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, `AosElementAttribute`, and `BaseAttributes`.
  - `BaseAttributes` stores a `uint _names` bitmask plus sparse `int[] _values`, so adding bits within the 32-bit mask is save-compatible for existing items, but high-bit values need explicit care.
- Tooltip/OPL surfaces:
  - `Projects/UOContent/Items/Weapons/BaseWeapon.cs:GetProperties`.
  - `Projects/UOContent/Items/Armor/BaseArmor.cs:GetProperties`.
  - `Projects/UOContent/Items/Clothing/BaseClothing.cs:GetProperties`.
  - `Projects/UOContent/Items/Jewels/BaseJewel.cs:GetProperties`.
- Gameplay hooks:
  - `BaseWeapon.OnHit` handles existing hit spell, leech, area, and lower-attack/defense properties.
  - `BaseWeapon.AbsorbDamageAOS` handles parry/block and shield hit paths; Reactive Paralyze belongs here, not in tooltip/storage code.
  - `AOS.Damage` is the right central hook for damage-to-resource conversions such as Soul Charge / Eaters.
- Generation hooks:
  - `BaseRunicTool.ApplyAttributesTo(BaseWeapon/BaseArmor/BaseHat/BaseJewel/Spellbook)` controls current runic/random property application.
  - Do not add new SA properties to generation tables until drop/runic/imbuing policy is explicitly decided.

## Recommended implementation slices

### Slice 1: low-scope weapon hit properties

Start with `HitCurse`, `HitFatigue`, and `HitManaDrain` because they fit the existing `AosWeaponAttributes` + `BaseWeapon.OnHit` model.

Implementation checklist:

1. Add bits to `AosWeaponAttribute` using the next safe free bits. Keep within current storage constraints unless intentionally migrating storage.
2. Add `[CommandProperty]` wrappers to `AosWeaponAttributes`.
3. Add `Core.SA`-gated OPL rows in `BaseWeapon.GetProperties` using known cliloc IDs when available.
4. Add `Core.SA`-gated effect dispatch in `BaseWeapon.OnHit` after the existing hit-spell/hit-lower logic.
5. Keep generation disabled until a source/policy decision says the properties should roll on loot, runic reforging, or imbuing.
6. Add tests for storage/API, OPL, effect behavior, and a pre-SA no-effect control.

### Slice 2: defensive/parry properties

`SoulCharge` and `ReactiveParalyze` are higher risk and should be separate from weapon-hit work.

- `ReactiveParalyze` should trigger only from a successful parry/block path, not every incoming hit.
- `SoulCharge` should be implemented in the damage pipeline where post-resist damage is known.
- Both require PvP/PvM side-effect review because they affect counterplay and sustain.

### Slice 3: absorption/eater/resonance family

Damage Eater, Resonance, and Casting Focus should not be forced into the small `AosArmorAttribute` enum unless deliberately scoped. Prefer a separate SA-specific container (for example `SAAbsorptionAttributes`) if multiple absorption/casting-interrupt properties are implemented.

### Slice 4: loot/economy integration

Only after storage + tooltip + gameplay tests are in place:

- Decide whether each property is loot-only, runic reforging, imbuing, artifact-only, Ter Mur-only, or custom.
- Add generation tables/caps/intensities deliberately.
- Review economy impact: imbuing control, ingredient sinks, relic-fragment flow, and loot-value inflation.

## Important pitfalls

- Do not treat "enum value added" as "property implemented". Storage, tooltip, gameplay effect, and generation are separate surfaces.
- Do not leak SA properties to ML/AoS shards. `BaseAttributes.GetValue()` is only `Core.AOS`-gated; consumers and generation must explicitly gate `Core.SA`.
- Do not widen `BaseAttributes` storage casually. The current `uint` mask is compact and save-sensitive.
- Do not use conceptual documentation trees as development evidence. For implementation work, inspect RebirthUO source and authoritative product/mechanics sources directly.
- Do not mass-add all UO.com Magic Item Properties. Many current properties are post-SA or late-publish systems with major PvP/economy/durability side effects.
