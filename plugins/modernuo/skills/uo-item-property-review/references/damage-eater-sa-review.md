# Damage Eater SA item-property review

Use this when drafting, reviewing, or implementing `Damage Eater` / eater-family item-property work for RebirthUO/ModernUO.

## Source evidence

- Canonical: UO.com Magic Item Properties (`https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`) lists `Damage Eater` with intensity `3 – 15`, imbue weight `No`, found on `(R)(L)Shields, Armor`, total cap `30`, and the rule that damage must match the eater type. Same row states specific eaters stack to `30`, the all-damage eater caps at `18%`, up to `20` healing charges are stored, and charges convert every three seconds from the last time damage was received.
- Canonical: UO.com Publish 60 Stygian Abyss (`https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`) lists `Damage Eaters` under new item properties and repeats same-type conversion, 30% specific cap, and 18% all-damage cap.
- Community/reference: UOGuide `Damage Eater` explains the family: Kinetic = physical, Fire/Cold/Poison/Energy = matching elemental types, `Damage Eater` = all damage types. It says all-damage eater does not add to a matching specific eater; use the higher applicable heal. It also notes direct damage / Bleed-style damage only triggers all-damage eater, not kinetic.
- Community/reference conflict: UOGuide `Item Properties` has older table data (`5 - 20%`, type `Hit`, armor/shield/weapon availability). Prefer current UO.com unless maintainers intentionally target older/custom behavior.
- Engine precedent: ServUO `Scripts/Abilities/SAPropEffects.cs` has `DamageEaterContext` with per-type delayed healing, 30% specific cap, 18% all-damage cap, 20 charges, and three-second delayed heals. ServUO `Scripts/Misc/AOS.cs` models eaters/resonance/casting focus in an `SAAbsorptionAttribute` family.

## RebirthUO repo anchors observed

- `Projects/UOContent/Misc/AOS.cs` damage pipeline computes post-resist `totalDamage`, applies final damage, then has the actual-hit-delta pattern: `var oldHits = m.Hits; m.Damage(totalDamage, from); var appliedDamage = Math.Max(0, oldHits - m.Hits); BattleLust.OnDamageTaken(m, from, appliedDamage);`. Eater healing should be based on actual/post-resist positive damage rather than raw pre-resist damage.
- On `origin/main` as of the 2026-07-09 review sweep, RebirthUO/ModernUO has a neutral `AbsorptionAttribute` / `AbsorptionAttributes` container for `CastingFocus` on armor, but no `DamageEater`, `Damage Eater`, `KineticEater`, `FireEater`, `ColdEater`, `PoisonEater`, `EnergyEater`, or eater cliloc symbols under `Projects/UOContent`. Verify again at implementation time before assigning bits.
- `ExtendedWeaponAttribute` is weapon-only and currently used for Bane/Battle Lust/Sparks/Blood Drinker/Swarm-style weapon properties. Do not put Damage Eater there for the UO.com default Armor/Shields scope.
- `AosArmorAttribute` is small (`LowerStatReq`, `SelfRepair`, `MageArmor`, `DurabilityBonus`). Extend the existing neutral absorption-family container for Damage Eater unless current implementation review finds a stronger reason for a separate container; do not overload the small armor enum.
- `BaseArmor` owns standard AoS and armor attributes plus negative attributes plus serialized `AbsorptionAttributes`, initializes/dupes them, and emits absorption tooltips; `BaseShield` derives from `BaseArmor`, so shield hosting can generally share armor storage/tooltip paths.

## Recommended ticket / implementation shape

- Era gate: `Core.SA` for tooltip and gameplay. Stored values must be inert pre-SA.
- Host default: Armor and Shields only. Document the conflict before adding UOGuide/ServUO weapon hosting.
- Implement family together when possible: `Damage Eater`, `Kinetic`, `Fire`, `Cold`, `Poison`, `Energy`, because caps and non-additive matching are shared and hard to validate in isolation.
- Storage/tooltip/gameplay are separate from distribution. Do not enable random loot, runic reforging, imbuing, artifact distribution, or vendors in the first storage/gameplay PR unless the issue explicitly includes the economy decision.
- Tooltip cliloc candidates from ServUO/client precedent: `1113593` Fire Eater, `1113594` Cold Eater, `1113595` Poison Eater, `1113596` Energy Eater, `1113597` Kinetic Eater, `1113598` Damage Eater. Verify against local client data/property-list tests before merging.
- Message candidate: `1113617` (`Some of the damage you received has been converted to heal you.`). Verify locally.

## Test expectations

- Storage and dupe/copy behavior on armor and shields.
- SA tooltip presence and pre-SA tooltip absence for every eater row in scope.
- Damage-pipeline tests using controlled physical/fire/cold/poison/energy/direct portions and asserting delayed heal amount.
- Cap tests: 30% specific, 18% all-damage, 20 pending charges, and non-additive all-damage vs specific behavior.
- Era tests proving pre-SA inertness.
- Cleanup tests: delayed heals do not fire after death, deletion, removal, or loss of the relevant equipment/property.
- Distribution guard: prove loot/runic/reforging/imbuing tables are unchanged in a storage/gameplay slice.

## Risks / side effects

- PvP sustain and burst-window changes; enforce caps/delay/cleanup.
- PvM farming uptime and loot-value inflation if distribution is enabled too early.
- Source conflict on weapon hosting; default to current UO.com Armor/Shields.
- Raw pre-resist damage over-heals high-resist builds; prefer actual/post-resist damage portions or explicitly reviewed equivalent math.
- Timer/context leaks; use cancellable cleanup or owner/context validation before applying delayed heals.
