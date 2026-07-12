# Skill Catalog

Curated index for the ModernUO plugin skill payload (75 skills). Skills stay in a flat `skills/<name>/` layout; grouping is via frontmatter (`skill_group`, `skill_subgroup`, `workflow_phase`, `workflow_tier`).

See [README.md](../../README.md) for sync contract and [uo-modernuo-workflow/SKILL.md](uo-modernuo-workflow/SKILL.md) for routing.

## Agentic Workflow (Primary)

| Phase | Skill | Repository | Notes |
|---|---|---|---|
| Create | `rebirthuo-issue-create` | `RebirthUO/rebirthuo` | Label `needs-review` |
| Review | `rebirthuo-issue-review` | `RebirthUO/rebirthuo` | Use with `rebirthuo-review-patterns` |
| Implement | `rebirthuo-implement` | `RebirthUO/ModernUO` | Canonical implementation skill |

**Companion skills:** `rebirthuo-implementation-checkpoints`, `modernuo-test-workflow`, `modernuo-code-audit`, `modernuo-verification-guard`.

**Escape hatch (direct ModernUO issues):** `modernuo-issue-create`, `modernuo-issue-review`, `modernuo-issue-implement`, `modernuo-issue-template-gate` (`workflow_tier: direct-modernuo`).

## Removed / Deprecated

| Skill | Action | Redirect |
|---|---|---|
| `ultima-online-product-model` | removed | `uo-product-model` |
| `rebirthuo-implementation` | removed | `rebirthuo-implement` |

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

**Count:** 20

| Skill | Subgroup | Workflow phase | Description |
|---|---|---|---|
| `uo-aos-item-properties` | domain | none | Use when working with the Age of Shadows (AoS) item property system in ModernUO/RebirthUO servers -  |
| `uo-bulk-orders-bod` | domain | none | Use when working with the UO Bulk Order Deed (BOD) system in ModernUO/RebirthUO servers - SmallBOD,  |
| `uo-champions-cannedevil-treasures` | domain | none | Use when working with the UO Champion Spawn system and Treasures events in ModernUO/RebirthUO server |
| `uo-combat-pipeline` | domain | none | Use when working with the UO combat pipeline in ModernUO/RebirthUO servers - the BaseWeapon swing li |
| `uo-crafting-recipes-resources` | domain | none | Use when working with the UO crafting engine in ModernUO/RebirthUO servers - CraftSystem, CraftItem, |
| `uo-era-product-timeline` | domain | none | Use when mapping Ultima Online eras, expansions, or publishes to product side effects, local Expansi |
| `uo-era-publish-source-gate` | gate | none | Require official sources for UO eras and publishes. |
| `uo-harvest-gathering-resources` | domain | none | Use when working with the UO resource gathering system in ModernUO/RebirthUO servers - the HarvestSy |
| `uo-housing-houses-multis` | domain | none | Use when working with the UO housing system in ModernUO/RebirthUO servers - BaseHouse, HouseSign, Ho |
| `uo-items-foundation` | domain | none | Use when working with the UO item entity model in ModernUO/RebirthUO servers - Item base class, Cons |
| `uo-living-world-review` | gate | none | Use when reviewing UO/RebirthUO changes for era/ruleset, facet/map, player-loop, economy, housing, P |
| `uo-loot-generation-artifacts` | domain | none | Use when working with the UO loot generation system in ModernUO/RebirthUO servers - LootPack, LootPa |
| `uo-magic-spells` | domain | none | Use when working with the UO magic system in ModernUO/RebirthUO servers - the Spell base class lifec |
| `uo-modernuo-workflow` | meta | none | Use when working on Ultima Online or ModernUO projects, shared UO/ModernUO agent instructions, or co |
| `uo-product-model` | domain | none | Use when reasoning about Ultima Online as a product/living sandbox before gameplay, economy, housing |
| `uo-quests-engine-ml` | domain | none | Use when working with the UO ML Quest engine in ModernUO/RebirthUO servers - MLQuestSystem, MLQuest  |
| `uo-sa-item-property-implementation` | domain | none | Use when implementing Stygian Abyss-era item properties in RebirthUO/ModernUO, especially SA weapon/ |
| `uo-samurai-empire-skills` | domain | none | Use when explaining, documenting, auditing, or implementing Samurai Empire skill mechanics such as B |
| `uo-skills-stats-races` | domain | none | Use when working with the UO skill/stat/race system in ModernUO/RebirthUO servers - the 58 Skills, t |
| `uo-world-facets-regions` | domain | none | Use when working with the UO world structure in ModernUO/RebirthUO servers - the 7 Facets (Felucca,  |

## ModernUO (Engine & Dev)

**Count:** 47

| Skill | Subgroup | Workflow phase | Description |
|---|---|---|---|
| `migrate-commands-events` | migration | none | > |
| `migrate-foundation` | migration | none | > |
| `migrate-gumps` | migration | none | > |
| `migrate-items-mobiles` | migration | none | > |
| `migrate-packets` | migration | none | > |
| `migrate-persistence` | migration | none | > |
| `migrate-property-lists` | migration | none | > |
| `migrate-serialization` | migration | none | > |
| `migrate-systems` | migration | none | > |
| `migrate-timers` | migration | none | > |
| `modernuo-code-audit` | domain | none | > |
| `modernuo-commands-targeting` | domain | none | > |
| `modernuo-configuration` | domain | none | > |
| `modernuo-content-patterns` | domain | none | > |
| `modernuo-content-taxonomy` | domain | none | > |
| `modernuo-custom-module` | domain | none | Use when creating, registering, reviewing, or maintaining a custom ModernUO/RebirthUO content module |
| `modernuo-era-change-gate` | gate | none | Use when a ModernUO/RebirthUO content change, parity finding, implementation plan, diff, issue, or r |
| `modernuo-era-expansion` | domain | none | > |
| `modernuo-event-scheduler` | domain | none | > |
| `modernuo-events` | domain | none | > |
| `modernuo-gump-system` | domain | none | > |
| `modernuo-issue-create` | agentic | create | Use when the user explicitly asks to draft or create a GitHub issue only in https://github.com/Rebir |
| `modernuo-issue-implement` | agentic | implement | Use when the user explicitly asks to implement a GitHub issue only in https://github.com/RebirthUO/M |
| `modernuo-issue-review` | agentic | review | Use when the user explicitly asks to research, triage, or update a GitHub issue only in https://gith |
| `modernuo-issue-template-gate` | agentic | create | Use when an explicitly requested GitHub issue draft or update must conform to the current template o |
| `modernuo-lifecycle-cleanup` | domain | none | > |
| `modernuo-lootpack-preservation` | domain | none | Use when editing or migrating ModernUO/RebirthUO creature loot, especially GenerateLoot() and AddLoo |
| `modernuo-monster-abilities` | domain | none | Use when adding, migrating, or reviewing ModernUO/RebirthUO creature special attacks as reusable Mon |
| `modernuo-networking` | domain | none | > |
| `modernuo-no-publish-prefix-names` | domain | none | Use when naming ModernUO/RebirthUO functions, variables, constants, fields, helpers, tests, or other |
| `modernuo-pathfinding` | domain | none | > |
| `modernuo-performance-hot-paths` | domain | none | > |
| `modernuo-property-lists` | domain | none | > |
| `modernuo-regions` | domain | none | > |
| `modernuo-regression-testing` | domain | implement | Use when writing or repairing ModernUO/RebirthUO regression tests for gameplay mechanics, spells, sp |
| `modernuo-serialization` | domain | none | > |
| `modernuo-server-lifecycle` | domain | none | Use when changing or reviewing ModernUO startup, bootstrap phases, reflection lifecycle hooks, first |
| `modernuo-skill-discovery` | meta | none | Use when asked to analyze the ModernUO codebase, inspect installed or attached skills, compare repos |
| `modernuo-spatial-range-geometry` | domain | none | Use when calculating exact in-game tile coverage for ModernUO/RebirthUO AoE and spatial range querie |
| `modernuo-string-handling` | domain | none | Use when working on ModernUO string construction, interpolation handlers, ValueStringBuilder, packet |
| `modernuo-symbol-discipline` | domain | none | Use when writing, reviewing, or refactoring ModernUO/RebirthUO C# code involving constants, local va |
| `modernuo-test-naming` | domain | none | Use when writing, reviewing, or cleaning up ModernUO/RebirthUO C# xUnit tests whose file, class, or  |
| `modernuo-test-workflow` | domain | implement | Use when writing, modifying, validating, or preparing PRs for ModernUO/RebirthUO xUnit tests, especi |
| `modernuo-threading` | domain | none | > |
| `modernuo-timers` | domain | none | > |
| `modernuo-verification-guard` | gate | implement | Use when Hermes reports edited ModernUO/RebirthUO files lack fresh verification evidence and asks fo |
| `modernuo-world-saves-archives` | domain | none | Use when working with ModernUO world save backups, archive rollups, archive restore flows, ArchiveJo |

## RebirthUO (Project-Specific)

**Count:** 8

| Skill | Subgroup | Workflow phase | Description |
|---|---|---|---|
| `rebirthuo-implement` | agentic | implement | Use when implementing RebirthUO GitHub issues: read each ticket, check for sufficient data, skip und |
| `rebirthuo-implementation-checkpoints` | agentic | implement | Use during RebirthUO implementation sessions when issue analysis exposes unresolved gameplay/product |
| `rebirthuo-issue-create` | agentic | create | Turn RebirthUO ideas into review-ready issues. |
| `rebirthuo-issue-review` | agentic | review | Review RebirthUO needs-review issues fachlich. |
| `rebirthuo-modernuo-codebase` | agentic | none | 'Use when navigating the RebirthUO ModernUO codebase: repository layout, Projects/Server vs Projects |
| `rebirthuo-review-patterns` | agentic | review | Reusable review patterns for RebirthUO GitHub issues: mechanics source framing, repo anchors, implem |
| `uo-game-docs-canonical-authoring` | domain | none | Use when authoring canonical-era RebirthUO game-docs under game-docs/GameDocs/01_Broadsword with one |
| `uo-item-property-review` | domain | none | Review and plan Ultima Online item-property tickets in RebirthUO/ModernUO, including source classifi |
