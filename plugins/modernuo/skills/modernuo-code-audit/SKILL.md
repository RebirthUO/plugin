---
name: modernuo-code-audit
description: Use when reviewing new or modified ModernUO C# for correctness, serialization, lifecycle, event-loop safety, performance, strings, UI, and era conventions. Report evidence-ranked findings; do not edit code unless the user explicitly requested fixes. Do not use as a substitute for domain-specific behavior or parity review.
license: MIT
metadata:
  version: "1.2.0"
---

# ModernUO Code Audit

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Audit the requested files or diff and report actionable findings. A review request is read-only: never apply fixes unless the user explicitly authorizes implementation. Do not decide gameplay parity, era policy, or architecture from this skill alone.

## Workflow

1. Require a file set or diff, intended behavior, target era/profile when relevant, and requested review/fix mode. If scope, callers, tests, or a local API cannot be resolved, return a limited review or `BLOCKED` result with the exact missing input; preserve unrelated work.
2. Read each complete changed file plus definitions/callers needed to understand behavior.
3. Classify code as game-loop content or infrastructure and as hot, warm, or cold before applying performance/threading rules.
4. Read [audit-rules.md](references/audit-rules.md). Keep this audit self-contained; recommend a separately triggered specialist skill only when its own exact trigger applies, and never represent an unrun specialist review as completed audit evidence.
5. Trace each potential finding to a concrete path/line, impact, and locally valid correction. Avoid style-only findings unless repository policy requires them.
6. Check tests and generated schemas against changed behavior; run read-only build/test commands only when useful and authorized by the task.
7. For legacy serialization migration, cross-thread ownership, or player-visible era claims, report the specialized follow-up needed and the evidence gap. Do not delegate inside this audit; trace the current local contract and label unavailable evidence.
8. Re-read the diff to remove false positives, duplicates, and claims not supported by local code.

## Finding priorities

Use the priority guidance in [audit-rules.md](references/audit-rules.md). Format each as `[P#] Short title — path:line`, then state the failure scenario, why code permits it, and the smallest valid correction. If none remain, say so and name residual verification gaps.

## Mandatory safety pass

- Generated serialization, version/schema migration, dirty tracking, and runtime-only handles.
- Timer/event/owned-reference cleanup across disable, delete, death, logout, and reload where applicable.
- Game-loop threading, world scans, pooling, allocation, and blocking work.
- Gump non-empty paths, stale response authorization, property-list arguments, and handler-aware strings.
- Era/profile gates and player-visible PvP, PvM, economy, housing, or client effects.
- Local code, client data, emulators, and community material may establish implementation observations only. Require OSI/EA/Broadsword evidence for gameplay claims; otherwise label the claim unresolved and request policy direction.

## Verification/self-check

Re-read every finding against the complete file, callers, tests, and local API; remove duplicates, speculation, and style-only noise. Confirm priorities match the demonstrated impact, that review-only work made no edits, and that every required output section appears in the prescribed order with allowed source, verification, and confidence values.

## Output contract

Return these sections in order: `Outcome` (`REVIEWED`, `LIMITED`, or `BLOCKED`); `Findings` (P0 through P3, or `No findings`); `Evidence` (path/line anchors and source class); `Verification` (each result is `PASSED`, `FAILED`, `SKIPPED`, or `UNAVAILABLE`, with reason); `Assumptions and Confidence`; and `Residual Risks`. Source classes are `local-source`, `test-output`, `official-gameplay`, `user-supplied`, or `unresolved`. Use `high` confidence only when local evidence and relevant verification are complete; `medium` when evidence is partial with named gaps; and `low` for `LIMITED` or `BLOCKED`. Each finding includes failure scenario, cause, smallest safe correction, evidence, and test gap. For player-visible claims, separate official gameplay evidence from local implementation observations. For review-only work, do not edit.

## Reference routing

- Always read [audit-rules.md](references/audit-rules.md).
- For player-visible or era-sensitive claims, identify `uo-official-evidence` as the required follow-up; otherwise keep the audit local and disclose the evidence limit.
