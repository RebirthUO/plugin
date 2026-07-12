# Bane Item Property Review Notes

Use these notes when reviewing or implementing the `Bane` weapon item property for RebirthUO/ModernUO.

## Source status

- UO.com Magic Item Properties is the canonical source for the high-level row:
  - Property: `Bane`
  - Intensity: `N/A`
  - Imbue weight: `No`
  - Found on: `Weapons (L)`
  - Total cap: `N/A`
  - Behavior: on-hit property only triggers when target health is below 50%; as target health decreases, both proc chance and damage increase; damage is 30% of target max hit points as physical damage.
- UO.com Publish 83 is canonical publish-note evidence:
  - Introduces `New Item Property Bane` on certain weapons.
  - Confirms below-50% target-health eligibility, increasing chance and damage as health decreases, up to 30% of target max HP.
  - Confirms the raw damage cannot exceed 350 physical damage.
- UOAlive Bane page is community/reference evidence:
  - Damage is 30% of target max HP, capped at 350 physical damage before physical resistance.
  - Damage potential starts around 50% at half health and grows toward 100% near death.
  - Example values: 12,000 HP target => raw 3,600 capped to 350; with 70% physical resist => 105 max post-resist, about 52.5 at half health. 150 HP target => raw 45; with 70% physical resist => 13.5 max post-resist, about 6.75 at half health.
- ServUO is engine precedent, not canonical proof:
  - `ExtendedWeaponAttribute.Bane = 0x00000008` in `Scripts/Misc/AOS.cs`.
  - `ExtendedWeaponAttributes.Bane` command property.
  - `BaseWeapon` applies Bane when `Bane > 0 && defender.Hits < defender.HitsMax / 2` using `inc = min(350, defender.HitsMax * .3)` and subtracting the current HP fraction before adding to weapon damage.
  - Tooltip cliloc candidate: `1154671` (`Bane`), ServUO emits it under `Core.TOL`.
  - Loot-generation metadata registers Bane as non-imbuable/non-loot-style extended weapon property with cliloc `1154671` and label cliloc candidate `1154570`.

## RebirthUO planning guidance

- Treat Bane as a post-AoS, weapon-only, on-hit property. It should not be added blindly to the classic `AosWeaponAttribute` bit set if an extended/family weapon-property container is the better local architecture.
- Era gate is a review decision. UOAlive says Publish 83 (High Seas timeframe), while ServUO tooltip gating uses `Core.TOL`; RebirthUO should choose deliberately (`Core.HS`, `Core.TOL`, or custom publish/ruleset gate).
- Split storage/tooltip/mechanics/distribution:
  - Storage + GM/test setting can be implemented first.
  - Tooltip needs cliloc verification for `1154671` against local client data/tests.
  - Mechanics need explicit decisions for proc chance scaling, rounding, physical-resist order, and whether zero-damage/parried hits can proc.
  - `Weapons (L)` is distribution evidence only; do not add Bane to random loot, runics, reforging, imbuing, vendor search, or artifacts without explicit distribution scope.

## Focused test expectations

- Pre-gate: no tooltip and no effect.
- Tooltip: `Bane` line appears with cliloc `1154671` once verified.
- Thresholds: no effect above or exactly at 50% HP unless review decides otherwise; effect is eligible below 50% HP.
- Formula examples: 12,000 HP / 70% physical resist and 150 HP / 70% physical resist should cover the cap and PvP-size target cases.
- Distribution guard: existing `BaseRunicTool.ApplyAttributesTo(...)` and loot paths should not roll Bane unless the ticket explicitly includes distribution.
