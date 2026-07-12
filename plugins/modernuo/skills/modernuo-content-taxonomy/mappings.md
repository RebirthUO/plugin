# Content Taxonomy → ModernUO Mappings

Taxonomy concepts are design vocabulary. This reference maps each to the closest ModernUO type, data file, or pattern.

Paths are relative to the repo root unless noted.

---

## World

**Parity summary:** Core facets, regions, towns, and dungeons are present via `map-definitions.json` and `regions.json`. Decoration and spawner placement require manual `[Decorate]` / `[ImportSpawners]` — verify per-era dungeon access against UO.com world pages and UOGuide Places.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| Facet | `Map` | `Projects/Server/Maps/Map.cs`, `Projects/Server/Maps/MapLoader.cs`, `Distribution/Data/map-definitions.json` | Present | UO term "facet"; engine type is `Map` (`Felucca`, `Trammel`, etc.). Terrain/statics from client files via `TileMatrix`. |
| Region | `Region`, `BaseRegion` | `Projects/Server/Regions/Region.cs`, `Projects/UOContent/Regions/BaseRegion.cs`, `Distribution/Data/regions.json` | Present | Hierarchical spatial rule volumes. Lookup: `Region.Find(loc, map)`. See `dev-docs/regions.md`. |
| Dungeon | `DungeonRegion` | `Projects/UOContent/Regions/DungeonRegion.cs`, `Distribution/Data/regions.json` (`"$type": "DungeonRegion"`) | Partial | No housing, dungeon lighting, young not protected. ML access (Prism, Grove, Palace) — see `mondains-legacy.md` open gaps. |
| Town | `TownRegion`, `GuardedRegion` | `Projects/UOContent/Regions/TownRegion.cs`, `Projects/UOContent/Regions/GuardedRegion.cs`, `Distribution/Data/regions.json` | Present | Spatial towns: guards, travel restrictions, `Entrance`/`GoLocation`. Separate Factions `Town`/`TownDefinition` in `Engines/Factions/`. |
| StaticPlacement | `DecorationList`, `DecorationEntry`, client `TileMatrix` | `Projects/UOContent/Commands/Object Creation/Decorate.cs`, `Distribution/Data/Decoration/**/*.cfg` | Partial | Two layers: (1) client map statics via `TileMatrix`; (2) server decoration from `.cfg` via `[Decorate]` — not auto-loaded at startup. |
| MultiDefinition | `MultiData`, `MultiComponentList`, `MultiTileEntry` | `Projects/Server/Client/MultiData.cs` | Present | House/addon component layouts from client `multi.mul`/`MultiCollection.uop`. `Distribution/Data/Components/*.txt` is housing verification tables, not multi defs. |
| TeleportLink | `TeleporterDefinition`, `Teleporter`, `WorldLocation` | `Projects/UOContent/Commands/Object Creation/GenTeleporter.cs`, `Projects/UOContent/Items/Misc/Teleporter.cs`, `Distribution/Data/teleporters.json` | Present | JSON `src`/`dst`/`back` pairs. Generated via `[TelGen]` into invisible `Teleporter` items. |
| HousingArea | `HouseRegion`, `HousePlacement`, `NoHousingRegion` | `Projects/UOContent/Regions/HouseRegion.cs`, `Projects/UOContent/Multis/Houses/HousePlacement.cs`, `Projects/UOContent/Regions/NoHousingRegion.cs` | Present | Placement legality: `HousePlacement.Check()`. Occupied footprint: dynamic `HouseRegion` per `BaseHouse`. Blocked zones in `regions.json`. |
| ResourceArea | `HarvestDefinition`, `HarvestBank`, `HarvestVein`, `HarvestSystem` | `Projects/UOContent/Engines/Harvest/` (`Mining.cs`, `Lumberjacking.cs`, `Fishing.cs`) | Present | Harvestable areas are per-tile banks keyed by land/static tile IDs. `Region.GetResource()` can alter type by location. Reagent spawns: `Distribution/Data/Spawns/**/Reagents.json`. |

---

## Entity

**Parity summary:** Type-per-content pattern covers most OSI items and mobiles. Coverage is era-dependent — audit `dev-docs/eras/{expansion}.md` mobile/item tables for `Partial`/`Gap` rows.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| ItemDefinition | Item `Type` subclass + `ItemData` | `Projects/UOContent/Items/**`, `Projects/Server/TileData.cs`, `[Constructible]` in `Projects/Server/Attributes.cs` | Partial | Definition = C# class + ctor defaults. `ItemData` is client art/weight/flags metadata by `ItemID`. Full artifact catalog varies by era. |
| ItemInstance | `Item` | `Projects/Server/Items/Item.cs` | Present | Runtime world object. Created via `[Constructible]` ctors, spawners, or loot. Registered with `World.AddEntity`. |
| MobileDefinition | Mobile `Type` subclass + `Body` | `Projects/UOContent/Mobiles/**`, `Projects/Server/Mobiles/Body.cs`, `Distribution/Data/bodyTable.cfg` | Partial | Definition = creature/NPC class + ctor stat setup. ML named monsters — several `Partial` in `mondains-legacy.md`. |
| MobileInstance | `Mobile`, `BaseCreature`, `PlayerMobile` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/UOContent/Mobiles/BaseCreature.cs`, `Projects/UOContent/Mobiles/PlayerMobile.cs` | Present | Runtime mobile. Players use `PlayerMobile`; NPCs/monsters use `BaseCreature` subclasses. |
| SpawnerDefinition | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Partial | DTO-driven standard, region, and proximity spawners with focused JSON/import/cache tests. Package selection/reachability remains profile-specific; use `uo-spawners-world-population`. |
| ControllerDefinition | Engine controller subclasses | `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs`, `Projects/UOContent/Engines/Doom/GauntletSpawner.cs` | Partial | No generic controller type. Current main has no coherent `Engines/Peerless` controller/altar implementation; treat Peerless controller claims as research needed. |

---

## ItemSystem

**Parity summary:** AOS+ item property system is present. No central artifact registry — per-item classes. SA/TOL item sets and imbuing vary by era profile.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| ItemCategory | Class hierarchy + `TileFlag` | `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, `Container` under `Projects/UOContent/Items/` | Present | No `ItemCategory` enum. Category is implicit from base class + `ItemData` flags. |
| ItemPropertyDefinition | `AosAttribute`, `AosElementAttribute`, attribute bags | `Projects/UOContent/Misc/AOS.cs`, `IAosItem` on gear classes | Present | AOS property system: enum keys + `AosAttributes`/`AosWeaponAttributes` bags. Tooltip via `GetProperties`. |
| MaterialDefinition | `CraftResource`, `CraftResourceType`, `CraftAttributeInfo` | `Projects/UOContent/Misc/ResourceInfo.cs` | Present | Material rules (resists, durability bonuses, runic ranges) in static `CraftAttributeInfo` tables. |
| DurabilityRule | `IDurability`, `IWearableDurability`, HP on gear | `Projects/UOContent/Items/Misc/IDurability.cs`, `WeaponDurabilityLevel`, `ArmorDurabilityLevel`, `HitPoints`/`MaxHitPoints` on `BaseWeapon`/`BaseArmor` | Present | Durability = HP on wearables + level enums; `ScaleDurability`/`UnscaleDurability`. |
| LootType | `LootType` enum on `Item` | `Projects/Server/Items/Item.cs` | Present | `Regular`, `Newbied`, `Blessed`, `Cursed` — controls steal/loot behavior. |
| EquipmentLayer | `Layer` enum | `Projects/Server/Items/Layer.cs`, `Mobile.Layers` equip logic | Present | Client equip slot mapping (`OneHanded`, `Chest`, `Helm`, etc.). |
| ArtifactDefinition | Per-artifact item classes | `Projects/UOContent/Items/**/Artifacts/**`, `ArtifactRarity` on `BaseWeapon`/`BaseArmor` | Partial | No central artifact registry. Each artifact is typically a standalone subclass; rarity is a virtual int. |
| SetItemDefinition | `ArmorSetItem` enum, set fields on gear | `Projects/UOContent/Items/Armor/Sets/ArmorSetItem.cs`, `Projects/UOContent/Items/Sets/ItemSetHelper.cs` | Partial | Set membership + piece count + bonus application at equip time. ML sets documented in era doc. |

---

## MobileSystem

**Parity summary:** AI, loot, taming, and vendor patterns are mature. Current main contains ML creature/data surfaces but no coherent Peerless controller tree; do not infer a wired encounter or official boss behavior from creature classes alone.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| MobileCategory | `BodyType`, `Body` struct | `Projects/Server/Mobiles/Body.cs`, `Distribution/Data/bodyTable.cfg` | Present | `IsAnimal`, `IsMonster`, `IsHuman`, `IsSea` from body table. Creature folders are organizational only. |
| AIProfile | `AIType`, `BaseAI` subclasses | `Projects/UOContent/Mobiles/AI/BaseAI/AIType.cs`, `MeleeAI`, `MageAI`, `AnimalAI`, `VendorAI` under `Mobiles/AI/` | Present | Set in `BaseCreature` ctor (`AIType`, `FightMode`). `BaseAI` is the runtime behavior profile. |
| CreatureAbility | `MonsterAbility`, `MonsterAbilityGroup` | `Projects/UOContent/Mobiles/Abilities/MonsterAbility.cs`, concrete abilities (`FireBreath`, `PoisonGasAreaAttack`, etc.) | Partial | Registered via `GetMonsterAbilities()` on `BaseCreature`. ML bosses: many abilities `RuntimeBlocked`. |
| TamingProfile | Taming fields on `BaseCreature` | `Tamable`, `MinTameSkill`, `ControlSlots`, `FoodType`, `PackInstinct` on `BaseCreature`; `Projects/UOContent/Skills/AnimalTaming.cs` | Present | Per-creature overrides in subclass ctors; ownership/orders/stables span `BaseCreature`, `BaseAI`, `AnimalTrainer`, and `PlayerMobile`. Use `uo-pets-taming-stables`. |
| VendorProfile | `BaseVendor`, `SBInfo`, `GenericBuyInfo` | `Projects/UOContent/Mobiles/Vendors/BaseVendor.cs`, `Projects/UOContent/Mobiles/Vendors/SBInfo/SBInfo.cs`, `VendorAI` | Present | NPC stock and buy/sell behavior are distinct from persistent player-vendor listings/proceeds. Use `uo-vendors-commerce`. |
| TrainerProfile | `CanTeach`, `CheckTeach`, `Teach` on `BaseCreature` | Overrides on townfolk (`Noble.cs`, `WanderingHealer.cs`, `BaseVendor.cs`) | Present | No `TrainerProfile` type. Skill training is virtual methods + per-NPC overrides. |
| LootProfile | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `GenerateLoot()` / `AddLoot()` on `BaseCreature` | Partial | Template packs + per-creature overrides. Do not infer Peerless reward distribution from named boss or artifact item classes; current-main controller/distribution anchors require research. |
| CorpseProfile | `Corpse`, death hooks on `BaseCreature` | `Projects/UOContent/Items/Misc/Corpses/Corpse.cs`, `OnDeath`, `DeleteCorpseOnDeath`, `CorpseName` on `BaseCreature` | Present | Corpse creation hooked in `Corpse.Initialize()`. Death loot via `OnDeath(Container c)`. |

---

## Progression

**Parity summary:** Core skills and spell schools through ML are present. Current main contains Mysticism spell files, but no coherent Imbuing, Throwing, or TOL Skill Mastery implementation was found; classify those jobs as research needed rather than profile-blocked implementation.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| SkillDefinition | `SkillInfo`, `SkillName` | `Projects/UOContent/Skills/SkillsInfo.cs`, `Distribution/Data/skills.json`, `Projects/Server/Skills.cs` | Present | Loaded from JSON at startup. UOContent registers callbacks and grouping helpers (`CombatSkills`, `CraftSkills`). |
| StatDefinition | `Stat`, `StatType`, `StatLockType`, `AosAttributes` | `Projects/Server/` stat types; `Mobile.SetStr/SetDex/SetInt` | Present | No content-side stat catalog. Caps/influences via AOS in `SkillsInfo.Configure()`. |
| SpellDefinition | `Spell`, `SpellInfo`, `SpellRegistry` | `Projects/UOContent/Spells/`, `Projects/UOContent/Spells/Initializer.cs` | Partial | Each spell is a `Spell` subclass with ctor `SpellInfo`. SA/TOL spell coverage varies by profile. |
| AbilityDefinition | `WeaponAbility`, `SpecialMove` | `Projects/UOContent/Items/Weapons/Abilities/`, `Projects/UOContent/Spells/Base/SpecialMove.cs` | Present | Weapon specials (primary/secondary) vs. Bushido/Ninjitsu moves in `SpellRegistry.SpecialMoves`. |
| MasteryDefinition | `DefenseMastery`, ML Spellweaving unlock | `Projects/UOContent/Items/Weapons/Abilities/DefenseMastery.cs`, `Projects/UOContent/Engines/ML Quests/Definitions/Spellweaving.cs` | Gap | No SA "Skill Mastery" system (TOL Publish 90). Closest: weapon Defense Mastery + ML quest chain for Spellweaving. |
| VirtueDefinition | `VirtueName`, `VirtueLevel`, `VirtueSystem` | `Projects/UOContent/Engines/Virtues/` (`Honor.cs`, `Justice.cs`, etc.) | Present | Enum + persistence; behavior split across per-virtue files and `VirtueContext`. |
| StatusEffectDefinition | `Poison`/`PoisonImpl`, `BuffIcon`, `BuffInfo` | `Projects/UOContent/Misc/Poison.cs`, `Projects/UOContent/Engines/BuffIcons/` | Present | Debuffs/buffs: poison levels + client buff icons. Spells/abilities call `BuffInfo.AddBuff`. |
| TitleDefinition | `Titles`, `ChampionTitleSystem` | `Projects/UOContent/Misc/Titles.cs`, `Projects/UOContent/Engines/CannedEvil/ChampionTitleSystem.cs` | Present | Fame/karma/skill titles in static tables; champion titles are separate persisted context. |

---

## EconomyCrafting

**Parity summary:** Core crafting professions and harvest systems are present. ML recipe distribution, BODs, and rare recipes flagged `Partial` in era docs.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| ResourceDefinition | `CraftResource`, `CraftResourceInfo`, `HarvestResource` | `Projects/UOContent/Misc/ResourceInfo.cs`, `Projects/UOContent/Engines/Harvest/Core/HarvestResource.cs` | Present | Craft mats (metal/leather/wood/scales) vs. harvest output types with skill gates. |
| HarvestRule | `HarvestDefinition`, `HarvestSystem`, `HarvestVein` | `Projects/UOContent/Engines/Harvest/Core/`, `Mining.cs`, `Lumberjacking.cs`, `Fishing.cs` | Present | Rules = tile ranges, veins, respawn, skill, messages, resource tables. |
| CraftRecipe | `CraftItem`, `CraftSystem` subclasses | `Projects/UOContent/Engines/Craft/Core/CraftItem.cs`, `DefBlacksmithy`, `DefTailoring`, etc. (`Engines/Craft/Def*.cs`) | Partial | Recipes registered in each `CraftSystem.InitCraftList()`. Rare recipe distribution — `Partial`. |
| ToolDefinition | `BaseTool`, `BaseHarvestTool` | `Projects/UOContent/Items/Skill Items/Tools/BaseTool.cs`, concrete tools (`Tongs`, `SewingKit`, `Pickaxe`) | Present | Tools bind to a `CraftSystem` via `CraftSystem` property. |
| BulkOrderTemplate | `SmallBulkEntry`, `LargeBulkEntry` | `Projects/UOContent/Engines/Bulk Orders/`, `Distribution/Data/Bulk Orders/**/*.cfg` | Partial | Templates loaded from cfg by profession/name (`GetEntries("Blacksmith", "armor")`). |
| VendorInventory | `VendorInventory` | `Projects/UOContent/Mobiles/Vendors/VendorInventory.cs`, `BaseHouse.VendorInventories` | Present | Offline player-vendor stash on house deletion — not NPC shop stock. NPC stock is `SBInfo` under MobileSystem. |
| RewardStore | `RewardSystem`, `TreasuresOfTokuno` | `Projects/UOContent/Engines/Veteran Rewards/`, `Projects/UOContent/Engines/Treasures of Tokuno/` | Present | Veteran-reward tables in code; Tokuno = point-based artifact redemption store. |
| CurrencyOrToken | `Gold`, `BankCheck`, `PromotionalToken` | `Projects/UOContent/Items/Misc/`, Tokuno points in `TreasuresOfTokuno` | Present | Account gold on trade/deposit. Quest/promo tokens are item subclasses. |

---

## QuestNarrative

**Parity summary:** Dual quest engines (classic + ML). ML peerless access quests and key lifecycle have documented `Gap`/`Partial` rows. No dedicated `QuestStep` type.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| QuestDefinition | `MLQuest`, `QuestSystem` subclasses | `Projects/UOContent/Engines/ML Quests/Definitions/`, `Projects/UOContent/Engines/Quests/*/*Quest.cs` | Partial | Two parallel systems: ML (Mondain's Legacy) and pre-ML story quests. EJ profile ML pack loading — `Gap`. |
| QuestStep | *(no dedicated type)* | ML: objective list on `MLQuest` + `MLQuestInstance` state; classic: ordered `QuestConversation` list | Gap | No `QuestStep` class. Progress tracked via objective/conversation ordering. |
| QuestObjective | `QuestObjective`, `BaseObjective` subclasses | `Projects/UOContent/Engines/Quests/Core/QuestObjective.cs`, `CollectObjective`, `KillObjective`, `DeliverObjective` in `Engines/ML Quests/Objectives/` | Present | Classic = abstract subclasses per quest; ML = composable objective types on quest defs. |
| QuestGiver | `IQuestGiver`, `BaseQuester` | `Projects/UOContent/Engines/ML Quests/IQuestGiver.cs`, `Projects/UOContent/Engines/Quests/Core/BaseQuester.cs` | Present | ML questers implement `IQuestGiver`; classic questers extend `BaseQuester`. |
| QuestItemRequirement | `CollectObjective`, `DeliverObjective`, `QuestItem` | `Projects/UOContent/Engines/Quests/Core/Items/QuestItem.cs`, `Engines/ML Quests/Items/` | Present | Requirements = type + count (+ destination for deliver). `QuestItem` enforces backpack rules. |
| DialogueNode | `QuestConversation` | `Projects/UOContent/Engines/Quests/Core/QuestConversation.cs`, per-quest `Conversations.cs` | Present | Classic dialogue tree nodes. ML uses `TextDefinition` fields on `MLQuest` + `QuestConversationGump`. |
| RewardTable | `RewardSystem`, `BaseReward`/`ItemReward` | `Projects/UOContent/Engines/Veteran Rewards/`, `Projects/UOContent/Engines/ML Quests/Rewards/` | Present | Veteran rewards = global categories; quest rewards = per-quest `List<BaseReward>`. |
| AccessUnlock | Quest context, items, regions, and teleporters | `Projects/UOContent/Engines/ML Quests/`, `Projects/UOContent/Engines/Quests/Regions/`, spawn/teleporter data | Unverified | Current main has no `PeerlessKeyDefinition` or `Engines/Peerless` anchor. Reconstruct each access chain from current quests/items/regions/data and official evidence before assigning status. |

---

## Encounter

**Parity summary:** Champion spawns and treasure maps have concrete controllers. Current main has ML boss creatures and dungeon spawn data but no coherent Peerless encounter controller/altar tree; Peerless lifecycle, access, and rewards remain research needed.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| SpawnTable | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Partial | DTO-backed weighted entries on world spawner items. Import/export, identity, cleanup, and era-package reachability belong to `uo-spawners-world-population`. |
| LootTable | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `Projects/UOContent/Misc/Loot.cs` | Present | Static preset tables (`AosSuperBoss`, `Gems`, etc.). Creatures call `AddLoot(...)` in `GenerateLoot()`. |
| TreasureMapTemplate | `TreasureMap` | `Projects/UOContent/Items/Maps/TreasureMap.cs` | Present | Level-driven: spawn types, chest location generation, guardian spawn. No external JSON template. |
| TreasureChestTemplate | `TreasureChestLevel1`–`4`, `TreasureMapChest` | `Projects/UOContent/Items/TreasureChests/`, `Projects/UOContent/Items/Containers/TreasureMapChest.cs` | Present | Level chests hardcode trap/lock/loot in ctors. Map chests built when a map is dug up. |
| ChampionSpawnDefinition | `ChampionSpawnInfo`, `ChampionSpawnType` | `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs`, `ChampionSpawn.cs` | Partial | Static `ChampionSpawnInfo.Table[]`: champion type, per-level spawn types, cliloc names. Pre-ML coverage `Partial`. |
| BossEncounter | No generic current-main Peerless controller found | ML boss creature classes plus dungeon spawn/quest/item data | Unverified | Creature classes and spawn data do not establish an encounter state machine. Locate current access, controller, reward, cleanup, and test anchors before claiming implementation. |
| EventDefinition | `BaseScheduledEvent`, `EventScheduler` | `Projects/UOContent/Engines/Events/`, domain events (e.g. `TreasuresOfTokuno`) | Partial | Wall-clock scheduling with `IRecurrencePattern`. TOL/HS event coverage varies. |

---

## ClientPresentation

**Parity summary:** Server-side presentation uses client IDs (art, sound, cliloc, gumps). Client asset files are not in repo — parity is ID correctness, not asset fidelity. Third Dawn 3D client not emulated.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| ArtAsset | `Item.ItemID`, `Body`, `TileData` | `Projects/Server/Items/Item.cs`, `Projects/Server/Mobiles/Body.cs`, `Projects/Server/TileData.cs`, `Distribution/Data/bodyTable.cfg` | Present | Item/mobile graphics are numeric IDs. No `ArtAsset` wrapper type. Client art files not in repo. |
| AnimationAsset | `Mobile.Animate`, `Animations` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/UOContent/Misc/Animations.cs` | Present | Action IDs passed as `int` (e.g. bow=32). Creature anims tied to `Body`. |
| SoundAsset | `Mobile.PlaySound`, `Effects.PlaySound`, `BaseSoundID` | `Projects/Server/Mobiles/Mobile.cs`, `Projects/Server/Effects.cs` | Present | Sounds are raw client sound IDs. No `SoundAsset` class. |
| Hue | `Item.Hue`, `Mobile.Hue`, `HuePicker` | `Projects/Server/Items/Item.cs`, `Projects/Server/Mobiles/Mobile.cs`, `Projects/Server/HuePicker.cs` | Present | 16-bit dye index on entities. `[Hue]` attribute for staff tools. |
| Gump | `BaseGump`, `Gump`, `DynamicGump`, `GumpLayoutBuilder` | `Projects/UOContent/Gumps/Base/`, `Projects/UOContent/Gumps/Base/GumpSystem.cs` | Present | UI built in code. Gump graphics are client gumpart IDs. See `dev-docs/gump-system.md`. |
| ClilocString | `TextDefinition`, `Localization` | `Projects/Server/Text/TextDefinition.cs`, `Projects/Server/Localization/` | Present | Cliloc = `TextDefinition.Of(number)` or `AddHtmlLocalized(cliloc, …)`. Loaded from client `cliloc.*`. |
| Icon | `BuffIcon`, `BuffInfo` | `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs`, `Projects/UOContent/Engines/BuffIcons/BuffInfo.cs` | Partial | Status-bar icons (SA+). Buff bar completeness vs. OSI — audit per profile. |

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
| Progression | SA Skill Masteries (TOL) | Gap | No Skill Mastery system; only `DefenseMastery` + ML Spellweaving quest | [UO.com Skill Mastery](https://uo.com/2015/08/26/publish-90-part-1-time-of-legends/), UOGuide |
| Progression | Mysticism, Imbuing, Throwing (SA) | Research needed | Mysticism spell files exist; no coherent Imbuing/Throwing implementation found in current main | Current repository scan plus official source required |
| QuestNarrative | `QuestStep` type | Gap | No dedicated class; objectives/conversations only | — |
| QuestNarrative | EJ profile ML quest/spawn packs | Gap | Not explicitly loaded in EJ profile | `mondains-legacy.md`, `endless-journey.md` |
| QuestNarrative | Peerless key expiration / master-key lifecycle | Research needed | No current-main Peerless key/controller anchor found | Current repository scan plus official source required |
| QuestNarrative | Prism of Light ticket access | Research needed | Reconstruct quest, item, teleporter, region, and spawn reachability before status | Current repository scan plus official source required |
| World | ML dungeon access placement | Partial | Grove, Palace, Prism access tests | `MondainsLegacySourceReferences` |
| MobileSystem | ML peerless boss live specials | Research needed | Boss creature classes do not prove live encounter hooks or official behavior | Current repository scan plus official source required |
| MobileSystem | MasterJonath, MasterMikael, CorruptedSoul | Partial | Named ML creatures | UOGuide creature pages |
| Encounter | ML champion-style (Meraktus, etc.) | Partial | End-to-end encounter flow | UOGuide [Meraktus](https://www.uoguide.com/Meraktus) |
| EconomyCrafting | Rare recipe / BOD / vendor distribution | Partial | ML crafting economy | UOGuide [Recipe](https://www.uoguide.com/Recipe) |
| Entity | EJ vs ML baseline feature parity | Partial | Profile-dependent content activation | `endless-journey.md` |
| Encounter | TOL / HS event coverage | Partial | Audit `Core.TOL` / `Core.HS` gates | `time-of-legends.md`, `high-seas.md` |
| World | Third Dawn 3D client | Gap | Network-layer 3D not emulated | `third-dawn.md` |
| ClientPresentation | Buff bar completeness (SA+) | Partial | Not all OSI buff/debuff icons | UO.com client wiki |

**Enhanced examples** (intentional, not gaps):

- Configured-project era/profile tuning versus official publish behavior
- Deterministic test seams that are verified in the current branch and clearly separated from live hooks
- `RuntimeBlocked` mechanics only when concrete implementation and the blocking registration/data/profile surface are both evidenced

See [parity-check.md](parity-check.md) for report template and workflow.
