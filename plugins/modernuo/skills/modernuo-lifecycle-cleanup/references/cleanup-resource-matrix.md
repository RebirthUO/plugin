# Lifecycle Cleanup Resource Matrix

Read this reference when a ModernUO object owns more than one runtime resource or
when `OnDelete()` versus `OnAfterDelete()` is unclear.

## Resource matrix

| Resource | Create/register | Cleanup | Restore | Main risk |
|---|---|---|---|---|
| `TimerExecutionToken` | `Timer.StartTimer(..., out token)` | `token.Cancel()` | Restart from durable state in an after-load hook | Callback touches deleted owner |
| Legacy `Timer` | `DelayCall`, subclass, `Start()` | `Stop()`, then clear the field | `[DeserializeTimerField]` or after-load hook | Duplicate/stale timer |
| Dynamic `Region` | construct and `Register()` | `Unregister()`, then clear | Usually deferred until map/parent exists | Ghost travel/housing/spawn rule |
| Owned `Item` | create/move to world | owning controller calls `Delete()` once | Recreate/relink only from durable state | Orphan/economy leak |
| Owned `Mobile` | spawn/summon | owning controller calls `Delete()` once | Recreate carefully; prevent duplicates | Orphan/combat leak |
| Static process hook | `Configure()` subscription | normally none until process exit | boot calls `Configure()` | False-positive cleanup demands |
| Instance event hook | object/system `+=` | matching `-=` on disable/delete | resubscribe once if durable | Deleted object retained/called |
| Bidirectional reference | A points to B and B to A | clear both sides | relink loaded entities safely | Stale pointer/resurrection |

## Hook selection

- `OnDelete()`: stop behavior that must not run once deletion begins. Typical:
  tokens, timers, active effects, work that closes over the owner.
- `OnAfterDelete()`: cascade owned external entities, unregister regions, and
  clear references when the hierarchy expects the object to be fully deleted.
- `[AfterDeserialization]`: restore runtime state derived only from this entity.
- `[AfterDeserialization(false)]`: wait for the full world when other entities,
  regions, deletion, or world-facing registration are involved.

Always inspect the base implementation and neighboring types before moving the
base call. Hook order is a class-hierarchy contract, not a universal style rule.

## Safe patterns

```csharp
public override void OnDelete()
{
    _token.Cancel();
    _timer?.Stop();
    _timer = null;
    base.OnDelete();
}
```

```csharp
private void ClearRegion()
{
    _region?.Unregister();
    _region = null;
}

public override void OnAfterDelete()
{
    ClearRegion();
    _child?.Delete();
    _child = null;
    base.OnAfterDelete();
}
```

Delayed callbacks should validate every independently mutable participant:

```csharp
if (Deleted || target?.Deleted != false || Map == null || Map == Map.Internal)
{
    return;
}
```

Add connection, range, ownership, or alive checks only when the callback depends
on them. Cancellation is preferred for owned work, but it cannot prevent a target
from being deleted independently.

## High-risk examples to inspect

- `Projects/UOContent/Engines/Doom/LeverPuzzle/LeverPuzzleController.cs` for timer,
  owned-item, and region cleanup split across deletion hooks.
- `Projects/UOContent/Engines/CannedEvil/ChampionSpawn.cs` for controller-owned
  altar/platform/idol/skull cleanup.
- `Projects/UOContent/Engines/BuffIcons/BuffInfo.cs` for a small token lifecycle.
- Champion altar/platform implementations for deferred cross-world restoration.

Examples are evidence for the pattern, not permission to copy their base-call
order into an unrelated hierarchy.
