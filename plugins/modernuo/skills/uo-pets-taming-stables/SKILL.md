---
name: uo-pets-taming-stables
description: Use when adding, debugging, or auditing ModernUO animal-taming eligibility, controlled-pet ownership and slots, pet orders, transfer or release, stable/claim/auto-stable behavior, or pet persistence and cleanup. Do not use for shared skill gain/caps, ordinary creature design, summoned followers, generic pathfinding, or vendor stock.
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

Own the controlled-pet aggregate: taming eligibility/action, owner and follower-slot accounting, order authorization/state, transfer/release, stable/claim/auto-stable, persistence, login/logout reconciliation, and cleanup. Route shared skill gain to `uo-skills-stats-races`, creature definition to `modernuo-content-patterns`, and movement algorithms to `modernuo-pathfinding`.

## Core Workflow

1. State era/profile, creature, actor, taming/ownership state, control slots, intended order or transition, stable context, and expected observable result.
2. Inspect `AnimalTaming`, `BaseCreature`, pet order handlers/state, trainer stable flow, `PlayerMobile` follower and auto-stable behavior, serialization/migrations, and focused pet-order tests.
3. Trace the lifecycle: wild -> taming attempt -> controlled ownership -> order execution -> transfer/release -> stable -> claim/auto-claim -> death/delete. Identify the authoritative owner and slot mutation at every edge.
4. Validate actor, target, range/visibility, creature eligibility, existing ownership, follower capacity, commandability, and destination before mutating owner, control state, location, or stable collections.
5. Make multi-object transitions failure-safe. Ownership, follower count, control target/order, stable storage, and world placement must either converge or roll back without orphaning or duplicating a pet.
6. Add deterministic tests for authorization, slot boundaries, transfer/release, order changes, stable capacity, claim placement failure, auto-stabling, login reconciliation, save/load, and deletion cleanup.

## Evidence boundary

Establish official taming difficulty, control chances, slot costs, stable limits/fees, loyalty, and era behavior through `uo-official-evidence`. Repository values prove implementation state only; emulator or community tables cannot resolve official rules.

## Output Contract

Return a pet lifecycle/state diagram, taming/control/slot matrix, order authorization trace, stable and rollback behavior, persistence and orphan/duplication risks, changed source/tests, exact automated results, and remaining in-game checks.

## Reference Routing

- Read [taming-and-control.md](references/taming-and-control.md) for eligibility, attempts, ownership, follower slots, loyalty/control, and transfer/release.
- Read [pet-ownership-lifecycle.md](references/pet-ownership-lifecycle.md) for orders, authorization, login/logout, death/delete, persistence, and cleanup.
- Read [stabling-and-auto-stabling.md](references/stabling-and-auto-stabling.md) for trainer speech/actions, stable capacity, claim, auto-stable, rollback, and placement.

## Verification

- Cover tameable/untameable, already controlled, owner/non-owner, capacity boundaries, success/failure, transfer acceptance/rejection, release, and every supported pet order.
- Run focused `PetOrderTests` and add taming/stable regression tests where coverage is absent.
- Cover stable/claim success and failure, login/logout, internal-map storage, save/load, dead/deleted pets, owner deletion, and follower-slot reconciliation.
- Self-check that summoned followers were not treated as tameable pets and that pathfinding changes remain with the movement owner.
