# uo.com Creature / Monster Ability Audit Notes

Use this reference when auditing the configured ModernUO-based repository's
monster abilities against current official UO creature or pet documentation.

## Official source shape

- uo.com does not currently expose a dedicated `monster-abilities` or `creature-abilities` master page under the obvious combat/PvM slugs.
- For a current official master list of trainable creature/pet abilities, start with:
  - `https://uo.com/wiki/ultima-online-wiki/skills/animal-taming/animal-training-abilities/`
  - WordPress search result id observed in June 2026: `13571`
  - REST route shape: `https://uo.com/wp-json/wp/v2/wiki-page/13571`
- The page groups abilities into four categories:
  - Magical Abilities/packages: Piercing, Bashing, Slashing, Battle Defense, Wrestle Mastery.
  - Special Abilities: Angry Fire, Conductive Blast, Dragon Breath, Grasping Claw, Inferno, Lightning Force, Mana Drain, Raging Breath, Repel, Searing Wounds, Steal Life, Venomous Bite, Vicious Bite, Rune Corruption, Life Leech, Sticky Skin, Tail Swipe.
  - Special Moves: mostly normal weapon special moves, with creature notes for Cold Wind, Frenzied Whirlwind, and Whirlwind Attack.
  - Area Effect Abilities: Aura of Energy, Explosive Goo, Essence of Earth, Aura of Nausea, Poison Breath, Essence of Disease.

## Audit workflow

1. Verify the official page live via WP search/API or HTML fetch; do not assume an old copied list is complete.
2. Try obvious dedicated `monster-abilities` / `creature-abilities` slugs only as a discovery check. If they 404, record that and use Animal Training Abilities as the official master list.
3. Extract the configured repository in three layers, not one:
   - `Projects/UOContent/Mobiles/Abilities/MonsterAbilities.cs` factory properties.
   - Recursive `Projects/UOContent/Mobiles/Abilities/**/*.cs` concrete classes, including subfolders such as `Fire Breath/` and `Summon Undead/`.
   - `Projects/UOContent/Items/Weapons/Abilities/**/*.cs` for official Special Moves.
4. Classify results conservatively:
   - `Present as MonsterAbility` when a named or very close monster ability exists.
   - `Present as WeaponAbility` when the special move exists only in the weapon-special system.
   - `Partial/similar` when a legacy ability resembles the official page but differs in name, formula, trigger, area behavior, or poison/damage level.
   - `Not found` when normalized class/file search finds no matching implementation.
5. Separate pet-training package choices from combat procs. Piercing/Bashing/Slashing/Battle Defense/Wrestle Mastery are package choices on uo.com; implementing them likely belongs in an Animal Training / pet ability-selection layer, not only `MonsterAbility`.

## Common pitfalls

- Do not claim official creature specials are missing merely because they are not `MonsterAbility` classes; many uo.com Special Moves already exist as `WeaponAbility` classes.
- Do not claim a similar legacy effect is complete without checking formula, trigger chance, cooldown, target filter, poison level, and era gate.
- Do not treat repo-only abilities as wrong just because uo.com Animal Training omits them. Legacy creature specials such as summon counters, death explosions, ninja/yomotsu abilities, and named-boss abilities may be era- or monster-specific.
- Include the repo baseline (`branch`, `HEAD`, and clean/dirty status) and keep generated audit reports outside the repo unless the user asks to add documentation.
