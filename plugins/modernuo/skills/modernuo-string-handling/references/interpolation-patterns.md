# Interpolation and ValueStringBuilder Patterns

Read this reference only after inspecting the repository's current overloads and
`Server.Text.ValueStringBuilder` implementation. Examples are candidate patterns,
not proof that an API exists at the consuming revision.

## Handler-aware calls

Handler selection normally requires interpolation directly in argument position:

```csharp
mobile.SendMessage($"You have {gold:N0} gold");
gump.AddLabel(x, y, hue, $"Score: {score:N0}");
```

Verify this by inspecting the overload declaration or compiler binding. Common
intermediate-string risks include a pre-built interpolated local, interpolated
ternary or switch result, `string.Format`, string concatenation inside a hole,
and `.ToString()` inside a hole. Branch the call itself when necessary.

Custom format specifiers such as `:L` are repository-specific. Use one only when
the inspected handler implements it and tests cover the visible result.

## Builder selection and lifetime

For a proven small bound, a stack-backed builder may be appropriate:

```csharp
using var builder = new ValueStringBuilder(stackalloc char[128]);
builder.Append($"{name}: {score:N0}");
Consume(builder.AsSpan());
```

For unbounded input, use the inspected growth-capable factory and dispose any
rented storage. Confirm whether `Append`, `Reset`, `Create`, and ref-taking
extensions exist at the target revision before using them.

`AsSpan()` is borrowed: the consumer must finish before reset or disposal. Use
`ToString()` when data is stored, returned, queued, cached, or otherwise escapes
the buffer lifetime.

When a verified helper takes `ref ValueStringBuilder`, follow the compiler and
repository disposal requirements. A common safe shape is explicit cleanup:

```csharp
var builder = new ValueStringBuilder(stackalloc char[64]);
try
{
    AppendVerifiedHelper(ref builder, value);
    return builder.ToString();
}
finally
{
    builder.Dispose();
}
```

## Capacity, culture, and encoding

Derive capacity from maximum inputs, existing limits, representative telemetry,
or measurement. Do not use a universal size table. Large stack allocations and
deep or recursive call paths require particular care.

Preserve the caller's culture contract. Tests for invariant output must establish
that contract explicitly and restore any changed ambient culture. Packet encoding,
terminators, truncation, and byte limits belong to `modernuo-networking`; gump
HTML escaping and layout belong to `modernuo-gump-system`.

## Property-list boundary

`IPropertyList` has distinct delimiter and argument rules. Do not generalize those
rules to ordinary message, gump, or packet handlers. Load
`modernuo-property-lists` before changing tooltip construction.
