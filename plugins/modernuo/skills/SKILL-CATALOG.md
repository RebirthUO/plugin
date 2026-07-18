# Skill Catalog

Curated index for the ModernUO plugin skill payload (72 skills). Skills stay in a flat `skills/<name>/` layout; grouping is via frontmatter (`skill_group`, `skill_subgroup`, `workflow_phase`, `workflow_tier`).

See [README.md](../../../README.md) for repository resolution, evidence policy, and workflow routing.

## Agentic Workflow (Primary)

| Phase | Skill | Repository | Stop condition |
|---|---|---|---|
| Template gate | `modernuo-issue-template-gate` | Exact repository from project `AGENTS.md` | Ask when no single live template fits |
| Create | `modernuo-issue-create` | Exact repository from project `AGENTS.md` | Stop after `IntakePacket` |
| Research | `modernuo-issue-research` | Same verified repository | Rewrite the existing body format; ask and stop on unresolved behavior |
| Implement | `modernuo-issue-implement` | Same verified repository and push remote | Require current `READY` research |
| Orchestrate | `modernuo-issue-workflow` | Same verified repository | Existing issue skips create; no completion before a verified PR |

**Companion skills:** `uo-official-evidence`, `uo-living-world-review`, `modernuo-codebase`, `modernuo-test-workflow`, `modernuo-code-audit`, and `modernuo-verification-guard`.

## Removed / Deprecated

| Skill | Action | Redirect |
|---|---|---|
| `rebirthuo-issue-create` | absorbed | `modernuo-issue-create` |
| `rebirthuo-issue-review` | absorbed | `modernuo-issue-research` |
| `rebirthuo-review-patterns` | absorbed | `modernuo-issue-research` |
| `modernuo-issue-review` | absorbed | `modernuo-issue-research` |
| `rebirthuo-implementation-checkpoints` | absorbed | `modernuo-issue-research` / `modernuo-issue-implement` |
| `rebirthuo-implement` | absorbed | `modernuo-issue-implement` |
| `rebirthuo-modernuo-codebase` | absorbed | `modernuo-codebase` |
| `uo-era-publish-source-gate` | absorbed | `uo-official-evidence` |
| `uo-era-product-timeline` | absorbed | `uo-official-evidence` / `uo-living-world-review` |
| `uo-product-model` | absorbed | `uo-living-world-review` |
| `uo-modernuo-workflow` | absorbed | README and this catalog |
| `ultima-online-product-model` | removed | `uo-living-world-review` |
| `rebirthuo-implementation` | removed | `modernuo-issue-implement` |

## migrate-* → modernuo-* Pairs

| migrate | modernuo counterpart |
|---|---|
| `migrate-serialization` | `modernuo-serialization` |
| `migrate-timers` | `modernuo-timers` |
| `migrate-gumps` | `modernuo-gump-system` |
| `migrate-packets` | `modernuo-networking` |
| `migrate-property-lists` | `modernuo-property-lists` |
| `migrate-commands-events` | `modernuo-commands-targeting`, `modernuo-events` |
| `migrate-persistence` | `modernuo-serialization`, `modernuo-events` |
| `migrate-items-mobiles` | `modernuo-content-patterns`, `modernuo-serialization` |
| `migrate-foundation` | hub for all `migrate-*` |
| `migrate-systems` | multi-file orchestration |

## UO (Game Mechanics)

**Count:** 23

| Skill | Subgroup | Workflow phase | Description |
|---|---|---|---|
| `uo-aos-item-properties` | domain | none | Use when adding, debugging, or reviewing AoS-style item-property storage, OPL rows, equipped-value aggregation, gameplay hooks, or era gates in a ModernUO-based repository. Do not  |
| `uo-bulk-orders-bod` | domain | none | Use when adding, debugging, or auditing ModernUO-based Bulk Order Deeds, BOD books and filters, Smith/Tailor offers/turn-ins, bribery, material matching, or BOD reward selection. D |
| `uo-champions-cannedevil-treasures` | domain | none | Use when adding, debugging, or auditing Champion Spawn/CannedEvil altars, candle progression, champions, Harrower skulls, Doom or Treasures event integration, and facet-specific re |
| `uo-combat-pipeline` | domain | none | Use when tracing or changing ModernUO-based melee/ranged hit checks, parry, weapon abilities, special moves, slayers, damage modifiers, elemental splits, resist application, or com |
| `uo-crafting-recipes-resources` | domain | none | Use when adding, debugging, or auditing ModernUO-based CraftSystem/CraftItem registrations, recipe scrolls, subresources, expansion gates, tools, exceptional outcomes, or ICraftabl |
| `uo-factions-towns-sigils` | domain | none | Use when adding, debugging, or auditing ModernUO Factions membership and ranks, faction towns and strongholds, sigil capture/corruption, elections and offices, silver/taxes, factio |
| `uo-game-docs-canonical-authoring` | domain | none | Use when a configured project asks to create or audit official-era UO documentation in its game-docs canonical tree with one file per mechanic, Knot-schema sections, linked indexes |
| `uo-harvest-gathering-resources` | domain | none | Use when adding, debugging, or auditing ModernUO-based Mining, Lumberjacking, Fishing, HarvestDefinition banks/veins, bonus or mutate resources, respawn, race bonuses, and facet/er |
| `uo-housing-houses-multis` | domain | none | Use when adding, debugging, or auditing ModernUO-based house placement, BaseHouse/multi ownership, HouseRegion permissions, lockdowns/secures, customization, addons, transfer/demol |
| `uo-item-property-review` | domain | none | Use when reviewing or planning a named official Ultima Online item property for a ModernUO-based repository, including official evidence, era/container placement, tooltip or cliloc |
| `uo-items-foundation` | domain | none | Use when creating, debugging, or reviewing ModernUO Item construction, ownership/movement, equipment, OPL, decay, LootType, death/corpse allocation, stealing, blessing, insurance,  |
| `uo-living-world-review` | gate | none | Use when a proposed ModernUO or UO change has a concrete cross-system effect on progression, PvP/PvM, economy, housing/storage, travel, social systems, client experience, or player |
| `uo-loot-generation-artifacts` | domain | none | Use when adding, debugging, or auditing ModernUO-based creature loot packs, drop probabilities, artifact sources, Paragon bonuses, treasure maps/chests, or boss/event reward distri |
| `uo-magic-spells` | domain | none | Use when adding, debugging, or auditing a ModernUO-based spell, spell-school registration, cast/fizzle/resource sequence, targeting, delayed/field/summon behavior, AI casting, or t |
| `uo-official-evidence` | gate | research | Use when a ModernUO or Ultima Online task must establish official OSI/EA/Broadsword behavior, chronology, era, publish, formula, restriction, or source authority before comparison  |
| `uo-pets-taming-stables` | domain | none | Use when adding, debugging, or auditing ModernUO animal-taming eligibility, controlled-pet ownership and slots, animal training, pet orders, transfer/release, stabling, persistence |
| `uo-quests-engine-ml` | domain | none | Use when adding, debugging, or auditing ModernUO-based MLQuest definitions, quest-giver offers, objectives, chains, per-player context/flags, config registration, quest gumps, pers |
| `uo-sa-item-property-implementation` | domain | none | Use when an implementation-ready task adds or fixes an official Stygian Abyss item property in a ModernUO-based repository across storage, OPL, gameplay hooks, transient contexts,  |
| `uo-samurai-empire-skills` | domain | none | Use when explaining, documenting, auditing, or implementing Samurai Empire Bushido or Ninjitsu mechanics, abilities, passives, equipment hooks, template impact, or SE-era reachabil |
| `uo-skills-stats-races` | domain | none | Use when adding, debugging, or auditing ModernUO-based skill registration/use/gain, skill/stat caps and locks, stat gain, scroll modifiers, race definitions/bonuses, character crea |
| `uo-spawners-world-population` | domain | none | Use when adding, migrating, importing, exporting, debugging, or auditing ModernUO BaseSpawner implementations or Distribution/Data/Spawns JSON packs, including entries, bounds, tim |
| `uo-vendors-commerce` | domain | none | Use when adding, debugging, or auditing ModernUO NPC or player-vendor stock, buy/sell transactions, BaseVendor, GenericBuy/GenericSell, SBInfo, prices, quantities, payment, VendorI |
| `uo-world-facets-regions` | domain | none | Use when adding, debugging, or auditing ModernUO-based maps/facets, Region definitions/lifecycle hooks, overlap priority, travel restrictions, guarded/dungeon/champion/house zones, |

## ModernUO (Engine & Dev)

**Count:** 49

| Skill | Subgroup | Workflow phase | Description |
|---|---|---|---|
| `migrate-commands-events` | migration | none | Use when converting RunUO command registration, EventSink subscriptions, event delegates, or handler signatures to ModernUO. Covers startup registration, renamed connection events, |
| `migrate-foundation` | migration | none | Use when starting any RunUO-to-ModernUO migration or applying cross-cutting namespace, naming, logging, time, pooling, threading, and performance conventions. Load before specializ |
| `migrate-gumps` | migration | none | Use when converting RunUO Gump subclasses, layout calls, SendGump patterns, or OnResponse handlers to ModernUO DynamicGump or StaticGump. Covers type selection, builders, placehold |
| `migrate-items-mobiles` | migration | none | Use when converting RunUO Item, Mobile, or BaseCreature subclasses to ModernUO and coordinating their serialization, construction, timers, properties, ownership, and deletion lifec |
| `migrate-packets` | migration | none | Use when converting RunUO Packet subclasses, PacketWriter/PacketReader code, or packet-handler registration to ModernUO span-based networking. Covers outgoing buffers, incoming rea |
| `migrate-persistence` | migration | none | Use when replacing RunUO WorldSave/WorldLoad handlers or custom binary files with ModernUO GenericPersistence for global, non-entity system state. Covers schema/version preservatio |
| `migrate-property-lists` | migration | none | Use when converting RunUO GetProperties(ObjectPropertyList) overrides or tooltip arguments to ModernUO IPropertyList. Covers interpolation arguments, cliloc formatting, and the pro |
| `migrate-serialization` | migration | none | Use when migrating RunUO Serialize/Deserialize methods, Serial constructors, Constructable attributes, or saved fields to ModernUO generated serialization. Covers new types, genera |
| `migrate-systems` | migration | none | Use when converting a multi-file RunUO engine or system with interdependent entities, persistence, commands, gumps, packets, configuration, or lifecycle hooks. Covers dependency ma |
| `migrate-timers` | migration | none | Use when converting RunUO Timer subclasses, DelayCall patterns, TimerPriority, or post-load timer restoration to ModernUO timer callbacks and TimerExecutionToken lifecycle. Do not  |
| `modernuo-code-audit` | domain | none | Use when reviewing new or modified C# under Projects/ for ModernUO correctness, serialization, lifecycle, event-loop safety, performance, strings, UI, and era conventions. Report e |
| `modernuo-codebase` | domain | none | Use when locating project ownership, repository instructions, source, configuration, data, build, or test anchors in a confirmed ModernUO-based checkout. Resolve the repository fro |
| `modernuo-commands-targeting` | domain | none | Use when creating or changing ModernUO in-game commands, access levels, CommandEventArgs parsing, Target subclasses, or command-to-target flows. Covers registration, validation, st |
| `modernuo-configuration` | domain | none | Use when adding or changing ModernUO server settings, modernuo.json keys, custom JsonConfig files, configuration defaults, or startup reads. Covers key ownership, persistence, vali |
| `modernuo-content-patterns` | domain | none | Use when implementing new ModernUO items, mobiles, creatures, spells, skill handlers, loot, context menus, or other UOContent types. Routes shared patterns; specialist spawner, ven |
| `modernuo-content-taxonomy` | domain | none | Use when classifying a UO feature into World, Entity, ItemSystem, MobileSystem, Progression, EconomyCrafting, QuestNarrative, Encounter, or ClientPresentation, or when a user expli |
| `modernuo-custom-module` | domain | none | Use when creating, registering, reviewing, renaming, or testing a separate ModernUO-based content assembly beside Projects/UOContent. Covers project/test wiring, solution/applicati |
| `modernuo-era-change-gate` | gate | none | Use when a ModernUO-based request, diff, issue, plan, or parity finding moves behavior, evidence, data, registration, or profile activation across Ultima Online eras. Identifies th |
| `modernuo-era-expansion` | domain | none | Use when implementing or reviewing era-conditional ModernUO behavior, Core.AOS/SE/ML/etc. checks, Expansion values, or an unspecified target era that changes mechanics. Establishes |
| `modernuo-event-scheduler` | domain | none | Use when implementing or reviewing wall-clock/calendar scheduling such as daily resets, weekly activities, seasonal windows, or maintenance. Covers recurrence selection, time zones |
| `modernuo-events` | domain | none | Use when subscribing to, handling, or defining ModernUO EventSink or generated events, including connection, speech, movement, combat, world, death, or deletion hooks. Covers event |
| `modernuo-gump-system` | domain | none | Use when creating or changing ModernUO StaticGump, DynamicGump, builders, placeholders, SendGump/CloseGump flows, or response handling. Covers layout choice, non-empty construction |
| `modernuo-issue-create` | agentic | create | Use when the user explicitly asks to draft or create a ModernUO or UO GitHub issue from the target repository's live issue template. Resolve the exact repository only from applicab |
| `modernuo-issue-implement` | agentic | implement | Use when implementing a ModernUO or UO GitHub issue with a current READY modernuo-issue-research handoff and clean, format-preserving body. Resolve the repository only from applica |
| `modernuo-issue-research` | agentic | research | Use when researching, reviewing, or making an existing ModernUO or UO issue implementation-ready. Resolve the repository only from applicable project AGENTS.md, establish official  |
| `modernuo-issue-template-gate` | agentic | gate | Use when a ModernUO or UO issue workflow must select and validate the exact live GitHub Issue_Template before drafting or creating an issue. Resolve the exact repository only from  |
| `modernuo-issue-workflow` | agentic | workflow | Use when taking a ModernUO or UO GitHub request from template-gated intake or an identified issue through research, format-preserving issue cleanup, blocker interviews, isolated im |
| `modernuo-lifecycle-cleanup` | domain | none | Use when implementing or reviewing ModernUO object-lifetime cleanup for timers, event subscriptions, dynamic regions, owned entities, callbacks, and restored runtime state. Do not  |
| `modernuo-lootpack-preservation` | domain | none | Use when editing or migrating ModernUO-based creature loot that contains GenerateLoot, AddLoot(LootPack.*), PackGold, PackItem, or loot-policy helpers. Preserve source-derived pack |
| `modernuo-monster-abilities` | domain | none | Use when adding, migrating, or reviewing reusable ModernUO-based creature combat specials implemented as MonsterAbility classes. Do not route boss phase orchestration or WeaponAbil |
| `modernuo-networking` | domain | none | Use when creating or modifying ModernUO packet encoders, incoming handlers, NetState sends, SpanWriter/SpanReader protocol code, or client message fan-out. Do not use for ordinary  |
| `modernuo-no-publish-prefix-names` | domain | none | Use when naming ModernUO-based symbols for mechanics sourced from an Ultima Online publish. Keep publish numbers in evidence comments, tests, docs, issues, or PR text, not in runti |
| `modernuo-pathfinding` | domain | none | Use when changing or diagnosing ModernUO AI movement, PathFollower, MovementPath, bounded A*, StepCache, .swb caches, prebake, PathCache commands, or pathfinding tests and tuning.  |
| `modernuo-performance-hot-paths` | domain | none | Use when reviewing or changing ModernUO game-loop hot paths such as AI, combat, spatial scans, packet fan-out, region hooks, timers, pathfinding, pooling, LINQ, or dynamic text. Do |
| `modernuo-property-lists` | domain | none | Use when implementing or reviewing ModernUO GetProperties, AddNameProperties, IPropertyList/ObjectPropertyList tooltip entries, cliloc arguments, property ordering, or invalidation |
| `modernuo-regions` | domain | none | Use when creating or changing ModernUO static or dynamic regions, dungeon or town sub-zones, travel/housing/spawn rules, region JSON, parent inheritance, or region lifecycle. Do no |
| `modernuo-regression-testing` | domain | implement | Use when designing or repairing focused ModernUO-based regression tests for gameplay formulas, entities, combat hooks, timers, summons, or fixture state. Use modernuo-test-workflow |
| `modernuo-serialization` | domain | none | Use when adding or changing ModernUO generated serialization, persistent fields/properties, version migrations, legacy readers, GenericPersistence, or save/load restoration. Treat  |
| `modernuo-server-lifecycle` | domain | none | Use when changing or reviewing ModernUO startup/shutdown phases, ConfigurePrompts/Configure/Initialize ordering, CallPriority, world load/save events, networking startup, or the ev |
| `modernuo-skill-discovery` | meta | none | Use when auditing or curating ModernUO skill-library coverage against current repository patterns, installed skills, developer docs, and source domains. Prefer evidence-backed patc |
| `modernuo-spatial-range-geometry` | domain | none | Use when proving exact ModernUO tile coverage for GetMobilesInRange, GetItemsInRange, GetClientsInRange, Get*InBounds, AoE radii, rings, or Rectangle2D conversions. Do not use for  |
| `modernuo-string-handling` | domain | none | Use when constructing ModernUO runtime strings with interpolation handlers, ValueStringBuilder, message/gump/packet APIs, or replacing StringBuilder in repeated game code. Use mode |
| `modernuo-symbol-discipline` | domain | none | Use when deciding whether ModernUO-based C# values should be inline, locals, constants, static readonly objects, fields, properties, or explicit Policy* surfaces. Report overexposu |
| `modernuo-test-naming` | domain | none | Use when auditing or normalizing ModernUO-based xUnit file, class, or method names polluted by publish, era-context, branch, issue, task, AI, regression, coverage, or smoke prefixe |
| `modernuo-test-workflow` | domain | implement | Use when executing or validating tests in a ModernUO-based repository, especially entity fixtures, process-global state, client data, isolated worktrees, focused versus broad evide |
| `modernuo-threading` | domain | none | Use when reviewing ModernUO async/await, Task/thread usage, game-loop ownership, concurrent collections, pooling, network/server infrastructure, or parallel world-save serializatio |
| `modernuo-timers` | domain | none | Use when implementing ModernUO delayed, recurring, cancellable, decay, expiry, or awaitable time-based behavior with Timer.StartTimer, Timer.DelayCall, TimerExecutionToken, or Time |
| `modernuo-verification-guard` | gate | implement | Use when an explicit post-edit guard requires a fresh, auditable ModernUO verification bundle beyond ordinary test output. Re-run scoped evidence from the exact worktree and prove  |
| `modernuo-world-saves-archives` | domain | none | Use when changing ModernUO world-save backups, archive rollups/destinations, ArchiveJournal recovery, restore prompts, verification, retention, pruning, or post-snapshot events. Do |
