---
name: modernuo-custom-module
description: Use when creating, registering, reviewing, or maintaining a custom ModernUO/RebirthUO content module beside Projects/UOContent. Covers CUOContent default naming, module/test projects, ModernUO.slnx, Application.csproj, Distribution/Data/assemblies.json runtime loading, lifecycle hooks, top-level folder mirroring, and assembly-load smoke tests. Do not use for ordinary feature edits inside Projects/UOContent unless a separate custom module boundary is part of the task.
---

# ModernUO Custom Module

## Overview

Use this skill to keep shard-specific content in a separate assembly that builds and loads beside `UOContent`. Read `references/custom-module-setup.md` before editing; trigger cases live in `evals/trigger_cases.json`.

## Naming

- If the user gives a server, shard, or module shortcut, normalize it to PascalCase and use `{Shortcut}Content`, `{Shortcut}Content.Tests`, and `{Shortcut}Content.dll`.
- If no shortcut is given, offer and use `CUOContent`, `CUOContent.Tests`, and `CUOContent.dll`. `CUO` means `CustomUO`.
- Use `CustomUO Content` as the default product/display text.
- Ask for a name only if `CUOContent` conflicts or the user requires a brand.

## Setup Workflow

1. Inspect `ModernUO.slnx`, `Projects/Application/Application.csproj`, `Distribution/Data/assemblies.json`, `Projects/UOContent/UOContent.csproj`, and existing custom module projects.
2. Create `Projects/{Module}` and `Projects/{Module}.Tests`.
3. Configure `{Module}.csproj` with `RootNamespace=Server`, output/publish paths under `Distribution/Assemblies`, `Server` and `UOContent` references, and `InternalsVisibleTo` for `{Module}.Tests`.
4. Mirror only top-level `UOContent` domain folders; add deeper folders only for real content.
5. Configure `{Module}.Tests.csproj` with `Server`, `UOContent`, `{Module}`, and `Server.Tests`.
6. Register both projects in `ModernUO.slnx`.
7. Reference `{Module}.csproj` from `Projects/Application/Application.csproj` with existing non-copying content assembly metadata.
8. Add `{Module}.dll` to `Distribution/Data/assemblies.json` after `UOContent.dll`.
9. Build instead of hand-editing generated `.deps.json`.
10. Add an assembly-load smoke test.

## Lifecycle

- Startup reads `assemblies.json`, loads DLLs from `Distribution/Assemblies`, then reflects public static `ConfigurePrompts`, `Configure`, and `Initialize`.
- Use `Configure` for settings/static registration, `Initialize` for post-world/entity-dependent registration, and `ConfigurePrompts` only for self-gated first-boot prompts.
- Keep project references separate from runtime loading: `Application.csproj` builds the module; `assemblies.json` loads it.

## Maintenance Checks

Use the reference for rename checks, generated-file boundaries, migration schemas, test fixture shape, and related skills.
