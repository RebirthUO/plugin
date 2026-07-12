# Event Surfaces

Use this as a discovery map, then verify declarations and signatures in the current repository.

## Common EventSink groups

- Lifecycle: server started, shutdown, world load/save, post-snapshot.
- Connection/account: connected, before disconnected, disconnected, logout, account login, socket connect.
- Communication/UI: speech, paperdoll request.
- Combat/movement: aggressive action, movement.
- Failure: server crashed.

Payloads may expose mutable decisions such as accepted/reject reason, handled/blocked, movement blocked, connection allowed, or crash-close behavior. Update them only when the subscriber owns that policy.

## Generated events

```csharp
[GeneratedEvent(nameof(EntityChangedEvent))]
public static partial void EntityChangedEvent(Mobile mobile);

[OnEvent(nameof(OwnerType.EntityChangedEvent))]
private static void OnEntityChanged(Mobile mobile)
{
}
```

The generator owns discovery/wiring. Check the generated-event package and existing declarations for supported visibility, parameter variance, and naming.

## Pooled arguments

Some high-frequency EventArgs expose `Create(...)` and `Free()`. When invoking manually:

```csharp
var args = MovementEventArgs.Create(mobile, direction);
try
{
    EventSink.InvokeMovement(args);
}
finally
{
    args.Free();
}
```

Do not retain `args` or references into its pooled buffers after invocation.

## Verification matrix

- startup registers exactly once;
- the intended event fires at the intended semantic moment;
- irrelevant payloads are ignored;
- mutable handled/cancel fields work;
- disable/reload unsubscribes;
- handler exceptions do not leak pooled state;
- duplicate delivery does not duplicate irreversible side effects.
