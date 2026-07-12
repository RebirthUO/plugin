# Focus Item Property Research

Use this reference when drafting or implementing the UO `Focus` weapon property. It is distinct from `Casting Focus` and `Spell Focusing`.

## Source classification

- **Canonical — UO.com Magic Item Properties:** `Focus`; intensity `N/A`, imbue weight `No`, found on `Weapons (L)`, cap `N/A`. The description says successful hits against the same target cycle weapon damage from an initial `-50%` of base damage toward a later `+20%`; changing target resets the cycle.
- **Canonical — UO.com Publish 71:** https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2011-2/publish-71-21st-july/ — dated July 21, 2011 and lists `Focusing Weapons` among new buff icons. Treat this as the earliest official introduction evidence found and route the property to High Seas / `Core.HS`; the note does not explicitly state the property-introduction sentence.
- **Community/reference — UOGuide Item Properties:** https://www.uoguide.com/Item_Properties — has no matching `Focus` weapon-property row and instead lists unrelated `Rage Focus`; do not use that omission to override UO.com.
- **Engine precedent — ServUO:** `Scripts/Abilities/Focus.cs` tracks transient attacker/target state, resets on weapon removal or target change, updates a focus buff, and advances on hits. `Scripts/Misc/AOS.cs` stores `Focus` in `ExtendedWeaponAttribute`. `Scripts/Items/Equipment/Weapons/BaseWeapon.cs` applies the offset in weapon damage and uses tooltip cliloc candidate `1150018`; buff candidates are `1151393` / `1151394`.

## Conflict gate

UO.com specifies the endpoints and target reset but not the exact intermediate values or the precise meaning of “successful hit” for miss, parry, zero-damage, and special-move cases. Current ServUO precedent uses a `-40` default, a `-50` first transition, then `+10` below `-40` and `+8` afterward, so it conflicts with the canonical starting point and must not be copied as authoritative.

Conservative issue default:

- Preserve canonical `-50%` start, `+20%` maximum, and target-change reset.
- Advance only after a landed, non-missed, non-parried weapon hit; explicitly decide zero post-resist damage behavior before implementation merge.
- Treat intermediate values as an implementation-review decision requiring client evidence or an explicitly accepted parity choice.

## RebirthUO anchors

- `Projects/UOContent/Misc/AOS.cs:1230-1339`: `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes`; no `Focus` bit exists in the reviewed baseline.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:196-202`, `:239-244`, and `:981-986`: serialized extended weapon attributes, initialization, and duplication.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:1860-1992`: central `GetAosDamage` path; `:1987-1992` applies Battle Lust, clamps the percentage aggregate, and scales damage.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:2144-2153` and `:2359-2363`: existing post-hit and normal-hit-only hooks useful for choosing Focus advancement timing.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:3084-3161`: weapon tooltip dispatch.
- `Projects/UOContent/Items/Weapons/BattleLust.cs` and `Projects/UOContent.Tests/Tests/Items/Weapons/BattleLustPropertyTests.cs`: transient state, cleanup, era gate, tooltip, and runtime-test precedents.
- Local `SpellFocusing.cs`, `FocusAttack.cs`, and `ArcaneFocus.cs` are unrelated systems; do not treat name matches as an existing Focus property implementation.

## Issue-slicing boundaries

The first storage/gameplay issue should add the weapon flag, tooltip, reusable transient context, central damage hook, lifecycle cleanup, and focused tests. Keep `Weapons (L)` distribution separate: do not modify loot, runic crafting/reforging, imbuing, artifacts, vendors, or event rewards without an explicit economy/distribution scope.
