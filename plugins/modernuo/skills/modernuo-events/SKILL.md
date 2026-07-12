---
name: modernuo-events
description: Use when subscribing to, handling, or defining ModernUO EventSink or generated events, including connection, speech, movement, combat, world, death, or deletion hooks. Covers event choice, signatures, lifetime, pooling, cleanup, and tests. Do not use for calendar schedules or short delayed callbacks.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, events, eventsink, lifecycle, hooks]
    related_skills:
      - modernuo-code-audit
      - modernuo-server-lifecycle
      - modernuo-configuration
      - modernuo-threading
      - modernuo-lifecycle-cleanup
      - modernuo-content-patterns
      - migrate-commands-events
---

# ModernUO Events

## Boundary

Own game/lifecycle event surfaces. Calendar recurrence belongs to [modernuo-event-scheduler](../modernuo-event-scheduler/SKILL.md); elapsed callbacks belong to timers. RunUO conversions use [migrate-commands-events](../migrate-commands-events/SKILL.md).

## Workflow

1. Define the producer, subscriber, exact semantic moment, payload, cancellation/handled behavior, lifetime, ordering, frequency, and failure policy.
2. Read [event-surfaces.md](references/event-surfaces.md), then inspect the actual local event declaration, invoker, and nearest subscriber. Never choose an event by name alone.
3. For process-lifetime static EventSink handlers, subscribe deterministically in `Configure()`. For instance, reloadable, temporary, or disableable systems, store ownership and unsubscribe.
4. Use `[OnEvent]` only for an existing/generated event contract; do not also add a manual EventSink subscription.
5. Match the exact signature, validate payload/entity state, honor handled/blocked semantics, and keep the handler bounded on the game loop.
6. If defining an event, prefer the repository's generated-event/pooling conventions and document invocation ownership and ordering.
7. Test registration once, event firing, filters, handled/cancel flow, disable/unsubscribe, deletion/stale payload, and repeated initialization.

## Safety gates

- Connection, disconnect, logout, death, deletion, world save, and shutdown are not interchangeable cleanup points.
- Do not retain pooled EventArgs or other borrowed payload state after the callback.
- If code creates pooled args manually, return them on every path, including exceptions.
- Event handlers must not block, start unsafe background game logic, or scan the full world without a bounded reason.
- Make side effects idempotent when an event can fire more than once.

## Verification/self-check

Prove registration count, semantic firing point, filters/handled behavior, pooled cleanup, disable/unsubscribe, and duplicate delivery. Re-read the actual declaration/invoker rather than relying on the event map.

## Output contract

Return selected event and semantic rationale, subscription/invocation changes, lifetime and cleanup owner, changed files, verification results, and ordering or coverage risks.

## Reference routing

- Always read [event-surfaces.md](references/event-surfaces.md).
- Read [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) for lifetime decisions and [modernuo-server-lifecycle](../modernuo-server-lifecycle/SKILL.md) for startup/shutdown ordering.
