---
name: modernuo-timers
description: >
  Use when implementing ModernUO delayed, recurring, cancellable, decay, expiry,
  or awaitable time-based behavior with Timer.StartTimer, Timer.DelayCall,
  TimerExecutionToken, or Timer.Pause. Use modernuo-event-scheduler for calendar
  events and modernuo-lifecycle-cleanup for broader ownership cleanup.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, timers, scheduling, lifecycle, serialization]
    related_skills:
      - modernuo-code-audit
      - modernuo-serialization
      - modernuo-lifecycle-cleanup
      - modernuo-threading
      - modernuo-content-patterns
      - modernuo-event-scheduler
      - modernuo-test-workflow
      - migrate-timers
---

# ModernUO Timers and Scheduling

## Boundary

Use the timer wheel for game-loop delays and recurrence. Use the event scheduler
for wall-clock calendars such as daily resets, weekly events, and holidays.

## Workflow

1. Define the first delay, interval/count, cancellation owner, durable state,
   restart policy, target validity, and whether timing is relative or calendar
   based.
2. Prefer `Timer.StartTimer(..., out TimerExecutionToken)` when later cancellation
   is required; omit the token only for genuinely fire-and-forget work.
3. Use `Timer.DelayCall` when an actual `Timer` object or state-parameter overload
   is needed; state parameters can avoid closure allocation on hot paths.
4. Store deadlines/expiry state, not tokens. Restore active behavior once after
   load and handle already-expired state explicitly.
5. Cancel the owned timer in the lifecycle hook chosen from the class hierarchy;
   callbacks must still validate independently deletable targets.
6. Test first fire, repetition/count, cancellation before fire, owner deletion,
   target deletion, and save/load/expiry as applicable.

## Guardrails

- `TimerExecutionToken` is runtime-only and must never be `[SerializableField]`.
- Timer APIs are game-thread-only. Do not start/stop/cancel timers from
  `Serialize()` or arbitrary worker threads.
- Timers have about 8 ms minimum wheel precision and delays round to scheduler
  ticks; do not promise sub-tick timing.
- `Thread.Sleep()` blocks the game loop. Use a timer or `await Timer.Pause(...)`.
- Repeating fire-and-forget work without an owner/cancellation story is a leak
  risk.
- Do not start duplicate timers from both construction and deserialization.
- Use `[DeserializeTimerField]` only for supported serialized `Timer` fields;
  token-based behavior restores from durable deadlines in an after-load hook.

## Output Contract

Return the chosen API, schedule, owner, cancellation hook, persisted deadline/
state, restoration behavior, callback guards, and test evidence. For reviews,
identify duplicate, orphaned, off-thread, or non-restorable timer risk.

## Verification

- Timing/count and cancel idempotence match the contract.
- Delete/disable prevents future effects and clears retained targets.
- Save/load restores at most one timer and handles elapsed deadlines.
- Focused timer/lifecycle tests pass; precision assumptions are documented.

## Reference Routing

- Read `dev-docs/timers.md` and the current `Timer.StartTimer`/`DelayCall` overloads
  when selecting an API.
- Load `modernuo-event-scheduler` for calendar semantics,
  `modernuo-serialization` for persistence, `modernuo-lifecycle-cleanup` for hook
  choice, and `modernuo-threading` for context ownership.
