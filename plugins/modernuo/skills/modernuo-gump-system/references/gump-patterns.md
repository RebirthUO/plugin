# Gump Patterns

Verify exact method signatures against current local builders.

## Type selection

| Fixed/cached structure | Variable structure |
|---|---|
| `StaticGump<TSelf>` | `DynamicGump` |
| labels/HTML vary through placeholders | loops/conditional controls vary |
| `BuildLayout` + `BuildStrings` | `BuildLayout` per instance |

`Singleton => true` is appropriate when only one instance should exist per player. Do not set it automatically for workflows that intentionally compare or stack windows.

## Display and response shape

```csharp
public static void DisplayTo(Mobile from)
{
    if (from.NetState == null || !CanOpen(from))
    {
        return;
    }

    from.SendGump(new MyGump(from));
}

public override void OnResponse(NetState sender, in RelayInfo info)
{
    if (info.ButtonID == 0)
    {
        return;
    }

    // Revalidate sender/mobile, authorization, target state, IDs, and text.
}
```

Make the constructor private when all instances must pass `DisplayTo`. Layout builders commonly support pages, backgrounds, images/items, localized HTML, labels, buttons, checks/radios, text entries, tooltips, and no-close/no-move/no-resize modifiers.

## Strings

Direct interpolated literals can use handler-aware overloads:

```csharp
builder.AddLabel(20, 40, hue, $"You have {gold:N0} gold");
```

Avoid a prebuilt single-use string, `string.Format`, unnecessary `.ToString()`, or a ternary that returns interpolated strings when it bypasses the handler. Use verified cliloc IDs for localized UI.

## Verification matrix

- prerequisites fail before construction;
- every constructed layout has visual/dismissible content;
- button `0`, valid actions, unknown actions;
- malformed/oversized text and switches;
- actor/target moved, deleted, unauthorized, or changed after display;
- repeated open obeys singleton/stack policy;
- cached/static strings vary correctly between instances.
