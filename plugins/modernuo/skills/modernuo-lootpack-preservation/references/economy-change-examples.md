# Loot Preservation Economy Examples

Read this reference when prose and source code imply different loot shapes.

Replacing:

```csharp
AddLoot(LootPack.FilthyRich);
AddLoot(LootPack.Rich);
AddLoot(LootPack.Gems, 2);
```

with:

```csharp
PackGold(700, 1000);
TokunoMagicItemPolicy.PackUOGuideListedMagicItem(this);
```

is not a formatting conversion. It can change gold variance, magic-item rolls,
gem count, reagents, special chances, farming value, and the shard economy.
Generic guide prose such as "700 to 1000 gold and magic items" does not identify
which ModernUO pack or policy helper reproduces live behavior.

Record pack names/counts/order and special drops first. If the request does not
already authorize the replacement, recommend preserving source code and ask the
user to choose. If approved, name every removed/added roll in the final output and
leave unrelated entries untouched.

Direct implementation is reasonable when the user explicitly requests the exact
alignment, the profile is brand new, or stronger evidence proves a scoped entry
dead, duplicated, uncompilable, or outside the selected era.
