# Mysticism: Healing Stone issue research notes

Use these notes as a compact evidence bank when drafting or reviewing a ModernUO/RebirthUO issue for the Mysticism spell **Healing Stone**. Do not copy mechanically; re-check sources if exact numbers drive implementation.

## Source set

- **Canonical — UO.com Mysticism page**: `https://uo.com/wiki/ultima-online-wiki/skills/mysticism/`
  - Lists Healing Stone as a first-circle Mysticism spell.
  - Words of power: `Kal In Mani`.
  - Reagents: Bone, Garlic, Ginseng, Spider's Silk.
  - Describes a large, non-transferable red gem in the caster's backpack with stored healing points.
  - Use requires a free hand.
  - On use, it attempts to cure or heal and deducts points.
  - Says the stone fully recharges in **20 seconds**.
  - Stone lasts until points are used up or it is dropped on the floor.
- **Canonical — Publish 60 / Stygian Abyss**: `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`
  - Introduces Mysticism and lists Healing Stone: “Conjures a Healing Stone that will instantly heal the Caster when used.”
- **Canonical — Publish 65 Mysticism Revamp**: `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2010-2/publish-65/`
  - Changes Healing Stone to stored life/healing points based on Mysticism and Focus/Imbuing.
  - Max heal per use is determined by Mysticism and Focus/Imbuing.
  - Adds healing energy that is consumed per use and replenishes over time.
  - Gives a **2-second** use cooldown and **15-second** full replenish.
  - Adds poison cure support with cost by poison level; failed cures cost one-third of the life-energy cost.
  - Says summoning time was increased significantly.
- **Community/reference — UOGuide Healing Stone**: `https://www.uoguide.com/Healing_Stone`
  - Mana cost 4, minimum Mysticism 0, casting delay shown as 5, caster-only use, blessed/non-transferable behavior, disappears if dropped.
  - Repeats Publish 65 changes and the 15-second replenish model.
- **Engine precedent — ServUO**:
  - Spell: `https://github.com/ServUO/ServUO/blob/master/Scripts/Spells/Mysticism/SpellDefinitions/HealingStoneSpell.cs`
  - Item: `https://github.com/ServUO/ServUO/blob/master/Scripts/Items/Consumables/HealingStone.cs`
  - Registration: spell ID `678` in the Mysticism block.
  - Spell uses first circle, 4 mana via Mystic base, 5-second `CastDelayBase`, Bone/Garlic/Ginseng/Spider's Silk, and creates/replaces a caster-bound `HealingStone` in backpack.
  - Item precedent uses finite life force, max-heal-per-use, 2-second use cooldown, 15 one-second recharge ticks, free-hand check, non-transferable/blessed behavior, drop-to-world delete, secure-trade refusal, serialization, and timer cleanup.

## Repo anchors observed in ModernUO/RebirthUO

- `Projects/UOContent/Spells/Initializer.cs`: SA Mysticism block exists; Healing Stone registration at spell ID `678` may be commented out in incomplete implementations.
- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs`: Mysticism base handles CastSkill, mana table, required skill table, Focus/Imbuing support skill via `GetDamageSkill()`.
- `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs`: `BookOffset => 677`, `BookCount => 16`; Healing Stone is the second Mystic spellbook slot / spell ID `678`.

## Conflicts to surface in issues

When drafting, do not collapse these into one confident value:

1. **Recharge duration**
   - UO.com current Mysticism page says 20 seconds.
   - Publish 65, UOGuide, and ServUO use/describe 15 seconds.
   - Suggested issue default: 15 seconds, because Publish 65 is the explicit revamp note and engine precedent matches it.
2. **Cast delay**
   - Current UO.com circle table says first-circle delay 0.50 seconds.
   - Publish 65 says Healing Stone summoning time increased significantly.
   - ServUO uses 5 seconds.
   - Suggested issue default: 5 seconds for PvP safety and Publish 65 alignment.
3. **Poison cure formula**
   - Official/community text says chance-based by Mysticism plus Focus/Imbuing and poison level.
   - ServUO precedent is closer to a deterministic energy-threshold/cost check.
   - Suggested issue default: require an explicit RebirthUO decision and test the final formula.

## Issue-writing reminder

Use the `spell.yml` template. Include `Observed conflict`, `Likely interpretation`, and `Decision needed` in `## Formulas / Values / Duration` or `## Open Questions` for the three conflicts above. Keep PvP and economy/storage side effects explicit: free hand, 2-second use cooldown, finite energy, caster-only/non-transferable behavior, drop/delete behavior, and persistence/timer cleanup.