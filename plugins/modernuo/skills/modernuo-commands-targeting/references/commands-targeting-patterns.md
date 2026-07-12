# Command and Targeting Patterns

Use after the main skill selects a command/target flow. Verify signatures against the current repository.

## Registration shape

```csharp
public static void Configure()
{
    CommandSystem.Register("MyCommand", AccessLevel.GameMaster, OnCommand);
}

[Usage("MyCommand <name>")]
[Description("Performs one specific staff action.")]
private static void OnCommand(CommandEventArgs e)
{
    if (e.Length != 1)
    {
        e.Mobile.SendMessage("Usage: [MyCommand <name>");
        return;
    }

    var name = e.GetString(0);
    // Validate all policy before mutation.
}
```

`CommandEventArgs` commonly exposes `Mobile`, `Command`, `ArgString`, `Arguments`, `Length`, and typed getters. Read the getters before deciding how invalid input is reported; several return defaults.

## Target shape

```csharp
private sealed class MyTarget : Target
{
    public MyTarget() : base(12, false, TargetFlags.None)
    {
    }

    protected override void OnTarget(Mobile from, object targeted)
    {
        if (targeted is not Item item || item.Deleted)
        {
            from.SendMessage("That is not a valid target.");
            return;
        }

        // Revalidate access, map, range, LOS, ownership, and mechanic policy.
    }
}
```

Use `TargetFlags.Harmful` or `Beneficial` when combat/notoriety semantics require it. Supported target objects commonly include `Mobile`, `Item`, `LandTarget`, and `StaticTarget`. Override range/LOS/not-accessible handlers only when a distinct response is useful.

## Verification matrix

Test:

- minimum access level and one level below;
- missing, extra, malformed, and boundary arguments;
- each allowed and disallowed target type;
- deleted, moved, different-map, out-of-range, and out-of-LOS targets;
- cancellation and repeated response;
- success side effects, logs, and rollback/no-partial-mutation on failure.
