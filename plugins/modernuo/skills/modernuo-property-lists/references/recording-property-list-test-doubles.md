# RecordingPropertyList test doubles after IPropertyList interface changes

When `IPropertyList` gains new members, existing content tests with private
`RecordingPropertyList : IPropertyList` doubles can fail at compile time before
any assertions run.

Typical symptom:

```text
error CS0535: "<TestClass>.RecordingPropertyList" does not implement interface member
"IPropertyList.Add(ReadOnlySpan<char>)"
error CS0535: "<TestClass>.RecordingPropertyList" does not implement interface member
"IPropertyList.Add(int, ReadOnlySpan<char>)"
error CS0535: "<TestClass>.RecordingPropertyList" does not implement interface member
"IPropertyList.AddChunked(ReadOnlySpan<char>)"
error CS0535: "<TestClass>.RecordingPropertyList" does not implement interface member
"IPropertyList.TextBlock()"
```

Root cause: the product interface changed, but legacy per-test doubles still implement the old shape. This often appears when merging/cherry-picking OPL refactors such as `OplTextBlock` / `AddChunked` support.

Minimal compatibility implementation for recording-only tests:

```csharp
public void Add(ReadOnlySpan<char> argument) => Add(argument.ToString());
public void Add(int number, ReadOnlySpan<char> argument) => Entries.Add(new Entry(number, argument.ToString()));
public void AddChunked(ReadOnlySpan<char> text) => Add(text);
public OplTextBlock TextBlock() => new(this);
```

This is correct for tests that only assert emitted cliloc/argument entries; `OplTextBlock.Dispose()` will call back into `AddChunked`, so the recorded output still flows through the same `Entries` path.

Validation pattern:

```bash
export MODERNUO_TEST_DATA_DIR='<client-data-directory-containing-tiledata.mul>'
export MODERNUO_CLIENT_PATH="$MODERNUO_TEST_DATA_DIR"
export MODERNUO_CLIENT_PATH="$MODERNUO_TEST_DATA_DIR"
MSBUILDDISABLENODEREUSE=1 dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter 'FullyQualifiedName~PropertiesTests' --no-restore --nologo --verbosity quiet \
  --logger 'console;verbosity=minimal'
```

If the filtered compile is green, run the owning project broadly when feasible:

```bash
MSBUILDDISABLENODEREUSE=1 dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity quiet --logger 'console;verbosity=minimal'
```
