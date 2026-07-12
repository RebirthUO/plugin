---
name: uo-quests-engine-ml
description: Use when adding, debugging, or auditing ModernUO-based MLQuest definitions, quest-giver offers, objectives, chains, per-player context/flags, config registration, quest gumps, persistence, or rewards. Do not use for BODs, generic loot, spell mechanics, or ad-hoc vendor transactions that should be modeled as quests.
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
    - quests
    - mondains-legacy
    - pvm
    related_skills:
    - uo-loot-generation-artifacts
    - uo-magic-spells
    - modernuo-gump-system
    - uo-skills-stats-races
version: 1.0.0
author: Crome696
---
# UO ML Quests Engine

## Boundary

Own quest definition/registration, offer eligibility, instance/context persistence, objective event tracking, chains, report-back/claim, context flags, gumps, and quest-specific rewards. Route underlying combat, spell, skill, region, and generic loot behavior to their domain skills.

## Core Workflow

1. State era/profile, quest area/giver, one-time/repeat/chain policy, objectives, reward/flag, prerequisites, cancellation behavior, and source evidence.
2. Inspect `Engines/ML Quests`, the concrete definition, `MLQuests.cfg` (or active config), quest-giver spawn/reachability, objective implementation, gumps, player context serialization, reward item, and focused tests.
3. Trace the state machine: discovery/offer -> eligibility/concurrency -> accept -> objective subscriptions/progress -> report back -> consume/validate objective items -> reward/flag -> chain advance/completion -> save/load/cancel/reconnect.
4. Use existing objective and reward abstractions. Do not replace a sourced quest purchase/delivery with ad-hoc vendor or double-click logic merely because it is shorter.
5. Keep shared quest definitions stateless; player-specific state belongs in the quest instance/context. Preserve quest-giver identity/re-attachment, permanent flags, one-time completion, and delivered-item ownership across saves.
6. Register definition and giver consistently and prove the giver exists in world data. Localized gumps must use established clilocs and distinguish all-rewards from choose-one rewards.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Provide a quest state diagram, objective/reward/flag matrix, config and spawn anchors, persistence/economy risks, changed files, and exact validation results. Distinguish canonical flow, repo behavior, and custom policy.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for detailed system/objective/gump/context/config notes, area/chain tables, examples, and historical test names. Re-check duplicated area rows, old line numbers, and config assumptions before use.

## Verification

- Build and run config-resolution plus focused objective/context/gump/persistence tests.
- Cover eligible/ineligible offer, accept/refuse/cancel, progress and wrong-target/item controls, report-back, reward/flag, chain advance, concurrency/one-time policy, and save/load/reconnect.
- Prove quest giver and required destination/region/item are reachable.
- Self-check that cancellation cannot duplicate/lose delivered items and that context flags survive exactly as intended.
