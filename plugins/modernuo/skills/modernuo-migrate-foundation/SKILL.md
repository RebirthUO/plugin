---
name: modernuo-migrate-foundation
description: Use for a cross-cutting RunUO or ServUO migration to ModernUO that spans conventions, compatibility, lifecycle, persistence, time, threading, or performance. Do not use for a narrow serialization-only, timer-only, gump-only, packet-only, threading-only, or unrelated C# task.
license: MIT
metadata:
  version: 1.2.0
  author: RebirthUO
---

# RunUO to ModernUO Migration Foundation

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

Establish an evidence-backed migration baseline, account for compatibility risks, and produce a verifiable plan, implementation, or audit result. This skill owns the cross-cutting pass; it does not claim subsystem expertise that is absent from the current portfolio.

## Required inputs

Before analysis or mutation, establish:

- requested mode: `PLAN`, `IMPLEMENT`, or `AUDIT`;
- migration scope and source files;
- target repository and current revision;
- compatibility expectations, including whether existing saves must load;
- saved-state, registration, timer, lifecycle, UI, packet, and threading exposure;
- target era or server profile when player-visible behavior can vary by era.
- for `IMPLEMENT`, the pre-mutation working-tree status and whether existing changes overlap the migration scope.

Accept only `PLAN`, `IMPLEMENT`, or `AUDIT`. Reject an unknown mode as `BLOCKED_INPUT`; if the requested artifacts or mutation intent conflict with the selected mode, ask which one should govern before continuing. Inspect repository instructions and the nearest current ModernUO implementation. If a required input cannot be discovered, ask for the smallest missing input and return `BLOCKED_INPUT` without guessing.

## Workflow

1. Inventory source files, type identity, namespaces, registrations, saved fields, timers, owned references, UI, packets, concurrency, and user-visible behavior.
2. Classify evidence as `official-source`, `repository`, `user-policy`, `community-or-emulator`, `assumption`, or `unresolved`. Only current official OSI/EA/Broadsword material may establish gameplay behavior. Keep repository, client, community, and emulator observations separately labeled; they may prove implementation state but may not fill an unresolved official claim. Repository evidence requires a path and revision; external evidence requires a direct source locator.
3. Select ModernUO precedent in this order: same subsystem and API at the target revision; its focused tests; a current same-domain implementation; then a broader repository pattern. Record the selected locator and rejected conflicting precedent. If equally relevant precedents conflict, classify the choice as `unresolved` rather than selecting silently.
4. Evaluate these internal checklist categories in this fixed order: source layout and naming; type identity and saved-state compatibility; registration and lifecycle ownership; timers and time semantics; UI and packets; threading; allocation and query performance; gameplay era; focused verification. Mark a category `applicable` when an inventoried file, dependency, or requested behavior exposes it. Mark it `skipped` only with a concrete scope fact or evidence locator; preference alone is not a skip reason.
5. Preserve legacy fields unless a behavior or compatibility need justifies renaming. Preserve serial constructors, serialization paths, type aliases, registrations, and synchronization until their replacement and compatibility path are proven.
6. In game-loop code, prefer repository-proven map or sector queries over global scans. Do not introduce locks, tasks, threads, concurrent collections, or general pooling without demonstrated ownership and measurement. Use [modernuo-threading](../modernuo-threading/SKILL.md) only when the task becomes specifically about cross-thread ownership or synchronization.
7. For `IMPLEMENT`, make only evidence-backed changes, then run the repository's focused build and tests. For `PLAN` or `AUDIT`, do not imply that files changed or checks passed when they were not run.
8. Re-read the result for incidental behavior changes, unsupported API assumptions, save incompatibility, lifecycle leaks, and unresolved era policy.

For `IMPLEMENT`, preserve non-overlapping existing changes. If an existing change overlaps the proposed edit and its intent cannot be reconciled from the diff, return `BLOCKED_COMPATIBILITY` before mutation. If the request is narrow enough to match an excluded subsystem, do not approximate specialized guidance: return `OUT_OF_SCOPE` and name the required specialization without making claims about which skills are installed. Threading-only work may route to the existing threading skill.

## Terminal states

- `PLANNED`: a decision-complete migration plan with no mutation.
- `IMPLEMENTED`: scoped changes completed and required verification passed.
- `AUDITED`: findings delivered without mutation.
- `OUT_OF_SCOPE`: the request belongs to an excluded narrow specialization; name the required capability.
- `BLOCKED_INPUT`: required scope, repository, revision, compatibility, or era input is missing.
- `BLOCKED_COMPATIBILITY`: save, identity, lifecycle, or behavior compatibility needs a user decision.
- `BLOCKED_EVIDENCE`: local evidence cannot support a proposed transformation.
- `VALIDATION_FAILED`: implementation occurred but a required check failed; include the failure and current working-tree state.

Do not report `IMPLEMENTED` while an applicable checklist item, compatibility decision, or required validation remains unresolved.

For a transient tool failure, retry once only when the operation is read-only or safely repeatable. Preserve the exact command or method, exit status, and diagnostic. If runtime validation is unavailable, continue only with explicitly labeled static analysis and lower confidence; never substitute it for a required runtime check or report `IMPLEMENTED`.

## Output contract

Return these headings in order:

1. `# Outcome` Ã¢â‚¬â€ exactly one Markdown table with columns `State | Mode | Confidence` and one data row, using confidence `high`, `medium`, or `low`.
2. `# Scope` Ã¢â‚¬â€ repository, revision, requested files, compatibility target, and era/profile; write `None` for an empty optional field.
3. `# Migration Inventory` Ã¢â‚¬â€ table `Category | Surface | Evidence locator | Disposition`, ordered by the checklist below.
4. `# Evidence` Ã¢â‚¬â€ table `Claim | Classification | Locator | Confidence | Notes`.
5. `# Checklist` Ã¢â‚¬â€ table `Category | Status | Evidence or skip reason`. In `PLAN`, use `applicable`, `skipped`, or `blocked`; in `IMPLEMENT` and `AUDIT`, every applicable category must finish as `completed` or `blocked`, while unexposed categories remain `skipped`.
6. `# Compatibility Decisions` Ã¢â‚¬â€ table `Decision | Status | Evidence | Impact`, using only `accepted`, `rejected`, `unresolved`, or `not-applicable`; include era decisions and use `None` only when verified empty.
7. `# Files` Ã¢â‚¬â€ changed files for `IMPLEMENT`, proposed files for `PLAN`, or finding locations for `AUDIT`.
8. `# Validation` Ã¢â‚¬â€ table `Check | Command or method | Status | Evidence`, using only `passed`, `failed`, `blocked`, or `not-run`.
9. `# Residual Risk` Ã¢â‚¬â€ assumptions, unresolved items, and residual risks, or `None` when verified empty.

Assign `high` confidence only when the material conclusion has direct authoritative or revision-bound repository evidence and required runtime verification passed. Use `medium` when evidence is indirect or validation is static-only. Use `low` when assumptions, conflicts, missing runtime evidence, or unresolved inputs materially affect the conclusion.

A complete result accounts for every saved field, registration, timer, owned reference, and user-visible behavior in scope without converting assumptions into facts.

Before returning, verify that all nine headings appear once, every checklist category has a disposition, every material claim has a locator and confidence, validation tokens match the contract, file claims match the selected mode, and the terminal state agrees with blockers and validation results.
