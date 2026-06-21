---
name: modernuo-lootpack-preservation
description: "Preserve source-derived LootPack calls when editing ModernUO/RebirthUO creature loot. Use when migrating source code, editing GenerateLoot(), reconciling AddLoot(LootPack.*) with UOGuide loot prose, or proposing PackGold/policy replacements such as TokunoMagicItemPolicy. Require a recommendation and user confirmation before replacing, adding, or removing source LootPack entries unless the user explicitly requested that loot change."
---

# ModernUO LootPack Preservation

## Core Rule

Preserve source-derived `AddLoot(LootPack.*[, count])` calls by default.

Treat existing repo code, migration source code, and source-derived snippets as behavior evidence. Do not replace, remove, collapse, or reinterpret `LootPack` entries unless the user explicitly asks to add, remove, replace, align with UOGuide exact gold, or use a named policy conversion.

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

This replacement changes economy and drop behavior. UOGuide prose such as "700 to 1000 Gold and Magic Items" is not enough by itself to justify removing source `LootPack` entries.

## Recommended Workflow

1. Identify every source-derived loot call in the scoped `GenerateLoot()` or constructor loot block, including pack names, counts, order, and nearby special drops.
2. Preserve those calls exactly while implementing unrelated stats, skills, abilities, resistances, names, body values, or serialization work.
3. If UOGuide lists exact gold or generic "Magic Items" that conflicts with the source `LootPack` block, explain the conflict and recommend one path.
4. Ask the user to confirm before changing the loot surface.
5. After confirmation, implement only the confirmed loot change and leave unrelated `LootPack` entries untouched.

## Recommendation Format

Use a short recommendation that names the behavior difference:

```text
Recommendation: preserve the source LootPack block for now. Replacing it with PackGold(700, 1000) plus TokunoMagicItemPolicy would enforce UOGuide exact-gold prose, but it removes the source pack rolls and changes economy/drop behavior. Should I make that replacement, or keep the source LootPack calls?
```

If the user already said to replace with exact UOGuide gold, do not ask again. Implement the requested replacement and note that it intentionally changes source loot behavior.

## Direct Implementation Is Allowed When

- The user explicitly requests UOGuide alignment, exact-gold replacement, removed loot, added loot, or a named policy conversion.
- The scoped creature has no source-derived loot block, and the task is to create a new loot profile.
- A `LootPack` call is clearly dead, duplicated by typo, uncompilable, or outside the scoped era, and the user asked for cleanup or parity correction.

For new loot profiles with no preservation question, use `uo-loot-generation-artifacts` for loot-system design and `modernuo-content-patterns` for creature templates.

## Review Checklist

- Source `AddLoot(LootPack.*)` calls are still present unless an explicit user-approved replacement removed them.
- Counts such as `AddLoot(LootPack.Gems, 2)` are preserved.
- `PackGold(...)` was not added as a substitute for a pack unless explicitly requested or confirmed.
- Policy helpers such as `TokunoMagicItemPolicy.PackUOGuideListedMagicItem(this)` were not introduced as silent replacements.
- The response names any loot behavior change as economy/drop behavior, not just a mechanical refactor.
