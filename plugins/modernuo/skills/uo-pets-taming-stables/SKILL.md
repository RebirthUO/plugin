---
name: uo-pets-taming-stables
description: Use when adding, debugging, or auditing ModernUO animal-taming eligibility, controlled-pet ownership and slots, animal training, pet orders, transfer/release, stabling, persistence, or cleanup. Do not use for shared skill gain/caps outside pets, ordinary creature design, summoned followers, pathfinding, or vendor stock.
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
      - pets
      - animal-taming
      - stables
    related_skills:
      - uo-skills-stats-races
      - modernuo-content-patterns
      - modernuo-pathfinding
      - modernuo-lifecycle-cleanup
      - modernuo-serialization
      - uo-vendors-commerce
version: 1.0.0
author: RebirthUO
---
# UO Pets, Taming, and Stables

## Boundary

Own the controlled-pet aggregate: taming, owner/follower slots, animal-training state and application, orders, transfer/release, stable/claim/auto-stable, persistence, login/logout reconciliation, and cleanup. Route shared skill gain to `uo-skills-stats-races`, creature definition to `modernuo-content-patterns`, and movement to `modernuo-pathfinding`.

## Triggers

- Animal Training profiles, points, progress, options, or Animal Lore gumps.

## Core Workflow

1. State era/profile, creature, actor, taming/ownership/training state, slots, transition, stable context, and expected result.
2. Inspect `AnimalTaming`, `AnimalLore`, `BaseCreature`, pet-training system/profile/gumps, order handlers/state, trainer flow, `PlayerMobile`, serialization/migrations, and focused pet tests.
3. Trace the lifecycle: wild -> tame -> controlled -> lore/training -> order -> transfer/release -> stable/claim -> death/delete. Identify owner and slot mutation at every edge.
4. Validate actor, target, range/visibility, eligibility, ownership, follower capacity, commandability, and destination before mutating state.
5. Make multi-object transitions converge or roll back without orphaning or duplicating a pet.
6. Add deterministic tests for authorization, slots, transfer/release, orders, stable capacity, claim failure, auto-stabling, login, save/load, and deletion cleanup.

## Evidence boundary

Establish official taming, control, animal-training eligibility/progression/options, slots, stable limits/fees, loyalty, and era behavior through `uo-official-evidence`. Repository values prove implementation state only; emulator or community tables cannot resolve official rules.

## Output Contract

Return lifecycle/state, taming/control/training/slot matrix, order authorization, stable rollback behavior, persistence and orphan/duplication risks, changed source/tests, exact automated results, and remaining in-game checks.

## Reference Routing

- Read [taming-and-control.md](references/taming-and-control.md) for eligibility, attempts, ownership, follower slots, loyalty/control, and transfer/release.
- Read [pet-training.md](references/pet-training.md) for Animal Lore, TOL gates, profile/progress/options, slot increases, gump revision guards, and source separation.
- Read [pet-ownership-lifecycle.md](references/pet-ownership-lifecycle.md) for orders, authorization, login/logout, death/delete, persistence, and cleanup.
- Read [stabling-and-auto-stabling.md](references/stabling-and-auto-stabling.md) for trainer speech/actions, stable capacity, claim, auto-stable, rollback, and placement.

## Verification

- Cover tameable/untameable, controlled, owner/non-owner, capacity, training begin/progress/apply, success/failure, transfer, release, and supported orders.
- Run focused pet-order and pet-training tests, then add taming/stable regression tests where coverage is absent.
- Cover stable/claim success and failure, login/logout, internal-map storage, save/load, dead/deleted pets, owner deletion, and follower-slot reconciliation.
- Self-check that summoned followers were not treated as tameable pets and that pathfinding changes remain with the movement owner.
