---
name: modernuo-migrate-persistence
description: Replace existing RunUO WorldSave or WorldLoad handlers and custom binary files with GenericPersistence APIs verified in a specific ModernUO repository revision. Use for global non-entity state, schema and version preservation, dirty tracking, legacy migration, rollback, and post-load restoration. Use entity serialization migration for Item or Mobile fields.
---

# RunUO to ModernUO Persistence Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require all legacy readers/writers and data files or fixtures, one explicit ModernUO repository and revision, supported save versions, compatibility and rollback requirements, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and applicable build/test facilities. Route entity fields to [modernuo-migrate-serialization](../modernuo-migrate-serialization/SKILL.md).

Return `BLOCKED_INPUT` for incomplete legacy artifacts or requirements, `BLOCKED_EVIDENCE` for unknown field order/version/identity, and `VALIDATION_FAILED` for generator, build, or test failures. Preserve data and stop on corruption or unsupported versions; do not silently skip, reinterpret, delete, or quarantine data without explicit project policy. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory file paths, version encoding, exact write/read order and types, references, mutations, missing/corrupt behavior, and startup/save hooks.
2. Inspect a current local `GenericPersistence` implementation and exact reader/writer, registration, dirty, and post-load APIs at the target revision.
3. Define a stable name and versioned contract. Preserve a tested legacy reader or an explicit one-time migration plus backup and rollback boundary.
4. Replace file management and old hooks only after the new registration and legacy path are proven.
5. Handle deleted/null references explicitly, call `MarkDirty()` for every persistent mutation, and rebuild runtime-only state only in the verified post-load phase.
6. Test empty/missing state, every supported legacy version, current round trip, unsupported/corrupt data, deletion/null references, and dirty/no-dirty saves.

## Result contract

This skill owns the top-level result; embed serialization results as evidence and propagate its blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with schema/version and dirty/runtime ownership; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires tested legacy/current paths, rollback evidence, and no unresolved schema claim.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map sibling blockers and embed ready evidence. Use confidence `high` only for direct schema/revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, files, versions, rollback, and mode; `# Checklist` covers schema, references, dirty tracking, runtime state, rollback, and tests; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, recovery input, or `None`.

Read the schema again in write order, cite revision/path/symbol evidence, prove backup and rollback before old-code removal, and distinguish verified facts, decisions, and unresolved assumptions.
