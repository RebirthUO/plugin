---
name: modernuo-event-scheduler
description: Use when implementing or reviewing wall-clock/calendar scheduling such as daily resets, weekly activities, seasonal windows, or maintenance. Covers recurrence selection, time zones, DST/restart policy, ownership, cancellation, and tests. Do not use for short game-time delays or sub-second ticks; use modernuo-timers.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, event-scheduler, calendar, seasonal-events, scheduling]
    related_skills:
      - modernuo-timers
      - modernuo-code-audit
      - modernuo-threading
      - modernuo-content-patterns
      - modernuo-test-workflow
---

# ModernUO Event Scheduler

## Boundary

Use EventScheduler for civil/calendar time (“Monday at 09:00”, annual seasonal window). Use [modernuo-timers](../modernuo-timers/SKILL.md) for elapsed game time (“five seconds later”), combat ticks, and sub-second work.

## Workflow

1. Define the civil schedule, named time zone, recurrence/window, first-run, missed-run/catch-up, duplicate-run, disable, restart, and operator override policy.
2. Read [schedule-patterns.md](references/schedule-patterns.md) and inspect the current local scheduler/recurrence APIs plus an existing event of the same lifetime.
3. Choose the simplest recurrence that exactly expresses the requirement. Use a callback event for a simple static action and a custom event class only when state/behavior warrants it.
4. Store and cancel the returned event according to its owner. Make registration idempotent across reload/enable paths.
5. Make `OnEvent` fast and safe on the game loop; queue/batch bounded work through repository-supported mechanisms rather than blocking.
6. Test schedule calculation around time-zone conversion, DST gaps/overlaps, month/year/leap boundaries, restart/missed runs, duplicate initialization, cancellation, and disabled state.

## Safety gates

- Never rely on the host's implicit local time zone; use an explicit reviewed `TimeZoneInfo`.
- Decide whether a seasonal end is inclusive/exclusive and how invalid month-days behave.
- Calendar scheduling has coarse granularity and is not a combat timer.
- Do not issue duplicate rewards, resets, or spawns after restart; define idempotency keys/state when side effects are not naturally idempotent.
- Persist durable progress separately when a restart must not reset event state.

## Verification/self-check

Calculate next occurrences across DST/month/year/leap/restart boundaries, verify duplicate registration and cancellation, and test idempotent side effects without sleeping on wall-clock time.

## Output contract

Return the schedule specification (zone, recurrence, window, catch-up/idempotency), owner/cancellation path, changed files, deterministic verification evidence, and remaining environment/manual clock checks.

## Reference routing

- Always read [schedule-patterns.md](references/schedule-patterns.md).
- Read [modernuo-timers](../modernuo-timers/SKILL.md) if the requirement mixes calendar activation with elapsed in-event delays.
- Read [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) when ownership/disable cleanup is ambiguous.
