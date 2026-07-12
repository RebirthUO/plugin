---
name: uo-item-property-review
description: Use when reviewing or planning a named official Ultima Online item property for a ModernUO-based repository, including official evidence, era/container placement, tooltip or cliloc, gameplay hooks, distribution boundaries, and tests. Do not use for ordinary item construction, unrelated combat mechanics, or automatic loot rollout.
version: 1.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - ultima-online
      - item-properties
      - modernuo
      - evidence
    related_skills:
      - uo-official-evidence
      - uo-aos-item-properties
      - uo-sa-item-property-implementation
      - uo-items-foundation
---

# UO Item Property Review

## Boundary

Turn a named property into an evidence-backed review. Storage, presentation, mechanics, and distribution are separate; test/GM support does not authorize economy rollout.

## Core Workflow

1. Confirm property, repository/issue revision, era/ruleset, output, and review-versus-plan authority.
2. Classify official, dated community, custom policy, current repo, pinned comparison-engine, and unresolved evidence; expose conflicts.
3. Decide property-only versus reusable mechanics. Scope shared timers/state/events/damage/buffs/cleanup before artifacts.
4. Choose era, hosts, and container from current free values, aggregation, persistence, inherited properties, and pre-era behavior—not a copied enum.
5. Verify cliloc/client presentation separately from mechanics. Define formula, trigger/order, actual/raw basis, caps, PvP/PvM, cooldown/stacking, lifecycle cleanup, durability/resources, and exclusions.
6. Keep `(L)`, `(R)`, or found-on distribution separate. Test era, round trip, aggregation, tooltip, trigger/boundaries/cleanup, pre-era, and non-distribution.

## Guardrails

- Pin comparison-engine revisions and re-check current containers/free values before implementation.
- Found-on rows do not supply omitted formulas/lifecycle; special markers are not automatically rollable properties.
- Another engine's cliloc is guidance, not official mechanics proof.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return evidence classes, era/hosts/container, tooltip status, mechanic/lifecycle contract, distribution boundary, repo anchors, tests, slices, policy decisions, and `missing evidence`.

## Verification

- Evidence tiers and four property surfaces stay distinct; transient effects have reset/cleanup tests.
- Pre-era/negative paths exist and property-only work implies no economy rollout.

## Reference Routing

Use the [property reference index](references/README.md) and load only the named property. Read scope correction only when the ticket needs a reusable mechanic.
