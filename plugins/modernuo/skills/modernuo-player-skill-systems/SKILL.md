---
name: modernuo-player-skill-systems
description: 'Use when creating, reviewing, or changing ModernUO player skill systems, active skill use, passive skill behavior, use delays, targeting, gain behavior, prerequisites, skill-driven effects, or skill-specific validation. Do not use for a spell, craft recipe, or generic attribute change with no player-skill contract.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Player Skill Systems

## Boundary

Own player-skill behavior from activation or passive trigger through
prerequisites, targeting, delay, resolution, gain/effect, cancellation, and
restoration. Keep spell, craft, generic targeting, or entity-only work with its
narrow owner unless it changes the skill contract.

## Required Context

Confirm the consuming checkout, revision, skill action/passive behavior,
eligibility, gain/effect ownership, delay semantics, player-facing policy
source, and validation surface. Return `BLOCKED` when a material contract is
missing.

## Workflow

1. Read [player-skill workflow guidance](references/player-skill-workflow.md)
   for a behavior that spans delay, target, gain, or retained state.
2. Map the entry point, prerequisites, target acquisition, resolution-time
   validation, delay owner, effect/gain mutation, cancellation, and cleanup.
3. Define whether the action can be retried, interrupted, or restored after
   load; prove state cannot be applied twice.
4. Obtain official evidence for player-facing requirements, gain rules, values,
   and era behavior unless an approved custom policy supplies them.
5. Hand off spell behavior to `modernuo-spell-systems`, crafting to
   `modernuo-crafting-systems`, target infrastructure to
   `modernuo-commands-targeting`, and delay mechanics to `modernuo-timers`.
6. Verify eligible/ineligible use, stale target, delay/retry, cancellation,
   gain/effect boundaries, and load restoration where applicable.

## Guardrails

- Do not infer player-facing skill formulas or requirements from local code.
- Revalidate retained targets and actor state at the resolution point.
- Assign one owner to every delay, retained effect, and cancellation path.
- Keep passive consumers and active-use paths consistent when they share state.

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
Record prerequisite, delay, target, mutation, and cleanup decisions separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Test eligible/ineligible, active/passive, delay/retry, stale-target, and
  cancellation cases that apply.
- Test before/after gain/effect and restored state where state changes.
- Report focused test/build and runtime-smoke evidence separately.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-player-skill-systems` before publishing a skill change.
