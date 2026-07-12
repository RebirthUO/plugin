---
name: modernuo-content-taxonomy
description: Use when classifying a UO feature into World, Entity, ItemSystem, MobileSystem, Progression, EconomyCrafting, QuestNarrative, Encounter, or ClientPresentation, or when a user explicitly requests a cross-domain parity inventory. Routes concepts to ModernUO code/data. Do not use for ordinary implementation or deep single-mechanic review.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, taxonomy, content, parity, planning]
    related_skills:
      - modernuo-content-patterns
      - modernuo-era-change-gate
      - uo-living-world-review
      - uo-official-evidence
---

# ModernUO Content Taxonomy

## Boundary and branch

Choose one branch:

- **Classification/scoping:** answer “where does this belong?” or decompose a feature across domains. Do not force a full parity inventory.
- **Parity inventory:** only when the user asks for parity, gaps, implementation status, or a 9-domain inventory. Requires a target era/profile and [parity-check.md](parity-check.md).

Use [modernuo-content-patterns](../modernuo-content-patterns/SKILL.md) for implementation after classification. Use a narrow UO domain skill for deep mechanic review.

## Nine domains

`World`, `Entity`, `ItemSystem`, `MobileSystem`, `Progression`, `EconomyCrafting`, `QuestNarrative`, `Encounter`, and `ClientPresentation`. Read the matching section of [mappings.md](mappings.md) for concepts and code/data anchors.

These are design vocabulary, not guaranteed C# types; ModernUO commonly uses subclasses, data rows, enums/tables, and virtual profiles.

## Workflow: classification

1. State the user outcome and target era/profile if behavior depends on it.
2. Identify the primary domain, then direct dependencies. A placed boss may span Entity, MobileSystem, Encounter, loot, World, and ClientPresentation.
3. Read only the matching sections of [mappings.md](mappings.md), then verify every proposed path/type in the current repository.
4. Separate definition/data, runtime instance, registration/bootstrap, persistence, and presentation surfaces.
5. Return the smallest implementation map; mark absent or unverified anchors explicitly.

## Parity workflow

When the parity branch triggers, read [parity-check.md](parity-check.md) and [uo-official-evidence](../uo-official-evidence/SKILL.md). Do not claim `Present` or `Gap` without era-scoped official evidence plus current repository evidence.

## Safety gates

- Distinguish `Gap`, `Partial`, `SourceLocked`, `RuntimeBlocked`, and intentional `Custom` behavior.
- Repository code is implementation evidence, not proof of official UO history.
- Client asset fidelity cannot be inferred from server-side numeric IDs alone.
- Do not create issues or mutate trackers unless the user explicitly asks; issue slicing is a draft/report operation by default.

## Verification/self-check

Verify every proposed path/type in the current repository and every parity status against the stated era/profile and cited source class. Re-scan for implementation already present, unverified claims, and cross-domain dependencies.

## Output contract

For classification, return primary/dependent domains, verified ModernUO types/paths, integration order, era assumptions, and open evidence. For parity, return the full English Markdown contract in [parity-check.md](parity-check.md), with citations and confidence. In either branch, identify checks performed and unresolved paths/source conflicts.

## Reference routing

- Read [mappings.md](mappings.md) only for the domains in scope.
- Read [parity-check.md](parity-check.md) only for explicit parity/inventory work.
- Read [modernuo-era-change-gate](../modernuo-era-change-gate/SKILL.md) when ownership or behavior moves between eras/profiles.
