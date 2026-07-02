---
name: modernuo-code-audit
description: >
  Use when writing, modifying, or reviewing .cs files under Projects/. Audits code for ModernUO convention, safety, serialization, lifecycle, and performance issues; reports findings by severity and asks before fixing unless fixes were explicitly requested.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, csharp, audit, safety, performance]
    related_skills:
      - modernuo-serialization
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-threading
      - modernuo-performance-hot-paths
      - modernuo-string-handling
      - modernuo-property-lists
      - modernuo-gump-system
      - modernuo-content-patterns
      - modernuo-test-workflow
---

# ModernUO Code Audit

## When to Use
- Any time you write, edit, or modify a `.cs` file under `Projects/`
- After generating code snippets for the user
- During code review

## Audit Rules

Flag findings by severity but do NOT auto-fix. Report issues and ask before changing code unless the user explicitly requested automatic fixes.

## Quick Pre-Submit Checklist

For any `.cs` edit under `Projects/`, check this before claiming done:

- Logging uses `LogFactory.GetLogger(...)`, not `Console.WriteLine` / `Console.Write`.
- Game logic does not introduce `lock`, `volatile`, concurrent collections, `Task.Run`, thread pool work, or manual threads.
- World scans avoid `World.Mobiles` / `World.Items`; prefer map/sector spatial queries.
- Deleted objects cancel timers/tokens and clear held `Item` / `Mobile` references in `OnDelete()` / `OnAfterDelete()`.
- Serializable types follow `[SerializationGenerator]`, `partial`, `[Constructible]`, non-serialized `TimerExecutionToken`, and generated-version migration rules.
- Hot paths avoid allocating LINQ, `new List<T>()`, `ArrayPool<T>.Shared`, and `System.Text.StringBuilder` unless the detailed rules below explicitly allow the pattern.
- Property lists, gumps, packets, and player-facing strings use the appropriate ModernUO handlers and no empty-gump code path exists.
- Era-conditional behavior names the target era/ruleset or asks before changing mechanics.

Completion criterion: every modified `.cs` file has been checked against this list, and any finding is reported with file/line evidence before optional fixes.

### 1. LINQ: Know What's Optimized (.NET 10)
Not all LINQ is banned. .NET 10 JIT/PGO eliminates overhead for specific patterns. Anything not listed below is still forbidden on hot paths.

**Tier 1 — Zero-cost (use freely on hot paths):**
- `foreach` over `IEnumerable<T>` backed by `T[]`, `List<T>`, `Stack<T>`, `Queue<T>` — PGO devirtualizes the enumerator, zero heap allocation
- `.Contains()` after a preceding LINQ operator (`.Distinct()`, `.OrderBy()`, `.Reverse()`, `.Union()`, `.Intersect()`, `.Except()`, `.Concat()`, `.SelectMany()`, `.Where().Select()`, `.Skip()`, `.Take()`, `.OfType()`, `.Cast()`, `.Shuffle()`) — LINQ has ~30 specialized overrides that skip the intermediate work (no sort, no HashSet, no buffering)
- `.Count()` on sized collections (`ICollection<T>`, or after `Range`/`Repeat`/`Skip`/`Take`/`Append`) — O(1) property access, no enumeration
- `.OrderBy().First()` / `.OrderByDescending().First()` / `.OrderBy().Last()` — O(N) min/max scan, no sort performed
- `.Shuffle().Take(n)` — reservoir sampling, single pass, O(n) memory
- `Enumerable.Range()` / `Enumerable.Sequence()` followed by `.Count()`, `.Contains()`, `.ToArray()`, `.ToList()`, `.ElementAt()`, `.Last()` — arithmetic, not enumeration

**Tier 2 — Low overhead (acceptable on warm paths, benchmark if critical):**
- `.Skip(n).Take(m).ToArray()` on `T[]`/`List<T>` — vectorized `Span<T>.CopyTo` (still allocates output)
- `.LeftJoin()` / `.RightJoin()` — ~2x faster than manual `GroupJoin`+`SelectMany`+`DefaultIfEmpty`
- `.Where(predicate)` on `T[]`/`List<T>` — `WhereIterator` still heap-allocates, but enumeration is PGO-optimized. Manual `foreach`+`if` is still faster for true hot paths.

**Tier 3 — Still forbidden on hot paths (write manual code):**
- `.Select(f).Where(p)` (this order — each intermediate iterator allocates)
- `.GroupBy()`, `.ToDictionary()`, `.ToHashSet()`, `.ToLookup()` (always allocate internal structures)
- `.Aggregate()` (delegate overhead per element)
- `.Sum()` / `.Min()` / `.Max()` on `float`/`double` (no SIMD in LINQ on ARM)
- `.SelectMany()` when iterating results (not `.Contains()`) — multiple enumerator allocations
- `.Zip()` when iterating — enumerator allocations
- Any LINQ over `IAsyncEnumerable<T>` — no PGO/escape analysis
- Long chains like `.Where().Select().OrderBy().Take()` — each step allocates an iterator

**Prerequisites**: .NET 10, tiered compilation + Dynamic PGO enabled (default). Tier 1 optimizations require ~30+ calls for JIT warmup.

**Quick decision**: If the exact pattern is in Tier 1 → use it. If it's in Tier 2 → acceptable unless profiling shows it's a bottleneck. If it's anything else → manual `for`/`foreach` + `PooledRefList<T>`.

### 2. No Console.WriteLine
**Bad**: `Console.WriteLine(...)`, `Console.Write(...)`
**Good**: `private static readonly ILogger logger = LogFactory.GetLogger(typeof(MyClass));` then `logger.Information(...)`, `logger.Warning(...)`, `logger.Error(...)`
**Requires**: `using Server.Logging;`

### 3. No Concurrency Primitives in Game Code
**Bad**: `ConcurrentDictionary`, `ConcurrentQueue`, `ConcurrentBag`, `volatile`, `lock(...)`, `Mutex`, `Semaphore`, `Monitor`, `Interlocked`, `ReaderWriterLock`
**Why**: Server is single-threaded. These add overhead for no benefit.
**Instead**: Use regular `Dictionary<K,V>`, `List<T>`, plain fields.

### 4. Never Iterate World.Mobiles or World.Items Directly
**Bad**: `foreach (var m in World.Mobiles.Values)`, `World.Items.Values.Where(...)`
**Good**: `map.GetMobilesInBounds<T>(bounds)`, `map.GetMobilesInRange<T>(point, range)`, `map.GetItemsInRange<T>(point, range)`
**Why**: Full world iteration is O(n) over all entities. Spatial queries use sector indexing.

### 5. Clean Up References in OnDelete/OnAfterDelete
**Check**: Classes with `Item` or `Mobile` references should clean them in `OnDelete()` or `OnAfterDelete()`.
**Pattern**:
```csharp
public override void OnAfterDelete()
{
    _someReference = null;
    base.OnAfterDelete();
}
```

### 6. Cancel Timers in OnDelete/OnAfterDelete
**Check**: Any class with `TimerExecutionToken` or `Timer` fields must cancel them on deletion.
**Pattern**:
```csharp
public override void OnAfterDelete()
{
    _timerToken.Cancel();  // For TimerExecutionToken
    _timer?.Stop();        // For Timer references
    _timer = null;
    base.OnAfterDelete();
}
```

### 7. Use STArrayPool, Not ArrayPool
**Bad**: `ArrayPool<T>.Shared.Rent(...)` in game logic
**Good**: `STArrayPool<T>.Shared.Rent(...)` in game logic
**Why**: STArrayPool is single-threaded optimized (no locks). Use ArrayPool only in explicitly multi-threaded code.
**Also**: Always return rented arrays in a `finally` block.

### 8. No new List in Hot Paths
**Bad**: `var list = new List<Mobile>();` in frequently-called methods
**Good**: `using var list = PooledRefList<Mobile>.Create();`
**Why**: PooledRefList uses pooled arrays, zero GC pressure. It's a ref struct (stack-allocated).

### 9. Serialization Class Requirements
**Check**: Classes with `[SerializationGenerator]` MUST be `partial`.
**Check**: `[Constructible]` on parameterless constructors for items/mobiles.
**Check**: `TimerExecutionToken` fields must NOT have `[SerializableField]`.
**Check**: Use `using ModernUO.Serialization;` when using serialization attributes.

### 10. No Task.Run or new Thread
**Bad**: `Task.Run(...)`, `new Thread(...)`, `ThreadPool.QueueUserWorkItem(...)` in game code
**Why**: Game logic runs on the single-threaded event loop. Background threads cause race conditions.
**Exception**: Server infrastructure code (Projects/Server/Main.cs, World saves) may use threading.

### 11. Never Assume Era
**Check**: If code uses era-conditional logic (`Core.AOS`, `Core.SE`, etc.) and the user hasn't specified a target era, ASK which expansion to target.
**Why**: Different eras have dramatically different mechanics.

### 12. Naming Conventions
**Check**: `_camelCase` for private fields, `PascalCase` for properties/methods/classes.
**Note**: Legacy code may use `m_` prefix -- don't flag existing `m_` fields but use `_` for new code.

### 12a. No Publish-Number Prefixes in Symbols
**Check**: Do not introduce or keep symbols whose names start with `PublishXX`, `PubXX`, or similar publish-number prefixes (for example `Publish30PoisonCloudMaxDamage`, `Pub96RequiredTactics`). This applies to functions, variables, constants, fields, properties, helper classes, and test helpers.
**Good**: Name the domain mechanic (`PoisonCloudMaxDamage`, `PrimaryTacticsRequirement`) and keep publish/source evidence in comments, PR bodies, docs, source-reference strings, or test data notes.
**Why**: Publish numbers are evidence, not stable domain names. Baking them into runtime/test symbols makes later era/source reconciliation harder.
**See**: `modernuo-no-publish-prefix-names` for the detailed naming rule and replacement pattern.

### 13. No Empty Gumps
**Check**: Any gump (legacy `Gump` constructor, or `BuildLayout`) must not have a code path that produces zero visual elements (no `AddBackground`, no `AddPage` with content, etc.).
**Why**: The client has no way to close an empty gump — no close button, no right-click dismiss. This leaks a gump slot on both client and server until relog.
**Common cause**: Early `return` in a constructor or `BuildLayout` when prerequisites aren't met.
**Fix**: Use a static `DisplayTo(Mobile from)` method that validates prerequisites **before** constructing the gump. Make the constructor `private`. See `Projects/UOContent/Gumps/Go/GoGump.cs` for the canonical pattern.

### 14. PropertyList String Literals Must Be Holes
**Check**: In any `IPropertyList.Add()` interpolated string, string constants must be wrapped as holes `{"text"}`, not bare literals.
**Bad**: `list.Add(1060658, $"Chances\t{_charges}");` — "Chances" becomes a delimiter, not an argument.
**Good**: `list.Add(1060658, $"{"Chances"}\t{_charges}");` — "Chances" is an argument.
**Why**: The handler treats bare text as delimiters and `{}` contents as arguments. The property list system is used beyond the game client (e.g., web rendering) which must distinguish arguments from delimiters. Only `\t` should be a bare literal.
**Also**: If you don't know the text for a cliloc number, see `Projects/Server/Localization/Localization.cs` `LoadClilocs()` to learn the binary format, and ask the user where their `cliloc.enu` file is.

### 15. Braces Required on All Control Flow
**Check**: ALL `if`, `else`, `for`, `foreach`, `while`, `do`, `switch` statements must have braces, even for single-line bodies.
**Bad**:
```csharp
if (condition)
    DoSomething();
```
**Good**:
```csharp
if (condition)
{
    DoSomething();
}
```
**Why**: Reduces merge conflicts and diff sizes.

### 16. Prefer Switch Expressions and Switch-When Patterns
**Check**: Where a chain of `if`/`else if` maps inputs to outputs, prefer a switch expression. Where pattern matching with guards improves clarity, prefer `switch`-`when`.
**Bad**:
```csharp
if (type == GemType.StarSapphire) return "star sapphire";
else if (type == GemType.Emerald) return "emerald";
else return "gem";
```
**Good**:
```csharp
return type switch
{
    GemType.StarSapphire => "star sapphire",
    GemType.Emerald      => "emerald",
    _                    => "gem"
};
```
**Why**: Switch expressions enable JIT/PGO optimization and improve readability.
**Exception**: Skip if the switch would be unreadable or the code is on a cold path.

### 17. Interpolation Anti-Patterns (handler-aware APIs)

**Context**: Many ModernUO APIs accept `ref RawInterpolatedStringHandler` (`Mobile.SendMessage`/`Say`/`Emote`/etc., `Item.Public/Local/NonlocalOverheadMessage`/`SendLocalizedMessageTo`/`SendMessageTo`, `IPropertyList.Add`, `SpanWriter.WriteAscii`/`WriteLatin1`, gump `AddLabel`/`AddHtml`/`AddHtmlLocalized`, `Html.Center`/`Color`/`Right`). The handler overload renders the interpolation directly into a pooled buffer with **zero `string` allocation** — but only when the call-site argument is a `$"..."` literal directly in the parameter slot.

**Check**: Flag any of the following patterns when the call target is one of those handler-aware APIs. The handler overload is silently bypassed and a `string` is allocated per call.

| Pattern | Fix |
|---|---|
| `Send(cond ? $"a" : $"b")` | `if/else` with two calls |
| `Send(thing switch { 1 => $"a", _ => $"b" })` | `switch` statement, call per arm |
| `var s = $"foo {x}"; Send(s);` (single-use) | Inline at call site |
| `Send($"x {value.ToString()}")` | Drop `.ToString()` — handler formats directly |
| `Send($"x {td.String()}")` | Drop `.String()` — pass `td` directly |
| `Send($"x {a + b}")` (string concat) | Multiple holes: `Send($"x {a}{b}")` |
| `Send(string.Format("x {0}", v))` | `Send($"x {v}")` |
| `Send($"x {items.Aggregate(...)}")` | Build via `ValueStringBuilder`, pass span |

**For lowercase output**, use the `:L` format specifier instead of `value.ToString().ToLowerInvariant()`:
```csharp
mob.SendMessage($"You earned a {rank:L} trophy!");          // "gold" not "Gold"
```

**Why**: These methods are called constantly during gameplay (every chat line, every system message, every gump label, every tooltip). The handler overload exists specifically to eliminate per-call `string` allocation. Each anti-pattern leaks one or more strings per call.

**Severity**: WARNING. Flag and ask before fixing — some patterns (e.g., reused locals across multiple call sites) are intentional and shouldn't be inlined.

**See**: `dev-docs/string-handling.md` § "Interpolation Anti-Patterns" for the full reference with detailed before/after examples.

## Severity Levels
- **ERROR**: Rules 3, 9, 10, 13 (will cause bugs, build failures, or client-side leaks)
- **WARNING**: Rules 1 (Tier 3 LINQ), 2, 4, 5, 6, 7, 8, 12, 12a, 14, 15, 17 (performance/convention issues)
- **INFO**: Rules 1 (Tier 2 LINQ on warm paths — note it but don't flag as violation), 16 (switch patterns — suggest but don't flag)
- **ASK**: Rule 11 (need user input)

## How to Report Issues
When you find violations, report them as:
```
[AUDIT] {SEVERITY}: {Description}
  File: {path}:{line}
  Suggestion: {fix}
```

Do NOT silently fix issues. Always report findings first; ask before fixing unless the task explicitly requested fixes.

## See Also
- `dev-docs/code-standards.md` - Full coding standards documentation
- `plugins/modernuo/skills/modernuo-serialization/SKILL.md` - Serialization rules
- `plugins/modernuo/skills/modernuo-timers/SKILL.md` - Timer cleanup rules
- `plugins/modernuo/skills/modernuo-lifecycle-cleanup/SKILL.md` - Deletion, ownership, timer, event, and region cleanup doctrine
- `plugins/modernuo/skills/modernuo-threading/SKILL.md` - Threading model details
- `plugins/modernuo/skills/modernuo-performance-hot-paths/SKILL.md` - Hot/warm/cold path classification and performance decision matrix
- `plugins/modernuo/skills/modernuo-property-lists/SKILL.md` - PropertyList interpolation rules
- `plugins/modernuo/skills/modernuo-server-lifecycle/SKILL.md` - Startup and lifecycle phase risks
- `plugins/modernuo/skills/modernuo-pathfinding/SKILL.md` - AI movement and StepCache risks
- `plugins/modernuo/skills/modernuo-world-saves-archives/SKILL.md` - Save/archive/restore data-loss risks
