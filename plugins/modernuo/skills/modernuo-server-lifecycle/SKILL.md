---
name: modernuo-server-lifecycle
description: 'Use when changing or reviewing ModernUO startup/shutdown phases, ConfigurePrompts/Configure/Initialize
  ordering, CallPriority, world load/save events, networking startup, or the event
  loop. Do not use for per-entity deletion cleanup; route that to modernuo-lifecycle-cleanup.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Server Lifecycle

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own process bootstrap, reflection hook ordering, first-boot interaction, world
readiness, shutdown, and runtime-loop placement. The production sequence, not a
partial test fixture, is authoritative.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Trace the current production path through configuration load, assembly load,
   `ConfigurePrompts`, logging, serialization verification/timer setup,
   `Configure`, tile/region/world load, `Initialize`, networking,
   `ServerStarted`, and `RunEventLoop()`.
2. Classify the work by earliest safe phase:
   - `ConfigurePrompts()`: self-gated first-boot console input only.
   - `Configure()`: commands, settings, event subscriptions, and pre-world wiring.
   - `Initialize()`: work requiring tile data, regions, or loaded world entities.
   - lifecycle events: behavior tied to a completed load/save/start/stop boundary.
3. Inspect `CallPriority`, explicit calls, and neighboring hooks. Do not depend on
   reflection enumeration or same-priority order.
4. Keep prompts and their later world-dependent work separate; make headless and
   redirected-input behavior non-blocking.
5. Verify production startup behavior as well as targeted fixture tests.

## Guardrails

- `ConfigurePrompts()` runs before normal logging; use the established console
  path, self-gate, and skip redirected input. It must not touch world entities,
  regions, tile matrices, or map-dependent content.
- Do not prompt from `Configure()` or `Initialize()` where it can block services
  or interleave with runtime logging.
- Use explicit priority/calls/events when order matters; same-priority hooks have
  no reliable relative order.
- Tests may invoke only a curated startup subset. A passing fixture does not prove
  first-boot console behavior or full `Core.Setup()` ordering.
- Keep post-snapshot archive work and background serialization boundaries with
  their owning lifecycle event.

## Output Contract

Return the chosen phase, dependencies available there, ordering mechanism,
headless/test behavior, changed paths, and verification. Review findings must
name the exact phase mismatch and consequence.

## Verification

- Fresh configuration, existing configuration, and redirected/headless input do
  not block or repeat prompts.
- World/tile/region consumers run only after their dependencies are ready.
- Hook order is explicit where required.
- Targeted tests and a production startup/shutdown smoke check are distinguished.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-server-lifecycle`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-server-lifecycle` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- When present, read `dev-docs/server-lifecycle.md` before moving code between phases.
- Load `modernuo-configuration` for settings, `modernuo-events` for lifecycle
  events, `modernuo-threading` for loop/continuation behavior, and
  `modernuo-world-saves-archives` for post-snapshot backup work.
