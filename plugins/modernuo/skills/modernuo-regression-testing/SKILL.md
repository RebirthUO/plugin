---
name: modernuo-regression-testing
description: 'Use when designing or repairing focused ModernUO-based regression tests
  for gameplay formulas, entities, combat hooks, timers, summons, or fixture state.
  Use modernuo-test-workflow for full build/suite/PR execution and modernuo-test-naming
  for rename-only cleanup.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Regression Testing

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Choose the smallest reliable test surface that proves the player-visible bug and
would fail if it returned. This skill covers test design and UOContent fixture
pitfalls, not the entire PR validation workflow.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

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

## Intake and result contract

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT` before acting. Record `Repository revision`, `Requested behavior`, `Evidence available`, and `Validation surface`; return `BLOCKED` when any required field is unavailable.

Emit exactly one fenced `yaml` document with this ordered, machine-readable schema. Keep all values factual; use `null` or an empty list rather than prose placeholders. Every datum promised by this skill's earlier output contract belongs in one or more `Decision.records` entries; use one record per affected surface, matrix row, warning, or finding. Place optional narrative after the YAML document only when it adds human context without changing the record values.

```yaml
Outcome: IMPLEMENTED | REVIEWED | BLOCKED
Repository revision:
  commit: <full revision or null>
  dirty: <true | false | null>
Decision:
  kind: REVIEW | PLAN | IMPLEMENT
  summary: <single factual sentence>
  records:
    - kind: <skill-specific contract item>
      subject: <path, symbol, matrix row, or finding>
      status: <verified | proposed | blocked | not-applicable>
      details: <required skill-specific fields>
      evidence_refs: [<Evidence.records.id>]
Evidence:
  records:
    - id: E1
      class: repository | official | test | runtime | user-supplied
      locator: <revision-bound path, URL, command, or null>
      claim: <fact supported by the record>
Verification:
  checks:
    - command_or_method: <command or inspection>
      result: passed | failed | not-run | blocked
      evidence_refs: [E1]
  runtime_smoke:
    result: passed | failed | not-run | unavailable
    runner_sha256: <summary value or null>
Confidence:
  level: high | medium | low
  basis: <evidence and verification basis>
Limitations:
  items: [<unresolved input, source, or validation limit>]
```

Use `high` confidence only with a current revision plus focused verification, `medium` with current static evidence but an unrun required check, and `low` when blocked or a required source is unavailable.

## Portable evidence

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-regression-testing`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-regression-testing` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [UOContent fixture pitfalls](references/uocontent-test-fixture-pitfalls.md)
  when constructors, skills, NPC speeds, bodies, summons, or registry setup fail
  before assertions.
- Load `modernuo-test-workflow` for worktrees, client-data setup, broad-suite
  clustering, guard verification, commit/push, or PR readiness.
- Load the owning mechanic skill before freezing behavior into a regression test.
