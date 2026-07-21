---
name: modernuo-spatial-range-geometry
description: 'Use when proving exact ModernUO tile coverage for GetMobilesInRange,
  GetItemsInRange, GetClientsInRange, Get*InBounds, AoE radii, rings, or Rectangle2D
  conversions. Do not use for path-search behavior or region policy; route those to
  modernuo-pathfinding or modernuo-regions.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Spatial Range Geometry

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Prove the coordinate set selected by a range/bounds call before changing gameplay.
For the standard centered range conversion, range `N` is a 2D Chebyshev radius:
`[x-N, x+N] x [y-N, y+N]`, a `(2N+1) x (2N+1)` box including the source tile
before gameplay filters.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Trace the exact current call from the spell/ability/system into the map
   enumerator; do not infer semantics from the method name.
2. Inspect the range-to-`Rectangle2D` conversion. Confirm width/height and the
   half-open `Contains` rule (`start` inclusive, `end` exclusive).
3. Check whether `makeBoundsInclusive` or a custom bounds overload modifies the
   rectangle. Account for that call site explicitly.
4. Separate spatial membership from gameplay filters such as source exclusion,
   LOS, Z, alive/harmful/team checks, and era gates.
5. Translate source wording as radius, diameter, ring, rectangle, or another
   metric. Resolve contradictory prose with a concrete numerical example and
   state the chosen source.
6. Add boundary tests for cardinal and diagonal points at `N`, just outside `N`,
   source inclusion, and any custom inner/outer ring or Z filter.

## Guardrails

- Range `0` is `1x1`; `1` is `3x3`; `3` is `7x7`, not `3x3`.
- The `+1` in `2N+1` represents the source coordinate, not padding.
- Default range queries are Chebyshev, not Manhattan or Euclidean; a diagonal
  offset `(N,N)` is inside.
- Standard mobile/item range enumeration is 2D. Do not claim vertical filtering
  unless the caller adds it.
- `makeBoundsInclusive` is a separate expansion convention; never mix it into the
  default centered-range result.
- Community/source numbers can conflict. Cite which value and era/ruleset the
  implementation follows.

## Output Contract

Return the call chain, input value, rectangle start/end and inclusivity, metric,
dimensions/tile count, source inclusion, post-query filters, source/era, and
verification. For a code change, include before/after coverage.

Emit each geometry proof as one `Decision.records` entry with `kind: geometry-proof`; put the call chain, coordinate bounds, inclusivity, metric, tile count, filters, and before/after coverage in `details`. This is the single source for any optional human-readable table.

## Verification

- Test cardinal and diagonal boundary coordinates plus one coordinate outside.
- Confirm default/custom inclusivity and source filtering independently.
- Inspect current repository implementations rather than relying on remembered
  line numbers.
- Run the focused owning test/build or label a static geometry proof as such.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-spatial-range-geometry`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-spatial-range-geometry` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [range verification chain and worked cases](references/range-verification.md)
  when translating a specification or auditing a custom bounds path.
- Load `modernuo-pathfinding` for route search, `modernuo-regions` for spatial
  policy, and `modernuo-performance-hot-paths` for query cost.
