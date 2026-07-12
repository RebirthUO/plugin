# Antique item-property review notes

Use when reviewing or drafting `Antique` for RebirthUO/ModernUO.

## Canonical behavior

- UO.com Magic Item Properties lists `Antique` with intensity `N/A`, imbue weight `No`, found on `(L) Armor, jewelry, weapons, shields`, cap `N/A`.
- The canonical description is increased durability loss; the item can be repaired; Powder of Fortifying can be applied three times, reducing maximum durability to `250`, `200`, and `150`.
- UO.com Publish 86 (Worldwide Release `2014-09-25`) adds Antique to the negative-property family, converts Ephemeral items to Antique, and limits items to at most one negative property.
- Random-loot `(L)` availability is distribution evidence, not permission to add loot/runic/reforging generation to a storage/mechanics ticket.

## Community and engine evidence

- UOGuide Antique says the effect occurs during combat even when the wearer is not hit, reports initial `255/255` durability, says Antique items can be repaired, and says they cannot be enhanced. Treat these as community/reference evidence where UO.com is silent.
- ServUO provides comparison clues: `NegativeAttribute.Antique`, candidate tooltip cliloc `1076187`, weapon/armor-specific decay paths, an older central `OnCombatAction` path, jewelry durability handling, and jewelry repair handling. ServUO constants are not canonical; its paths are not equivalent and must not be copied without an explicit decision.
- The current Classic client/repo uses `1076187` for an Antique statue material. When checked against the configured Classic `Cliloc.enu` using the repository's BWT decompressor/localization record format, entry `1076187` resolves exactly to `Antique`; retain the client-data verification as evidence separate from ServUO precedent.

## RebirthUO anchors

- Shared storage: `Projects/UOContent/Misc/AOS.cs` → `NegativeAttribute`, `NegativeAttributes`, `IsPrized`, `IsMassive`, `IsBrittle`, and `GetProperties()`; add Antique as a coordinated non-colliding flag gated by `Core.HS`.
- Hosts: `BaseWeapon.cs` and `BaseArmor.cs` implement `IDurability`/`IWearableDurability`; `BaseJewel.cs` has hit-point fields and a durability property row but is not currently on the durability interface/combat path.
- Powder: `Items/Special/Bulk Order Rewards/Blacksmithy/PowderOfTemperament.cs` targets `IDurability`, currently raises max durability toward 255, and rejects Brittle before charge consumption. Keep jewelry out of this target path; add Antique thresholds only for eligible non-jewelry equipment.
- Enhancement: `Engines/Craft/Core/Enhance.cs` accepts weapons/armor without an Antique check; if the UOGuide restriction is accepted, reject before resource consumption or mutation.
- Repair: `Engines/Craft/Core/Repair.cs` currently covers weapons/armor/clothing but not jewelry. ServUO's jewelry repair branch is useful evidence if the issue includes the minimal jewelry lifecycle seam.
- Distribution: `Items/Skill Items/Tools/BaseRunicTool.cs` and loot generation must not roll Antique accidentally in the first slice.

## Required issue decisions

1. **Decay formula:** UO.com does not specify chance, cadence, or loss amount. Record the conflict explicitly. Prefer one centralized, deterministic-in-tests, PvM/PvP-consistent combat-action rule over mixing incompatible ServUO weapon, armor, jewelry, and legacy constants. A conservative first-slice policy can be made concrete (for example, one independent `2%` roll per equipped host on an accepted weapon-swing action, removing one current durability and using the existing zero/max/deletion lifecycle); label those numbers as custom policy/engine precedent, not OSI fact.
2. **Jewelry lifecycle:** Official found-on includes jewelry, while current ModernUO lacks jewelry combat/repair integration. Include only the smallest generic jewelry combat/repair seam needed by the accepted scope; do not broaden powder eligibility or rewrite unrelated jewelry systems.
3. **Enhancement:** UOGuide says Antique cannot be enhanced, but UO.com's row is silent. A conservative default is to block the existing weapon/armor enhancement path and document the evidence class.
4. **Initial durability:** Keep UOGuide's `255/255` generation behavior in a later loot/generation ticket unless item creation is explicitly in scope.

## Focused test checklist

- Storage, duplication, serialization, deletion cleanup on weapon, armor/shield, and jewelry.
- High Seas tooltip versus pre-High Seas no-op; verify cliloc candidate against local client data.
- Deterministic active-combat decay for PvM and PvP, including no-direct-hit activity, equipped-only scope, and removal/deletion cleanup.
- Powder progression `255 -> 250 -> 200 -> 150`, no fourth use, no charge mutation on rejection, jewelry excluded.
- Repair remains allowed; enhancement is rejected before mutation if the conservative restriction is accepted.
- `BaseRunicTool.ApplyAttributesTo(...)` and current loot generation do not roll Antique until a separate distribution ticket.

## Issue-template guidance

For `item_property.yml`, use `Persistent`, `N/A` intensity, `No` imbue weight, `N/A` total cap, and `Armor/Jewelry/Shields/Weapons` under `Found on`. Add reviewer sections after the template fields: `Implementation Notes / Repo Anchors`, `Acceptance Criteria`, `Test Plan`, `Risks / Side Effects`, and `Open Questions`. Keep canonical, community/reference, engine-precedent, and repo-evidence claims labeled separately.
