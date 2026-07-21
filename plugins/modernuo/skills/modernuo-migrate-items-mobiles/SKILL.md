---
name: modernuo-migrate-items-mobiles
description: Migrate an existing RunUO Item, Mobile, or BaseCreature subclass to a specific ModernUO repository revision while coordinating construction, serialization, timers, properties, ownership, deletion, and player-visible behavior. Use for whole-entity migrations; use narrower migration skills for isolated persistence, timer, tooltip, or UI work.
---

# RunUO to ModernUO Item and Mobile Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require complete source types and callers, one explicit ModernUO repository and revision, supported save versions, intended era and behavior, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and applicable schema/build/test facilities. Treat official OSI/EA/Broadsword material as the only authority for gameplay; label repository, client, and emulator observations separately.

Return `BLOCKED_INPUT` when scope or compatibility requirements are missing, `BLOCKED_EVIDENCE` when save identity, ownership, era, or gameplay behavior cannot be established, and `VALIDATION_FAILED` for failed required checks. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory constructors, type identity, every saved field/version, command properties, timers, owned entities, deletion hooks, tooltips, context menus, loot, AI, taming, and era gates.
2. Select the exact mode through [modernuo-migrate-serialization](../modernuo-migrate-serialization/SKILL.md) before removing manual readers or `Serial` constructors.
3. Apply only generator, construction, property, context-menu, and lifecycle patterns verified in the target revision.
4. Route timers through [modernuo-migrate-timers](../modernuo-migrate-timers/SKILL.md) and tooltips through [modernuo-migrate-property-lists](../modernuo-migrate-property-lists/SKILL.md). Restore runtime state only after load and cancel owned state on deletion.
5. Mutate generated persistent properties rather than backing fields; never serialize runtime handles.
6. Preserve stats, skills, combat, loot, economy, access, taming, names, and era behavior unless explicitly authorized by official evidence or a labeled custom policy.
7. Run schema generation when required, build, and test construct/add, save-load for every supported version, properties, timer cleanup, deletion, ownership, and visible behavior.

## Result contract

This skill owns the top-level result; embed narrower skill outputs as evidence and propagate their blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` including serialization/identity and lifecycle ownership; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires full inventory reconciliation, compatible supported saves, lifecycle coverage, and passing checks.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE` for narrow/unrelated work, `BLOCKED_INPUT` for missing artifacts/access, `BLOCKED_COMPATIBILITY` for unresolved save/behavior/overlap decisions, `BLOCKED_EVIDENCE` for insufficient proof, `VALIDATION_FAILED` after a failed implementation check, then the mode success state. Map sibling blockers to the matching parent state and embed ready sibling evidence. Use confidence `high` only for direct authoritative or revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, types/callers, saves, era, and mode; `# Checklist` records each inventory category; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, manual checks, recovery input, or `None`.

Trace every persistent field and runtime resource, verify base-call ordering locally, distinguish facts from assumptions, and never represent unresolved old-save or gameplay behavior as complete.
