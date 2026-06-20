---
name: "uo-quests-engine-ml"
description: "Use when working with the UO ML Quest engine in ModernUO/RebirthUO servers - MLQuestSystem, MLQuest definitions, QuestGivers, MLQuestContext (per-player quest state), MLQuest objectives (kill/deliver/escort/obtain/collect), reward gumps, QuestConversation/ReportBack/Info/DetailedLog gumps, Bedlam/Blighted Grove/Heartwood/Sanctuary/Citadel access chains, ML context flags (Spellweaving/SummonFey/SummonFiend/BedlamAccess), and the quest config CFG file. Use when adding a new quest, debugging why a quest does not offer, wiring a quest reward, or auditing ML content parity."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Quests Engine (ML)

## Overview

The UO Quest engine is the post-ML system for content-driven quests: kill X of monster Y, deliver item Z to quester Q, escort NPC E, obtain an artifact, etc. Each quest is a typed `MLQuest` subclass with an `MLQuestObjective` collection and a reward set. The engine tracks per-player state via `MLQuestContext` and exposes offers/conversations/report-back via typed gumps.

The engine lives in `Projects/UOContent/Engines/ML Quests/`. The central class is `MLQuestSystem` (`MLQuestSystem.cs:16-1103`). The quest definitions are loaded from `Distribution/Data/MLQuests.cfg`. Quest gumps are in `Projects/UOContent/Engines/ML Quests/Gumps/`. The quest objective types are in `Projects/UOContent/Engines/ML Quests/Objectives/`. Per the `mondains-legacy-content-matrix.md`, this is one of the most regression-tested areas of the codebase (`MLQuestConfigResolutionTests`, `DeliverObjectiveRuntimeTests`, `GainSkillObjectiveRuntimeTests`, `MLQuestPersistenceTests`, `MLQuestPacketTests`).

This skill covers the quest engine architecture, the per-player context, the objective types, the reward gumps, the ML context flags, the quest giver system, the per-era quest sets (Heartwood, Sanctuary, Bedlam, Blighted Grove, Citadel, New Haven, etc.), the quest config file format, and the persistence model.

## When to Use

- Adding a new ML-era quest.
- Debugging why a quest does not offer to a player.
- Wiring a quest reward item.
- Adding a new quest giver NPC.
- Auditing the per-area quest roster (Heartwood, Sanctuary, Blighted Grove, Bedlam, etc.).
- Wiring a quest context flag (e.g. for Peerless altar access).
- Reading the `MLQuests.cfg` file format.
- Auditing ML content parity via `MLQuestConfigResolutionTests`.

Don't use for:

- Base item/mobile entity model (use `uo-items-foundation`).
- Combat/spell/skills (use the relevant `uo-combat-pipeline` / `uo-magic-spells` / `uo-skills-stats-races`).
- BOD reward system (use `uo-bulk-orders-bod`).
- Loot generation (use `uo-loot-generation-artifacts`).

## The MLQuestSystem Static Class

`MLQuestSystem` (`Projects/UOContent/Engines/ML Quests/MLQuestSystem.cs:16-1103`) is the central registry. Key static fields:

| Member | Purpose |
|---|---|
| `Enabled` | Master switch (typically `Core.ML`). |
| `AutoGenerateNew` | Whether to auto-generate quests for questers that have no quest list. |
| `MaxConcurrentQuests` | 10. A player can have up to 10 active quests. |
| `Quests` | `Dictionary<Type, MLQuest>` keyed by quest type. |
| `QuestGivers` | `Dictionary<Type, List<MLQuest>>` keyed by quester `Mobile` type. |
| `Contexts` | `Dictionary<PlayerMobile, MLQuestContext>` per-player state. |
| `ActiveConfigPaths` | The loaded `MLQuests.cfg` paths. |

The static constructor calls `LoadQuestConfiguration()` which reads `Data/MLQuests.cfg` and instantiates the `MLQuest` classes. The `MLQuests.cfg` format is a line-based config file: each line is a quest type or a quester line.

The admin commands live in `MLQuestsInfo`, `MLQuestsValidate`, `SaveQuest`, `ViewQuests`, `ViewMLContext`. They are the canonical debug surface.

## The MLQuest Base Class

`Projects/UOContent/Engines/ML Quests/MLQuest.cs` defines the `MLQuest` abstract base. Concrete subclasses live in `Projects/UOContent/Engines/ML Quests/Definitions/` (one file per quest area: `Heartwood.cs`, `Sanctuary.cs`, `BlightedGrove.cs`, `Bedlam.cs`, `NewHaven.cs`, `Spellweaving.cs`, `Paladin.cs`, etc.).

The key fields and methods:

| Member | Purpose |
|---|---|
| `Title` | The quest title shown in the offer gump. |
| `Description` | The quest description. |
| `RefuseMessage` | Shown when the player declines. |
| `OfferMessage` | Shown when the quest is offered. |
| `Objectives` | `List<MLQuestObjective>`. The quest's tasks. |
| `Rewards` | `MLQuestReward[]`. The reward set. |
| `QuestGiverType` | The `Type` of the `Mobile` that offers the quest. |
| `DestinationType` | The `Type` of the `Mobile` to deliver to (for delivery quests). |
| `Activation` | `MLQuestActivation` enum (e.g. `NewHaven`). |
| `MLQuestContextFlags` | The flags this quest grants. |
| `MaxConcurrent` | Per-player concurrency cap (1-10). |
| `OneTime` | Whether the quest can be completed only once per player. |
| `ChainID` | The chain this quest belongs to. |
| `GetDetails` / `ReportBack` | Methods that return localized descriptions for the gumps. |

The quest instance is constructed once at config load and reused for all offers. Per-player state (active, completed, refused) is tracked in the player's `MLQuestContext`.

## The MLQuestContext (Per-Player State)

`MLQuestContext` is the per-player state container. It tracks:

- `OwnedQuests`: `List<MLQuestInstance>` of the quests the player has accepted.
- `ChainOffers`: which quest chains the player has been offered.
- `ContextFlags`: the ML context flags the player has earned (e.g. `Spellweaving`, `SummonFey`, `SummonFiend`, `BedlamAccess`, `PeerlessKeyAccess<DreadHorn>`, etc.).
- `OneTimeQuestsCompleted`: the set of one-time quests the player has completed.

The context is serialized as part of the `PlayerMobile` save. The `MLQuestContext` is loaded on login and saved on logout.

The context flags drive the per-quest access checks. For example, `Bedlam` quests check `PlayerContext.BedlamAccess` before offering the Bedlam chain. The `Monstrous Interred Grizzle` altar requires `PlayerContext.BedlamAccess == true` (`docs/mondains-legacy-content-matrix.md:59`).

## The MLQuestObjective Types

`Projects/UOContent/Engines/ML Quests/Objectives/` holds the objective types:

| Objective | Use |
|---|---|
| `KillObjective` | Kill X of creature type Y in region Z. |
| `DeliverObjective` | Deliver item I to quester Q (the item can be generated or pre-stacked). |
| `ObtainObjective` | Have item I in inventory at claim time. |
| `CollectObjective` | Collect X of item I (sometimes held on the cursor). |
| `EscortObjective` | Escort NPC E to destination D. |
| `GainSkillObjective` | Reach skill S at value V (often accelerated via New Haven accelerated-skill window). |
| `BaseObjective` (abstract) | Custom objective for special cases. |

Each objective has:

- `Description`: the localized task description.
- `Progress`: the in-progress state (e.g. `5/10 rats killed`).
- `OnAccept` / `OnCompleted` / `OnResign` hooks.
- `OnTick` (for time-based objectives).

The objective rolls completion via the `IsCompleted()` method, called by the quest system on a per-tick basis (via `Timer`) and on relevant game events (kill, item pickup, etc.).

## The Quest Gumps

`Projects/UOContent/Engines/ML Quests/Gumps/` contains the gumps:

| Gump | Purpose |
|---|---|
| `QuestOfferGump` | The offer screen (Accept / Decline buttons). |
| `QuestConversationGump` | The quester's pre-offer conversation. |
| `QuestRewardGump` | The reward screen (selectable if multiple rewards). |
| `QuestCancelGump` | The confirmation gump for canceling an active quest. |
| `QuestReportBackGump` | The delivery / completion confirmation. |
| `QuestLogGump` | The player's current quest list. |
| `QuestDetailedLogGump` | The per-quest detail view. |
| `QuestInfoNPCGump` | The non-quester info dialog. |
| `BaseQuestGump` | The shared base class for the gumps. |
| `RaceChangeGump` | The Elf/Gargoyle race change UI. |

The `MLQuestPacketTests` covers the race-change packets and the multi-reward quest offer/claim pages (verifying the `All of the following` reward label rather than objective-choice text).

## The Quest Configuration File

`Distribution/Data/MLQuests.cfg` is the central config file. The format is line-based:

```
# Comment lines start with #
# Format: <QuestTypeName> [quester=QuesterTypeName]
# Each line is one quest entry

Heartwood.OrcSlaying
Heartwood.AllThatGlittersIsNotGood
Sanctuary.SanctuaryOrcKill
Sanctuary.DallidChain
Bedlam.NotQuiteThatEasy quester=BedlamQuester
BlightedGrove.BoundToTheLand quester=LadyMelisande
Spellweaving.HeartwoodSpellweavingUnlock quester=LorekeeperRollarn
NewHaven.MoreOrePlease
NewHaven.DeliciousFishes
...
```

The config is loaded by `MLQuestSystem.LoadQuestConfigurationFile` (`MLQuestSystem.cs:60-...`). The parser:

1. Reads each non-comment, non-blank line.
2. Resolves the quest type via `Type.GetType` against the loaded assemblies.
3. Resolves the quester type (defaulting to the quest's `QuestGiverType` if not specified).
4. Adds the quest to `Quests[type]` and `QuestGivers[questerType]`.

The `MLQuestConfigResolutionTests` covers:

- All ML quest config rows are registered.
- Invalid fixture diagnostics fire.
- Report-back warning for collection quests without required items.
- Collection quest counting/claiming for cursor-held items.
- Permanent context flag serialization.
- Active non-escort quest context restoration with questgiver type preservation.
- Reattachment when the saved questgiver entity reference is missing.

## Quest Chains

A quest chain is a sequence of quests that the player progresses through. The chain is identified by a `ChainID` and tracked in `MLQuestContext.ChainOffers`. The next quest in a chain is offered when the previous one is completed.

The `MLQuestSystem.OnQuestCompleted` hook fires the chain-update logic. The next quest in the chain is registered in the `QuestGivers` for the appropriate quester.

The Heartwood chain examples:

- `OrcSlaying`: kill 8 Orcs + 4 OrcScouts in Heartwood.
- `AllThatGlittersIsNotGood`: collect items from Heartwood.
- `ExAssassins`: kill Ex-Assassins (male-only filter).
- `ExtinguishingTheFlame`: collect items (male-only filter).
- `DeathToTheNinja`: kill Ninjas (male-only filter).
- `CrimeAndPunishment`: collect items (male-only filter).

The Sanctuary chains:

- `SanctuaryOrcKill`: kill Orcs in Sanctuary.
- `DallidChain`: `Moug-Guur` → `Chiikkaha` → `Szavetra`.
- `OgreLordChain`: `Ogre` → `Ogre Lord` → `Cyclops` → `Titan`.
- `BrotherlyLove`: deliver to Ahie.

The Bedlam chain:

- `NotQuiteThatEasy`: grants `BedlamAccess` permanently.

The Blighted Grove chain:

- `VilePoison` → `SubContracting` → `BoundToTheLand` (rewards `DryadsBlessing`).

The Citadel chain:

- `TigerClawThief` → `SerpentsFangHighExecutioner` → `Travesty` (the boss; not strictly chained but the starter items feed in).

## ML Context Flags

The ML context flags are persistent per-player booleans. They live on `PlayerContext` (an attached object on `PlayerMobile`). The set:

- `Spellweaving`: granted by the Heartwood/Sanctuary Arcanist quests.
- `SummonFey`: granted by the FriendOfTheFey follow-up.
- `SummonFiend`: granted by the CrackingTheWhip follow-up.
- `BedlamAccess`: granted by `NotQuiteThatEasy`.
- `PeerlessKeyAccess<TBoss>`: granted by the boss's specific quest or key-drop chain.
- `CitadelAccess`: granted by the sect quest chains.

The flags are used by the magic system (e.g. `ArcanistSpell.CheckCast` requires `PlayerContext.Spellweaving`), by the boss altar system (e.g. `MonstrousInterredGrizzleAltar` requires `BedlamAccess`), and by the spell-summon check (e.g. `Summon Fey` requires `SummonFey` flag).

`MLQuestConfigResolutionTests` covers the permanent context flags surviving serialization.

## The ML Quest System for New Haven

`Projects/UOContent/Engines/ML Quests/Definitions/NewHaven.cs` defines the New Haven training quests (the post-ML starting-area quests). The key patterns:

- Skill training quests: `GainSkillObjective` accelerates the player's skill to 50.0 in the relevant skill.
- Reward tools: `AmeliasToolbox` (Tinkering), `JacobsPickaxe` (Mining), `HammerOfHephaestus` (Blacksmithy).
- One-time flags prevent repeated acceptance.

`GainSkillObjectiveRuntimeTests` covers owned New Haven skill-acceleration windows, active acceleration preservation, cancellation safety when another acceleration window replaces the quest-owned one, and objective acceleration-state serialization.

## Per-Area Quest Definitions

Each area has its own file in `Projects/UOContent/Engines/ML Quests/Definitions/`:

| File | Quests | Region |
|---|---|---|
| `Heartwood.cs` | Orc Slaying, Glitters, Ex-Assassins, ... | Heartwood (Elf village) |
| `Sanctuary.cs` | Orc Kill, Dallid Chain, Ogre Chain, Brotherly Love | Sanctuary |
| `Bedlam.cs` | Not Quite That Easy (grants Bedlam access) | Bedlam dungeon |
| `BlightedGrove.cs` | Vile Poison, Sub-Contracting, Bound to the Land (grants Dryad's Blessing) | Blighted Grove |
| `Citadel.cs` | Tiger Claw Thief, Serpents Fang High Executioner (courier quests for Travesty) | The Citadel |
| `TwistedWeald.cs` | Dread Horn key quests (Dread Horn starter items) | Twisted Weald |
| `PrismOfLight.cs` | Crystal key quests (Shimmering Effusion starter items) | Prism of Light |
| `Paladin.cs` | Various Chivalry-related quests | Various |
| `Necromancer.cs` | Various Necromancy-related quests | Various |
| `NewHaven.cs` | Training quests, tool rewards | New Haven |
| `Spellweaving.cs` | Heartwood/Sanctuary Arcanist quests | Heartwood/Sanctuary |
| `PaintedCaves.cs` | Painted Caves dungeon quests | Painted Caves |
| `Labyrinth.cs` | Labyrinth dungeon quests | Labyrinth |
| `Bedlam.cs` | Bedlam dungeon quests | Bedlam |
| `PalaceOfParoxysmus.cs` | Palace of Paroxysmus dungeon quests | Palace of Paroxysmus |
| `Tokuno.cs` | Tokuno-related quests | Tokuno |
| `Heartwood.cs` | Heartwood elf village quests | Heartwood |

The `MLQuestConfigResolutionTests` covers the Bedlam access chain, the Blighted Grove delivery chain, the Sanctuary quester quest-list exposure, the Heartwood elf race quests, and the New Haven skill training quests.

## Common Pitfalls

1. **Implementing ML quest-item purchases as ad-hoc vendors.** If an ML source says the player must mark an item as a quest item or identifies a named quest/reward, model it through the ML quest engine first, not as a direct `OnDoubleClick` purchase or generic `BaseVendor` buy list. Example: UO.com Prism of Light says Lefty sells access for 10,000 gp and the gold is marked as a quest item; UOGuide identifies Lefty's quest as `Wonders of the Natural World`, objective `Obtain 10,000 gold coin`, reward `Prism of Light Admission Ticket`. The correct first implementation shape is a `Lefty` quest giver + quest definition + `MLQuests.cfg` row + quest/reward tests, with direct seller code only if the quest engine cannot express the source flow.
2. **Forgetting `[Constructible]` on the quest class.** A quest type without `[Constructible]` cannot be instantiated by the `MLQuestSystem` config loader; the quest silently fails to load.
2. **Registering the quester type in the config without the quest type, or vice versa.** The config line `quester=...` is for the quester; the prefix `Heartwood.OrcSlaying` is for the quest type. Mismatched registration is a silent failure.
3. **Setting `MaxConcurrent` > 10.** The hard cap is 10; values above are clamped and produce a warning.
4. **Forgetting the `ChainID` for chained quests.** Without a chain ID, the next quest in the sequence is never offered.
5. **Setting `OneTime = false` on a quest that should be one-time (e.g. `NotQuiteThatEasy`).** A player can re-earn the context flag repeatedly, which is harmless but produces extra reward items.
6. **Referencing a quester type that does not exist on the map.** The quester `Type` must be the actual `Mobile` class. Mismatch produces a runtime error on quest offer.
7. **Using the wrong region for the `KillObjective`.** The region check is the `Region` class; using the wrong region name makes the objective unfulfillable.
8. **Setting `MLQuestContextFlags` to a value that the magic system does not recognize.** The flag is checked in `PlayerContext` setters; an unknown flag is silently ignored.
9. **Forgetting to set `Enabled = true` on the `MLQuestSystem`.** The `Enabled` flag is the master switch; without it, no quests offer even if they are loaded.
10. **Hardcoding the quest reward item type instead of using a constructor.** A hardcoded `typeof(SomeSword)` in the `MLQuestReward` constructor makes the quest a single-reward quest. The standard pattern is `new MLQuestReward(typeof(SomeSword))` to allow the engine to instantiate the type per offer.

## Common Recipes

### Adding a New ML Quest

```csharp
namespace Server.Engines.MLQuests.Definitions;

public class MyNewQuest : MLQuest
{
    public MyNewQuest()
    {
        Activated = true;
        Title = 1075555; // A localized title cliloc
        Description = 1075556;
        RefuseMessage = 1075557;
        OfferMessage = 1075558;
        Objectives.Add(new KillObjective(1, 0, "heartwood", typeof(Orc)));
        Rewards.Add(new MLQuestReward(typeof(Gold), 1000));
    }
}
```

Register in `MLQuests.cfg`:
```
Heartwood.MyNewQuest
```

### Adding a Quest Reward with Multiple Items

```csharp
Rewards.Add(new MLQuestReward(typeof(AncientSmithyHammer)));
Rewards.Add(new MLQuestReward(typeof(PowderOfTemperament), 3));
```

### Adding a Context Flag Reward

```csharp
public class MyNewQuest : MLQuest
{
    public MyNewQuest()
    {
        ...
        MLQuestContextFlags = MLQuestContextFlags.MyNewContext;
    }
}
```

`MLQuestContextFlags` is a `[Flags]` enum. New flags can be added with a unique bit.

### Adding a Quester

The quester is a `Mobile` subclass:

```csharp
public class MyQuester : BaseCreature
{
    [Constructible]
    public MyQuester() : base(AIType.AI_Vendor, FightMode.None)
    {
        ...
        // Add to ML questers via QuestGiver registration in MLQuestSystem
    }
}
```

Register in `MLQuests.cfg`:
```
Heartwood.MyNewQuest quester=MyQuester
```

### Wiring an Access Check

```csharp
// In the altar's OnDoubleClick
if (MLQuestSystem.GetContext(player)?.BedlamAccess != true)
{
    player.SendLocalizedMessage(1072764); // You must complete a quest to access this area.
    return;
}
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New quest: `[Constructible]` is present, `Activated = true`, the quester `Type` is registered, the config line is in `MLQuests.cfg`.
- [ ] `MLQuestConfigResolutionTests` passes (the canonical regression test for quest registration).
- [ ] `MLQuestsValidate` command runs without errors.
- [ ] Quest offer works in-game: the quester offers the quest, the player accepts, the objectives roll completion, the rewards drop.
- [ ] Quest context flag grants persist across save/load (the `BedlamAccess` and `Spellweaving` flags are tested in `MLQuestConfigResolutionTests`).
- [ ] Quest chain: completing quest N offers quest N+1.
- [ ] Quest concurrency: the player can have up to 10 active quests, no more.
- [ ] Quest cancel: canceling an active quest refunds delivered items (per `DeliverObjectiveRuntimeTests`).
- [ ] Quest gumps: `QuestOfferGump`, `QuestConversationGump`, `QuestRewardGump`, `QuestLogGump`, `QuestDetailedLogGump` render with the right localizations.
- [ ] Quest packet: `MLQuestPacketTests` covers the race-change and reward-claim packet structure.
- [ ] Per-area questers: Heartwood, Sanctuary, Bedlam, Blighted Grove, Citadel, Twisted Weald, Prism of Light questers are present in the spawn data.
- [ ] For Bedlam access: `MonstrousInterredGrizzleAltar` requires `BedlamAccess`.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-items-foundation` - the `Item` model used for quest rewards, delivery items, and starter items.
- `uo-world-facets-regions` - the `Region` system that the quest objectives use for kill/escort tracking.
- `uo-skills-stats-races` - the skill-gain accelerated windows for New Haven training quests.
- `uo-combat-pipeline` - the kill/loot pipeline that the kill objectives hook.
- `uo-magic-spells` - the spell-summon checks that require ML context flags.
- `uo-loot-generation-artifacts` - the loot tables for the boss drops (ML Peerless artifacts).
- `uo-crafting-recipes-resources` - the recipe/rare resources that quest rewards grant (e.g. `CapturedEssence` for Hovering Wisp).
- `modernuo-content-patterns` - canonical templates for new quest types.
- `modernuo-era-expansion` - per-era quest set availability (ML-gated quests).
- `uo.stratics.com/content/ml/quests.shtml` (offline reference) - the original Stratics overview of the ML quest system.
- `www.uoguide.com/Bulk_Order_Deed` (offline reference) - the canonical BOD system (separate from ML quests).
- `docs/mondains-legacy-content-matrix.md:51-65` (offline reference) - the per-area quest test coverage.
