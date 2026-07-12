# Blood Drinker SA Item Property Review

Session-derived source and implementation notes for drafting/reviewing a Blood Drinker item-property ticket.

## Source classification

- `Canonical` UO.com Magic Item Properties: Blood Drinker row lists intensity `N/A`, imbue `No`, found on `Weapons (L)`, total cap `N/A`, and describes the effect as allowing the attacker to gain life from Bleed Attack; damage done through Bleed Attack is transferred to the attacker’s health.
- `Canonical` UO.com Publish 60 / Stygian Abyss launch page: lists Life Syphon with `Blood Drinker` among Stygian Abyss artifacts.
- `Canonical` UO.com Stygian Abyss artifacts page: Life Syphon and Vampiric Essence include Blood Drinker.
- `Community/reference` UOGuide Blood Drinker: successful Bleed Attack with such a weapon transfers bleed damage to the attacker’s health.
- `Community/reference` UOGuide Bleed Attack: Bleed Attack is AoS, but Blood Drinker is a later property used by Blood Drinker weapons.
- `Community/reference` UOGuide Publish 60: Publish 60 is the September 8, 2009 Stygian Abyss launch and lists Life Syphon with Blood Drinker.
- `Engine precedent` ServUO stores `BloodDrinker` in `AosWeaponAttribute`, displays cliloc `1113591`, uses heal message cliloc `1113606`, and snapshots Blood Drinker when the bleed context starts.

## RebirthUO repo anchors observed

- `Projects/UOContent/Misc/AOS.cs`: `AosWeaponAttribute` storage exists. Do **not** blindly copy ServUO’s `BloodDrinker = 0x02000000` because the observed RebirthUO branch used that bit for `Bane`.
- `Projects/UOContent/Items/Weapons/Abilities/BleedAttack.cs`: `BeginBleed` starts a timer; `DoBleed` currently applies tick damage and doubles it for non-player defenders. There was no Blood Drinker hook in the observed branch.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs`: weapons own `AosWeaponAttributes`, emit weapon OPL rows through `WeaponAttributes.GetProperties(list)`, and dispatch weapon abilities.

## Recommended implementation shape

- Treat Blood Drinker as a Stygian Abyss, weapon-only, fixed-presence property. Gate tooltip/gameplay by `Core.SA`.
- Store it in the selected weapon-property container, but choose the next safe free bit or a neutral extended weapon-property container if the branch has one. Avoid collision with existing persistent bits.
- Tooltip should be a name-only row; ServUO precedent uses cliloc `1113591`. Verify against local client/property-list tests before merge.
- Hook gameplay to the Bleed Attack context, not to generic Hit Life Leech. Healing should occur only after a successful Bleed Attack creates a bleed context.
- Conservative default: snapshot Blood Drinker eligibility at successful Bleed Attack application, matching ServUO and avoiding per-tick equipment churn.
- Conservative default for heal amount: use actual applied bleed damage where practical because UO.com says “damage done”; otherwise cap the scheduled tick amount by remaining defender hits.
- Do not add imbuing rollout. UO.com lists imbue weight `No`. Treat loot/artifact rollout (Life Syphon, Vampiric Essence) as a separate explicit scope decision unless the ticket includes it.

## Review decision notes

When reviewing a Blood Drinker issue for implementation readiness, the minimal safe slice is **storage + tooltip + Bleed Attack healing**. Treat named SA artifacts (`Life Syphon`, `Vampiric Essence`) and loot distribution as follow-up scope unless the ticket explicitly includes them.

Local client cliloc extraction confirmed these useful IDs in Classic `cliloc.enu`:

- `1113591 = Blood Drinker`
- `1113606 = The blood drinker effect heals you.`
- `1152387` long description: Blood Drinker allows hit-point gain when using the Bleed Attack special move; all damage inflicted through Bleed Attack transfers to the attacker; only found on weapons that allow Bleed Attack.

Implementation review nuance: RebirthUO `Mobile.Damage` returns `void`, so a strict “damage done” implementation should measure the defender HP difference around the Bleed tick (`oldHits - m.Hits`) rather than healing from the scheduled random damage amount. This also handles death/remaining-HP truncation better. Use `Mobile.Heal` for the attacker so normal `HitsMax`, region, and `OnHeal` behavior still applies, and send cliloc `1113606` only for a positive Blood Drinker heal.

For the equipment-swap ambiguity, prefer snapshotting Blood Drinker eligibility when the Bleed context is successfully created, matching ServUO and avoiding per-tick weapon/equipment churn.

## Implementation notes from first RebirthUO slice

- On branches where `ExtendedWeaponAttribute.HitSparks` already occupies `0x00000004`, Blood Drinker should use the next free extended weapon bit (`0x00000008`) unless later parallel work changes the allocation. Keep the bit-order test updated with Bane, Battle Lust, Sparks, and Blood Drinker together.
- Preserve the public `DoBleed(Mobile m, Mobile from, int level)` behavior for existing callers and add an internal/testable overload that carries the snapped Blood Drinker boolean. This avoids changing non-Blood-Drinker Bleed Attack semantics while letting focused tests drive deterministic ticks.
- Send cliloc `1113606` only after `Mobile.Heal` actually raises the attacker's Hits. This avoids a misleading Blood Drinker message when the attacker is already at `HitsMax`, dead, invalid, or when region/heal hooks prevent healing.
- In tests, use `PredictableRandom(0)` to make `Utility.RandomMinMax(level, level * 2)` return the low bleed tick value deterministically. For non-player defenders, assert the existing PvM multiplier by expecting double the same tick amount.
- Do not set `Hits = 0` and assume `Mobile.Alive == false`; use `Kill()` when a test needs a genuinely dead attacker. `Hits = 0` alone can leave the mobile logically alive in lightweight fixtures.
- For bleed-immunity failure coverage, a minimal `BaseCreature` test stub can override `BleedImmune => true` and `GetSpeeds(...)` with fixed values so the `AIType` constructor does not require NPC speed JSON fixture setup.

## Suggested tests

- Tooltip appears in SA and is absent before SA, preferably through `BaseWeapon.GetProperties` rather than only the container method.
- Successful Bleed Attack with Blood Drinker heals the attacker on bleed ticks.
- Bleed Attack without Blood Drinker does not heal.
- Non-player defender path follows the existing PvM bleed damage multiplier.
- Player defender path has no unsourced extra PvP cap.
- Bleed-immune/failure paths create no heal context.
- Healing is based on applied HP loss, caps at attacker `HitsMax`, and sends cliloc `1113606` only when positive.
- Storage serialization/clone/copy remains compatible if a new bit/container is added.
- Distribution remains unchanged: no runic, loot, artifact, or imbuing rollout in the storage/gameplay slice.
