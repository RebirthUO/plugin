---
name: uo-factions-towns-sigils
description: Use when adding, debugging, or auditing ModernUO Factions membership and ranks, faction towns and strongholds, sigil capture/corruption, elections and offices, silver/taxes, faction guards/vendors/items, notoriety integration, or faction persistence. Do not use for generic regions, guilds, ordinary PvP combat, generic vendors, or champion spawns.
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - ultima-online
      - modernuo
      - factions
      - towns
      - sigils
    related_skills:
      - uo-world-facets-regions
      - uo-combat-pipeline
      - uo-vendors-commerce
      - modernuo-gump-system
      - modernuo-serialization
      - uo-living-world-review
version: 1.0.0
author: RebirthUO
---
# UO Factions, Towns, and Sigils

## Boundary

Own the Factions engine aggregate: faction/player/town state, membership/rank, elections/offices, strongholds, sigils/monoliths, silver/tax economy, faction guards/vendors/items, persistence, and integration hooks. Route generic region behavior, guilds, combat formulas, vendor mechanics, and UI infrastructure to their owning skills.

## Core Workflow

1. State era/ruleset, faction/town, actor and role, object or currency, requested transition, current state, and expected player-visible result.
2. Inspect `Engines/Factions/Core`, definitions/instances, persistent state, sigil/monolith items, stronghold region, election and gump flows, faction mobiles/vendors/items, and integration call sites in stealing, notoriety, death, combat, and login.
3. Model the affected transitions before editing: join/leave/kick, rank/kill points, election/candidate/office, town ownership/tax/finance, sigil home/carry/corrupt/purify/return, or guard/vendor lifecycle.
4. Authorize every transition from canonical state, revalidate delayed/gump actions, and keep faction, player, town, item, region, and economy mutations consistent across failure and restart.
5. Treat silver, taxes, vendor stock, guard hiring, faction items, rewards, and death effects as one economy-impacting boundary; run `uo-living-world-review` for value or eligibility changes.
6. Add focused state-transition and persistence tests. When current source lacks a test harness, report missing automated evidence and use bounded admin/in-game verification without claiming parity.

## Evidence boundary

Establish official Factions rules, timers, ranks, rewards, costs, limits, and era availability through `uo-official-evidence`. Repository code proves current implementation only; inherited RunUO behavior and community documentation cannot establish official parity.

## Output Contract

Return a faction/player/town/sigil state model, actor/permission matrix, transition and persistence trace, economy/region/combat integrations, rollback and exploit risks, changed source/tests, available automated evidence, and explicit manual or missing verification.

## Reference Routing

- Read [faction-state-model.md](references/faction-state-model.md) for core registries, membership/ranks, durable state, lifecycle, and integration boundaries.
- Read [towns-sigils-elections.md](references/towns-sigils-elections.md) for ownership, elections/offices, sigil/monolith transitions, permissions, and timers.
- Read [faction-economy-and-integration.md](references/faction-economy-and-integration.md) for silver/taxes, guards/vendors/items, notoriety/combat/stealing links, and verification risk.

## Verification

- Cover join/leave/kick and capacity, rank changes, election phases/candidate eligibility/voting, office permissions, town ownership, and restart persistence.
- Cover every sigil state and invalid transition, including death/logout, disconnect, monolith removal, purification/corruption timing, duplicate possession, and return home.
- Cover silver/tax debit and credit, guard/vendor hire/delete, faction-item ownership/expiration, and positive/negative notoriety/combat integrations.
- Self-check that limited focused tests are reported honestly and that generic PvP, region, vendor, or gump behavior was not duplicated.
