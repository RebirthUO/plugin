# Era Parity Aspects — Scan Paths & Source URLs

Forty-seven aspects for fine-grained era parity. For each aspect:

1. Scan the **repo paths** below (grep + read era doc section)
2. Cross-check **UO.com** then **UOGuide** starting URLs
3. Emit summary coverage + entity rows for `Partial`/`Gap`/`RuntimeBlocked` items

Paths are relative to repo root. Era gating: `Core.*`, `dev-docs/eras/{slug}.md`, `Distribution/Configuration/EraProfiles/`.

---

## 1. Races

| Repo paths | `Projects/UOContent/Mobiles/PlayerMobile.cs`, `Projects/UOContent/Races/`, `CharacterCreation.cs` |
|---|---|
| UO.com | [Racial abilities](https://uo.com/wiki/ultima-online-wiki/player/racial-abilities/) |
| UOGuide | [Races](https://www.uoguide.com/Races), [Elves](https://www.uoguide.com/Elves), [Gargoyle Race](https://www.uoguide.com/Gargoyle_Race) |

Check: Human (always), Elf (`Core.ML`), Gargoyle (`Core.SA`), racial abilities, stat bonuses, body restrictions.

---

## 2. Skills

| Repo paths | `Distribution/Data/skills.json`, `Projects/UOContent/Skills/`, `SkillsInfo.cs` |
|---|---|
| UO.com | [Skills](https://uo.com/wiki/ultima-online-wiki/skills/) |
| UOGuide | [Skills](https://www.uoguide.com/Skills) |

Check: skill count, caps, gain formulas, era-gated skills (Bushido `Core.SE`, Spellweaving `Core.ML`, Mysticism/Imbuing `Core.SA`, Skill Mastery `Core.TOL`). Respect EraProfile blocks.

---

## 3. Stats

| Repo paths | `Projects/Server/Mobiles/Mobile.cs`, `SetStr/SetDex/SetInt`, `SkillsInfo.Configure()`, stat locks |
|---|---|
| UO.com | [Player stats](https://uo.com/wiki/ultima-online-wiki/player/) |
| UOGuide | Stat cap pages under Skills/Player |

Check: 225 cap, stat locks, natural vs item stat influence, era-specific caps.

---

## 4. Spells

| Repo paths | `Projects/UOContent/Spells/`, `Spells/Initializer.cs`, per-school folders |
|---|---|
| UO.com | [Magery](https://uo.com/wiki/ultima-online-wiki/skills/magery/), [Necromancy](https://uo.com/wiki/ultima-online-wiki/skills/necromancy/), [Chivalry](https://uo.com/wiki/ultima-online-wiki/skills/chivalry/), [Mysticism](https://uo.com/wiki/ultima-online-wiki/skills/mysticism/) |
| UOGuide | [Spells](https://www.uoguide.com/Spells), [Magery](https://www.uoguide.com/Magery), [Necromancy](https://www.uoguide.com/Necromancy), [Chivalry](https://www.uoguide.com/Chivalry), [Mysticism](https://www.uoguide.com/Mysticism), [Spellweaving](https://www.uoguide.com/Spellweaving), [Bushido](https://www.uoguide.com/Bushido), [Ninjitsu](https://www.uoguide.com/Ninjitsu) |

Check: spell IDs, mana/reagent costs, circle/level, summon caps, school unlock quests.

---

## 5. Item Properties

| Repo paths | `Projects/UOContent/Misc/AOS.cs`, `IAosItem`, `GetProperties` on gear |
|---|---|
| UO.com | [Magic item properties](https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/), [Base properties](https://uo.com/wiki/ultima-online-wiki/items/base-properties/) |
| UOGuide | [Item Properties](https://www.uoguide.com/Item_Properties) |

Check: property enum coverage, intensity ranges, caps, negative properties, SA/TOL additions.

---

## 6. Armor

| Repo paths | `Projects/UOContent/Items/Armor/`, `BaseArmor.cs`, SE/ML/SA armor subclasses |
|---|---|
| UO.com | [Items](https://uo.com/wiki/ultima-online-wiki/items/) |
| UOGuide | Armor pages under Items |

Check: material bonuses, durability, medable/non-medable, era-specific armor types (SE samurai armor, gargish `Core.SA`).

---

## 7. Weapons

| Repo paths | `Projects/UOContent/Items/Weapons/`, `BaseWeapon.cs`, `SE Weapons/` |
|---|---|
| UO.com | [Items](https://uo.com/wiki/ultima-online-wiki/items/) |
| UOGuide | Weapon index under Items |

Check: weapon types per era, swing speed, specials assignment, SE weapons (no-dachi, tekagi, etc.).

---

## 8. Shields

| Repo paths | `Projects/UOContent/Items/Armor/BaseShield.cs`, shield subclasses |
|---|---|
| UO.com | Items wiki |
| UOGuide | Shield pages |

---

## 9. Jewelry

| Repo paths | `Projects/UOContent/Items/Jewelry/`, `BaseJewel.cs` |
|---|---|
| UO.com | Items wiki |
| UOGuide | Jewelry under Items |

---

## 10. Talismans

| Repo paths | `Projects/UOContent/Items/Talismans/`, `BaseTalisman.cs` |
|---|---|
| UO.com | Talisman pages (ML+) |
| UOGuide | Talisman pages |

Era: `Core.ML` baseline.

---

## 11. Clothing

| Repo paths | `Projects/UOContent/Items/Clothing/`, `BaseClothing.cs` |
|---|---|
| UO.com | Items wiki |
| UOGuide | Clothing under Items |

---

## 12. Item Sets

| Repo paths | `Projects/UOContent/Items/Armor/Sets/`, `Items/Sets/ItemSetHelper.cs`, `ArmorSetItem.cs` |
|---|---|
| UO.com | Item sets (ML event sets) |
| UOGuide | [Item set](https://www.uoguide.com/Item_set) |

---

## 13. Artifacts

| Repo paths | `Projects/UOContent/Items/**/Artifacts/`, `ArtifactRarity`, stealable tables |
|---|---|
| UO.com | [Artifact collections](https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/) |
| UOGuide | [Artifacts](https://www.uoguide.com/Artifacts), [Artifacts (Doom)](https://www.uoguide.com/Artifacts_(Doom)), [Artifacts (Peerless)](https://www.uoguide.com/Artifacts_(Peerless)) |

Group by source: Doom, Peerless, Champion, Tokuno, SA, etc.

---

## 14. Veteran Rewards

| Repo paths | `Projects/UOContent/Engines/Veteran Rewards/`, `RewardSystem.cs` |
|---|---|
| UO.com | Veteran rewards pages |
| UOGuide | Veteran reward pages |

---

## 15. Craftables

| Repo paths | `Projects/UOContent/Engines/Craft/Def*.cs`, `CraftItem.cs`, `InitCraftList()` |
|---|---|
| UO.com | [Crafting](https://uo.com/wiki/ultima-online-wiki/gameplay/crafting/), [Complete recipe list](https://uo.com/wiki/ultima-online-wiki/gameplay/crafting/complete-recipe-list/) |
| UOGuide | [Crafting](https://www.uoguide.com/Crafting) |

Check: recipes per profession, rare recipes, era-gated craftables.

---

## 16. Resources

| Repo paths | `Projects/UOContent/Misc/ResourceInfo.cs`, `CraftResource`, harvest outputs |
|---|---|
| UO.com | Material bonuses, resources |
| UOGuide | [Resources](https://www.uoguide.com/Resources) |

---

## 17. Plants & Seeds

| Repo paths | `Projects/UOContent/Engines/Plants/`, seed items, `PlantSystem` |
|---|---|
| UO.com | Gardening/plant pages |
| UOGuide | Plant/seed pages |

---

## 18. Rares

| Repo paths | Rare item subclasses, holiday items, server-spawned decor |
|---|---|
| UO.com | Limited |
| UOGuide | Rare item community lists |

Label `Unverified` when only community-sourced.

---

## 19. Facets

| Repo paths | `Distribution/Data/map-definitions.json`, `Map.cs`, `MapLoader.cs` |
|---|---|
| UO.com | [World](https://uo.com/wiki/ultima-online-wiki/world/) |
| UOGuide | [Facets](https://www.uoguide.com/Facets) |

Check: Felucca, Trammel, Ilshenar, Malas, Tokuno (`Core.SE`), Ter Mur (`Core.SA`), Valley of Eodon (`Core.TOL`).

---

## 20. Cities & Towns

| Repo paths | `Distribution/Data/regions.json` (`TownRegion`, `GuardedRegion`), `Locations/*.json` |
|---|---|
| UO.com | [World / towns](https://uo.com/wiki/ultima-online-wiki/world/) |
| UOGuide | [Atlas](https://www.uoguide.com/Atlas) |

---

## 21. Dungeons

| Repo paths | `DungeonRegion` in `regions.json`, decoration cfg, spawn JSON per dungeon |
|---|---|
| UO.com | World wiki dungeon pages |
| UOGuide | [Dungeons](https://www.uoguide.com/Dungeons) |

---

## 22. Animals

| Repo paths | `Projects/UOContent/Mobiles/Animals/`, tameable `BaseCreature` subclasses |
|---|---|
| UO.com | Creatures / taming |
| UOGuide | Animal pages, [Animal Taming](https://www.uoguide.com/Animal_Taming) |

---

## 23. Monsters

| Repo paths | `Projects/UOContent/Mobiles/Monsters/`, era subfolders (`SE/`, `ML/`, `SA/`) |
|---|---|
| UO.com | [PvM](https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/) |
| UOGuide | [Monsters](https://www.uoguide.com/Monsters), [Named Monsters](https://www.uoguide.com/Named_Monsters) |

Primary entity-level parity surface. Cross-ref era doc mobile tables.

---

## 24. Champion Spawns

| Repo paths | `Projects/UOContent/Engines/CannedEvil/`, `ChampionSpawnInfo.cs`, `ChampionSpawn.cs` |
|---|---|
| UO.com | [Champion spawns](https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/champion-spawns/) |
| UOGuide | [Champion spawn](https://www.uoguide.com/Champion_spawn) |

Check: spawn types, champions, idols, Power Scrolls, Scrolls of Transcendence.

---

## 25. Doom Gauntlet

| Repo paths | `Projects/UOContent/Engines/Doom/`, `GauntletSpawner.cs`, Doom artifacts |
|---|---|
| UO.com | Doom pages |
| UOGuide | [Doom](https://www.uoguide.com/Doom) |

Era: `Core.AOS`.

---

## 26. Peerless

| Repo paths | `Projects/UOContent/Engines/Peerless/`, boss classes, `PeerlessAltar`, ML quest keys |
|---|---|
| UO.com | [Peerless quests](https://uo.com/wiki/ultima-online-wiki/gameplay/quests/peerless-quests/) |
| UOGuide | [Peerless](https://www.uoguide.com/Peerless) |

ML: use `MondainsLegacySourceReferences`. Check key lifecycle, altar states, boss specials.

---

## 27. PvP

| Repo paths | `Projects/UOContent/Engines/ConPVP/`, arena systems, `PlayerMobile` PvP flags |
|---|---|
| UO.com | [Combat / PvP](https://uo.com/wiki/ultima-online-wiki/combat/) |
| UOGuide | PvP pages |

---

## 28. Criminal

| Repo paths | `Criminal` flag logic on `Mobile`, guard behavior, `GuardedRegion` |
|---|---|
| UO.com | Player / criminal pages |
| UOGuide | Criminal system pages |

---

## 29. Murderer

| Repo paths | `PlayerMobile` murder counts, red status, `MurderContext` |
|---|---|
| UO.com | [Murder system](https://uo.com/wiki/ultima-online-wiki/player/the-murder-system/) |
| UOGuide | Murder/red pages |

---

## 30. Vice vs Virtue

| Repo paths | `Projects/UOContent/Engines/VvV/` |
|---|---|
| UO.com | Vice vs Virtue pages |
| UOGuide | VvV pages |

Era: publish-dependent; often `Gap` on custom shards.

---

## 31. Damage Calculations

| Repo paths | `BaseWeapon.cs`, `AOS.cs`, `GetNewAosDamage`, resist application, `Core.AOS` branches |
|---|---|
| UO.com | [Melee damage increase](https://uo.com/wiki/ultima-online-wiki/skills/melee-fighting/melee-damage-increase/), combat wiki |
| UOGuide | Damage formula pages |

Check pre-AOS vs AOS+ branches, DI caps, resist math.

---

## 32. Special Moves

| Repo paths | `Projects/UOContent/Items/Weapons/Abilities/`, `WeaponAbility`, `SpecialMove.cs` |
|---|---|
| UO.com | [Special moves](https://uo.com/wiki/ultima-online-wiki/combat/special-moves/) |
| UOGuide | [Special move](https://www.uoguide.com/Special_move) |

Check weapon assignment, mana costs, Bushido/Ninjitsu moves in `SpellRegistry.SpecialMoves`.

---

## 33. Templates

| Repo paths | `LootPack`, spawn templates, `ChampionSpawnInfo.Table`, treasure map levels |
|---|---|
| UO.com | Loot generation, spawn pages |
| UOGuide | Template-related pages |

---

## 34. Crafting

| Repo paths | `Projects/UOContent/Engines/Craft/`, `CraftSystem`, BOD integration |
|---|---|
| UO.com | [Crafting](https://uo.com/wiki/ultima-online-wiki/gameplay/crafting/) |
| UOGuide | [Crafting](https://www.uoguide.com/Crafting) |

Includes success chance, resource consumption, runic/imbuing (SA).

---

## 35. Trading

| Repo paths | `TradeSystem`, `SecureTrade`, vendor buy/sell, `BaseVendor` |
|---|---|
| UO.com | Gameplay / economy |
| UOGuide | Trading, vendor pages |

---

## 36. Pets

| Repo paths | `AnimalTaming.cs`, `BaseCreature` control slots, `AnimalTrainer` (Publish 97) |
|---|---|
| UO.com | [Animal taming](https://uo.com/wiki/ultima-online-wiki/skills/animal-taming/), Publish 97 |
| UOGuide | [Animal Taming](https://www.uoguide.com/Animal_Taming) |

Check taming, stabling, pet bonding, animal training (`Core.TOL`+).

---

## 37. Houses & Boats

| Repo paths | `Projects/UOContent/Multis/Houses/`, `HousePlacement`, `High Seas` ship code |
|---|---|
| UO.com | Housing, ships (HS) |
| UOGuide | Housing, boat pages |

Check `Core.HS` for naval content.

---

## 38. Quests

| Repo paths | `Engines/Quests/`, `Engines/ML Quests/Definitions/` |
|---|---|
| UO.com | [Quests](https://uo.com/wiki/ultima-online-wiki/gameplay/quests/) |
| UOGuide | [Quest](https://www.uoguide.com/Quest), [List of Quests](https://www.uoguide.com/List_of_Quests) |

---

## 39. NPCs

| Repo paths | `Projects/UOContent/Mobiles/Vendors/`, `Mobiles/Townfolk/`, spawn JSON |
|---|---|
| UO.com | NPC/quest giver pages |
| UOGuide | [List of Quest NPCs](https://www.uoguide.com/List_of_Quest_NPCs) |

---

## 40. Virtues

| Repo paths | `Projects/UOContent/Engines/Virtues/`, `VirtueName`, per-virtue files |
|---|---|
| UO.com | Virtue pages |
| UOGuide | Virtue pages |

---

## 41. Cooperative Collections

| Repo paths | `Projects/UOContent/Engines/Collections/` |
|---|---|
| UO.com | Cooperative collection pages (ML) |
| UOGuide | Collection pages |

---

## 42. Formulas and Game Mechanics

| Repo paths | Cross-cutting: `SkillsInfo`, loot gen, skill gain, luck, insurance, resists |
|---|---|
| UO.com | [Loot generation](https://uo.com/wiki/ultima-online-wiki/items/loot-generation/), publish notes |
| UOGuide | Mechanics pages per system |

Catch-all for formulas not covered above: insurance (`Core.AOS`), luck, skill gain (`Core.ML` adjustments), etc.

---

## UOGuide URL Convention

- Base: `https://www.uoguide.com/{Title_With_Underscores}`
- Spaces → `_`; apostrophes → `%27` when needed
- Creature example: `Yomotsu_Elder` → `https://www.uoguide.com/Yomotsu_Elder`

## Accuracy Grading (per row)

| Grade | Criteria |
|---|---|
| 90–100% | UO.com + UOGuide agree; repo matches field-by-field |
| 70–89% | Sources agree; repo mostly matches; minor stat/skill deltas |
| 50–69% | Partial implementation or source disagreement on non-critical fields |
| 30–49% | Major gaps (missing abilities, wrong loot, unwired spawns) |
| 0–29% | Missing type, wrong era, or only unverified emulator sources |
