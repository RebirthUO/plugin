---
name: uo-skills-stats-races
description: Use when adding, debugging, or auditing ModernUO-based skill registration/use/gain, skill/stat caps and locks, stat gain, scroll modifiers, race definitions/bonuses, character creation, or era-gated skill availability. Do not use for pet/taming lifecycle or combat/spell/crafting mechanics beyond the shared skill/stat/race pipeline.
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
    - skills
    - stats
    - races
    related_skills:
    - modernuo-skill-discovery
    - uo-magic-spells
    - uo-combat-pipeline
    - uo-crafting-recipes-resources
    - uo-pets-taming-stables
version: 1.1.0
author: Crome696
---
# UO Skills, Stats, and Races

## Boundary

Own shared skill metadata/availability/use checks, gain and lock/cap behavior, stat gain/caps/mods, race definitions/bonuses/change flow, character-creation validation, and skill-cap scroll effects. Animal Taming registration/gain stays here; the taming action and controlled-pet aggregate belong to `uo-pets-taming-stables`. Other domain actions remain with their owners.

## Core Workflow

1. State ruleset/era, skill/stat/race, action, base/modified value, locks/caps, scroll/account effects, and expected observable result. Source current versus historical cap/roster claims.
2. Inspect active skill data/enum/table, configuration, `SkillCheck`, `Mobile` caps/mods, character creation, race definitions/hooks, scroll/reward code, registration order, and focused tests.
3. Trace the relevant flow: action -> success check -> gain eligibility/anti-macro -> skill lock/cap/total-cap movement -> stat-gain selection/locks/caps -> client delta; or race selection/change -> persisted race -> centralized bonus consumers.
4. Use the shared gain/check APIs; never mutate skill base or stats directly to simulate normal progression. Read `Skill.Cap` and current stat caps instead of hard-coding 100/125.
5. Gate registration, creation, UI, books/trainers, and consumers consistently by cumulative expansion. Changing `Core.Expansion` in a test may require rebuilding/restoring process-global registries.
6. Apply racial bonuses in their semantic consumer (resist cap, harvest, movement, combat, baseline skill), not as unrelated permanent stat mutation.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return a roster/cap/lock or race-bonus matrix, traced gain/use flow, source/repo anchors, persistence and balance risks, changed files, and exact verification results.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for the detailed taxonomy, skill/stat/race tables, cap/scroll notes, examples, and historical pitfalls. Treat counts and formulas as targets to confirm, not constants to copy blindly.

Use `uo-pets-taming-stables` when the request crosses from shared Animal Taming checks/gain into creature eligibility, ownership, control slots/orders, transfer, or stabling.

## Verification

- Build and run focused skill/gain/stat/race/creation/scroll tests.
- Cover success/failure, locked/up/down, individual and total caps, anti-macro/time boundary, primary/secondary stat paths, pre-era/target-era roster, save/load, and race/non-race controls.
- Restore expansion, clocks, delegates, and registries in sequential tests.
- Self-check that modified versus base skill and natural versus item/account caps are not conflated.
