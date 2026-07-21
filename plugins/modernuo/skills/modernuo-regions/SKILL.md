---
name: modernuo-regions
description: 'Use when creating or changing ModernUO static or dynamic regions, dungeon
  or town sub-zones, travel/housing/spawn rules, region JSON, parent inheritance,
  or region lifecycle. Do not use for range-query geometry alone; route that to modernuo-spatial-range-geometry.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Regions

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own spatial rule inheritance, JSON/type registration, travel and housing policy,
dynamic register/unregister behavior, and world-load restoration. Exact AoE/range
math belongs to `modernuo-spatial-range-geometry`; object cleanup details belong
to `modernuo-lifecycle-cleanup`.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Record the map, bounds, Z semantics, parent region, base class, priority,
   affected hooks, era gate, and staff behavior.
2. Prefer an existing region type. For JSON-defined regions, verify type
   registration and schema shape; for dynamic regions, derive the parent from
   `Region.Find(location, map)` unless isolation is intentional.
3. Override only the behavior that differs and preserve parent delegation/base
   calls unless the rule intentionally blocks it.
4. For item/controller regions, centralize replacement: unregister the old
   region, validate owner/map, create and register one replacement.
5. Invoke replacement on location/map/enable changes and unregister on deletion.
   Restore only after the required world/map/parent state is available.
6. Test inside/outside boundaries, parent inheritance, travel/housing policy,
   movement/recreation, deletion, and save/load.

## Guardrails

- Choose the semantic base: `BaseRegion` for general rules, `DungeonRegion` for
  dungeon defaults, `GuardedRegion`/`TownRegion` for guards, and existing
  no-travel/no-housing variants when they already express the rule.
- Dynamic regions must never double-register or leave the old instance active.
- Use deferred `[AfterDeserialization(false)]` for cross-world dependencies;
  add a zero-delay timer only when the current repository pattern requires a
  further tick boundary.
- Travel/spell restrictions normally preserve the established staff bypass.
- `Region.Find(point, map)` is suitable for gameplay; `Region.Find(name, map)` is
  a linear lookup for startup/config/admin paths.
- Housing, travel, spawn, combat, and facet changes are gameplay changes; keep
  their source/era decision explicit.

## Output Contract

Return the region type/base, map/area/parent, changed hooks, lifecycle table,
player/staff behavior, era/source decision, and verification. Review findings
must identify whether the risk is a ghost region, lost parent rule, hot lookup,
or incorrect spatial policy.

## Verification

- Boundary tiles and parent inheritance behave as intended.
- Register/unregister is exactly once across move, map change, disable, delete,
  and load.
- Travel, housing, spawn, and staff cases are tested independently where changed.
- Focused tests/build and any in-game smoke check are reported separately.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-regions`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-regions` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [dynamic and JSON region patterns](references/dynamic-region-patterns.md)
  when selecting a base, parent, lifecycle hook, or JSON registration.
- Load `modernuo-lifecycle-cleanup` for owned-resource cleanup,
  `modernuo-serialization` for load hooks, and `uo-official-evidence` for
  player-facing production world/era policy.
- When present, read `dev-docs/regions.md` for the current hook and type inventory.
