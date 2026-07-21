# Content Taxonomy → ModernUO Mappings

Taxonomy concepts are design vocabulary. This reference maps each to the closest ModernUO type, data file, or pattern.

Paths are relative to the repo root unless noted.

> **Evidence boundary:** All paths and `Parity` cells below are repository-discovery notes, not official gameplay claims. Record the consuming repository revision and revalidate each named anchor before use; if an anchor is stale or absent, mark it `Unverified`. Establish `Present`, `Partial`, or `Gap` for production parity only with era-scoped official evidence.


---

## World

**Repository discovery summary (not official parity):** Core facets, regions, towns, and dungeons are present via `map-definitions.json` and `regions.json`. Decoration and spawner placement require manual `[Decorate]` / `[ImportSpawners]` — verify per-era dungeon access against UO.com world pages and non-authoritative discovery material Places.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| Facet | `Map` | `Projects/Server/Maps/Map.cs`, `Projects/Server/Maps/MapLoader.cs`, `Distribution/Data/map-definitions.json` | Repository observed | UO term "facet"; engine type is `Map` (`Felucca`, `Trammel`, etc.). Terrain/statics from client files via `TileMatrix`. |
| Region | `Region`, `BaseRegion` | `Projects/Server/Regions/Region.cs`, `Projects/UOContent/Regions/BaseRegion.cs`, `Distribution/Data/regions.json` | Repository observed | Hierarchical spatial rule volumes. Lookup: `Region.Find(loc, map)`. See `dev-docs/regions.md`. |
| Dungeon | `DungeonRegion` | `Projects/UOContent/Regions/DungeonRegion.cs`, `Distribution/Data/regions.json` (`"$type": "DungeonRegion"`) | Repository partial | No housing, dungeon lighting, young not protected. ML access (Prism, Grove, Palace) — see `mondains-legacy.md` open gaps. |
| Town | `TownRegion`, `GuardedRegion` | `Projects/UOContent/Regions/TownRegion.cs`, `Projects/UOContent/Regions/GuardedRegion.cs`, `Distribution/Data/regions.json` | Repository observed | Spatial towns: guards, travel restrictions, `Entrance`/`GoLocation`. Separate Factions `Town`/`TownDefinition` in `Engines/Factions/`. |
| StaticPlacement | `DecorationList`, `DecorationEntry`, client `TileMatrix` | `Projects/UOContent/Commands/Object Creation/Decorate.cs`, `Distribution/Data/Decoration/**/*.cfg` | Repository partial | Two layers: (1) client map statics via `TileMatrix`; (2) server decoration from `.cfg` via `[Decorate]` — not auto-loaded at startup. |
| MultiDefinition | `MultiData`, `MultiComponentList`, `MultiTileEntry` | `Projects/Server/Client/MultiData.cs` | Repository observed | House/addon component layouts from client `multi.mul`/`MultiCollection.uop`. `Distribution/Data/Components/*.txt` is housing verification tables, not multi defs. |
| TeleportLink | `TeleporterDefinition`, `Teleporter`, `WorldLocation` | `Projects/UOContent/Commands/Object Creation/GenTeleporter.cs`, `Projects/UOContent/Items/Misc/Teleporter.cs`, `Distribution/Data/teleporters.json` | Repository observed | JSON `src`/`dst`/`back` pairs. Generated via `[TelGen]` into invisible `Teleporter` items. |
| HousingArea | `HouseRegion`, `HousePlacement`, `NoHousingRegion` | `Projects/UOContent/Regions/HouseRegion.cs`, `Projects/UOContent/Multis/Houses/HousePlacement.cs`, `Projects/UOContent/Regions/NoHousingRegion.cs` | Repository observed | Placement legality: `HousePlacement.Check()`. Occupied footprint: dynamic `HouseRegion` per `BaseHouse`. Blocked zones in `regions.json`. |
| ResourceArea | `HarvestDefinition`, `HarvestBank`, `HarvestVein`, `HarvestSystem` | `Projects/UOContent/Engines/Harvest/` (`Mining.cs`, `Lumberjacking.cs`, `Fishing.cs`) | Repository observed | Harvestable areas are per-tile banks keyed by land/static tile IDs. `Region.GetResource()` can alter type by location. Reagent spawns: `Distribution/Data/Spawns/**/Reagents.json`. |

---

## Entity

**Repository discovery summary (not official parity):** Type-per-content pattern covers most OSI items and mobiles. Coverage is era-dependent — audit `dev-docs/eras/{expansion}.md` mobile/item tables for `Partial`/`Gap` rows.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| ItemDefinition | Item `Type` subclass + `ItemData` | `Projects/UOContent/Items/**`, `Projects/Server/TileData.cs`, `[Constructible]` in `Projects/Server/Attributes.cs` | Repository partial | Definition = C# class + ctor defaults. `ItemData` is client art/weight/flags metadata by `ItemID`. Full artifact catalog varies by era. |
| ItemInstance | `Item` | `Projects/Server/Items/Item.cs` | Repository observed | Runtime world object. Created via `[Constructible]` ctors, spawners, or loot. Registered with `World.AddEntity`. |
| MobileDefinition | Mobile `Type` subclass + `Body` | `Projects/UOContent/Mobiles/**`, `Projects/Server/Mobiles/Body.cs`, `Distribution/Data/bodyTable.cfg` | Repository partial | Definition = creature/NPC class + ctor stat setup. ML named monsters — several `Partial` in `mondains-legacy.md`. |
| MobileInstance | `Mobile`, `BaseCreature`, `PlayerMobile` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/UOContent/Mobiles/BaseCreature.cs`, `Projects/UOContent/Mobiles/PlayerMobile.cs` | Repository observed | Runtime mobile. Players use `PlayerMobile`; NPCs/monsters use `BaseCreature` subclasses. |
| SpawnerDefinition | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Repository partial | DTO-driven standard, region, and proximity spawners with focused JSON/import/cache tests. Package selection/reachability remains profile-specific; use `uo-spawners-world-population`. |
| ControllerDefinition | Engine controller subclasses | `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs`, `Projects/UOContent/Engines/Doom/GauntletSpawner.cs` | Repository partial | No generic controller type. Current main has no coherent `Engines/Peerless` controller/altar implementation; treat Peerless controller claims as research needed. |

---

## ItemSystem

**Repository discovery summary (not official parity):** AOS+ item property system is present. No central artifact registry — per-item classes. SA/TOL item sets and imbuing vary by era profile.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| ItemCategory | Class hierarchy + `TileFlag` | `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, `Container` under `Projects/UOContent/Items/` | Repository observed | No `ItemCategory` enum. Category is implicit from base class + `ItemData` flags. |
| ItemPropertyDefinition | `AosAttribute`, `AosElementAttribute`, attribute bags | `Projects/UOContent/Misc/AOS.cs`, `IAosItem` on gear classes | Repository observed | AOS property system: enum keys + `AosAttributes`/`AosWeaponAttributes` bags. Tooltip via `GetProperties`. |
| MaterialDefinition | `CraftResource`, `CraftResourceType`, `CraftAttributeInfo` | `Projects/UOContent/Misc/ResourceInfo.cs` | Repository observed | Material rules (resists, durability bonuses, runic ranges) in static `CraftAttributeInfo` tables. |
| DurabilityRule | `IDurability`, `IWearableDurability`, HP on gear | `Projects/UOContent/Items/Misc/IDurability.cs`, `WeaponDurabilityLevel`, `ArmorDurabilityLevel`, `HitPoints`/`MaxHitPoints` on `BaseWeapon`/`BaseArmor` | Repository observed | Durability = HP on wearables + level enums; `ScaleDurability`/`UnscaleDurability`. |
| LootType | `LootType` enum on `Item` | `Projects/Server/Items/Item.cs` | Repository observed | `Regular`, `Newbied`, `Blessed`, `Cursed` — controls steal/loot behavior. |
| EquipmentLayer | `Layer` enum | `Projects/Server/Items/Layer.cs`, `Mobile.Layers` equip logic | Repository observed | Client equip slot mapping (`OneHanded`, `Chest`, `Helm`, etc.). |
| ArtifactDefinition | Per-artifact item classes | `Projects/UOContent/Items/**/Artifacts/**`, `ArtifactRarity` on `BaseWeapon`/`BaseArmor` | Repository partial | No central artifact registry. Each artifact is typically a standalone subclass; rarity is a virtual int. |
| SetItemDefinition | `ArmorSetItem` enum, set fields on gear | `Projects/UOContent/Items/Armor/Sets/ArmorSetItem.cs`, `Projects/UOContent/Items/Sets/ItemSetHelper.cs` | Repository partial | Set membership + piece count + bonus application at equip time. ML sets documented in era doc. |

---

## MobileSystem

**Repository discovery summary (not official parity):** AI, loot, taming, and vendor patterns are mature. Current main contains ML creature/data surfaces but no coherent Peerless controller tree; do not infer a wired encounter or official boss behavior from creature classes alone.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| MobileCategory | `BodyType`, `Body` struct | `Projects/Server/Mobiles/Body.cs`, `Distribution/Data/bodyTable.cfg` | Repository observed | `IsAnimal`, `IsMonster`, `IsHuman`, `IsSea` from body table. Creature folders are organizational only. |
| AIProfile | `AIType`, `BaseAI` subclasses | `Projects/UOContent/Mobiles/AI/BaseAI/AIType.cs`, `MeleeAI`, `MageAI`, `AnimalAI`, `VendorAI` under `Mobiles/AI/` | Repository observed | Set in `BaseCreature` ctor (`AIType`, `FightMode`). `BaseAI` is the runtime behavior profile. |
| CreatureAbility | `MonsterAbility`, `MonsterAbilityGroup` | `Projects/UOContent/Mobiles/Abilities/MonsterAbility.cs`, concrete abilities (`FireBreath`, `PoisonGasAreaAttack`, etc.) | Repository partial | Registered via `GetMonsterAbilities()` on `BaseCreature`. ML bosses: many abilities `RuntimeBlocked`. |
| TamingProfile | Taming fields on `BaseCreature` | `Tamable`, `MinTameSkill`, `ControlSlots`, `FoodType`, `PackInstinct` on `BaseCreature`; `Projects/UOContent/Skills/AnimalTaming.cs` | Repository observed | Per-creature overrides in subclass ctors; ownership/orders/stables span `BaseCreature`, `BaseAI`, `AnimalTrainer`, and `PlayerMobile`. Use `uo-pets-taming-stables`. |
| VendorProfile | `BaseVendor`, `SBInfo`, `GenericBuyInfo` | `Projects/UOContent/Mobiles/Vendors/BaseVendor.cs`, `Projects/UOContent/Mobiles/Vendors/SBInfo/SBInfo.cs`, `VendorAI` | Repository observed | NPC stock and buy/sell behavior are distinct from persistent player-vendor listings/proceeds. Use `uo-vendors-commerce`. |
| TrainerProfile | `CanTeach`, `CheckTeach`, `Teach` on `BaseCreature` | Overrides on townfolk (`Noble.cs`, `WanderingHealer.cs`, `BaseVendor.cs`) | Repository observed | No `TrainerProfile` type. Skill training is virtual methods + per-NPC overrides. |
| LootProfile | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `GenerateLoot()` / `AddLoot()` on `BaseCreature` | Repository partial | Template packs + per-creature overrides. Do not infer Peerless reward distribution from named boss or artifact item classes; current-main controller/distribution anchors require research. |
| CorpseProfile | `Corpse`, death hooks on `BaseCreature` | `Projects/UOContent/Items/Misc/Corpses/Corpse.cs`, `OnDeath`, `DeleteCorpseOnDeath`, `CorpseName` on `BaseCreature` | Repository observed | Corpse creation hooked in `Corpse.Initialize()`. Death loot via `OnDeath(Container c)`. |

---

## Progression

**Repository discovery summary (not official parity):** Core skills and spell schools through ML are present. Current main contains Mysticism spell files and a TOL-gated Skill Mastery foundation with Intuition passive support; Imbuing and Throwing still require focused repository and official-source review before implementation claims.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| SkillDefinition | `SkillInfo`, `SkillName` | `Projects/UOContent/Skills/SkillsInfo.cs`, `Distribution/Data/skills.json`, `Projects/Server/Skills.cs` | Repository observed | Loaded from JSON at startup. UOContent registers callbacks and grouping helpers (`CombatSkills`, `CraftSkills`). |
| StatDefinition | `Stat`, `StatType`, `StatLockType`, `AosAttributes` | `Projects/Server/` stat types; `Mobile.SetStr/SetDex/SetInt` | Repository observed | No content-side stat catalog. Caps/influences via AOS in `SkillsInfo.Configure()`. |
| SpellDefinition | `Spell`, `SpellInfo`, `SpellRegistry` | `Projects/UOContent/Spells/`, `Projects/UOContent/Spells/Initializer.cs` | Repository partial | Each spell is a `Spell` subclass with ctor `SpellInfo`. SA/TOL spell coverage varies by profile. |
| AbilityDefinition | `WeaponAbility`, `SpecialMove` | `Projects/UOContent/Items/Weapons/Abilities/`, `Projects/UOContent/Spells/Base/SpecialMove.cs` | Repository observed | Weapon specials (primary/secondary) vs. Bushido/Ninjitsu moves in `SpellRegistry.SpecialMoves`. |
| MasteryDefinition | `MasterySystem`, `BookOfMasteries`, mastery gump | `Projects/UOContent/Spells/SkillMasteries/MasterySystem.cs`, `Projects/UOContent/Items/Skill Items/Magical/BookOfMasteries.cs`, `Projects/UOContent/Gumps/MasterySelectionGump.cs` | Repository partial | TOL-gated skill mastery learning/activation exists with Intuition passive for Bushido/Chivalry/Ninjitsu. Other mastery spells/effects require per-skill audit and official-source evidence. |
| VirtueDefinition | `VirtueName`, `VirtueLevel`, `VirtueSystem` | `Projects/UOContent/Engines/Virtues/` (`Honor.cs`, `Justice.cs`, etc.) | Repository observed | Enum + persistence; behavior split across per-virtue files and `VirtueContext`. |
| StatusEffectDefinition | `Poison`/`PoisonImpl`, `BuffIcon`, `BuffInfo` | `Projects/UOContent/Misc/Poison.cs`, `Projects/UOContent/Engines/BuffIcons/` | Repository observed | Debuffs/buffs: poison levels + client buff icons. Spells/abilities call `BuffInfo.AddBuff`. |
| TitleDefinition | `Titles`, `ChampionTitleSystem` | `Projects/UOContent/Misc/Titles.cs`, `Projects/UOContent/Engines/CannedEvil/ChampionTitleSystem.cs` | Repository observed | Fame/karma/skill titles in static tables; champion titles are separate persisted context. |

---

## EconomyCrafting

**Repository discovery summary (not official parity):** Core crafting professions and harvest systems are present. ML recipe distribution, BODs, and rare recipes flagged `Partial` in era docs.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| ResourceDefinition | `CraftResource`, `CraftResourceInfo`, `HarvestResource` | `Projects/UOContent/Misc/ResourceInfo.cs`, `Projects/UOContent/Engines/Harvest/Core/HarvestResource.cs` | Repository observed | Craft mats (metal/leather/wood/scales) vs. harvest output types with skill gates. |
| HarvestRule | `HarvestDefinition`, `HarvestSystem`, `HarvestVein` | `Projects/UOContent/Engines/Harvest/Core/`, `Mining.cs`, `Lumberjacking.cs`, `Fishing.cs` | Repository observed | Rules = tile ranges, veins, respawn, skill, messages, resource tables. |
| CraftRecipe | `CraftItem`, `CraftSystem` subclasses | `Projects/UOContent/Engines/Craft/Core/CraftItem.cs`, `DefBlacksmithy`, `DefTailoring`, etc. (`Engines/Craft/Def*.cs`) | Repository partial | Recipes registered in each `CraftSystem.InitCraftList()`. Rare recipe distribution — `Partial`. |
| ToolDefinition | `BaseTool`, `BaseHarvestTool` | `Projects/UOContent/Items/Skill Items/Tools/BaseTool.cs`, concrete tools (`Tongs`, `SewingKit`, `Pickaxe`) | Repository observed | Tools bind to a `CraftSystem` via `CraftSystem` property. |
| BulkOrderTemplate | `SmallBulkEntry`, `LargeBulkEntry`, profession BOD subclasses | `Projects/UOContent/Engines/Bulk Orders/`, `Distribution/Data/Bulk Orders/**/*.cfg`, `Projects/UOContent/Migrations/Server.Engines.BulkOrders.*.json` | Repository partial | Smith/Tailor and TOL-gated Alchemy, Inscription, Tinkering, Cooking, Fletching, and Carpentry paths exist in `BulkOrderSystem`; verify active era/profile, vendor reachability, reward calculator, and generated schema coverage. |
| VendorInventory | `VendorInventory` | `Projects/UOContent/Mobiles/Vendors/VendorInventory.cs`, `BaseHouse.VendorInventories` | Repository observed | Offline player-vendor stash on house deletion — not NPC shop stock. NPC stock is `SBInfo` under MobileSystem. |
| RewardStore | `RewardSystem`, `TreasuresOfTokuno` | `Projects/UOContent/Engines/Veteran Rewards/`, `Projects/UOContent/Engines/Treasures of Tokuno/` | Repository observed | Veteran-reward tables in code; Tokuno = point-based artifact redemption store. |
| CurrencyOrToken | `Gold`, `BankCheck`, `PromotionalToken` | `Projects/UOContent/Items/Misc/`, Tokuno points in `TreasuresOfTokuno` | Repository observed | Account gold on trade/deposit. Quest/promo tokens are item subclasses. |

---

## QuestNarrative

**Repository discovery summary (not official parity):** Dual quest engines (classic + ML). ML peerless access quests and key lifecycle have documented `Gap`/`Partial` rows. No dedicated `QuestStep` type.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| QuestDefinition | `MLQuest`, `QuestSystem` subclasses | `Projects/UOContent/Engines/ML Quests/Definitions/`, `Projects/UOContent/Engines/Quests/*/*Quest.cs` | Repository partial | Two parallel systems: ML (Mondain's Legacy) and pre-ML story quests. EJ profile ML pack loading — `Gap`. |
| QuestStep | *(no dedicated type)* | ML: objective list on `MLQuest` + `MLQuestInstance` state; classic: ordered `QuestConversation` list | Gap | No `QuestStep` class. Progress tracked via objective/conversation ordering. |
| QuestObjective | `QuestObjective`, `BaseObjective` subclasses | `Projects/UOContent/Engines/Quests/Core/QuestObjective.cs`, `CollectObjective`, `KillObjective`, `DeliverObjective` in `Engines/ML Quests/Objectives/` | Repository observed | Classic = abstract subclasses per quest; ML = composable objective types on quest defs. |
| QuestGiver | `IQuestGiver`, `BaseQuester` | `Projects/UOContent/Engines/ML Quests/IQuestGiver.cs`, `Projects/UOContent/Engines/Quests/Core/BaseQuester.cs` | Repository observed | ML questers implement `IQuestGiver`; classic questers extend `BaseQuester`. |
| QuestItemRequirement | `CollectObjective`, `DeliverObjective`, `QuestItem` | `Projects/UOContent/Engines/Quests/Core/Items/QuestItem.cs`, `Engines/ML Quests/Items/` | Repository observed | Requirements = type + count (+ destination for deliver). `QuestItem` enforces backpack rules. |
| DialogueNode | `QuestConversation` | `Projects/UOContent/Engines/Quests/Core/QuestConversation.cs`, per-quest `Conversations.cs` | Repository observed | Classic dialogue tree nodes. ML uses `TextDefinition` fields on `MLQuest` + `QuestConversationGump`. |
| RewardTable | `RewardSystem`, `BaseReward`/`ItemReward` | `Projects/UOContent/Engines/Veteran Rewards/`, `Projects/UOContent/Engines/ML Quests/Rewards/` | Repository observed | Veteran rewards = global categories; quest rewards = per-quest `List<BaseReward>`. |
| AccessUnlock | Quest context, items, regions, and teleporters | `Projects/UOContent/Engines/ML Quests/`, `Projects/UOContent/Engines/Quests/Regions/`, spawn/teleporter data | Unverified | Current main has no `PeerlessKeyDefinition` or `Engines/Peerless` anchor. Reconstruct each access chain from current quests/items/regions/data and official evidence before assigning status. |

---

## Encounter

**Repository discovery summary (not official parity):** Champion spawns and treasure maps have concrete controllers. Current main has ML boss creatures and dungeon spawn data but no coherent Peerless encounter controller/altar tree; Peerless lifecycle, access, and rewards remain research needed.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| SpawnTable | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Repository partial | DTO-backed weighted entries on world spawner items. Import/export, identity, cleanup, and era-package reachability belong to `uo-spawners-world-population`. |
| LootTable | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `Projects/UOContent/Misc/Loot.cs` | Repository observed | Static preset tables (`AosSuperBoss`, `Gems`, etc.). Creatures call `AddLoot(...)` in `GenerateLoot()`. |
| TreasureMapTemplate | `TreasureMap` | `Projects/UOContent/Items/Maps/TreasureMap.cs` | Repository observed | Level-driven: spawn types, chest location generation, guardian spawn. No external JSON template. |
| TreasureChestTemplate | `TreasureChestLevel1`–`4`, `TreasureMapChest` | `Projects/UOContent/Items/TreasureChests/`, `Projects/UOContent/Items/Containers/TreasureMapChest.cs` | Repository observed | Level chests hardcode trap/lock/loot in ctors. Map chests built when a map is dug up. |
| ChampionSpawnDefinition | `ChampionSpawnInfo`, `ChampionSpawnType` | `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs`, `ChampionSpawn.cs` | Repository partial | Static `ChampionSpawnInfo.Table[]`: champion type, per-level spawn types, cliloc names. Pre-ML coverage `Partial`. |
| BossEncounter | No generic current-main Peerless controller found | ML boss creature classes plus dungeon spawn/quest/item data | Unverified | Creature classes and spawn data do not establish an encounter state machine. Locate current access, controller, reward, cleanup, and test anchors before claiming implementation. |
| EventDefinition | `BaseScheduledEvent`, `EventScheduler` | `Projects/UOContent/Engines/Events/`, domain events (e.g. `TreasuresOfTokuno`) | Repository partial | Wall-clock scheduling with `IRecurrencePattern`. TOL/HS event coverage varies. |

---

## ClientPresentation

**Repository discovery summary (not official parity):** Server-side presentation uses client IDs (art, sound, cliloc, gumps). Client asset files are not in repo — parity is ID correctness, not asset fidelity. Third Dawn 3D client not emulated.

| Concept | ModernUO equivalent | Key paths | Repository discovery | Notes |
|---|---|---|---|---|
| ArtAsset | `Item.ItemID`, `Body`, `TileData` | `Projects/Server/Items/Item.cs`, `Projects/Server/Mobiles/Body.cs`, `Projects/Server/TileData.cs`, `Distribution/Data/bodyTable.cfg` | Repository observed | Item/mobile graphics are numeric IDs. No `ArtAsset` wrapper type. Client art files not in repo. |
| AnimationAsset | `Mobile.Animate`, `Animations` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/UOContent/Misc/Animations.cs` | Repository observed | Action IDs passed as `int` (e.g. bow=32). Creature anims tied to `Body`. |
| SoundAsset | `Mobile.PlaySound`, `Effects.PlaySound`, `BaseSoundID` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/Server/Effects.cs` | Repository observed | Sounds are raw client sound IDs. No `SoundAsset` class. |
| Hue | `Item.Hue`, `Mobile.Hue`, `HuePicker` | `Projects/Server/Items/Item.cs`, `Projects/Server/Mobiles/Mobile.cs`, `Projects/Server/HuePicker.cs` | Repository observed | 16-bit dye index on entities. `[Hue]` attribute for staff tools. |
| Gump | `BaseGump`, `Gump`, `DynamicGump`, `GumpLayoutBuilder` | `Projects/UOContent/Gumps/Base/`, `Projects/UOContent/Gumps/Base/GumpSystem.cs` | Repository observed | UI built in code. Gump graphics are client gumpart IDs. See `dev-docs/gump-system.md`. |
| ClilocString | `TextDefinition`, `Localization` | `Projects/Server/Text/TextDefinition.cs`, `Projects/Server/Localization/` | Repository observed | Cliloc = `TextDefinition.Of(number)` or `AddHtmlLocalized(cliloc, …)`. Loaded from client `cliloc.*`. |
| Icon | `BuffIcon`, `BuffInfo` | `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs`, `Projects/UOContent/Engines/BuffIcons/BuffInfo.cs` | Repository partial | Status-bar icons (SA+). Buff bar completeness vs. OSI — audit per profile. |

---

## Key Data Directories

| Path | Role |
|---|---|
| `Distribution/Data/map-definitions.json` | Facet registry |
| `Distribution/Data/regions.json` | Regions, towns, dungeons, housing blocks |
| `Distribution/Data/Locations/*.json` | GM Go-menu taxonomy (Towns/Dungeons POIs) |
| `Distribution/Data/teleporters.json` | Teleport link definitions |
| `Distribution/Data/Decoration/**/*.cfg` | Server-side static/item placement |
| `Distribution/Data/Spawns/**/*.json` | Creature/resource spawner definitions |
| `Distribution/Data/Bulk Orders/**/*.cfg` | Bulk order templates |
| `Distribution/Data/skills.json` | Skill definitions |
| `Distribution/Data/bodyTable.cfg` | Body → category mapping |
| Client `Data/` (map/static/multi/cliloc files) | Map statics, multi defs, localization — not in repo |

---

## Known Cross-Domain Gaps

Structural gaps that span multiple taxonomy domains. Era-specific detail: `dev-docs/eras/{expansion}.md` → **Open gaps**.

| Domain | Concept / topic | Status | Notes | Sources |
|---|---|---|---|---|
| Progression | SA/TOL Skill Masteries | Repository partial | `MasterySystem`, `BookOfMasteries`, and `MasterySelectionGump` exist; Intuition passive is implemented, while other mastery effects need per-skill verification | [UO.com Skill Mastery](https://uo.com/2015/08/26/publish-90-part-1-time-of-legends/), current repository scan |
| Progression | Mysticism, Imbuing, Throwing (SA) | Research needed | Mysticism spell files exist; no coherent Imbuing/Throwing implementation found in current main | Current repository scan plus official source required |
| QuestNarrative | `QuestStep` type | Gap | No dedicated class; objectives/conversations only | — |
| QuestNarrative | EJ profile ML quest/spawn packs | Gap | Not explicitly loaded in EJ profile | `mondains-legacy.md`, `endless-journey.md` |
| QuestNarrative | Peerless key expiration / master-key lifecycle | Research needed | No current-main Peerless key/controller anchor found | Current repository scan plus official source required |
| QuestNarrative | Prism of Light ticket access | Research needed | Reconstruct quest, item, teleporter, region, and spawn reachability before status | Current repository scan plus official source required |
| World | ML dungeon access placement | Repository partial | Grove, Palace, Prism access tests | `MondainsLegacySourceReferences` |
| MobileSystem | ML peerless boss live specials | Research needed | Boss creature classes do not prove live encounter hooks or official behavior | Current repository scan plus official source required |
| MobileSystem | MasterJonath, MasterMikael, CorruptedSoul | Repository partial | Named ML creatures | non-authoritative discovery material creature pages |
| Encounter | ML champion-style (Meraktus, etc.) | Repository partial | End-to-end encounter flow | non-authoritative discovery material [Meraktus](https://www.uoguide.com/Meraktus) |
| EconomyCrafting | Rare recipe / BOD / vendor distribution | Repository partial | ML crafting economy | non-authoritative discovery material [Recipe](https://www.uoguide.com/Recipe) |
| Entity | EJ vs ML baseline feature parity | Repository partial | Profile-dependent content activation | `endless-journey.md` |
| Encounter | TOL / HS event coverage | Repository partial | Audit `Core.TOL` / `Core.HS` gates | `time-of-legends.md`, `high-seas.md` |
| World | Third Dawn 3D client | Gap | Network-layer 3D not emulated | `third-dawn.md` |
| ClientPresentation | Buff bar completeness (SA+) | Repository partial | Not all OSI buff/debuff icons | UO.com client wiki |

**Enhanced examples** (intentional, not gaps):

- Configured-project era/profile tuning versus official publish behavior
- Deterministic test seams that are verified in the current branch and clearly separated from live hooks
- `RuntimeBlocked` mechanics only when concrete implementation and the blocking registration/data/profile surface are both evidenced

See [parity-check.md](parity-check.md) for report template and workflow.
