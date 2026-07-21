---
name: modernuo-migrate-property-lists
description: Migrate an existing RunUO GetProperties(ObjectPropertyList) override or tooltip arguments to IPropertyList APIs verified in a specific ModernUO repository revision. Use for base-call order, cliloc arguments, delimiters, handler-aware interpolation, conditional properties, invalidation, and supported client or era checks. Do not apply property-list string rules to ordinary messages or gumps.
---

# RunUO to ModernUO Property-List Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require source overrides and callers, one explicit ModernUO repository and revision, target clients/era, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and repository/client localization evidence when exact text matters. Inspect the target `IPropertyList` signatures, interpolation handlers, formatters, and invalidation behavior before transforming arguments.

Return `BLOCKED_INPUT` for missing scope or client target, `BLOCKED_EVIDENCE` for unknown cliloc text/count/order or unverified overload behavior, and `VALIDATION_FAILED` for failed build/tooltips/tests. Do not invent labels or edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory every cliloc, argument count/order, delimiter, conditional property, base-call order, and invalidation source.
2. Apply the verified target override signature while preserving ordering.
3. Apply the property-list-only string-hole rule only when the inspected target handler proves it. Keep protocol delimiters literal and preserve numeric/culture formatting.
4. Use the target's verified cliloc-as-argument formatter. Keep property-list argument formatting owned here; ordinary adjacent strings remain outside this skill's scope.
5. Preserve escaping/encoding of player text and `InvalidateProperties` after visible changes.
6. Build and test base, conditional, invalidation, unknown-ID, argument-order, and earliest supported client/era paths.

## Result contract

This skill owns the top-level result; embed string-skill results as evidence and propagate its blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with `Cliloc | Arguments | Order | Delimiters | Evidence`; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires verified overloads, all cliloc argument mappings, invalidation, and applicable client checks.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map sibling blockers and embed ready evidence. Use confidence `high` only for direct revision/client evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, overrides, clients/era, and mode; `# Checklist` covers signature, clilocs, ordering, formatting, invalidation, and tests; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, manual client checks, recovery input, or `None`.

Re-scan that the property-list rule did not leak into normal strings, cite repository revision/path/symbol evidence, and keep official gameplay evidence separate from repository/client observations.
