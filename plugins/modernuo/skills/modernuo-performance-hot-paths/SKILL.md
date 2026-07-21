---
name: modernuo-performance-hot-paths
description: 'Use when reviewing or changing ModernUO game-loop hot paths such as
  AI, combat, spatial scans, packet fan-out, region hooks, timers, pathfinding, pooling,
  LINQ, or dynamic text. Do not use to claim a measured speedup without profiling
  or benchmarks; use modernuo-code-audit for the broader code review.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Performance Hot Paths

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Classify cost before optimizing. Hot code runs per tick, movement, combat event,
target, region hook, timer pulse, or visible client; warm code runs regularly but
not continuously; cold code is startup, admin, migration, or rare diagnostics.
Optimize repeated/fan-out cost while preserving gameplay and era behavior.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Name the path class, invocation frequency, fan-out, and current evidence.
2. Trace the owning API and inspect neighboring code before replacing a query,
   collection, buffer, string, region lookup, or pathfinding budget.
3. Find the dominant cost: O(world) enumeration, allocation, formatting, copying,
   algorithmic budget, blocking work, or unnecessary synchronization.
4. Apply the smallest repository-native change that removes that cost without
   changing target sets, ordering, timing, or era mechanics.
5. Run a focused correctness test first; benchmark/profile representative load
   for any performance claim.

## Guardrails

- Never scan `World.Mobiles` or `World.Items` for local gameplay. Use map/sector
  range or bounds queries and verify exact geometry when range matters.
- Process directly when possible; otherwise use repository-native pooled/stack
  storage selected for the actual thread context.
- Apply the repository LINQ tiers. Do not enforce a blanket no-LINQ rule, but keep
  allocating/chained Tier 3 patterns out of hot paths.
- Keep handler-aware `$"..."` expressions directly at message/gump/property-list
  call sites; pre-built strings and `.ToString()` holes defeat zero-allocation
  formatting.
- `Region.Find(point, map)` is sector-indexed; name lookup is a linear cold-path
  operation.
- Do not raise A* budgets, add synchronous cache construction, or move world state
  to background threads as an unmeasured shortcut.
- Performance work cannot silently change gameplay or era semantics.

## Output Contract

Return the path class and frequency, before/after algorithm or allocation shape,
behavioral invariants, evidence type, commands/results, and residual risk.

```text
[PERF] {ERROR|WARN|INFO}: {issue}
  File: {path}:{line}
  Path: {hot|warm|cold} because {frequency/fan-out}
  Cost: {allocation|O(world)|linear lookup|blocking|budget}
  Evidence: {static|test|benchmark|profile}
```

## Verification

- Target set, ordering, timing, and era gates are unchanged unless explicitly in
  scope.
- Focused tests pass before performance measurements are interpreted.
- Allocation/throughput/tick claims include reproducible measured evidence.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-performance-hot-paths`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-performance-hot-paths` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [hot-path decision matrix](references/hot-path-decision-matrix.md) when
  selecting spatial, pooling, string, region, or pathfinding patterns.
- Load the corresponding specialist skill for exact APIs:
  `modernuo-threading`, `modernuo-string-handling`, `modernuo-regions`,
  `modernuo-pathfinding`, `modernuo-networking`, or
  `modernuo-spatial-range-geometry`.
- When present, read `dev-docs/code-standards.md` for the current LINQ tiers.
