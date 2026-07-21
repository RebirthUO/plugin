---
name: modernuo-vendor-systems
description: 'Use when creating, reviewing, or changing ModernUO vendor systems, buy or sell flows, inventory, restocking, stock rules, prices, player-vendor interactions, or commerce-facing validation. Do not use for a standalone mobile, item, or faction change that has no vendor or transaction contract.'
license: MIT
metadata:
  version: 1.0.0
---

# ModernUO Vendor Systems

## Boundary

Own vendor transaction and inventory workflows: eligibility, listings,
selection, price, stock, transfer, restock, cancellation, feedback, and durable
state. Keep an unrelated mobile, item, gump, faction, or generic economy policy
with its narrow owner.

## Required Context

Confirm the consuming checkout, revision, vendor type, transaction direction,
inventory/currency owners, failure behavior, player-facing policy source, and
validation surface. Return `BLOCKED` if a transaction contract is missing.

## Workflow

1. Read [vendor workflow guidance](references/vendor-workflow.md) before
   changing a multi-step transaction.
2. Map the transaction from eligibility through quote, affordability, stock
   reservation, transfer, currency mutation, inventory mutation, and feedback.
3. Specify the atomicity boundary and recovery behavior before changing price or
   stock logic.
4. Obtain official evidence for player-facing price, limits, restock, and era
   rules unless an approved custom policy supplies them.
5. Hand off UI to `modernuo-gump-system`, NPC/entity behavior to
   `modernuo-content-patterns`, faction-scoped behavior to
   `modernuo-faction-systems`, and durable state to `modernuo-serialization`.
6. Verify successful purchase/sale, affordability, capacity, stale stock,
   cancellation, repeated action, restock, and restoration paths.

## Guardrails

- Never mutate currency and inventory independently without a confirmed
  recovery contract.
- Revalidate stock, price, ownership, and capacity at commitment time.
- Do not infer player-facing commercial policy from local code.
- Preserve explicit staff and player-vendor authorization behavior.

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
Record quote, stock, currency, transfer, and recovery decisions separately.

## Verification

- Run a plugin-local validator only when its command and package path are
  present; otherwise record the exact unavailable command as `not-run`.

- Test every commitment/rejection branch with before/after inventory and
  currency state.
- Test stale UI/stock and duplicate-action behavior.
- Report focused tests/builds and integration-smoke limitations separately.
- Run `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-vendor-systems` before publishing a skill change.
