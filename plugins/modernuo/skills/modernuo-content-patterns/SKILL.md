---
name: modernuo-content-patterns
description: Use when implementing new ModernUO items, mobiles, creatures, spells,
  skill handlers, loot, context menus, or other UOContent types. Routes shared patterns;
  specialist spawner, vendor, pet, and faction behavior stays with its domain skill.
  Do not use for taxonomy, parity, or RunUO migration.
license: MIT
metadata:
  version: 1.2.0
---

# ModernUO Content Patterns

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

This is the implementation hub for new UOContent types. Use `modernuo-content-taxonomy` for classification/parity, `migrate-*` for conversion, and domain skills for spawner, vendor, pet, or Factions state.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Establish the target era/profile, player-visible behavior, authoritative evidence, non-goals, side effects, and owning content domain. For every gameplay-affecting claim, route through official OSI/EA/Broadsword evidence and record the era-scoped citation; repository code remains implementation evidence only. If era, authoritative evidence, or acceptance criteria are missing, return `BLOCKED` with `Missing input`, `Why required`, and `Resume action`.
2. Inspect the nearest current sibling implementation, its base types, registration, tests, schemas, localization, and data files. Do not guess constructor or hook signatures.
3. Select the smallest shape from [content-shapes.md](references/content-shapes.md). Type construction stays here; specialist system behavior routes outward.
4. Implement the behavior with local conventions: generated serialization for durable entities, `[Constructible]` where staff construction is intended, explicit ownership/cleanup, and bounded game-loop work.
5. Preserve economy, loot, combat, housing, PvP/PvM, and client-presentation boundaries; do not add adjacent features incidentally.
6. Add behavior-level tests for success, rejection, era gates, lifecycle, persistence, and exploit boundaries. Generate schemas when required.
7. When a local code-audit workflow is available, run
   it alongside focused tests and the owning project. Otherwise perform the
   equivalent direct current-source audit and state that the optional audit
   workflow was unavailable; distinguish automated evidence from manual
   in-game/client checks.

## Core safety gates

- Persistent state uses generated setters/dirty tracking; runtime timers and temporary effects are not serialized.
- Every timer, event subscription, owned entity, and held reference has an owner and cleanup path.
- Loot and stat values require era/source support; no placeholder balance values are presented as parity.
- Property-list arguments, clilocs, gump responses, commands, and targets follow their dedicated safety rules.
- Hot paths avoid full-world scans, blocking work, and unmeasured allocation.

## Verification/self-check

Map each acceptance criterion and non-goal to code/tests, run schema/build/focused/owning checks after the final edit, and audit lifecycle, era, and economy/client side effects. Label remaining manual checks honestly.

## Output contract

Return changed content/registration/test/schema paths, source and era decisions, behavior and non-goal summary, lifecycle/persistence map, verification commands/results, and residual manual or parity checks.

## Reference routing

- Always read [content-shapes.md](references/content-shapes.md) for the selected type.
- For a temporary weapon enchantment, read [weapon-buff-spell-pattern.md](references/weapon-buff-spell-pattern.md).
- Route spawner, vendor, controlled-pet, and Factions state to their named `uo-*` domain skills.
- Load locally available serialization, lifecycle, gump, or other domain
  workflows only when their surface exists.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-content-patterns`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-content-patterns` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
