---
name: uo-official-evidence
description: Use when a ModernUO or Ultima Online task must establish official OSI/EA/Broadsword behavior, chronology, era, publish, formula, restriction, or source authority before comparison or implementation. Separate official gameplay truth from community discovery and repository implementation evidence; unresolved official claims remain blocked. Do not use emulator or local code as official mechanics proof.
version: 1.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: gate
    workflow_phase: research
    workflow_tier: support
    tags: [ultima-online, osi, ea, broadsword, evidence, parity]
    related_skills:
      - modernuo-issue-research
      - modernuo-era-expansion
      - modernuo-era-change-gate
      - uo-living-world-review
---

# UO Official Evidence

## Boundary

Establish the expected official-server contract for a named claim. This skill
owns source authority and reconciliation; domain skills own mechanic analysis,
and ModernUO skills own implementation.

## Workflow

1. Read [the evidence policy](references/evidence-policy.md).
2. List each behavior, chronology, era, formula, restriction, or presentation
   claim separately and name the target official ruleset and time period.
3. Capture the exact UO.com/Broadsword or archived official EA/OSI source that
   supports each claim. For publishes, start from the official publish index
   and linked entry rather than guessing a URL.
4. Check the complete official page and later official fixes/revisions. Current
   wording does not automatically prove launch-era behavior.
5. Use community archives only to locate official material or expose a conflict.
   Use client data only for presentation facts it directly proves.
6. Only after the official contract is recorded, inspect ModernUO, another
   engine, or the target repository to classify implementation status.
7. If official evidence is unavailable, incomplete, or conflicting for a
   behavior-changing claim, return `UNRESOLVED_OFFICIAL_EVIDENCE` and a focused
   user question. Do not infer or vote among unofficial sources.

## Output contract

Return one evidence record per claim with statement, official source URL/title,
official time scope, checked date, exact support, conflicts/revisions,
implementation evidence when requested, classification, and unresolved
questions.

Allowed implementation classifications are `match`, `partial`, `absent`,
`custom`, and `unreachable`. They never change the official statement.

## Verification

- Every official gameplay claim has direct official support and an exact time
  scope.
- Community, emulator, client, and repository sources are labeled and never
  promoted to official authority.
- Current and historical official wording are not conflated.
- Unresolved claims remain blockers instead of defaults.
