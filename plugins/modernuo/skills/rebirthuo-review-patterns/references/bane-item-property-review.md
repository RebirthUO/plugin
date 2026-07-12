# Bane Item Property Review Notes

Use when reviewing or refining RebirthUO issues for the Publish 83 `Bane` weapon property.

## Source Frame

- UO.com Magic Item Properties: `Bane`, intensity `N/A`, imbue weight `No`, found on `Weapons (L)`, cap `N/A`; on-hit property only triggers below 50% target health; chance and damage increase as target health decreases; damage is 30% of target max hit points as physical damage.
- UO.com Publish 83: Bane is found on certain weapons; below-50% trigger; increasing chance and damage; up to 30% target max HP; cannot exceed 350 physical damage.
- UOAlive/UOGuide community detail: examples commonly used for tests are 12,000 HP / 70% physical resist => 350 raw cap => 105 max post-resist, scaling from about 52 near half health; and 150 HP / 70% physical resist => 45 raw => 13.5 post-resist, scaling from about 7 near half health.
- ServUO precedent: `ExtendedWeaponAttribute.Bane`, tooltip cliloc candidate `1154671`, deterministic below-50% extra damage scaling with raw potential `min(350, HitsMax * 0.3)` reduced by current health fraction before `AOS.Damage` mitigation. This precedent does not by itself prove the canonical proc-chance formula.

## RebirthUO Issue #1 Decisions Captured During Interview

- Era gate: `Core.HS` / Publish 83.
- If no exact proc-chance formula is found, follow ServUO-style deterministic scaling below 50% HP rather than inventing a custom chance formula.
- PvP: same formula/cap/physical-resist mitigation applies to player targets.
- Storage: add Bane as a one-off flag in `AosWeaponAttributes`; do not introduce a general `ExtendedWeaponAttributes` container for this ticket unless the issue is later changed.

## Repo Anchors Observed

- `Projects/UOContent/Misc/AOS.cs` currently defines `AosWeaponAttribute` through `DurabilityBonus` and `AosWeaponAttributes`; no local `Bane` or `ExtendedWeaponAttributes` surface was found.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` serializes `AosWeaponAttributes`; no Bane storage field/container was present at review time.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` `OnHit` performs normal damage, `AOS.Damage`, leeches, area/spell/lower-attack-defense effects; no Bane hook was present at review time.
- `Projects/UOContent/Items/Skill Items/Tools/BaseRunicTool.cs` random weapon property generation uses the classic property set; Bane should remain absent unless distribution is explicitly scoped.

## Review Pitfalls

- Do not download or trust unsolicited external zip attachments from issue comments during mechanics review. Ignore them unless the user explicitly asks for sandbox review.
- Do not call local repo absence canonical UO behavior; label repo findings as repo evidence.
- If updating GitHub issue #1 per the user's workflow, update the initial issue body only; do not add a solution comment.
- Keep distribution separate unless the user explicitly scopes loot/runic/reforge/imbue/artifact/event sources.
