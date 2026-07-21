---
name: modernuo-migrate-commands-events
description: Migrate existing RunUO command registrations, EventSink subscriptions, event delegates, and handler signatures to the APIs verified in a specific ModernUO repository revision. Use for startup registration, renamed connection events, generated events, or subscription cleanup. Do not use to design new commands, targets, or event APIs.
---

# RunUO to ModernUO Commands and Events

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require the RunUO source, one explicit ModernUO repository and revision, the requested mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and access to build or test evidence appropriate to that mode. Inspect the target revision's command/event declarations and every affected subscriber; never migrate a remembered API.

Return `BLOCKED_INPUT` when scope or repository identity is missing, `BLOCKED_EVIDENCE` when lifecycle or API evidence cannot select one safe mapping, and `VALIDATION_FAILED` when a required check fails. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory registration sites, handler signatures, access levels, argument checks, subscriber lifetimes, cleanup, and persistence hooks.
2. Map each source hook to a verified target symbol and record repository revision, file, and symbol evidence.
3. Register process-lifetime commands and static handlers in the target's verified startup phase. Use `[OnEvent]` only for a verified generated event and never also subscribe that handler manually.
4. Choose `Connected`, `BeforeDisconnected`, `Disconnected`, or another hook by required lifecycle semantics, not name similarity.
5. Pair reloadable, temporary, instance, or disableable subscriptions with deterministic unsubscription. Route custom global save files to [modernuo-migrate-persistence](../modernuo-migrate-persistence/SKILL.md).
6. Preserve permissions, validation, player-type checks, event-loop safety, and tested old-save paths.
7. Build and test registration, rejection, firing order, single delivery, reload/disable cleanup, and persistence handoff.

## Result contract

This skill owns the top-level result. Treat any sibling-skill result as evidence and map its blocker or failed validation to this contract; never replace these headings. Return, in order: `# Outcome` with one table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` including the hook map; `# Evidence` with `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` with `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`. Validation statuses are `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires all applicable checks to pass and no unresolved behavior decision.

## Self-check

Resolve the repository to its canonical path or URL and an immutable 40-character commit SHA before evidence collection. Select terminal states in this precedence: `OUT_OF_SCOPE` for a non-migration or excluded design request; `BLOCKED_INPUT` for missing required artifacts/access; `BLOCKED_COMPATIBILITY` for a user decision about preserved saves, behavior, or overlapping edits; `BLOCKED_EVIDENCE` when present evidence cannot prove one safe mapping; `VALIDATION_FAILED` after an attempted implementation check fails; otherwise use the mode success state. For a sibling `blocked`, use the matching parent blocker; for sibling `ready`, embed its evidence without changing the parent state.

Use confidence `high` only for direct revision-bound evidence plus every required runtime check, `medium` for indirect evidence or static-only validation, and `low` for unresolved inputs/conflicts. Outcome confidence is the lowest confidence of any material claim. `# Scope` must identify repository, full SHA, files, compatibility target, and mode. `# Checklist` uses `applicable`, `completed`, `skipped` with evidence, or `blocked`. `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`. `# Files` distinguishes proposed, changed, and finding-only paths by mode. `# Residual Risk` lists assumptions, manual checks, recovery input, or `None`.

Confirm one registration per handler, correct cleanup, current target signatures, no obsolete delegate wrappers, and evidence for every mapping. Lower confidence for indirect evidence; never call a blocked or partially verified migration complete.
