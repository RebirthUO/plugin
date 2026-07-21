---
name: modernuo-event-scheduler
description: Use when implementing or reviewing wall-clock/calendar scheduling such
  as daily resets, weekly activities, seasonal windows, or maintenance. Covers recurrence
  selection, time zones, DST/restart policy, ownership, cancellation, and tests. Do
  not use for short game-time delays or sub-second ticks; use modernuo-timers.
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Event Scheduler

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Use EventScheduler for civil/calendar time (“Monday at 09:00”, annual seasonal window). Use an available local timer workflow for elapsed game time (“five seconds later”), combat ticks, and sub-second work.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Define the civil schedule, named time zone, recurrence/window, first-run, missed-run/catch-up, duplicate-run, disable, restart, and operator override policy.
2. Read [schedule-patterns.md](references/schedule-patterns.md) and inspect the current local scheduler/recurrence APIs plus an existing event of the same lifetime.
3. Choose the simplest recurrence that exactly expresses the requirement. Use a callback event for a simple static action and a custom event class only when state/behavior warrants it.
4. Store and cancel the returned event according to its owner. Make registration idempotent across reload/enable paths.
5. Make `OnEvent` fast and safe on the game loop; queue/batch bounded work through repository-supported mechanisms rather than blocking.
6. Test schedule calculation around time-zone conversion, DST gaps/overlaps, month/year/leap boundaries, restart/missed runs, duplicate initialization, cancellation, and disabled state.

## Safety gates

- Never rely on the host's implicit local time zone; use an explicit reviewed `TimeZoneInfo`.
- If DST gaps/overlaps, catch-up, restart, duplicate-run, or idempotency policy is unspecified, return `BLOCKED` and request that policy before implementation.
- Decide whether a seasonal end is inclusive/exclusive and how invalid month-days behave.
- Calendar scheduling has coarse granularity and is not a combat timer.
- Do not issue duplicate rewards, resets, or spawns after restart; define idempotency keys/state when side effects are not naturally idempotent.
- Persist durable progress separately when a restart must not reset event state.

## Verification/self-check

Calculate next occurrences across DST/month/year/leap/restart boundaries, verify duplicate registration and cancellation, and test idempotent side effects without sleeping on wall-clock time.

## Output contract

Return the schedule specification (zone, recurrence, window, catch-up/idempotency), owner/cancellation path, changed files, deterministic verification evidence, and remaining environment/manual clock checks.

## Reference routing

- Always read [schedule-patterns.md](references/schedule-patterns.md).
- Read an available local timer workflow if the requirement mixes calendar activation with elapsed in-event delays.
- Read an available local lifecycle workflow when ownership/disable cleanup is ambiguous.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-event-scheduler`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-event-scheduler` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
