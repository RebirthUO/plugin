# Property-List Formatting and Ordering

Read this reference when choosing a property-list overload, localized argument
shape, relative position, text-block mechanism, or refresh path. Confirm every
API against the consuming repository's pinned revision.

## Select the Emission Path

Normal additions usually follow the verified base call in `GetProperties`:

```csharp
public override void GetProperties(IPropertyList list)
{
    base.GetProperties(list);
    list.Add(1060741, $"{charges}");
}
```

Use a name-stage override only when the current base sequence proves the entry
must appear there. Call its base implementation first, then assert the custom
entry's relative position in a focused test. Do not infer a hook name or order
from an older source tree.

## Construct Arguments

In the specialized `IPropertyList` interpolated handler, literal text is
structural delimiter metadata. Put human text and string constants inside holes;
normally only `\t` remains a bare literal:

```csharp
// Wrong: the handler receives "Charges" as delimiter text.
list.Add(1060658, $"Charges\t{charges}");

// Correct: both values are formatted arguments.
list.Add(1060658, $"{"Charges"}\t{charges}");
```

Pass values directly. Do not place `.ToString()`, `string.Format`, concatenated
strings, prebuilt strings, LINQ output, or conditional formatting expressions
inside a hole. When an argument is itself a cliloc, use the current localized
argument overload or supported format specifier rather than raw `"#number"`
text.

These rules do not apply automatically to a normal message or gump interpolation
handler; inspect that handler separately.

## Free Text and Refresh

For variable multi-line free text, use the current `AddChunked` primitive or a
scoped text-block builder if the active interface provides one. Preserve line
boundaries and dispose the scoped builder so it flushes. A short localized
property should remain a normal property-list entry.

For a serialized displayed field, use the repository's generated invalidation
attribute only when supported. A custom setter or runtime state transition must
invalidate exactly when visible output changes and retain the local persistence
or dirty-marking rule. Avoid repeated invalidation when the displayed value is
unchanged.

## Test Shape

Record property number, argument payload, and sequence. Test both sides of an
era gate and the state transition that refreshes visible output. Use byte-level
or hash assertions only when packet behavior is the requested contract.
