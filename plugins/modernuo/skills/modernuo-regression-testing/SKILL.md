---
name: modernuo-regression-testing
description: >
  Use when designing or repairing focused ModernUO-based regression tests
  for gameplay formulas, entities, combat hooks, timers, summons, or fixture
  state. Use modernuo-test-workflow for full build/suite/PR execution and
  modernuo-test-naming for rename-only cleanup.
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

## Boundary

Choose the smallest reliable test surface that proves the player-visible bug and
would fail if it returned. This skill covers test design and UOContent fixture
pitfalls, not the entire PR validation workflow.

## Workflow

1. Reproduce or trace the issue on the requested/current baseline and identify
   the owning production path before writing assertions.
2. Use a pure helper/formula test only when it proves the behavior. Use real
   entities, maps, timers, combat hooks, or registries when those are part of the
   contract.
3. Reuse existing fixture/setup patterns. Initialize only required registries and
   keep process-global tests in the sequential collection.
4. Pin era-dependent behavior by saving/restoring `Core.Expansion` in
   `try/finally`; clean every static table, timer, entity, and action lock changed
   by the test.
5. Make probabilistic branches deterministic with an existing test RNG or a
   narrow seam. Do not loop until a random proc appears.
6. Run diff check, owning build, focused test, and a neighboring filter for shared
   hooks. Hand broader validation to `modernuo-test-workflow`.

## Guardrails

- Do not widen production visibility merely to inspect protected state; prefer
  existing internal seams or a local test helper/reflection pattern.
- Named skill access requires `SkillInfo.Table`; real `BaseCreature`
  construction may require `NPCSpeeds`; entity deletion requires normal mobile/
  world initialization.
- Runtime tests are required for follower slots, summon cleanup, timer expiry,
  map sectors, targeting, LOS, and region/combat integration.
- Restore global state even when assertions fail. A focused pass plus broad-run
  failure can indicate static-state leakage, not product correctness.
- Label focused, neighboring, project, and solution runs accurately.

## Output Contract

Return the bug/owner, chosen test layer and why, fixture/global state used,
assertions that prove the visible behavior, commands/results, and broader-suite
status. Do not call a focused filter suite-green.

## Verification

- The test fails against the faulty behavior or otherwise demonstrates its
  regression sensitivity.
- It is deterministic, isolated, and cleans all entities/global state.
- Era-before and era-after cases are covered when applicable.
- Focused and neighboring tests pass; broader validation status is explicit.

## Reference Routing

- Read [UOContent fixture pitfalls](references/uocontent-test-fixture-pitfalls.md)
  when constructors, skills, NPC speeds, bodies, summons, or registry setup fail
  before assertions.
- Load `modernuo-test-workflow` for worktrees, client-data setup, broad-suite
  clustering, guard verification, commit/push, or PR readiness.
- Load the owning mechanic skill before freezing behavior into a regression test.
