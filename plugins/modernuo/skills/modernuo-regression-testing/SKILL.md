---
name: modernuo-regression-testing
description: Use when writing or repairing ModernUO/RebirthUO regression tests for gameplay mechanics, spells, special moves, timers, summons, combat hooks, and UOContent fixture pitfalls. Complements modernuo-test-workflow with concrete runtime-test patterns.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: implement
    workflow_tier: support
    tags: [modernuo, rebirthuo, tests, regression, xunit]
    related_skills:
      - modernuo-test-workflow
      - modernuo-test-naming
      - modernuo-code-audit
      - modernuo-era-expansion
---

# ModernUO Regression Testing

## Overview

Use this skill for class-level regression-test patterns that prevent a fixed UO mechanic from drifting again. It is intentionally narrower than `modernuo-test-workflow`: load `modernuo-test-workflow` for the full build/test/PR validation path, and load this skill when the hard part is choosing the right test surface or handling UOContent runtime fixtures.

A good regression test proves the player-visible behavior that failed, at the smallest reliable layer, without widening production APIs or inventing a fake server world that hides the bug.

## When to Use

- Adding or debugging tests under `Projects/UOContent.Tests` or related ModernUO test projects.
- A parity ticket is labeled `Test missing`, `needs regression`, or similar.
- Testing spells, skill formulas, special moves, summons, timers, `BaseCreature`, combat hooks, movement, poison, or era-gated behavior.
- A focused test fails because server registries, static tables, NPC speeds, poison definitions, movement settings, or spell registries were not initialized.

Don't use this as a replacement for broad validation. After the focused regression passes, still follow `modernuo-test-workflow` for build/test scope and PR-readiness reporting.

## Core Workflow

1. Validate the issue against current `origin/live` and owning code before writing a test.
2. Prefer the smallest owning test surface: formula-only tests for pure helpers, runtime tests for real entity/combat/timer/map-sector behavior.
3. Keep era explicit in tests that depend on AOS/SE/ML/SA/TOL/EJ behavior. Save and restore `Core.Expansion` in `try/finally`.
4. Use existing repository fixture patterns before inventing new ones.
5. Run, in order:
   - `git diff --check -- <changed files>`
   - `dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj --nologo --verbosity quiet -m:1`
   - focused `dotnet test` for the changed test class or namespace
   - a neighboring test filter when the change touches shared hooks.
6. Commit/push only when the user asked for PR branch changes and real validation output is green.

## Patterns and Pitfalls

### Lightweight Formula Tests

For pure scalar/formula hooks, avoid full world setup when possible. Use uninitialized objects plus `DefaultMobileInit()` only if the required static tables are configured.

If a test touches `mobile.Skills.<Skill>.Base`, ensure `SkillInfo.Table` is available first. In isolated formula contexts, call the repository's normal setup or `SkillsInfo.Configure()` before creating `Skills`; otherwise skill lookup can fail because the skill table is empty.

### BaseCreature / NPC-Speed Tests

Any test that constructs a `BaseCreature` subclass may need `NPCSpeeds` configured. If the full JSON fixture is not loaded, register a minimal `SpeedLevel.Medium` entry once in the test class before constructing the creature.

### Runtime Tests vs Formula Tests

Use runtime tests when the behavior depends on real `Mobile`, `Item`, `BaseCreature`, follower slots, clone cleanup, timers, map sectors, targeting, line of sight, or region hooks. Do not force these through pure formula tests just to avoid setup.

### Protected Timer / Summon State

Do not widen production visibility just to test protected state such as `BaseCreature.SummonEnd`. Use reflection in tests following existing repository patterns, and keep the reflection local to the test helper.

### SpecialMove Reset Tests

When testing a `SpecialMove` hook directly, you can insert it into `SpecialMove.Table[mobile]` and invoke the hook. If spell registry/netstate toggle support is not initialized, clean up with `SpecialMove.Table.Remove(mobile)` rather than `SpecialMove.ClearCurrentMove(mobile)`.

## Common Pitfalls

1. **Writing the test before proving the owner.** Search the owning code path first; otherwise the test may lock in the wrong layer.
2. **Calling a focused test run a suite pass.** Report focused filters as focused. Run broader checks when the user expects PR readiness.
3. **Changing production visibility for test convenience.** Prefer test helpers/reflection over public API expansion unless the API is product-justified.
4. **Forgetting global-state cleanup.** Restore `Core.Expansion`, static tables, special-move tables, and any configured registries in `try/finally` or fixture disposal.
5. **Skipping neighboring tests.** Shared spell/combat/timer hooks can pass the new test while breaking a sibling mechanic.

## References

- `references/ninjitsu-special-move-regression-tests.md` — session-derived patterns for Mirror Image clone tests, Focus Attack formula tests, NPCSpeeds setup, `SummonEnd` reflection, and SE-MISS ledger caveats.

## Verification Checklist

- [ ] The test target is the smallest layer that still proves the player-visible behavior.
- [ ] Era-dependent tests save and restore `Core.Expansion`.
- [ ] Fixture setup initializes required registries or explicitly uses the repository's standard test setup.
- [ ] Global/static state is cleaned up after the test.
- [ ] Focused and neighboring test commands actually ran, and the final report labels their scope accurately.

## Reporting

In PR descriptions, explain the player-visible mechanic first, then the test/code anchor. For parity tickets, cite the issue-supplied source and explicitly note when a cited ledger file is absent on the target base.
