---
name: modernuo-item-properties
description: Use when reviewing, planning, implementing, or auditing a ModernUO-based item property that needs aligned gameplay mechanics, Object Property List output, storage, expansion gating, persistence, and focused verification. Use modernuo-property-lists for tooltip-formatting-only work and uo-official-evidence for player-facing gameplay research before a property contract exists.
---

# ModernUO Item Properties

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own the complete server behavior of a requested item property: its storage,
mechanics, tooltip, era gate, persistence, and tests. Do not treat a
player-facing gameplay claim as established by implementation code; route that
claim through `uo-official-evidence`. Formatting-only work belongs to
`modernuo-property-lists`.

## Required Context

Inspect the consuming repository's instructions, exact revision, dirty state,
item hierarchy, property-list interface, and owning test project. Establish the
requested property, affected item types, expected mechanics, display contract,
era, and persistence requirement. Separate implementation facts from
player-facing gameplay facts: current repository evidence can establish only
the former; the latter requires applicable official evidence or an explicitly
approved custom policy labeled as non-official. If a required fact is absent,
return `BLOCKED` with the smallest missing decision; do not invent a formula,
lifecycle, or expansion policy.

## Workflow

1. Classify the change as a display fact, passive equipped aggregate, active or
   proc effect, durability/repair rule, transfer/insurance rule,
   generation/crafting rule, or an era-gated combination. Read
   [the property workflow](references/modernuo-item-property-workflow.md).
2. Inspect the current item base class, attribute families, property emission,
   existing equivalent property, serialization pattern, and nearby tests. Read
   [property systems](references/modernuo-property-systems.md) when choosing
   storage or aggregation.
3. Reuse the narrowest established storage and aggregation mechanism. Add new
   content-level storage only when no current type owns the behavior; do not
   broaden engine-level item state without explicit authority.
4. Implement or verify mechanics before display. Keep tooltip order and cliloc
   argument shape consistent with the current base class; use
   `modernuo-property-lists` when the requested work is limited to that layer.
5. Persist only durable state. Use the repository's current generated-field and
   migration patterns, invalidate visible property lists after a displayed value
   changes, and define the load-time behavior of every durable effect.
6. Add focused tests for display and behavior. Test absence or no-effect paths,
   equipped removal for aggregates, deterministic trigger and blocked paths for
   procs, both sides of a relevant era gate, and save/load when state is new.

## Guardrails

- Prefer an existing item-specific or attribute-family type over duplicate
  fields and copied property-list code.
- Keep implementation evidence and official gameplay evidence distinct. A
  community, emulator, client, or repository source may locate a seam but never
  resolves a missing official gameplay claim.
- Do not emit a gameplay tooltip until its corresponding mechanic is present or
  the request explicitly classifies it as a non-mechanical display fact.
- Do not guess cliloc numbers, localized argument order, attribute aggregation,
  serialization indexes, or expansion gates.
- Do not claim focused tests prove broad compatibility; report the actual
  commands, denominators, revision, and limitations.

## Result Contract

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT`. Emit exactly one
fenced `yaml` document with this schema; keep values factual and use `null` or
empty lists rather than prose placeholders.

Use `REVIEWED` for a `REVIEW` or `PLAN` result, `IMPLEMENTED` only after an
authorized change with post-change evidence, and `BLOCKED` when a required
input or authority is unavailable.

```yaml
Outcome: IMPLEMENTED | REVIEWED | BLOCKED
Repository revision:
  commit: <full revision or null>
  dirty: <true | false | null>
Decision:
  kind: REVIEW | PLAN | IMPLEMENT
  summary: <single factual sentence>
  records:
    - kind: property-contract | storage | mechanics | tooltip | persistence | test-evidence
      subject: <path, symbol, or behavior>
      status: verified | proposed | blocked | not-applicable
      details: <required facts and decisions>
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

Use high confidence only with a current revision and focused post-change
verification; use low confidence for a blocker or missing required source.

## Reference Routing and Verification

- Read [source checks](references/source-checks.md) before relying on any
  player-facing gameplay claim, and [property systems](references/modernuo-property-systems.md)
  before adding storage or aggregation. If `uo-official-evidence` is unavailable,
  inspect applicable official material directly; if it remains unavailable or
  inconclusive, return `BLOCKED` rather than using a technical source as a fallback.
- Load `modernuo-serialization`, `modernuo-era-expansion`, or
  `modernuo-test-workflow` only when their specialized concern is present and
  the sibling is available.
- Before completion, run `python scripts/validate-modernuo-skill-evals.py
  plugins/modernuo/skills/modernuo-item-properties` from the plugin root. When
  the Codex CLI runtime is available, also run `python
  scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir>
  plugins/modernuo/skills/modernuo-item-properties` and report its result plus
  `runner_sha256`; otherwise record that limitation.
