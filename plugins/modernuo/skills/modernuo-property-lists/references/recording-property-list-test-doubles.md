# Recording Property-List Test Doubles

Read this reference only when a private `IPropertyList` test double stops
compiling after the consuming repository changes the interface.

## Diagnose Before Patching

Inspect the active interface and compiler diagnostics first. A stale double can
fail before assertions execute because it lacks new span, chunking, or text-block
members. Do not copy a member list from this reference without comparing it with
the pinned source.

For a recording-only double, delegate new text forms to the same entry recorder
that existing assertions use. A current ModernUO-style interface may require a
shape like this:

```csharp
public void Add(ReadOnlySpan<char> argument) => Add(argument.ToString());
public void Add(int number, ReadOnlySpan<char> argument) =>
    Entries.Add(new Entry(number, argument.ToString()));
public void AddChunked(ReadOnlySpan<char> text) => Add(text);
public OplTextBlock TextBlock() => new(this);
```

This is suitable only when tests assert recorded cliloc/raw entries. If the
feature relies on chunk boundaries, disposal, packet encoding, hashing, or
allocation behavior, test the real property-list implementation at the smallest
reliable layer instead.

## Verify

Rebuild the owning test project before interpreting assertion results. Then run
the focused property-list filter and report its exact denominator. Run the
broader owning project only when the changed interface or shared helper makes
that proportionate.
