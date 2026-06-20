---
name: "uo-skills-stats-races"
description: "Use when working with the UO skill/stat/race system in ModernUO/RebirthUO servers - the 58 Skills, the 3 Stats (Str/Dex/Int), the 3 Races (Human/Elf/Gargoyle), the 720-point cap, 100/225/125/150 stat caps, skill gain mechanics, anti-macro, stat gain, the 7 expansion skill gates, and the PowerScroll/Scroll of Alacrity/Transcendence extension system. Use when adding a new skill, debugging why a skill does not gain, wiring a custom skill use, balancing a stat-gain path, or auditing per-era skill availability."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Skills, Stats, Races

## Overview

The UO character system is built on three pillars: 58 distinct skills (plus the 1 removed Enticement), 3 stats (Strength, Dexterity, Intelligence), and 3 playable races (Human, Elf, Gargoyle). Players distribute 720 skill points at character creation, gain skills by using them, and gain stats when skills with primary/secondary stat associations are used. The 12 expansions (None through EJ) progressively add skills and adjust the gain formulas.

The engine side is `Projects/UOContent/Skills/` with `SkillsInfo` (skill table + categories) and `SkillCheck` (gain logic). The data side is `Distribution/Data/skills.json` plus the `SkillName` enum. Stats live on `Mobile.Str`/`Dex`/`Int` with cap management in `Mobile` and the stat-mod system. Race data is in `Projects/UOContent/Misc/Race.cs`, `Heritage.cs`, and `RaceChangeGump.cs`.

This skill covers the 58 skill taxonomy, the skill categories per era, the skill gain pipeline, the stat gain pipeline, the three races and their racial abilities, the 720 / 225 / 125 / 150 cap system, the PowerScroll / Scroll of Alacrity / Scroll of Transcendence extension system, the Veteran Reward stat-cap extension, and the per-era skill gating.

## When to Use

- Adding a new skill to the system.
- Debugging why a skill does not gain (gain chance too low, anti-macro trigger, skill locked, wrong category).
- Wiring a custom action to a skill use and gain check.
- Adding a new character template (e.g. a "Custom Class" with 50/50/50 spread).
- Wiring a stat-gain window for a custom quest.
- Auditing the per-era skill roster for the current expansion target.
- Auditing the per-facet racial ability behavior (Elf +5 Energy cap, Gargoyle Berserk, Human Jack of All Trades).

Don't use for:

- Base entity model (use `uo-items-foundation`).
- Combat damage formulas (use `uo-combat-pipeline`).
- The map/facet/region system (use `uo-world-facets-regions`).

## The 58 Skills Taxonomy

Per `www.uoguide.com/Skills`, UO has 58 skills + 1 removed. They are organized into 6 categories. The category layout shifts with the active expansion: SE adds Bushido/Ninjitsu, ML adds Spellweaving, SA adds Mysticism/Throwing/Imbuing. The dynamic roster is built by `SkillsInfo.Configure()` based on the `Distribution/Data/skills.json` and the `Expansion`/`Core.<Era>` flags.

| Category | Skills |
|---|---|
| **Combat** | Archery, Chivalry (AOS), Fencing, Focus (SE), Mace Fighting, Parrying, Swordsmanship, Tactics, Wrestling, Bushido (SE), Throwing (SA) |
| **Healing** | Healing, Veterinary |
| **Magical** | Alchemy, Evaluating Intelligence, Inscription, Magery, Meditation, Necromancy (AOS), Resisting Spells, Spirit Speak, Spellweaving (ML), Mysticism (SA) |
| **Bardic** | Discordance, Musicianship, Peacemaking, Provocation |
| **Rogue** | Begging, Detecting Hidden, Hiding, Lockpicking, Poisoning, Remove Trap, Snooping, Stealing, Stealth, Ninjitsu (SE) |
| **Creatures & Sensing** | Anatomy, Animal Lore, Animal Taming, Camping, Forensic Evaluation, Herding, Taste Identification, Tracking |
| **Crafting** | Arms Lore, Blacksmithy, Bowcraft/Fletching, Carpentry, Cartography, Cooking, Glassblowing (?), Item Identification, Tailoring, Tinkering, Masonry, Basket Weaving, Imbuing (SA) |
| **Resource Gathering** | Fishing, Mining, Lumberjacking |

The 1 removed skill is **Enticement**, replaced by **Discordance** (the barding system). Old Enticement scrolls/items are still in the data but the skill is gone.

## Skill Table and Configuration

`Projects/UOContent/Skills/SkillsInfo.cs:133-141` is the `SkillInfo.Table` lookup. The table is filled by `SkillsInfo.Configure()` during `Configure()` phase. Each `SkillInfo` row holds:

- `Name` (the typed `SkillName` enum value).
- `Title` (cliloc for the skill title shown on the paperdoll).
- `StrScale` / `DexScale` / `IntScale` (how much the skill contributes to stat gain per 0.1 skill gained).
- `StatTotal` (multiplier for the stat-gain chance).
- `Primary` / `Secondary` (which stat the skill prefers).
- `Use` (whether the skill is in the active rotation; gates per-expansion).

The expansion gates work like this:

```csharp
// From SkillsInfo.cs (paraphrased)
if (Core.SE) AddUse(Bushido); AddUse(Ninjitsu);
if (Core.ML) AddUse(Spellweaving);
if (Core.SA) AddUse(Mysticism); AddUse(Throwing); AddUse(Imbuing);
```

The `Distribution/Data/skills.json` file is the data-driven source for the skill name, primary/secondary stat, and skill cap.

## Skill Gain Pipeline

Skill gain is gated by `SkillCheck.cs:8` (`Projects/UOContent/Skills/SkillCheck.cs`). Every action that uses a skill calls `CheckSkill(...)` which returns whether the action succeeded. The actual gain logic is a separate path:

```
SkillCheck.CheckSkill(attacker, skill, min, max)
 ├─ caller's check (success/miss)
 ├─ if success and not at cap and not locked:
 │   ├─ if not at GainFactor: gain 0.1 skill
 │   ├─ if at GainFactor: gain 0.1 + chance at +1
 │   └─ if at 100: PowerScroll-gated only
 └─ StatGainTick: chance per skill use to gain primary (75%) or secondary (25%) stat
```

The GainFactor defaults are in `Distribution/Configuration/modernuo.json` (e.g. `stats.gainDelay`, `skills.gainFactor`).

**Anti-macro**: A `NextSkillGainTime` (a UTC timestamp) is tracked on the `Mobile`. If a player uses the same skill twice within the `antiMacro` window (default 3 seconds), the second use is rejected for gain. This stops the "click-mining" exploit.

**Stat gain**: Per `www.uoguide.com/Stat`, a 1-in-20 chance of stat gain fires per skill advance. The primary stat gains 75% of the time when both primary and secondary are unlocked; if primary is locked, secondary gains 100%. `SkillInfo.StrScale`/`DexScale`/`IntScale` determine how much each skill contributes to stat gain on success.

The stat-gain cap is 125 per stat naturally, 150 with items (so items can boost a stat but combined stat total is capped at 150 per stat). The cumulative stat cap is 225 by default, extendable to 260 via veteran reward (6-month account: +5) and stat scrolls (1 per stat per scroll, +5 per Scroll of Valiant Commendation).

## Skill Categories and Per-Expansion Roster

`SkillsInfo.cs:8-121` declares the per-expansion max-index for each category. The intent is that pre-SE shards do not expose Bushido/Ninjitsu, pre-ML shards do not expose Spellweaving, pre-SA shards do not expose Mysticism/Throwing/Imbuing. The dynamic roster is rebuilt at `Configure()`.

The skills are stored in `Distribution/Data/skills.json` with the per-expansion `MinExpansion` flag on each entry. `SkillsInfo` reads the JSON at config time and uses the `Expansion` property to filter.

`Character Creation` (`Projects/UOContent/Misc/CharacterCreation.cs`) reads the active skill roster and blocks Bushido/Ninjitsu before SE, Mysticism/Throwing/Imbuing before SA, etc. `CharacterCreationSkillValidationTests` is the regression surface.

## The 3 Stats (Str / Dex / Int)

Per `www.uoguide.com/Stat`:

- **Strength** (Str): determines carry weight, melee damage, hit points.
- **Dexterity** (Dex): determines Stamina, and is important for skills like Snooping and Parrying.
- **Intelligence** (Int): determines Mana, and affects Magery-related skills.

Stat gain mechanics:

- **Stat Locks** (up arrow, down arrow, lock): control which stats can move. The lock symbol on the paperdoll pins the stat.
- **Stat Cap**: 125 per stat naturally. 150 with items. 225 cumulative naturally. 260 with Veteran Reward + Stat Scrolls.
- **Gain on Skill Advance**: 1-in-20 chance of a stat gain per skill-up. Primary is selected 75% of the time, secondary 25% of the time (when both are unlocked).
- **Training Strategy**: Players can grind one skill to raise a stat, then switch to a skill with the opposite primary/secondary to "draw down" the unwanted stat. The classic "mule trick" uses Evaluate Intelligence to gain Int, then Musicianship (primary Dex, secondary Int) to lower Dex/raise Int.

## The 3 Races

Per `www.uoguide.com/Races` and the engine's `Race.cs`:

| Race | Racial abilities | Source expansion |
|---|---|---|
| **Human** | Strong Back (+60 stone carry), Tough (+2 HP Regen), Workhorse (+1-2 logs/+1 ore), Jack of All Trades (20 base all skills, removed Publish 64 for LMC) | None (original) |
| **Elf** | Night Sight (always), Infused (+5 Energy cap, 75 total), Difficult to Track, Perception (detect hidden), Knowledge of Nature (rare resource bonus), Wisdom (+20 Mana) | ML |
| **Gargoyle** | Flying (mount-speed), Berserk (15% damage + 3% SDI per 20% HP lost, capped 60% weapon / 12% SDI), Master Artisan (Imbuing bonus), Deadly Aim (20 Throwing baseline, +5% hit), Mystic Insight (30 Mysticism baseline, +2 Mana Regen) | SA |

The race change flow:

- **Human -> Elf**: Elven Heritage quest.
- **Elf -> Human**: Human Heritage quest.
- **Human <-> Elf <-> Gargoyle**: Race Change Token (introduced with Gargoyle launch).
- **Heritage Tokens** in `Projects/UOContent/Engines/ML Quests/HeritageTokenGump.cs` provide quest-based and promotional rewards that bundle multiple Heritage items.

The `RaceDefinitions` enum and the racial-ability hooks are in `Race.cs`. The `Is` checks (`Mobile.Race == Race.Elf`) are how content code branches on race.

## The 720-Point Cap

A new character can place 720 skill points across the 58 skills, each skill capped at 100. Power Scrolls (and the rare Scroll of Transcendence) raise the cap to 105, 110, 115, or 120 per skill. The active cap is stored on `Skill.Cap`.

`PowerScroll` is the classic 5-point bonus scroll; the drop sources are Champion Spawns (Felucca-only), Doom artifacts, peerless keys, and various event items. `ScrollOfAlacrity` boosts gain rate (not the cap) and lasts 30 minutes of real time. `ScrollOfTranscendence` is a stat-skill cap scroll awarded for champion kills (Felucca has 2x potency).

The Veteran Rewards program (`Projects/UOContent/Engines/RewardSystem.cs`) grants stat-cap extensions and other goodies at 6-month account-age intervals. The ML-era half-level stat reward (`+5` to the cumulative cap) is gated by `Expansion.ML`.

## Skill Use and CheckSkill

Every skill use path calls `SkillCheck.CheckSkill(Mobile, SkillName skill, double min, double max)` to gate success. The min/max define the difficulty band:

- 0-30: easy (always succeeds at 0, often at 30).
- 50: medium.
- 80-100: hard.
- > 100: usually impossible without PowerScroll bonuses.

The skill gain chance is a function of `(max - skill)`: if `max` is close to `skill`, the gain chance is high; if `max` is much higher, the gain chance is low. This is the "training wall" mechanic.

`SkillCheck.cs:21-33` and `SkillCheck.cs:94-200` document the per-skill gain table. The modern table:

- Skill range 0-30: 1-in-2 (50%) chance of gain per use.
- 30-50: 1-in-3 (33%).
- 50-70: 1-in-5 (20%).
- 70-90: 1-in-10 (10%).
- 90-100: 1-in-20 (5%).

The Publish-45 update (and ML `GainSkillObjectiveRuntimeTests`) introduced accelerated-skill windows for New Haven quest chains. Each accelerated window has a 50.0 real-skill objective that can be completed in 15 minutes of real time. The window is removed on completion or cancellation.

## Common Pitfalls

1. **Calling `Mobile.Skills[skill].Base += 0.1` directly.** This bypasses the gain window, the anti-macro timer, and the stat-gain pipeline. Use `SkillCheck.CheckSkill` and the `Skill.UseSkill` path instead.
2. **Forgetting the skill lock check.** A locked skill (`Mobile.Skills[skill].Lock == SkillLock.Locked`) does not gain and does not affect the success formula.
3. **Setting `Core.Expansion = Expansion.ML` without updating the skill roster.** The dynamic SkillsInfo must be rebuilt; this happens automatically on `Configure()` restart.
4. **Hardcoding skill max values.** PowerScroll bonuses are per-skill; the engine reads `Skill.Cap` and the `SkillCheck` path respects it. Hardcoding 100 breaks PowerScroll gameplay.
5. **Forgetting the `NextSkillGainTime` reset on death/logout.** Anti-macro should be a per-session or per-real-time window, not a per-death window. The default is real-time.
6. **Using the wrong stat as the primary.** `Magery`'s primary is `Intelligence`, `Tactics`' primary is `Strength`, `Swordsmanship`'s primary is `Strength`. The skill-table row is the source of truth; overriding it in content code is a regression.
7. **Setting `Mobile.Str` above 125 without an item basis.** Items can boost a stat up to 150; above 150 the stat is a bug. The cap check is in `Mobile` setters and `GainStat`.
8. **Bypassing `Race` checks in `Region` hooks.** The Elf +5 Energy cap and Gargoyle Berserk are part of `Mobile.GetMaxResistance` and `BaseCreature.OnDamage`; setting them via race hooks is correct, mutating `Mobile.Str` is not.
9. **Forgetting that `Lock` is per-skill, not global.** A player can lock a single skill and gain another; locking all skills stops gain entirely.
10. **Setting `Core.SE = true` without checking that SE-only skills are registered.** Bushido/Ninjitsu registration is gated by `Core.SE`; setting the flag without re-running `Configure()` leaves the skill table inconsistent.

## Common Recipes

### Adding a New Skill

The skill enum is in `Server.SkillName` (in `Projects/Server/Mobiles/Mobile.cs` or a dedicated file). Adding a new skill is intrusive: the enum, the `SkillInfo` table, the `SkillsInfo.Configure()` registration, the `skills.json` data, and any `SkillCheck` per-skill gain all need updates. Most new skills are added only at major releases; the `Expansion`-gated `AddUse` pattern is the typical extension path.

```csharp
// 1. Add to SkillName enum
public enum SkillName
{
    ...
    MyNewSkill = 57,
}

// 2. Add to skills.json
{ "id": 57, "name": "My New Skill", "primary": "Intelligence", "secondary": "Strength", "minExpansion": "SA" }

// 3. Register in SkillsInfo.Configure
new SkillInfo(SkillName.MyNewSkill, 1080123, 1098012, 0, 0, 0, 0, SkillCat.Magical)
    .Register();
```

### Wiring a Custom Skill Use

```csharp
// In the skill's Use() method
public override void Use(Mobile from)
{
    if (SkillCheck.CheckSkill(from, SkillName.MyNewSkill, 0.0, 100.0))
    {
        // success
        from.SendMessage("You succeed!");
    }
    else
    {
        from.SendMessage("You fail.");
    }
}
```

### Adding a Race-Gated Bonus

```csharp
// In Mobile.GetMaxResistance or similar
public override int GetMaxResistance(ResistanceType type)
{
    int baseVal = base.GetMaxResistance(type);
    if (Race == Race.Elf && type == ResistanceType.Energy) baseVal = Math.Min(75, baseVal + 5);
    return baseVal;
}
```

### Wiring a PowerScroll Bonus

```csharp
// PowerScroll.OnDoubleClick or similar
public override void OnDoubleClick(Mobile from)
{
    if (IsChildOf(from.Backpack) && from.Skills[Skill].Lock != SkillLock.Locked)
    {
        from.Skills[Skill].Cap = 120;
        Delete();
    }
}
```

## Verification Checklist

- [ ] `dotnet build` succeeds.
- [ ] New skill: `SkillName` enum updated, `skills.json` updated, `SkillsInfo.Configure` registers it with the right category and scales, `SkillCheck` gain table covers the new skill.
- [ ] Skill gain is gated through `SkillCheck.CheckSkill` (not a direct `Base` mutation).
- [ ] `Anti-macro` window is respected: rapid-fire skill uses do not grant free gains.
- [ ] Stat gain fires at 1-in-20 per skill advance, with the right primary/secondary ratio.
- [ ] Per-era skill availability is gated: pre-SE shards do not expose Bushido/Ninjitsu, pre-ML shards do not expose Spellweaving, pre-SA shards do not expose Mysticism/Throwing/Imbuing.
- [ ] Race-specific bonuses are wired through `Race`/`Heritage` (not direct stat mutations).
- [ ] PowerScroll application respects `Skill.Cap` and `Lock`.
- [ ] Stat cap checks: 125 natural, 150 item, 225 cumulative natural, 260 with veteran + scrolls.
- [ ] Stat locks are respected on gain and on cap enforcement.
- [ ] Veteran Reward half-level stat bonus fires once on the 6-month milestone.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-combat-pipeline` - Anatomy, Tactics, Swordsmanship, etc. are the combat skills that feed the damage formula.
- `uo-magic-spells` - Magery, Necromancy, Chivalry, Mysticism, etc. are the magic skills; their skill-check uses feed into the gain pipeline.
- `uo-items-foundation` - skill scrolls, totems, and reward items.
- `uo-aos-item-properties` - `AosSkillBonuses` and item-based skill boosts.
- `uo-world-facets-regions` - the regional hooks for travel, guards, and respawns that influence which skills are trainable where.
- `modernuo-content-patterns` - canonical templates for new skills.
- `modernuo-era-expansion` - per-expansion skill roster and the `Core.<Era>` gate logic.
- `www.uoguide.com/Skills` (offline reference) - the canonical 58-skill taxonomy and category list.
- `www.uoguide.com/Stat` (offline reference) - the per-skill primary/secondary stat table and cap mechanics.
- `www.uoguide.com/Races` (offline reference) - the per-race racial-ability table.
