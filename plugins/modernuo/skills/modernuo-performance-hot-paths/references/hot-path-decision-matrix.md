# Hot-Path Decision Matrix

Read this reference after classifying the path as hot, warm, or cold.

| Need | Prefer | Escalate/avoid | Specialist |
|---|---|---|---|
| Nearby entities | map/sector range or bounds query | `World.Mobiles`/`World.Items` gameplay scan | `modernuo-spatial-range-geometry` |
| Temporary targets | direct loop; otherwise `PooledRefList<T>` | repeated `new List<T>()` | `modernuo-threading` |
| Buffer in game code | bounded stack storage or `STArrayPool<T>` with `finally` return | `ArrayPool<T>.Shared` without worker context | `modernuo-threading` |
| Dynamic text | direct handler interpolation or `ValueStringBuilder` | pre-built/intermediate strings | `modernuo-string-handling` |
| Packet/message fan-out | current `Mobile`/`Item`/`NetState` range APIs | manual packet duplication | `modernuo-networking` |
| Region lookup | `Region.Find(point, map)` | name scan in repeated gameplay | `modernuo-regions` |
| Pathfinding | greedy fast path, bounded A*, measured corpus | global search or anecdotal budget increase | `modernuo-pathfinding` |
| LINQ | repository Tier 1 on hot paths; Tier 2 by evidence | Tier 3 allocating chains on hot paths | `modernuo-code-audit` |

## Path classification

- **Hot:** AI think/movement, combat/damage, spell target scans, region movement,
  recurring timer pulses, per-client packet fan-out. Avoid avoidable allocation,
  linear/global scans, blocking, and unnecessary synchronization.
- **Warm:** regular commands, one gump build, login/logout, crafting/loot operation.
  Clarity can win unless work nests, fans out, or allocates substantially.
- **Cold:** startup validation, admin diagnostics, migrations, test setup. Prefer
  clarity unless the operation blocks boot/save/operator workflows or scales with
  all world state.

## LINQ gate

Use the current `dev-docs/code-standards.md` tier definitions. Do not memorize
operator classifications across .NET/repository revisions.

- Hot: Tier 1 only by default; manual loops for Tier 3 and usually repeated Tier 2.
- Warm: Tier 1/2 normally acceptable; justify Tier 3 or use a loop.
- Cold: clarity is acceptable, but avoid hidden O(world) and very large materialization.

## Evidence standard

Correctness tests show behavior, not speed. Static review may identify an obvious
allocation or complexity regression, but claims about throughput, GC, tick time,
or solved-route rate require a reproducible benchmark/profile. Record data set,
iteration count, runtime/build mode, before/after values, and variance.
