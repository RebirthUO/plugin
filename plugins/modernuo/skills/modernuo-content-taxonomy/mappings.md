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
| SpawnerDefinition | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Partial | Weighted entries: type name, probability, max count. EJ profile may not load all ML spawn packs — see era open gaps. |
| ControllerDefinition | Engine controller subclasses | `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs`, `Projects/UOContent/Engines/Peerless/`, `Projects/UOContent/Engines/Doom/GauntletSpawner.cs` | Partial | No generic controller type. Peerless lifecycle present; key expiration lifecycle is `Gap`. |

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

**Parity summary:** AI, loot, taming, and vendor patterns are mature. ML peerless boss specials often `SourceLocked` + `RuntimeBlocked` — stats may match UOGuide while live combat hooks are unwired.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| MobileCategory | `BodyType`, `Body` struct | `Projects/Server/Mobiles/Body.cs`, `Distribution/Data/bodyTable.cfg` | Present | `IsAnimal`, `IsMonster`, `IsHuman`, `IsSea` from body table. Creature folders are organizational only. |
| AIProfile | `AIType`, `BaseAI` subclasses | `Projects/UOContent/Mobiles/AI/BaseAI/AIType.cs`, `MeleeAI`, `MageAI`, `AnimalAI`, `VendorAI` under `Mobiles/AI/` | Present | Set in `BaseCreature` ctor (`AIType`, `FightMode`). `BaseAI` is the runtime behavior profile. |
| CreatureAbility | `MonsterAbility`, `MonsterAbilityGroup` | `Projects/UOContent/Mobiles/Abilities/MonsterAbility.cs`, concrete abilities (`FireBreath`, `PoisonGasAreaAttack`, etc.) | Partial | Registered via `GetMonsterAbilities()` on `BaseCreature`. ML bosses: many abilities `RuntimeBlocked`. |
| TamingProfile | Taming fields on `BaseCreature` | `Tamable`, `MinTameSkill`, `ControlSlots`, `FoodType`, `PackInstinct` on `BaseCreature`; `Projects/UOContent/Skills/AnimalTaming.cs` | Present | Per-creature overrides in subclass ctors. Animal trainers: `AnimalTrainer.cs`. |
| VendorProfile | `BaseVendor`, `SBInfo`, `GenericBuyInfo` | `Projects/UOContent/Mobiles/Vendors/BaseVendor.cs`, `Projects/UOContent/Mobiles/Vendors/SBInfo/SBInfo.cs`, `VendorAI` | Present | Stock = `SBInfos` list; buy/sell behavior + `AIType.AI_Vendor`. |
| TrainerProfile | `CanTeach`, `CheckTeach`, `Teach` on `BaseCreature` | Overrides on townfolk (`Noble.cs`, `WanderingHealer.cs`, `BaseVendor.cs`) | Present | No `TrainerProfile` type. Skill training is virtual methods + per-NPC overrides. |
| LootProfile | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `GenerateLoot()` / `AddLoot()` on `BaseCreature` | Partial | Template packs + per-creature overrides. ML peerless artifact tables — `Partial` distribution gaps. |
| CorpseProfile | `Corpse`, death hooks on `BaseCreature` | `Projects/UOContent/Items/Misc/Corpses/Corpse.cs`, `OnDeath`, `DeleteCorpseOnDeath`, `CorpseName` on `BaseCreature` | Present | Corpse creation hooked in `Corpse.Initialize()`. Death loot via `OnDeath(Container c)`. |

---

## Progression

**Parity summary:** Core skills and spell schools through ML are present. SA Skill Masteries (TOL) and full Mysticism/Imbuing depend on era profile — `ml-baseline.json` blocks several SA skills.

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
| AccessUnlock | `PeerlessKeyDefinition`, `QuestNoEntryRegion` | `Projects/UOContent/Engines/Peerless/`, `Projects/UOContent/Engines/Quests/Regions/` | Partial | Area access via key sets on altars or quest-gated regions. Prism ticket access — `Gap`. |

---

## Encounter

**Parity summary:** Champion spawns, treasure maps, and peerless encounters are implemented. ML peerless boss combat specials and champion-style encounters (Meraktus) remain `Partial`.

| Concept | ModernUO equivalent | Key paths | Parity | Notes |
|---|---|---|---|---|
| SpawnTable | `BaseSpawner`, `Spawner`, `SpawnerEntry` | `Projects/UOContent/Engines/Spawners/`, `Distribution/Data/Spawns/**/*.json` | Partial | Weighted entries on world spawner items. Import via `[ImportSpawners]`. Era-profile spawn pack gaps. |
| LootTable | `LootPack`, `LootPackEntry`, `LootPackItem` | `Projects/UOContent/Misc/LootPack.cs`, `Projects/UOContent/Misc/Loot.cs` | Present | Static preset tables (`AosSuperBoss`, `Gems`, etc.). Creatures call `AddLoot(...)` in `GenerateLoot()`. |
| TreasureMapTemplate | `TreasureMap` | `Projects/UOContent/Items/Maps/TreasureMap.cs` | Present | Level-driven: spawn types, chest location generation, guardian spawn. No external JSON template. |
| TreasureChestTemplate | `TreasureChestLevel1`–`4`, `TreasureMapChest` | `Projects/UOContent/Items/TreasureChests/`, `Projects/UOContent/Items/Containers/TreasureMapChest.cs` | Present | Level chests hardcode trap/lock/loot in ctors. Map chests built when a map is dug up. |
| ChampionSpawnDefinition | `ChampionSpawnInfo`, `ChampionSpawnType` | `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs`, `ChampionSpawn.cs` | Partial | Static `ChampionSpawnInfo.Table[]`: champion type, per-level spawn types, cliloc names. Pre-ML coverage `Partial`. |
| BossEncounter | `PeerlessEncounter`, `PeerlessAltar` | `Projects/UOContent/Engines/Peerless/`, boss classes (e.g. `LadyMelisande`, `DreadHorn`) | Partial | Lifecycle: `PeerlessEncounterState` (Idle→Active→Looting→Cooldown). Boss specials often `RuntimeBlocked`. |
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
| Progression | Mysticism, Imbuing, Throwing (SA) | Gap | Blocked in `ml-baseline.json`; needs SA era profile | `dev-docs/eras/stygian-abyss.md` |
| QuestNarrative | `QuestStep` type | Gap | No dedicated class; objectives/conversations only | — |
| QuestNarrative | EJ profile ML quest/spawn packs | Gap | Not explicitly loaded in EJ profile | `mondains-legacy.md`, `endless-journey.md` |
| QuestNarrative | Peerless key expiration / master-key lifecycle | Gap | Access unlock incomplete | UOGuide [Peerless](https://www.uoguide.com/Peerless) |
| QuestNarrative | Prism of Light ticket access (Lefty) | Gap | Quest exists; runtime access `Partial` | UOGuide [Lefty the Ticket Seller](https://www.uoguide.com/Lefty_the_Ticket_Seller) |
| World | ML dungeon access placement | Partial | Grove, Palace, Prism access tests | `MondainsLegacySourceReferences` |
| MobileSystem | ML peerless boss live specials | Partial / RuntimeBlocked | Stats often `SourceLocked`; combat hooks unwired | Era anchors e.g. `#dread-horn`, `#lady-melisande` |
| MobileSystem | MasterJonath, MasterMikael, CorruptedSoul | Partial | Named ML creatures | UOGuide creature pages |
| Encounter | ML champion-style (Meraktus, etc.) | Partial | End-to-end encounter flow | UOGuide [Meraktus](https://www.uoguide.com/Meraktus) |
| EconomyCrafting | Rare recipe / BOD / vendor distribution | Partial | ML crafting economy | UOGuide [Recipe](https://www.uoguide.com/Recipe) |
| Entity | EJ vs ML baseline feature parity | Partial | Profile-dependent content activation | `endless-journey.md` |
| Encounter | TOL / HS event coverage | Partial | Audit `Core.TOL` / `Core.HS` gates | `time-of-legends.md`, `high-seas.md` |
| World | Third Dawn 3D client | Gap | Network-layer 3D not emulated | `third-dawn.md` |
| ClientPresentation | Buff bar completeness (SA+) | Partial | Not all OSI buff/debuff icons | UO.com client wiki |

**Enhanced examples** (intentional, not gaps):

- Deterministic test seams on ML peerless bosses (`TriggerAreaLethalPoison`, etc.) — wired for tests, not live combat until doc status changes
- RebirthUO `EraProfiles/` tuning vs. raw OSI publish defaults
- `RuntimeBlocked` mechanics documented in era docs before live hook wiring

See [parity-check.md](parity-check.md) for report template and workflow.
