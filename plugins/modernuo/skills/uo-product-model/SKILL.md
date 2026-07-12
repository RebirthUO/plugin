---
name: uo-product-model
description: Use when reasoning about Ultima Online as a product/living sandbox before gameplay, economy, housing, PvP/PvM, or era-policy decisions.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
    - UltimaOnline
    - Product
    - Facets
    - Shards
    - GameDesign
    related_skills:
    - uo-living-world-review
    - uo-era-product-timeline
    - uo-era-publish-source-gate
license: MIT
---
# Ultima Online Product Model

## Overview

This skill gives a product-first mental model for Ultima Online so code work starts from the living world: shards, eras, facets, player loops, trust, and economy. It does not replace source verification, era parity research, or code-domain skills. It depends only on Hermes tools plus official/community UO pages and the local RebirthUO repository; no extra packages are required.

## When to Use

- "Understand Ultima Online as a product", "learn UO", or "what is UO?"
- "What facets does UO have?" or any question about Felucca, Trammel, Ilshenar, Malas, Tokuno, Ter Mur, or Eodon.
- Before planning gameplay, balance, economy, PvP, PvM, housing, shard-policy, or era-parity changes.
- When a code change looks small but may alter player behavior, progression, storage, risk, or economy.
- When triaging RebirthUO/ModernUO issues that cite UO features rather than code symbols.

## Prerequisites

- Local repo, when available: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- Source hierarchy: official `uo.com` for live product wording, UOGuide for mechanics tables/history, Stratics for historical era context, then repo anchors for implementation state.
- Load `uo-era-publish-source-gate` for canonical-source discipline, `rebirthuo-modernuo-codebase` for local repo navigation, and `modernuo-content-taxonomy` when mapping product concepts to code domains.
- No credentials or environment variables are required.

## How to Run

Use `browser_navigate` or `web_extract` for UO product pages, `read_file` for local data files, `search_files` for implementation anchors, and `terminal` only for repository or .NET checks. Start by naming the shard/ruleset, era, facet, player loop, and risk category before proposing a code or policy answer. Keep the final answer source-backed: canonical UO source first, repo implementation second, unknowns explicit.

## Quick Reference

- `https://uo.com/what-is-uo/`
- `https://uo.com/wiki/ultima-online-wiki/gameplay/`
- `https://uo.com/wiki/ultima-online-wiki/skills/`
- `https://uo.com/wiki/ultima-online-wiki/gameplay/houses-placing-a-house/`
- `https://uo.com/wiki/ultima-online-wiki/combat/champion-spawns/dynamic-champion-spawns/`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Facets&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Ultima%20Online&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Skills&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Shards&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Houses&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Crafting&format=json`
- `https://www.uoguide.com/api.php?action=parse&prop=text&page=Champion%20spawn&format=json`
- `Distribution/Data/map-definitions.json`
- `Distribution/Data/expansions.json`
- `Projects/Server/Skills.cs`
- `Projects/Server/ExpansionInfo.cs`
- `Projects/UOContent/Misc/Notoriety.cs`
- `Projects/UOContent/Multis/Houses/BaseHouse.cs`
- `Projects/UOContent/Engines/Craft/Core/CraftSystem.cs`

## Procedure

1. **Start from the product promise.** Treat UO as a sandbox world where players fight, craft, explore, trade, build houses, sail, roleplay, and choose hero/villain roles. Use `browser_navigate` or `web_extract` on `https://uo.com/what-is-uo/`; you are done when the answer names at least three non-combat loops.

2. **Name the shard and ruleset.** A shard is a separate server/world; UO mechanics differ between official production shards, Siege-style rules, New Legacy, freeshards, and custom RebirthUO profiles. You are done when the answer says which shard/ruleset is assumed or explicitly marks it unknown.

3. **Lock the era before mechanics.** Use `read_file` on `Distribution/Data/expansions.json` and, for history, the UOGuide expansion table. Era boundaries change maps, skills, item properties, insurance, housing flags, account policy, and PvP risk. Key pivots: UOR creates Trammel, AoS is the item-property/insurance/resist divide, SE adds Tokuno/Bushido/Ninjitsu, ML adds Elves/Spellweaving/peerless/quests, SA adds Gargoyles/Ter Mur/Mysticism/Imbuing/Throwing, ToL adds Eodon/Shadowguard/masteries, EJ adds free-account constraints.

4. **Map the world facet.** Use the UOGuide Facets page for product behavior and `Distribution/Data/map-definitions.json` for local implementation. Official product vocabulary has seven facets:
   - **Felucca** ÔÇö original world, non-consensual PvP and stealing, double resources, Power Scroll champion rewards.
   - **Trammel** ÔÇö Renaissance mirror of Felucca with non-consensual PvP and player stealing disabled.
   - **Ilshenar** ÔÇö Third Dawn land, no housing, moongate entry, travel restrictions, paragons/artifacts.
   - **Malas** ÔÇö Age of Shadows land with Luna, Umbra, Doom, housing, and AoS systems.
   - **Tokuno** ÔÇö Samurai Empire islands with Zento, Bushido/Ninjitsu context, dungeon travel restrictions.
   - **Ter Mur** ÔÇö Stygian Abyss gargoyle homeland, tied to SA systems and Abyss access.
   - **Eodon** ÔÇö Time of Legends valley; verify local support before planning because this RebirthUO map file currently lists Felucca, Trammel, Ilshenar, Malas, Tokuno, TerMur, and Internal.

5. **Inventory player-loop impact.** Classify the feature into one or more product loops before code placement:
   - **Progression:** 58 skills, 720 total skill cap, stats, races, scrolls, masteries.
   - **PvM/encounters:** monsters, dungeons, spawns, champion spawns, peerless bosses, treasure maps, quests.
   - **PvP/risk:** Felucca rules, reds/blues, murder counts, criminals, stealing, guards, factions/VvV, escape tools.
   - **Economy/crafting:** gold faucets/sinks, resources, CraftSystem, BODs, vendors, loot, insurance.
   - **Housing/social:** placement, lockdowns, secure storage, vendors, decay/IDOC, guilds, towns, events.
   - **Client presentation:** gumps, cliloc text, art IDs, maps, travel, visibility, tooltips.

6. **Tie product concepts to repo anchors.** Use `search_files` to find the smallest implementation anchor: maps in `map-definitions.json`, expansions in `ExpansionInfo.cs` and `expansions.json`, skills in `Skills.cs`, PvP reputation in `Notoriety.cs`, housing in `BaseHouse.cs`, crafting in `CraftSystem.cs`, champion spawns under `Engines/CannedEvil`, quests under `Engines/ML Quests`, and loot under `LootPack`/artifact files.

7. **State consequences before prescribing a change.** For every recommendation, write the side-effect row: affected era, facet, player loop, who benefits, who loses, faucet/sink/storage impact, PvP counterplay impact, save/client compatibility, and whether the behavior is canonical, partial, or custom.

8. **Answer "facets" in both senses when ambiguous.** If the user says facets, cover the world facets first, then the product facets: world, progression, combat, economy, housing, social/community, content/quests/events, and client presentation.

9. **Report with evidence, not vibes.** Cite product pages by URL and repo anchors by path. If UO.com/UOGuide/Stratics do not settle a value, write `Needs source confirmation`; do not turn local code or memory into canonical product truth.

## Pitfalls

- Do not treat UO as just code. A behavior change can alter trust, housing memory, PvP risk, vendor economy, or shard identity.
- Do not assume live UO rules apply to pre-AoS, UOR, T2A, or custom shard rulesets.
- Do not assume all official facets are implemented locally; verify `Distribution/Data/map-definitions.json` before planning Eodon or any custom map.
- Do not reduce Felucca to "PvP only"; guards, towns, murder counts, resources, stealing, and champion rewards all matter.
- Do not reduce Trammel to "safe mode"; it changes economy, travel, field spells, stealing, and player social patterns.
- Do not balance from a single anecdote. Check logs, reproduction, source behavior, and impacted playstyles.
- Do not make economy changes without asking whether the output is tradeable, blessed, insured, farmable, bottable, or storage-limited.
- Do not change housing lightly; placement, decay, lockdowns, vendors, IDOC behavior, and secure storage are trust systems.
- Do not call a feature "implemented" just because a class exists; check registration, era gate, data files, spawn access, and tests/live reachability.

## Verification

A product-grounded answer passes only if it explicitly includes: shard/ruleset, era/expansion, facet/map, affected player loop(s), canonical source URL(s), repo anchor(s), and side effects or unknowns.
