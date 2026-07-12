---
name: migrate-timers
description: Use when converting RunUO Timer subclasses, DelayCall patterns, TimerPriority, or post-load timer restoration to ModernUO timer callbacks and TimerExecutionToken lifecycle. Do not use for wall-clock/calendar scheduling; use modernuo-event-scheduler.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, timers, lifecycle]
    related_skills:
      - migrate-foundation
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-serialization
      - modernuo-threading
      - modernuo-code-audit
---

# RunUO to ModernUO Timer Migration

## Boundary

Convert game-time delays and recurring callbacks. Calendar events such as “every Monday at 09:00” belong to [modernuo-event-scheduler](../modernuo-event-scheduler/SKILL.md).

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Inventory start sites, delay/interval/count, callback state, restart behavior, owner lifetime, cancellation, and persistence semantics.
2. Inspect the current local `Timer.StartTimer` or stateful `DelayCall` overload; choose the least-allocating pattern that preserves behavior.
3. Move nested `OnTick` logic to the owning type and replace timer objects with callbacks plus `TimerExecutionToken` only when cancellation is required.
4. Remove `TimerPriority`; do not invent a replacement.
5. Cancel tokens at every owner disable/delete boundary before callback state can be invalid, using the local base-call convention.
6. Keep tokens runtime-only. Persist durable progress/deadlines separately and restore the timer in the correct after-deserialization phase.
7. Test exact timing boundaries through deterministic seams, repeated start/cancel, deletion, save-load restoration, and callback idempotence.

## Safety gates

- Never serialize `TimerExecutionToken`.
- Do not start world-dependent timers inside the raw deserialize read.
- Avoid closure allocations on hot/repeating paths; use supported state parameters.
- Make cancellation and expiry safe when both race through adjacent lifecycle paths on the event loop.
- Preserve remaining-duration versus reset-on-load semantics explicitly.

## Verification/self-check

Exercise exact deterministic timing boundaries, repeated start/cancel, delete/disable, and save-load restoration. Re-scan for serialized tokens, orphan callbacks, closures on repeating hot paths, and calendar misuse.

## Output contract

Return the timer ownership matrix, converted callbacks/tokens, persistence/restoration policy, cleanup hooks, deterministic test evidence, and any real-time/manual timing check still required.

## Reference routing

- Read [modernuo-timers](../modernuo-timers/SKILL.md) for exact overloads and deterministic test seams.
- Read [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) when the owning hook is ambiguous.
- Read [modernuo-event-scheduler](../modernuo-event-scheduler/SKILL.md) only for wall-clock recurrence.
