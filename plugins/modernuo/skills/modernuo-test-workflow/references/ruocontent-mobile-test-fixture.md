# RUOContent Mobile / BaseCreature Test Fixture Pattern

Use this when adding tests under `Projects/RUOContent.Tests` that instantiate real `Mobile`, `BaseCreature`, or RUOContent mobiles.

## Why

The RUOContent smoke fixture that only loads assemblies is not enough for entity construction. `Mobile()` and `BaseCreature()` require core world/test bootstrap state:

- `Map.Internal.DefaultRegion` must exist.
- `World.NewMobile`, `World.AddEntity`, and entity registries must be configured.
- `BaseCreature` speed initialization needs `NPCSpeeds.Configure()` so `SpeedLevel.Medium` exists.
- Entity tests often need `DecayScheduler`, timers, and world serialization worker shutdown initialized like `Server.Tests` / `UOContent.Tests` fixtures.

Without this, focused RUOContent tests can fail before assertions with null refs in `Mobile..ctor()` or `KeyNotFoundException: Medium` in `NPCSpeeds.GetSpeeds()`.

## Fixture bootstrap checklist

For RUOContent tests that instantiate entities, extend the RUOContent fixture after `ServerConfiguration.Load(true)` and `AssemblyHandler.LoadAssemblies(["UOContent.dll", "RUOContent.dll"])` with the same core pieces used by server/UOContent tests:

```csharp
Core.LoopContext = new EventLoopContext();
Core.Expansion = Expansion.EJ;

Server.Network.NetState.Configure();
TestMapDefinitions.ConfigureTestMapDefinitions();
Server.Mobiles.NPCSpeeds.Configure();
World.Configure();
Server.Timer.Init(0);
World.Load();
World.ExitSerializationThreads();
DecayScheduler.Configure();
```

Add the required usings:

```csharp
using Server.Items;
using Server.Tests.Maps;
```

Use `Server.Timer.Init(0)` explicitly when `System.Threading` is imported, otherwise `Timer` is ambiguous.

## RUOContent serializable classes

If RUOContent introduces `[SerializationGenerator]` content classes, verify `Projects/RUOContent/RUOContent.csproj` references the serialization packages and migrations input, not just `Server`/`UOContent`:

```xml
<PackageReference Include="ModernUO.Serialization.Annotations" Version="2.14.2" />
<PackageReference Include="ModernUO.Serialization.Generator" Version="2.14.3" />
<AdditionalFiles Include="Migrations/*.v*.json" />
```

Match versions already used by `Projects/UOContent/UOContent.csproj` unless the repo has deliberately bumped them.

## Validation pattern

After changing the fixture or adding an entity test:

```bash
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/RUOContent.Tests/RUOContent.Tests.csproj \
  --filter "FullyQualifiedName~<NewTestClass>" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
dotnet test Projects/RUOContent.Tests/RUOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

Label the first test as focused and the second as the RUOContent.Tests project, not full solution green.
