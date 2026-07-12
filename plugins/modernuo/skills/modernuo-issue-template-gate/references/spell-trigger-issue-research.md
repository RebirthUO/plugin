# Spell Trigger Issue Research Notes

Session-derived reference for drafting SA/Mysticism spell issues, especially when the repository has partial spellbook/scroll support but the spell class is missing.

## Durable research pattern

1. **Use the spell issue template first.** For player-facing spells such as Mysticism: Spell Trigger, select `spell.yml` and preserve its exact field order.
2. **Resolve official era/publish through UO.com REST when direct publish slugs fail.** UO.com's current publish index may not expose older `technical/previous-publishes/...` pages through the simple `/publish-notes/publish-<n>/` pattern. Use WordPress REST search terms such as `Publish 60`, `Stygian Abyss Mysticism`, or the expansion name to discover the canonical page URL.
3. **Use UOGuide MediaWiki `parse` for page text.** Browser fetches can hang or SSL-timeout on individual UOGuide pages. The API usually returns usable page text for `Mysticism`, `Spell Trigger`, and `Ultima Online: Stygian Abyss`.
4. **Use engine precedent as precedent, not canon.** `gh search code` plus raw GitHub URLs can locate ServUO spell implementations. Treat those as implementation hints; prefer UO.com when values conflict.
5. **Cross-check local partial implementation.** Search/read local anchors for:
   - `Projects/UOContent/Spells/Initializer.cs` registration gate and commented spell ID.
   - `Projects/UOContent/Spells/Mysticism/MysticSpell.cs` base mana/skill/support-skill/cast-delay tables.
   - Mystic scroll classes under `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/`.
   - `Projects/UOContent/Engines/Craft/DefInscription.cs` spell scroll recipes.
   - `MysticSpellbook.cs` and `Spellbook.cs` spell ID range/book offset.

## Spell Trigger facts captured

- Official source: UO.com Mysticism and UO.com Publish 60, 8 September 2009.
- Initial era: Stygian Abyss (SA).
- Initial publish: Publish 60.
- Spell ID in ModernUO/RebirthUO: 685.
- Mystic spellbook offset: 677; 16 Mystic spell slots.
- Circle: Fifth.
- Mana: 14.
- Min Mysticism: 45.0.
- Reagents: Dragon's Blood, Garlic, Mandrake Root, Spider's Silk.
- UO.com current page: 1.50 second fifth-circle delay, 5-minute cooldown, max stored circle scales with Mysticism plus Focus/Imbuing.
- UOGuide dedicated Spell Trigger page conflict: labels `Delay` as 5 seconds and `Duration` as 5 minutes.
- Suggested default for issues: prefer UO.com current spell table and existing `MysticSpell` base delay; document the UOGuide conflict rather than silently choosing.

## Label creation lesson

If the selected template's class label (for example `spell`) is missing but adjacent low-risk UO labels already exist (`ultima-online`, `triage`, another class label), create the missing class label before `gh issue create` when authenticated and the task is to create the issue. Use the existing class-label color/description convention where visible; otherwise report the blocker instead of creating an off-template issue.
