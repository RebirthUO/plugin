---
name: modernuo-pathfinding
description: >
  Use when changing or diagnosing ModernUO AI movement, PathFollower,
  MovementPath, bounded A*, StepCache, .swb caches, prebake, PathCache commands,
  or pathfinding tests and tuning. Do not use for generic distance math alone;
  route exact range geometry to modernuo-spatial-range-geometry.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, pathfinding, ai, movement, performance]
    related_skills:
      - modernuo-performance-hot-paths
      - modernuo-threading
      - modernuo-spatial-range-geometry
      - modernuo-server-lifecycle
      - modernuo-test-workflow
      - modernuo-code-audit
---

# ModernUO Pathfinding

## Boundary

Preserve both movement correctness and the main-thread cost model across greedy
approach logic, bounded A*, walkability caches, persisted `.swb` data, prebake,
and diagnostics.

## Workflow

1. Reproduce with actor type/capabilities, map, start, goal, desired range,
   obstacle state, and cache state. Capture `PathRecord` or focused test evidence.
2. Trace the current path through `ApproachTarget`, `PathFollower`,
   `MovementPath`, `BitmapAStarAlgorithm`, and `StepCache` before changing a
   budget or fallback.
3. Keep open terrain on the greedy fast path. Engage or retain a path follower
   only when a step fails or makes no real progress.
4. Treat cache data as optional optimization: misses and unsupported walkers
   must fall through to live movement validation.
5. Compare solved routes, failed-route cost, allocations, and cache behavior on a
   representative corpus before tuning.
6. Run pathfinding tests sequentially and include cache-format tests when `.swb`
   layout or fingerprinting changes.

## Guardrails

- The local `38x38` search window and default `MaxSearchNodes` of `1000` are CPU
  guards. Do not raise them from anecdotal evidence.
- Do not replace bounded local A* with an unbounded/global search without a
  measured game-loop budget.
- `.swb` files are fingerprint-bound lazy backing stores, not portable universal
  assets. Stale data must regenerate from local client data.
- Resident chunk limits bound RAM; synchronous chunk building in movement hot
  paths requires tick-impact evidence.
- Preserve stationary-unreachable give-up behavior while testing moving targets,
  pets, and obstacle detours separately.
- Shared A* statics and live map data make parallel pathfinding tests unsafe.

## Output Contract

Return the reproduction, traced decision point, cache/budget assumptions, exact
behavioral change, benchmark/test evidence, and residual map/client-data risks.

```text
[PATHFINDING] {severity}: {issue}
  Actor/route: {type}, {map}:{start}->{goal}, range {n}
  Cache: {resident/lazy/miss/fingerprint}
  Evidence: {PathRecord|PathCacheStats|test|benchmark}
```

## Verification

- Cover open terrain, obstacle detour, moving goal, unreachable goal, and the
  relevant walker capability.
- Verify cache miss/fingerprint/eviction behavior when caches changed.
- Compare before/after solved count and failed-route cost for tuning work.
- Report focused tests and benchmarks separately from unmeasured reasoning.

## Reference Routing

- Read `dev-docs/pathfinding.md` for architecture, commands, formats, and current
  tuning evidence.
- Load `modernuo-server-lifecycle` for prompt/prebake phase changes,
  `modernuo-threading` for main-loop constraints, and
  `modernuo-spatial-range-geometry` for exact bounds semantics.
