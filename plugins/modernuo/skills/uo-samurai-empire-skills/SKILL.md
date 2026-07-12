---
name: uo-samurai-empire-skills
description: Use when explaining, documenting, auditing, or implementing Samurai Empire Bushido or Ninjitsu mechanics, abilities, passives, equipment hooks, template impact, or SE-era reachability in official UO or a ModernUO-based repository. Do not route all Tokuno content here, and do not classify AoS, ML, or SA systems as SE skills.
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
    - SamuraiEmpire
    - Skills
    - Bushido
    - Ninjitsu
    related_skills:
    - uo-magic-spells
    - uo-skills-stats-races
    - uo-combat-pipeline
    - modernuo-era-expansion
license: MIT
---
# Samurai Empire Skills

## Boundary

Samurai Empire skill work means exactly Bushido and Ninjitsu unless the request explicitly broadens to Tokuno creatures, items, crafting, housing, or events. AoS combat/item systems are prerequisites; Spellweaving, Mysticism, Imbuing, Throwing, masteries, and later races are separate.

## Core Workflow

1. State whether the target is SE launch, a later publish/current official UO,
   the configured repository's behavior, or custom policy. Current UO.com
   wording is not automatically launch parity.
2. Capture the official UO.com Bushido or Ninjitsu page and the historical cross-check before making mechanic claims. Record exact ability/passive/equipment rows and source conflicts.
3. Inspect local `Core.SE` registration, skill data, spell/special-move classes, weapon hooks, books/trainers/items, Tokuno/New Haven reachability, context state, and focused tests.
4. Trace the owning pipeline: Bushido Honor/Perfection/parry/stances/special moves through combat; Ninjitsu stealth/movement/forms/clones/poison/equipment through spell, movement, follower, and weapon paths.
5. Preserve high-impact constraints: PvP diminishing returns/caps, stealth/range/time checks, follower slots, poison rules, active-state replacement, mana/ability clearing, and cleanup on death/delete/logout/map/equipment transitions.
6. For implementation, use the narrower combat, spell, skill, item, or test skill after the sourced mechanic contract is fixed.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return the exact SE skill, source URLs and mechanic table, local registration/reachability anchors, implementation status, PvP/PvM/template/economy/new-player effects, unknowns, and exact validation results.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for the detailed Bushido, Ninjitsu, Animal Form, equipment, special-move, and product-impact tables. Re-verify every number against the target ruleset before copying it into code/tests.

## Verification

- Explanation work names exactly Bushido and/or Ninjitsu and cites official pages.
- Implementation work covers SE and pre-SE registration/reachability plus the real owning pipeline.
- Tests restore global expansion/timer/static-effect state and initialize movement/poison/client fixtures when required.
- Self-check that a class, book, or skill row was not mistaken for a reachable live feature.
