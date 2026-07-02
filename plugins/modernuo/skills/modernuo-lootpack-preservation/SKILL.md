---
name: modernuo-lootpack-preservation
description: Use when editing or migrating ModernUO/RebirthUO creature loot, especially GenerateLoot() and AddLoot(LootPack.*) calls. Preserves source-derived loot entries unless the user explicitly approves an economy-changing replacement.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, rebirthuo, loot, lootpack, economy]
    related_skills:
      - uo-loot-generation-artifacts
      - modernuo-content-patterns
      - modernuo-code-audit
      - modernuo-era-expansion
---

# ModernUO LootPack Preservation

## Overview

Use this skill as the economy-safety gate for creature loot edits. `AddLoot(LootPack.*[, count])` calls are not formatting noise: they encode gold, magic-item, gem, reagent, and artifact-roll behavior that affects shard inflation, farming value, PvM risk/reward, and source-era parity.

The default stance is preservation. Replace a source-derived loot block only when the user explicitly requests the economy change or confirms it after seeing the behavioral difference.

## When to Use

- Migrating RunUO/ServUO creature code into ModernUO/RebirthUO.
- Editing `GenerateLoot()`, constructor loot blocks, `AddLoot(LootPack.*)`, `PackGold(...)`, `PackItem(...)`, or named loot-policy helpers.
- Reconciling source code with UOGuide/UO.com prose such as "700 to 1000 gold and magic items".
- Reviewing a creature stat, ability, or serialization change that happens near loot code.
- Proposing era-specific loot policy conversions, such as Tokuno magic-item helper policies.

Don't use this as the main loot-design reference for brand-new systems; load `uo-loot-generation-artifacts` for loot-system design and this skill only for the preservation gate.

## Core Rule

Preserve source-derived `AddLoot(LootPack.*[, count])` calls by default.

Treat existing repo code, migration source code, and source-derived snippets as behavior evidence. Do not replace, remove, collapse, or reinterpret `LootPack` entries unless the user explicitly asks to add, remove, replace, align with exact source-gold values, or use a named policy conversion.

## Confirmation Gate

When source code and a guide page suggest different loot shapes, stop before editing the loot behavior. Give a concise recommendation and ask whether that is the intended solution.

Use this gate for changes like:

```csharp
AddLoot(LootPack.FilthyRich);
AddLoot(LootPack.Rich);
AddLoot(LootPack.Gems, 2);
```

being replaced by:

```csharp
PackGold(700, 1000);
TokunoMagicItemPolicy.PackUOGuideListedMagicItem(this);
```

That replacement changes economy and drop behavior. UOGuide prose such as "700 to 1000 Gold and Magic Items" is not enough by itself to justify removing source `LootPack` entries.

## Recommended Workflow

1. Identify every source-derived loot call in the scoped `GenerateLoot()` or constructor loot block, including pack names, counts, order, and nearby special drops.
2. Preserve those calls exactly while implementing unrelated stats, skills, abilities, resistances, names, body values, or serialization work.
3. If a guide lists exact gold or generic "magic items" that conflicts with the source `LootPack` block, explain the conflict and recommend one path.
4. Ask the user to confirm before changing the loot surface unless the original request already explicitly authorizes that exact loot change.
5. After confirmation, implement only the confirmed loot change and leave unrelated `LootPack` entries untouched.
6. Verify the diff still contains the expected loot calls or the confirmed replacement, then report the economic behavior change plainly.

## Recommendation Format

Use a short recommendation that names the behavior difference:

```text
Recommendation: preserve the source LootPack block for now. Replacing it with PackGold(700, 1000) plus TokunoMagicItemPolicy would enforce UOGuide exact-gold prose, but it removes the source pack rolls and changes economy/drop behavior. Should I make that replacement, or keep the source LootPack calls?
```

If the user already requested the exact replacement, do not ask again. Implement the requested replacement and note that it intentionally changes source loot behavior.

## Direct Implementation Is Allowed When

- The user explicitly requests UOGuide alignment, exact-gold replacement, removed loot, added loot, or a named policy conversion.
- The scoped creature has no source-derived loot block, and the task is to create a new loot profile.
- A `LootPack` call is clearly dead, duplicated by typo, uncompilable, outside the scoped era, or contradicted by stronger source evidence, and the user asked for cleanup or parity correction.

## Common Pitfalls

1. **Treating generic source prose as a replacement recipe.** "Magic Items" does not imply a specific ModernUO `LootPack` or custom helper without an explicit policy decision.
2. **Collapsing multiple pack rolls into one exact `PackGold`.** This removes variance, item rolls, and often gem/reagent rolls; it is an economy change, not a refactor.
3. **Editing loot while doing unrelated creature work.** Stats, skills, AI, abilities, and serialization can usually be fixed while leaving loot untouched.
4. **Forgetting count arguments.** `AddLoot(LootPack.Gems, 2)` and `AddLoot(LootPack.Gems)` are different drop surfaces.
5. **Calling a UOGuide alignment canonical without era scope.** Name the era/ruleset and source tier before replacing loot behavior.

## Verification Checklist

- [ ] Source `AddLoot(LootPack.*)` calls are still present unless an explicit user-approved replacement removed them.
- [ ] Counts such as `AddLoot(LootPack.Gems, 2)` are preserved or intentionally changed.
- [ ] `PackGold(...)` was not added as a substitute for a pack unless explicitly requested or confirmed.
- [ ] Policy helpers such as `TokunoMagicItemPolicy.PackUOGuideListedMagicItem(this)` were not introduced as silent replacements.
- [ ] The final response names any loot behavior change as economy/drop behavior, not only as a mechanical refactor.
