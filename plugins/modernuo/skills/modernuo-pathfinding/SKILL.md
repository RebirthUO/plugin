---
name: modernuo-pathfinding
description: Use when working with ModernUO creature movement, BaseAI approach behavior, PathFollower, MovementPath, BitmapAStarAlgorithm, StepCache, .swb path cache files, pathfinding first-boot prebake, PathCache admin commands, PathRecord telemetry, or pathfinding tests and benchmarks. Use before tuning pathfinding.maxSearchNodes, pathfinding.maxResidentChunks, pathfinding.prebakeMaps, cache file formats, AI obstacle behavior, pet follow/chase behavior, or map walkability cache logic.
---

# ModernUO Pathfinding

## Purpose

Use this skill to preserve movement correctness and shard performance when changing AI navigation, A* search, static walkability caching, path cache files, first-boot prebake, or pathfinding diagnostics.

## When This Activates

- Editing `Projects/UOContent/Engines/Pathing/`, `Mobiles/AI/BaseAI/AIMovement.cs`, movement/path cache tests, or pathfinding config.
- Debugging pets, monsters, vendors, escorts, or bosses that stall, oscillate, fail to chase, or path through/around obstacles incorrectly.
- Changing `BitmapAStarAlgorithm`, `StepCache`, `StepCacheFile`, `PathFollower`, `MovementPath`, `PathfindRecorder`, or `[Path*]` admin commands.
- Adjusting `.swb` bake/load behavior, file formats, cache eviction, promotion thresholds, or map/static walkability rules.

## Key Rules

- Open terrain should stay on the greedy fast path; persistent `PathFollower` should engage when greedy movement stalls or a blocked/auto-turn step makes no real progress.
- `BitmapAStarAlgorithm` is bounded local A*: the `38x38` search window and `MaxSearchNodes` are intentional CPU guards, not incidental constants.
- The default `MaxSearchNodes` of `1000` is a tuned balance; do not raise it without corpus evidence showing solved routes improve more than failed-route cost regresses.
- `StepCache` is an optimization layer. Cache misses and unsupported walkers must fall through to live movement checks, not silently approve movement.
- `.swb` files are optional lazy backing stores. They reduce first-pathfind-after-boot latency but should stay fingerprint-gated and RAM-bounded by resident chunk limits.
- Pathfinding tests that share A* statics or live map data must stay in the sequential pathfinding collection.

## Patterns

### AI Approach Decision

Use the centralized `ApproachTarget` primitive for chase/follow logic. It takes one greedy LOS step only when the move succeeds and gets closer; otherwise it creates or keeps a `PathFollower` and tracks best-distance progress before giving up on a stationary unreachable goal.

### Cache Operation Flow

Use `PathCacheCommands.Configure()` for resident-chunk cap and command registration, `ConfigurePrompts()` only for the first-boot prebake choice, and `Initialize()` for baking missing/stale `.swb` files after tile data and world load.

### Diagnostics

Use `[PathCacheStats]`, `[PathCacheClear]`, `[PathBake]`, `[PathCacheSave]`, `[PathCacheLoad]`, and `[PathRecord]` to inspect cache behavior before changing algorithms. Prefer test corpus and recorder evidence over anecdotal movement reports.

## Anti-Patterns

- Replacing bounded local A* with a global search without a main-thread cost model.
- Treating `MaxSearchNodes` as a quality knob only; it is also a single-threaded CPU budget.
- Building cache chunks synchronously in new hot movement paths without measuring tick impact.
- Assuming a pathfinding test can run in parallel with another pathfinding test.
- Shipping `.swb` files as universal assets; they are tied to tile data fingerprints and should regenerate from local client data.
- Fixing an unreachable-target behavior by disabling give-up logic for all chases.

## Real Examples

- `Projects/UOContent/Mobiles/AI/BaseAI/AIMovement.cs` centralizes pet/chase obstacle behavior in `ApproachTarget`.
- `Projects/UOContent/Engines/Pathing/BitmapAStarAlgorithm.cs` owns the bounded A* search, per-find scratch buffers, `MaxSearchNodes`, and StepCache integration.
- `Projects/UOContent/Engines/Pathing/PathCacheCommands.cs` wires first-boot prebake, lazy `.swb` loading, and pathfinding admin commands.
- `Projects/UOContent.Tests/Tests/Mobiles/AI/ApproachTargetTests.cs` covers open terrain, obstacle detours, moving targets, and unreachable target give-up behavior.
- `Projects/UOContent.Tests/Tests/Engines/Pathing/StepCacheFileV8Tests.cs` protects the compact `.swb` v8 format.

## How to Report Issues

Report pathfinding issues with the actor, map/coordinates, branch, cache state, and test evidence:

```text
[PATHFINDING] {severity}: {movement/cache/format issue}
  Actor: {mobile type and movement capability}
  Route: {map, start, goal, range}
  Evidence: {PathRecord, PathCacheStats, test, benchmark, or repro file}
  Suggested check: {specific xUnit test or diagnostic command}
```

## See Also

- `dev-docs/pathfinding.md` - architecture, tuning levers, cache formats, and benchmark notes.
- `dev-docs/server-lifecycle.md` - why prebake prompting and baking are split across startup phases.
- `plugins/modernuo/skills/modernuo-server-lifecycle/SKILL.md` - startup and first-boot prompt rules.
- `plugins/modernuo/skills/modernuo-threading/SKILL.md` - single-threaded game-loop performance constraints.
- `plugins/modernuo/skills/modernuo-spatial-range-geometry/SKILL.md` - spatial query range semantics.
