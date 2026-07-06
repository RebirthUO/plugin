# Last Parry Chance Runtime Tooltip

Session source: RebirthUO issue #18 (`Item Property: Last Parry Chance`) review on 2026-07-03.

## Classification

`Last Parry Chance` is not a normal rollable AoS/SA item property in RebirthUO terms. Treat it as a dynamic runtime tooltip value that is written to the item that just successfully parried an attack.

Official UO.com Magic Item Properties table says:

- Property: `Last Parry Chance`
- Imbue Weight: `No`
- Found on: `shields, Weapons`
- Mechanic: `When players parry any attack with a shield or weapon it will now display the last parry chance % on the item.`

Do not infer loot/runic/imbuing/artifact distribution from this property.

## ServUO comparison

ServUO implements this as `LastParryChance` on `BaseShield` and `BaseWeapon`, not as an `AosAttributes` bit. It emits cliloc `1158861` (`Last Parry Chance: ~1_val~%`) and gates the tooltip/update with `Core.EJ`.

Relevant ServUO anchors at review time:

- `Scripts/Items/Equipment/Armor/BaseShield.cs`: runtime `LastParryChance`, EJ-gated `AddNameProperties`, reset on `OnRemoved`.
- `Scripts/Items/Equipment/Weapons/BaseWeapon.cs`: runtime `LastParryChance`, set inside `CheckParry`, EJ-gated tooltip row.

## RebirthUO implementation shape

Prefer a small content-layer implementation:

1. Add a non-serialized runtime `LastParryChance` property to `BaseWeapon` and `BaseShield`.
2. In `BaseWeapon.CheckParry(Mobile defender)`, after a successful parry, set the value on the shield or melee weapon used to parry and call `InvalidateProperties()` only when it changes.
3. Add tooltip rows:
   - `if (Core.EJ && LastParryChance > 0) list.Add(1158861, LastParryChance);`
4. Reset to `0` on `OnRemoved` for weapons and shields.
5. Add focused UOContent tests for EJ-only tooltip display, non-EJ suppression, successful shield/weapon update, excluded fists/ranged path, and unequip reset.

No save migration should be needed if the value remains runtime-only.

## Formula caution

RebirthUO `BaseWeapon.CheckParry` can compare two candidate weapon-parry chances (`chance` vs `aosChance`). Decide explicitly whether to display:

- **Actual used chance** — recommended for product clarity because the UO.com wording says last parry chance; or
- **ServUO exact behavior** — ServUO stores `chance` in one weapon branch even when `aosChance` was the branch that actually produced success.

Expected examples from the reviewed formulas:

| Scenario | Display if actual-used chance |
|---|---:|
| Shield, Parry 120, Bushido 0, Dex 100 | 35% |
| Shield, Parry 80, Bushido 0, Dex 80 | 20% |
| Shield, Parry 80, Bushido 0, Dex 60 | 16% |
| One-handed weapon, Parry 120, Bushido 120 | 35% |
| Two-handed weapon, Parry 120, Bushido 120 | 40% |
| One-handed weapon, Parry 100, Bushido 0, actual `aosChance` branch | 17% |

## Risk profile

- Era: EJ+ unless shard policy says otherwise.
- PvP/PvM: transparency only, no direct balance change.
- Economy: no generation, faucet, sink, or item-value distribution change.
- Saves: runtime-only state avoids migration.
- Client: cliloc availability is an EJ-era/client compatibility concern; keep the `Core.EJ` gate unless a custom policy overrides it.
