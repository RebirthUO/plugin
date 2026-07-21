---
name: modernuo-migrate-gumps
description: Migrate an existing RunUO Gump, layout calls, SendGump usage, or OnResponse handler to the gump APIs verified in a specific ModernUO repository revision. Use for static-versus-dynamic layout selection, builders, placeholders, DisplayTo gates, stable IDs, and stale-response safety. Do not use for unrelated new UI design.
---

# RunUO to ModernUO Gump Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require the source gump and callers, one explicit ModernUO repository and revision, intended player-visible behavior, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and available build/UI-test facilities. Verify current gump bases, builders, send/close APIs, and response signatures in that revision before selecting an API.

Return `BLOCKED_INPUT` for missing scope or behavior, `BLOCKED_EVIDENCE` when target APIs or client requirements remain ambiguous, and `VALIDATION_FAILED` when required checks fail. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory pages, controls, button/switch/text-entry IDs, dynamic structure, state, prerequisites, callers, and response validation.
2. Choose the verified fixed-layout type when structure is fixed and the verified dynamic type when control structure varies; cite the inspected target declarations.
3. Move layout and dynamic strings through the target revision's builders without changing IDs or player-visible behavior. Button `0` remains close/cancel.
4. Centralize construction prerequisites in the verified display entry point and prevent invalid instances.
5. Revalidate authority, ownership, range, and object state in every response; displayed state may be stale.
6. Preserve handler-aware strings and verified cliloc IDs. Load [modernuo-string-handling](../modernuo-string-handling/SKILL.md) only when strings change, and incorporate its evidence into this result contract.
7. Test success, cancel, invalid/stale response, prerequisite failure, stacking behavior, and every constructed layout. Never send an empty gump.

## Result contract

This skill owns the top-level result; embed string-skill findings as evidence and propagate any sibling blocker or validation failure. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` containing gump type and `Control ID | Source meaning | Target meaning | State rule`; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`, including manual client checks. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires every applicable workflow check to pass, including nonempty layouts, stable IDs, success/cancel/stale/prerequisite/stacking paths, with only evidence-backed non-applicable checks exempted.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state. Map sibling `blocked` to the matching parent blocker and sibling `ready` to embedded evidence only. Use `high` confidence only for direct revision evidence plus all runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, files, behavior, client, and mode; `# Checklist` records status and evidence; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, manual checks, recovery input, or `None`.

Confirm all target APIs against the recorded revision, preserve visible behavior, prove every layout nonempty, exercise stale inputs, and distinguish repository evidence from official gameplay claims.
