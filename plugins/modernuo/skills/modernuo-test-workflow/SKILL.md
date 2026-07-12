---
name: modernuo-test-workflow
description: Use when executing or validating tests in a ModernUO-based repository, especially entity fixtures, process-global state, client data, isolated worktrees, focused versus broad evidence, or PR readiness. Use modernuo-regression-testing to design assertions and modernuo-test-naming for rename-only work.
version: 2.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: implement
    workflow_tier: support
    tags: [modernuo, tests, xunit, validation, fixtures]
    related_skills:
      - modernuo-codebase
      - modernuo-code-audit
      - modernuo-regression-testing
      - modernuo-test-naming
      - modernuo-verification-guard
---

# ModernUO Test Workflow

## Boundary

Own test placement, fixture/bootstrap reliability, worktree correctness,
command scope, failure clustering, and honest validation reporting. Assertion
design and rename-only cleanup belong to their specialist skills.

## Workflow

1. Read repository instructions and confirm exact root, branch/HEAD, base, dirty
   and untracked state before editing or testing.
2. Locate the owning test project from the current solution/project graph and
   reuse its fixtures, collections, data conventions, and naming.
3. Read [testing patterns](references/testing-patterns.md) for entity,
   process-global, client-data, and worktree risks.
4. Run changed-path diff checks, required generators, the owning build, and the
   narrow behavior filter from the verified worktree.
5. Run adjacent tests for shared hooks. For global/shared changes or PR
   readiness, run the owning project or broader solution in proportion to risk.
6. Cluster broad failures and compare a clean baseline when needed. Report
   environment/bootstrap failures separately from product regressions.
7. Repeat focused checks after the final code or test edit and audit final
   status/diff.

## Guardrails

- Restore expansion/profile, static tables, registries, RNG, timers, entities,
  action locks, and files even when assertions fail.
- Missing generated output or configured client/server data is a fixture
  blocker, not a gameplay pass or failure.
- Verify worktree registration/root/status before trusting results from sibling
  checkouts.
- Never call a focused filter, ad-hoc verifier, or local broad run “CI green.”
- Commit, push, PR, merge, and post-merge validation require their own authority.

## Output contract

Return repository/worktree/branch/HEAD, changed tests, fixture/global state,
exact commands and denominators, focused/adjacent/broad results, baseline or
environment blockers, and any authorized external mutation state.

## Verification

- Diff checks cover every changed path in the correct worktree.
- Owning build and focused behavior tests ran after the final edit.
- Shared/global changes have proportional broad evidence or an explicit blocker.
- Evidence labels match what actually ran.
