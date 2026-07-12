# Property-List Formatting and Ordering

Read this reference when a tooltip needs cliloc arguments, a specific relative
position, or a testable recording representation.

## Normal append versus name-property insertion

Normal tooltip additions belong in `GetProperties()` after the base call:

```csharp
public override void GetProperties(IPropertyList list)
{
    base.GetProperties(list);
    list.Add(1060741, $"{_charges}");
}
```

`Item.GetProperties()` calls `AddNameProperties()` for name, loot flags, quest
state, and weight. If a source requires a custom entry immediately after that
block rather than at the end, use:

```csharp
public override void AddNameProperties(IPropertyList list)
{
    base.AddNameProperties(list);

    if (Core.HS)
    {
        list.Add(1150058);
    }
}
```

Record entry numbers in a focused test and assert the custom cliloc relative to
weight and later equipment properties. Test both sides of an era gate.

## Argument separators

Cliloc placeholders receive tab-separated arguments:

```csharp
list.Add(1060637, $"{current}\t{maximum}");
list.Add(1072241, $"{items}\t{maxItems}\t{weight}\t{maxWeight}");
```

The `IPropertyList` interpolation handler treats bare literal text as delimiter
metadata. Human text must be a hole; normally only `\t` is bare:

```csharp
// Wrong: "Charges" is parsed as a literal delimiter.
list.Add(1060658, $"Charges\t{_charges}");

// Correct: both values are arguments.
list.Add(1060658, $"{"Charges"}\t{_charges}");
```

This rule is specific to property lists. Normal message and gump handlers should
keep ordinary text as interpolation literals.

## Values and cliloc references

Pass values directly so the handler can format into its buffer:

```csharp
list.Add(1060658, $"{"Charges"}\t{_charges}");
```

Avoid `_charges.ToString()`, `string.Format`, concatenation, pre-built locals,
ternary/switch interpolated branches, or LINQ aggregation in the hole.

When an argument is itself a cliloc, mark it as localized data:

```csharp
list.Add(1050039, $"{amount}\t{1060000:#}");
// Or use the applicable AddLocalized overload.
```

A string such as `"#1060000"` is raw text and can render literally in alternate
consumers.

## Refresh behavior

Generated fields that change the tooltip can use:

```csharp
[SerializableField(0)]
[InvalidateProperties]
[SerializedCommandProperty(AccessLevel.GameMaster)]
private int _charges;
```

Custom setters/non-serialized state must call `InvalidateProperties()` when the
visible value changes. Custom persistent setters also call `this.MarkDirty()`.
Do not invalidate repeatedly when no visible state changed.

## Useful source anchors

- `Projects/Server/PropertyList/IPropertyList.cs`
- `Projects/Server/PropertyList/ObjectPropertyList.cs`
- `Projects/Server/Items/Item.cs`
- `Projects/Server/Items/Container.cs`

Use the current interfaces rather than a copied overload list; private recording
test doubles can lag interface additions. See
`recording-property-list-test-doubles.md` when that occurs.
