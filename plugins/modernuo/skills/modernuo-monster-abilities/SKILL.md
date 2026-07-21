---
name: modernuo-monster-abilities
description: 'Use when adding, migrating, or reviewing reusable ModernUO-based creature
  combat specials implemented as MonsterAbility classes. Do not route boss phase orchestration
  or WeaponAbility work here; keep those in encounter code or the weapon-ability system.

  '
license: MIT
metadata:
  version: 1.2.0
---

# ModernUO Monster Abilities

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Combat procs, debuffs, counters, breaths, area effects, and summons-on-hit belong
in reusable classes under `Projects/UOContent/Mobiles/Abilities/`. A creature
should normally only expose them through `GetMonsterAbilities()`. Keep encounter
phases, altar/retinue ownership, and HP-threshold orchestration with the owning
encounter. `WeaponAbility` remains a separate engine slot.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Search the creature for `GetMonsterAbilities()`, `GetWeaponAbility()`, and
   inline combat hooks such as `OnGaveMeleeAttack`, `OnGotMeleeAttack`,
   `OnDamagedBySpell`, `OnDamage`, and `OnHarmfulSpell`.
2. Classify the behavior as reusable combat special, weapon ability, or encounter
   orchestration before moving code.
3. Reuse an existing ability or select the narrowest base class. Keep tunable
   constants, trigger, chance, cooldown, targeting, and effect ownership on the
   ability.
4. Add a `MonsterAbilityType` value only when typed lookup is needed; register the
   ability in `MonsterAbilities.cs`, then wire the creature.
5. Preserve era gates, target eligibility, damage/debuff semantics, and cooldown
   tracking. Do not manually dispatch logic already reached by trigger flags.
6. Add focused tests for creature registration and the player-visible effect.

## Guardrails

- Call `base.Trigger(...)` where the selected base contract records cooldown.
- Parameterize shared effects instead of cloning one class per creature.
- Debuff/helper items must use ModernUO serialization, cancel owned timers on
  deletion, and restore or delete transient state safely after load.
- Use spatial queries and pooled collections on area-effect hot paths; do not scan
  `World.Mobiles` or add allocating LINQ chains.
- An absent registration does not prove a missing special: record discovered
  inline hooks as migration candidates before changing behavior.
- Audit both `MonsterAbility` and `WeaponAbility`; a creature may use both.

## Output Contract

Implementation output names the ability class, base/trigger, registry and creature
wiring, preserved source behavior, tests, and any inline-hook follow-up. Review
output names the exact path/line, architecture mismatch, gameplay risk, and
focused verification.

## Verification

- Creature exposes the expected ability without duplicate inline dispatch.
- Chance, cooldown, target filters, era gate, and effect values are exercised.
- Helper items clean timers and do not survive load incorrectly.
- The owning project builds and focused ability tests pass; label any remaining
  runtime/manual check explicitly.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-monster-abilities`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-monster-abilities` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [ability bases, triggers, templates, and registry checklist](references/reference.md)
  when selecting a base class or implementing a new ability.
- Read [uo.com creature ability audit notes](references/uo-com-creature-ability-audit.md)
  only for official pet/creature ability parity research.
- For damage-hook ordering, inspect the consuming repository's current combat
  pipeline directly; load `modernuo-timers` or `modernuo-serialization` only
  when available for stateful helper items.
