---
name: modernuo-lifecycle-cleanup
description: 'Use when implementing or reviewing ModernUO object-lifetime cleanup
  for timers, event subscriptions, dynamic regions, owned entities, callbacks, and
  restored runtime state. Do not use for timer API choice alone or server startup/shutdown;
  route those to modernuo-timers or modernuo-server-lifecycle.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Lifecycle Cleanup

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own the lifetime match between an item, mobile, or system and every runtime
resource it creates or retains. The result must prevent callbacks against
deleted objects, ghost regions, event leaks, orphaned children, stale reverse
references, and duplicate restoration after world load.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Inventory each timer/token, event hook, region, owned entity, cache, and
   forward/reverse reference. Name its owner and intended lifetime.
2. Inspect base and neighboring implementations before choosing `OnDelete()`,
   `OnAfterDelete()`, or their base-call position.
3. Stop active behavior, unregister external state, delete or release owned
   objects once, and clear reusable references or collections.
4. Make delayed callbacks validate owner, target, map, connection, and ownership
   conditions that can change independently.
5. Persist only durable state. Recreate runtime-only state once in
   `[AfterDeserialization]`; use `[AfterDeserialization(false)]` when other
   entities must be loaded or the hook may mutate world state.
6. Exercise deletion, pending-callback, and save/load transitions appropriate to
   the change.

## Guardrails

- Cancel `TimerExecutionToken` with `Cancel()` and legacy `Timer` objects with
  `Stop()`. Never mark a token `[SerializableField]`.
- Prefer early cancellation in `OnDelete()` when a callback could observe
  partially deleted state. Use `OnAfterDelete()` for owned-object cascades,
  region unregister, and external-reference cleanup when the hierarchy expects
  deletion to have completed.
- Unregister dynamic regions before delete/disable/replacement; unsubscribe
  temporary instance events while leaving intentional process hooks intact.
- Clear both sides of relationships, give each child one deletion owner, and
  validate independently mutable callback targets even after cancellation.

## Output Contract

For implementation, return the changed paths plus an ownership table naming the
resource, owner, cleanup hook, restoration hook, and verification. For review,
report findings as:

```text
[LIFECYCLE] {ERROR|WARN|INFO}: {issue}
  File: {path}:{line}
  Resource/owner: {resource} / {owner}
  Risk: {deleted callback|leak|ghost region|duplicate restore|stale reference}
  Check: {focused test or smoke transition}
```

## Verification

- Delete the owner while delayed work is pending; no callback acts afterward.
- Owned entities and dynamic regions disappear exactly once.
- Save/load restores active runtime state once and never serializes tokens.
- Event and reverse-reference cleanup prevents later retention or invocation.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-lifecycle-cleanup`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-lifecycle-cleanup` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [cleanup resource matrix and hook patterns](references/cleanup-resource-matrix.md)
  when selecting hooks or reviewing mixed resource ownership.
- Load `modernuo-timers`, `modernuo-events`, `modernuo-regions`, or
  `modernuo-serialization` only for the corresponding API details.
- When present, read `dev-docs/content-patterns.md` and the matching timer/event/region/
  serialization developer doc when repository behavior is uncertain.
