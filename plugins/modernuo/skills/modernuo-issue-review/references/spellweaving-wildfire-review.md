# Spellweaving Wildfire issue-review notes

Use for RebirthUO/ModernUO issue reviews or implementation scoping involving the ML Spellweaving `Wildfire` spell.

## Source findings

- Canonical/current UO.com Spellweaving row lists Wildfire as `30(50)` mana, `2.5` cast delay, minimum skill `66`, fire damage formula, multi-target split, 1-5 second duration, 5-tile radius plus focus, and says it does **not** damage hidden characters.
- UOGuide Wildfire is useful community/historical support: mana `50`, minimum skill `66.0`, cast delay `2.5`, duration `(Spellweaving Skill x 10) / 240`, 5-11 tile radius, +1 radius/damage/second per focus, once-per-second valid-target damage, extra fire columns, and caster LOS required to targets.
- UOGuide Spellweaving says Spellweaving was introduced with Mondain's Legacy. Do not claim a numbered publish for Wildfire unless a canonical publish note specifically introducing it is found.

## RebirthUO implementation-review defaults

- Resolve UO.com's parenthesized Spellweaving mana notation by checking existing repo classes. RebirthUO stores the parenthesized value as `RequiredMana` for current Spellweaving spells, e.g. `Arcane Circle` 14(24) -> 24, `Thunderstorm` 19(32) -> 32, `Essence of Wind` 24(40) -> 40, `Word of Death` 30(50) -> 50. Therefore Wildfire should default to `RequiredMana = 50` unless a broader Spellweaving display/cost model is introduced.
- Resolve formula scale against local skill units. UO.com's `/ 240` player-facing formula corresponds to UOGuide's `(Spellweaving Skill x 10) / 240`; with RebirthUO `Skills.Spellweaving.Value` represented as 0.0-120.0, tests should expect integer-style `skill / 24` for the skill-derived duration/damage component plus focus.
- For placement/region policy, use existing RebirthUO field and harmful-target helpers for the first slice: `SpellHelper.CheckTown`, `SpellHelper.AdjustField`, `ValidIndirectTarget`, `CanBeHarmful`, `DoHarmful`, and LOS checks. ServUO's stricter BaseHouse/guarded checks are engine precedent but should not override current RebirthUO field policy without a separate housing/field policy issue.

## Repo anchors to verify live

- `Projects/UOContent/Spells/Initializer.cs`: ML block has `// Register(609, typeof(WildfireSpell));` when the spell is missing.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/SpellweavingScrolls.cs`: `WildfireScroll` uses spell ID `609`, item ID `0x2D5A`, hue `0x8FD`.
- `Projects/UOContent/Items/Skill Items/Magical/SpellweavingBook.cs`: `BookOffset => 600`, `BookCount => 16`.
- `Projects/UOContent/Spells/Spellweaving/ArcanistSpell.cs`: ML expansion support, quest gate, required skill/mana, focus capture, fizzle behavior.
- `Projects/UOContent/Spells/Spellweaving/Thunderstorm.cs` and `EssenceOfWind.cs`: area target collection, focus scaling, SDI/PvP-cap precedent.
- `Projects/UOContent/Spells/Fourth/FireField.cs`: temporary field lifecycle, timer cleanup, damage-on-tick, `AOS.Damage` fire damage.

## Issue-review wording pattern

When the only remaining questions are Wildfire mana notation, skill-scale rounding, and region/house policy, they can usually be moved from `## Open Questions` into `## Resolved Questions` as implementation-policy decisions if the live repo anchors above still match and no source conflict remains. Set `## Remaining Open Questions` to `None blocking` and remove `triage` only after verifying the body contains research notes and no stale blocking heading remains.
