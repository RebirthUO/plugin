---
name: modernuo-era-expansion
description: Use when implementing or reviewing era-conditional ModernUO behavior, Core.AOS/SE/ML/etc. checks, Expansion values, or an unspecified target era that changes mechanics. Establishes cumulative versus exact gates and test coverage. Do not use for broad era-ownership changes; use modernuo-era-change-gate.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, era, expansion, core-flags, parity]
    related_skills:
      - modernuo-era-change-gate
      - modernuo-content-taxonomy
      - modernuo-content-patterns
      - modernuo-code-audit
      - uo-official-evidence
---

# ModernUO Era and Expansion Behavior

## Boundary

Own a concrete era-conditioned implementation or review. Use [modernuo-era-change-gate](../modernuo-era-change-gate/SKILL.md) when behavior ownership moves between eras/profiles, and taxonomy/parity skills for broad inventories.

## Era gate

If the target era/profile materially changes behavior and is neither stated nor discoverable from configuration, ask before editing or claiming parity. Do not default silently to AoS, latest-era, or shard policy.

## Workflow

1. Read [expansion-map.md](references/expansion-map.md), then inspect `ExpansionInfo`, `Core.Expansion`, active expansion/profile configuration, and the nearest local mechanic.
2. State the target era/profile and whether the requirement is:
   - cumulative (`Core.AOS`: AoS and later);
   - exact (`Core.Expansion == Expansion.AOS`);
   - profile/config-specific;
   - intentionally custom/Enhanced.
3. Gather source evidence for values and introduction/changes; distinguish current official behavior, historical publish behavior, repo precedent, and shard policy.
4. Place the branch at the narrowest stable behavior boundary. Preserve earlier and later behavior explicitly and avoid scattering equivalent checks.
5. Test at least the immediately earlier era, target era, and a later era for cumulative gates; test exact/profile behavior separately.
6. Audit side effects on combat, stats, loot/economy, skills, housing, persistence, client presentation, and registration/data loading as applicable.

## Safety gates

- Later expansions satisfy cumulative convenience properties; this may intentionally or accidentally inherit behavior.
- Era-specific APIs/data must not be invoked before their gate.
- Stored fields can still leak behavior through runtime aggregation or tooltips even if one special hook is gated.
- Do not encode publish numbers in symbol names; keep evidence in comments/docs/tests.
- Update matching profile/data/docs only when the requested behavior requires it.

## Verification/self-check

Run the earlier-target-later/profile matrix and inspect both display and runtime behavior where stored values exist. Recheck cumulative versus exact semantics against current `Core` implementation.

## Output contract

Return the target era/profile, evidence class, cumulative/exact decision, changed gates/paths, earlier-target-later behavior matrix, tests/results, and unresolved parity or policy decisions.

## Reference routing

- Always read [expansion-map.md](references/expansion-map.md).
- Read [modernuo-era-change-gate](../modernuo-era-change-gate/SKILL.md) when ownership/profile activation changes.
- Read [modernuo-content-taxonomy](../modernuo-content-taxonomy/SKILL.md) only for an explicit cross-domain parity inventory.
