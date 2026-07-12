# Mysticism: Healing Stone research notes

Use when drafting, reviewing, or implementing the SA Mysticism spell **Healing Stone** (`Kal In Mani`).

## Source findings

- **UO.com Mysticism page** (canonical current player-facing table): Healing Stone is a first-circle Mysticism spell using Bone, Garlic, Ginseng, and Spider's Silk. It creates a large non-transferable red gem in the caster's backpack with stored healing points based on Mysticism plus Focus/Imbuing. It requires a free hand, attempts cure or heal on use, deducts healed/cure points from the stone, says the stone takes **20 seconds** to fully recharge, and lasts until points are used up or it is dropped.
- **UO.com Publish 60 / Stygian Abyss** (canonical introduction): Mysticism introduced with SA; Healing Stone listed as a spell that conjures a stone that instantly heals the caster when used.
- **UO.com Publish 65** (canonical revamp): Healing Stone gains stored life/healing points, per-use healing energy, **2-second** usage cooldown, **15-second** full energy replenish, poison cure chance based on Mysticism plus Focus/Imbuing, poison-level life-energy cure cost, one-third life-energy cost on failed cure, cure not affecting healing energy, and significantly increased summoning time.
- **UOGuide Healing Stone** (community/reference): mana 4, minimum skill 0, **5-second** delay, Blessed/non-transferable behavior, disappear if dropped, cannot trade/sell, and Publish 65 mechanics including 15-second replenish and cure behavior.
- **ServUO engine precedent**: `HealingStoneSpell` uses a **5-second** cast delay, creates/replaces a backpack `HealingStone`, stored life force `(Mysticism + supportSkill) * 1.25`, max heal `(Mysticism + supportSkill) / 6`, item id `0x4078`, localized success `1080115`, and effect/sound precedent. `HealingStone` is blessed/non-transferable, blocks secure trade, deletes on drop, uses a 2-second action cooldown, replenishes per-use healing over 15 one-second ticks, and resets per-use healing after potion healing. Its cure path is mostly threshold/cost based, so do not treat it as proof against Publish 65's chance-based wording.

## RebirthUO repo anchors

- `Projects/UOContent/Spells/Initializer.cs:181-186` — `Core.SA` Mysticism block; Healing Stone registration at spell ID 678 may be commented until implemented.
- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs:34-56` — Mysticism cast skill, support skill, mana, and required-skill behavior.
- `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs:13-14` — Mystic spellbook offset 677 and count 16, so Healing Stone is spell ID 678 / second Mystic book slot.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/HealingStoneScroll.cs` — scroll support may already exist with spell ID 678 and item ID `0x2D9F`.
- `Projects/UOContent/Engines/Craft/DefInscription.cs` — `AddMysticismSpell` and SA inscription block may already register Healing Stone scroll crafting.
- Local cure chance shapes to inspect before implementing: `Spells/Second/Cure.cs`, `Spells/Chivalry/CleanseByFire.cs`, and `Spells/Mysticism/CleansingWindsSpell.cs`.

## Recommended first-slice policy

For a post-Publish 65 SA implementation unless the shard intentionally chooses a custom/current-table rule:

- Cast delay: **5 seconds**. Publish 65 says summoning time increased significantly; UOGuide and ServUO both use 5 seconds. This is safer for PvP than the generic first-circle 0.5s table delay.
- Full per-use healing-energy replenish: **15 seconds**. Publish 65 is the explicit revamp note and is corroborated by UOGuide and ServUO. Document the UO.com current-table **20-second** conflict in comments/tests.
- Use cooldown: **2 seconds**.
- Stored life force: `(Mysticism + max(Focus, Imbuing)) * 1.25` unless local balance policy says otherwise.
- Max heal per full-energy use: `(Mysticism + max(Focus, Imbuing)) / 6` unless local balance policy says otherwise.
- Poison cure: chance-based, because Publish 65 and UOGuide explicitly say chance-based. A local-friendly starting formula is to mirror existing Cure/Cleanse style with `effectiveSkill = (Mysticism + max(Focus, Imbuing)) / 2.0`, then subtract poison-level difficulty and control random in tests.
- Poison energy cost: ServUO-style `min(120, poison.RealLevel * 25)` is useful engine precedent, but verify local poison-level semantics.
- Potion interaction: reset or reduce per-use stone healing after potion heals, following ServUO precedent and PvP burst-control policy.
- Lifecycle: caster-bound/self-only, non-transferable, no secure trade, no vendor sale path, delete on drop, finite energy, timer cleanup on delete, safe serialization/load behavior.

## Test focus

- SA registration at spell ID 678 and no pre-SA exposure.
- Mystic spellbook slot and scroll/inscription path.
- Cast prerequisites: mana, reagents, backpack, existing-stone replacement/no stockpiling.
- Item use: owner-only, free-hand required, full-health/no-poison refusal, finite life force, 2-second cooldown, 15-second recharge.
- Cure: poison-level cost, chance-controlled success/failure, one-third failure cost, no healing-energy consumption on cure.
- Transfer/storage: drop deletes, trade/secure-trade/vendor/containers cannot create an economy item.
- Persistence/timers: partial depletion, active recharge, delete during timer, world save/load.
- PvP side effects: Mortal Strike/heal-prevention consistency, potion-heal reset/reduction, poison cadence.