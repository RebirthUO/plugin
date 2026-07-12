---
name: modernuo-custom-module
description: Use when creating, registering, reviewing, renaming, or testing a separate ModernUO-based content assembly beside Projects/UOContent. Covers project/test wiring, solution/application references, assemblies.json load order, lifecycle hooks, and load smoke tests. Do not use for ordinary UOContent feature edits without a module boundary.
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

## Boundary

Own a separate content assembly/runtime-load contract. Do not use it to organize ordinary UOContent or add placeholder gameplay. Follow naming/rename rules in [custom-module-setup.md](references/custom-module-setup.md).

## Workflow

1. Read [custom-module-setup.md](references/custom-module-setup.md); inspect solution/Application/`assemblies.json`, UOContent/test projects, loader/lifecycle, and existing modules.
2. Define name, ownership, dependency direction, lifecycle, schema needs, and rollback.
3. Create module/tests from local project metadata; wire solution and Application, then load the DLL after `UOContent.dll` without a reverse dependency.
4. Add only real folders/hooks; let builds generate `.deps.json`.
5. Add an assembly-load/lifecycle smoke test, build/test, and inspect load order plus DLL/deps output.

## Safety gates

- Project references build; `assemblies.json` loads. Verify both and no base-assembly reverse dependency.
- `partial` types cannot extend a type across assemblies; use neutral hooks/interfaces instead.
- Serializable content requires the current generator packages and schema inputs.
- Preserve unrelated generated outputs and existing user changes.

## Verification/self-check

Confirm all wiring agrees, inspect generated DLL/deps output, and run the load smoke test.

## Output contract

Return project paths, solution/application/runtime wiring, dependency/load order, lifecycle surface, smoke/build/test evidence, generated-output status, and rollback/loading risks.

## Reference routing

- Always read [custom-module-setup.md](references/custom-module-setup.md) for creation, rename, or maintenance.
- Read [custom-module-smoke-and-guard.md](references/custom-module-smoke-and-guard.md) only for an infrastructure-only marker, assembly smoke suite, or explicitly requested post-commit verification.
- Read [modernuo-server-lifecycle](../modernuo-server-lifecycle/SKILL.md) when hook ordering is unclear.
