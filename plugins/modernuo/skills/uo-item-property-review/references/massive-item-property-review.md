# Massive — item property review notes

Use when reviewing, drafting, or implementing `Massive` on RebirthUO/ModernUO (GitHub issue #12 pattern).

## Canonical behavior (UO.com)

- Publish 86 negative item property family member (with `Prized`, `Brittle`, `Unwieldy`, `Antique`, `Cursed`).
- Intensity `N/A`, imbue weight `No`, found on `Armor(L) weapons(L) shields (L)` only (not jewelry in the official row).
- Effect: **strength requirement becomes 125**.
- Presentation: **no separate `Massive` tooltip line** — only the normal **Strength Requirement** row (`1061170`).
- Override rule: **cannot be overridden by lower requirements from imbuing or enhancing** (UO.com wording).

## Publish 86 loot context

- Introduced in global loot negative-property set; at most **one negative property** per item.
- Distribution is a separate economy ticket from storage/equip/property-list behavior.

## ServUO engine precedent (not parity proof)

- `NegativeAttribute.Massive` on `NegativeAttributes`; no Massive cliloc in `NegativeAttributes.GetProperties` (Brittle `1116209`, Prized `1154910` only).
- `StrRequirement` getter returns `125` when `Massive > 0` on `BaseWeapon` / `BaseArmor`.
- **Divergence:** ServUO still applies `AOS.Scale(StrRequirement, 100 - GetLowerStatReq())` for equip and property list. RebirthUO should follow UO.com and **skip lower-requirements scaling** when Massive is set.

## RebirthUO/ModernUO anchors (verify line numbers on branch)

- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` — `StrRequirement`, `GetLowerStatReq()`, `CheckEquip` str check, `GetProperties` str req display.
- `Projects/UOContent/Items/Armor/BaseArmor.cs` — `ComputeStatReq`, `GetLowerStatReq()`, equip stat checks, property list str req.
- `Projects/UOContent/Misc/ResourceInfo.cs` — resource `*LowerRequirements` folded into `GetLowerStatReq()`.
- `Projects/UOContent/Engines/Craft/Core/Enhance.cs` — imbue/enhance lower-requirements paths.
- Storage: shared **negative-property container** with Prized (#8) / Brittle (#10); do not use positive `AosAttribute` slots.

## Tests to require

- Equip at Str 124 fails, 125 succeeds (with era gate).
- `LowerStatReq` 100% + Massive still shows and requires **125** (equip + property list).
- No Massive-named property-list row.
- No accidental runic/loot roll until distribution is scoped.

## Issue drafting

- Template: `item_property.yml`; title `Item Property: Massive`; labels `ultima-online`, `triage`, `item-property`.
- Document UO.com vs ServUO lower-requirements conflict under `## Research Notes`.