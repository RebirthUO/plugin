---
name: modernuo-era-change-gate
description: Use when a ModernUO-based request, diff, issue, plan, or parity finding moves behavior, evidence, data, registration, or profile activation across Ultima Online eras. Identifies the smallest affected era/profile set and requires parity evidence before completion. Do not use for code that merely reads an unchanged era flag.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: gate
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, rebirthuo, era, parity, gate]
    related_skills:
      - modernuo-content-taxonomy
      - modernuo-era-expansion
      - uo-official-evidence
      - uo-living-world-review
      - modernuo-issue-research
---

# ModernUO Era Change Gate

## Boundary

This gate detects and scopes era/profile deltas. It does not decide official parity or implement the change. A completion claim requires targeted parity evidence for every affected era/profile, or an explicit blocker.

## Trigger evidence

Activate when a request/diff changes or disputes an era/profile gate, expansion-owned content/mechanic, profile activation, back/forward-port, or code/data/docs/source ownership.

Do not activate merely because unchanged code contains an era check.

## Workflow

1. Identify the content object, old and new behavior, old/new gates, profile/data/doc changes, and source evidence.
2. Normalize aliases using [modernuo-era-expansion](../modernuo-era-expansion/SKILL.md).
3. Build the smallest set: source era, target era, actual introducing/dependency era when different, and each changed profile. Do not add chronological intermediates without evidence.
4. Run or request targeted [modernuo-content-taxonomy](../modernuo-content-taxonomy/SKILL.md) parity work for the affected set. Keep narrower spell/skill/item-property checks involved when they discovered the delta.
5. Reconcile code gates, profile JSON, data placement, era docs, tests, and player communication. Classify intentional shard policy as `Enhanced`, not official parity.
6. Stop completion when a required era check is missing, contradictory, or blocked; name the exact evidence needed.

## Safety gates

- Ordinal `Core.X` checks often remain true for later eras; review inherited behavior, not only exact-equality branches.
- Changing an expansion enum/table can affect client flags, housing, map selection, required client, status versions, data lookup, and serialization/config ordinals.
- Never use a custom era as a code-ownership marker.
- Do not create tracker issues from findings without explicit user authorization.

## Verification/self-check

Recompute the affected set from code, profile, data, docs, and source evidence; confirm no required source/target/dependency era is omitted. Completion requires every listed check be Done or explicitly Blocked.

## Output contract

Return Markdown with change/evidence, source/target/dependency eras/profiles, affected checks and Done/Required/Blocked status, related parity, decisions, reconciliation/verification, and issue-slice options only when requested. Nothing is era-safe while a required check is omitted or still `Required`.

## Reference routing

- Always read [modernuo-era-expansion](../modernuo-era-expansion/SKILL.md) for aliases and gate semantics.
- For a custom post-official ruleset, require its policy from the configured
  project's instructions or an explicit user decision. Never import another
  project's custom-era policy.
