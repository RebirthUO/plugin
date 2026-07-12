---
name: modernuo-performance-hot-paths
description: >
  Use when reviewing or changing ModernUO game-loop hot paths such as AI,
  combat, spatial scans, packet fan-out, region hooks, timers, pathfinding,
  pooling, LINQ, or dynamic text. Do not use to claim a measured speedup without
  profiling or benchmarks; use modernuo-code-audit for the broader code review.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, performance, hot-paths, allocations, game-loop]
    related_skills:
      - modernuo-code-audit
      - modernuo-threading
      - modernuo-string-handling
      - modernuo-regions
      - modernuo-pathfinding
      - modernuo-spatial-range-geometry
      - modernuo-networking
      - modernuo-content-patterns
      - migrate-foundation
      - modernuo-codebase
---

# ModernUO Performance Hot Paths

## Boundary

Classify cost before optimizing. Hot code runs per tick, movement, combat event,
target, region hook, timer pulse, or visible client; warm code runs regularly but
not continuously; cold code is startup, admin, migration, or rare diagnostics.
Optimize repeated/fan-out cost while preserving gameplay and era behavior.

## Workflow

1. Name the path class, invocation frequency, fan-out, and current evidence.
2. Trace the owning API and inspect neighboring code before replacing a query,
   collection, buffer, string, region lookup, or pathfinding budget.
3. Find the dominant cost: O(world) enumeration, allocation, formatting, copying,
   algorithmic budget, blocking work, or unnecessary synchronization.
4. Apply the smallest repository-native change that removes that cost without
   changing target sets, ordering, timing, or era mechanics.
5. Run a focused correctness test first; benchmark/profile representative load
   for any performance claim.

## Guardrails

- Never scan `World.Mobiles` or `World.Items` for local gameplay. Use map/sector
  range or bounds queries and verify exact geometry when range matters.
- Process directly when possible; otherwise use repository-native pooled/stack
  storage selected for the actual thread context.
- Apply the repository LINQ tiers. Do not enforce a blanket no-LINQ rule, but keep
  allocating/chained Tier 3 patterns out of hot paths.
- Keep handler-aware `$"..."` expressions directly at message/gump/property-list
  call sites; pre-built strings and `.ToString()` holes defeat zero-allocation
  formatting.
- `Region.Find(point, map)` is sector-indexed; name lookup is a linear cold-path
  operation.
- Do not raise A* budgets, add synchronous cache construction, or move world state
  to background threads as an unmeasured shortcut.
- Performance work cannot silently change gameplay or era semantics.

## Output Contract

Return the path class and frequency, before/after algorithm or allocation shape,
behavioral invariants, evidence type, commands/results, and residual risk.

```text
[PERF] {ERROR|WARN|INFO}: {issue}
  File: {path}:{line}
  Path: {hot|warm|cold} because {frequency/fan-out}
  Cost: {allocation|O(world)|linear lookup|blocking|budget}
  Evidence: {static|test|benchmark|profile}
```

## Verification

- Target set, ordering, timing, and era gates are unchanged unless explicitly in
  scope.
- Focused tests pass before performance measurements are interpreted.
- Allocation/throughput/tick claims include reproducible measured evidence.

## Reference Routing

- Read [hot-path decision matrix](references/hot-path-decision-matrix.md) when
  selecting spatial, pooling, string, region, or pathfinding patterns.
- Load the corresponding specialist skill for exact APIs:
  `modernuo-threading`, `modernuo-string-handling`, `modernuo-regions`,
  `modernuo-pathfinding`, `modernuo-networking`, or
  `modernuo-spatial-range-geometry`.
- Read `dev-docs/code-standards.md` for the current LINQ tiers.
