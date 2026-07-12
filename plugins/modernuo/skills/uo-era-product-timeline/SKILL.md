---
name: uo-era-product-timeline
description: Use when mapping Ultima Online eras, expansions, or publishes to product side effects, local Expansion/Core gates, map/facet availability, and RebirthUO implementation decisions.
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
    - Era
    - Expansion
    - Product
    - RebirthUO
    related_skills:
    - uo-product-model
    - uo-living-world-review
    - modernuo-era-expansion
    - modernuo-content-taxonomy
license: MIT
---
# UO Era Product Timeline

## Overview

This skill frames Ultima Online eras as product realities, not just `Expansion` enum values. Use it to predict side effects on maps, player loops, economy, PvP, housing, skills, client flags, and RebirthUO implementation anchors. It depends on Hermes tools, official/community UO sources, and local repo files only; no extra packages are required.

## When to Use

- "Which era/ruleset should this UO feature target?"
- Before changing any code that uses `Core.AOS`, `Core.SE`, `Core.ML`, `Core.SA`, `Core.TOL`, or `Core.EJ`.
- When a player-facing feature may change combat, loot, housing, storage, travel, skills, or account policy.
- When explaining why a ModernUO/RebirthUO behavior differs between pre-AoS, AoS, SE, ML, SA, ToL, or EJ.
- When triaging an issue that cites an expansion, publish, map, skill, item property, or official UO feature.

## Prerequisites

- Local repo: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- Load `uo-product-model` first for the product-loop lens.
- Load `modernuo-era-expansion` before editing era-conditional code.
- Source hierarchy: UO.com for current product wording, UOGuide for era tables/history, Stratics for historical mechanics, then repo anchors for implementation.
- No credentials or environment variables are required.

## How to Run

Use `read_file` on `Distribution/Data/expansions.json`, `Distribution/Data/map-definitions.json`, and `Projects/Server/ExpansionInfo.cs`. Use `search_files` for `Core.<Era>` and feature-specific anchors. Use `browser_navigate` or a `terminal`-invoked HTTP fetch for UO.com/UOGuide/Stratics pages, then reconcile the source behavior with the repo implementation.

## Quick Reference

- `Projects/Server/ExpansionInfo.cs:24-38` — `Expansion` enum order.
- `Projects/Server/ExpansionInfo.cs:56-96` — `FeatureFlags` expansion aliases.
- `Projects/Server/ExpansionInfo.cs:133-156` — `HousingFlags` era aliases.
- `Projects/Server/ExpansionInfo.cs:223-232` — loads `Data/expansions.json`.
- `Distribution/Data/expansions.json` — canonical local expansion metadata.
- `Distribution/Data/map-definitions.json` — local map/facet availability.
- `https://www.uoguide.com/Expansion` — expansion dates and headline mechanics.
- `https://uo.com/what-is-uo/` — product promise and sandbox framing.
- `https://uo.com/wiki/ultima-online-wiki/skills/` — current skill index.
- Search pattern: `Core\.(T2A|UOR|UOTD|LBR|AOS|SE|ML|SA|HS|TOL|EJ)`.

## Per-Era Source Extraction

When the user asks for a per-era overview document (e.g. "erstelle eine Era Übersicht für Samurai Empire"), the canonical data path is:

1. **Engine metadata first** — `Distribution/Data/expansions.json` (Id, ClientFlags, FeatureFlags, MapSelectionFlags, HousingFlags per era).
2. **Facet metadata** — `Distribution/Data/map-definitions.json` (per-era facets: Tokuno for SE, Malas for AoS, Ter Mur for SA, Eodon for ToL, etc.).
3. **Skill content** — `uo.com/wiki/ultima-online-wiki/skills/<skill>/` pages. For SE these are exactly two skills: `bushido/` and `ninjitsu/`. Extract per-ability tables via the `browser_console` recipe in `uo-era-publish-source-gate/references/uo-source-tiers.md` ("uo.com Wiki Table Extraction via Browser Console"). This bypasses the `web_extract` summarizer and the `browser_snapshot` truncation that drop per-row data.
4. **Facet overviews** — `uo.com/wiki/.../worlds/<facet>/` URLs **404** (Broadsword has not migrated world overview pages). Reconstruct from per-skill/per-item/per-mob pages plus `map-definitions.json`; flag Tokuno-style overviews as `Needs source confirmation`.

## Procedure

1. **Name the ruleset before the feature.** State the assumed era, shard, and whether the target is canonical UO, ModernUO default, RebirthUO policy, or custom. You are done when the answer names one era or explicitly says `era unknown`.

2. **Classify the era pivot.** Use this product timeline:

   | Era | Product meaning | Side-effect questions |
   |---|---|---|
   | Original / Pre-T2A | Harsh sandbox baseline, Felucca-only world, simpler combat/item model. | Does this preserve danger, scarcity, and old-school PvP? |
   | T2A | Lost Lands and early expansion content. | Does the feature assume later maps, skills, or client flags? |
   | UOR | Trammel/Felucca split and consent boundary. | Does it change PvP, stealing, resources, fields, or safe progression? |
   | UOTD / LBR | Ilshenar and 3D/2D client-era content. | Does travel, no-housing, paragon/artifact, or map access apply? |
   | AoS | The big systems divide: item properties, insurance, resist model, Malas, Necromancy/Chivalry. | Does it inflate item power, remove loss, or change PvP burst/counterplay? |
   | SE | Tokuno, Bushido, Ninjitsu, Samurai/Ninja fantasy, faster casting context. | Does it create template extinction or new mobility/defense imbalance? |
   | ML | Elves, Spellweaving, peerless bosses, quests, recipes, Heartwood. | Does access require quests, keys, group mechanics, or recipe economy? |
   | SA | Gargoyles, Ter Mur, Mysticism, Imbuing, Throwing, Abyss systems. | Does imbuing/crafting power replace loot or destabilize gear value? |
   | HS | Ships and sea gameplay. | Does it introduce new travel, fishing, cargo, or naval combat loops? |
   | ToL | Eodon, Shadowguard, masteries, late-game progression. | Does it add endgame power or mastery dependencies? |
   | EJ | Free-to-play constraint layer. | Is this expansion content or account/storage/housing policy? |

3. **Read local expansion metadata.** Use `read_file` on `Distribution/Data/expansions.json`; check `SupportedFeatures`, `MapSelectionFlags`, `CharacterListFlags`, `HousingFlags`, `RequiredClient`, and `MobileStatusVersion`. You are done when the local metadata supports the era claim.

4. **Check local map reality.** Use `read_file` on `Distribution/Data/map-definitions.json`. This RebirthUO checkout lists Felucca, Trammel, Ilshenar, Malas, Tokuno, TerMur, and Internal; do not assume Eodon exists locally without verifying a map definition or custom map work.

5. **Find code gates.** Use `search_files` for `Core.<Era>`, `Expansion.<Era>`, `RequiredExpansion`, and feature-specific classes. Treat classes without registration, map access, spawn data, or era gates as implementation clues, not proof of live product availability.

6. **Write the side-effect row.** Before recommending a change, record: era, facet/map, player loop, PvP impact, PvM impact, economy/faucet/sink impact, housing/storage impact, new-player impact, veteran impact, client/save compatibility, and whether behavior is canonical, partial, or custom.

7. **Escalate to parity research when needed.** If the task asks whether behavior is correct, load `uo-era-publish-source-gate` and use UO.com/UOGuide/Stratics before treating repo behavior as canonical. You are done when every mechanic claim has a source URL or is marked `Needs source confirmation`.

## Pitfalls

- Era enums are cumulative in ModernUO: `Core.ML` means expansion is at least ML, not exactly ML.
- AoS is not just another content drop; it changes combat, resists, item properties, insurance, loot, and player risk.
- UOR is not just Trammel; it creates a product split between consent and non-consent play.
- EJ is not just `Expansion.EJ`; official EJ includes account, bank, storage, and housing restrictions that may be only partially represented by expansion flags.
- Local map support can lag product vocabulary; verify Eodon and any custom facet before planning content.
- A feature class existing in `Projects/UOContent` does not prove live reachability; check registration, data, spawns, commands, and era gates.
- Do not use private shard wikis as canonical UO behavior. They are useful only as breadcrumbs or comparative custom-policy references.

## Verification

A valid era/product answer includes one explicit era/ruleset, one player-loop impact, one canonical source URL or `Needs source confirmation`, and one repo anchor such as `Distribution/Data/expansions.json` or `Projects/Server/ExpansionInfo.cs`.
