---
name: "uo-combat-pipeline"
description: "Use when working with the UO combat pipeline in ModernUO/RebirthUO servers - the BaseWeapon swing lifecycle, AOS.Damage damage formula, the 5 elemental resists, slayer groups, weapon abilities, special moves, parry, parrying with shields vs weapons, anatomy/tactics/swordsmanship modifiers, PvP vs PvM damage, delayed damage, and area-effect damage. Use when debugging why a hit connects/misses, why a damage type splits, why a slayer does not apply, or how the pre-AOS vs AOS damage formula differ."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Combat Pipeline

## Overview

UO combat is a layered pipeline: a swing resolves into a hit/miss check, the hit's damage is computed (base damage + skill modifiers + slayer + weapon properties + tactics/anatomy), the damage is split across 5 elemental types, the targets' resists reduce each split, the result is applied via `AOS.Damage`, and side effects (reveal, aggression, durability, skill gain) follow.

The engine split between engine code (`Projects/Server/Mobiles/Mobile.cs:195-197`, `Projects/Server/Items/Item.cs`) and content code (`Projects/UOContent/Items/Weapons/BaseWeapon.cs:31-160+`, `Projects/UOContent/Items/Armor/BaseArmor.cs:16-140+`, `Projects/UOContent/Misc/AOS.cs:28-239`). The single most important function in the pipeline is `AOS.Damage`, defined at `Projects/UOContent/Misc/AOS.cs:37-246`.

This skill covers the swing lifecycle, the damage formula, the resist split, slayer groups, weapon abilities, special moves, parry, anatomy/tactics, ranged-archery modifiers, and the per-facet combat differences. The pre-AOS flat-damage path and the AOS/SE/ML/SA damage splits are the era boundary that most code reviews touch.

## When to Use

- Debugging why a hit misses, deals reduced damage, or gets parried.
- Adding a new weapon type or weapon ability.
- Implementing or fixing a slayer check.
- Adding a new damage type or new elemental resist cap.
- Wiring the AOS damage split to a new spell or special move.
- Auditing per-facet combat differences (Felucca vs Trammel vs Ilshenar etc.).
- Building a custom boss with a unique damage profile (Peerless, Champ, Paroxysmus).

Don't use for:

- The base item model (use `uo-items-foundation`).
- The full property enumeration (use `uo-aos-item-properties`).
- Spell casts as such (use `uo-magic-spells`).

## The Swing Lifecycle

A `BaseWeapon.OnSwing(Mobile attacker, Mobile defender)` call drives the lifecycle. The flow (paraphrased from `BaseWeapon.cs`):

```
OnSwing(attacker, defender)
 ├─ alive / warmode / distance / disarm check
 ├─ CheckSkill(attacker, weaponSkill, min, max)
 ├─ if miss: animation/sound + return
 ├─ Compute base damage: GetBaseDamage(attacker)
 ├─ Apply modifiers:
 │   ├─ Strength bonus (StrScale)
 │   ├─ Tactics bonus
 │   ├─ Anatomy bonus
 │   ├─ Lumberjacking bonus (for axes)
 │   ├─ Slayer check (2x or 3x)
 │   ├─ WeaponAttributes.HitLeech (Hits/Stam/Mana)
 │   ├─ WeaponAttributes.HitLowerAttack/Defend
 │   ├─ WeaponAttributes.HitMagicArrow/Harm/Fireball/Lightning/Dispel
 │   ├─ WeaponAttributes.HitArea (Physical/Cold/Fire/Energy/Poison)
 │   └─ AOS attributes (DamageIncrease, etc.)
 ├─ Split damage across 5 elementals (AosElementAttributes)
 ├─ AOS.Damage(defender, attacker, damage, phys, fire, cold, pois, nrgy)
 └─ Side effects:
     ├─ Reveal if hidden
     ├─ Aggression (Aggressors / Aggressed lists)
     ├─ Weapon durability loss
     ├─ Stat gain check (Anatomy → +Str/HP)
     ├─ Skill gain check (Tactics, weapon skill)
     └─ CurseWeapon, Corpse Skin, Consecrate Weapon active
```

`CheckSkill(attacker, SkillName.Swordsmanship, 0.0, 100.0)` is the gating miss chance. The actual hit/miss formula lives in `WeaponAbility.GetHitChance` (or in the basic weapon base for non-ability swings): `((attacker.Skills[weapon].Value + 20.0) * (100 + attacker.PhysicalHitChanceIncrease) / 100) - defender.DefenseChance - 50`. The 50 is a flat penalty from the attacker that pushes 0-skill characters below 50% hit chance.

## Base Damage and Skill Modifiers

`BaseWeapon.GetBaseDamage(Mobile attacker)` is the source of truth for the weapon's damage range before any modifiers. The range is `[min, max]` from the item's `MinDamage`/`MaxDamage` plus random variance.

Skill-modifier ordering in `BaseWeapon.OnHit`:

1. **Base damage roll**: `min..max`.
2. **Strength contribution**: `attacker.Str * StrScale / 100` (StrScale is per-skill, 5-30% typical).
3. **Tactics contribution**: `(attacker.Tactics * 0.3) / 100 * damage` (Tactics adds up to 30% at 100).
4. **Anatomy contribution**: `attacker.Anatomy * 0.1` added to base (Anatomy adds up to 10 HP per swing at 100).
5. **Lumberjacking**: `(Lumber * 0.1) * damage / 100` for axes only.
6. **Slayer**: 2x damage against the matched creature type, 3x for super-slayers.
7. **AOS WeaponDamage**: `+WeaponDamage%` from items.
8. **AOS AosAttribute.DamageIncrease**: `% damage` for that combat style.
9. **Consequent damage**: `SwingSpeedIncrease` (the next swing is faster but not the current one).

`AOS.Damage` then receives the final damage and splits it across the 5 elemental types.

## The 5 Elemental Damage Types and Resists

The five damage types and their canonical sources (from the official UO Stratics AoS Combat spotlight at `uo.stratics.com/content/aos/combatchanges.shtml`):

| Type | Source examples |
|---|---|
| **Physical** | Standard melee and ranged weapons. |
| **Energy** | Energy Bolt, Lightning, Magic Arrow (partial), spell-trigger items. |
| **Fire** | Fireball, Fire Field, Flame Strike, Meteor Swarm. |
| **Cold** | Snow Elemental aura, Frost spells (added in AoS). |
| **Poison** | Poison spell, Poison Strike, applied poisons, Acid Blood. |

The six-element model includes **Chaos** (randomly distributed across the five) and **Direct** (bypasses armor, capped at 35 PvP / 70 PvM with Death Strike) as AoS+ extensions.

Resists are exposed on `Item` via the hooks at `Item.cs:566-570` and on `Mobile` via `PhysicalResistance`/`FireResistance`/etc. The static `Mobile.GetMaxResistance(ResistanceType)` helper in `AOS.cs:258-280` reads the max resistance from equipment. The `GetStatus(from, index)` method exposes the values to the client status window.

`AOS.Damage` (the main damage sink) is at `AOS.cs:37-246`. The pre-AOS path is the early `if (!Core.AOS) { m.Damage(damage, from); return damage; }`. The AoS+ path:

```csharp
totalDamage = damage * phys * (100 - resPhys);
totalDamage += damage * fire * (100 - resFire);
totalDamage += damage * cold * (100 - resCold);
totalDamage += damage * pois * (100 - resPois);
totalDamage += damage * nrgy * (100 - resNrgy);
totalDamage /= 10000;  // (percent * percent)
```

This is the pre-resist split. The `resPhys` etc. values come from the `Mobile.GetMaxResistance` helper (which reads equipped items).

For ML, the chaos distribution (Chaos Damage randomizes across elements at `AOS.cs:76-106`) and the direct-damage formula (`damage * direct / 100`, capped at 35) are added.

## Slayer System

`BaseWeapon.Slayer` and `BaseWeapon.Slayer2` are the slayer slots. The `SlayerName` enum lives in `BaseWeapon.cs` and covers all creature types plus a "super slayer" variant for each family.

The standard slayer values (`AosWeaponAttribute.HitLeechHits` etc.):

| Slayer | 2x damage vs |
|---|---|
| `SlayerName.Silver` | Undead |
| `SlayerName.Repond` | Repond (humanoid) |
| `SlayerName.Reptile` | Dragons, drakes, serpents |
| `Slachnid`, `Arachnid` | Spiders, scorpions |
| `Elemental` | All elementals |
| `Fey` | Fey |
| `Undead` | Undead |
| `Gargoyles` | Gargoyles (SA) |
| `Abyss` | Abyss creatures (SA) |
| `Eodon` (ToL) | Valley of Eodon creatures |

A super-slayer (`Superslayer` like `Reptile` covers all reptiles including dragons, drakes, serpents) gives 3x damage. `BaseWeapon.Slayer` is checked in `OnHit` against the defender's type via `SlayerGroup` mapping in `BaseWeapon` and the engine's creature-type registry.

The pre-SE Slayer system was the only `AosWeaponAttribute` that pre-dated AoS; pre-AoS only 5 slayer groups existed (Reptile, Undead, Elemental, Fey, Repond).

## Special Moves (AOS+)

A special move is a weapon-bound ability that costs mana and can be activated by the player. `BaseWeapon.PrimaryAbility` and `BaseWeapon.SecondaryAbility` are the per-weapon bindings. The abilities themselves live in `Projects/UOContent/Items/Weapons/Abilities/` and inherit from `WeaponAbility`.

The current requirements (per UOGuide Publish 96):

- **Primary move**: 30 Tactics + 70 weapon skill
- **Secondary move**: 60 Tactics + 90 weapon skill

Wrestling abilities are exempt from the Tactics requirement. Shadowstrike (Stealth ability) and Infectious Strike (Poisoning ability) are also exempt.

Mana cost can be reduced with `Lower Mana Cost` (LMC) from items. The cost is also reduced when combined-skill totals reach 200 (-5) or 300 (-10). The Publish 64 change removed Humans' "Jack of All Trades" racial bonus from the LMC reduction pool.

`BaseWeapon` fires the special move after the swing resolves if the player pre-activated it. The order is `WeaponAbility.OnHit` -> the ability's effect (e.g. `DoubleStrike` swings a second time at no swing-delay cost). The ability's effect is added to the swing's damage via `WeaponAbility.OnHit` and/or `AOS.Damage` callbacks.

Common abilities by weapon class (the official list per UOGuide):

| Weapon class | Primary | Secondary |
|---|---|---|
| Fencing (Spear) | Double Strike | Execute |
| Fencing (Kryss) | Double Strike | Armor Pierce |
| Fencing (War Fork) | Double Strike | Bleed Attack |
| Swordsmanship (Katana) | Double Strike | Lightning Strike |
| Swordsmanship (Scimitar) | Double Strike | Double Whirlwind |
| Swordsmanship (Broadsword) | Double Strike | Bladeweave (ML) |
| Mace Fighting (War Hammer) | Double Strike | Crushing Blow |
| Mace Fighting (Mace) | Double Strike | Disarm |
| Mace Fighting (Club) | Double Strike | Concussion Blow |
| Archery (Heavy Crossbow) | Double Strike | Moving Shot |
| Archery (Bow) | Double Strike | Force Arrow (ML) |
| Wrestling (Fist) | Disarm | Stagger (SE) |

`Disarm` checks 30/60 Tactics thresholds. `Stagger` is an SE move that prevents the next attack. `Bladeweave`, `Force Arrow`, `Lightning Arrow`, `Psychic Attack`, `Serpent Arrow`, `Force of Nature` are the 6 ML moves.

## Parry

Parry lives in `Projects/UOContent/Skills/Parry.cs` and is invoked during the swing:

- With a shield: full parry value used.
- With a weapon only: 50% of parry value used.

`Parry` blocks the entire hit (not partial damage absorption). A successful parry consumes no mana; a failed parry costs the attacker mana for the activated special move but the hit lands. Parry does not consume a swing.

`Parry` interacts with the AoS Resist system: a parried hit is treated as "no hit" for the purpose of AOS.Damage, so the elemental split does not apply.

`Block` is the dedicated shield-skill path. The `AosArmorAttribute` system provides per-armor bonuses that affect parry/block chances (`AosArmorAttributes.GetValue(m, AosArmorAttribute.SelfRepair)`, etc.).

## Anatomy, Tactics, Evaluating Intelligence, Spirit Speak

Skill modifiers feed the damage formula:

- **Anatomy**: +HP per swing (max +10 at 100 skill). Also gives +5% crit chance for some classes.
- **Tactics**: up to +30% damage at 100 skill. Required for all weapon special moves.
- **Evaluating Intelligence (Magery)**: scales Magery damage; +1% per 10 skill on most damage spells.
- **Spirit Speak (Necromancy)**: scales Necro damage and duration. Has its own heal formula.
- **Focus (SE)**: passive +Stamina/Mana regen when not in armor.
- **Resisting Spells**: passive minimum resist floor (40 at GM), plus damage reduction on Blood Oath per Publish 48.

The full skill-vs-damage table is in `BaseWeapon.cs` and `AOS.Damage` calls into `AosAttributes.GetValue(m, AosAttribute.WeaponDamage)` etc.

## Resistances and Cap

`Mobile.GetMaxResistance(ResistanceType)` reads the highest contribution from equipped items plus the `Resisting Spells` floor:

- `PhysicalResistance`: from armor `AR` value, `AosArmorAttribute` bonuses, racial bonuses.
- `Fire/Cold/Poison/Energy`: from armor, `AosArmorAttribute`, race (Elf +5 Energy cap), `AosAttribute` bonuses.

The natural cap per element is 70 in the standard ruleset. Items that exceed 70 are clamped at `Mobile.GetMaxResistance`. The actual applied resistance per swing is computed by `AOS.Damage` against the equipped items, not against the cap.

`Mobile.PhysicalResistance` is the new (AoS) name for the classic `Armor Rating` (AR). The client shows the same number in the status window.

## Combat Across Facets

The seven facets have different combat rules:

| Facet | PvP | Stealing | Note |
|---|---|---|---|
| Felucca | Free (non-consensual) | Allowed | Resources double; only facet with Champion Spawn Power Scrolls. |
| Trammel | Disallowed | Disallowed | Spells like Wall of Stone / Energy Field won't impact other players. |
| Ilshenar | Disallowed | Disallowed | Travel restricted (no Recall/Gate/Sacred Journey in). |
| Malas | Disallowed | Disallowed | New AOS land; Doom and Bedlam dungeons. |
| Tokuno | Disallowed | Disallowed | SE land; travel is unrestricted except in dungeons. |
| Ter Mur | Disallowed | Disallowed | SA land; mostly-instanced Stygian Abyss dungeon. |
| Eodon | Disallowed | Disallowed | ToL land; PvE-focused. |

`SpellHelper` and `Region` enforce these rules: `SpellHelper` checks the region's `IsDungeonRuleset` and `OnBeginSpellCast` hook; the `FacetRules` for travel are in `SpellHelper.cs:52-145`. The PvP-flag check is `Mobile.Warmode && faction/enemy-faction` plus `Mobile.Criminal` and `Mobile.Murderer`.

## Champion Spawn Combat

Champion Spawns (`Projects/UOContent/Engines/ChampionSpawn/`) are a special combat context. The level scaling is documented at `www.uoguide.com/Champion_spawn`:

- 256 kills to clear level 1 (red candles 1-5/6).
- 128 kills to clear level 2.
- 64 kills to clear level 3.
- 32 kills to clear level 4.
- At 16 red candles, the Champion can be summoned by targeting the Idol.

Combat rules in spawn zones:

- Pet summoning is forbidden, with the no-summon radius decreasing as the spawn strength increases.
- No Recall, Gate Travel, or Sacred Journey.
- No rune marking.

The `ChampionSpawnRegion` (a `Region` subclass) enforces these via the `Region.OnBeginSpellCast` and `Region.OnTravel` hooks. The post-kill `TryDropLoot` path gives Champion Spawn Artifacts (30% overall: 10% Shared/Replica, 15% Decorative, 5% Unique), Power Scrolls (Felucca-only; 105, 110, 115, 120 tiers), and Scrolls of Transcendence (Felucca has 2x potency).

## Boss-Specific Damage Profiles (Peerless)

The 6 ML Peerless bosses use combat profiles documented in `docs/mondains-legacy-content-matrix.md`:

- **Dread Horn**: 50,000 HP, 5-element damage split, bard immunity, `Dismount` weapon ability.
- **Shimmering Effusion**: cold aura, frost-damage field, `CapturedEssence` drop.
- **Travesty**: faction-themed, follows the Citadel leader model.
- **Lady Melisande**: dryad-themed, poison pool.
- **Chief Paroxysmus**: paroxysm-themed, acid blood, parrot mount drop.
- **Monstrous Interred Grizzle**: Bedlam-themed, acid blood pool, 6-10 damage pools.

Each Peerless altar has a 10-minute post-kill loot window (`PeerlessAltar.CompleteEncounter`) and an exit teleporter. The model is fully wired in the engine; see `docs/mondains-legacy-content-matrix.md:63-69` for the per-boss evidence and `docs/manual-test-mondains-legacy.md` for the live test path.

## Quivers and Archery Damage

`BaseQuiver` provides an archery-specific damage modifier. The `AOS.Damage` archer path (`AOS.cs:108-142`) reads `BaseQuiver.DamageIncrease` and adds it to the total. This is the per-shard bonus: Quiver of Infinity gives +25% damage, Quiver of Rage gives +20% damage, etc. `ML`-only quivers are gated by `Core.ML`.

`AOS.Damage` also has a "Direct Damage cap of 35" for player-vs-player and 70 with Death Strike. The archer path applies a separate cap when the damage type is `Direct`.

## Common Pitfalls

1. **Calling `Mobile.Damage` directly instead of `AOS.Damage`.** Pre-AoS path is OK; AoS+ shards must use `AOS.Damage` to get the elemental split.
2. **Forgetting to set `WeaponAttributes.DurabilityBonus` for artifact weapons.** The durability roll is in `BaseWeapon.OnHit` and the `DurabilityBonus` value scales the max HP. Forgetting the bonus on a 255/255 artifact weapon breaks the durability band.
3. **Setting `Slayer` instead of `Slayer2` for the second slot.** The engine reads `Slayer2` for the second slayer. Setting both slots to `Slayer` is a duplication bug.
4. **Using `Core.AOS` check for `Slayer` activation.** Slayer is pre-AoS; gating it to `Core.AOS` excludes the pre-AoS shards that need it.
5. **Forgetting to disable the special-move icon on spell cast.** `Spell.Cast` clears the activated special move per `Spell.cs:565-568`. If a weapon ability fires after a spell cast, it is a regression.
6. **Not respecting `Mobile.Blessed` or `Mobile.Blessed` (pre-AoS).** Some creatures are flagged invulnerable to certain damage types.
7. **Forgetting the `BaseCreature` damage hooks.** `BaseCreature.AlterMeleeDamageTo` and `AlterMeleeDamageFrom` can modify damage mid-pipeline. Custom boss code uses these to apply 5-element splits that override the default `AosElementAttributes`.
8. **Setting `Fame`/`Karma` on a creature without setting `VirtualArmor`/`SetResistance`.** The base `AOS.Damage` formula reads both the resistance (set via `SetResistance` or armor) and the damage range. Skipping one produces wonky damage scaling.
9. **Forgetting that `AOS.Damage` does not return a number the spell can use directly for skill gain.** Skill gain is computed separately against the actual damage applied; the pre-AoS `m.Damage` path returns the value used for skill gain.
10. **Hardcoding the slayer check to a creature name.** Use the creature's `Is` checks (e.g. `defender is BaseCreature { }` and the type's slayer group) rather than `defender.GetType().Name == "..."`.

## Common Recipes

### Adding a Custom Weapon Class

```csharp
namespace Server.Items;

[SerializationGenerator(0)]
public partial class KatanaOfDoom : Katana
{
    [Constructible]
    public KatanaOfDoom()
    {
        Hue = 0x4EA; // Quest hue
        Slayer = SlayerName.Silver;
        Attributes.WeaponDamage = 50;
        WeaponAttributes.HitFireball = 30;
    }
}
```

### Modifying the Per-Swing Damage for a Custom NPC

```csharp
public class CustomBoss : BaseCreature
{
    public override void AlterMeleeDamageTo(Mobile to, ref int damage)
    {
        if (to is PlayerMobile) damage = (int)(damage * 1.25);
    }

    public override void AlterMeleeDamageFrom(Mobile from, ref int damage)
    {
        if (from is PlayerMobile) damage = (int)(damage * 0.9);
    }
}
```

### Implementing a Custom Weapon Ability

```csharp
public class CrushingBlow : WeaponAbility
{
    public override int BaseMana => 25;

    public override void OnHit(Mobile attacker, Mobile defender, int damage)
    {
        if (!Validate(attacker) || !CheckMana(attacker, true)) return;
        ClearCurrentAbility(attacker);

        // custom damage multiplier
        AOS.Damage(defender, attacker, damage * 2, 100, 0, 0, 0, 0);
        defender.SendLocalizedMessage(1060165); // You have been hit by a crushing blow!
    }
}
```

### Adding a Per-Facet Damage Modifier

```csharp
public override void AlterMeleeDamageTo(Mobile to, ref int damage)
{
    if (Map == Map.Felucca && to is PlayerMobile) damage += 5;
}
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New weapon ability: `BaseMana` is set, `OnHit` is implemented, `CheckMana` is called, `ClearCurrentAbility` is invoked.
- [ ] `BaseWeapon.GetBaseDamage` is the source of the damage range; no inline `MinDamage = X` / `MaxDamage = Y` mutations.
- [ ] `AOS.Damage` is used for all combat damage on AOS+ shards; pre-AoS shards use `Mobile.Damage`.
- [ ] `Slayer` and `Slayer2` are set via the typed `SlayerName` enum, not magic numbers.
- [ ] New damage type is added to `AosElementAttribute` and `AOS.Damage` (the function handles the new element).
- [ ] `BaseCreature.AlterMeleeDamageTo`/`From` are overridden for any custom boss; the override does not bypass the `AOS.Damage` call.
- [ ] Combat-side effects (Reveal, Aggression, Stat gain, Skill gain, Durability loss) are present in the swing lifecycle.
- [ ] Facet-specific behavior is gated through `Region`/`SpellHelper`/`SpellHelper.TravelCheckType` rather than `Map == Map.Felucca` checks scattered through content.
- [ ] Champion Spawn region hooks (`Region.OnBeginSpellCast`, `Region.OnTravel`) are not bypassed in custom content.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the `BaseWeapon`/`BaseArmor`/`BaseClothing` model that owns the swing entry point.
- `uo-aos-item-properties` - the property containers (`AosAttribute`, `AosWeaponAttribute`, etc.) that the combat pipeline reads.
- `uo-magic-spells` - spell damage is fed into `AOS.Damage`.
- `uo-skills-stats-races` - the skill/stat/race modifiers that feed Anatomy, Tactics, Str, RaceBonus, etc.
- `modernuo-content-patterns` - canonical templates for weapon types and abilities.
- `modernuo-era-expansion` - the `Core.AOS` / `Core.SE` / `Core.ML` / `Core.SA` boundaries that gate damage formulas.
- `uo.stratics.com/content/aos/combatchanges.shtml` (offline reference) - the official AOS combat spotlight.
- `www.uoguide.com/Special_move` (offline reference) - the per-weapon primary/secondary special move matrix and the Publish 96 requirements.
- `www.uoguide.com/Champion_spawn` (offline reference) - the level scaling and reward tables.
