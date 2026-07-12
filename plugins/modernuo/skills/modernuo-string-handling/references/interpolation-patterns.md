# Interpolation and ValueStringBuilder Patterns

Read this reference when converting complex branches, choosing capacity, or using
builder helpers that take `ref`.

## Handler-aware calls

The compiler selects a handler overload only when the interpolation is directly
in argument position:

```csharp
mobile.SendMessage($"You have {gold:N0} gold");
gump.AddLabel(x, y, hue, $"Score: {score:N0}");
```

Common allocation traps and repairs:

| Trap | Repair |
|---|---|
| `Send(condition ? $"a {x}" : $"b {x}")` | `if/else`, one direct call per branch |
| switch expression returning interpolated strings | switch statement with calls |
| `var text = $"..."; Send(text)` | inline at the single call site |
| `$"{value.ToString()}"` | pass `{value}` directly |
| `$"{a + b}"` for strings | use `{a}{b}` |
| `string.Format(...)` | direct interpolation |
| LINQ aggregation in a hole | assemble with `ValueStringBuilder` |

Use `:L` only where the ModernUO handler defines lowercase formatting:

```csharp
mobile.SendMessage($"You earned a {rank:L} trophy");
```

## ValueStringBuilder

Bounded, stack-backed assembly:

```csharp
using var builder = new ValueStringBuilder(stackalloc char[128]);
builder.Append($"{name}: {score:N0}");
Consume(builder.AsSpan());
```

Unbounded assembly that may rent:

```csharp
using var builder = ValueStringBuilder.Create(256);
builder.Append(prefix);
builder.Append(value);
return builder.ToString(); // allocate only because the API returns string
```

Reuse within a loop with `Reset()`. `Append` returns `void`, so do not chain it.

If an extension takes `ref ValueStringBuilder`, a `using var` local cannot be
passed by ref. Dispose explicitly:

```csharp
var builder = new ValueStringBuilder(stackalloc char[64]);
try
{
    builder.AppendSpaceWithArticle(text, articleAn);
    return builder.ToString();
}
finally
{
    builder.Dispose();
}
```

## Capacity guidance

Choose from evidence, not a fixed universal table:

- small coordinates/version fragments often fit in 32–64 chars;
- player/item labels commonly fit in 64–128;
- bounded descriptions/HTML fragments may use 128–256;
- unbounded reports or large HTML should use the renting factory.

Stack allocation is not automatically better if the bound is large or called
deeply. Measure hot-path stack/heap behavior and keep maximum input lengths safe.

## Culture and ownership

Default interpolation follows the applicable handler/current culture unless the
API says otherwise. Tests expecting invariant decimal/date output must set and
restore culture or use an explicit invariant contract. `AsSpan()` is valid only
while the builder/buffer lives; call `ToString()` when text must escape that
lifetime.

## Property-list exception

`IPropertyList` has special delimiter/argument semantics: human text constants
belong in holes and tabs are bare delimiters. Do not transfer that rule to normal
message/gump handlers. Load `modernuo-property-lists` for tooltip examples.
