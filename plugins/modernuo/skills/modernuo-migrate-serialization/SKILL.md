---
name: modernuo-migrate-serialization
description: Migrate existing RunUO Serialize and Deserialize methods, Serial constructors, Constructable attributes, saved fields, or generated schemas to serialization APIs verified in a specific ModernUO repository revision. Use for new generated types, generated version bumps, legacy readers, TypeAlias identity, dirty tracking, and post-load restoration. Use persistence migration for global files.
---

# RunUO to ModernUO Serialization Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and mode gate

Require complete legacy write/read code, one explicit ModernUO repository and revision, all supported save versions and type identities, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and applicable schema/build/test facilities. Route global files to [modernuo-migrate-persistence](../modernuo-migrate-persistence/SKILL.md).

Select exactly one evidence-backed serialization mode: `NEW_GENERATED_TYPE`, `GENERATED_VERSION_BUMP`, or `LEGACY_MANUAL_MIGRATION`. Return `BLOCKED_INPUT` for incomplete artifacts, `BLOCKED_EVIDENCE` when field order, version encoding, identity, or mode is ambiguous, and `VALIDATION_FAILED` for generator/build/test failure. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Record inheritance, type identity, every version branch, exact write/read order and types, defaults, deleted fields, and runtime-only state from the actual methods.
2. Inspect generator attributes, setters, schema commands, TypeAlias patterns, and post-load hooks at the target revision.
3. For a new type, apply the verified initial generator pattern. For a version bump, increment version, implement the verified migration shape, and retain prior schemas. For legacy manual migration, preserve the compatible reader and encoded-version behavior.
4. Give persistent fields stable unique indices and use generated setters or verified dirty APIs for mutations.
5. Remove manual methods or `Serial` constructors only after every supported old-save path is proven.
6. Restore timers, caches, and registrations only in the verified post-load phase; never serialize execution tokens.
7. Run required schema generation, build, and test new round trip, every supported old version, renamed types, deleted/null references, and unsupported/corrupt inputs.

## Result contract

This skill owns the top-level result; embed persistence results as evidence and propagate its blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with serialization mode and `Version | Field index | Type | Identity | Migration`; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires every supported version and identity mapped and tested.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map sibling blockers and embed ready evidence. Use confidence `high` only for direct schema/revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, types, versions, identities, and mode; `# Checklist` covers every field/version, schema, runtime state, and test; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, unsupported versions, recovery input, or `None`.

Compare every old version with the final map, reject reused indices or runtime handles, inspect generated schemas and the final diff, and never claim save compatibility from declaration order or inference.
