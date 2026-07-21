---
name: modernuo-timers
description: >
  Use when implementing ModernUO delayed, recurring, cancellable, decay, expiry,
  or awaitable time-based behavior with Timer.StartTimer, Timer.DelayCall,
  TimerExecutionToken, or Timer.Pause. Use modernuo-event-scheduler for calendar
  events and modernuo-lifecycle-cleanup for broader ownership cleanup.
license: MIT
metadata:
  version: "1.2.0"
---

# ModernUO Timers and Scheduling

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Use the timer wheel for game-loop delays and recurrence. Use the event scheduler
for wall-clock calendars such as daily resets, weekly events, and holidays.

## Workflow

1. Inspect the consuming repository's pinned ModernUO revision, timer API
   overloads, nearby ownership pattern, serialization schema, and focused tests.
   Treat current repository code as implementation evidence, not official UO
   gameplay authority.
2. Define the first delay, interval/count, cancellation owner, durable deadline
   or state, restart policy, target validity, and whether timing is relative or
   calendar based. Ask for the missing behavior decision before implementation.
3. Choose the smallest API that satisfies the contract:
   - use pooled `Timer.StartTimer` for callback-only work;
   - request `out TimerExecutionToken` when later cancellation or observation is
     required;
   - use `Timer.DelayCall` for a `Timer` object, a custom timer, or state-parameter
     overloads that avoid closure allocation on measured hot paths;
   - use `Timer.Pause` only inside an async flow that owns failure and lifetime.
4. Make start, restart, and stop idempotent. Store one runtime handle per owner,
   cancel before replacement, and make the callback reject deleted, disabled,
   stale, or otherwise invalid owners and targets before causing effects.
5. Persist the gameplay deadline or state, never `TimerExecutionToken`. Restore
   active behavior exactly once after deserialization; execute, expire, or skip
   an elapsed deadline according to the explicit gameplay contract.
6. Cancel in the lifecycle hook supported by the actual class hierarchy and
   clear retained references. Do not assume callback validation replaces cleanup.
7. Add or update focused tests for schedule rounding, first fire, interval/count,
   cancel-before-fire, repeated cancel/restart, owner and target deletion,
   callback failure isolation, and save/load expiry when applicable.

## Guardrails

- `TimerExecutionToken` is runtime-only and must never be `[SerializableField]`.
- Treat timer mutation as game-loop-owned. Do not start, stop, or cancel timers
  from `Serialize()`, during world save, or from arbitrary worker threads.
- Timers have about 8 ms minimum wheel precision and delays round to scheduler
  ticks; do not promise sub-tick timing.
- `Thread.Sleep()` blocks the game loop. Use a timer or `await Timer.Pause(...)`.
- Repeating fire-and-forget work without an owner/cancellation story is a leak
  risk.
- Do not swallow callback exceptions or assume an async callback is observed;
  follow the repository's current event-loop error-handling pattern.
- Do not start duplicate timers from both construction and deserialization.
- Use `[DeserializeTimerField]` only for supported serialized `Timer` fields;
  token-based behavior restores from durable deadlines in an after-load hook.

## Output Contract

Return:

- repository revision and inspected timer/source/test paths;
- relative-versus-calendar decision and chosen API/overload;
- first delay, interval/count, precision assumption, owner, runtime handle, and
  cancellation hook;
- persisted deadline/state, exactly-once restoration, and elapsed-deadline rule;
- callback target guards, failure behavior, and retained-reference cleanup;
- changed files plus focused test commands and observed results.

For advice-only or review requests, make no edits and identify duplicate,
orphaned, off-thread, precision-sensitive, exception-prone, or non-restorable
timer risk. Mark unverified claims and unavailable tests explicitly.

## Verification

- Timing/count and cancel idempotence match the contract.
- Delete/disable prevents future effects and clears retained targets.
- Save/load restores at most one timer and handles elapsed deadlines.
- Focused timer/lifecycle tests pass; precision assumptions are documented.
- Every implementation claim names inspected repository evidence; every
  official gameplay claim routes through `uo-official-evidence`.

## Reference Routing

- Read `dev-docs/timers.md` and the current `Timer.StartTimer`/`DelayCall` overloads
  plus `TimerExecutionToken`, timer-wheel, and timer-test sources when selecting
  an API or asserting precision and lifecycle behavior.
- Load `modernuo-event-scheduler` for calendar semantics,
  `modernuo-serialization` for persistence, `modernuo-lifecycle-cleanup` for hook
  choice, and `modernuo-threading` for context ownership.
