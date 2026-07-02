---
name: modernuo-performance-hot-paths
description: >
  Use when reviewing or changing ModernUO hot-path performance: AI ticks, combat loops,
  spatial scans, packet/message sends, region hooks, timers, pathfinding, allocation-heavy
  strings, LINQ, pooled collections, buffers, and game-loop cost decisions.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
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
      - uo-modernuo-workflow
---

# ModernUO Performance Hot Paths

## Purpose

Use this skill as the performance decision lens for ModernUO/RebirthUO code. It does not replace `modernuo-code-audit` or `dev-docs/code-standards.md`; it routes performance questions to the right source and forces a hot/warm/cold classification before choosing LINQ, allocation, string, spatial, or pathfinding patterns.

ModernUO game logic runs on a single-threaded event loop. A small cost in an AI tick, combat loop, packet fan-out, region hook, or timer callback can become shard-wide latency. A small cost in an admin command may be irrelevant. Classify before optimizing.

## When to Use

- Reviewing or changing code that runs per tick, per movement, per combat swing, per spell target, per AI think, per region hook, per visible client, or per timer pulse.
- Replacing or adding LINQ, `new List<T>()`, `ArrayPool<T>.Shared`, `StringBuilder`, dynamic string formatting, packet writing, spatial scans, or pathfinding calls.
- Tuning pathfinding, region lookup, map range queries, broadcast/message loops, gump/property-list generation, or pooling behavior.
- Migrating RunUO code that uses broad world scans, allocating LINQ chains, old `Timer` subclasses, or ad-hoc lists in gameplay loops.
- Deciding whether a performance concern is worth fixing now or should be noted as cold-path/readability acceptable.

## Path Classification

| Path | Examples | Default posture |
|---|---|---|
| **Hot** | AI think/movement, combat damage loops, spell AoE target scans, packet fan-out, region enter/move hooks, timer callbacks running often, property-list/gump/message generation for many clients | Avoid avoidable allocation and O(world) scans. Prefer spatial queries, pooled collections, stackalloc/handlers, and explicit loops. |
| **Warm** | Player command used regularly, one gump page build, one craft/loot operation, login/logout hooks, infrequent scheduled checks | Tier 1 LINQ is fine; Tier 2 may be fine. Avoid obvious allocations inside nested loops or fan-out. |
| **Cold** | Admin-only commands, startup validation, one-off migration tools, test setup, rare diagnostics | Prefer clarity unless the code blocks startup, saves, or operator workflows. Still avoid dangerous threading/world mutation rules. |

Completion criterion: every performance review names the path class and why the chosen pattern is acceptable for that class.

## Decision Matrix

| Question | Prefer | Avoid / escalate | Load for details |
|---|---|---|---|
| Need nearby entities? | `map.GetMobilesInRange<T>()`, `GetItemsInRange<T>()`, bounds queries | `World.Mobiles` / `World.Items` full scans in gameplay | `modernuo-spatial-range-geometry`, `modernuo-code-audit` |
| Need temporary collection on hot path? | `PooledRefList<T>.Create()` or stack/local direct loop | `new List<T>()` in repeated loops | `modernuo-threading`, `modernuo-code-audit` |
| Need rented array/buffer in game code? | `STArrayPool<T>.Shared` with `finally` return | `ArrayPool<T>.Shared` unless truly multi-threaded infrastructure | `modernuo-threading` |
| Need dynamic text? | Handler-aware `$"..."` literal at call site; `ValueStringBuilder` for assembled spans | `StringBuilder`, `string.Format`, `.ToString()` inside handler holes, ternary interpolated branches | `modernuo-string-handling` |
| Need packet/message fan-out? | Existing `Mobile`/`Item`/`NetState` APIs and handler overloads; range clients | Manual packet duplication or string prebuilding | `modernuo-networking`, `modernuo-string-handling` |
| Need region lookup? | `Region.Find(Point3D, Map)` in gameplay; cache when repeated | `Region.Find(string, Map)` in hot paths | `modernuo-regions` |
| Need pathfinding change/tuning? | Preserve greedy fast path; bounded A*; evidence from diagnostics/tests | Global search, raising budgets from anecdote, sync cache build in new hot path | `modernuo-pathfinding`, `modernuo-threading` |
| Need LINQ? | Tier 1 on hot paths; Tier 2 on warm paths; manual loops for Tier 3 | Blanket “no LINQ” or unchecked allocating chains | `modernuo-code-audit`, `dev-docs/code-standards.md` |

## Core Rules

1. **Do not optimize blind.** First identify whether the code is hot, warm, or cold. If it is hot, explain invocation frequency or fan-out. If it is cold, prefer clear code unless it risks startup, saves, or operator workflows.

2. **No O(world) scans in gameplay.** Do not iterate `World.Mobiles` or `World.Items` for local mechanics. Use map/sector spatial APIs and verify range geometry when source parity depends on exact tiles.

3. **Use LINQ tiers, not folklore.** ModernUO targets .NET 10; some LINQ is optimized. Tier 1 patterns from `modernuo-code-audit` are acceptable on hot paths. Tier 2 patterns are warm-path/benchmark choices. Tier 3 patterns remain forbidden on hot paths.

4. **Avoid heap churn in repeated loops.** Prefer direct loops, `PooledRefList<T>`, stackalloc, `Span<T>`, `ValueStringBuilder`, and handler-aware APIs. Allocations inside nested loops, fan-out, AI ticks, or per-client broadcasts need justification.

5. **Use single-threaded pools in game code.** `STArrayPool<T>.Shared` avoids lock overhead. `ArrayPool<T>.Shared`, concurrent collections, locks, and atomics belong only in explicitly multi-threaded server infrastructure.

6. **Keep strings zero-alloc where APIs support it.** A direct `$"..."` literal in a handler-aware call can avoid string allocation. Prebuilding the string in a local, ternary, switch expression, `string.Format`, concat inside holes, or `.ToString()` inside holes usually defeats that path.

7. **Respect pathfinding budgets.** `BitmapAStarAlgorithm` is bounded local A* on the main thread. Do not raise `MaxSearchNodes`, alter StepCache behavior, or add synchronous cache builds without corpus, diagnostic, or benchmark evidence.

8. **Region lookup has hot/cold forms.** `Region.Find(Point3D, Map)` is sector-indexed. `Region.Find(string, Map)` is a linear name scan; keep it to config, JSON resolution, startup, admin tools, or rare flows.

9. **Performance does not override era or gameplay.** If a faster implementation changes PvP/PvM, economy, housing, facet, or era behavior, treat it as a mechanics change and use the relevant UO domain/era skill.

10. **Report measured vs reasoned confidence.** If no benchmark/test was run, say the finding is static/hot-path reasoning. Do not present a static allocation review as measured performance proof.

## LINQ Quick Gate

Use `modernuo-code-audit` as the source of truth. This summary only decides routing:

- **Hot path:** only Tier 1 LINQ without further justification; use manual loops for Tier 3 and usually for Tier 2 when repeated per tick/per target.
- **Warm path:** Tier 1 and Tier 2 are acceptable; Tier 3 needs a reason or a manual alternative.
- **Cold path:** clarity can win, but avoid patterns that become O(world), save-thread unsafe, or hidden allocation explosions over large data.

Never write or enforce “no LINQ in game logic” as a blanket rule. The correct rule is path class + LINQ tier.

## Common Patterns

### Spatial scan with pooled list

```csharp
using var targets = PooledRefList<Mobile>.Create();
foreach (var m in map.GetMobilesInRange<Mobile>(location, range))
{
    if (m.Alive && m.CanBeHarmful(source))
    {
        targets.Add(m);
    }
}
```

Use when targets are reused after enumeration. If work can be done immediately, skip the list and process in the loop.

### Handler-aware message

```csharp
from.SendMessage($"You hit {target.Name} for {damage:N0} damage.");
```

Do not prebuild the string unless it is reused. For branching text, branch the call so each arm keeps a direct `$"..."` argument.

### Region lookup

```csharp
var region = Region.Find(point, map); // sector-indexed gameplay lookup
```

Reserve `Region.Find("Name", map)` for startup/config/admin flows unless you have measured that it is cold enough.

## Anti-Patterns

- Blanket “No LINQ in game logic” guidance that conflicts with .NET 10 tier rules.
- `World.Mobiles.Values.Where(...).ToList()` for local gameplay effects.
- `new List<T>()` in AI, movement, combat, spell, or broadcast loops where `PooledRefList<T>` or direct processing would work.
- `ArrayPool<T>.Shared` in normal single-threaded game code.
- `System.Text.StringBuilder` instead of `ValueStringBuilder`.
- Prebuilt interpolated locals passed once to `SendMessage`, `AddLabel`, `IPropertyList.Add`, `SpanWriter.Write*`, or related handler-aware APIs.
- `Region.Find(string, Map)` from movement, combat, spell, or frequently firing region code.
- Raising pathfinding budgets or disabling give-up behavior based only on one anecdotal route.
- Adding background threads to “fix” game-loop performance.

## Review Checklist

- [ ] Path classified as hot, warm, or cold with evidence.
- [ ] No local gameplay mechanic uses `World.Mobiles` / `World.Items` full scans.
- [ ] LINQ use is classified by tier; Tier 3 is absent from hot paths.
- [ ] Temporary collections/buffers use pooled/stack patterns when repeated.
- [ ] Handler-aware text keeps direct `$"..."` call-site binding where possible.
- [ ] Pathfinding or region lookup changes preserve existing cost model and diagnostics.
- [ ] Any performance claim states whether it is measured, tested, benchmarked, or static reasoning.

## How to Report Issues

```text
[PERF] {severity}: {hot-path issue}
  File: {path}:{line}
  Path class: {hot|warm|cold} because {reason}
  Cost: {allocation|O(world)|linear region scan|string allocation|pathfinding budget|threading overhead}
  Suggested route: {skill or doc to load}
  Evidence: {static reasoning, grep count, test, benchmark, profiler, diagnostic command}
```

Severity guide:

- `ERROR`: O(world) scan in gameplay; background thread touching game state; pathfinding change likely to stall the main loop; allocation in very high-frequency fan-out with easy zero-alloc replacement.
- `WARN`: likely hot-path allocation; Tier 3 LINQ in warm/hot path; avoidable string/collection allocation; linear region name scan in repeated code.
- `INFO`: cold-path clarity tradeoff, optional benchmark, or documentation suggestion.

## See Also

- `modernuo-code-audit` — enforcement checklist and LINQ tier details.
- `modernuo-threading` — single-threaded game loop, STArrayPool, PooledRefList, and world-save threading.
- `modernuo-string-handling` — `ValueStringBuilder` and interpolation-handler anti-patterns.
- `modernuo-regions` — `Region.Find` and dynamic region lifecycle.
- `modernuo-pathfinding` — bounded A*, StepCache, `.swb` files, and tuning evidence.
- `modernuo-spatial-range-geometry` — exact range and bounds semantics.
- `modernuo-networking` — packet/message fan-out and span writers.
- `dev-docs/code-standards.md`, `dev-docs/string-handling.md`, `dev-docs/pathfinding.md`.
