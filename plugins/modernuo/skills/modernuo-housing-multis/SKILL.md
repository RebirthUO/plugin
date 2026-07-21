---
name: modernuo-housing-multis
description: 'Use when creating, reviewing, or changing ModernUO housing and multis, including placement, ownership, access, secure or lockdown state, structures, addons, deeds, movement, demolition, or restoration. Do not use for an isolated decorative item with no house or multi contract.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Housing and Multis

## Boundary

Own multi and housing lifecycle contracts: placement, ownership, access,
structure state, secured/locked-down contents, addons and deeds, movement,
demolition, and restoration. Keep standalone region, item, UI, or geometry work
with its narrow owner unless it changes that contract.

## Required Context

Confirm the consuming checkout, revision, requested ownership/policy behavior,
affected state, placement or movement rules, and validation surface. Return
`BLOCKED` for a missing policy or source anchor.

## Workflow

1. Read [housing and multis guidance](references/housing-multis-workflow.md)
   before changing lifecycle or ownership behavior.
2. Map placement, owner/access authorization, state mutation, visible
   structures, contents, teardown, and post-load restoration.
3. Identify the owner and deletion path for every component, addon, deed,
   secured item, and retained mobile/item reference.
4. Use `uo-official-evidence` for player-facing placement, access, decay,
   storage, and era policy unless an approved custom policy supplies them.
5. Hand off exact boundary math to `modernuo-spatial-range-geometry`, region
   policy to `modernuo-regions`, cleanup to `modernuo-lifecycle-cleanup`, and
   entity fields to `modernuo-serialization`.
6. Verify authorization, placement failure, movement, component consistency,
   deletion, and save/load restoration.

## Guardrails

- Never leave orphan components, secured references, or stale access state.
- Treat ownership and staff bypass behavior as explicit policy decisions.
- Do not infer player-facing housing limits or placement rules from local code.
- Ensure demolition and deletion are safe when content was already removed.

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
Record policy, ownership, component, and restoration decisions separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Test authorized and unauthorized actions plus placement rejection.
- Test movement, deletion/demolition, orphan cleanup, and save/load.
- Report focused test/build and runtime smoke evidence separately.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-housing-multis` before publishing a skill change.
