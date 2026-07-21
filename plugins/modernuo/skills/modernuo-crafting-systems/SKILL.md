---
name: modernuo-crafting-systems
description: 'Use when creating, reviewing, or changing ModernUO crafting systems, recipes, resources, tools, quality, maker marks, repair, resmelting, or bulk-order integration. Do not use for an isolated craftable item when no crafting workflow changes.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Crafting Systems

## Boundary

Own recipe-driven crafting workflows and their resource, tool, quality, repair,
resmelting, and bulk-order interactions. Keep a standalone item or UI concern
with its narrow owner unless it changes the crafting contract.

## Required Context

Confirm the consuming checkout, revision, requested craft action, resource and
tool rules, output state, and available validation surface. Return `BLOCKED`
for a missing behavior contract or source anchor.

## Workflow

1. Read [crafting workflow guidance](references/crafting-workflow.md) for a
   multi-surface request.
2. Map the action from entry point through eligibility, resource selection,
   consumption, result selection, quality, maker mark, delivery, and feedback.
3. Identify which mutations are atomic and which failure paths must leave
   resources, tool uses, and result state unchanged.
4. Treat recipe values, success rates, rewards, and era gates as gameplay
   claims; obtain official evidence or an approved custom policy before
   choosing them.
5. Hand off pure UI layout to `modernuo-gump-system`, item persistence to
   `modernuo-serialization`, tooltip-only work to `modernuo-property-lists`,
   and focused tests to `modernuo-regression-testing`.
6. Verify success, failure, insufficient resources, invalid tool, capacity,
   exceptional quality, repair, and repeat execution.

## Guardrails

- Never consume resources or uses on a rejected action unless the confirmed
  contract requires that cost.
- Preserve current validation order when it protects duplication or loss.
- Do not infer player-visible rates or rewards from source code.
- Keep bulk-order policy separate unless the request changes its integration.

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
Record each resource, output, and failure-path contract separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Exercise success and every resource/tool rejection branch.
- Verify output and source inventory state before and after each branch.
- Run focused tests/builds and report any unavailable runtime check.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-crafting-systems` before publishing a skill change.
