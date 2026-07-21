---
name: modernuo-spell-systems
description: 'Use when creating, reviewing, or changing ModernUO spell systems, cast lifecycles, spell registration, reagents, mana or skill checks, targeting, interruption, transformations, summons, or spell effects. Do not use for a generic command, timer, or gump change with no spell behavior.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Spell Systems

## Boundary

Own the spell cast contract from invocation through validation, resource cost,
targeting, resolution, interruption, cleanup, and persistent or timed effects.
Keep non-spell UI, range math, timer mechanics, or entity serialization with
their narrow owner.

## Required Context

Confirm the consuming checkout, revision, requested spell behavior, activation
surface, resource rules, target/effect lifecycle, and validation surface.
Return `BLOCKED` for missing behavior or source evidence.

## Workflow

1. Read [spell workflow guidance](references/spell-workflow.md) for a
   lifecycle or effect request.
2. Map validation, resource commitment, target acquisition, disturbance,
   resolution, effect ownership, expiration, and cleanup.
3. Prove every target is valid at resolution time, not only at selection time.
4. Use `uo-official-evidence` for player-facing mechanics, values, reagents,
   duration, and era behavior unless an approved custom policy supplies them.
5. Hand off target framework work to `modernuo-commands-targeting`, duration
   ownership to `modernuo-timers`, geometry to
   `modernuo-spatial-range-geometry`, and cleanup to
   `modernuo-lifecycle-cleanup`.
6. Verify cast success, invalid target, interruption, resource rejection,
   repeated effect, expiry, deletion, and save/load where applicable.

## Guardrails

- Do not spend a resource or apply an effect before the confirmed commitment
  point.
- Revalidate deleted, moved, hidden, disconnected, or otherwise stale targets.
- Avoid inferring production mechanics from source or client behavior.
- Ensure timed, transformed, and summoned effects have one explicit owner.

## Result Contract

Use this exact schema: `Outcome` is `IMPLEMENTED`, `REVIEWED`, or `BLOCKED`;
`Repository revision` has `commit` and `dirty`; every `Decision.records` entry
has `subject`, `status`, `details`, and `evidence_refs`; every evidence entry
has `id`, `class`, `locator`, and `claim`; every verification entry has
`command_or_method`, `result`, and `evidence_refs`. `Confidence.level` is
`high` only with a verified revision, official/policy evidence where needed,
and executed focused checks; use `medium` for static-only evidence and `low`
for a blocker or missing required evidence. A blocked result names the smallest
missing input in `Limitations.items` and uses no guessed decision value.

Return one fenced `yaml` document with `Outcome`, `Repository revision`,
`Decision`, `Evidence`, `Verification`, `Confidence`, and `Limitations`.
Record validation, cost, target, effect, and cleanup decisions separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Test valid and invalid casts, interruption, insufficient resources, and
  effect expiry.
- Test stale-target and deletion paths when a target or effect is retained.
- Report focused tests/builds separately from an in-game smoke check.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-spell-systems` before publishing a skill change.
