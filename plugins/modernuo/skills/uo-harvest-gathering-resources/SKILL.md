---
name: "uo-harvest-gathering-resources"
description: "Use when working with the UO resource gathering system in ModernUO/RebirthUO servers - the HarvestSystem base class, Mining, Lumberjacking, Fishing, vein tables, BonusHarvestResource, RandomizeVeins, Elf respawn-reduction, Ter Mur sub-resources (Sand/Granite/Quality Gems), HarvestTarget and HarvestTimer, RaceBonus, and the ML harvest branches. Use when adding a new harvest system, adjusting a vein table, debugging why a player does not get a colored resource, wiring an Elf bonus, or auditing per-era resource parity."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Harvest & Gathering Resources

## Overview

The UO resource gathering system is the entry point to the crafting pipeline: a player goes to a mountain, a tree, or a body of water, uses a tool (pickaxe, axe, fishing pole), and gets a `BaseResource` (ore, wood, fish) that the crafting system consumes. The engine treats every harvest system (Mining, Lumberjacking, Fishing) as a subclass of `HarvestSystem` with shared `HarvestDefinition`, `HarvestVein`, `BonusHarvestResource`, and `MutateEntry` mechanics.

The engine code lives in `Projects/UOContent/Engines/Harvest/`. The `Core/HarvestSystem.cs` is the abstract base, `Core/HarvestDefinition.cs` holds the vein table and bonus-resource table, `Core/HarvestVein.cs` defines a single vein row. The concrete subclasses are `Mining.cs`, `Lumberjacking.cs`, `Fishing.cs`. Per the `mondains-legacy-content-matrix.md:74`, the ML-era harvest branches include SE/ML mining gem gates, ML lumber wood types, ML-only reveal behavior, and the elf respawn reduction.

This skill covers the `HarvestSystem` lifecycle, the per-system definitions (Mining/Lumber/Fishing), the vein-table construction, the bonus-resource mechanic, the Ter Mur sub-resources (Sand for glass, Granite for masonry, Quality Gems for jewelcrafting), the Elf racial bonus, the harvest per-tick flow (`HarvestTarget` + `HarvestTimer`), the `RaceBonus` per-facet hooks, and the per-era gating.

## When to Use

- Adding a new harvest system (rare, but possible for a custom shard).
- Adjusting the vein table for a new expansion.
- Wiring a bonus resource (e.g. a custom "Rare Ore" drop).
- Debugging why a player does not get a colored resource.
- Wiring the Elf racial bonus for a new race.
- Auditing the Ter Mur sub-resources (Sand/Granite/Quality Gems).
- Adding a new craft resource type (e.g. Mythril Ore) and a matching vein row.

Don't use for:

- The base item/mobile model (use `uo-items-foundation`).
- The crafting system that consumes the resources (use `uo-crafting-recipes-resources`).
- The loot table that drops finished goods (use `uo-loot-generation-artifacts`).

## HarvestSystem Base Class

`Projects/UOContent/Engines/Harvest/Core/HarvestSystem.cs` is the abstract base. The `HarvestSystem` owns the `HarvestDefinition` for a single skill (Mining, Lumberjacking, Fishing), and exposes the public API for the harvest flow:

```
Player double-clicks tool (e.g. pickaxe)
 ├─ tool check: tool type matches HarvestDefinition
 ├─ target: HarvestTarget(definition)
 ├─ on target acquired: HarvestTimer starts
 ├─ on each tick: roll vein, attempt bonus resource, attempt mutate entry
 └─ on success: drop resource at player's feet
```

The `HarvestDefinition` holds:

| Field | Purpose |
|---|---|
| `Veins` | The list of `HarvestVein` rows (the main resource table). |
| `BonusResources` | The list of `BonusHarvestResource` rows (e.g. colored ore, special wood, big fish). |
| `MutateEntries` | The list of `MutateEntry` rows (rare / cursed / special rolls). |
| `PrimaryResourceType` | The `Type` of the main resource (Iron Ore, Regular Wood, Fish). |
| `EffectActions` | The per-tick animation (sound, particle). |
| `EffectSounds` | The success / failure sounds. |
| `EffectCounts` | The per-tool swing count (e.g. 2 swings per attempt for pickaxe). |
| `Range` | The target range (1 tile for pickaxe, 1-2 for axe, 1-4 for fishing pole). |
| `BankedVeinTypes` | Whether the vein is randomly chosen from the bank or fixed per resource. |

The `HarvestSystem` is a singleton per skill: `Mining.System`, `Lumberjacking.System`, `Fishing.System`. Each is created at startup and registered for the matching tool type.

## HarvestTarget and HarvestTimer

`HarvestTarget` is a `Target` subclass that fires when the player targets a tile with the tool. The target validates:

- The target tile is a valid harvest tile (mountain, tree, water).
- The tile is in range.
- The tile is not a "dead" tile (e.g. felled tree, mined-out mountain).

`HarvestTimer` is a `Timer.DelayCall` that runs the per-attempt logic. The default is 1 attempt every ~1.5s real-time. The timer:

1. Validates the player is still standing on the tile.
2. Validates the tool is still in the player's hands.
3. Rolls the `HarvestVein` table.
4. Rolls the `BonusHarvestResource` table.
5. Rolls the `MutateEntry` table.
6. If a resource is generated, drops it at the player's feet.
7. If the resource is mined out, sets a "regrow" timer (respawn).

The `HarvestSoundTimer` plays the per-tick sound (the pickaxe swing, the axe chop, the fishing splash).

## Vein Tables

`HarvestVein` is a single row in the vein table. The fields:

| Field | Purpose |
|---|---|
| `VeinType` | The `Type` of the resource this vein produces (e.g. `IronOre`, `DullCopperOre`, `ShadowIronOre`). |
| `VeinChance` | The probability of this vein being selected per attempt. |
| `MinSkill` | The minimum skill to attempt this vein. |
| `MaxSkill` | The maximum skill to attempt this vein (excluded). |
| `RequiredRace` | The race that can mine this vein (used for Elf-only resources, pre-SA). |

The classic Mining vein table (in `Mining.cs`) is a per-ore table: Iron, Dull Copper, Shadow Iron, Copper, Bronze, Golden, Agapite, Verite, Valorite, with per-skill requirements. The Lum vein table is per-wood: Regular, Oak, Ash, Yew, Heartwood. The Fishing vein table is a per-fish table (or per-special-roll table).

The `RandomizeVeins` flag on the `HarvestDefinition` controls whether the vein is randomly chosen per attempt (the standard) or fixed (used for special cases like the Doom Gauntlet iron vein).

## Bonus Resources

`BonusHarvestResource` is the bonus row that adds an extra roll on top of the base vein. The fields:

| Field | Purpose |
|---|---|
| `Type` | The `Type` of the bonus resource (e.g. `Citrine`, `Amber`, `Board`, `WhitePearl`). |
| `Chance` | The per-attempt probability of this bonus firing. |
| `MinSkill` / `MaxSkill` | The skill gate. |
| `RequiredExpansion` | The era gate. |
| `Facets` | The facets this bonus applies to (some bonuses are Felucca-only). |

Examples:

- Mining bonus: `Amethyst`, `Citrine`, `Diamond`, `Emerald`, `Ruby`, `Sapphire`, `StarSapphire`, `Tourmaline`. SE-introduced: 1.0-1.5x chance. ML-introduced: bonus messages, gem type variety.
- Lumber bonus: `BarkFragment`, `LuminescentFungi`, `Switch`, `ParasiticPlant`, `BrilliantAmber`. ML-introduced.
- Fishing bonus: `BigFish`, `TreasureMap`, `MessageInABottle`, `PrizedFish`/`WondrousFish`/`TrulyRareFish`/`PeculiarFish` (ToL+).

The bonus is rolled *after* the base vein. The bonus resource drops as a separate item alongside the base resource.

## Mutate Entries

`MutateEntry` is the rare/special roll. The fields:

| Field | Purpose |
|---|---|
| `ReqSkill` | The minimum skill to qualify. |
| `MinChance` | The minimum probability (at `ReqSkill`). |
| `MaxChance` | The maximum probability (at 100 skill). |
| `Mutate` | Whether the entry can replace the base resource (true) or add to it (false). |
| `Type` (or `Types[]`) | The `Type` of the special item (e.g. `SpecialFishingNet`, `BigFish`, `TreasureMap`). |

The mutate entry is rolled only when the player has the required skill. At 100 skill, the chance is `MaxChance`; below the threshold, the chance scales linearly.

The Fishing mutate table (per `Fishing.cs:13-31`):

| Type | Mutate | ReqSkill | MaxChance | Notes |
|---|---|---|---|---|
| `SpecialFishingNet` | true | 80 | 80% | Fishing net (HS, 3-5 fish at once) |
| `BigFish` | true | 80 | 80% | Big Fish, for the Fishmonger Quest |
| `TreasureMap` | true | 90 | 80% | Drops a Treasure Map (level 1-3) |
| `MessageInABottle` | true | 100 | 80% | Rare special |
| `PrizedFish`/`WondrousFish`/`TrulyRareFish`/`PeculiarFish` | false | 0 | 125% | High Seas Fish (ToL+ bonus, not mutated) |
| `Boots`/`Shoes`/`Sandals`/`ThighBoots` | false | 0 | 105% | "Shoes" fishing bonus (joke) |
| `null` (e.g. nothing) | false | 0 | 200% | "Nothing" (no bonus) |

The Mining mutate table adds cursed ore, special ingots, and rare gems. The Lumber mutate table adds `RotwormStew` (BarkFragment), `LuminescentFungi` (rare ML drop), and `Switch` (rare ML drop).

## Elf Racial Bonus

Per `www.uoguide.com/Races`, Elves get:

- **Knowledge of Nature**: increased chance of acquiring special resources (colored ore, special boards).
- **Per-facet respawn reduction**: Elves reduce the regrow time on the resource tile.

The `RaceBonus` field on the `BonusHarvestResource` (or the vein row) sets the Elf bonus multiplier. The `RespawnReduction` is applied to the `HarvestBank.RespawnTime` for the tile.

The engine implementation is in `Mining.cs`, `Lumberjacking.cs`, `Fishing.cs` via `mobile.Race == Race.Elf` checks. The bonus is per-skill (e.g. `Mining.cs:ElfBonusChance`).

`Melisande's Corroded Hatchet` is the only item in the game that raises Lumberjacking when equipped (+5). `Harvester's Axe` is the SA-era counterpart (from the Huntmaster's Challenge). `Mining Gloves` (BOD reward) raise Mining by +5.

## Ter Mur Sub-Resources

Ter Mur introduced 3 sub-resources that are gathered with the standard tool, but require a **sub-book** from a Ter Mur vendor:

- **Sand** (glass-quality sand, for `Glassblowing`): read the "Find Glass-Quality Sand" book from the Alchemist in Royal City. Activated automatically when using a pickaxe on a sandy tile.
- **Granite** (quality stone, for `Masonry`): read the "Mining for Quality Stone" book from the Stone Crafter in Royal City. Activated via context menu (click pickaxe → "Mine for Granite").
- **Quality Gems** (high-quality gems, for `Jewelery`): read the "Mining for Quality Gems" book from the Blacksmith in Royal City. Activated automatically when mining ore.

The sub-resource is rolled in addition to the standard resource (it's a `BonusHarvestResource`). The skill requirement is 0 for sand, 65 for granite, 65 for quality gems.

## Mining Implementation Notes

`Mining.cs` is the most complex of the three systems because of the colored-ore table and the 9 ore types (Iron through Valorite). The vein table:

| Vein | MinSkill | MaxSkill | Chance |
|---|---:|---:|---:|
| Iron | 0 | 65 | 50% |
| Dull Copper | 65 | 70 | 20% |
| Shadow Iron | 70 | 75 | 15% |
| Copper | 75 | 80 | 12% |
| Bronze | 80 | 85 | 10% |
| Golden | 85 | 90 | 8% |
| Agapite | 90 | 95 | 6% |
| Verite | 95 | 99 | 4% |
| Valorite | 99 | 100 | 2% |

`SmallForge` and `Forge` (placed in houses) speed up the smelt step but do not affect mining.

The Mining tool is a `BaseAxe` or `Pickaxe` (`Projects/UOContent/Items/Skill Items/Mining/Pickaxe.cs`). The Mining skill check fires `SkillCheck.CheckSkill(mobile, SkillName.Mining, 0, 100)`.

## Lumberjacking Implementation Notes

`Lumberjacking.cs` covers wood harvesting with an axe. The vein table (ML-extended):

| Vein | MinSkill | MaxSkill | Chance |
|---|---:|---:|---:|
| Regular Wood | 0 | 65 | 50% |
| Oak | 65 | 80 | 15% |
| Ash | 75 | 90 | 12% |
| Yew | 85 | 95 | 8% |
| Heartwood | 95 | 100 | 5% |

ML introduced the rare drops: `BarkFragment`, `LuminescentFungi`, `Switch`, `ParasiticPlant`, `BrilliantAmber`. The bonus is per-skill (0.1-2% at low skill, 0.5-5% at high skill).

`Melisande's Corroded Hatchet` is a +5 Lumberjacking item. The tool is a `BaseAxe` (hatchet) or `Hatchet`. The Lumber skill check fires `SkillCheck.CheckSkill(mobile, SkillName.Lumberjacking, 0, 100)`.

## Fishing Implementation Notes

`Fishing.cs` covers fishing with a fishing pole. The vein is "Fish" (a single type, with a single resource: `FishSteak`). The bonuses are the mutate entries (Big Fish, Treasure Map, Special Fishing Net, Message in a Bottle).

The `Bait` is required (worms from the Worms for Bobbing quest, or bought). The water must be a static or land water tile. The fishing range is up to 4 tiles.

The `High Seas` expansion (Publish 70) added the `SpecialFishingNet` (3-5 fish at once, 80+ skill), the `PrizedFish`/`WondrousFish`/`TrulyRareFish`/`PeculiarFish` for the Fishmonger Quest, and the `Fish Pie` recipe for Cooking.

The `Fishing` skill check fires `SkillCheck.CheckSkill(mobile, SkillName.Fishing, 0, 100)`.

## Per-Facet and Per-Era Differences

- **Felucca**: double resources, no special bonus. The standard.
- **Trammel**: standard rates, half the resources of Felucca. Most "safe" facet.
- **Ilshenar**: standard rates. Paragon creatures are a special case.
- **Malas / Tokuno / Ter Mur / Eodon**: standard rates, but per-facet resource restrictions (e.g. Tokuno wood types are different).

The ML-introduced Elf respawn reduction is 1.5x speed in Felucca, 2x in other facets (per the source-level test). The Human Workhorse bonus is +1-2 logs in Trammel/Felucca, +1 ore when mining.

## Common Pitfalls

1. **Calling `AddItem` to drop a harvest resource instead of using the `HarvestSystem` API.** The harvest system tracks regrow timers; bypassing it leaves the tile permanently harvested.
2. **Forgetting `[Constructible]` on a custom `BaseResource` subclass.** The resource is not reachable from the harvest table if it cannot be instantiated by the `Func<>`.
3. **Setting `VeinChance` > 1.0.** A vein chance > 1.0 produces 100% drop rates; the engine clamps but warns.
4. **Adding a new `BonusHarvestResource` with `RequiredExpansion = Expansion.ML` on a pre-ML shard.** The bonus silently fails to roll; no error is logged.
5. **Setting `RequiredRace` on a vein row that the player's race cannot satisfy.** The vein is silently skipped, and the player gets the next valid vein (which may be the default).
6. **Forgetting the respawn timer on a custom harvest tile.** A `HarvestBank.RespawnTime` is required for the tile to regrow; without it, the resource is one-time.
7. **Wiring a MutateEntry with `ReqSkill = 100` and `MaxChance = 50%`.** The chance scales linearly from 0 at `ReqSkill - 1` to `MaxChance` at 100; the actual probability is `(skill - ReqSkill) / (100 - ReqSkill) * MaxChance`.
8. **Modifying the static `_mutateTable` field without restarting the engine.** The mutate entries are loaded at `Configure()` time; runtime changes are not picked up.
9. **Forgetting the `EffectActions` on a custom harvest definition.** The per-tick animation (sound, particle) is set on the definition; without it, the harvest is silent.
10. **Using `LootPack` to drop harvest resources.** The harvest system is the canonical path; `LootPack` is for mob drops.

## Common Recipes

### Adding a New Vein Row

```csharp
// In Mining.cs vein table
new HarvestVein(50.0, 0.0, 65.0, typeof(IronOre)),
new HarvestVein(20.0, 65.0, 70.0, typeof(DullCopperOre)),
// New row:
new HarvestVein(10.0, 100.0, 120.0, typeof(MythrilOre)),  // 100-120 skill
```

### Adding a New Bonus Resource

```csharp
// In Mining.cs bonus table
new BonusHarvestResource(0.5, 0, 100.0, "You find a rare gem!", typeof(StarSapphire)),
```

### Adding a Ter Mur Sub-Resource

```csharp
// In Mining.cs sub-resource section
if (mobile.Race == Race.Gargoyle && mobile.HasBook("Find Quality Gems"))
{
    BonusHarvestResource(0.2, 65, 100, "You find a perfect gem!", typeof(PerfectEmerald));
}
```

### Adding a New MutateEntry

```csharp
// In Fishing.cs mutate table
new MutateEntry(95.0, 110.0, 60.0, true, typeof(MessageInABottle)),
```

### Wiring a Custom Elf Bonus

```csharp
// In Mining.cs per-vein roll
double chance = vein.VeinChance;
if (mobile.Race == Race.Elf) chance *= 1.3;  // 30% Elf bonus
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New harvest vein: `Type` is a valid `BaseResource` subclass, `VeinChance` is between 0 and 1, `MinSkill`/`MaxSkill` are non-overlapping with the other veins.
- [ ] New bonus resource: `Chance` is between 0 and 1, `MinSkill`/`MaxSkill` are valid, `RequiredExpansion` matches the era.
- [ ] New mutate entry: `ReqSkill` is non-negative, `MinChance` <= `MaxChance`, `Mutate` is set correctly (true replaces, false adds).
- [ ] The `HarvestDefinition` is set on the system's static `Definition` field; `System` is registered with the matching tool type.
- [ ] The respawn timer fires (the resource tile regrows after the configured `RespawnTime`).
- [ ] Elf racial bonus: the bonus is per-vein or per-bonus, not a flat multiplier.
- [ ] Ter Mur sub-resources: the book is consumed (or the book is a flag), the sub-resource drops alongside the main resource.
- [ ] `SkillCheck.CheckSkill` is called on the matching skill (`Mining`, `Lumberjacking`, `Fishing`).
- [ ] Per-facet behavior: Felucca doubles resources, Trammel halves, Ilshenar is standard.
- [ ] Per-era behavior: SE-gated mining gems only fire on SE+, ML-gated lumber wood types only fire on ML+.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the `BaseResource` and `Item` model.
- `uo-aos-item-properties` - the property rolls used on rare harvest items.
- `uo-crafting-recipes-resources` - the crafting system that consumes the harvested resources.
- `uo-world-facets-regions` - the per-facet resource rules.
- `uo-skills-stats-races` - the Elf racial bonus and the skill gain on harvest use.
- `uo-combat-pipeline` - the combat-related drops from harvesting (e.g. Paragon retaliation).
- `uo-loot-generation-artifacts` - the loot table for finished items (the harvest system is upstream of this).
- `uo-champions-cannedevil-treasures` - the CannedEvil/ChampionSpawn system is the late-game PvE activity; the per-boss drops and the per-facet reward differences are downstream of the harvest/loot pipeline.
- `modernuo-content-patterns` - canonical templates for new harvest systems and veins.
- `modernuo-era-expansion` - per-era resource availability.
- `www.uoguide.com/Lumberjacking` (offline reference) - the Lum mechanic and the +5 hatchet.
- `www.uoguide.com/Races` (offline reference) - the Elf Knowledge of Nature bonus.
- `docs/mondains-legacy-content-matrix.md:74` (offline reference) - the ML harvest branches and the Elf respawn reduction.
