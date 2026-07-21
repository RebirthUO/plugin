---
name: modernuo-migrate-timers
description: Migrate existing RunUO Timer subclasses, DelayCall patterns, TimerPriority, cancellation, or post-load restoration to timer APIs verified in a specific ModernUO repository revision. Use for callback selection, TimerExecutionToken ownership, deterministic timing, persistence semantics, and lifecycle cleanup. Do not use for wall-clock or calendar scheduling.
---

# RunUO to ModernUO Timer Migration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required inputs and evidence gate

Require all source start/cancel/restore sites, one explicit ModernUO repository and revision, owner lifetime, delay/interval/count, restart/deadline semantics, mode (`PLAN`, `IMPLEMENT`, or `AUDIT`), and applicable deterministic test facilities. Inspect [modernuo-timers](../modernuo-timers/SKILL.md) for the target's supported overloads and test seams.

Return `BLOCKED_INPUT` when ownership or timing semantics are missing, `BLOCKED_EVIDENCE` when current APIs or lifecycle hooks cannot be proven, and `VALIDATION_FAILED` when required checks fail. Classify wall-clock recurrence as `OUT_OF_SCOPE` and name the capability needed instead of inventing a local scheduler. Do not edit in `PLAN` or `AUDIT` mode.

## Workflow

1. Inventory every start, repeat, cancel, expiry, owner delete/disable, save, load, and callback-state path.
2. Choose the least-allocating verified callback API that preserves semantics; use `TimerExecutionToken` only when cancellation is required.
3. Move nested tick logic to the owner when appropriate and remove `TimerPriority` without inventing a replacement.
4. Cancel tokens before owner state becomes invalid. Make repeated start/cancel and adjacent cancel/expiry paths idempotent on the event loop.
5. Keep tokens runtime-only. Persist durable progress or deadlines separately and restore only in the verified post-load phase, explicitly preserving remaining-duration versus reset-on-load behavior.
6. Use [modernuo-threading](../modernuo-threading/SKILL.md) when callbacks cross ownership boundaries.
7. Test exact timing boundaries, repeated start/cancel, expiry, delete/disable, save-load restoration, callback idempotence, and hot-path allocation expectations.

## Result contract

This skill owns the top-level result; embed timer/threading results as evidence and propagate their blockers or failed checks. Return, in order: `# Outcome` table `State | Mode | Confidence`; `# Scope`; `# Migration Inventory` with `Timer | Owner | Start | Cancel | Persistence | Evidence`; `# Evidence` table `Claim | Classification | Locator | Confidence | Notes`; `# Checklist`; `# Compatibility Decisions`; `# Files`; `# Validation` table `Check | Command or method | Status | Evidence`; and `# Residual Risk`. Use `PLANNED`, `IMPLEMENTED`, `AUDITED`, `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, or `VALIDATION_FAILED`; validation uses `passed`, `failed`, `blocked`, or `not-run`. `IMPLEMENTED` requires every timer and owner path mapped and deterministic tests passing.

## Self-check

Resolve the repository to its canonical path or URL and immutable 40-character commit SHA. State precedence is `OUT_OF_SCOPE`, `BLOCKED_INPUT`, `BLOCKED_COMPATIBILITY`, `BLOCKED_EVIDENCE`, `VALIDATION_FAILED`, then the mode success state; map sibling blockers and embed ready evidence. Use confidence `high` only for direct revision evidence plus all deterministic runtime checks, `medium` for indirect/static-only evidence, and `low` for unresolved inputs; outcome confidence is the lowest material-claim confidence. `# Scope` records repository, SHA, timer owners, timing/persistence semantics, and mode; `# Checklist` covers every start/cancel/restore/expiry path; `# Compatibility Decisions` uses `accepted`, `rejected`, `unresolved`, or `not-applicable`; `# Files` is mode-specific; `# Residual Risk` records assumptions, manual timing checks, recovery input, or `None`.

Re-scan for serialized tokens, orphan callbacks, hot repeating closures, premature restoration, calendar misuse, and unsupported API assumptions. Cite repository revision/path/symbol evidence for every implementation claim.
