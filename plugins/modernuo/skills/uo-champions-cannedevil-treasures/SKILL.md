---
name: "uo-champions-cannedevil-treasures"
description: "Use when working with the UO Champion Spawn system and Treasures events in ModernUO/RebirthUO servers - CannedEvil/ChampionSpawn altars, the 16-candle level scaling, the Harrower / Star Room mechanic, the 6 Champion Skull altars, Champion Artifact rolls, Doom Gauntlet, Treasures of Tokuno (ToT) Lesser/Moderate/Greater artifacts, and the per-facet reward differences. Use when adding a new champion altar, debugging why a champion does not summon, wiring Treasures event drops, auditing Felucca-vs-other-facet rewards, or connecting champion spawns to regional region hooks."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Champions, CannedEvil, Treasures

## Overview

The UO Champion Spawn system is the late-game PvE activity: players clear escalating waves of monsters at an altar, eventually summon a Champion boss, and receive themed rewards. The system originated in `Third Dawn` and was re-introduced in `Publish 16` for Felucca. The engine code is in `Projects/UOContent/Engines/CannedEvil/` (the historical name of the system in RunUO) and `Projects/UOContent/Engines/Peerless/` (the 6 ML bosses). Treasures of Tokuno is the post-SE event-driven artifact drop system in `Projects/UOContent/Engines/Treasures of Tokuno/`.

The central class is `ChampionSpawn` (`Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs`). The `GenChamps.cs` file generates the canonical spawn altars at world-load time. The Star Room (with the 6 Champion Skull altars that summon the Harrower) is in `Projects/UOContent/Engines/Peerless/StarRoom.cs`. The Doom Gauntlet is in `Projects/UOContent/Engines/Doom/`. Treasures of Tokuno lives in `Projects/UOContent/Engines/Treasures of Tokuno/`.

This skill covers the CannedEvil/Champion Spawn architecture, the 16-candle level scaling, the Champion types (per expansion), the Harrower and the Star Room, the Champion Skull altar mechanic, the Champion Artifact distribution, the Doom Gauntlet, the Treasures of Tokuno system, the per-facet reward differences (Felucca vs Trammel/Ilshenar/Tokuno/ML), and the integration with the Peerless system (the 6 ML bosses share the same Champion Spawn infrastructure).

## When to Use

- Adding a new Champion Spawn altar.
- Debugging why a Champion does not summon.
- Wiring Treasures of Tokuno drops.
- Auditing the per-facet reward differences.
- Adding a Champion Skull altar for the Star Room.
- Wiring the Doom Gauntlet.
- Auditing the per-expansion Champion types.
- Connecting a Champion Spawn to a `Region` for the per-facet restrictions.

Don't use for:

- The base item/mobile model (use `uo-items-foundation`).
- The combat damage pipeline (use `uo-combat-pipeline`).
- The loot generation system (use `uo-loot-generation-artifacts`).
- The Map/Region system itself (use `uo-world-facets-regions`).

## The CannedEvil Architecture

`Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs` is the central class. The `ChampionSpawn` instance is bound to an altar (an `Item` with a specific `ItemID` placed in the world). The altar has:

- `ChampionSpawn` instance: the spawn controller.
- `Type` (`ChampionSpawnType` enum): the spawn category (Abyss, Arachnid, Cold Blood, Forest Lord, Unholy Terror, Vermin Horde, Sleeping Dragon, Minotaur, Corrupt, Glade, Abyssal Infernal, Primeval Lich, Dragon Turtle).
- `SpawnRadius` / `SpawnArea`: the region of monster spawns around the altar.
- `SpawnLevel`: the current level (0-16 candles).
- `Active`: whether the spawn is currently active.
- `Champion`: the spawned Champion boss (when at 16 candles and summoned).
- `RedSkull`, `WhiteSkull`: the candle indicators on the altar graphic.

The `ChampionSpawn` lifecycle:

```
1. Inactive: altar shows "no candles". Activation requires Valor (Knight of Valor virtue) or a special book.

2. Player activates: candles go to 0, spawn starts.

3. Monsters spawn around the altar. As the player kills them, the candle counter advances.

4. At certain kill thresholds (256/128/64/32), the spawn strength increases:
   Level 1: 1-5 red candles (256 kills)
   Level 2: 6-9 red candles (128 kills)
   Level 3: 10-13 red candles (64 kills)
   Level 4: 14-16 red candles (32 kills)

5. At 16 candles, the player can target the altar's Idol to summon the Champion.

6. Champion is summoned: it's a `BaseCreature` subclass (e.g. `MorgBergen`, `Neira`, `Serado`, etc.) with the appropriate stats and a unique `Name`.

7. Champion is killed: rewards drop (Champion Artifact + Power Scrolls + Scroll of Transcendence + 250,000 gold).

8. In Felucca: 6 Power Scrolls are awarded to the top 6 damage dealers; the Idol becomes a moongate to the Star Room.
```

The `GenChamps.cs` file generates the canonical altars at world load. The altars are placed at fixed coordinates per the official OSI/EA map.

## The 16-Candle Level Scaling

Per `www.uoguide.com/Champion_spawn`, the 16-candle level scaling is:

| Level | Red candles | Kills to advance |
|---|---:|---:|
| 1 | 1-5/6 | 256 |
| 2 | 5/6-9/10 | 128 |
| 3 | 9/10-13/14 | 64 |
| 4 | 13/14-16 | 32 |

The spawn strength increases with each level. The monsters at level 4 are the toughest of the type (e.g. for Abyss, level 4 spawns Balrons, Daemons, and Succubi). At 16 candles, the spawn can cycle a few times before the champion is summoned.

The 10-minute decay rule: if the player does not kill enough spawn within 10 minutes of the first monster kill at a level, the white candle advancement resets to 0. If the player does not advance at least 20% at a single level, one red candle disappears and the spawn moves backward.

## The 13+ Champion Types

Per the official UOGuide and the engine's `ChampionSpawnType` enum (in `ChampionSpawn.cs`):

| Era | Type | Themed monsters |
|---|---|---|
| Third Dawn | Abyss | Daemons, Gargoyles, Balrons |
| Third Dawn | Arachnid | Spiders, Scorpions, Terathan Warriors |
| Third Dawn | Cold Blood | Lizardmen, Ophidians, Dragons |
| Third Dawn | Forest Lord | Pixies, Sprites, Centaurs |
| Third Dawn | Unholy Terror | Undead, Mummies, Liches |
| Third Dawn | Vermin Horde | Rats, Ophidians, Slimes |
| Samurai Empire | Sleeping Dragon | Reptiles, Dragons, Wyrms |
| Mondain's Legacy | Minotaur | Minotaurs, Minotaur Captains, Tormented Minotaurs |
| Mondain's Legacy | Corrupt | Corrupted creatures |
| Mondain's Legacy | Glade | Twisted creatures |
| Stygian Abyss | Abyssal Infernal | Abyss creatures |
| Stygian Abyss | Primeval Lich | Liches, Skeletal Dragons |
| Time of Legends | Dragon Turtle | Sea creatures, Dragon Turtles |

Per the engine, the ML/Spawners `Project/UOContent/Engines/CannedEvil/GenChamps.cs` declares which altar type is at which location.

## Champion Spawn Artifacts

Per `www.uoguide.com/Champion_spawn`, the Champion Spawn Artifact drop rates:

- 30% overall drop chance
- 10% Replica (shared reward)
- 15% Decorative reward
- 5% Unique reward

The Replica tier is a themed shared reward (e.g. a decorative shield, a banner). The Decorative tier is a thematic but non-combat item. The Unique tier is the boss-themed artifact with a stat bonus and a unique hue.

The artifact is rolled on `Champion.OnDeath` and added to the top damage dealer's backpack. The `ChampionSpawn.OnChampionKilled` callback fires the artifact roll.

Per the engine, the artifact list is in `Projects/UOContent/Items/Champion Artifacts/`. The artifact types are per Champion type (e.g. Forest Lord drops `Quiver of Rage`, `Bow of the Juka King`, etc.).

## Power Scrolls and Scrolls of Transcendence

- **Power Scrolls** are 5-point skill cap boosts. The 105 cap scrolls are randomly awarded for killing regular mobs at the spawn (across all levels). The 110, 115, 120 cap scrolls are only awarded for slaying the Champion. **Felucca only** (per `www.uoguide.com/Champion_spawn`).
- **Scrolls of Transcendence** are 0.1-0.5 skill point boosts that count toward a Power Scroll's worth. They are awarded on regular mob kills and Champion kills. Felucca has 2x potency.

The `ChampionSpawn.OnChampionKilled` distributes the rewards to the top damage dealers (Felucca) or to all damage dealers (other facets, but with reduced rewards).

## The Harrower and the Star Room

Per `www.uoguide.com/Star_Room` and `www.uoguide.com/Champion_spawn`:

- The Star Room is a hidden area in Terathan Keep. The gateway is at the deepest part of the dungeon.
- 6 Champion Skull altars (one per Champion type) are placed in the Star Room. Each skull is obtained from a different Champion spawn (only Felucca, only at 16-candle Champion kills).
- The player must place all 6 skulls on the 6 altars to open a black gate.
- The black gate leads to the Harrower's lair, a Felucca-only dungeon.
- The Harrower is a special Champion-tier monster with a unique stat scroll drop.

The `StarRoom.cs` file in `Projects/UOContent/Engines/Peerless/` holds the Star Room logic. The `ChampionSkull` item is in `Projects/UOContent/Items/Champion Artifacts/ChampionSkull.cs`.

The Stat Scrolls are Felucca-only and the most valuable reward in the game. They grant +5 to a single stat (up to a 125 cap). The 6 stats are Str/Dex/Int/Hits/Stam/Mana.

## Doom Gauntlet

The Doom Gauntlet is a Felucca-only boss event in the Doom Dungeon (introduced in UOR). The player enters the Gauntlet area, fights escalating waves of monsters, and eventually faces a boss with a unique drop.

The engine code is in `Projects/UOContent/Engines/Doom/`. The `GauntletSpawner.cs` holds the spawn controller, the `GenGauntlet.cs` generates the spawns at world load.

The Doom artifacts are tier-based (the Doom Gauntlet is a Publish 16-era activity, but the drops are still relevant for ML). The Doom artifacts are listed in `Projects/UOContent/Items/Doom/`.

## Treasures of Tokuno (ToT)

The Treasures of Tokuno is a post-SE event that drops lesser, moderate, and greater artifacts from monsters on the Tokuno facet. The engine code is in `Projects/UOContent/Engines/Treasures of Tokuno/`. The central class is `TreasuresOfTokuno.cs`. The artifact list is in `LesserArtifacts.cs`, `ModerateArtifacts.cs`, and `GreaterArtifacts.cs` (in the same folder).

The ToT drops are per-monster: certain Tokuno creatures drop a ToT artifact on death, with a small chance. The artifacts are tiered:

- **Lesser** (Publish 15+): cosmetic / minor-stat items. Drop rate 1-2% per Tokuno creature.
- **Moderate** (Publish 20+): themed items with usable properties. Drop rate 0.5-1%.
- **Greater** (Publish 27+): rare artifacts with significant properties. Drop rate 0.1-0.5%.

The artifacts are tracked per-account (the player can only have one of each, and the drop is suppressed if the player already has the artifact). The `TreasuresOfTokuno` callback fires on each Tokuno mob kill.

## Paragon Integration

The Champion Spawn system integrates with the Paragon monster system (`BaseCreature.Paragons`). Paragon monsters have a chance to spawn in any region with a high monster density. The Paragon has boosted stats and rolls an additional `LootPack` (covered in `uo-loot-generation-artifacts`).

The Champion Spawn regions do not produce Paragons by default. The Paragon chance is per-facet and per-monster-type, and is gated by the era.

## Per-Facet and Per-Era Differences

| Facet | Champion rewards | Skull drop | Power Scrolls | Star Room access |
|---|---|---|---|---|
| Felucca | Full (Champion Artifact + 6 Power Scrolls + Transcendence + 250k gold) | Yes | 105, 110, 115, 120 | Yes (via Star Room) |
| Trammel | Champion Artifact + Transcendence only | No | No | No |
| Ilshenar | Champion Artifact + Transcendence only | No | No | No |
| Malas | Champion Artifact + Transcendence only | No | No | No |
| Tokuno | Champion Artifact + Transcendence only | No | No | No |
| Ter Mur | Champion Artifact + Transcendence only | No | No | No |
| Eodon | Champion Artifact + Transcendence only | No | No | No |

The `ChampionSpawn.OnChampionKilled` callback branches on `Map` to apply the per-facet reward rules.

## Integration with the Region System

The Champion Spawn regions are typed `Region` subclasses (`ChampionSpawnRegion`). The region:

- Blocks `Recall`, `Gate Travel`, `Sacred Journey` (`OnBeginSpellCast` returns false).
- Blocks pet-summoning past a certain level (`IsMobileAllowed` returns false).
- Forbids rune marking (`OnTravel` returns false).
- Distributes kill credit to the `ChampionSpawn` instance (`OnDeath` forwards the damage entry).

The `ChampionSpawnRegion` is registered in `Distribution/Data/regions.json` with the `ChampionSpawnRegion` type. The altar is placed in the region's center.

## Common Pitfalls

1. **Setting the altar's `Type` to the wrong ChampionSpawnType.** The spawn table is loaded per `Type`; the wrong type spawns the wrong monsters.
2. **Forgetting the `Activation` requirement.** Most altars require `Valor` (Knight of Valor virtue) to activate. The `Engine_Activation` test verifies this.
3. **Using `Recall` to enter the spawn zone.** The `Region.OnBeginSpellCast` blocks this; the player must walk in.
4. **Not resetting the spawn timer on server restart.** The `ChampionSpawn` is serialized; on restart, the candle state is preserved. A spawn that was at 16 candles continues to 16.
5. **Allowing pet-summoning in the spawn zone.** The pet-summon ban is enforced by `IsMobileAllowed`; bypassing it lets players cheat the spawn.
6. **Setting `Active = true` on a spawn that has not been activated by a player.** The spawn should start at 0 candles and require player activation.
7. **Forgetting the per-facet reward rules.** The `OnChampionKilled` callback branches on `Map`; if the branch is removed, all facets get the full Felucca reward set, breaking the per-facet economy.
8. **Adding a new Champion type without a `ChampionSpawnType` enum value.** The type must be in the enum for the engine to recognize it.
9. **Using `LootPack` for the Champion artifact instead of the per-Champion drop table.** The Champion artifact is a per-boss drop, not a random `LootPack` roll. The `MLPeerlessArtifacts.cs` mapping is the canonical source for ML bosses.
10. **Forgetting the `GenChamps` world-generation step.** New altars are not generated at world load; the `GenChamps` regeneration is required.
11. **Setting the Doom Gauntlet boss's `LootPack` to a tier that is too low.** The Doom boss drops rare artifacts; the `LootPack` must be at least `FilthyRich` plus a per-boss drop.
12. **Skipping the `Harrower` entry in the Star Room gate check.** The black gate requires all 6 skulls; bypassing the count check is a regression.

## Common Recipes

### Adding a New Champion Spawn Altar

```csharp
public class MyChampionAltar : ChampionSpawn
{
    [Constructible]
    public MyChampionAltar() : base(ChampionSpawnType.ArenaChampions)
    {
        // Set location
        Location = new Point3D(1234, 5678, 0);
        Map = Map.Felucca;
    }
}
```

### Wiring a Champion Artifact

The Champion artifact is registered in the per-Champion drop table, not as a `LootPackEntry`. The `ChampionSpawn.OnChampionKilled` callback rolls the artifact and adds it to the top damage dealer's backpack.

### Adding a New Tokuno Artifact Tier

```csharp
// In TreasuresOfTokuno.cs
public static bool GiveTokunoArtifact(Mobile m, TokunoTier tier)
{
    var artifact = RollArtifact(tier);
    if (artifact == null) return false;
    if (HasArtifact(m, artifact.GetType())) return false;  // per-account dedup
    m.AddToBackpack(artifact);
    return true;
}
```

### Adding a New Doom Boss

```csharp
public class MyDoomBoss : BaseCreature
{
    [Constructible]
    public MyDoomBoss() : base(AIType.AI_Melee, FightMode.Closest)
    {
        ...
        LootPack.FilthyRich.Generate(this);
        m_DropArtifacts.Add(new BossArtifactEntry(typeof(MyDoomArtifact), 1.0));
    }
}
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New altar: `Type` is a valid `ChampionSpawnType`, location is in a valid `Map`, region hook is registered.
- [ ] Activation: altar starts at 0 candles and requires `Valor` (or a special book) to activate.
- [ ] Level scaling: kill thresholds (256/128/64/32) advance candles; 16 candles trigger Champion summon.
- [ ] Champion summoned: `Champion` field is set, `OnChampionKilled` fires.
- [ ] Reward distribution: Felucca gets 6 Power Scrolls + Champion Artifact + Transcendence + gold; other facets get Champion Artifact + Transcendence only.
- [ ] Travel rules: Recall/Gate/Sacred Journey are blocked in the spawn zone.
- [ ] Pet-summon rule: pet-summoning is blocked past the configured level.
- [ ] Rune marking: rune marking is blocked in the spawn zone.
- [ ] Star Room: all 6 skulls open the black gate to the Harrower's lair.
- [ ] Harrower drop: the Stat Scroll is awarded to the top damage dealer.
- [ ] Doom Gauntlet: the boss drops the per-boss artifact and the standard FilthyRich+ tier loot.
- [ ] Treasures of Tokuno: per-account dedup works (a player who already has the artifact does not get a duplicate).
- [ ] Paragon: Paragon monsters do not spawn in Champion Spawn regions by default.

## Related Skills

- `uo-world-facets-regions` - the `Region` and per-facet rules that the Champion Spawn regions enforce.
- `uo-combat-pipeline` - the combat damage pipeline that Champion mobs use.
- `uo-loot-generation-artifacts` - the loot table for the per-boss drops.
- `uo-items-foundation` - the `Item` and `BaseCreature` model.
- `uo-quests-engine-ml` - the ML quest system that can reward Champion access.
- `uo-magic-spells` - the field spells and Champion-boss spell loadouts.
- `uo-skills-stats-races` - the racial abilities and the Knight of Valor virtue.
- `modernuo-content-patterns` - canonical templates for new Champion types and bosses.
- `modernuo-era-expansion` - per-era Champion Spawn availability.
- `www.uoguide.com/Champion_spawn` (offline reference) - the canonical 16-candle level scaling and the per-facet reward table.
- `www.uoguide.com/Star_Room` (offline reference) - the 6 Champion Skull altars and the Harrower.
- `docs/mondains-legacy-content-matrix.md:75` (offline reference) - the ML-era Champion Spawn regression coverage and the per-facet reward rule.
