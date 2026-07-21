---
name: modernuo-test-naming
description: 'Use when auditing or normalizing ModernUO-based xUnit file, class, or
  method names polluted by publish, era-context, branch, issue, task, AI, regression,
  coverage, or smoke prefixes. Keep real product/domain names and make rename-only
  changes; use modernuo-regression-testing for test behavior.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Test Naming

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Name tests after the tested production object, operation, or stable area—not the
work batch that created them. This skill changes identity only: no assertions,
fixtures, data, production code, or behavior.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Inspect the test body, production symbols, namespace/path, fixture/data names,
   and assertions before choosing a name.
2. Scan file stems, classes, and xUnit methods separately; classify prefix noise
   with the audit reference.
3. Review `Coverage`, `Smoke`, and era words; keep only real suite/domain names.
4. Rename files/classes to `{ObjectOrArea}Tests` and methods to the local style
   (concise PascalCase or `Subject_Scenario_Expected`).
5. Search references/collisions, then run prefix scan, diff check, build, and
   focused renamed-class filters.
6. Complete the repository branch/PR workflow when requested.

## Guardrails

- Keep era/publish names when they are the actual tested object/domain.
- Move source/era context into scenario text, inline data, setup, comments, or
  assertion messages when it is not the subject.
- Ask before ambiguous, colliding, or cross-file renames.
- Do not mix behavior fixes into rename-only work.
- Preserve production-type acronym/casing conventions.

## Output Contract

For audit-only work, emit a table with `Status` (`ACTIONABLE`, `AMBIGUOUS`, or
`CLEAR`), `Confidence`, `Path`, `Line`, `Current`, `Suggested`, and `Reason`;
state `CLEAR` when hard-noise count is zero. For
implementation, return old/new mappings, unchanged behavior scope,
commands/results, and requested PR state.

## Verification

- Prefix scan has no actionable hard-noise findings after cleanup.
- File, class, and method names identify the actual tested object/operation.
- Only identifiers/direct references changed; staged diff contains no behavior.
- Focused renamed-class tests/build pass; broad exploratory failures are labeled
  separately.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-test-naming`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-test-naming` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [test prefix audit checklist](references/test-prefix-audit.md) for hard vs
  soft classification and era/domain examples.
- Read [rename-only PR cleanup](references/rename-pr-cleanup.md) only when applying
  the normalization in an isolated branch/worktree or completing a PR.
- When changing this skill's trigger, run the existing cases in
  `evals/trigger_cases.json` with `evals/semantic_config.json`.
- Load `modernuo-regression-testing` for assertion/fixture changes and
  `modernuo-test-workflow` for full validation.
