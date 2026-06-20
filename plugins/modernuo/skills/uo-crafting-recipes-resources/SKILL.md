---
name: "uo-crafting-recipes-resources"
description: "Use when working with the UO crafting engine in ModernUO/RebirthUO servers - CraftSystem, CraftItem, Def* registration files, recipe scrolls, subresources, ML-era recipe gates, runic tools, and bulk order deeds. Use when adding a new craftable item, wiring a new recipe scroll, debugging why a craft succeeds/exceptional/fails, or auditing ML/HL/SA crafting parity."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Crafting, Recipes, Resources

## Overview

UO crafting is a declarative system: each skill (Blacksmithy, Tailoring, Carpentry, ...) has a `CraftSystem` registered in a `Def*.cs` file, and the `CraftSystem` holds a list of `CraftItem` entries that describe a recipe. The runtime pipeline is identical for every skill: validate context, validate tool, validate expansion gate, validate resources, start a timer, make a skill check, and produce an item via reflection (`ICraftable.OnCraft`).

This skill covers the engine (`CraftSystem`, `CraftItem`, `CraftContext`, `CraftSubRes`), the registration DSL (`AddCraft`, `AddRes`, `AddSkill`, `SetNeededExpansion`, `AddRecipe`), the ML recipe/resource extensions (recipe scrolls, runic tools, ML-gated subresources, Darkglow/Parasitic poisons, Parrot Wafer), the Bulk Order Deed (BOD) system, and the recipe-to-system regression test surface.

The reference implementations are `Projects/UOContent/Engines/Craft/Core/CraftSystem.cs`, `CraftItem.cs`, and the `Def*.cs` files. The current ML/SA parity map is in `docs/mondains-legacy-crafting-matrix.md` and the broader feature matrix in `docs/mondains-legacy-content-matrix.md`.

## When to Use

- Adding a new craftable item to an existing `Def*.cs`.
- Adding a new crafting system (rare case; usually a skill is its own system).
- Wiring a recipe scroll so the player can learn the recipe.
- Adding an ML-gated recipe (recipe ID >= 100 in Alchemy, >= 200 in Fletching, etc.).
- Debugging why a craft succeeds/fails/exceptional.
- Auditing ML/SA/HS craft parity against `mondains-legacy-crafting-matrix.md`.
- Wiring a BOD reward item to a BOD profile.

Don't use for:

- The base item types (use `uo-items-foundation`).
- AoS attribute values on a crafted item (use `uo-aos-item-properties`).
- The skill progression system (use the skills system docs).

## The Three-Layer Architecture

```
DefBlacksmithy.cs        CraftSystem                  CraftItem
--------------           -----------                  ---------
static Configure()       AddCraft(type, name)         entry per recipe
                         AddRes(type, ...)            resources, skills, tools
                         AddSkill(skill, min, max)    expansion gate
                         SetNeededExpansion(ML)       optional
                         AddRecipe(id, ...)           rare/normal/quest recipes
```

`Projects/UOContent/Engines/Craft/Core/CraftSystem.cs:14-67` defines `CraftSystem`. It is the per-skill registry. The static `Configure` method on each `Def*.cs` is called from `AssemblyHandler.Invoke("Configure")` during the `Main.cs:418-432` startup sequence.

`CraftItem.cs:27` defines `CraftItem`. One instance per recipe. Holds:

- `Type`/`Name`/`Cliloc` - the produced item type and the localized name.
- `Resources` - `Type[]` of consumed resources, each with a min amount and optional hue retention.
- `Skills` - secondary skill requirements (each with min skill value).
- `Tools` - which tool types (Forge, Saw, Loom, etc.) are accepted.
- `NeedHeat`/`NeedOven`/`NeedMill` - placement gates.
- `RequiredExpansion` - `Expansion.ML` / `Expansion.SA` / etc. gate.
- `Recipe` - optional recipe scroll id, used for rare/quest recipes.
- `Mana`/`Stam`/`Hits` - resource cost to craft.
- `Quality`, `Exceptional`, `QuestItem` flags.

The `CraftItem.cs:896-1422` block is the runtime `Craft()` method, executed when the player clicks `MAKE NOW` in the craft gump. It is the canonical reading reference for "what does the engine actually check?"

## CraftSystem Registration DSL

The DSL methods are the public API. From `CraftSystem.cs:126-344`:

| Method | Purpose |
|---|---|
| `AddCraft(Type type, string name)` | Register a new craftable item. `type` is the produced `Item` subclass. |
| `AddRes(Type type, int amount = 1)` | Required resource. `type` is the consumed `Item` subclass. |
| `AddRes(Type type, string name, int amount, Func<...> text)` | Named subresource (e.g. wood type, ingot type, leather type). |
| `AddSkill(SkillName skill, double min, double max)` | Secondary skill requirement. |
| `SetNeededExpansion(Expansion e)` | Gate the recipe to `Core.ML`/`Core.SA`/etc. |
| `AddRecipe(int id, int? name = null)` | Bind a recipe scroll id to the recipe. Players must learn the scroll before they can craft. |
| `SetSubRes(Type type, string name)` | Subresource base type. Each skill has a base (Iron Ingot, Leather, Board, Cloth). |
| `SetUseSubRes(Type type, bool use)` | Whether the recipe should consume a specific subresource. |
| `SetUseAllRes(bool use)` | Multi-resource list (e.g. chainmail links). |
| `SetMaterial(bool fromSubRes)` | Whether the output inherits the subresource hue/material. |
| `SetNeedHeat(bool heat)` | Whether the recipe must be near a forge. |
| `SetNeedOven(bool oven)` | Whether the recipe must be near an oven. |
| `SetNeedMill(bool mill)` | Whether the recipe must be near a mill. |
| `SetMana(int mana)`, `SetStam(int stam)`, `SetHits(int hits)` | Resource cost to craft. |
| `SetQuality(IQuality quality)` | Quality strategy (`QualityNone`, `QualityVanq`, `QualityExceptional`). |
| `SetExceptional(bool exceptional)` | Whether the recipe can produce an exceptional. |
| `SetQuestItem(bool quest)` | Whether the produced item is quest-flagged. |
| `SetNonColorable()` | Item ignores subresource hue. |

The classic Blacksmithy example: `Projects/UOContent/Engines/Craft/DefBlacksmithy.cs` registers 143 craftable items (`docs/server-engine-knowledge-base.md:471`).

## Expansion and Recipe Gating

ML-era recipes follow a documented ID range pattern, captured in `docs/mondains-legacy-crafting-matrix.md:47-58`:

| ID range | System | Notes |
|---|---|---|
| 0-41 | Blacksmithy | Rare 0-3, 37; normal 4-31, 33-36, 38-41; quest 32 (Bone Machete) |
| 100-103 | Alchemy | Normal 100-102 (Invisibility, Darkglow, Parasitic); rare 103 (Hovering Wisp) |
| 200-212 | BowFletching | Rare 200-204, normal 205-212 |
| 300-321 | Carpentry | Mixed normal/rare |
| 400 | Inscription | Rare Scrapper's Compendium |
| 501-508 | Tailoring | Quivers 501-505; rare tailoring armor 506-508 |
| 600-602 | Tinkering | Rare jewelry |

Every ML-gated recipe calls `SetNeededExpansion(Expansion.ML)` in the `Def*.cs` registration. The runtime filter in `CraftItem.cs:904-916` enforces the gate against `Core.Expansion`.

To verify a recipe is correctly ML-gated in tests, the `MondainsLegacyCraftingCoverageTests.cs` regression file (referenced in `docs/mondains-legacy-crafting-matrix.md:23-45`) checks: known ML recipe IDs resolve through `Recipe.Recipes`; registered IDs point back to the expected craft system; every registered ML recipe is gated with `Expansion.ML`; expected ML craft systems expose at least one ML-gated item; ML-gated craft items have resources and the craft system's main skill.

## Subresources

Subresources are typed material choices (Iron vs. Dull Copper vs. Shadow Iron) that influence the produced item's hue and stat bonuses. The pattern in `CraftSystem.cs:295-331`:

- `SetSubRes(Type baseType, string name)` declares the base material category (Iron Ingot, Leather, Board, Cloth, ...).
- `AddRes(Type subType, string name, int amount, ...)` adds a specific material under the base. The player's selection in the craft gump determines which subresource is consumed.
- `SetUseSubRes(Type type, bool use)` opts in to subresource consumption.
- `SetMaterial(bool fromSubRes)` opts in to inheriting the subresource hue/material on the produced item.

`CraftItem.cs:62-94` and `CraftItem.cs:1305-1418` document the resource resolution at craft time. ML introduced rare subresource tiers: Oak, Ash, Yew, Heartwood for wood; the equivalent for ingots, leather, and cloth. Rare subresources are part of the `OakRunicFletchersTools`, etc. drop pool from Craftsman's Satchel and Fletching Satchel (`docs/mondains-legacy-content-matrix.md:73`).

## Recipe Scrolls

`Recipe` is the static registry of learned recipes, indexed by `int` id. Players learn recipes by double-clicking a `RecipeScroll` in their backpack; the scroll teaches the matching id and deletes itself if the player's skill is high enough. The `MondainsLegacyCraftingCoverageTests` regression verifies this with the `RecipeScroll` test (`docs/mondains-legacy-crafting-matrix.md:37`).

The recipe's `AddRecipe(int id, int? name = null)` line in `Def*.cs` binds a recipe id to a craftable item. Without a binding, the recipe has no entry in `Recipe.Recipes` and the scroll cannot teach it.

Rare recipe scroll sources (ML-era):

- Craftsman's Satchel drop pool - covers Alchemy, Blacksmithy, BowFletching, Carpentry, Tailoring normal recipes.
- Tinker satchels - normal non-artifact Alchemy, Blacksmithy, BowFletching, Carpentry, Tailoring branches; rare Inscription 400 (Scrapper's Compendium) and Alchemy 103 (Hovering Wisp) odds are tracked separately.
- Fletching Satchel and Carpentry Satchel - rare Oak/Ash/Yew/Heartwood Runic Fletcher's Tools / Dovetail Saws.
- Peerless boss drops (quest/ML recipes like Bone Machete) - source-defined per the item-properties plan.

## Durability Rules by Source

ML-era craftable weapons split into two durability bands (`docs/mondains-legacy-crafting-matrix.md:42`):

- Normal and magical ML craftable weapons: 36-48 durability (matches the in-game roll).
- Craftable artifact weapons: 255/255 (Soulbound-style maximum).

The plan's `ItemPropertyFlags.cs` work (tracked in `docs/superpowers/plans/2026-06-02-item-properties-completion.md:34-37`) introduces content-level saved flags for the new no-drop/no-trade/shard-bound properties. Recipe outputs will be a primary consumer: blessing an item at the forge, marking it as crafter-bound, etc.

## ICraftable and ICraftable.OnCraft

The runtime call path is `CraftItem.Craft() -> ICraftable.OnCraft(...)` for items that implement the interface (`Projects/UOContent/Engines/Craft/ICraftable.cs`). OnCraft is the post-craft hook to:

- Apply exceptional bonuses.
- Set the crafter's name (`MakeMark`).
- Roll the magical properties (for runic tools and ML rare recipes).
- Set the durability band.
- Set `LootType.Blessed` for quest items.
- Bind the item to a specific account (for content-level no-trade rules).

`BaseArmor`, `BaseWeapon`, `BaseClothing`, and `BaseJewel` all implement `ICraftable`. The hook fires after the resource and skill check pass.

## BOD (Bulk Order Deed) System

BODs are pre-rolled craft orders the player picks up from a BOD vendor (Smith or Tailor for ML). They are stored in the BOD engine under `Projects/UOContent/Engines/Bulk Orders`. The player crafts the small items listed on the BOD, double-clicks it, and the engine validates that the player has the right quantity of the right type with the right material.

The ML-era BOD behavior is described in `docs/mondains-legacy-content-matrix.md:78`:

- `MondainsLegacyRewardsCoverageTests` covers the Smith/Tailor BOD enum and vendor scope, ML BOD turn-in timer reset behavior, large tailor ShoeSet material combine rules, Tinker Guildmaster weapon-engraver recharge context, and the eight special ore hues for Colored Anvil / mining-glove rewards.
- The ML BOD turn-in inspection has a cooldown enforced post-ML; pre-ML has no cooldown.
- `BowcraftingBOD`, `TinkeringBOD`, `CarpentryBOD`, etc. are out of scope for the ML baseline (only Smith and Tailor are in `Distribution/Configuration/EraProfiles/ml-baseline.json`).

## Potion Subclass Behavior (Alchemy)

Alchemy is special because potions have type-specific effects. The `BasePotion` infrastructure lives under `Projects/UOContent/Items/Potions/`. ML extended the family:

- `InvisibilityPotion` - ML duration is 20 seconds + Alchemy scaling + Enhance Potions scaling; pre-ML fallback is 30 seconds flat.
- `DarkglowPotion` and `ParasiticPotion` - ML poison family profiles.
- `HoveringWisp` - rare ML Alchemy recipe using `CapturedEssence` (drop from Shimmering Effusion).

`PotionEffect` and the related classes apply the effect on `Drink`. The duration/strength scaling is in the Alchemy `Def*.cs` registration.

## Veteran and Promotional Reward Tooling

ML introduced "New Haven" reward tools that behave like craft tools with charges:

- `AmeliasToolbox` - blessed 500-use Tinkering reward (label `1077749`, item art `0x1EB8`, hue `1895`).
- `JacobsPickaxe` - blessed mining tool starting at 20 charges; recharges one use every five minutes; stays in place at 0 uses; sends localized message `1072306` when used empty.
- `HammerOfHephaestus` - same recharge behavior; applies +10 Blacksmithing equip bonus.

`NewHavenRewardToolTests` (referenced in `docs/mondains-legacy-content-matrix.md:62`) covers the toolbox reward shape, recharge cap, zero-charge message, non-breaking behavior, Jacob's mining bonus, and the Hammer equip/remove skill bonus.

## Common Recipes

### Adding a New ML-Gated Craftable Item

```csharp
// In DefBlacksmithy.cs inside Configure()
AddCraft(typeof(ElvenMachete), "Elven Weapons", "elven machete", 50.0, 100.0, typeof(IronIngot), 1044037, 10);
AddRes(typeof(Board), 1044041, 5);                  // Boards
AddSkill(SkillName.Tinkering, 50.0, 55.0);
SetNeededExpansion(Expansion.ML);
SetUseSubRes(typeof(IronIngot), true);
AddRecipe(0, 1075030);                              // Rare recipe scroll id 0
```

The runtime, when an ML client is detected and the player has the right resources, will allow the craft and call `ElvenMachete.OnCraft` (since `BaseWeapon` implements `ICraftable`).

### Adding a New Recipe Scroll Source

If the recipe should drop from a satchel, register the recipe id in the satchel's drop pool (`Projects/UOContent/Items/CraftSatchel*.cs` or similar). The `MondainsLegacyCraftingCoverageTests` regression verifies the satchel recipes resolve to the expected normal pool.

If the recipe is a quest reward, override the quest reward in the quest definition (e.g. `Projects/UOContent/Engines/ML Quests/Definitions/`) and call `AddRecipe` in the matching `Def*.cs`.

### Auditing ML Parity

Use the test files referenced in `docs/mondains-legacy-crafting-matrix.md:23-45` as the source-of-truth baseline:

1. Run `MondainsLegacyCraftingCoverageTests` - the current source-level baseline.
2. Run `CookingCraftingCoverageTests` for cooking-specific coverage.
3. Run `CraftGumpItemMondainsLegacyTests` for the rendered craft-detail gump packet, including the ML expansion cliloc and the learned/unlearned recipe button state.
4. For the runic tool drop parity, run the satchel tests referenced in the matrix.

Live QA gaps are listed in `docs/mondains-legacy-crafting-matrix.md:60-70` (rare recipe acquisition, Tinker satchel rare sourcing, peerless ingredient live drop rates, etc.) and are not part of the source-level baseline.

## Pitfalls

1. **Forgetting `SetNeededExpansion(Expansion.ML)`.** The recipe will appear on pre-ML shards and players can craft it. The `MondainsLegacyCraftingCoverageTests` regression catches this.
2. **Using the wrong `AddRes` overload.** The `(Type type, string name, int amount, Func<...> text)` form is for subresources; the `(Type type, int amount)` form is for plain resources. Mixing them produces null-resource crafts and silent success.
3. **Binding a recipe scroll id that is already used.** Recipe ids are global. `Recipe.Recipes` is a single registry; colliding ids cause the second registration to win. Always check `Recipe.Recipes` in the test.
4. **Forgetting `SetUseSubRes`.** Without it, the craft consumes any matching subresource and does not respect the player's material selection. With it but without `SetMaterial`, the produced item does not inherit the subresource hue.
5. **Hardcoding `RequiredExpansion` in `OnCraft` instead of `SetNeededExpansion`.** The `CraftItem` runtime check is the only reliable gate. If the runtime check is bypassed, the player can craft the item on pre-ML shards.
6. **Calling `AOS.Damage` from `OnCraft` to test the produced weapon.** OnCraft is a constructor-like context; the item is not in the world yet. The damage paths use the equipped Mobile's `Items` and will not see the produced item. Use a separate test that equips the item to a `PlayerMobile` and exercises the combat path.
7. **Setting `Stackable = true` on a craftable weapon output.** Weapons are non-stackable by UO convention. `Stackable` defaults to false and the engine's container-merge logic will refuse to merge them anyway, but the explicit `false` is clearer in the code.
8. **Inheriting the wrong `LootType`.** Crafted items default to `LootType.Regular` unless `SetQuestItem` is called or `OnCraft` sets a different type. Quest items need explicit `LootType.Blessed` and `BumpQuantity` for stackables.
9. **Forgetting to register a `BaseTool` requirement for the matching skill.** A craft that requires Blacksmithing but accepts no Forge gate will be craftable on a player with no tongs. `Def*.cs` lines like `AddCraft(typeof(...), ..., typeof(Forge), ...)` are how the system enforces tool requirements.
10. **Adding a recipe to a satchel that does not exist in `Distribution/Data`.** Satchels are content items with their own drop tables. Adding a recipe id to a satchel that no player can obtain breaks parity with the parity target.

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] The new `Def*.cs` line uses `SetNeededExpansion(Expansion.ML)` for any ML-gated recipe.
- [ ] The recipe id (if any) is not already registered in `Recipe.Recipes`.
- [ ] `MondainsLegacyCraftingCoverageTests` passes.
- [ ] `CraftGumpItemMondainsLegacyTests` renders the new recipe with the correct expansion cliloc and a `MAKE NOW` button reflecting learned/unlearned state.
- [ ] For a BOD-related change, `MondainsLegacyRewardServiceRuntimeTests` and `MondainsLegacyBodRewardColorTests` pass.
- [ ] For a subresource/hue inheritance change, a live test crafts an item with each of the relevant subresources and verifies the produced item's hue and stat bonuses.
- [ ] For a runic tool change, the satchel drop tables include the new tool at the expected rate.
- [ ] `OnCraft` is implemented for any non-default behavior (exceptional, makers mark, magical property roll, durability band).
- [ ] For quest items, `LootType.Blessed` is set, and the quest definition grants the recipe.
- [ ] For an in-progress check during development, `dotnet test --filter <recipe name or Def*>` runs the relevant test subset only.

## Related Skills

- `uo-items-foundation` - the produced item type (`BaseArmor`, `BaseWeapon`, `BaseClothing`, `BaseJewel`, etc.) and `ICraftable`; also hosts the cross-cutting reading recipe at `uo-items-foundation/references/analyzing-modernuo-subsystems.md` (use it before analyzing other UO subsystems).
- `uo-aos-item-properties` - the magical property roll applied to rare/exceptional/artifact outputs.
- `modernuo-content-patterns` - canonical templates for new content.
- `modernuo-era-expansion` - `Core.ML` / `Core.SA` gating for recipe visibility.
- `uo-bulk-orders-bod` - the BOD system is the canonical "I have to craft many items for a reward" path; the ML-era Smith/Tailor BOD turn-in flow consumes the same `Def*` registration.
- `docs/mondains-legacy-crafting-matrix.md` - the source-level parity map and recipe id range table.
- `docs/mondains-legacy-content-matrix.md` - broader feature matrix including the BOD system.
