# Mysticism: Purge Magic research notes

Use these notes when drafting or implementing a RebirthUO/ModernUO Purge Magic issue or PR. They condense one issue-intake session and should be treated as research breadcrumbs, not a full parity spec.

## Source hierarchy

- Canonical current mechanics: `https://uo.com/wiki/ultima-online-wiki/skills/mysticism/`
  - Purge Magic is a second-circle Mysticism spell.
  - Mana: 6.
  - Delay: 0.75 seconds.
  - Minimum skill: 8.0.
  - Reagents: Fertile Dirt, Garlic, Mandrake Root, Sulfurous Ash.
  - Attempts to remove a target's buff/beneficial ward; if no purgeable ward exists, applies mana disruption.
- Canonical launch history: `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`
  - Publish 60 / Stygian Abyss introduced Mysticism and lists Purge Magic as removing a randomly chosen beneficial ward.
- Canonical revamp history: `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2010-2/publish-65/`
  - Publish 65 documents the no-ward mana-disruption effect and additional purge immunity after disruption.
- Community/reference cross-checks:
  - `https://www.uoguide.com/Purge_Magic`
  - `https://www.uoguide.com/Mysticism`
  - `https://www.uoguide.com/Publish_60`
  - `https://www.uoguide.com/Publish_65`
- Engine precedent:
  - ServUO: `Scripts/Spells/Mysticism/SpellDefinitions/PurgeMagicSpell.cs`
  - GitHub code search query: `PurgeMagicSpell repo:ServUO/ServUO`

## Mechanics summary

- School: Mysticism.
- Circle: Second.
- Words of power: `An Ort Sanct`.
- Target: harmful mobile target.
- Primary behavior: remove one valid beneficial ward from the target, chosen randomly.
- Skill comparison: caster Mysticism plus Focus/Imbuing support skill vs target Resisting Spells and the ward's difficulty/level.
- No-ward fallback: mana-disruption curse; increases target mana requirements and ends when the target damages another player/creature or expires.
- Damage: mana disruption causes chaos damage proportional to time under the effect when it ends.
- Restriction: caster should not cast Purge Magic while under its own mana-disruption curse.

## Known source conflict and review default

Canonical/current sources disagree on standard post-purge immunity:

- Current UO.com Mysticism says players can only be purged once every 8 seconds.
- UO.com Publish 65 says immunity is calculated from caster Mysticism/Focus vs target Resisting Spells, range 1–6 seconds.
- UOGuide is split: the Purge Magic page mirrors the Publish 65 1–6 second detail, while the UOGuide Publish 65 page mirrors the 8-second rule.
- Sources agree that mana disruption grants an additional 16 seconds of purge immunity.

Issue-review default: if this is the only blocker and the issue is otherwise implementation-ready, resolve the conflict by **implementation policy** rather than leaving triage open. Use current player-facing 8-second immunity as the first RebirthUO implementation default, keep the 1–6 second formula documented as conflicting historical evidence, and require named constants/helper methods plus focused tests so the policy can be changed later without rewriting the spell model.

## RebirthUO / ModernUO anchors found in review sessions

- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs` — base Mysticism class; uses `SkillName.Mysticism`, Focus/Imbuing support skill, circle mana/skill tables, cast delay, and resist helper.
- `Projects/UOContent/Spells/Initializer.cs` — `Core.SA` Mysticism registration block. `Register(679, typeof(PurgeMagicSpell))` was present as a commented expected slot in the inspected worktree.
- `Projects/UOContent/Spells/Mysticism/` — included several Mysticism spells but no `PurgeMagicSpell` in the inspected worktree.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/PurgeMagicScroll.cs` — `PurgeMagicScroll : SpellScroll` already exists at spell ID 679; do not duplicate the scroll item when adding the spell class/registration.
- `Projects/UOContent/Spells/Base/Spell.cs` — `ScaleMana` is the central spell mana-cost path and already handles Mind Rot and Lower Mana Cost; Purge Magic's mana-disruption implementation should hook mana scaling centrally rather than patching individual Mysticism spells only.
- `Projects/UOContent/Spells/Base/SpellHelper.cs` and `Projects/UOContent/Spells/Mysticism/SpellPlagueSpell.cs` — examples of central damage callbacks / per-target state used to clear or advance spell effects; use as precedent for removing mana disruption when the affected target deals damage.
- Potential purgeable ward helpers/patterns:
  - `Projects/UOContent/Spells/Fifth/MagicReflect.cs` — `MagicReflectSpell.EndReflect(Mobile)`.
  - `Projects/UOContent/Spells/Second/Protection.cs` — `ProtectionSpell.EndProtection(Mobile)`.
  - `Projects/UOContent/Spells/First/ReactiveArmor.cs` — `ReactiveArmorSpell.EndArmor(Mobile)` removes current AoS reactive armor state; include only with helper-backed tests.
  - `Projects/UOContent/Spells/Third/Bless.cs` — Bless applies three stat bonuses and a buff icon; treat whole Bless separately from individual stat buffs if matching Publish 65 examples.
  - `Projects/UOContent/Spells/Mysticism/CleansingWindsSpell.cs` — curse cleanup pattern.
  - `Projects/UOContent/Spells/Mysticism/SpellPlagueSpell.cs` — per-target runtime state and cleanup pattern.

## Issue-drafting/review notes

- Use the `spell.yml` template with title `Spell: Purge Magic` and labels `ultima-online`, `triage`, `spell`.
- Duplicate search should include exact `"Purge Magic"` and broad `"Purge" OR "Mysticism"`; broad Mysticism hits like `Spell: Mass Sleep` are related sibling gaps, not duplicates.
- During initial drafting, include `Observed conflict`, `Likely interpretation`, `Decision needed`, and `Suggested default` for the immunity disagreement.
- During issue review, move the immunity and first-ward-list choices into `## Resolved Questions` when the issue has enough canonical/community/repo evidence, set `## Remaining Open Questions` to `None blocking`, and remove `triage` after the normal readiness gate passes.
