# Antique Item Property Review Notes

## When this applies

Use these notes when reviewing or implementing the `Antique` magic item property for RebirthUO/ModernUO. This is a negative item property, not a normal AoS attribute roll, and it should not imply loot/runic/imbuing distribution by itself.

## Source summary

- UO.com Magic Item Properties lists `Antique` with intensity `N/A`, imbue weight `No`, found on `(L) Armor, jewelry, weapons, shields`, cap `N/A`.
- UO.com description: increased durability loss; can be powdered 3 times, excluding jewelry; each powder reduces max durability cap to 250, 200, and 150 respectively; can be repaired.
- Treat as SA/modern-era behavior unless the target shard explicitly defines a different custom ruleset.

## ServUO reference anchors checked

ServUO commit checked during review: `6fd01855840590e22cc73d94b5f7d9a97b1cf537`.

- `Scripts/Misc/AOS.cs:3214-3264` — `NegativeAttribute` includes `Antique = 0x00000010`; `NegativeAttributes.GetProperties()` emits cliloc `1076187`.
- `Scripts/Misc/AOS.cs:3266-3320` — Antique combat durability decay helper (`CombatDecayChance = 0.02`) that lowers `HitPoints` by up to 4 or `MaxHitPoints` by 1.
- `Scripts/Items/Consumables/PowderOfTemperament.cs:194-241` — Powder caps are `Antique == 1 => 250`, `== 2 => 200`, otherwise `150`; successful powder increments the Antique counter.
- `BaseWeapon.cs:313`, `BaseArmor.cs:271-276`, `BaseClothing.cs:79`, `BaseJewel.cs:676-677` — `CanFortify` allows Antique values below 4 and blocks further powder after three successful applications.
- `BaseWeapon.cs:2310-2314`, `BaseArmor.cs:2604-2608`, `BaseClothing.cs:785-789`, `BaseJewel.cs:629-633` — Antique increases durability-wear likelihood in the normal combat wear paths.

## RebirthUO anchors checked

- `Projects/UOContent/Misc/AOS.cs` currently has normal AoS/SA containers such as `AosAttributes` and `SaWeaponAttributes`; no negative-property container was present during the review.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:2085-2119` has the weapon durability wear path.
- `Projects/UOContent/Items/Armor/BaseArmor.cs:753-805`, `Projects/UOContent/Items/Clothing/BaseClothing.cs:342-402`, and `Projects/UOContent/Items/Shields/BaseShield.cs:31-112` have armor/clothing/shield durability wear paths.
- `Projects/UOContent/Items/Special/Bulk Order Rewards/Blacksmithy/PowderOfTemperament.cs:77-126` currently handles generic fortification but not Antique caps/counter behavior.
- `Projects/UOContent/Items/Jewels/BaseJewel.cs:21-67` and `:514-517` show jewelry has durability fields/tooltip, but it was not `IDurability`/`IWearableDurability` in the reviewed branch.
- `Projects/UOContent/Items/Misc/IDurability.cs:3-20` defines the local durability interfaces.

## Recommended implementation shape

1. Add a `NegativeAttribute`/`NegativeAttributes` storage container in UOContent, modeled after the existing `BaseAttributes` pattern and gated by the target era (`Core.SA` unless custom policy says otherwise).
2. Wire `NegativeAttributes` into `BaseWeapon`, `BaseArmor`, `BaseClothing`, and `BaseJewel`; `BaseShield` inherits the armor path.
3. Emit cliloc `1076187` for Antique in SA+ only.
4. Integrate Antique into durability wear paths for weapons, armor, clothing, and shields.
5. For jewelry, decide explicitly whether to add `IDurability`/wear support. Full source parity favors adding durability support while still rejecting Powder of Fortifying on jewelry.
6. Update Powder of Fortifying so Antique acts as an application counter: start at `1`, then successful powder increments to `2`, `3`, and `4`; caps are `250`, `200`, `150`; `>= 4` blocks further fortification.
7. Keep distribution separate. Do not add Antique to loot/runic/imbuing/artifact generation unless the task explicitly scopes that economy decision.

## Tests to require

- SA+ tooltip shows cliloc `1076187`; pre-SA does not.
- Powder cap transitions: `1 -> 250 -> 2`, `2 -> 200 -> 3`, `3 -> 150 -> 4`, and `4` cannot fortify.
- Jewelry powder attempt remains rejected.
- At least one forced/random-controlled durability wear test proves Antique increases wear compared with a non-Antique control.
- Serialization/migration tests cover every host item that receives `NegativeAttributes`.

## Product side effects

- Economy: Antique increases durability churn and Powder of Fortifying demand; distribution is a separate faucet/sink decision.
- PvM/PvP: Raises long-run gear maintenance cost but does not directly alter burst/counterplay.
- Trust/save compatibility: new serialized fields on base item classes require careful migration tests before live deployment.
