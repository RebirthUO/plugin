---
name: modernuo-test-naming
description: >
  Use when auditing or normalizing ModernUO-based xUnit file, class, or
  method names polluted by publish, era-context, branch, issue, task, AI,
  regression, coverage, or smoke prefixes. Keep real product/domain names and
  make rename-only changes; use modernuo-regression-testing for test behavior.
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
      - tests
      - naming
      - code-style
    related_skills:
      - modernuo-test-workflow
      - modernuo-regression-testing
      - modernuo-no-publish-prefix-names
---

# ModernUO Test Naming

## Boundary

Name tests after the tested production object, operation, or stable area—not the
work batch that created them. This skill changes identity only: no assertions,
fixtures, data, production code, or behavior.

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

For audit-only work, group findings by confidence with
path/line/current/suggested/reason and state when hard-noise count is zero. For
implementation, return old/new mappings, unchanged behavior scope,
commands/results, and requested PR state.

## Verification

- Prefix scan has no actionable hard-noise findings after cleanup.
- File, class, and method names identify the actual tested object/operation.
- Only identifiers/direct references changed; staged diff contains no behavior.
- Focused renamed-class tests/build pass; broad exploratory failures are labeled
  separately.

## Reference Routing

- Read [test prefix audit checklist](references/test-prefix-audit.md) for hard vs
  soft classification and era/domain examples.
- Read [rename-only PR cleanup](references/rename-pr-cleanup.md) only when applying
  the normalization in an isolated branch/worktree or completing a PR.
- When changing this skill's trigger, run the existing cases in
  `evals/trigger_cases.json` with `evals/semantic_config.json`.
- Load `modernuo-regression-testing` for assertion/fixture changes and
  `modernuo-test-workflow` for full validation.
