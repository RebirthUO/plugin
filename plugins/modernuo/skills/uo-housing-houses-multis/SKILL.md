---
name: uo-housing-houses-multis
description: Use when adding, debugging, or auditing ModernUO-based house placement, BaseHouse/multi ownership, HouseRegion permissions, lockdowns/secures, customization, addons, transfer/demolition, or decay/IDOC. Do not use for generic region, item, crafting, or vendor logic unless it crosses the house lifecycle.
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
    - housing
    - multis
    - economy
    related_skills:
    - uo-world-facets-regions
    - uo-items-foundation
    - uo-living-world-review
    - modernuo-regions
version: 1.0.0
author: Crome696
---
# UO Housing, Houses, and Multis

## Boundary

Own the house aggregate and its trust-critical lifecycle: placement, multi/sign/region creation, access roles, lockdown/secure accounting, customization/addons, ownership transfer, refresh/decay, demolition, and cleanup. Route generic map/region behavior to `uo-world-facets-regions` and base item semantics to `uo-items-foundation`.

## Core Workflow

1. State ruleset/facet, house type, actor role, storage/decay policy, and whether behavior is canonical or custom. Treat housing changes as trust and economy changes.
2. Inspect the active `BaseHouse`, sign/gump, `HouseRegion`, placement validator, customization/design data, addon tracking, decay scheduler, rental/vendor paths, serialization, and focused tests.
3. Trace the affected transaction end to end: validate actor/location/capacity -> mutate house-owned collections/counters -> update sign/region/multi -> invalidate UI/properties -> persist -> reverse/cleanup on failure or deletion.
4. Use the authoritative house APIs for owner, roles, lockdowns, secures, addons, transfer, and demolition. Never toggle item flags or delete a house directly while bypassing counters, region deregistration, or addon cleanup.
5. For component/data work, verify actual client TileData and use the initialized UOContent test collection. For decay, use deterministic time/scheduler seams; do not wait on wall clock.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return actor/permission and lifecycle matrices, source/repo anchors, storage/IDOC/trust risks, save compatibility, changed files, rollback boundary, and exact validation results.

## Reference Routing

Read [domain-map.md](references/domain-map.md) for detailed component/placement/role/customization/decay notes, examples, and the UOContent component-test fixture. Re-confirm numeric capacities, decay durations, and facet availability before changing them.

## Verification

- Build and run focused placement, permission, storage, customization/component, transfer, and decay tests as applicable.
- Cover owner/co-owner/friend/access/banned/outsider cases and capacity boundaries.
- Prove multi, sign, region, addons, secured/locked items, and counters remain consistent after success, rollback, save/load, transfer, demolition, and decay.
- Self-check that no orphan region/addon or uncounted locked item can remain.
