---
name: uo-bulk-orders-bod
description: Use when adding, debugging, or auditing ModernUO-based Bulk Order Deeds, BOD books and filters, Smith/Tailor turn-ins, bribery, material matching, or BOD reward selection. Do not use for ordinary craft recipes, quest rewards, or generic monster loot.
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
    - bod
    - crafting
    - economy
    related_skills:
    - uo-crafting-recipes-resources
    - uo-items-foundation
    - uo-loot-generation-artifacts
version: 1.0.0
author: Crome696
---
# UO Bulk Order Deeds

## Boundary

Own the BOD lifecycle from vendor offer through deed fill/combine, BOB storage/filtering, turn-in, cooldown, and BOD-specific reward calculation. Route recipe metadata to `uo-crafting-recipes-resources`, quest rewards to `uo-quests-engine-ml`, and non-BOD drops to `uo-loot-generation-artifacts`.

## Core Workflow

1. State ruleset and publish boundary. Verify whether the target is the Smith/Tailor baseline or a later/custom craft expansion; do not infer post-Publish-95 crafts from enum placeholders.
2. Inspect `Projects/UOContent/Engines/Bulk Orders/`, the relevant vendor/context-menu path, BOB gumps/filters, `BulkMaterialType` mapping, reward tables, config/spawn reachability, and existing BOD tests.
3. Trace one real transaction: eligibility and cached offer -> deed construction -> item/material/quality validation -> small/large combine -> deed/item consumption -> cooldown -> reward delivery. Identify the authoritative owner of every mutation.
4. For new types, keep deed entry metadata, craft-system output type, graphic, material mapping, exceptional rule, and reward profile aligned. For bribery, require an empty deed, correct publish gate, gold debit, upgrade step, and scrutiny/greed state.
5. Preserve save compatibility and BOB capacity/filter behavior. Avoid direct reward selection when the local BOD reward calculator owns probability and cost.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Report the target craft/era, offer and turn-in paths, validation/reward matrix, economy and save risks, changed files, and commands actually run. For audits, distinguish source parity, repository behavior, and custom policy.

## Reference Routing

Read [domain-map.md](references/domain-map.md) when you need the hierarchy, BOB/material tables, bribery background, examples, or historical test names. Re-verify all numeric cooldowns, reward odds, and publish claims against current sources and code before changing behavior.

## Verification

- Build and run the focused BOD reward/runtime tests.
- Cover correct and wrong type, material, exceptional flag, amount, and large-deed membership; prove consumed inputs and delivered reward.
- Cover pre-era and target-era cooldown/bribery behavior, BOB round-trip/filter/capacity, and save/load where state changed.
- Self-check that a BOD change did not silently expand supported crafts or bypass the configured reward calculator.
