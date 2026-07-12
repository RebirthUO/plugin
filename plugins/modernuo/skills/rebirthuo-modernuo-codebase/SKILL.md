---
name: rebirthuo-modernuo-codebase
description: 'Use when navigating the RebirthUO ModernUO codebase: repository layout, Projects/Server vs Projects/UOContent boundaries, build/test anchors, data/config folders, and common implementation surfaces.'
version: 0.1.0
author: Hermes
metadata:
  hermes:
    skill_group: rebirthuo
    skill_subgroup: agentic
    workflow_phase: none
    workflow_tier: support
    tags:
    - ModernUO
    - RebirthUO
    - Codebase
    - DotNet
    - UltimaOnline
    related_skills:
    - uo-modernuo-workflow
    - modernuo-code-audit
    - modernuo-test-workflow
license: MIT
---
# RebirthUO ModernUO Codebase

## Overview

This skill maps the local RebirthUO ModernUO service repository so you can pick the right project, docs, search strategy, and validation before editing. It does not replace domain-specific UO mechanics research, external era verification, or the specialized ModernUO skills. It uses Hermes built-in tools and the local .NET SDK; no extra packages are required.

## When to Use

- "Learn ModernUO", "navigate the ModernUO codebase", or "where does this live in RebirthUO?"
- Before editing `.cs` files under `Projects/` in `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- When deciding whether a change belongs in `Projects/Server/`, `Projects/UOContent/`, `Projects/Application/`, or tests.
- When translating RunUO/ServUO code into ModernUO patterns.
- When checking for repository conventions before implementation, review, or triage.

## Prerequisites

- Repository root: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- Read `AGENTS.md`; it delegates to `CLAUDE.md` in the repository root.
- Local SDK evidence: `global.json` requests .NET SDK `10.0.201` with `rollForward: latestMajor`; live tool output showed `dotnet --version` as `10.0.300`.
- Git remotes seen in this clone: `origin` is `https://github.com/RebirthUO/service.git`; `upstream` fetch is `https://github.com/modernuo/ModernUO.git`.
- No credentials are required for local inspection or build/test commands.

## How to Run

Use `read_file` for root instructions and project files, `search_files` for source discovery, and `terminal` only for `git`/`.NET` commands. Start every task by reading `AGENTS.md` and `CLAUDE.md`, then inspect the domain-specific docs under `dev-docs/` before editing. Invoke build and test commands through the `terminal` tool with `workdir` set to the repository root.

## Quick Reference

- Root: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`
- Agent instructions: `AGENTS.md`, `CLAUDE.md`
- Main solution: `ModernUO.slnx`
- SDK/config: `global.json`, `Directory.Build.props`, `version.json`
- Core engine: `Projects/Server/Server.csproj`
- Primary gameplay/content: `Projects/UOContent/UOContent.csproj`
- Server executable: `Projects/Application/Application.csproj`
- Tests: `Projects/Server.Tests/Server.Tests.csproj`, `Projects/UOContent.Tests/UOContent.Tests.csproj`
- Build: `dotnet build`
- Server tests: `dotnet test Projects/Server.Tests/Server.Tests.csproj --no-restore`
- Content tests: `dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --no-restore`
- Publish: `./publish.cmd [release|debug] [os] [arch]`, `./publish.sh [release|debug] [os] [arch]`
- Status: `git status --short --branch`
- Important docs: `dev-docs/code-standards.md`, `dev-docs/serialization.md`, `dev-docs/content-patterns.md`, `dev-docs/threading-model.md`, `dev-docs/server-lifecycle.md`, `dev-docs/string-handling.md`, `dev-docs/property-lists.md`, `dev-docs/gump-system.md`

## Procedure

1. **Load the repository contract.** Use `read_file` on `AGENTS.md`, `CLAUDE.md`, `README.md`, `global.json`, `Directory.Build.props`, and `ModernUO.slnx`. You are done when you can state the SDK target, project list, build command, and the rule that `Projects/Server/` is not edited without explicit request.

2. **Classify the task by project.** Prefer `Projects/UOContent/` for gameplay/content, `Projects/Server/` only for explicit engine changes, `Projects/Application/` for the executable host, `Projects/BuildTool/` for publish tooling, and `Projects/*Tests/` for tests. You are done when every planned file maps to one of those scopes.

3. **Read the closest dev-doc before code.** Use `read_file` on the relevant `dev-docs/` file: serialization, content patterns, timers, event scheduler, property lists, gumps, events, server lifecycle, configuration, networking, regions, string handling, threading, or RunUO migration. You are done when each risky convention has a source path you can cite.

4. **Load specialized skills for risky domains.** Use `skill_view` for the ModernUO skill matching the task, especially `modernuo-code-audit` for any `.cs` edit, `modernuo-serialization` for generated serialization, `modernuo-era-expansion` for `Core.*`, `modernuo-timers` for delayed actions, and the relevant UO domain skill for items, mobiles, housing, loot, combat, crafting, spells, quests, skills, harvest, or world/facet work. You are done when no active domain is covered only by this overview skill.

5. **Search by API shape, not only by filename.** Use `search_files` with `target="content"` and focused patterns:
   - Serialization: `\[SerializationGenerator|\[SerializableField|\[SerializableProperty|\[SerializedCommandProperty|\[TypeAlias`
   - Construction: `\[Constructible\]|public .*\(Serial serial\)`
   - Lifecycle: `public static void Configure\(|public static void ConfigurePrompts\(|public static void Initialize\(`
   - Era gates: `Core\.(AOS|SE|ML|SA|HS|TOL|EJ|PreAOS|UOR|T2A)`
   - Hot-path risks: `World\.(Items|Mobiles)|System\.Text\.StringBuilder|ArrayPool\.Shared|Task\.Run|new Thread|lock\s*\(|ConcurrentDictionary`
   - Client/UI/networking: `GetProperties\(|IPropertyList|BuildLayout\(|OnResponse\(|PacketHandlers\.Register|PacketWriter|ref RawInterpolatedStringHandler`
   You are done when you have at least one existing nearby pattern and one counterexample or doc rule for the risky part.

6. **Apply the core invariants before editing.** Keep all game logic single-threaded; avoid locks, `Task.Run`, `new Thread`, and concurrent collections in gameplay. Use `LogFactory.GetLogger(...)` instead of console writes, map spatial queries instead of direct `World.Items`/`World.Mobiles` scans in hot paths, `STArrayPool<T>.Shared` and `PooledRefList<T>` where the docs call for them, and `ValueStringBuilder`/direct `$"..."` calls for handler-aware string APIs.

7. **Respect persistence and client contracts.** Serializable entities must be `partial`; new generated entities use `[SerializationGenerator(version)]`; version bumps need `MigrateFrom(VXContent)`; `Deserialize(IGenericReader reader, int version)` is only for pre-codegen legacy saves; `TimerExecutionToken` is not serialized. Gumps must always produce visible UI, property-list string literals must be interpolation holes, and packets must preserve client-compatible layout and send checks.

8. **Validate through the narrowest honest command set.** Invoke `dotnet build` through the `terminal` tool from the repository root after code changes. Add `dotnet test Projects/Server.Tests/Server.Tests.csproj --no-restore` and/or `dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --no-restore` when touched behavior has tests or test helpers. You are done only when the command output is recorded, or failures are separated into baseline failures and regressions.

9. **Report with evidence.** Include repo paths, line ranges from `read_file`/`search_files`, commands actually run, and whether validation was broad or focused. For UO mechanics, state era/ruleset assumptions and external source status instead of treating local code as gameplay truth.

## Pitfalls

- `Projects/Server/` is core engine code; `CLAUDE.md` says not to modify it without explicit request.
- The clone has `ModernUO.slnx`; a `*.sln` search may return nothing.
- `Projects/UOContent/UOContent.csproj` uses `RootNamespace` `Server`, so namespace names alone do not prove the owning project.
- `Distribution/` is build/publish output, not source.
- `dev-docs/claude-skills/` files are opt-in Claude Code materials; in Hermes, prefer installed `skill_view` skills with the same domains.
- `Configure()`, `ConfigurePrompts()`, and `Initialize()` have different startup phases; do not move prompt, logging, tile-matrix, or world-dependent work between them casually.
- Migration JSON files under `Migrations/*.v*.json` are `AdditionalFiles` for source generators and are compile-time inputs, not runtime output.
- Focused tests are not broad-suite proof; label them focused unless the relevant suite actually ran.

## Verification

Invoke through the `terminal` tool from `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`:

```bash
dotnet build
```
