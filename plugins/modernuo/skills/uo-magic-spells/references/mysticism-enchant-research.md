# Mysticism Enchant research notes

Use when reviewing or implementing the Stygian Abyss Mysticism spell **Enchant**.

## Source findings

- **UO.com Mysticism page** (`https://uo.com/wiki/ultima-online-wiki/skills/mysticism/`) lists Enchant as second-circle Mysticism (`In Ort Ylem`) with Spider's Silk, Mandrake Root, and Sulfurous Ash. It adds up to 60 Hit Spell chosen from Fireball, Harm, Magic Arrow, Lightning, or Dispel. If Focus or Imbuing are over 80 it also adds Spell Channeling and `-1 Faster Casting`. Duration scales based on the selected spell level with a 150-second base/cap. The spell is cancelled if the weapon is disarmed.
- **UO.com Publish 60** (`https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`) introduces Enchant as a temporary weapon hit-spell enchant. Launch wording says Imbuing and Mysticism over 80 allow casting Magery or Mysticism while holding the weapon.
- **UO.com / UOGuide Publish 64** changes Mysticism support from Imbuing-only to either Focus or Imbuing and removes Evaluate Intelligence from Mystic spell power.
- **UO.com / UOGuide Publish 65** increases Enchant base duration and says duration scales based on the level of the enchanted spell.
- **UOGuide Enchant** (`https://www.uoguide.com/Enchant`) corroborates mana 6, minimum skill 8, delay 0.75s, single-item target, reagents, up to ~150s duration, and the Mysticism + either Focus or Imbuing >80 equipped-casting behavior.

## Implementation defaults for RebirthUO/ModernUO issues

- Target **post-Publish 64/65 current-SA behavior** by default unless the shard explicitly asks for launch-day SA.
- Spell Channeling threshold: require Mysticism at/over the documented 80 threshold and `max(Focus, Imbuing)` at/over the documented 80 threshold before applying temporary Spell Channeling and `-1 Faster Casting`.
- Duration: official sources do **not** provide exact numeric per-option duration values. Treat the acceptance rule as: selected-spell-level scaling with a 150-second base/cap. Choose a deterministic table during implementation, document it in tests, and do not block issue triage solely on the missing official formula.

## Repo anchors to verify

- `Projects/UOContent/Spells/Initializer.cs` — spell ID 680 is commonly still commented out as `EnchantSpell`.
- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs` — should already use `max(Focus, Imbuing)` support skill from Publish 64.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/EnchantScroll.cs` — scroll surface exists for spell ID 680.
- `Projects/UOContent/Engines/Craft/DefInscription.cs` — SA inscription should expose `EnchantScroll` with Spider's Silk, Mandrake Root, Sulfurous Ash.
- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs` — `BuffIcon.Enchant` exists.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` — hit-spell pipeline reads `AosWeaponAttributes` for Hit Magic Arrow/Harm/Fireball/Lightning/Dispel and equipped casting checks `Attributes.SpellChanneling`.

## ServUO precedent caveats

- ServUO has useful Enchant implementation precedent: selection gump, `ClearHandsOnCast = false`, conflict checks, temporary hit-spell/channeling attributes, `BuffIcon.Enchant`, and cleanup on weapon removal.
- ServUO's raw file path is unusual: `Scripts/Spells/Mysticism/SpellDefinitions/EnchantSpell .cs` includes a space before `.cs`. If a raw guessed URL 404s, list the Git tree first.
- Treat ServUO's skill-only duration formula, e.g. `((Mysticism + support) / 2) + 30`, as emulator precedent only. It conflicts with the official selected-spell-level wording from Publish 65/current UO.com.
