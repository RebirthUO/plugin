---
name: modernuo-serialization
description: 'Use when adding or changing ModernUO generated serialization, persistent
  fields/properties, version migrations, legacy readers, GenericPersistence, or save/load
  restoration. Treat changes as save-compatibility work; do not use for generic JSON/configuration
  serialization.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Serialization

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Persistent layout is a compatibility contract. Classify every change as a new
generated type, a generated-version transition, a pre-codegen legacy migration,
or custom/global persistence before editing.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Inspect the current class, generated attributes, migration JSON, prior
   versions, legacy read/write order, aliases, timers, and custom setters.
2. For a new generated type, use a `partial` class and version `0`; add
   `[Constructible]` when the content is intended for the in-game add command.
3. For an existing generated type, preserve field indexes, bump the generator
   version for layout changes, create the previous-version migration content,
   and generate/commit the schema with the repository's migration command.
4. For pre-codegen data, preserve the exact old read order and encoded/plain
   version format in the legacy deserializer; do not use that path for normal
   post-codegen bumps.
5. Persist durable state only. Restore timers, caches, registrations, and derived
   state in the appropriate after-deserialization hook.
6. Build the owning project immediately, inspect generated/schema output, and run
   old-save/default/new-round-trip coverage proportional to risk.

## Guardrails

- `[SerializableField(N)]` indexes are save-format contracts; never reorder or
  reuse one casually.
- Custom serialized-property setters must call `this.MarkDirty()` and invalidate
  properties when visible tooltip state changes.
- Never serialize `TimerExecutionToken`. Persist deadline/state and restart on
  load; cancel the runtime token on deletion.
- Custom `Serialize()` may run on background serialization workers. It must only
  read stable fields and write the stream: no entity mutation/deletion, timers,
  packets, `NetState`, or shared mutable state.
- Use synchronous `[AfterDeserialization]` only for own-state restoration. Use
  `false` when other entities must exist or the hook may delete/register/mutate
  world state.
- Build immediately around high field/save-flag indexes; generated flag types
  can expose representation mismatches. Prefer no flag when defaults are safe.

## Output Contract

Return the change classification, version/field map, compatibility path,
generated/migration artifacts, runtime restoration/cleanup, tests, and rollback
risk. State missing old-save evidence.

## Verification

- New/default values, round trip, previous generated version, and legacy stream
  are covered as applicable.
- Migration schema exists and matches indexes/save flags.
- Generated code and the owning solution/project compile.
- Timer/runtime state restores once and delete/load transitions stay safe.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-serialization`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-serialization` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [generated fields, migrations, and persistence patterns](references/serialization-migrations.md)
  for attribute selection, schema generation, and legacy examples.
- Load `modernuo-migrate-serialization` for RunUO/manual-to-generated conversion,
  `modernuo-timers` for time-based state, and `modernuo-property-lists` for
  generated tooltip invalidation.
- Consult `dev-docs/serialization.md` and the current ModernUO serialization docs
  before relying on remembered generator behavior.
