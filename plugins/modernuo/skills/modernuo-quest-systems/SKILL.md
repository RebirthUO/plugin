---
name: modernuo-quest-systems
description: 'Use when creating, reviewing, or changing ModernUO quest systems, quest offers, conversations, objectives, rewards, restart or cancellation behavior, or quest-owned state. Do not use for a standalone item, mobile, gump, region, or timer change that has no quest lifecycle.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Quest Systems

## Boundary

Own the quest lifecycle across offer, acceptance, progress, objective
completion, rewards, cancellation, restart, and durable quest state. Keep a
standalone UI, entity, region, timer, or serialization concern with its narrow
owner unless it changes that lifecycle.

## Required Context

Confirm the consuming checkout, its pinned revision, the requested player
outcome, the quest entry point, the state owner, and the available validation
surface. Return `BLOCKED` with the smallest missing input; do not infer APIs,
save formats, or player-facing mechanics.

## Workflow

1. Read [quest workflow guidance](references/quest-workflow.md) when mapping a
   lifecycle or selecting source anchors.
2. Map every transition: offer, accept, objective progress, completion,
   reward, cancellation, restart, deletion, and load restoration.
3. Name the owner of each state value and prove idempotence for repeated or
   stale actions before changing rewards or completion.
4. Separate production gameplay requirements from local implementation facts.
   Obtain player-facing rules from `uo-official-evidence` when they are not
   supplied as an approved custom policy.
5. Hand off UI layout to `modernuo-gump-system`, entity fields to
   `modernuo-serialization`, cleanup to `modernuo-lifecycle-cleanup`, and
   focused assertions to `modernuo-regression-testing`.
6. Verify normal completion, denial, cancellation, stale response, repeat,
   restart, and save/load paths independently.

## Guardrails

- Never grant a reward twice after reconnect, replay, delayed callback, or
  stale UI action.
- Preserve validated eligibility and ownership checks at every transition.
- Treat objective text, rewards, progression gates, and era behavior as
  gameplay claims, not as facts inferred from local code.
- Do not make a generic content change own global quest policy.

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

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT`. Return one fenced
`yaml` document containing `Outcome`, `Repository revision`, `Decision`,
`Evidence`, `Verification`, `Confidence`, and `Limitations`. Record lifecycle
transitions and state ownership as separate decision records.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Check each lifecycle transition and reward idempotence.
- Check save/load or other durable-state restoration when state changes.
- Run the smallest focused test/build surface and report unrun checks.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-quest-systems` before publishing a skill change.
