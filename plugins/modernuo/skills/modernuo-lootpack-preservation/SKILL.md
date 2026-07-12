---
name: modernuo-lootpack-preservation
description: >
  Use when editing or migrating ModernUO-based creature loot that contains
  GenerateLoot, AddLoot(LootPack.*), PackGold, PackItem, or loot-policy helpers.
  Preserve source-derived pack behavior unless the request explicitly authorizes
  an economy change; use uo-loot-generation-artifacts for new loot-system design.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, rebirthuo, loot, lootpack, economy]
    related_skills:
      - uo-loot-generation-artifacts
      - modernuo-content-patterns
      - modernuo-code-audit
      - modernuo-era-expansion
---

# ModernUO LootPack Preservation

## Boundary

Treat existing or migration-source `LootPack` calls as economy behavior, not
formatting. This skill guards unrelated creature work from silently changing
gold variance, item rolls, gems, reagents, artifacts, or farming value. It does
not design a new loot system.

## Workflow

1. Record every scoped loot call, pack name, count, order, special drop, era
   branch, and source tier before editing.
2. Implement unrelated stats, skills, AI, abilities, or serialization while
   leaving that loot surface unchanged.
3. If prose and source code disagree, describe the concrete behavior difference
   and recommend a path. Generic prose such as "gold and magic items" is not a
   replacement recipe.
4. Ask for confirmation before removing or replacing source-derived calls unless
   the request already authorizes that exact economy change.
5. Implement only the confirmed delta and compare the resulting loot block with
   the recorded baseline.

## Guardrails

- Preserve count arguments: `AddLoot(LootPack.Gems, 2)` is not equivalent to the
  one-roll form.
- Replacing several packs with `PackGold(min, max)` changes more than the gold
  range; it can remove item, gem, reagent, and variance behavior.
- Do not introduce a named policy helper as a silent substitute for source code.
- State the relevant era/ruleset before calling a guide-alignment canonical.
- Direct replacement is allowed when explicitly requested, when designing a new
  profile with no source-derived block, or when the user asked to fix proven
  dead, duplicated, uncompilable, or out-of-era loot.

## Confirmation Shape

```text
Recommendation: preserve the source LootPack block. Replacing it with {new form}
would change {gold variance/item rolls/gems/reagents/artifacts}. Should that
economy change be made, or should the source calls remain?
```

## Output Contract

Return the before/after loot calls, source/era used, whether confirmation was
required and obtained, and a plain-language statement of any drop/economy
change. Do not describe an intentional loot replacement as only a refactor.

## Verification

- Expected `AddLoot(LootPack.*[, count])` calls remain unless explicitly replaced.
- No `PackGold` or policy helper silently substitutes for a pack.
- Special drops and era branches remain intact outside the approved scope.
- The diff and focused build/test are reported with their actual scope.

## Reference Routing

- Read [economy-change examples](references/economy-change-examples.md) when a
  guide and source-derived pack block imply different drop shapes.
- Load `uo-loot-generation-artifacts` for brand-new generation, artifact, runic,
  or distribution design.
- Load `modernuo-era-expansion` when the decision differs by expansion.
- Inspect the current creature, its migration source, and the active loot-pack
  implementation before relying on guide prose.
