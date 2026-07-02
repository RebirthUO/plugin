---
name: modernuo-spell-parity-check
description: Use when asked to perform a named Ultima Online spell parity, mechanics, discrepancy, formula, registration, casting, effect, or gap audit against ModernUO/RebirthUO source code. Trigger for requests like "Flamestrike parity check", "Blood Oath formula audit", "compare Spell Plague with UO.com", or "find spell implementation gaps"; requires one concrete UO spell name and optional user-provided URLs, documents, or notes.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - ultima-online
    - modernuo
    - spells
    - parity
    - research
    related_skills:
    - uo-magic-spells
    - uo-domain-research
    - modernuo-era-parity-check
    - modernuo-item-property-parity-check
---
# ModernUO Spell Parity Check

## Overview

Use this skill to compare one named Ultima Online spell against ModernUO/RebirthUO source code and produce a decision-ready parity report. The job is to reduce spell behavior gaps and discrepancies safely, not to assume the current implementation is correct.

Do not edit code, propose concrete patches, or collapse discrepancies into a fix plan until the user decides how to handle each issue.

## Required Input

Require one concrete spell name before starting. If the user names only a school such as `Magery`, `Necromancy`, or `Mysticism`, ask for the specific spell and stop.

Accept optional extra sources: URLs, documents, notes, shard rules, or era constraints. If no extra sources are provided, use these default references:

- `https://uo.com`
- `https://www.uoguide.com`

Use UO Stratics only as a secondary fallback when UO.com and UOGuide lack the needed detail. Label Stratics evidence as fallback evidence. If sources conflict, record the conflict as unclear instead of choosing silently.

## Normalize the Spell

Normalize player-facing UO names to the likely ModernUO spell class before searching. Use aliases conservatively and show the normalized class name in the report.

Common aliases:

| Player/source name | ModernUO class |
|---|---|
| Flamestrike, Flame Strike | `FlameStrikeSpell` |
| Magic Reflection, Reflect | `MagicReflectSpell` |
| Gate, Gate Travel | `GateTravelSpell` |
| EV, Energy Vortex | `EnergyVortexSpell` |
| Rez, Res, Resurrection | `ResurrectionSpell` |
| Blood Oath | `BloodOathSpell` |
| Enemy of One | `EnemyOfOneSpell` |
| Arcane Circle | `ArcaneCircleSpell` |
| Spell Plague | `SpellPlagueSpell` |
| Magic Arrow | `MagicArrowSpell` |
| Mana Vampire | `ManaVampireSpell` |
| Poison Field | `PoisonFieldSpell` |
| Paralyze Field | `ParalyzeFieldSpell` |
| Sacred Journey | `SacredJourneySpell` |
| Curse Weapon | `CurseWeaponSpell` |
| Vampiric Embrace | `VampiricEmbraceSpell` |
| Wraith Form | `WraithFormSpell` |
| Gift of Life | `GiftOfLifeSpell` |
| Rising Colossus | `RisingColossusSpell` |

If the name maps to multiple schools or classes, state the selected scope. Example: `Gate Travel` includes the Magery spell, travel validation, gate item behavior, spellbook/scroll access, and region travel restrictions that materially affect that spell.

## Gather Expected Behavior

Read user-provided resources first. Then use default sources when needed.

Extract only behavior that can be cited or clearly labeled as uncertain:

- Spell school, circle/tier, spell ID, skill requirement, mana/tithing/focus cost, and era or expansion gate.
- Required reagents, foci, spellbooks, scrolls, quests, karma, tithing, race, location, target, or equipment.
- Cast time, recovery, interruption rules, success/failure formulas, and cooldowns.
- Targeting rules, travel restrictions, line-of-sight, field placement, summon slots, dispel behavior, and region hooks.
- Damage, healing, buffs, debuffs, transformations, duration, scaling skills, item property interactions, and edge cases.
- PvP/PvM differences, publish changes, and shard-profile or era conditions.

Cite exact URLs for public sources. Do not invent exact formulas, timers, rates, caps, or spell IDs when sources only describe behavior qualitatively.

## Analyze ModernUO Source

Start at these anchors in the ModernUO/RebirthUO service repository:

- `Projects/UOContent/Spells/Base/Spell.cs` for cast lifecycle, mana/reagent checks, disturbance, sequence handling, cast delay, recovery, and skill checks.
- `Projects/UOContent/Spells/Base/SpellRegistry.cs` for spell ID registration, type lookup, and spell construction.
- `Projects/UOContent/Spells/Base/SpellInfo.cs` for names, mantras, reagents, and metadata passed to each spell.
- `Projects/UOContent/Spells/Base/SpellHelper.cs` for targeting, travel checks, damage helpers, delayed damage, field placement, and shared validation.
- `Projects/UOContent/Spells/Initializer.cs` for spell registration order, spell IDs, and era-gated school registration.
- `Projects/UOContent/Spells/<school>/` for the concrete spell class and school base class.
- `Projects/UOContent.Tests/Tests/Spells/` for spell regression coverage.

Then search neighboring systems that can own the actual player-visible behavior:

```bash
rg -n "<SpellName>|<SpellClass>|SpellRegistry|Register\(|RequiredSkill|RequiredExpansion|CastDelayBase|CastRecoveryBase|CheckSequence|CheckCast" Projects Distribution dev-docs
rg -n "Spellbook|SpellScroll|SpellbookType|AddToSpellbook|RandomScroll|Inscription|DefInscription|Reagent|Tithing|FocusLevel" Projects Distribution dev-docs
rg -n "TravelCheckType|CheckTravel|OnBeginSpellCast|NoTravel|Region|CanTravel|Recall|Gate|Teleport" Projects Distribution dev-docs
rg -n "SpellDamage|CastSpeed|CastRecovery|LowerManaCost|LowerRegCost|MageWeapon|MageArmor|Evaluate Intelligence|EvalInt|SpiritSpeak|Mysticism" Projects Distribution dev-docs
rg -n "Core\.(AOS|SE|ML|SA|HS|TOL|EJ)|Expansion\.(AOS|SE|ML|SA|HS|TOL|EJ)|EraProfile" Projects Distribution dev-docs
rg --files Projects/UOContent/Spells Projects/UOContent.Tests/Tests/Spells
```

For spell families, also inspect likely owning areas:

- Magery: `First/` through `Eighth/`, `MagerySpell`, regular spellbooks, scrolls, reagents, Inscription, fields, summons, travel, and `SkillName.Magery`.
- Necromancy: `Necromancy/`, `NecromancerSpell`, transformations, Spirit Speak scaling, necro reagents, karma, summons, and form cleanup.
- Chivalry: `Chivalry/`, `PaladinSpell`, tithing, karma scaling, holy travel, and Chivalry-specific cast speed/recovery.
- Bushido and Ninjitsu: `Bushido/`, `Ninjitsu/`, focus level, special move interactions, weapon/combat hooks, and SE gates.
- Spellweaving: `Spellweaving/`, `ArcanistSpell`, Arcane Focus, quest flags, ML quest rewards, and Arcane Circle group requirements.
- Mysticism: `Mysticism/`, `MysticSpell`, Gargoyle/race assumptions, focus skills, mystic scrolls, and SA gates.
- Cross-cutting spell surfaces: spellbooks, scroll items, vendors, loot scrolls, AI casting, player packet handlers, regions, item attributes, buffs, timers, mobiles, and tests.

Record classes, methods, formulas, gates, and tests with file paths and line numbers when possible.

## Compare and Categorize

Compare expected behavior against source behavior. Categorize every meaningful row with one of these labels:

- `Matching behavior`: code and cited references agree closely enough for the selected spell and era/profile scope.
- `Minor deviation`: behavior differs but impact appears limited, cosmetic, era-dependent, or low risk.
- `Critical discrepancy`: missing or wrong behavior could affect spell access, combat balance, PvP/PvM outcomes, travel, economy, save compatibility, exploits, or client-visible core mechanics.
- `Unclear`: sources conflict, evidence is missing, implementation is ambiguous, or the target era/shard policy is not defined.

Useful discrepancy types:

- Missing spell or registration.
- Incorrect spell ID, school, circle/tier, scroll, or spellbook mapping.
- Incorrect formula, damage, duration, scaling, cast time, recovery, cost, or reagent/tithing/focus rule.
- Missing or incorrect target, travel, region, AI, summon, field, buff, transformation, or cleanup behavior.
- Era/profile ambiguity.
- Source ambiguity.
- Test coverage gap.

## Report Format

Use these exact sections:

```markdown
# <Spell Name> Spell Parity Check

## Spell Overview

## Expected Behavior (Sources)

## ModernUO Implementation

## Discrepancy Analysis

| Area | Status | Expected | ModernUO Evidence | Impact | Recommendation |
|---|---|---|---|---|---|

## Recommended Actions

## Questions for User

## Issue Slice Options
```

In `Recommended Actions`, recommend decision direction only. Do not include code patches until the user chooses a policy for each discrepancy.

In `Questions for User`, list each unresolved decision with stable IDs:

- `SPC-1`: Align with official sources, keep current implementation, or apply a custom rule?
- `SPC-2`: Which era/profile should control this unclear behavior?

## Markdown Delivery and Issue Slicing

Deliver the final parity check as Markdown. End every report with `## Issue Slice Options` and offer to turn findings into single sliced issues.

Only create issue drafts or tracker issues when the user asks. When slicing is requested, create one independently actionable Markdown issue per discrepancy, gap, or unresolved decision. Each issue slice should include:

- Title.
- Source report row or stable decision ID.
- Expected behavior with cited source.
- ModernUO evidence with file path, line, or search evidence.
- Impact/risk category.
- Proposed decision direction, without code patches unless already approved.
- Acceptance criteria and suggested validation.
- Open questions or source conflicts.

Do not bundle unrelated findings into one issue just because they affect the same spell.

## Decision Loop

If discrepancies are found, ask the user what to do for each issue before suggesting fixes:

- Align with official sources.
- Keep current implementation.
- Apply a custom rule.

If no discrepancies are found, still list any remaining uncertainty, source limitations, or test gaps.

## Quality Bar

- Be precise and technical.
- Use current repository files as implementation truth.
- Do not treat source code as inherently correct.
- Separate cited facts from inference.
- Highlight uncertainty explicitly.
- Prefer clarity over completeness when data conflicts.
- Keep the main objective visible: reduce ModernUO spell-behavior gaps safely.

## Source-Conflict Patterns

### Death Strike formula and PvP cap

When auditing Ninjitsu `Death Strike`, do not treat the formula as fully source-confirmed from one page. The durable conflict is:

- Current UO.com Ninjitsu wording says damage uses the **target's** Hiding/Stealth average and says PvP is capped at `50%`.
- UOGuide Death Strike/Ninjitsu and RunUO/ServUO/ModernUO lineage point to the **attacker/Ninja's** Hiding/Stealth average.
- UO.com Publish 46 confirms the 30%-to-100% Hiding/Stealth scalar, ranged half-damage, and cap reduction, but not attacker-vs-target ownership.
- UOGuide Death Strike, UO.com Publish 69, and ServUO lineage point to a **fixed 50 damage PvP cap**, not `target.HitsMax / 2`.

Use `references/death-strike-source-conflicts.md` before proposing or reviewing Death Strike formula/cap changes. Label attacker-vs-target Hiding/Stealth as `source-conflict` unless the issue/era profile explicitly chooses one source tier. Default PvP cap recommendation is fixed `50` unless the project intentionally adopts the current UO.com `50%` wording as custom/current-official policy; if a half-Hits cap is chosen, require tests above and below 100 `HitsMax`.

## Related Skills

- `uo-magic-spells` for spell pipeline, school model, cast lifecycle, reagents, spellbooks, scrolls, fields, summons, and school-specific pitfalls.
- `uo-domain-research` for source triangulation and decision-grade UO mechanics reports.
- `modernuo-era-parity-check` for era-wide parity reports that require a target era.
- `modernuo-skill-parity-check` when the spell discrepancy depends on an underlying skill such as Magery, Spirit Speak, Chivalry, Focus, or Mysticism.
- `uo-aos-item-properties` for spell damage, cast speed, cast recovery, lower mana cost, lower reagent cost, mage weapon, and mage armor effects.
- `uo-combat-pipeline` when the spell's effect routes through combat damage, resists, slayers, or special moves.
- `references/death-strike-source-conflicts.md` for the Death Strike attacker-vs-target Hiding/Stealth and fixed-50-vs-half-Hits PvP cap source conflict.
