---
name: modernuo-lifecycle-cleanup
description: >
  Use when implementing or reviewing ModernUO object-lifetime cleanup for timers,
  event subscriptions, dynamic regions, owned entities, callbacks, and restored
  runtime state. Do not use for timer API choice alone or server startup/shutdown;
  route those to modernuo-timers or modernuo-server-lifecycle.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, lifecycle, cleanup, deletion, timers, references]
    related_skills:
      - modernuo-code-audit
      - modernuo-content-patterns
      - modernuo-timers
      - modernuo-events
      - modernuo-regions
      - modernuo-serialization
      - modernuo-threading
      - modernuo-test-workflow
---

# ModernUO Lifecycle Cleanup

## Boundary

Own the lifetime match between an item, mobile, or system and every runtime
resource it creates or retains. The result must prevent callbacks against
deleted objects, ghost regions, event leaks, orphaned children, stale reverse
references, and duplicate restoration after world load.

## Workflow

1. Inventory each timer/token, event hook, region, owned entity, cache, and
   forward/reverse reference. Name its owner and intended lifetime.
2. Inspect base and neighboring implementations before choosing `OnDelete()`,
   `OnAfterDelete()`, or their base-call position.
3. Stop active behavior, unregister external state, delete or release owned
   objects once, and clear reusable references or collections.
4. Make delayed callbacks validate owner, target, map, connection, and ownership
   conditions that can change independently.
5. Persist only durable state. Recreate runtime-only state once in
   `[AfterDeserialization]`; use `[AfterDeserialization(false)]` when other
   entities must be loaded or the hook may mutate world state.
6. Exercise deletion, pending-callback, and save/load transitions appropriate to
   the change.

## Guardrails

- Cancel `TimerExecutionToken` with `Cancel()` and legacy `Timer` objects with
  `Stop()`. Never mark a token `[SerializableField]`.
- Prefer early cancellation in `OnDelete()` when a callback could observe
  partially deleted state. Use `OnAfterDelete()` for owned-object cascades,
  region unregister, and external-reference cleanup when the hierarchy expects
  deletion to have completed.
- Unregister dynamic regions before delete/disable/replacement; unsubscribe
  temporary instance events while leaving intentional process hooks intact.
- Clear both sides of relationships, give each child one deletion owner, and
  validate independently mutable callback targets even after cancellation.

## Output Contract

For implementation, return the changed paths plus an ownership table naming the
resource, owner, cleanup hook, restoration hook, and verification. For review,
report findings as:

```text
[LIFECYCLE] {ERROR|WARN|INFO}: {issue}
  File: {path}:{line}
  Resource/owner: {resource} / {owner}
  Risk: {deleted callback|leak|ghost region|duplicate restore|stale reference}
  Check: {focused test or smoke transition}
```

## Verification

- Delete the owner while delayed work is pending; no callback acts afterward.
- Owned entities and dynamic regions disappear exactly once.
- Save/load restores active runtime state once and never serializes tokens.
- Event and reverse-reference cleanup prevents later retention or invocation.

## Reference Routing

- Read [cleanup resource matrix and hook patterns](references/cleanup-resource-matrix.md)
  when selecting hooks or reviewing mixed resource ownership.
- Load `modernuo-timers`, `modernuo-events`, `modernuo-regions`, or
  `modernuo-serialization` only for the corresponding API details.
- Read `dev-docs/content-patterns.md` and the matching timer/event/region/
  serialization developer doc when repository behavior is uncertain.
