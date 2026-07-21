---
name: modernuo-pathfinding
description: 'Use when changing or diagnosing ModernUO AI movement, PathFollower,
  MovementPath, bounded A*, StepCache, .swb caches, prebake, PathCache commands, or
  pathfinding tests and tuning. Do not use for generic distance math alone; route
  exact range geometry to modernuo-spatial-range-geometry.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Pathfinding

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Preserve both movement correctness and the main-thread cost model across greedy
approach logic, bounded A*, walkability caches, persisted `.swb` data, prebake,
and diagnostics.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Reproduce with actor type/capabilities, map, start, goal, desired range,
   obstacle state, and cache state. Capture `PathRecord` or focused test evidence.
2. Trace the current path through `ApproachTarget`, `PathFollower`,
   `MovementPath`, `BitmapAStarAlgorithm`, and `StepCache` before changing a
   budget or fallback.
3. Keep open terrain on the greedy fast path. Engage or retain a path follower
   only when a step fails or makes no real progress.
4. Treat cache data as optional optimization: misses and unsupported walkers
   must fall through to live movement validation.
5. Compare solved routes, failed-route cost, allocations, and cache behavior on a
   representative corpus before tuning.
6. Run pathfinding tests sequentially and include cache-format tests when `.swb`
   layout or fingerprinting changes.

## Guardrails

- The local `38x38` search window and default `MaxSearchNodes` of `1000` are CPU
  guards. Do not raise them from anecdotal evidence.
- Do not replace bounded local A* with an unbounded/global search without a
  measured game-loop budget.
- `.swb` files are fingerprint-bound lazy backing stores, not portable universal
  assets. Stale data must regenerate from local client data.
- Resident chunk limits bound RAM; synchronous chunk building in movement hot
  paths requires tick-impact evidence.
- Preserve stationary-unreachable give-up behavior while testing moving targets,
  pets, and obstacle detours separately.
- Shared A* statics and live map data make parallel pathfinding tests unsafe.

## Output Contract

Return the reproduction, traced decision point, cache/budget assumptions, exact
behavioral change, benchmark/test evidence, and residual map/client-data risks.

```text
[PATHFINDING] {severity}: {issue}
  Actor/route: {type}, {map}:{start}->{goal}, range {n}
  Cache: {resident/lazy/miss/fingerprint}
  Evidence: {PathRecord|PathCacheStats|test|benchmark}
```

## Verification

- Cover open terrain, obstacle detour, moving goal, unreachable goal, and the
  relevant walker capability.
- Verify cache miss/fingerprint/eviction behavior when caches changed.
- Compare before/after solved count and failed-route cost for tuning work.
- Report focused tests and benchmarks separately from unmeasured reasoning.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-pathfinding`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-pathfinding` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- When present, read `dev-docs/pathfinding.md` for architecture, commands, formats, and current
  tuning evidence.
- Load `modernuo-server-lifecycle` for prompt/prebake phase changes,
  `modernuo-threading` for main-loop constraints, and
  `modernuo-spatial-range-geometry` for exact bounds semantics.
