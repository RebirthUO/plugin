---
name: modernuo-events
description: Use when subscribing to, handling, or defining ModernUO EventSink or
  generated events, including connection, speech, movement, combat, world, death,
  or deletion hooks. Covers event choice, signatures, lifetime, pooling, cleanup,
  and tests. Do not use for calendar schedules or short delayed callbacks.
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Events

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own game/lifecycle event surfaces. Calendar recurrence belongs to an available
local scheduler workflow; elapsed callbacks belong to timers. Legacy conversion
uses an available local migration workflow.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Define the producer, subscriber, exact semantic moment, payload, cancellation/handled behavior, lifetime, ordering, frequency, and failure policy.
2. Read [event-surfaces.md](references/event-surfaces.md), then inspect the actual local event declaration, invoker, and nearest subscriber. Never choose an event by name alone.
3. For process-lifetime static EventSink handlers, subscribe deterministically in `Configure()`. For instance, reloadable, temporary, or disableable systems, store ownership and unsubscribe.
4. Use `[OnEvent]` only for an existing/generated event contract; do not also add a manual EventSink subscription.
5. Match the exact signature, validate payload/entity state, honor handled/blocked semantics, and keep the handler bounded on the game loop.
6. If defining an event, prefer the repository's generated-event/pooling conventions and document invocation ownership and ordering.
7. Test registration once, event firing, filters, handled/cancel flow, disable/unsubscribe, deletion/stale payload, and repeated initialization.

## Safety gates

- Connection, disconnect, logout, death, deletion, world save, and shutdown are not interchangeable cleanup points.
- Do not retain pooled EventArgs or other borrowed payload state after the callback.
- If code creates pooled args manually, return them on every path, including exceptions.
- Event handlers must not block, start unsafe background game logic, or scan the full world without a bounded reason.
- Make side effects idempotent when an event can fire more than once.

## Verification/self-check

Prove registration count, semantic firing point, filters/handled behavior, pooled cleanup, disable/unsubscribe, and duplicate delivery. Re-read the actual declaration/invoker rather than relying on the event map.

## Output contract

Return selected event and semantic rationale, subscription/invocation changes, lifetime and cleanup owner, changed files, verification results, and ordering or coverage risks.

## Reference routing

- Always read [event-surfaces.md](references/event-surfaces.md).
- For lifetime or startup/shutdown ambiguity, use an available local lifecycle
  workflow; otherwise inspect the current source directly and state the limit.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-events`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-events` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
