---
name: uo-loot-generation-artifacts
description: Use when adding, debugging, or auditing ModernUO-based creature loot packs, drop probabilities, artifact sources, Paragon bonuses, treasure maps/chests, or boss/event reward distribution. Do not use for item-property implementation, BOD/quest rewards, combat damage, or encounter controllers except at their explicit reward boundary.
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
    - loot
    - artifacts
    - economy
    related_skills:
    - modernuo-lootpack-preservation
    - uo-aos-item-properties
    - uo-champions-cannedevil-treasures
    - uo-quests-engine-ml
version: 1.0.0
author: Crome696
---
# UO Loot Generation and Artifacts

## Boundary

Own generated reward selection, construction, attribution, and delivery for ordinary creatures, Paragons, treasure maps/chests, named artifacts, and explicitly scoped event/boss reward surfaces. Route encounter state to `uo-champions-cannedevil-treasures` and item property behavior to `uo-aos-item-properties`.

## Core Workflow

1. State era/profile, source creature/encounter/chest, recipient/credit rule, item pool, chance units, amount, LootType/binding, and economy intent.
2. Inspect the actual death/completion path, local `LootPack`/entry constructors, creature `GenerateLoot` pattern, specialized artifact service/table, treasure map/chest generator, era/facet gates, reachability, and focused tests.
3. Trace one reward: eligible event -> attribution -> table selection -> RNG -> fresh item construction -> property packing -> corpse/backpack/chest delivery -> ownership/binding -> cleanup. Keep ordinary loot, boss artifacts, champion rewards, quest/BOD rewards, and event currency separate.
4. Preserve local loot-pack composition/order unless the task explicitly changes it. Probabilities must use the API's actual units; constructors must return fresh instances; do not bypass specialized helpers with direct corpse/world insertion.
5. For named/event artifacts, implement item behavior and distribution as separate decisions. Verify the source is reachable, enabled, and era/facet-correct rather than inferring distribution from an item class.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return a source-to-reward matrix, probability/amount and attribution rules, delivery/binding behavior, economy impact, repo anchors, changed files, and exact verification results. Label emulator-only rates as precedent, not canonical facts.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for detailed LootPack, treasure map, Champion/Peerless/minor artifact, Paragon, and example notes.
- Read [artifact-rarity-audit.md](references/artifact-rarity-audit.md) only for rarity value/OPL coverage.
- Research named artifacts and events from current official evidence and the
  configured repository rather than stored ticket snapshots.

## Verification

- Build and run focused loot/artifact/map tests with deterministic RNG where possible.
- Cover positive and negative chance/gate/facet/recipient cases, fresh-instance construction, amount bounds, LootType/binding, and specialized delivery.
- Use a statistical test only when deterministic table inspection cannot prove the contract; keep tolerances explicit.
- Self-check that no direct corpse/world insertion bypasses attribution or a specialized reward service.
