---
name: "uo-magic-spells"
description: "Use when working with the UO magic system in ModernUO/RebirthUO servers - the Spell base class lifecycle, 8 Magery circles, Necromancy/Chivalry/Bushido/Ninjitsu/Spellweaving/Mysticism schools, reagent mechanics, CastTimer flow, SpellHelper travel/damage/indirect-target validation, Karma/Tithing requirements, and content-gating per era. Use when adding a new spell, debugging why a spell fizzles, wiring AI to cast spells, or extending the spell model for SA/ToL."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Magic & Spells

## Overview

The UO magic system spans six distinct spell schools plus a unified `Spell` base class that owns the cast lifecycle. The engine treats every spell as a state machine driven by `Timer`: an initial cast phase (animation, reagents consumed at the right moment), a CastTimer that delays the actual effect (or "delayed damage"), and an `OnCast`/`Target`/`OnDisturb` callback set.

The `Spell` base class lives in `Projects/UOContent/Spells/Base/Spell.cs` and `SpellHelper` in `Projects/UOContent/Spells/Base/SpellHelper.cs`. Each school is its own folder under `Projects/UOContent/Spells/`: `First` through `Eighth` (Magery circles), `Necromancy/`, `Chivalry/`, `Ninjitsu/`, `Bushido/`, `Spellweaving/`, `Mysticism/`. The static `Spells/Initializer.cs` registers every spell by ID during `Configure()`.

This skill covers the Spell base class, the 8 Magery circles plus the 5 expansion-introduced schools, reagent and focus consumption, the cast-timer pattern, SpellHelper's target/damage/travel validation, AI caster integration, and the era-gates that determine which schools are even available on a given server. The combat-damage formulas that consume these spells live in `AOS.Damage` and are covered by `uo-combat-pipeline`.

## When to Use

- Adding a new spell to any school.
- Debugging why a spell fizzles (reagents missing, mana short, karma/tithing wrong, focus level too low, paralysis/frozen, etc.).
- Wiring a BaseCreature AI to cast a specific spell.
- Implementing delayed-damage spells (Lightning, Harm, Magic Arrow, Pain Spike, Strangle, Wither).
- Implementing field spells (Fire Field, Poison Field, Energy Field, Paralyze Field, Wall of Stone).
- Implementing summon spells (Blade Spirits, Energy Vortex, Summon Elemental, Summon Daemon, Vengeful Spirit, Arcane Fiend, Summon Fey, Wildfire, Rising Colossus).
- Adding new transformation spells (Polymorph, Wraith Form, Horrific Beast, Lich Form, Vampiric Embrace).
- Auditing whether a new content branch correctly handles pre-AOS vs AOS vs SE vs ML spell behavior.

Don't use for:

- Base item/entity model (use `uo-items-foundation`).
- Item properties consumed by spells (use `uo-aos-item-properties`).
- Combat damage formulas and weapon swing pipeline (use `uo-combat-pipeline`).
- Skill gain and stat association (use `uo-skills-stats-races`).

## The Spell Base Class

`Projects/UOContent/Spells/Base/Spell.cs:17-83` defines the abstract `Spell` class. Every concrete spell extends it and overrides a small set of methods.

Key fields and properties:

| Member | Purpose |
|---|---|
| `Caster` | The `Mobile` casting the spell. Set in constructor. |
| `Item` | The `ISpellbook` or `Runebook` or `Wand` source (null for scroll/wand paths). |
| `Scroll` | The `SpellScroll` if the source is a scroll. |
| `CastSkill` / `DamageSkill` | The skill checked at cast (`SkillName.Magery` for default) vs at impact. |
| `RequiredSkill` | Minimum skill to attempt the cast. |
| `Mana` / `ManaScale` | Base mana cost and per-spell scaling. |
| `CastDelayBase` | Animation cast time, in tenths of a second (0.25-1.5s typical). |
| `State` | `None`, `Casting`, `Casted`, `Fizzling`, `Disturbed`. |
| `Circle` | The Magery circle 1-8, or school-specific tier. |
| `Reagents` | Per-spell reagent list (Magery/Necro) or focus. |

The lifecycle (paraphrased from `Spell.cs:17-83` and the cast timer block at `Spell.cs:572-584`):

```
Spell.Cast()
 ├─ alive / existing cast / form blocks / frozen / next spell time / feature flag
 ├─ CheckDisturb: target lock, paralysis, mana shield
 ├─ mana availability
 ├─ Caster.CheckSpellCast + CheckCast + Region.OnBeginSpellCast
 ├─ reveal, mantra, animation, clear hands
 ├─ CastTimer.Start()   (delay = CastDelayBase)
 └─ OnCast effect
     ├─ reagents + mana + fizzle check
     ├─ consume scroll/wand/mana
     ├─ SingleTarget/LocationTarget/PerSecond logic
     └─ damage/targeting through SpellHelper/AOS/Region hooks
```

`SpellHelper` (`Projects/UOContent/Spells/Base/SpellHelper.cs`) provides reusable validation utilities: `GetCenterPoint`, `FindValidSpellLocation`, `TravelCheckType` matrix, `AdjustDamage` for scaling, `CanRevealCasterOnCast`, and the AoS damage hooks used by delayed-damage spells.

## The Eight Magery Circles

The classic Magery school is the bedrock of UO magic. Each circle takes more skill, time, and mana than the previous, and the spell ID range is fixed across the codebase. `Spells/Initializer.cs:21-178` is the source-of-truth registration.

| Circle | Mana cost | Typical skill range | Folder | Sample spells |
|---|---|---|---|---|
| 1st | 4 | 0-30 | `First/` | Clumsy, Create Food, Feeblemind, Heal, Magic Arrow, Night Sight, Reactive Armor, Weaken |
| 2nd | 6 | 30-50 | `Second/` | Agility, Cunning, Cure, Harm, Magic Trap, Remove Trap, Protection, Strength |
| 3rd | 9 | 50-65 | `Third/` | Bless, Fireball, Magic Lock, Poison, Telekinesis, Teleport, Unlock, Wall of Stone |
| 4th | 11 | 65-75 | `Fourth/` | Arch Cure, Arch Protection, Curse, Fire Field, Greater Heal, Lightning, Mana Drain, Recall |
| 5th | 14 | 75-85 | `Fifth/` | Blade Spirits, Dispel Field, Incognito, Magic Reflection, Mind Blast, Paralyze, Poison Field, Summon Creature |
| 6th | 20 | 85-95 | `Sixth/` | Dispel, Energy Bolt, Explosion, Invisibility, Mark, Mass Curse, Paralyze Field, Reveal |
| 7th | 40 | 95-100 | `Seventh/` | Chain Lightning, Energy Field, Flamestrike, Gate Travel, Mana Vampire, Mass Dispel, Meteor Swarm, Polymorph |
| 8th | 50 | 100 | `Eighth/` | Earthquake, Energy Vortex, Resurrection, Summon Air/Earth/Fire/Water Elemental, Summon Daemon |

The eight Reagents are the cornerstone of Magery: `Black Pearl`, `Bloodmoss`, `Garlic`, `Ginseng`, `Mandrake Root`, `Nightshade`, `Spider's Silk`, `Sulfurous Ash`. Every Magery spell has a 1-4 reagent combination; the cost is consumed at `OnCast`, not at cast-start. `Loot` generates reagents in `BaseReagent` derivatives and shop vendors stock them as `Reagent` items.

`[CommandProperty]` on a spell's fields is rare; spell parameters are usually fixed in the source. The exception is AI-configurable spells on `BaseCreature` (e.g. `BaseCreature.AI_Spell`).

## Necromancy (AOS)

Necromancy was introduced with `Age of Shadows` and lives in `Projects/UOContent/Spells/Necromancy/`. It uses the same 8 reagents plus `Pig Iron`, `Batwing`, `Grave Dust`, `Daemon Blood`, `Nox Crystal` (5 necromancy-specific reagents). The school is gated by `Core.AOS`.

The defining feature is that Necromancy draws power from `Spirit Speak` instead of `Evaluate Intelligence`. `Spirit Speak` is the support skill; casting Necro spells without it has a base rate, casting with it scales duration and damage.

Key spell families (from `uo.com/wiki` Necromancy reference):

| Spell | Effect |
|---|---|
| `Curse Weapon` | Life-drain on the caster's weapon; 50% of damage healed. |
| `Pain Spike` | Direct damage + brief stamina loss; bypasses armor. |
| `Corpse Skin` | Reshuffle target's elemental resists. |
| `Evil Omen` | Amplifies the next hostile strike (+25% damage, +1 poison, or -50% resist). |
| `Blood Oath` | Damage mirror between caster and target. |
| `Wraith Form` | Transformation: walk-through-people, +15 Phys, -5 Fire/Energy, mana leech. |
| `Mind Rot` | +25% mana cost to target. |
| `Summon Familiar` | Horde Minion → Shadow Wisp → Dark Wolf → Death Adder → Vampire Bat. |
| `Horrific Beast` | +20 HP Regen, +25% melee damage, base hand 5-15. |
| `Animate Dead` | Up to 3 uncontrolled undead followers (no follower slot). |
| `Poison Strike` | AoE poison damage in 2-tile radius. |
| `Wither` | AoE cold damage, scales with karma gap. |
| `Strangle` | Stamina-scaled poison DoT. |
| `Lich Form` | +1.3 mana/sec, +10 cold/poison, -10 fire, -1 HP/2s. |
| `Exorcism` | Relocates ghosts in champion spawn regions (requires 100 Spirit Speak). |
| `Vengeful Spirit` | Revenant summon, 3 control slots. |
| `Vampiric Embrace` | 20% life drain, immune to poison 1-4, +25% damage from Undead Slayers. |

Necro transformations (Wraith, Lich, Vampiric, Horrific Beast) interact with `Polymorph`-style form locks and the `CheckStatTimers` system. Cancelling them in favor of another transformation is a documented `SkillCheck` decision (`docs/server-engine-knowledge-base.md:601-613`).

## Chivalry (AOS)

The Paladin school, gated by `Core.AOS`. Uses **Tithing Points** instead of reagents: 1 gold donated to a shrine = 1 tithing point, capped at 100,000. Karma affects both duration and power of Chivalry spells. Lives in `Projects/UOContent/Spells/Chivalry/`.

Ten spells, ordered roughly by required skill:

| Spell | Effect |
|---|---|
| `Close Wounds` | Self/ally heal 7-39 HP. |
| `Cleanse by Fire` | Cures poison. |
| `Remove Curse` | Removes curse effects. |
| `Consecrate Weapon` | +damage vs target's weakest resist, 3-11s. |
| `Sacred Journey` | Single-target teleport equivalent to Recall (subject to combat restriction). |
| `Divine Fury` | +swing speed, +hit chance, +damage, -defense. |
| `Dispel Evil` | Damage summoned evil creatures; damages Necromancers in Horrid Beast/Lich/Vampire/Wraith forms. |
| `Enemy of One` | +50% weapon damage to one creature type; other types +100%. |
| `Holy Light` | AoE energy damage 8-24 HP. |
| `Noble Sacrifice` | Heal all nearby 9-24 HP, caster drops to 1 HP/Stam/Mana. |

`Faster Casting` cap for Chivalry is **4** unless `Magery >= 70.0`, then 2. This is a school-specific property on the Chivalry spell base, not a content override.

## Ninjitsu & Bushido (SE)

Two SE schools gated by `Core.SE`. Both use a Focus level (0-5 in Sanctuary, capped at 6 in ML) and a skill-level minimum (typically 50.0). Bushido has the Samurai moves; Ninjitsu has the Ninja toolkit.

Bushido spells live in `Projects/UOContent/Spells/Bushido/`: `Confidence`, `Counter Attack`, `Evasion`, `Honorable Execution`, `Lightning Strike`, `Momentum Strike`, `Peace`, `Sanctuary`, `Stagger`. Ninjitsu spells live in `Projects/UOContent/Spells/Ninjitsu/`: `Animal Form`, `Backstab`, `Death Strike`, `Focus Attack`, `Ki Attack`, `Mirror Image`, `Shadow Jump`, `Surprise Attack`.

Spell focus is the SE mechanic: a buff icon stacks as the player gains hits, capping at a school-specific max. The `BushidoFocusLevel` and `NinjitsuFocusLevel` are tracked in `Mobile`/`BaseCreature` and used by spell entry-point validation.

## Spellweaving (ML)

ML's solo school, gated by `Core.ML`. Spells live in `Projects/UOContent/Spells/Spellweaving/`. Key features:

- Spells cost a percentage of maximum mana (10-30%) rather than a fixed amount.
- `Arcane Circle` is required for some spells: 4+ casters (or 2+ at higher tiers) with Spellweaving in a 3-tile radius, providing +1 focus.
- The school is **quest-gated** for the player: must complete the Heartwood or Sanctuary Arcanist quest to acquire the `SpellweavingBook` and the `PlayerContext.Spellweaving` context flag.
- `ArcanistSpell.CheckCast` enforces the context flag at cast time.
- Focus cap is 5 normally, 6 in Sanctuary.

Spellweaving spells include `Arcane Circle`, `Attune Weapon`, `Dryad Allure`, `Essence of Wind`, `Ethereal Voyage`, `Gift of Life`, `Gift of Renewal`, `Immolating Weapon`, `Mana Drain`, `Nature's Fury`, `Reaper Form`, `Rising Colossus`, `Summon Fey`, `Summon Fiend`, `Thunderstorm`, `Wildfire`, `Word of Death`, `Arcane Empowerment`.

`Wildfire` is a tracked field-spell with a `Mobile` removal list; it ticks AoE fire damage around the spell's center.

## Mysticism (SA)

The Gargoyle school, gated by `Core.SA`. Spells live in `Projects/UOContent/Spells/Mysticism/`. Gargoyles have a baseline 30.0 Mysticism skill, which is the only skill with a race-specific starting value.

Mysticism spells include `Animated Weapon`, `Banish Evil`, `Bombard`, `Cleansing Winds`, `Eagle Strike`, `Enchant`, `Gate Travel` (SA version), `Hail Storm`, `Healing Stone`, `Mass Sleep`, `Nether Blast`, `Nether Cyclone`, `Purge Magic`, `Rising Colossus`, `Sleep`, `Spell Plague`, `Spell Trigger`, `Stone Form`, `Thunder`.

`Spell Plague` is the iconic "anti-caster" spell in this school: it bounces spell disruptions between targets. The implementation follows the `SpellHelper.IndirectDamage` pattern with the spell's specific targeting rule.

## Reagents, Scrolls, and Foci

Reagents (Magery/Necro/Chiv) and Foci (SE/ML/SA) are consumed at `OnCast`. The `ConsumeReagent` / `ConsumeReagentsFromList` helpers in `SpellHelper` walk the caster's reagent bag (or the `BaseReagent` items in their backpack) and consume one of each needed. Without reagents, the spell fizzles. Wands and `Wizard's Satchel` route through different consumption paths.

Spell scrolls (the `SpellScroll` item) are the standard way to teach a spell: drag-scroll-to-spellbook adds the spell, double-click from a spellbook executes the cast. `Inscription` produces scrolls from `BlankScroll` plus reagents.

Spellbooks are typed per school: `Spellbook` (Magery), `NecromancerSpellbook`, `BookOfChivalry`, `BookOfNinjitsu`, `BookOfBushido`, `SpellweavingBook`, `MysticBook`. Each holds a bit-mask of learned spell IDs; the spell book gump emits a grid of `SpellIcon` controls.

## CastTimer and Delayed Damage

Many damage spells apply their effect on a **delay** rather than instantly. `Lightning` (4th circle), `Harm` (2nd), `Magic Arrow` (1st), `Pain Spike`, `Mind Rot`, and the Necro transformations' `Dismount`/`Bleed Attack` follow the delayed-damage pattern. The engine uses `Timer.DelayCall` with the spell's `CastDelayBase`, then applies damage in the timer callback. The player's client shows a "spell-in-flight" particle; the actual damage is applied server-side after the delay.

`AOS.Damage` (covered in `uo-combat-pipeline`) reads the delayed damage and applies elemental splits. `SpellHelper.IndirectDamage` is the path for spells that have a primary target plus splash damage (e.g. `Poison Strike`).

## Field Spells (Persistent AoE)

`Fire Field`, `Poison Field`, `Energy Field`, `Paralyze Field`, `Wall of Stone` are persistent objects spawned in the world. The Spell's `OnCast` instantiates a `FieldItem` (or `InternalItem` for Paralyze Field) that does the actual `Damage` or paralyze in its `OnTick`. The spell target is a `Point3D` rather than a `Mobile`. The fields decay after a school-specific duration (3-30 seconds).

The `Item` lifecycle of a field is the same as any other item: `World.AddEntity`, decay timer, on-expire `Delete()`. The hot path is the per-tick `Damage` call which is a `Mobile.Damage` against the field's `Owner` caster.

## Summon Spells

`Summon Creature` (5th), the 4 elemental summons (8th), `Summon Daemon` (8th), `Energy Vortex` (8th), `Blade Spirits` (5th), `Summon Familiar` (Necro), `Summon Fey` (Spellweaving), `Summon Fiend` (Spellweaving), `Vengeful Spirit` (Necro), `Rising Colossus` (Spellweaving + Mysticism), `Wildfire` (Spellweaving field), `Animated Weapon` (Mysticism). The pattern is:

1. Validate cast prerequisites (skill, focus, mana, reagents, gate).
2. Spawn the `BaseCreature` subclass (e.g. `EnergyVortex`).
3. Set the caster as `ControlMaster`, set `ControlSlots`, set `ControlOrder = AttackTarget` (if targeted), set `BardProvoked = false`, set `BardPacified = false`.
4. Move the summon to the target location.
5. If needed, set `Combatant` to the spell target.
6. Use a `Timer` to expire the summon after its duration (most summons have a built-in `DeleteTimer`).

`Summon Fey` is ML content and lives in `Projects/UOContent/Spells/Spellweaving/SummonFeySpell.cs`. The follow-up quest chain (`FriendOfTheFey`, `TokenOfFriendship`, `Alliance`) is in `Projects/UOContent/Engines/ML Quests/`.

## AI Casting on BaseCreature

`BaseAI` (`Projects/UOContent/Mobiles/AI/BaseAI/BaseAI.cs`) calls `CastSpell()` when the AI type permits. The order is determined by `BaseCreature.SpellList` plus priority helpers like `MostDamagingSpell`, `UseAttackSpell`, `UseDefenseSpell`. The AI respects the spell's `RequiredSkill` and the caster's current mana, reagents, and `NextSpellTime`.

To wire a new spell to a creature:

1. Add the `Spell` class to the matching folder.
2. Register it in `Initializer.cs`.
3. Add the spell to the creature's `SpellList` (or use the `BaseCreature.SpellManifest`).
4. Verify the `Cast` pipeline in `BaseAI` invokes the new spell (most do via reflection over `SpellList`).

`uostratics.com/content/skills/` covers the Magery/Necro/Chiv spell lists for each school and is a good reference for the "what does this spell do" lookup when wiring AI.

## Era Gating and the Spell Pipeline

The pre-AOS spell model is a flat random damage path; `AOS.Damage` only runs if `Core.AOS`. The post-SE adjustment to `CastDelayBase` (`Core.SE ? 250 : Core.AOS ? 500 : 1000`) makes the game feel snappier on SE+ shards.

`ML` and `SA` introduced new schools that the engine must register conditionally. The `Initializer.Configure()` method has guards like `if (Core.SE) Register(N, typeof(BushidoXxxSpell))` for SE-only schools. ML/SA-only spells follow the same pattern. Removing `Core.ML` from a shard should make the Spellweaving school uncastable even if the spell is registered.

`SpellState` is reset on `Map` change and on death. Transformations (Wraith, Lich, Vampiric, Horrific Beast) interact with the `Polymorph` and `Incognito` form-lock mechanics; switching forms requires a `Magery > 38.1` check (Incognito) or `Magery > 66.1` (Polymorph).

## Common Pitfalls

1. **Consuming reagents at cast-start, not at OnCast.** The engine pattern is to consume at `OnCast` so the reagents return if the cast is interrupted. The `Disturb` path must refund reagents.
2. **Forgetting the `NextSpellTime` reset.** After a cast, the caster has a small window during which they cannot cast again. The `NextSpellTime` is set in the Spell constructor and must be checked in custom cast paths.
3. **Setting `CastDelayBase` lower than the timer granularity.** The engine uses `Timer` with ~250ms granularity. Setting `CastDelayBase` to 0.1s effectively still resolves to 250ms.
4. **Not handling `AOS.Damage` returns in damage spells.** `AOS.Damage` returns the actual damage applied. Delayed-damage spells should record the actual damage (not the pre-resist value) for skill-gain calculations.
5. **Using `SpellHelper.Damage` instead of `AOS.Damage` on AOS+ shards.** `SpellHelper.Damage` is the pre-AOS path; `AOS.Damage` is the right call for AOS+.
6. **Forgetting the respec / pulse requirements for transformations.** `Wraith Form`, `Lich Form`, `Vampiric Embrace` and `Horrific Beast` apply a per-tick effect (`-1 HP/2s` for Lich, etc.). The timer must be cleaned up in `OnAfterDelete`/`OnDeath`/`OnLogout`.
7. **Registering a spell for a school that is not gated.** Registering `MysticismSpell` on a pre-SA shard is allowed by the code but the `RequiredExpansion` check in `Spell` rejects casts. This leaks OPL rows and a `[AddSpell` admin command. Always gate at the registration level too.
8. **Target validation missing for AoE spells.** `Fire Field`, `Wall of Stone`, `Poison Field` need a `Point3D` target. The cast must call `Caster.GetTarget()` and validate the target is a legal location (`SpellHelper.FindValidSpellLocation`).
9. **Bypassing `CheckCast` on custom mounts.** `Mounted` blocks most spells, but some allow mounts (Magery with `SpellChanneling` on the weapon, some ML spells). The check is per-spell.
10. **Setting `Scroll` and `Item` both null when the source is a wand.** Wand path consumes the wand's `Charges` and uses a fixed CastDelayBase; the Item/Scroll are null and the `Disturb` path must not refund reagents.

## Common Recipes

### Adding a New Magery Spell

```csharp
// Projects/UOContent/Spells/Fifth/MyNewSpell.cs
public class MyNewSpell : MagerySpell
{
    public override SpellCircle Circle => SpellCircle.Fifth;
    public override double CastDelayBase => 1.5;  // 1.5 seconds

    [Constructible]
    public MyNewSpell(Mobile caster, Item scroll) : base(caster, scroll) { }

    public override void OnCast()
    {
        if (CheckSequence())
        {
            Caster.Mana -= Mana;
            Caster.PlaySound(0x1F7);
            // damage/target/effect
        }

        FinishSequence();
    }
}
```

Register in `Initializer.cs`:

```csharp
Register(48, typeof(MyNewSpell)); // next free ID in Fifth circle
```

Add a `SpellScroll` (auto-generated by the registration), define a `BaseReagent`-equivalent, and run the affected `SpellRegistration` tests.

### Wiring a BaseCreature to Cast

```csharp
// In the BaseCreature subclass constructor or via SpellList
SpellList.Add(8, typeof(EnergyBoltSpell));    // 6th circle
SpellList.Add(31, typeof(FireballSpell));     // 3rd circle
```

The AI cycle in `BaseAI.Think` calls these when the creature has line of sight to its target and the right `NextSpellTime`.

### Delayed Damage

```csharp
public override void OnCast()
{
    if (CheckSequence())
    {
        Timer.DelayCall(TimeSpan.FromSeconds(0.5), () =>
        {
            if (deleted) return;
            int damage = Utility.RandomMinMax(15, 25);
            AOS.Damage(target, Caster, damage, 0, 0, 0, 0, 100); // 100% energy
        });
    }
    FinishSequence();
}
```

### Field Spell

```csharp
public override void OnCast()
{
    if (CheckSequence())
    {
        var p = SpellHelper.GetSurfaceTop(Caster.Location);
        for (int i = -2; i <= 2; i++)
        for (int j = -2; j <= 2; j++)
        {
            var loc = new Point3D(p.X + i, p.Y + j, p.Z);
            if (!SpellHelper.AdjustField(ref loc, Caster.Map, 12, false))
                continue;
            new FireFieldItem(Caster, loc, Caster.Map, TimeSpan.FromSeconds(10));
        }
    }
    FinishSequence();
}
```

`FireFieldItem` (or equivalent) is a typed internal `Item` that does the per-tick damage and the visual.

## Verification Checklist

- [ ] `dotnet build` succeeds.
- [ ] Spell is registered in `Initializer.Configure()` with the correct ID slot (verify the ID is unique and the school's gate is honored).
- [ ] `OnCast` calls `CheckSequence()` first.
- [ ] Reagents are consumed inside `OnCast` (post-`CheckSequence`), not in the constructor.
- [ ] Delayed-damage spells use `Timer.DelayCall` and respect `deleted`.
- [ ] Transformations set up a per-tick timer in `OnCast` and cancel it on `OnAfterDelete`, `OnDeath`, and `OnLogout`.
- [ ] AI casting respects `NextSpellTime`, `NextMovement`, and `NextSound` in the cast site.
- [ ] For SA/ML/SE schools, the spell's `RequiredExpansion` and the registration gate are both present.
- [ ] Pre-AoS shards do not register or expose the spell.
- [ ] For quest-gated schools (Spellweaving), the spell's `CheckCast` requires the player's `PlayerContext.Spellweaving` flag.
- [ ] For Chivalry, the spell's mana cost is `0` (it costs Tithing instead) and `RequiredTithing` is the right value.
- [ ] For transformation spells, the form is removed if the player polymorphs or transforms again.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the `SpellScroll`, `Spellbook`, and reagent item models.
- `uo-aos-item-properties` - `SpellDamage`, `CastSpeed`, `CastRecovery`, `LowerManaCost`, `LowerRegCost`, `MageWeapon`, `MageArmor` consumed by the spell pipeline.
- `uo-combat-pipeline` - the `AOS.Damage` formula that consumes spell damage.
- `uo-skills-stats-races` - the SkillCheck mechanic and stat-gain engine that spell casts feed into.
- `modernuo-content-patterns` - canonical templates for spell classes.
- `modernuo-era-expansion` - era gate rules for SE/ML/SA spell registration.
- `www.uoguide.com/Magery_Spells` (offline reference) - per-circle mana cost and school list.
- `www.uoguide.com/Skills` (offline reference) - Magery and the 5 magic schools in the skill taxonomy.
- `uo.com/wiki/ultima-online-wiki/skills/necromancy` and `/chivalry` (offline reference) - per-spell mechanics, reagents, and skill requirements.
