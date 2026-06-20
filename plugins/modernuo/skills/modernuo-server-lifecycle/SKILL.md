---
name: modernuo-server-lifecycle
description: Use when changing or reviewing ModernUO startup, bootstrap phases, reflection lifecycle hooks, first-boot prompts, Configure/Initialize ordering, server shutdown, world load/save events, or runtime loop behavior. Use before editing ConfigurePrompts, Configure, Initialize, CallPriority, ServerConfiguration, AssemblyHandler, Core.Setup, RunEventLoop, NetState startup, PingServer startup, or EventSink lifecycle wiring.
---

# ModernUO Server Lifecycle

## Purpose

Use this skill to make startup, shutdown, reflection hook, first-boot prompt, and event-loop changes without breaking boot order, world readiness, logging boundaries, or test/runtime assumptions.

## When This Activates

- Editing `Projects/Server/Main.cs`, `ServerConfiguration`, `AssemblyHandler`, `EventSink`, `World`, `NetState`, or startup/shutdown code.
- Adding or moving `ConfigurePrompts()`, `Configure()`, `Initialize()`, or `[CallPriority]`.
- Adding first-boot prompts, startup validation, boot-time cache work, server-start hooks, or world-save/world-load behavior.
- Debugging behavior that differs between production startup and xUnit fixtures.

## Key Rules

- `ConfigurePrompts()` runs after assemblies load and before Serilog's first log line; use `Console`, self-gate, and skip redirected input.
- `Configure()` runs before world load; use it for command registration, settings, event subscriptions, and pre-world wiring.
- `Initialize()` runs after tile data, regions, and world entities are loaded; use it for world-dependent validation, decoration, generation, and cache work.
- Do not depend on same-priority hook order. Use `[CallPriority(n)]`, explicit calls, or event wiring when order matters.
- Do not touch `World` entities, tile matrix data, or map-dependent content from `ConfigurePrompts()`.
- Treat tests carefully: fixture startup calls a curated subset and does not prove the full `Core.Setup()` ordering or first-boot console behavior.

## Patterns

### First-Boot Prompt Plus Later Work

```csharp
public static void ConfigurePrompts()
{
    if (ServerConfiguration.GetSetting("my.feature", (string)null) != null || Console.IsInputRedirected)
    {
        return;
    }

    Console.Write("Enable my feature? [y/N] ");
    var enabled = Console.ReadLine()?.Trim().StartsWith("y", StringComparison.OrdinalIgnoreCase) == true;
    ServerConfiguration.SetSetting("my.feature", enabled);
}

public static void Initialize()
{
    if (ServerConfiguration.GetSetting("my.feature", false))
    {
        // World, regions, tile matrix, and content entities are available here.
    }
}
```

### Startup Phase Check

Before moving startup code, map it to the production sequence: `ServerConfiguration.Load()`, `AssemblyHandler.LoadAssemblies(...)`, `ConfigurePrompts`, first Serilog log, `VerifySerialization()`, `Timer.Init(...)`, `Configure`, tile/region load, `World.Load()`, `Initialize`, networking, `ServerStarted`, `RunEventLoop()`.

## Anti-Patterns

- Logging with Serilog inside `ConfigurePrompts()` before the logging pipeline is live.
- Prompting from `Configure()` or `Initialize()`, where console output can interleave with logs or block headless boots.
- Reading world entities, regions, tile matrices, or client data before their phase has loaded them.
- Assuming xUnit fixture success proves first-boot prompt order, async console behavior, or production `Main.cs` startup order.
- Adding same-priority startup hooks that silently depend on execution order.

## Real Examples

- `Projects/Server/Main.cs` runs `AssemblyHandler.Invoke("ConfigurePrompts")` before first logger output, then `Configure`, then `World.Load()`, then `Initialize`.
- `Projects/Server/Configuration/ServerConfiguration.cs` owns engine first-boot prompts and uses `[CallPriority(0)]` so map selection precedes content prompts.
- `Projects/UOContent/Engines/Pathing/PathCacheCommands.cs` stores `pathfinding.prebakeMaps` in `ConfigurePrompts()` and bakes in `Initialize()` because baking needs tile data.
- `Projects/UOContent.Tests/Fixtures/TestServerInitializer.cs` manually calls selected startup pieces; keep fixture coverage separate from first-boot runtime verification.

## How to Report Issues

Report lifecycle findings with the phase, path, risk, and verification boundary:

```text
[LIFECYCLE] {severity}: {phase or event} - {issue}
  File: {path}:{line}
  Why it matters: {world readiness, logging, prompt, ordering, or test/runtime gap}
  Suggested check: {targeted test, first-boot runtime check, or dotnet build}
```

## See Also

- `dev-docs/server-lifecycle.md` - canonical startup phase guide.
- `dev-docs/threading-model.md` - event loop, async continuation, and world save threading model.
- `plugins/modernuo/skills/modernuo-configuration/SKILL.md` - configuration setting patterns.
- `plugins/modernuo/skills/modernuo-events/SKILL.md` - `EventSink` and event subscription patterns.
- `plugins/modernuo/skills/modernuo-threading/SKILL.md` - single-threaded game loop constraints.
