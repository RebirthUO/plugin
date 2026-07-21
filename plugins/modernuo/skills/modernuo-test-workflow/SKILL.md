---
name: modernuo-test-workflow
description: Use when executing or validating tests in a ModernUO-based repository,
  especially entity fixtures, process-global state, client data, isolated worktrees,
  focused versus broad evidence, or PR readiness. Use modernuo-regression-testing
  to design assertions and modernuo-test-naming for rename-only work.
license: MIT
metadata:
  version: 2.0.0
---

# ModernUO Test Workflow

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own test placement, fixture/bootstrap reliability, worktree correctness,
command scope, failure clustering, and honest validation reporting. Assertion
design and rename-only cleanup belong to their specialist skills.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, validation surface, or gameplay/parity source claim cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. A source claim is required only when the requested test work makes or changes one. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

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
   Make one bounded retry after a reproducible environment repair and one clean
   baseline comparison; then return `BLOCKED` with the failing denominator,
   revision, and smallest environment or product decision. Do not loop on the
   same unexplained broad failure.
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

Return an evidence table with `Status` (`PASSED`, `FAILED`, or `BLOCKED`),
`Repository revision`, `Command`, `Denominator`, and `Limitation`; include
repository/worktree/branch/HEAD, changed tests, fixture/global state,
focused/adjacent/broad results, and any authorized external mutation state.

Emit each table row as one `Decision.records` entry with `kind: test-evidence`; put `Status`, command, denominator, limitation, worktree identity, and mutation state in `details`. Render the Markdown table only from those records after the YAML envelope.

## Verification

- Diff checks cover every changed path in the correct worktree.
- Owning build and focused behavior tests ran after the final edit.
- Shared/global changes have proportional broad evidence or an explicit blocker.
- Evidence labels match what actually ran.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-test-workflow`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-test-workflow` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
