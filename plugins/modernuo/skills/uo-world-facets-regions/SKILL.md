---
name: "uo-world-facets-regions"
description: "Use when working with the UO world structure in ModernUO/RebirthUO servers - the 7 Facets (Felucca, Trammel, Ilshenar, Malas, Tokuno, Ter Mur, Eodon), the Map and Sector spatial index, Region lifecycle and hooks (OnEnter, OnExit, OnTravel, OnBeginSpellCast, OnDeath, OnHarmful, OnResource), travel rule validation (Recall/Gate/Sacred Journey), Champion Spawn regions, Faction towns, dungeon regions, and content gating per facet/era. Use when wiring a new region, debugging a travel-blocked spell, defining a new Champion Spawn, or auditing per-facet combat/travel rules."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO World, Facets, Regions

## Overview

The UO world is a 2D grid per facet. The engine splits the world into 7 facets (Felucca, Trammel, Ilshenar, Malas, Tokuno, Ter Mur, Eodon), each with its own `Map` instance. Each `Map` is divided into a grid of `Sector`s, each holding lists of `Item`s and `Mobile`s for spatial queries. `Region`s are nested rule zones that overlay the map; they own the per-area behavior like guards, dungeons, travel restrictions, and housing rules.

The engine side is `Projects/Server/Maps/Map.cs:55`, `MapLoader.cs:47-118`, and `Projects/Server/Regions/Region.cs:122`. The data side is `Distribution/Data/map-definitions.json` and `Distribution/Data/regions.json`. The Region JSON polymorphism is `Projects/Server/Regions/RegionJsonSerializer.cs:28-113`. The travel-rule validation is in `Projects/UOContent/Spells/Base/SpellHelper.cs:52-145, 642-693`.

This skill covers the 7-facet architecture, the Map/Sector spatial index, the Region lifecycle and hook surface, travel rules per facet/dungeon, Champion Spawn region rules, faction-town regions, dungeon region templates, the spawn package system, and the per-facet combat/travel differences. It is the geographical "where" of UO and complements the player-side skills (`uo-skills-stats-races`), the combat formula (`uo-combat-pipeline`), and the magic system (`uo-magic-spells`).

## When to Use

- Adding a new region (dungeon, town, custom zone).
- Wiring a region's hook (e.g. `OnDeath` to apply per-faction loot rules).
- Debugging why a Recall/Gate/Sacred Journey does not work in a dungeon.
- Adding a new Champion Spawn altar with the right type and level scaling.
- Auditing per-facet combat and travel rules.
- Defining a new facet (e.g. for a custom world).
- Placing custom spawns in a specific region.
- Auditing the JSON-driven region registration for a new expansion.

Don't use for:

- The combat damage formula (use `uo-combat-pipeline`).
- The skill/stat/race system (use `uo-skills-stats-races`).
- The base item/mobile entity model (use `uo-items-foundation`).

## The 7 Facets

Per `www.uoguide.com/Facets` and the engine's `ExpansionInfo`:

| Facet | Era | Combat | Travel | Notes |
|---|---|---|---|---|
| **Felucca** | None (original) | Free PvP, stealing | Free | Resources 2x; only facet with Champion Spawn Power Scrolls. |
| **Trammel** | UOR | No non-consensual PvP, no stealing | Free | Default safe facet. |
| **Ilshenar** | UOTD | No PvP, no stealing | Restricted (no Recall/Gate/Sacred Journey in) | "One big dungeon"; no player housing. |
| **Malas** | AOS | No PvP, no stealing | Free | Luna, Umbra, Doom, Bedlam; lots of player housing. |
| **Tokuno** | SE | No PvP, no stealing | Restricted (in dungeons) | Zento; Asian-themed. |
| **Ter Mur** | SA | No PvP, no stealing | Restricted (mostly through Stygian Abyss dungeon) | Gargoyle homeland. |
| **Eodon** | ToL | No PvP, no stealing | Restricted (Time Lord) | Valley of Eodon; PvE. |

The `Map` instances are registered at startup via `MapLoader.Configure()` (`Projects/Server/Maps/MapLoader.cs:47-118`). The map definitions are data-driven through `Distribution/Data/map-definitions.json`:

```json
[
  { "index": 0, "id": 0, "name": "Felucca", "fileIndex": 0, "width": 7168, "height": 4096, "season": "Spring", "rules": "None" },
  { "index": 1, "id": 1, "name": "Trammel", "fileIndex": 1, "width": 7168, "height": 4096, "season": "Spring", "rules": "Trammel" },
  ...
]
```

The active facet is determined by the `Map` reference on a `Mobile` or `Item`. A `Mobile.Player` can move between facets by stepping through a moongate or by using Recall/Gate/Sacred Journey with a valid rune marked on the target facet.

## Map, Sector, Spatial Index

`Map` is the spatial index for a facet. It is divided into a grid of `Sector`s, default 64x64 tiles. Each `Sector` holds:

- `Items`: the items located in the sector (or overlapping it).
- `Mobiles`: the mobiles located in the sector.
- `Region`: the `Region` instance for the sector (cached for fast lookups).
- `Multis`: the multi-component houses overlapping the sector.
- `Clients`: the `NetState` instances with a `Mobile` in the sector (for outgoing packet range checks).

The sector size is `Map.SectorSize` (default 64). The sector is the unit of update: a client entering a sector receives packets for all items/mobiles in that sector and the 8 adjacent sectors. This is the basis of the visual-range system.

The `GetItemsInRange<T>(Point3D, range)` and `GetMobilesInRange<T>(Point3D, range)` helpers walk the affected sectors and filter by type. These are the canonical spatial-query APIs; never iterate `World.Items` or `World.Mobiles` (CLAUDE.md:4).

## Region Lifecycle and Hooks

`Region` is the base class for all rule zones. Concrete subclasses include `TownRegion`, `GuardedRegion`, `DungeonRegion`, `NoHousingRegion`, `ChampionSpawnRegion`, `HouseRegion`, and `BaseRegion`. The current region count in `Distribution/Data/regions.json` (per `docs/server-engine-knowledge-base.md:303-313`):

| Region type | Count |
|---|---:|
| `BaseRegion` | 145 |
| `TownRegion` | 116 |
| `DungeonRegion` | 77 |
| `NoHousingRegion` | 60 |
| `GuardedRegion` | 6 |
| Special regions | 8 |

The hooks (`Region.cs:748-778`):

| Hook | Fires when | Use |
|---|---|---|
| `OnEnter(Mobile m, Region previous)` | A mobile enters the region | Apply buffs, log entry, kick non-allowed races. |
| `OnExit(Mobile m, Region next)` | A mobile leaves | Cleanup, save state. |
| `OnBeginSpellCast(Mobile m, ISpell s)` | A cast starts in the region | Block Recall in dungeons, mark cast for champion tracking. |
| `OnSpellCast(Mobile m, ISpell s)` | A cast succeeds | Track casts, apply per-region modifiers. |
| `OnDeath(Mobile m)` | A mobile dies in the region | Per-region loot rules, kill credit. |
| `OnDamage(Mobile m, ref int damage, ...)` | A mobile takes damage | Per-region damage modifiers. |
| `OnTravel(Mobile m, Point3D loc, TravelType type)` | A travel attempt (gate/recall) | Block Recall to dungeon, redirect to safe location. |
| `OnResource(Mobile m, ResourceType type, int amount, ...)` | A resource is harvested | Per-region resource overrides. |
| `IsMobileAllowed(Mobile m)` | Test if a mobile can enter | Block enemies, ghost-only. |
| `CanBeHarmful(Mobile from, Mobile target, bool msg)` | Per-region harm permission | Disable PvP in towns, enable in Felucca. |

`OnBeginSpellCast` is the canonical place to block Recall/Gate/Sacred Journey in dungeons. The `DungeonRegion` subclass overrides this to return `false` for travel spells.

## Travel Rules

The travel rules matrix is in `SpellHelper.cs:52-145` and the validator matrix at `SpellHelper.cs:642-693`. The `TravelCheckType` enum and the rules:

- `Recall`: blocked in dungeons (`DungeonRegion`), blocked in champion spawn regions, allowed everywhere else.
- `GateTravel`: blocked in dungeons (with rare exceptions like Tokuno), allowed in Tokuno surface.
- `SacredJourney`: blocked in dungeons; restricted in Ilshenar (one-way out), allowed in Tokuno.
- `Mark`: blocked in dungeons, blocked in champion spawn regions, allowed in towns and wilderness.

The check is two-step: `SpellHelper.CheckTravel(mobile, target, TravelType.Recall)` validates the destination. The mobile must have a `Rune` marked at the destination; the destination region must permit the travel type. The `Runebook` charges a separate recall-check.

`SpellHelper.FindValidSpellLocation(mobile, target, range)` is the helper used to place field spells and other location-targeted spells. It returns a `Point3D` adjusted to be on a walkable surface within the requested range.

## Region JSON Polymorphism

Regions are declared in `Distribution/Data/regions.json` with a `$type` field for the concrete region class. The `RegionJsonSerializer` (`Projects/Server/Regions/RegionJsonSerializer.cs:28-113`) deserializes the JSON into the typed `Region` instance. The per-region properties:

- `Map`: the facet the region is on.
- `Name`: the displayed name.
- `Area`: a polygon (rectangle, sector, or 3D bounding box).
- `Priority`: higher priority wins when regions overlap.
- `Music`: the per-region background music.
- `MinExpansion` / `MaxExpansion`: the region only loads if the active expansion is in range.
- `$type`: the `Server.Regions.TownRegion` (or appropriate subclass) full type name.
- Subclass-specific: `GuardedRegion` has `GuardAmount`, `HouseRegion` has `House` instance, `ChampionSpawnRegion` has `Type` and `Level` references.

A region definition looks like:

```json
{
  "Map": "Felucca",
  "Name": "Britain",
  "Area": { "X1": 1397, "Y1": 1620, "X2": 1530, "Y2": 1733 },
  "Priority": 1,
  "Music": 30,
  "$type": "Server.Regions.TownRegion"
}
```

`Region` instances are loaded during `RegionJsonSerializer.LoadRegions()` at `Main.cs:425`. Expansion filtering is at `RegionJsonSerializer.cs:58-67`: regions with `MinExpansion > Core.Expansion` or `MaxExpansion < Core.Expansion` are skipped.

## Champion Spawn Regions

`ChampionSpawnRegion` is a specialized region. It is associated with a `ChampionSpawn` instance (an altar + spawn logic). The region overrides:

- `OnBeginSpellCast`: blocks Recall/Gate/Sacred Journey for the spawn zone.
- `OnDeath`: forwards kill credit to the spawn tracker.
- `IsMobileAllowed`: blocks pet-summoning after the spawn escalates past a threshold.

The 16-red-candle level scaling (per `www.uoguide.com/Champion_spawn`):

| Level | Red candles | Kills to advance |
|---|---|---:|
| 1 | 1-5/6 | 256 |
| 2 | 5/6-9/10 | 128 |
| 3 | 9/10-13/14 | 64 |
| 4 | 13/14-16 | 32 |

At 16 candles, the Champion is summoned by targeting the Idol. The Champion drops 6 Power Scrolls (Felucca-only), Champion Spawn Artifacts (30% overall), and 250,000 gold. The Idol becomes a moongate to the Star Room.

The dynamic champion types (per expansion) are listed at `www.uoguide.com/Champion_spawn`:

- **Original** (Third Dawn): Abyss, Arachnid, Cold Blood, Forest Lord, Unholy Terror, Vermin Horde.
- **SE**: Sleeping Dragon.
- **ML**: Minotaur, Corrupt, Glade.
- **SA**: Abyssal Infernal, Primeval Lich.
- **ToL**: Dragon Turtle.

## Faction Towns (Pre-Publish 86)

The original Faction system (pre-Publish 86, when it was replaced by Vice vs Virtue) was a Felucca-only group-PvP system. Per `www.uoguide.com/Factions`, the 4 factions were True Britannians, Council of Mages, Minax, Shadowlords, each with a stronghold base. 8 Felucca cities (Britain, Magincia, Minoc, Moonglow, Skara Brae, Trinsic, Vesper, Yew) were capturable via the town Sigil (held 10 hours to corrupt, secured 3 days afterward).

The faction-related region classes override:

- `OnDeath`: enemy faction members can loot; same-faction cannot.
- `CanBeHarmful`: same-faction cannot be harmed; other factions and non-faction are valid targets.
- `IsMobileAllowed`: non-faction members can walk through the stronghold; faction vendors refuse to sell to other factions.

ModernUO/RebirthUO has the legacy Faction system partially wired (`Projects/UOContent/Engines/Factions/`); the `Expansion.ML` content matrix notes that ML-era branches exist for `NotorietyHandlers`, faction vendors/traps, and `PartyMemberInfo` (see `docs/mondains-legacy-content-matrix.md:76`).

## Dungeon Regions

`DungeonRegion` is a typed region that flags its area as a dungeon. The properties:

- Recall is blocked in the region (`OnBeginSpellCast` returns `false` for `Recall`).
- Mark is blocked in the region.
- Sacred Journey is blocked in the region.
- The region is `IsDungeonRuleset = true` (used by some spells and by the `ChampionSpawnRegion` to check overlap).
- The region's `Light` is typically `LightType.Dungeon` (full dark with `Night Sight` needed).

The 77 dungeon regions per the server-engine knowledge base include the classic dungeons (Deceit, Despise, Destard, Covetous, Shame, Wrong, Hythloth) plus ML dungeons (Bedlam, Blighted Grove, Prism of Light, Palace of Paroxysmus, Twisted Weald, Citadel, Labyrinth, Painted Caves, Stygian Abyss).

## Spawn Packages

`Distribution/Data/Spawns/**/*.json` is the data-driven spawn system. The structure is by era folder (`pre-uor/`, `post-uor/`, `pre-uoml/`, `uoml/`, `post-uoml/`, etc.) and by facet (`felucca/`, `trammel/`, `ilshenar/`, etc.). The format:

```json
{
  "name": "Britain Graveyard",
  "map": "Felucca",
  "region": "Britain",
  "type": "GenericSpawner",
  "entries": [
    { "type": "Skeleton", "count": 5, "homeRange": 12, "probability": 1.0 },
    { "type": "Zombie", "count": 3, "homeRange": 12, "probability": 0.6 }
  ]
}
```

The `BaseSpawner` (in `Projects/UOContent/Engines/Spawners/`) reads the JSON, places the spawner at the location, and respawns the `BaseCreature`s on a timer. The `EraProfile` system (`Projects/UOContent/Engines/Era Profiles/`) can route spawn-pack generation through profile-specific commands and apply the right era gate.

`Projects/UOContent/Engines/Spawners/` has the spawner engine, the `BaseSpawner` class, the various typed spawners, and the `SpawnerPersistence` (saving spawner state across server restarts).

## Common Pitfalls

1. **Iterating `World.Items` or `World.Mobiles` for spatial lookups.** Use `map.GetItemsInRange<T>(loc, range)` (CLAUDE.md:4). Iterating the global collections is a hot-path bug.
2. **Blocking Recall by checking the `Map` field directly.** The correct check is `mobile.Region.IsDungeonRuleset` or the region's `OnBeginSpellCast` override. Map-level checks miss per-region overrides (e.g. Tokuno is not a dungeon, but some regions there block Recall).
3. **Forgetting the `$type` field in `regions.json`.** Without `$type`, the JSON deserializes to the abstract `Region` and the per-subclass fields (e.g. `GuardedRegion.GuardAmount`) are lost.
4. **Using `Map.Felucca` in content code instead of `Region.OnTravel`.** Facet-level checks are wrong: Felucca is not uniformly a PvP zone (towns are guarded). Use the region's `CanBeHarmful` or `IsMobileAllowed` instead.
5. **Overriding `OnBeginSpellCast` to throw.** A throwing override kills the cast; the engine pattern is to return `false` (block) and the cast pipeline logs the rejection.
6. **Setting the region's `Priority` too low.** When regions overlap (e.g. a town is also a guarded region), the highest-priority region wins. Setting `Priority = 0` for a town makes the dungeon rules apply over the town rules in the overlapping area.
7. **Forgetting the `MinExpansion`/`MaxExpansion` filter.** A region with `MinExpansion = Expansion.ML` should not load on a pre-ML shard. The filter is at `RegionJsonSerializer.cs:58-67`; check that it is applied.
8. **Blocking `Mark` in a town.** Towns are marked-safe (Recall and Mark are allowed). The check is `Region.IsTownRuleset` or `Region is TownRegion`.
9. **Adding a new region without checking the area overlap.** Two regions with the same priority and overlapping area produce undefined behavior. The validator at startup logs overlaps; check the boot log.
10. **Forgetting the `OnDeath` loot rule for champion regions.** The killer attribution is the top-damage dealer, not the last hitter. The `ChampionSpawn` instance tracks damage and credits on `OnDeath`.

## Common Recipes

### Adding a New Town Region

```json
{
  "Map": "Felucca",
  "Name": "New Town",
  "Area": { "X1": 1000, "Y1": 1000, "X2": 1100, "Y2": 1100 },
  "Priority": 50,
  "Music": 30,
  "Guarded": true,
  "GuardAmount": 4,
  "$type": "Server.Regions.GuardedRegion"
}
```

### Blocking Recall in a Dungeon

```csharp
public class MyDungeonRegion : DungeonRegion
{
    public override bool OnBeginSpellCast(Mobile m, ISpell s)
    {
        if (s is Spells.Fourth.RecallSpell || s is Spells.Seventh.GateTravelSpell || s is Spells.Chivalry.SacredJourneySpell)
        {
            m.SendLocalizedMessage(501802); // Thou can not recall from here.
            return false;
        }
        return base.OnBeginSpellCast(m, s);
    }
}
```

### Adding a Custom Spawn Region Override

```csharp
public class MyCustomRegion : BaseRegion
{
    public override void OnResource(Mobile m, SkillName skill, int amount)
    {
        if (skill == SkillName.Mining) amount += 5;  // +5 ore per swing
    }
}
```

### Adding a Per-Region Damage Modifier

```csharp
public class LavaRegion : DungeonRegion
{
    public override void OnDamage(Mobile m, ref int damage, DamageType type)
    {
        if (type == DamageType.Physical) damage += 5;  // 5 fire damage per tick
    }
}
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New region: `$type` is correct, `Map` references a registered map, `Area` is a valid polygon, `Priority` does not collide with overlapping regions, `MinExpansion`/`MaxExpansion` are appropriate.
- [ ] `OnBeginSpellCast` for new dungeons blocks Recall/Gate/Sacred Journey (or allows per facet).
- [ ] `OnDeath` correctly attributes kill credit (top-damage for champion spawns).
- [ ] `IsMobileAllowed` and `CanBeHarmful` are implemented for any region with non-standard entry/PvP rules.
- [ ] Travel-rule validation passes: Recall/Gate/Sacred Journey work in towns and wilderness, blocked in dungeons, blocked in champion spawn regions, blocked in Ilshenar entry.
- [ ] New champion spawn is wired with the right `Type` (Abyss, Arachnid, etc.), the level-scaling timer, and the `ChampionSpawnRegion` registration.
- [ ] New spawn package is in the right era folder and uses resolvable `type` names (`BaseCreature` subclasses).
- [ ] `Region` registration logs at startup do not show errors.
- [ ] Spatial queries in the new region use `GetItemsInRange` / `GetMobilesInRange`, not `World.Items` / `World.Mobiles`.
- [ ] Per-facet combat and travel differences are honored (Felucca PvP, Trammel safe, Ilshenar restricted, etc.).

## Related Skills

- `uo-combat-pipeline` - the combat rules that vary per facet (Felucca PvP, Trammel safe).
- `uo-magic-spells` - the spell cast pipeline that consults `Region.OnBeginSpellCast` for travel blocks.
- `uo-skills-stats-races` - the skill roster that varies per expansion (Bushido requires SE, Mysticism requires SA, etc.).
- `uo-items-foundation` - the Item and Mobile model that the spatial index manages.
- `uo-aos-item-properties` - the property bonuses that vary by region (e.g. resource bonuses).
- `uo-harvest-gathering-resources` - the `HarvestSystem` (Mining/Lumberjacking/Fishing) is the upstream of crafting; vein tables and bonus resources are the per-skill angle.
- `uo-housing-houses-multis` - the `BaseHouse` and `HouseRegion` system; house placement is a `Region` lifecycle question, and `NoHousingRegion` enforcement is the canonical per-facet housing rule.
- `modernuo-content-patterns` - canonical templates for new regions.
- `modernuo-era-expansion` - per-expansion map availability and `Core.<Era>` gating for regions.
- `www.uoguide.com/Facets` (offline reference) - the per-facet rules.
- `www.uoguide.com/Champion_spawn` (offline reference) - the spawn level scaling and reward tables.
- `www.uoguide.com/Factions` (offline reference) - the pre-Publish-86 faction system.
