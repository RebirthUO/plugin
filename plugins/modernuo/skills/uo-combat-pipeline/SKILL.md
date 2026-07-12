---
name: uo-combat-pipeline
description: Use when tracing or changing ModernUO-based melee/ranged hit checks, parry, weapon abilities, special moves, slayers, damage modifiers, elemental splits, resist application, or combat side effects. Do not use for spell casting, property storage, or creature-specific ability design unless the task crosses into the shared combat pipeline.
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
    - combat
    - pvp
    - pvm
    related_skills:
    - uo-aos-item-properties
    - uo-magic-spells
    - modernuo-spatial-range-geometry
    - modernuo-performance-hot-paths
version: 1.0.0
author: Crome696
---
# UO Combat Pipeline

## Boundary

Own shared attack resolution from eligibility and hit/parry through damage calculation, typed mitigation, final application, and post-hit state. Route spell sequencing to `uo-magic-spells`, property storage/OPL to `uo-aos-item-properties`, and bespoke boss actions to the monster-ability skill.

## Core Workflow

1. Fix the ruleset, PvP/PvM context, weapon/ability, attacker/defender types, and expected observable result. Source parity-sensitive formulas before editing.
2. Trace the real call path in the active branch: swing eligibility -> hit chance -> parry/absorb -> base and percentage modifiers -> elemental/chaos/direct split -> `AOS.Damage` -> actual `Mobile.Damage` -> post-hit effects. Record where each cap and era gate applies.
3. Preserve ordering. Distinguish candidate damage from actual applied HP loss; region and mobile hooks can cancel or mutate the latter. Do not bypass `AOS.Damage` for AoS+ typed damage or hard-code creature names for slayer logic.
4. Keep special-move/weapon-ability activation, mana consumption, clearing, and exclusions explicit. Temporary contexts need transition-time cleanup, not only lazy cleanup on the next accessor.
5. Test through the narrowest real seam: capture production hit chance, drive parry/ability hooks, or assert applied HP/resource deltas. Use deterministic RNG/timers and restore global test state.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Report the traced call path, formula/cap table, source and repo anchors, behavior change and intentional non-changes, PvP/PvM/era side effects, and exact build/test evidence. For diagnosis-only work, identify the first divergent stage and smallest reproducible case.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for broad swing, resist, slayer, parry, facet, and example detail.
- Research named mechanics from current official evidence and current
  repository consumers; use `uo-samurai-empire-skills` for SE skill scope.

## Verification

- Build and run the focused combat tests plus adjacent ability/damage tests.
- Include hit and miss/parry controls, pre-era and target-era controls, player and creature targets, caps, side effects, and cleanup/revalidation transitions.
- Confirm spatial queries use map range APIs and hot-path changes do not add global scans or avoidable allocations.
- Self-check that the test observes the production seam rather than reimplementing the formula under test.
