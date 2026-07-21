---
name: modernuo-faction-systems
description: 'Use when creating, reviewing, or changing ModernUO faction systems, membership, ranks, elections, towns, guards, faction items, sigils, faction UI, or faction-owned persistence. Do not use for a standalone PvP rule or generic vendor change that has no faction contract.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Faction Systems

## Boundary

Own coordinated faction state across membership, rank, town, election, guards,
items, rewards, UI, scheduled behavior, and durable restoration. Keep generic
region, vendor, timer, or gump work with its narrow owner unless it changes
faction policy or state.

## Required Context

Confirm the consuming checkout, revision, requested faction behavior, affected
state owner, authority rules, player-facing policy source, and validation
surface. Return `BLOCKED` when a material contract is absent.

## Workflow

1. Read [faction workflow guidance](references/faction-workflow.md) when a
   request crosses state owners.
2. Map the primary state, derived state, controller/item/mobile ownership,
   authorization, UI, scheduled action, and persistence surfaces.
3. Define transition invariants for join/leave, election, rank, town, and item
   state before editing a consumer.
4. Obtain official evidence for player-facing rules, values, and era behavior
   unless an approved custom policy explicitly supplies them.
5. Hand off generic UI to `modernuo-gump-system`, region policy to
   `modernuo-regions`, recurring work to `modernuo-timers`, entity/global
   persistence to `modernuo-serialization`, and vendor mechanics to
   `modernuo-vendor-systems`.
6. Verify authorization, state transition, repeated action, offline/load,
   scheduled, and teardown paths.

## Guardrails

- Do not permit one faction action to mutate another owner's state implicitly.
- Preserve eligibility and authorization checks at every entry and UI response.
- Treat production faction mechanics as unresolved without official evidence.
- Make controller, item, mobile, and persisted-state teardown idempotent.

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
Record each state owner and transition invariant separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Test authorized and rejected transitions plus repeated UI/command actions.
- Test offline, deletion, timer, and restoration behavior where applicable.
- Run focused tests/builds and state any unavailable integration check.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-faction-systems` before publishing a skill change.
