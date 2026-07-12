# ModernUO Audit Rules

Read this reference for every code audit. Apply rules to the actual local APIs and call frequency; nearby repository precedent outranks remembered examples.

## Correctness and lifecycle

- A type using `[SerializationGenerator]` is `partial`, uses stable field indices, and has the required migration schema/version path. `TimerExecutionToken`, caches, and live handles are not serialized.
- Persistent custom setters call `MarkDirty()`; visible property changes invalidate properties where required.
- Timers, temporary event subscriptions, owned entities, regions, and held `Item`/`Mobile` references have an explicit owner and deterministic cleanup. Check all boundaries named by the behavior; one deletion hook is not automatically sufficient.
- Process-lifetime static EventSink subscriptions belong in deterministic startup. Reloadable/disableable subscriptions must unsubscribe.
- Player-controlled commands, targets, gump responses, packet data, and indices revalidate access, ownership, range, object state, and input bounds at execution time.

## Event-loop and performance

- Game logic stays on the single-threaded event loop. Flag new `Task.Run`, manual threads, thread-pool work, locks, volatile fields, or concurrent collections unless the file is verified infrastructure with a real cross-thread contract.
- Use structured `LogFactory` logging instead of `Console.Write*`.
- Avoid `World.Items` or `World.Mobiles` scans when a map/sector query can bound the work.
- Classify the path before judging allocation. On hot paths, reject unmeasured allocating LINQ chains and repeated `new List<T>`; prefer local loops and `PooledRefList<T>`. Use `STArrayPool<T>` for event-loop buffers and return rentals in `finally`. Do not mechanically rewrite cold paths.
- Keep blocking I/O, network waits, and expensive parsing out of event handlers and timer callbacks.

## Strings, properties, and UI

- For handler-aware message, gump, packet, and property APIs, a direct interpolated literal reaches the allocation-free overload. A prebuilt string, ternary/switch expression returning strings, `string.Format`, concatenation inside a hole, or unnecessary `.ToString()` may bypass it; flag only meaningful call sites.
- In `IPropertyList.Add` interpolation, literal argument text belongs in holes and only delimiters such as `\t` remain literal. Do not apply this property-list rule to normal messages or gump HTML.
- Never invent cliloc IDs; verify exact client text when the ID is part of behavior.
- A gump must always contain dismissible visual content. Validate prerequisites before construction, preferably through `DisplayTo`, and revalidate stale responses. Button ID `0` is close/cancel.

## Style and domain discipline

- New private fields use `_camelCase`; existing legacy `m_` fields are not renamed without another reason.
- Control-flow bodies use braces. Prefer clear switch/pattern matching only when it improves the local code.
- Do not encode publish numbers in runtime/test symbol names (for example, `Publish96...`); name the mechanic and keep publish evidence in docs/comments/test data.
- Do not assume an era. Any `Core.*`, expansion folder, formula, loot, combat, crafting, or property behavior must identify its target era/profile.
- Do not treat a compile-successful change as behavior-complete. Require focused tests for the player/server-visible outcome, persistence, lifecycle, and edge cases that changed.

## Severity guidance

- **P0/P1:** data loss, save incompatibility without migration, exploit/security, crash, severe client leak/lock, or destructive side effect.
- **P2:** behavior bug, stale authorization, timer/reference leak, era leakage, incorrect persistence, or significant hot-path regression.
- **P3:** concrete convention or maintainability defect unlikely to break current behavior.
- Ask for a target-era/policy decision instead of guessing; an unanswered design choice is not itself a code defect.
