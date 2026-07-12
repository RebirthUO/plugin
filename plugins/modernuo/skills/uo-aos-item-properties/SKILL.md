---
name: uo-aos-item-properties
description: Use when adding, debugging, or reviewing AoS-style item-property storage, OPL rows, equipped-value aggregation, gameplay hooks, or era gates in a ModernUO-based repository. Do not use for base item lifecycle, crafting registration, or loot-table policy except where a property explicitly crosses those boundaries.
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
    - aos
    - item-properties
    - parity
    related_skills:
    - uo-official-evidence
    - uo-item-property-review
    - uo-items-foundation
    - uo-combat-pipeline
    - uo-loot-generation-artifacts
version: 1.0.0
author: Crome696
---
# UO AoS Item Properties

## Boundary

Own the complete property slice: storage, staff API, tooltip, equipped aggregation, gameplay consumer, persistence, era behavior, and tests. Treat generation/distribution as a separate economy decision. Route base entity work to `uo-items-foundation`, combat formulas to `uo-combat-pipeline`, and random loot to `uo-loot-generation-artifacts`.

## Core Workflow

1. Name the target ruleset, introduction era/publish, item families, official behavior, and explicit non-goals. Establish every behavior-changing claim through `uo-official-evidence` before coding.
2. Inspect the active branch: `Projects/UOContent/Misc/AOS.cs`, every owning `Base*` item, the actual consumer pipeline, serializers/migrations, and focused tests. Do not trust historical line numbers or class existence as proof of reachability.
3. Classify the property as persistent rollable state, item-specific state, or runtime-only display/effect state. Keep AoS as the property-system umbrella; prefer mechanic/family names for overflow containers and gate each property at its own consumer.
4. Implement each surface deliberately: safe unique bit, GM wrapper, constructor/default and dupe paths, save migration, OPL/cliloc and ordering, hard-coded equipped-family aggregation where needed, then the owning gameplay hook. Never mutate `BaseAttributes` internals directly.
5. Keep timed contexts transient unless save persistence is required. Cancel tokens and remove mobile/item references on expiry, removal, death, deletion, logout, and map invalidation.
6. Add distribution only when the request names loot, runic, reforging, imbuing, artifact, or event rollout. Otherwise prove those surfaces did not change.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Produce a source decision, repository anchors, changed-surface matrix (`storage | OPL | aggregation | effect | persistence | distribution`), compatibility/economy risks, and exact verification results. Mark unresolved mechanics as `Needs source confirmation`; do not fill gaps from emulator precedent alone.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for architecture, examples, project gotchas, and the named-property reference index.
- Read [aos-property-container-taxonomy.md](references/aos-property-container-taxonomy.md) before choosing storage and [extended-weapon-attribute-refactor.md](references/extended-weapon-attribute-refactor.md) for bit exhaustion/migration.
- Load the mechanics-dummy note only for that specific test deliverable.
  Research named properties at use
  time instead of loading stored ticket decisions.

## Verification

- Build the owning solution and run the narrow property tests plus adjacent pipeline tests.
- Cover storage/default/dupe/serialization or prove runtime-only state; positive OPL and pre-era suppression; formula/caps; cleanup; supported and unsupported hosts.
- Search distribution surfaces to prove intentional inclusion or exclusion.
- Self-check that storage, tooltip, gameplay, and distribution are not being treated as one implicit operation.
