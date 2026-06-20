---
name: modernuo-skill-parity-check
description: Use when asked to perform a named Ultima Online skill parity, clarity, mechanics, discrepancy, or gap audit against ModernUO/RebirthUO source code. Trigger for requests like "Magery parity check", "Blacksmithy skill clarity", "compare Animal Taming with UO.com", or "find skill implementation gaps"; requires one UO skill name and optional user-provided URLs, documents, or notes.
---

# ModernUO Skill Parity Check

Use this skill to compare one named Ultima Online skill against ModernUO/RebirthUO source code and produce a decision-ready parity report. The job is to reduce gaps and discrepancies in the ModernUO source, not to assume the current implementation is correct.

Do not edit code, propose concrete patches, or collapse discrepancies into a fix plan until the user decides how to handle each issue.

## Required Input

Require a skill name before starting. If the user does not provide one, ask for the missing skill name and stop.

Accept optional extra sources: URLs, documents, notes, shard rules, or era constraints. If no extra sources are provided, use these default references:

- `https://uo.com`
- `https://www.uoguide.com`

Treat `uo.com` as the strongest public source for official feature scope, publish notes, and current production behavior. Treat UOGuide as the strongest default secondary source for practical skill pages, tables, aliases, and related mechanics. If sources conflict, record the conflict as unclear instead of choosing silently.

## Normalize the Skill

Normalize player-facing UO names to the ModernUO `SkillName` enum before searching. Use aliases conservatively and show the normalized name in the report.

Common aliases:

| Player/source name | ModernUO name |
|---|---|
| Blacksmithy | `Blacksmith` |
| Resisting Spells | `MagicResist` |
| Evaluating Intelligence | `EvalInt` |
| Item Identification | `ItemID` |
| Forensic Evaluation | `Forensics` |
| Swordsmanship | `Swords` |
| Mace Fighting | `Macing` |
| Bowcraft, Bowcraft/Fletching | `Fletching` |
| Taste Identification | `TasteID` |
| Animal Lore | `AnimalLore` |
| Animal Taming | `AnimalTaming` |
| Spirit Speak | `SpiritSpeak` |
| Remove Trap | `RemoveTrap` |
| Detecting Hidden | `DetectHidden` |

If the name maps to multiple systems, state the selected scope. Example: `Magery` includes the skill entry, skill checks, spell casting formulas, spell availability, related support skills, and item/reagent interactions that materially affect Magery behavior.

## Gather Expected Behavior

Read user-provided resources first. Then use default sources when needed.

Extract only behavior that can be cited or clearly labeled as uncertain:

- Skill progression and training mechanics.
- Required tools, reagents, items, resources, targets, locations, timers, or cooldowns.
- Success/failure formulas and probability bands.
- Effects, outcomes, rewards, caps, support skills, stat interactions, and edge cases.
- Expansion, publish, race, facet, PvP/PvM, and shard-profile conditions.

Cite exact URLs for public sources. Do not invent exact formulas, timers, rates, or caps when public sources only describe behavior qualitatively.

## Analyze ModernUO Source

Start at these anchors in the ModernUO/RebirthUO service repository:

- `Projects/Server/Skills.cs` for `SkillName`, `Skill`, `Skills`, `SkillInfo`, direct skill use, caps, locks, values, and serialization.
- `Projects/UOContent/Skills/` for active skill handlers and skill-specific behavior.
- `Projects/UOContent/Skills/SkillsInfo.cs` for skill categories and expansion-sensitive random skill selection.
- `Projects/UOContent/Skills/SkillCheck.cs` for success checks, gain chance, anti-macro, stat gain, caps, and locks.
- `Distribution/Data/skills.json` if present, for skill metadata, stat weights, titles, callbacks, and table values.
- `Distribution/Configuration/` and `Distribution/Configuration/EraProfiles/` for expansion/profile policy.
- `Projects/UOContent.Tests/Tests/Skills/` for skill regression coverage.

Then search neighboring systems that can own the actual player-visible behavior:

```bash
rg -n "SkillName\.<Skill>|<Skill>|CheckSkill|UseSkill|SetSkill|SkillInfo|SkillCheck|AllowedSkill|AllowSkillUse" Projects Distribution dev-docs
rg -n "Core\.(AOS|SE|ML|SA|HS|TOL|EJ)|Expansion\.(AOS|SE|ML|SA|HS|TOL|EJ)" Projects Distribution dev-docs
rg --files Projects/UOContent/Skills Projects/UOContent.Tests/Tests/Skills
```

For skill families, also inspect likely owning areas:

- Magic skills: `Projects/UOContent/Spells/`, spellbooks, scrolls, reagents, AI casting, and `uo-magic-spells`.
- Craft skills: `Projects/UOContent/Engines/Craft/`, `Def*.cs`, tools, recipes, BODs, resources, and `uo-crafting-recipes-resources`.
- Harvest skills: `Projects/UOContent/Engines/Harvest/`, harvest tools, resource tables, maps, and region blockers.
- Combat skills: weapons, `BaseWeapon`, special moves, damage formulas, combat tests, and `uo-combat-pipeline`.
- Bard, stealth, taming, tracking, and utility skills: active handler files, timers, targeters, gumps, context menus, pet/AI hooks, and item interactions.
- Character creation and progression: creation templates, New Haven skill training, PowerScrolls, Scrolls of Alacrity/Transcendence, accelerated skill windows, and stat cap items.

Record classes, methods, formulas, gates, and tests with file paths and line numbers when possible.

## Compare and Categorize

Compare expected behavior against source behavior. Categorize every meaningful row with one of these labels:

- `Matching behavior`: code and cited references agree closely enough for the selected scope.
- `Minor deviation`: behavior differs but impact appears limited, cosmetic, era-dependent, or low risk.
- `Critical discrepancy`: missing or wrong behavior could affect progression, economy, PvP/PvM balance, content access, save compatibility, exploits, or client-visible core mechanics.
- `Unclear`: sources conflict, evidence is missing, implementation is ambiguous, or the target era/shard policy is not defined.

Useful discrepancy types:

- Missing feature.
- Incorrect formula.
- Outdated mechanic.
- Behavioral mismatch.
- Era/profile ambiguity.
- Source ambiguity.
- Test coverage gap.

## Report Format

Use these exact sections:

```markdown
# <Skill Name> Skill Parity Check

## Skill Overview

## Expected Behavior (Sources)

## ModernUO Implementation

## Discrepancy Analysis

| Area | Status | Expected | ModernUO Evidence | Impact | Recommendation |
|---|---|---|---|---|---|

## Recommended Actions

## Questions for User
```

In `Recommended Actions`, recommend decision direction only. Do not include code patches until the user chooses a policy for each discrepancy.

In `Questions for User`, list each unresolved decision with stable IDs:

- `SPC-1`: Align with official sources, keep current implementation, or apply a custom rule?
- `SPC-2`: Which era/profile should control this unclear behavior?

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
- Keep the main objective visible: reduce ModernUO skill-behavior gaps safely.

## Related Skills

- `uo-skills-stats-races` for general skill, stat, race, cap, gain, and PowerScroll behavior.
- `uo-domain-research` for source triangulation and decision-grade UO mechanics reports.
- `modernuo-era-parity-check` for era-wide parity reports that require a target era.
- `uo-magic-spells`, `uo-crafting-recipes-resources`, `uo-combat-pipeline`, and `uo-harvest-gathering-resources` when the named skill belongs to those subsystems.
