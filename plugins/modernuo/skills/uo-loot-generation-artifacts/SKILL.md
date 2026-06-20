---
name: "uo-loot-generation-artifacts"
description: "Use when working with the UO loot generation system in ModernUO/RebirthUO servers - LootPack, LootPackEntry, TypeRandom treasure rolls, Champion Spawn artifacts, Peerless artifacts, ML minor artifacts, Treasure Maps (Stash/Supply/Cache/Hoard/Trove), Cartography decoding, chest mob spawns, Paragon monsters, monster corpse loot generation, and the per-tier roll tables. Use when adding a new monster, adjusting drop rates, wiring treasure map chests, debugging why a boss does not drop the right artifact, or building a custom loot table."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Loot Generation & Artifacts

## Overview

The UO loot system is the bridge between "I killed a monster" and "I have a glowing katana in my backpack". The engine splits loot generation into four layers:

1. **LootPack** rolls a tier-based table when a monster dies (`Projects/UOContent/Misc/Loot.cs`).
2. **Treasure Map** decoding turns a tattered map into a chest with its own roll table (`Projects/UOContent/Items/Treasure Maps/`).
3. **Champion Spawn** artifact roll distributes artifacts to the top damage dealers on champ/peerless kills.
4. **ML minor artifacts** are flat, mostly bound items dropped by bosses and event creatures.

The loot table is data-driven: each `LootPack` holds a list of `LootPackEntry` items, each with a `Chance` and a `Type` or `ItemConstructor` resolver. The engine rolls the table when `ApplyLoot(Mobile from, Mobile killer, LootPack pack)` is called from the monster's death pipeline.

This skill covers the four layers, the `TypeRandom` resolver, the per-era loot pack naming convention (`Poor`/`Meager`/`Average`/`Rich`/`FilthyRich`/`UltraRich`/`SuperBoss`/`Meager` SA variants), Champion Spawn artifacts, ML minor artifacts, treasure map chest mechanics, Paragon monsters, and the per-monster loot generation hook.

## When to Use

- Adding a new monster with its own loot table.
- Debugging why a monster does not drop a specific item.
- Wiring a Champion Spawn to drop the right reward set.
- Adding a new Treasure Map tier (or adjusting the chest's spawn pool).
- Adding a new Peerless boss artifact.
- Auditing the loot generation to match an era's per-monster drop rates.
- Implementing a custom loot table for a custom boss.

Don't use for:

- Base item/mobile entity model (use `uo-items-foundation`).
- Item property containers (use `uo-aos-item-properties`).
- The combat damage pipeline (use `uo-combat-pipeline`).
- The quest reward system (use `uo-quests-engine-ml`).
- BOD reward selection (use `uo-bulk-orders-bod`).

## The LootPack Class

`Projects/UOContent/Misc/Loot.cs` defines the central `LootPack` class and its `LootPackEntry` items. A `LootPack` is a static definition: each entry has a probability (e.g. `0.10` = 10%) and a constructor (either a `Type` reference for a fixed item class or a `TypeRandom` for a roll across multiple types).

The engine exposes a tier-based naming convention used across monster profiles. Per the `server-engine-knowledge-base.md` and `uo-crafting-recipes-resources`:

| Pack | Typical use | Note |
|---|---|---|
| `Poor` | Trivial monsters (rats, birds) | 0.05-0.20 probability of low-tier items. |
| `Meager` | Easy monsters (mongbats, skeletons) | Common 1-3 gp items, low armor pieces. |
| `Average` | Mid-tier monsters (lizardmen, orcs) | Mixed gear, sometimes a weapon. |
| `Rich` | Tough monsters (ogres, ogre lords) | Higher-value gear, some magical items. |
| `FilthyRich` | Endgame PvE (dragons, balrons) | High-value magic items, occasional artifacts. |
| `UltraRich` | Boss-tier monsters (Balron, Ancient Wyrm) | Per-tier named artifacts. |
| `SuperBoss` | Peerless-tier bosses | Always drops the boss's named artifact, plus secondary. |
| `SePoor`/`SeMeager`/... | SE-introduced variants | Adjusted for SE-era loot pools. |
| `MlRich`/`MlFilthyRich`/... | ML-introduced variants | Adjusted for ML-era loot pools. |
| `SaRich`/... | SA-introduced variants | Adjusted for SA-era loot pools. |

The pack is selected by `BaseCreature` based on its `FightMode`, `Fame`, and `Karma`, plus era flags. The actual roll is per-entry: each `LootPackEntry` has a `Chance` and the engine rolls `Utility.RandomDouble() < entry.Chance` to decide whether to add that item.

## How Loot Generation Runs

When a `BaseCreature` dies, the engine calls `BaseCreature.OnDeath` (or `BaseCreature.Damage` in the case of `LootType.Cursed` / unlootable cases). The relevant call path:

```
BaseCreature.OnDeath(corpse)
 ├─ if Paragon: AddParagonLoot
 ├─ LootPack.ApplyLoot(killer, corpse, this.LootPack)  // default pack
 ├─ if Champion: ChampionArtifactRoll
 ├─ if Peerless: TryDropLoot(PeerlessArtifactTable)
 └─ for each killed damage entry: TryDropLoot(LootType.MLMinorArtifact)
```

`LootPack.ApplyLoot` walks the entries and, for each successful roll, calls `entry.Construct()` to materialize the item, then places it in the corpse's backpack or drops it on the corpse.

For Paragon monsters, the loot is amplified: the engine rolls a separate "Paragon boost" that can add a magic item, an essence, or a rare drop. The Paragon chance is gated by a `BaseCreature` constructor parameter (`Paragons = true`) and the era flag.

## Per-Monster Loot Configuration

The `BaseCreature` constructor accepts a `LootPack` parameter. The standard pattern is:

```csharp
[Constructible]
public ForestOgre() : base(AIType.AI_Melee, FightMode.Closest)
{
    Body = 1;  // Ogre
    ...
    SetDamage(8, 16);
    SetResistance(ResistanceType.Physical, 30);
    ...
    LootPack.Rich.Generate(this);  // <-- here
}
```

The `LootPack.Rich` is the static field that drives the tier. The `Generate(this)` call populates the monster's internal `LootPack` for the death roll.

Custom bosses override `LootPack` directly:

```csharp
public class DreadHorn : BaseCreature
{
    [Constructible]
    public DreadHorn() : base(...)
    {
        ...
        LootPack.SuperBoss.Generate(this);  // Peerless boss
        // Add custom rolls:
        m_DropArtifacts.Add(new PeerlessArtifactEntry(...));
    }
}
```

The `m_DropArtifacts` field on `BaseCreature` is the per-creature override that takes priority over the standard `LootPack` roll for boss-tier monsters.

## TypeRandom and Cross-Pack Rolls

`TypeRandom` is the resolver for entries that pull from a pool of types (e.g. "roll 1 random weapon from the 30 tier-1 weapon types"). The pattern:

```csharp
new LootPackEntry(0.05, new TypeRandom(typeof(Katana), typeof(LongSword), typeof(Broadsword), ...))
```

`TypeRandom` rolls uniformly across the listed types. It's used heavily in the standard packs to keep the loot varied without writing 30 individual entries.

For magic items, the engine uses `LootPackItem` (an item constructor) which can set `AosAttribute` values via a `MagicEquipmentPacker` or roll from a `BaseAttributes` instance. The `LootPackEntry` constructor accepts a `Func<>` that returns the item instance:

```csharp
new LootPackEntry(0.02, () => LootPackItem.MagicItem(1, 3, 1, 3, 50.0))
```

## Treasure Maps

`Projects/UOContent/Items/Treasure Maps/` covers the 5-level map system. Per `www.uoguide.com/Treasure_Map`:

| Level | Name (current) | Name (legacy) | Mob difficulty |
|---:|---|---|---|
| 1 | Stash | Plainly Drawn | Easy |
| 2 | Supply | Expertly/Adeptly Drawn | Medium-easy |
| 3 | Cache | Cleverly/Deviously Drawn | Medium |
| 4 | Hoard | Ingeniously Drawn | Hard |
| 5 | Trove | Diabolically Drawn | Boss-tier |

A map is a `TreasureMap` item with `Level = 1..5`. The player decodes it via `Cartography` (double-click). The `Cartography` skill also affects the digging radius:

| Cartography | Dig radius |
|---|---|
| 0 | 1 tile |
| 51 | 2 tiles |
| 81 | 3 tiles |
| 100 | 4 tiles |

Below 50 Cartography, the chest spawns with a "Rusty" tag and reduced quality loot.

When decoded, the map reveals the chest's location (a `Point3D`). The player uses a `Shovel` to dig, which spawns a `TreasureChest` (`Projects/UOContent/Items/Treasure Maps/TreasureChest.cs`). The chest has a `Level` (1-5) and a `Facet` (Felucca, Trammel, Ilshenar, Malas, Tokuno, Ter Mur, Eodon). The chest is locked; opening it requires `Lockpicking` (the Magery spell "Unlock" works for Stash/Supply/Cache).

The chest's contents are determined by a `LootPack` plus a `Level`-dependent bonus table. The 5 chest professions (Artisan, Assassin, Mage, Ranger, Warrior) determine the drop specialty (weapons vs armor vs reagents vs scrolls).

When a mob-spawning chest is opened, mobs spawn based on the chest's level (e.g. Level 5 spawns Lizardmen, Drakes, Wyverns). A `Grubber` spawns on a failed Lockpicking attempt and steals one random item from the chest.

The chest has a duration: per the UOAlive notes (and older OSI documentation), 1 hour for Levels 1-7, 2 hours for Level 8 (Lore Boss Chests). After expiry, the chest deletes with its contents.

`Davies' Locker` is a Veteran Reward that reveals the chest's exact coordinates. `Legendary Mapmaker's Glasses` increase Cartography (and thus digging radius and chest quality).

## Champion Spawn Artifacts

Champion Spawns (`Projects/UOContent/Engines/ChampionSpawn/`) drop Champion Spawn Artifacts on Champion kill. The drop rates (per `www.uoguide.com/Champion_spawn`):

- 30% overall drop chance
- 10% Replica (shared reward)
- 15% Decorative reward
- 5% Unique reward

The artifact list is `Projects/UOContent/Items/Champion Artifacts/`. The unique artifacts (per the Champion type) are themed: Forest Lord drops `Quiver of Rage` / `Bow of the Juka King` / etc., Undead Terror drops `Bonecrusher` / `Skullcrusher` / etc. The Replica tier is a themed shared reward (e.g. a decorative shield).

The `ChampionSpawn.OnChampionKilled` callback fires after the Champion dies; it runs the artifact roll and distributes the items to the top damage dealers. The same top-damage logic that distributes Power Scrolls is reused.

## ML Peerless Artifacts

The 6 ML Peerless bosses (Dread Horn, Shimmering Effusion, Travesty, Lady Melisande, Chief Paroxysmus, Monstrous Interred Grizzle) each have a unique artifact table. The mapping is in `Projects/UOContent/Misc/MLPeerlessArtifacts.cs`:

| Boss | Key artifact |
|---|---|
| Dread Horn | Dread Horn's Mane, Crop of the Evergrowth, ... |
| Shimmering Effusion | Pendant of the Shimmering Effusion, ... |
| Travesty | Travesty's Sideshow, ... |
| Lady Melisande | Melisande's Lacerating Wind, ... |
| Chief Paroxysmus | Paroxysmus' Dinner Bell, ... |
| Monstrous Interred Grizzle | Grizzle's Subjugation, ... |

`MLPeerlessArtifactsTests` covers the official source mapping, source counts/enumeration, factories, boss source constants, the tracked official source URL, representative artifact item profiles, and every mapped artifact being a generated-serializable constructible item.

`MLPeerlessArtifacts.cs` calls `TryDropLoot` on `BaseCreature.OnDeath` for the boss creature; the boss-specific artifact roll keeps the Peerless artifact, and the central ML minor artifact corpse roll is invoked for the secondary tier.

## ML Minor Artifacts

The ML minor artifact pool is a flat list of mid-tier items, all with `LootType.Blessed` (no-drop, no-steal). They drop from a wide variety of monsters with a small chance. The list is in `Projects/UOContent/Items/ML Minor Artifacts/`. Each artifact is an `Item` with a fixed hue and a small stat bonus.

The drop rate per kill is low (0.1-1%) and is gated by the `LootPack.SuperBoss` roll plus the central `MLMinorArtifact` roll. The `MLMinorArtifactTests` covers the artifact profiles, race restrictions (Robes of the Equinox are Elves-Only, Robes of the Eclipse are all-races), and the ML minor artifact flags for ML-gated items.

Some artifacts are race-restricted:

- Robe of the Equinox: Elves Only
- Robe of the Eclipse: All Races
- Aegis of Grace, Fey Leggings, Helm of Swiftness: All-races Peerless variants
- Flesh Ripper: one-handed, Mage Slayer tooltip, mage-target slayer behavior

## Paragon Monsters

`BaseCreature.Paragons` is a boolean flag set on specific monster types. A Paragon monster has boosted stats (HP, damage, resists) and a glowing hue. On death, it rolls an additional `LootPack` with a higher-tier roll and a small chance of dropping a Paragon-specific item (a "heart" or "essence" type item).

The Paragon chance is the per-monster base rate multiplied by the active facet. Ilshenar is the canonical Paragon facet, but any facet can spawn Paragons if the `Map` is enabled for them.

## Peerless Altar Loot Window

The 6 ML Peerless altars (`Projects/UOContent/Engines/Peerless/`) have a 10-minute post-kill loot window (`PeerlessAltar.CompleteEncounter`):

- Boss dies → `LootWindowState` set.
- 10 minutes pass → tracked participants ejected to exit teleporter (or altar fallback).
- During the window, the corpse can be looted by tracked participants; the boss artifact is in the corpse.

`Dread Horn` and `Travesty` have static `PeerlessExitTeleporter` spawn data. The other 4 altars use the altar fallback. `PeerlessExitTeleporterTests` covers the encounter-only exits, the altar fallback, and the participant/pet cleanup.

## Common Pitfalls

1. **Calling `AddItem` to the corpse directly instead of `LootPack.ApplyLoot`.** The corpse item is `Corpse`, and adding items directly skips the loot table logic, the karma-based roll, the blessed status, the `Owner` attribution, and the special-case logic for ML artifacts. Use `ApplyLoot` to keep the pipeline consistent.
2. **Setting `LootType.Blessed` on a Peerless artifact.** The Peerless artifact should be `LootType.Regular` so the killer can loot the corpse. The ML minor artifact is the one that's `Blessed`.
3. **Adding a `LootPackEntry` with `Chance = 1.0` for an artifact.** This forces a 100% drop, which the boss loot code overrides. Boss artifacts should be added to `m_DropArtifacts` separately, not as a `LootPackEntry` with 100% chance.
4. **Forgetting the `LootPack.Generate(this)` call in the constructor.** Without it, the monster rolls an empty loot table and the player gets no drops.
5. **Using `World.Items.Add` for treasure chest placement.** Use `TreasureChest.Spawn` (or the equivalent helper) which validates the location, sets the chest's `Facet` and `Level`, and applies the dig-radius rules.
6. **Setting the chest's `Level` to 0.** Level 0 is a bug; chests are 1-5 (or 8 for Lore Boss Chests). The chest rolls an invalid pack.
7. **Hardcoding `Utility.RandomMinMax(1, 100)` for drop rates.** Use the `LootPackEntry` table and the `Chance` field; the engine respects the era pack naming convention.
8. **Not adding the `LootType` field to the artifact item.** Some artifacts need `LootType.Regular`, others need `Blessed`. The default is `Regular`; if a custom artifact is meant to be no-drop, it must set `LootType.Blessed` in the constructor.
9. **Wiring the Champion artifact to the wrong spawn type.** The `ChampionSpawn.OnChampionKilled` callback is for the Champion itself; the `BaseCreature.OnDeath` artifact roll is for individual adds. Mixing them produces double-drops or no-drops.
10. **Forgetting to update the `LootPackEntry.Construct` callback for new item types.** The `LootPackEntry` constructor takes a `Func<>`; the function must return a fresh `Item` instance, not a static cached one. Loot generation in a hot path (champ spawn add kills) cannot share item instances.

## Common Recipes

### Adding a New Monster Loot

```csharp
[Constructible]
public class GrizzlyBear : BaseCreature
{
    [Constructible]
    public GrizzlyBear() : base(AIType.AI_Melee, FightMode.Closest)
    {
        Body = 212;
        ...
        SetDamage(6, 12);
        ...
        LootPack.Meager.Generate(this);  // <-- standard table
    }
}
```

### Adding a Boss-Grade Monster

```csharp
[Constructible]
public class CustomBoss : BaseCreature
{
    [Constructible]
    public CustomBoss() : base(AIType.AI_Melee, FightMode.Closest)
    {
        ...
        LootPack.SuperBoss.Generate(this);
        m_DropArtifacts.Add(new BossArtifactEntry(typeof(SpecialSword), 1.0));
    }
}
```

### Adding a New Treasure Map Tier

For most cases, the 5 levels (Stash-Trove) are sufficient. To add a new level (e.g. an event-only "Lore" level), the changes are:

1. Add the level to `TreasureMapLevel` enum.
2. Add a new `TreasureMap` constructor variant.
3. Add a new `TreasureChest` constructor with the matching level.
4. Add the chest profession and loot table to the chest's `Generate` method.
5. Test the level in `TreasureMapTests`.

### Wiring a Custom Loot Roll for an Event Boss

```csharp
public class EventBoss : BaseCreature
{
    [Constructible]
    public EventBoss() : base(...)
    {
        ...
        LootPack.FilthyRich.Generate(this);
        // Add the custom event drop:
        m_DropArtifacts.Add(new BossArtifactEntry(typeof(EventRewardItem), 0.5));  // 50% chance
    }
}
```

### Adding a New ML Minor Artifact

1. Create the `Item` subclass in `Projects/UOContent/Items/ML Minor Artifacts/`.
2. Set `LootType.Blessed` in the constructor.
3. Add the type to the central `MLMinorArtifactType` enum.
4. Add the type to the drop pool used by the central `MLMinorArtifact` roll.
5. Test the artifact profile in `MLMinorArtifactTests`.

## Verification Checklist

- [ ] `dotnet build` succeeds.
- [ ] New monster: `LootPack.<Tier>.Generate(this)` is called in the constructor; the tier matches the monster's `FightMode`/`Fame`/`Karma`.
- [ ] New artifact: `LootType` is set (Regular for looted, Blessed for ML minor), `DefaultName` is set, `Hue` is set if the artifact is themed, `[Constructible]` is present.
- [ ] Peerless artifact: registered in `MLPeerlessArtifacts.cs` mapping, factory exists, `m_DropArtifacts` includes the artifact.
- [ ] Champion artifact: dropped via the `ChampionSpawn.OnChampionKilled` callback, not as a direct `AddItem`.
- [ ] Treasure map: decoded via `Cartography`, chest has the right `Level` (1-5), drop pool is wired.
- [ ] Paragon monster: `Paragons = true` set, `LootPack` includes the Paragon boost.
- [ ] Loot generation tests pass (the relevant `*LootTests.cs` or `*ArtifactTests.cs`).
- [ ] No `AddItem` on corpses; the loot generation uses the LootPack pipeline.
- [ ] No direct `World.Items.Add` for chests; the chest spawn helper is used.
- [ ] For an item that is meant to drop multiple times, the `MaxAmount` on the entry is set correctly.
- [ ] The `LootPackEntry.Chance` is a probability, not a percentage: 0.05 = 5%, not 5.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the `Item` model that the loot system creates.
- `uo-aos-item-properties` - the property rolls used to generate magical items.
- `uo-crafting-recipes-resources` - the recipe/crafting system that produces items that the loot table can drop.
- `uo-combat-pipeline` - the death pipeline that triggers loot generation.
- `uo-magic-spells` - spell drops from named creatures.
- `uo-world-facets-regions` - the facet-based loot differences (Felucca-only drops, per-facet resources).
- `uo-skills-stats-races` - the `Fame`/`Karma` system that drives the loot tier.
- `modernuo-content-patterns` - canonical templates for new items, including artifacts.
- `modernuo-era-expansion` - per-era `LootPack` naming convention.
- `www.uoguide.com/Treasure_Map` (offline reference) - the 5-tier map system, Cartography radius, chest professions.
- `www.uoguide.com/Champion_spawn` (offline reference) - the 30% artifact drop rate, top-damage dealer attribution.
- `docs/mondains-legacy-content-matrix.md:70` (offline reference) - the ML Peerless artifact list and `MLPeerlessArtifactsTests` baseline.
