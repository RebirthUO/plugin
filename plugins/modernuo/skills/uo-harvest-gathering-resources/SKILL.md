---
name: uo-harvest-gathering-resources
description: Use when adding, debugging, or auditing ModernUO-based Mining, Lumberjacking, Fishing, HarvestDefinition banks/veins, bonus or mutate resources, respawn, race bonuses, and facet/era gates. Do not use for recipes, finished-item loot, or generic region implementation beyond harvest hooks.
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
    - harvest
    - resources
    - economy
    related_skills:
    - uo-crafting-recipes-resources
    - uo-world-facets-regions
    - uo-skills-stats-races
version: 1.0.0
author: Crome696
---
# UO Harvest and Gathering Resources

## Boundary

Own tool/target validation, harvest banks, depletion/respawn, vein selection, bonus/mutate rolls, skill/race/facet/era modifiers, and resource delivery. Route consumption recipes to `uo-crafting-recipes-resources` and world-region infrastructure to `uo-world-facets-regions`.

## Core Workflow

1. State system, ruleset, facet, resource family, base/bonus/mutate behavior, skill range, race effect, respawn policy, and economy intent.
2. Inspect `Projects/UOContent/Engines/Harvest/`, the concrete system definition, tool entry point, target/timer flow, bank state, resource item types, region hooks, config, and focused tests.
3. Trace one attempt: tool -> target/tile/range -> bank lookup -> skill check -> vein -> bonus/mutate -> amount/facet/race adjustment -> delivery -> depletion -> respawn. Confirm which roll replaces versus supplements the base resource.
4. Keep probabilities in the units expected by the local constructor; validate ordered/overlapping ranges and fallback rows. Gate special resources at the roll site and require any book/context entitlement explicitly.
5. Preserve bank state and restart behavior. Do not bypass the system with direct item drops, global world scans, or loot-pack generation.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return the attempt flow, source and repo anchors, probability/skill/facet matrix, faucet impact, persistence risks, changed files, and exact verification results. Separate canonical behavior from shard tuning.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for detailed definitions, Mining/Lumberjacking/Fishing tables, Ter Mur resources, examples, and historical pitfalls. Treat its numeric rates as discovery aids until confirmed in the active branch/source.

## Verification

- Build and run focused harvest tests with deterministic RNG/time where available.
- Cover valid/invalid tile and range, skill boundary, base/bonus/mutate outcomes, pre-era and target-era, race and non-race controls, facet amount, depletion, and respawn.
- Prove the produced type is constructible/stackable as intended and is consumed by the matching craft system when that boundary changed.
- Self-check that chance units and replace-versus-add semantics match the actual API.
