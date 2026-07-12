---
name: uo-living-world-review
description: Use when a proposed ModernUO or UO change has a concrete cross-system effect on progression, PvP/PvM, economy, housing/storage, travel, social systems, client experience, or player trust. Evaluate those product consequences after official behavior is established. Do not use as a general router or mechanics authority.
version: 1.0.0
author: RebirthUO
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: gate
    workflow_phase: none
    workflow_tier: support
    tags:
    - UltimaOnline
    - ModernUO
    - Product
    - Parity
    related_skills:
    - uo-official-evidence
    - modernuo-era-expansion
    - modernuo-era-change-gate
license: MIT
---
# UO Living-World Review

## Boundary

This gate identifies product consequences and evidence requirements before code, balance, policy, or documentation decisions. It does not decide mechanics or implementation details; route those to the narrow domain skill after the review frame is set.

## Core Workflow

1. State the configured project/profile, official era/ruleset, facet/map, parity versus explicit custom policy, and unknowns.
2. Name affected and intentionally unaffected player loops: progression, PvM, PvP, economy/crafting/vendors, housing/storage/IDOC, travel/maps, social/events, client presentation.
3. Capture expected official behavior through `uo-official-evidence`, then inspect the smallest local repo anchors that prove registration, gate, data, reachability, and tests.
4. Separate official evidence, discovery material, implementation evidence, and custom policy. A present class is not proof that players can reach the feature.
5. Fill the side-effect row: beneficiaries, stressed/losing playstyles, faucet/sink/trade/storage impact, PvP counterplay, PvM risk/reward, housing/trust, new/veteran players, bot/exploit risk, client/save compatibility.
6. Choose the smallest safe action and define rollback, validation, and monitoring for live-impacting changes. Hand the result to the owning domain skill.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return the assumption frame, source URLs, repo anchors, reachability status, side-effect row, explicit unknowns, recommended smallest action, rollback/validation, and the domain skill that owns execution.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for the product-loop and side-effect prompts.

## Verification

- Every official product claim has official evidence or remains blocked.
- At least one affected and one unaffected loop are named.
- Local behavior is labeled canonical match, partial, custom, or unreachable.
- Self-check that anecdote, community, emulator, repo-only evidence, or current-live wording was not presented as universal era truth.
