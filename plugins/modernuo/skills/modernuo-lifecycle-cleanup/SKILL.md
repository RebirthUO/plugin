---
name: modernuo-lifecycle-cleanup
description: >
  Use when creating, modifying, or reviewing ModernUO object lifecycle cleanup,
  including OnDelete and OnAfterDelete, timer cancellation, event unsubscription,
  dynamic region unregister, owned Item/Mobile cleanup, dangling references,
  callbacks against deleted objects, and AfterDeserialization restoration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
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

## Purpose

Use this skill to protect long-running ModernUO shards from deleted-object access, dangling references, ghost regions, timer callbacks after deletion, event leaks, duplicate restoration after world load, and owned world objects that survive their controller.

This is the cleanup lens. For API details, route outward to `modernuo-timers`, `modernuo-events`, `modernuo-regions`, `modernuo-serialization`, and `modernuo-content-patterns`.

## When to Use

- Adding or changing `OnDelete()` or `OnAfterDelete()`.
- Adding timers, delayed callbacks, recurring effects, `TimerExecutionToken`, or `Timer` fields.
- Holding references to `Item`, `Mobile`, `BaseCreature`, `Region`, `Gump`, quest state, spawners, temporary effects, summons, or owned child objects.
- Registering dynamic regions or subscribing to events.
- Restoring transient state in `[AfterDeserialization]`.
- Reviewing deletion behavior for items, mobiles, systems, puzzles, bosses, quests, buffs, summons, arenas, regions, or world controllers.

## Key Rules

1. **Cancel active behavior before owner state becomes invalid.** Cancel `TimerExecutionToken` with `_token.Cancel()` and legacy `Timer` fields with `_timer?.Stop()`. If callbacks close over `this`, `Item`, `Mobile`, `Region`, or collections of world objects, they must tolerate deletion or be cancelled before deletion can make those references unsafe.

2. **Never serialize timer tokens.** `TimerExecutionToken` must not be `[SerializableField]`. Persist only the durable deadline/state, then recreate runtime timers in `[AfterDeserialization]` when the object is valid and the behavior should resume.

3. **Clean owned child world objects.** If a controller owns child items/mobiles/effects, delete or release them in the deletion path. After cascading deletion, clear fields or collections where stale references could be reused.

4. **Unregister dynamic regions.** Any item/controller that creates a `Region` must unregister it when deleted, moved to an invalid map, disabled, or recreated. Ghost regions can leave invisible travel, housing, spawn, or combat rules active.

5. **Handle events by lifetime.** Static process-lifetime systems subscribed in `Configure()` normally live until server shutdown and do not need per-instance unsubscribe. Temporary, instance-owned, reloadable, disableable, or deleted systems must unsubscribe with `-=` when disabled/deleted, and static handlers must not retain deleted objects accidentally.

6. **Distinguish `OnDelete()` from `OnAfterDelete()`.** Use `OnDelete()` for early cancellation of active behavior. Use `OnAfterDelete()` for cleanup that relies on the object being deleted or for cascading deletes/unregisters of owned external objects. Follow the class hierarchy's established base-call order; do not move `base.OnDelete()` or `base.OnAfterDelete()` blindly.

7. **Callbacks must validate targets.** Timer, event, gump, quest, region, and delayed callbacks should check the relevant validity before acting: `Deleted`, `target?.Deleted == false`, `Map != null`, `Map != Map.Internal`, `mobile.NetState != null` when connection matters, and owner still controls/owns the target.

8. **Restore transient registrations in `[AfterDeserialization]`.** Recreate timers, dynamic regions, caches, and transient links there, not by editing generated `Deserialize`. Use deferred `[AfterDeserialization(false)]` when restoration needs other world entities loaded or may call `Delete()`.

9. **Clear bidirectional references.** If object A points to B and B points back to A, deletion of either side must avoid leaving stale references. High-risk zones include spawners, quests, arenas, summons, controllers, buffs, temporary blockers, and region-owned effects.

10. **Test lifecycle transitions when behavior is non-trivial.** Prefer focused tests or smoke checks for: delete owner and child objects disappear; delete while timer pending; serialize/load restores exactly once; dynamic region unregister removes its rule; event unsubscribe prevents later callbacks.

Completion criterion: every new runtime resource has a matching cleanup/restoration story, and every cleanup review identifies ownership, lifetime, deletion hook, and validation evidence.

## Cleanup Matrix

| Resource | Create/Register | Cleanup | Restore After Load | Main Risk |
|---|---|---|---|---|
| `TimerExecutionToken` | `Timer.StartTimer(..., out _token)` | `_token.Cancel()` | `[AfterDeserialization]` if still active | callback touches deleted owner |
| `Timer` field | `Timer.DelayCall` / subclass `.Start()` | `_timer?.Stop(); _timer = null` | `[DeserializeTimerField]` or `[AfterDeserialization]` | duplicate/stale timer |
| Dynamic `Region` | `region.Register()` | `region.Unregister(); region = null` | deferred `[AfterDeserialization(false)]` if map/parent needed | ghost travel/housing/spawn rule |
| Owned `Item` | create/move to world | `item?.Delete(); item = null` | recreate or relink only if durable state says so | orphan item/economy leak |
| Owned `Mobile` | spawn/summon | `mobile?.Delete(); mobile = null` | recreate carefully, avoid duplicates | orphan creature/combat leak |
| Static `EventSink` hook | `Configure() += handler` | usually process lifetime | automatic on boot via `Configure()` | false-positive unsubscribe demands |
| Instance event hook | `+= handler` from object/system | `-= handler` on disable/delete | resubscribe once if durable | deleted object retained/called |
| Bidirectional ref | A sets B.Owner / B sets A.Child | clear both sides | relink by serials/loaded refs | stale pointer or resurrection |

## Patterns

### Early Timer Cancellation

```csharp
public override void OnDelete()
{
    _timerToken.Cancel();
    _timer?.Stop();
    _timer = null;

    base.OnDelete();
}
```

Use this when a pending callback could observe partially deleted state or keep work running after the owner starts deleting.

### Cascading Owned Object Cleanup

```csharp
public override void OnAfterDelete()
{
    base.OnAfterDelete();

    _platform?.Delete();
    _platform = null;

    _altar?.Delete();
    _altar = null;

    if (_children != null)
    {
        foreach (var child in _children)
        {
            child?.Delete();
        }

        _children.Clear();
    }
}
```

Use this when the deleted controller owns external world objects. Keep cascade ownership explicit: one owner should be responsible for deleting each child.

### Dynamic Region Cleanup

```csharp
private void ClearRegion()
{
    _region?.Unregister();
    _region = null;
}

public override void OnAfterDelete()
{
    ClearRegion();
    base.OnAfterDelete();
}
```

If the region also changes when the owner moves maps or location, unregister the old region before registering the replacement.

### Safe Delayed Callback

```csharp
private void FinishEffect(Mobile target)
{
    if (Deleted || target?.Deleted != false || Map == Map.Internal)
    {
        return;
    }

    // Apply effect only after validating owner and target.
}
```

Cancellation is better when ownership is clear; guards are still needed for targets that can be deleted independently.

### Event Subscription Lifetime

```csharp
public void Enable()
{
    EventSink.Speech += OnSpeech;
}

public void Disable()
{
    EventSink.Speech -= OnSpeech;
}
```

Use explicit unsubscribe for instance, temporary, disableable, or reloadable systems. Do not require this for normal static `Configure()` subscriptions that are intentionally server-lifetime.

## Hook Choice Guide

- Use `OnDelete()` for immediate stop/cancel behavior that must not run once deletion begins.
- Use `OnAfterDelete()` for owned world-object cascades, region unregister, and clearing external references after base deletion has completed.
- Use `[AfterDeserialization]` for runtime-only restoration from durable fields.
- Use `[AfterDeserialization(false)]` when restoration depends on other entities/regions/maps being loaded or may call `Delete()`.
- Inspect base implementations and neighboring classes before changing hook order. Existing hierarchies may rely on a specific base-call position.

## Anti-Patterns

- Adding a `TimerExecutionToken` field without a cancellation path.
- Marking a token or runtime-only handle with `[SerializableField]`.
- Timer callback captures `this` or a target without `Deleted`/null guards.
- Dynamic region is registered but never unregistered.
- Instance-owned `EventSink` subscription is never unsubscribed.
- Child items/mobiles are deleted but collections still hold stale references reused later.
- `[AfterDeserialization]` restarts duplicate timers or registers duplicate regions.
- Cleanup assumes child refs are non-null or not already deleted.
- Treating static `Configure()` event subscriptions and temporary instance subscriptions as the same lifetime.
- Moving `base.OnDelete()` / `base.OnAfterDelete()` order without checking the hierarchy.

## Real Examples

- `Projects/UOContent/Engines/Doom/LeverPuzzle/LeverPuzzleController.cs` — `OnDelete()` calls `KillTimers()`, while `OnAfterDelete()` removes owned puzzle items and unregisters regions.
- `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs` — `OnAfterDelete()` deletes owned platform, altar, idol, and skull collections.
- `Projects/UOContent/Engines/BuffIcons/BuffInfo.cs` — `TimerExecutionToken` with `StartTimer()` and `StopTimer()` shows a small runtime-token lifecycle.
- `Projects/UOContent/Engines/CannedEvil/ChampionAltar.cs` and `ChampionPlatform.cs` — use deferred `[AfterDeserialization(false)]` patterns around world-linked champion objects.

Examples are pattern evidence, not proof that every local detail is universally correct. Follow the owning class hierarchy and current repo conventions.

## Review Checklist

- [ ] Ownership is explicit: who owns each timer, event subscription, region, child item/mobile, and reference?
- [ ] Every timer/token has cancellation or a proven process-lifetime reason not to.
- [ ] Runtime-only handles are not serialized.
- [ ] Timer/event callbacks validate owner and target liveness.
- [ ] Dynamic regions unregister on delete/disable/recreate/map change.
- [ ] Owned child world objects are deleted/released once and refs/collections are cleared when needed.
- [ ] `[AfterDeserialization]` restores transient state exactly once and only when valid.
- [ ] Event subscriptions match their lifetime: static process-lifetime vs instance/temporary/disableable.
- [ ] Base-call order was checked against neighboring classes before changes.
- [ ] Focused lifecycle test or smoke check exists for non-trivial behavior.

## How to Report Issues

```text
[LIFECYCLE] {severity}: {cleanup issue}
  File: {path}:{line}
  Owner: {item/mobile/system}
  Resource: {timer/event/region/child object/reference}
  Risk: {deleted callback, leak, ghost region, save/load drift, stale ref}
  Suggested check: {delete owner, pending timer, serialize/load, region unregister, targeted test}
```

Severity guide:

- `ERROR`: timer/event callback can touch deleted object; serialized timer token; dynamic region leak; owned world object leak; save/load duplicate registration.
- `WARN`: unclear ownership; missing null/deleted guard; cleanup depends on undocumented order; stale ref likely but not proven.
- `INFO`: test, documentation, or readability improvement.

## See Also

- `plugins/modernuo/skills/modernuo-code-audit/SKILL.md` — pre-submit lifecycle audit entry point.
- `plugins/modernuo/skills/modernuo-content-patterns/SKILL.md` — item/mobile/content templates and ownership patterns.
- `plugins/modernuo/skills/modernuo-timers/SKILL.md` — timer APIs, tokens, and deserialization patterns.
- `plugins/modernuo/skills/modernuo-events/SKILL.md` — `EventSink` and generated event patterns.
- `plugins/modernuo/skills/modernuo-regions/SKILL.md` — dynamic region register/unregister behavior.
- `plugins/modernuo/skills/modernuo-serialization/SKILL.md` — generated serialization and `[AfterDeserialization]` rules.
- `dev-docs/content-patterns.md`, `dev-docs/timers.md`, `dev-docs/events.md`, `dev-docs/regions.md`, `dev-docs/serialization.md`.
