---
name: modernuo-custom-module
description: Use when creating, registering, reviewing, or maintaining a custom ModernUO/RebirthUO content module beside Projects/UOContent. Covers CUOContent default naming, module/test projects, ModernUO.slnx, Application.csproj, Distribution/Data/assemblies.json runtime loading, lifecycle hooks, top-level folder mirroring, and assembly-load smoke tests. Do not use for ordinary feature edits inside Projects/UOContent unless a separate custom module boundary is part of the task.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
    - modernuo
    - rebirthuo
    - custom-module
    - content
    - assemblies
    related_skills:
    - modernuo-content-patterns
    - modernuo-server-lifecycle
    - modernuo-configuration
    - modernuo-test-workflow
    - modernuo-code-audit
---
# ModernUO Custom Module

## Overview

Use this skill to keep shard-specific content in a separate assembly that builds and loads beside `UOContent`. Read `references/custom-module-setup.md` before editing; trigger cases live in `evals/trigger_cases.json`.

## When to Use

- Creating a separate shard/custom content assembly beside `Projects/UOContent`.
- Registering module DLLs in `Distribution/Data/assemblies.json`.
- Reviewing custom module project references, test project setup, lifecycle hooks, or assembly-load smoke tests.

Do not use for ordinary content edits inside `Projects/UOContent` unless the request explicitly creates or maintains a separate module boundary.

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

For infrastructure-only custom module PRs and Hermes post-commit verification guards, see `references/custom-module-smoke-and-guard.md`. It covers the no-op marker pattern, assembly-load smoke tests, committed-branch `HEAD~1..HEAD` diff checks, generated DLL/deps checks, and how to report the result as ad-hoc/focused verification rather than broad suite-green.


## Common Pitfalls

1. **Hand-editing generated `.deps.json`.** Build the projects and let the SDK generate dependency files.
2. **Confusing build references with runtime loading.** `Application.csproj` builds/copies; `assemblies.json` controls runtime loading order.
3. **Mirroring deep folders before content exists.** Create top-level domain folders first; add nested folders only for real content.
4. **Skipping the smoke test.** A project can build while failing runtime assembly load or lifecycle reflection.

## Verification Checklist

- [ ] `ModernUO.slnx`, `Application.csproj`, and `assemblies.json` all reference the module consistently.
- [ ] Module output lands under `Distribution/Assemblies` without hand-editing generated files.
- [ ] Tests reference `Server`, `UOContent`, the module, and `Server.Tests` as needed.
- [ ] A build plus assembly-load smoke test ran, or the blocker is reported.
