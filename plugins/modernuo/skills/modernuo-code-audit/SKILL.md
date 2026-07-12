---
name: modernuo-code-audit
description: Use when reviewing new or modified C# under Projects/ for ModernUO correctness, serialization, lifecycle, event-loop safety, performance, strings, UI, and era conventions. Report evidence-ranked findings; do not edit code unless the user explicitly requested fixes. Do not use as a substitute for domain-specific behavior or parity review.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, csharp, audit, safety, performance]
    related_skills:
      - modernuo-serialization
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-threading
      - modernuo-performance-hot-paths
      - modernuo-string-handling
      - modernuo-property-lists
      - modernuo-gump-system
      - modernuo-content-patterns
      - modernuo-test-workflow
---

# ModernUO Code Audit

## Boundary

Audit the requested files or diff and report actionable findings. A review request is read-only: never apply fixes unless the user explicitly authorizes implementation. Do not decide gameplay parity, era policy, or architecture from this skill alone.

## Workflow

1. Establish the exact diff/files and preserve unrelated work. Read each complete changed file plus definitions/callers needed to understand behavior.
2. Classify code as game-loop content or infrastructure and as hot, warm, or cold before applying performance/threading rules.
3. Read [audit-rules.md](references/audit-rules.md) and route risky surfaces to the relevant domain skill.
4. Trace each potential finding to a concrete path/line, impact, and locally valid correction. Avoid style-only findings unless repository policy requires them.
5. Check tests and generated schemas against changed behavior; run read-only build/test commands only when useful and authorized by the task.
6. Re-read the diff to remove false positives, duplicates, and claims not supported by local code.

## Finding priorities

Use the priority guidance in [audit-rules.md](references/audit-rules.md). Format each as `[P#] Short title — path:line`, then state the failure scenario, why code permits it, and the smallest valid correction. If none remain, say so and name residual verification gaps.

## Mandatory safety pass

- Generated serialization, version/schema migration, dirty tracking, and runtime-only handles.
- Timer/event/owned-reference cleanup across disable, delete, death, logout, and reload where applicable.
- Game-loop threading, world scans, pooling, allocation, and blocking work.
- Gump non-empty paths, stale response authorization, property-list arguments, and handler-aware strings.
- Era/profile gates and player-visible PvP, PvM, economy, housing, or client effects.

## Verification/self-check

Re-read every finding against the complete file, callers, tests, and local API; remove duplicates, speculation, and style-only noise. Confirm priorities match the demonstrated impact and that review-only work made no edits.

## Output contract

Return findings ordered by priority, each with exact evidence and correction; then list assumptions, commands/results, and residual risks. Do not include a generic summary before findings. When asked to fix, make only approved changes and re-run the relevant audit plus focused verification.

## Reference routing

- Always read [audit-rules.md](references/audit-rules.md).
- Read [modernuo-serialization](../modernuo-serialization/SKILL.md), [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md), or [modernuo-performance-hot-paths](../modernuo-performance-hot-paths/SKILL.md) only when those surfaces changed.
- Read [modernuo-era-expansion](../modernuo-era-expansion/SKILL.md) when a mechanic is era-sensitive.
