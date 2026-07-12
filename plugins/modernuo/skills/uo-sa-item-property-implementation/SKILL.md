---
name: uo-sa-item-property-implementation
description: Use when an implementation-ready task adds or fixes an official Stygian Abyss item property in a ModernUO-based repository across storage, OPL, gameplay hooks, transient contexts, persistence, and tests. Do not use for research-only parity, post-SA properties, or loot/runic/imbuing rollout unless those surfaces are explicitly approved.
version: 1.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    tags:
    - ultima-online
    - modernuo
    - stygian-abyss
    - item-properties
    related_skills:
    - uo-aos-item-properties
    - uo-combat-pipeline
    - modernuo-serialization
    - modernuo-test-workflow
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
---
# UO SA Item Property Implementation

## Boundary

Own the implementation step for a reviewed SA property. `uo-aos-item-properties` remains the architecture authority; this skill adds SA-specific readiness, gates, gameplay placement, cleanup, and regression expectations. A source table row alone is not implementation-ready.

## Core Workflow

1. Require an explicit ruleset, canonical sources, supported item family, intensity/chance/formula/caps/timing, cliloc, acceptance criteria, persistence decision, and non-goals. Resolve blocking source conflicts before coding.
2. Inspect the active branch and reviewed issue: current property containers/free bits, owning `Base*` items, actual combat/spell/damage consumer, serializers/migrations, distribution surfaces, and focused tests.
3. Choose storage with the AoS taxonomy: prefer an existing semantic container when safe or a neutral mechanic/family overflow container. Do not default to an expansion-named container and do not widen save-sensitive storage casually.
4. Implement storage, GM wrapper, defaults/dupe/migration, SA-gated OPL, and the owning gameplay hook separately. Incoming-damage properties must use normalized actual/post-resist damage and preserve typed branches such as Armor Ignore/direct/mixed damage.
5. Keep cooldown/charge/stack/timer contexts transient unless persistence is required. Clean them on equipment/property loss, death/deletion, logout, map invalidation, and expiry; queue-full events must still update cadence when the mechanic says “since last damage.”
6. Leave loot/runic/reforging/imbuing/artifact distribution unchanged unless explicitly scoped and source-backed.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return the readiness/source decision, changed-surface matrix, container/bit and migration rationale, effect formula/caps/timing, cleanup map, distribution decision, risks, and exact build/test evidence.

## Reference Routing

Read [domain-map.md](references/domain-map.md) only for the detailed Battle Lust example, incoming-damage branch checklist, and historical verification patterns. For container and named-property details, follow the focused references routed by `uo-aos-item-properties`.

## Verification

- Build and run focused property tests plus adjacent combat/spell/damage tests.
- Cover supported/unsupported hosts, SA and pre-SA, OPL, formula/caps, normal/direct/Armor Ignore/mixed branches as relevant, timing/cooldown/queue-full cadence, cleanup, dupe/save migration, and distribution guard.
- Use actual applied deltas when the rule says damage dealt/received.
- Self-check that focused tests are not reported as broad-suite green.
