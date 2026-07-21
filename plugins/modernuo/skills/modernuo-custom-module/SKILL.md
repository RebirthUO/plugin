---
name: modernuo-custom-module
description: Use when creating, registering, reviewing, renaming, or testing a separate
  ModernUO-based content assembly beside Projects/UOContent. Covers project/test wiring,
  solution/application references, assemblies.json load order, lifecycle hooks, and
  load smoke tests. Do not use for ordinary UOContent feature edits without a module
  boundary.
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Custom Module

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own a separate content assembly/runtime-load contract. Do not use it to organize ordinary UOContent or add placeholder gameplay. Follow naming/rename rules in [custom-module-setup.md](references/custom-module-setup.md).

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Read [custom-module-setup.md](references/custom-module-setup.md); inspect solution/Application/`assemblies.json`, UOContent/test projects, loader/lifecycle, and existing modules.
2. Define name, ownership, dependency direction, lifecycle, schema needs, and rollback.
   If ownership, selected module name, rollback, or resolved project paths are
   missing, return `BLOCKED` with those exact fields rather than selecting a
   repository convention by default.
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
- When hook ordering is unclear, use an available local lifecycle workflow or
  inspect the current source directly and state the limitation.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-custom-module`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-custom-module` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
