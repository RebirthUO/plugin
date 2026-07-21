# Custom Module Setup Reference

Use this reference when the task is specifically about creating or maintaining a separate ModernUO content module. It is a pattern guide, not a literal name source. `{ModuleName}` is a placeholder, not a default: do not create or select a module name until the user has approved it and the consuming repository's project, assembly, and distribution paths have been confirmed at the recorded revision.

## Files To Inspect

- `ModernUO.slnx` - solution registration for the application, content projects, and test projects.
- `Projects/Application/Application.csproj` - application project references that make content modules build with the server.
- `Distribution/Data/assemblies.json` - runtime assembly load list read by `Projects/Server/Main.cs`.
- `Projects/UOContent/UOContent.csproj` - content project conventions for output paths, package references, generators, migration schemas, and `InternalsVisibleTo`.
- `Projects/UOContent.Tests/UOContent.Tests.csproj` - test project conventions, package references, project references, and copied data.
- `Projects/Server/AssemblyHandler.cs` - assembly loading and reflected lifecycle invocation.
- `Projects/Server/Main.cs` - startup order: load configured assemblies, invoke `ConfigurePrompts`, then `Configure`, then `Initialize`.

## Default Naming

If the user does not provide a server or shard shortcut:

- Module project: `Projects/{ModuleName}/{ModuleName}.csproj`
- Test project: `Projects/{ModuleName}.Tests/{ModuleName}.Tests.csproj`
- Assembly name: `{ModuleName}`
- Runtime DLL: `{ModuleName}.dll`
- Product text: `CustomUO Content`
- Test collection: `Sequential {ModuleName} Tests`

If the user says "make one for Avalon" or gives shortcut `AV`, derive the project names from that shortcut instead, such as `AVContent` and `AVContent.Tests`.

## Module Project Shape

The module project should generally include:

```xml
<PropertyGroup>
    <RootNamespace>Server</RootNamespace>
    <AssemblyName>{ModuleName}</AssemblyName>
    <Product>CustomUO Content</Product>
    <OutDir>..\..\Distribution\Assemblies</OutDir>
    <PublishDir>..\..\Distribution\Assemblies</PublishDir>
    <Configurations>Debug;Release;Analyze</Configurations>
</PropertyGroup>
```

Use project references like:

```xml
<ProjectReference Include="..\Server\Server.csproj" Private="false" PrivateAssets="All" IncludeAssets="None">
    <IncludeInPackage>false</IncludeInPackage>
</ProjectReference>
<ProjectReference Include="..\UOContent\UOContent.csproj" Private="false" PrivateAssets="All" IncludeAssets="None">
    <IncludeInPackage>false</IncludeInPackage>
</ProjectReference>
```

Mirror `UOContent` package references only when the module needs the same capabilities, such as serialization, generated events, compression, configuration, or content infrastructure. Include migration schemas when adding serializable content:

```xml
<AdditionalFiles Include="Migrations/*.v*.json" />
```

## Runtime Registration

The runtime chain has two separate requirements:

- `Projects/Application/Application.csproj` references the custom module so it builds with the server application.
- `Distribution/Data/assemblies.json` lists the built DLL so the server loads it at runtime.

Add the application project reference with the same non-copying metadata as the existing content assembly references:

```xml
<ProjectReference Include="..\{ModuleName}\{ModuleName}.csproj" Private="false" PrivateAssets="All" IncludeAssets="None">
    <IncludeInPackage>false</IncludeInPackage>
</ProjectReference>
```

Add the runtime DLL after `UOContent.dll`:

```json
[
  "UOContent.dll",
  "{ModuleName}.dll"
]
```

Do not hand-edit generated `.deps.json` files. Run a build and inspect generated output only when troubleshooting dependency resolution.

## Folder Layout

For a new module, create only top-level maintainability folders that mirror `UOContent` domain boundaries. Common starting folders are:

```text
Projects/{ModuleName}/
  Commands/
  Configuration/
  Engines/
  Gumps/
  Items/
  Migrations/
  Misc/
  Mobiles/
  Multis/
  Network/
  Regions/
  Skills/
  Spells/
  Systems/
  Targets/
  Text/
  Utilities/
```

Do not recursively duplicate the entire `UOContent` tree. Add deeper folders only when implementing actual content.

## Test Project Shape

The test project should reference the engine, base content, the custom module, and server test helpers:

```xml
<ProjectReference Include="..\Server\Server.csproj" />
<ProjectReference Include="..\UOContent\UOContent.csproj" />
<ProjectReference Include="..\{ModuleName}\{ModuleName}.csproj" />
<ProjectReference Include="..\Server.Tests\Server.Tests.csproj" />
<DataFiles Include="$(SolutionDir)\Distribution\Data\**" />
```

Add a fixture that initializes the server test host and loads `Server.dll`, `UOContent.dll`, and `{ModuleName}.dll` into `AssemblyHandler`.

Add a smoke test:

```csharp
using System.Linq;
using Server;
using Xunit;

namespace {ModuleName}.Tests.Smoke;

[Collection("Sequential {ModuleName} Tests")]
public class AssemblyLoadTests
{
    [Fact]
    public void {ModuleName}Assembly_IsLoaded()
    {
        var loaded = AssemblyHandler.Assemblies.Any(a => a.GetName().Name == "{ModuleName}");
        Assert.True(loaded);
    }
}
```

## Validation

- `dotnet build ModernUO.slnx`
- `dotnet test Projects/{ModuleName}.Tests/{ModuleName}.Tests.csproj`
- Inspect `Distribution/Assemblies/{ModuleName}.dll` and `Distribution/Assemblies/{ModuleName}.deps.json` after build.
- Confirm `Distribution/Data/assemblies.json` still loads `UOContent.dll` before `{ModuleName}.dll`.
> Treat all names and paths in this reference as examples. Select one
> user-approved module placeholder for the task, resolve it against the
> consuming repository revision, and do not combine distinct example assembly
> names in one implementation.
