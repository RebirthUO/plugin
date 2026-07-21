---
name: modernuo-migrate-systems
description: Coordinate migration of an existing multi-file RunUO engine or system with interdependent entities, persistence, commands, gumps, packets, configuration, timers, or lifecycle hooks to a specific ModernUO repository revision. Use for dependency mapping, vertical slices, contract preservation, integration ordering, verification, and rollback. Do not use for one isolated class or subsystem.
---

# RunUO to ModernUO Multi-File System Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require the complete source scope and entry points, one explicit ModernUO repository and revision, source/target versions, intended behavior and era, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), mutation authorization, baseline failures, test facilities, and a feasible rollback boundary. Treat official OSI/EA/Broadsword material as the only gameplay authority and label repository evidence separately.

Return `BLOCKED_INPUT` for missing scope, authority, tests, or rollback, `BLOCKED_EVIDENCE` for unresolved contracts or ownership, `BLOCKED_COMPATIBILITY` when a failed slice requires rollback or a compatibility decision, and `VALIDATION_FAILED` for failed required checks. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Produce a complete file/symbol inventory and dependency graph covering data, saved state, entities, UI, commands, packets, configuration, events, timers, tests, and entry points.
2. Record external contracts: saved identities/versions, keys, commands/access, packet IDs, data files, visible behavior, and era gates with provenance.
3. Assign each node to a verified installed `modernuo-migrate-*` capability or local repository evidence. Stop on missing mandatory ownership; never guess a similarly named skill.
4. Choose vertical slices with independent rollback. Prefer data types, persistence, entities, runtime services, UI/commands/packets, then startup where dependencies allow and record every ordering reason.
5. For each slice, inspect current local precedent, implement only in `implement` mode, validate, and stop before the next slice on failure.
6. Reconcile references, registration order, idempotent startup/cleanup, old-save migration, excluded files, and deferred dependencies.
7. Run slice tests, owning-project integration, save/restart, enable/disable, and failure/rollback tests.

## Result contract

This skill owns the top-level result; embed subsystem-skill results as evidence and propagate every blocker or failed check. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with dependency graph, ownership, and slices; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk` including rollback state. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires every node and contract reconciled and all checks passing.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map every subsystem blocker and embed ready evidence. Use confidence `high` only for direct authoritative/revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, system boundary, versions, behavior, rollback, and mode; `# Checklist` covers every graph category; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, deferred nodes, rollback/recovery input, or `None`.

Explain every excluded or deferred dependency, separate baseline from migration failures, verify no duplicate entry point remains, and never call a partially migrated system complete.
