# Massive negative item property (Publish 86)

Session-derived implementation notes for RebirthUO issue #20 / UO `Massive` item property.

## Source decision

- UO.com Magic Item Properties: `Massive` sets the item's Strength Requirement to **125**, does not show a separate `Massive` tooltip label, and cannot be overridden below 125 by Lower Requirements from imbuing/enhancing.
- UOGuide `Massive`, `Item Properties`, and `Publish 86`: introduced with **Publish 86** as a negative item property. The visible indication is the normal `strength requirement 125` item property.
- RebirthUO practical gate chosen by maintainer instruction: map Publish 86 to `Core.HS` for the mechanics-only slice.

## Implementation shape

- Mechanics-only: do **not** add loot/runic/reforging/imbuing/artifact distribution in the same PR.
- Storage fits existing containers:
  - `AosWeaponAttribute.Massive` + `AosWeaponAttributes.Massive` for weapons.
  - `AosArmorAttribute.Massive` + `AosArmorAttributes.Massive` for armor and shields (`BaseShield : BaseArmor`).
- Shared constant: `AOS.MassiveStrengthRequirement = 125`.
- Weapon behavior:
  - Add a `BaseWeapon.ComputeStrengthRequirement()` helper.
  - If `Core.HS && WeaponAttributes.Massive != 0`, return `125`.
  - Otherwise preserve existing `AOS.Scale(StrRequirement, 100 - GetLowerStatReq())` behavior.
  - Route weapon `CanEquip`, tooltip strength requirement (`1061170`), and `PlayerMobile.ValidateEquipment` through that helper.
- Armor/shield behavior:
  - In `BaseArmor.ComputeStatReq(StatType.Str)`, if `Core.HS && ArmorAttributes.Massive != 0`, return `125`.
  - Dex/Int stat requirements remain unchanged.
  - Armor/shield `CanEquip`, tooltip strength requirement (`1061170`), and `PlayerMobile.ValidateEquipment` already consume `ComputeStatReq`.

## Tooltip policy used

- Do not add any `Massive` tooltip row or raw string.
- Show `strength requirement 125` via cliloc `1061170`.
- If the item also has Lower Requirements, keep the existing Lower Requirements tooltip row (`1060435`) visible; Massive only overrides the effective Strength Requirement calculation.

## Tests to add

Use `[Collection("Sequential UOContent Tests")]` for real item/mobile construction.

Suggested focused class: `MassiveItemPropertyTests`.

Cover:

- Storage accessors for weapon, armor, and shield containers.
- `Core.HS` positive cases:
  - Weapon `StrRequirement = 10`, `LowerStatReq = 100`, `Massive = 1` => effective strength `125`.
  - Armor/shield `StrRequirement = 100`, `LowerStatReq = 100`, `Massive = 1` => effective strength `125`.
  - Mobile with Str 124 cannot equip; Str 125 can equip.
  - Tooltip has `1061170` argument `125` and no textual `Massive` row.
  - Optional explicit policy check: Lower Requirements row remains visible when present.
- Pre-HS control (`Expansion.SA`): Massive storage does not affect existing Lower Requirements calculation.
- `PlayerMobile.ValidateEquipment` drops equipped Massive weapon/armor/shield when Strength falls below 125. If needed, invoke the private sandbox method by reflection rather than waiting for the asynchronous timer.

Validation pattern:

```bash
git diff --check
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~MassiveItemPropertyTests" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

## Pitfalls

- Do not confuse this negative property with old durability levels named `Massive`; use stable mechanic names and avoid publish-number prefixes in symbols.
- Do not place Massive in SA-only or TOL extended weapon containers; the selected RebirthUO mechanics gate is `Core.HS`.
- Do not suppress Lower Requirements storage or tooltip rows unless a maintainer explicitly changes the tooltip policy; Massive overrides the effective Strength Requirement, not the existence of the other property.
- Do not update only tooltip or only equip checks. Tooltip, equip, and stat-change auto-drop must all use the same effective Strength Requirement helper.
