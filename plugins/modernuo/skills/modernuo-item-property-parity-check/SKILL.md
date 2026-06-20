---
name: modernuo-item-property-parity-check
description: Use when asked to perform a named Ultima Online item property parity, tooltip/OPL, formula, generation, effect, cap, era, discrepancy, or gap audit against ModernUO/RebirthUO source code. Trigger for requests like "Spell Damage item property parity", "Lower Mana Cost formula audit", "compare Hit Fireball with UO.com", "check Mage Armor tooltip behavior", or "find item property implementation gaps"; requires one concrete item property name and optional user-provided URLs, documents, notes, item names, artifact names, or era constraints.
---

# ModernUO Item Property Parity Check

Use this skill to compare one named Ultima Online item property against ModernUO/RebirthUO source code and produce a decision-ready parity report. The job is to reduce item property behavior, tooltip, generation, and formula gaps safely, not to assume the current implementation is correct.

Do not edit code, propose concrete patches, or collapse discrepancies into a fix plan until the user decides how to handle each issue.

## Required Input

Require one concrete item property name before starting. If the user names only an item, artifact, equipment category, expansion, loot system, or property family, ask for the specific property name and stop.

Treat item names, artifact names, loot systems, or equipment categories as optional context for where the property appears. They narrow the audit surface but do not replace the named property target.

Accept optional extra sources: URLs, documents, notes, shard rules, item tables, artifact tables, or era constraints. If no extra sources are provided, use these default references:

- `https://uo.com`
- `https://www.uoguide.com`

Use UO Stratics only as a secondary fallback when UO.com and UOGuide lack the needed detail. Label Stratics evidence as fallback evidence. If sources conflict, record the conflict as unclear instead of choosing silently.

## Normalize the Property

Normalize player-facing property names to the likely ModernUO enum, container, or helper before searching. Use aliases conservatively and show the normalized implementation target in the report.

Common aliases:

| Player/source name | ModernUO target |
|---|---|
| Spell Damage, SDI | `AosAttribute.SpellDamage` |
| Lower Mana Cost, LMC | `AosAttribute.LowerManaCost` |
| Lower Reagent Cost, LRC | `AosAttribute.LowerRegCost` |
| Faster Casting, FC | `AosAttribute.CastSpeed` |
| Faster Cast Recovery, FCR | `AosAttribute.CastRecovery` |
| Hit Chance Increase, HCI | `AosAttribute.AttackChance` |
| Defense Chance Increase, DCI | `AosAttribute.DefendChance` |
| Swing Speed Increase, SSI | `AosAttribute.WeaponSpeed` |
| Damage Increase, DI | `AosAttribute.WeaponDamage` |
| Reflect Physical Damage, RPD | `AosAttribute.ReflectPhysical` |
| Enhance Potions, EP | `AosAttribute.EnhancePotions` |
| Spell Channeling | `AosAttribute.SpellChanneling` |
| Night Sight | `AosAttribute.NightSight` |
| Mage Armor | `AosArmorAttribute.MageArmor` |
| Mage Weapon | `AosWeaponAttribute.MageWeapon` |
| Use Best Weapon Skill, Use Best Skill | `AosWeaponAttribute.UseBestSkill` |
| Hit Fireball | `AosWeaponAttribute.HitFireball` |
| Hit Magic Arrow | `AosWeaponAttribute.HitMagicArrow` |
| Hit Harm | `AosWeaponAttribute.HitHarm` |
| Hit Lightning | `AosWeaponAttribute.HitLightning` |
| Hit Dispel | `AosWeaponAttribute.HitDispel` |
| Hit Life Leech, Hit Leech Hits | `AosWeaponAttribute.HitLeechHits` |
| Hit Mana Leech, Hit Leech Mana | `AosWeaponAttribute.HitLeechMana` |
| Hit Stamina Leech, Hit Leech Stam | `AosWeaponAttribute.HitLeechStam` |
| Hit Lower Attack | `AosWeaponAttribute.HitLowerAttack` |
| Hit Lower Defense, Hit Lower Defence | `AosWeaponAttribute.HitLowerDefend` |
| Hit Physical Area | `AosWeaponAttribute.HitPhysicalArea` |
| Hit Fire Area | `AosWeaponAttribute.HitFireArea` |
| Hit Cold Area | `AosWeaponAttribute.HitColdArea` |
| Hit Poison Area | `AosWeaponAttribute.HitPoisonArea` |
| Hit Energy Area | `AosWeaponAttribute.HitEnergyArea` |
| Lower Requirements, Lower Stat Requirement | `AosWeaponAttribute.LowerStatReq` or `AosArmorAttribute.LowerStatReq` |
| Self Repair | `AosWeaponAttribute.SelfRepair` or `AosArmorAttribute.SelfRepair` |
| Durability Bonus | `AosWeaponAttribute.DurabilityBonus` or `AosArmorAttribute.DurabilityBonus` |
| Physical/Fire/Cold/Poison/Energy/Chaos/Direct Damage | `AosElementAttribute` values |
| Skill Bonus, +Skill | `AosSkillBonuses` |

If the name maps to multiple containers, state the selected scope. Example: `Lower Requirements` may require separate weapon and armor analysis. If the user does not specify the item type and the containers differ materially, ask for the item type and stop.

## Gather Expected Behavior

Read user-provided resources first. Then use default sources when needed.

Extract only behavior that can be cited or clearly labeled as uncertain:

- Display name, tooltip/OPL wording, cliloc behavior, and value formatting.
- Allowed item types, equipment layers, spellbooks, quivers, talismans, artifacts, loot tables, crafting/runic systems, and era or expansion gates.
- Value ranges, caps, stacking rules, negative value behavior, and generation weighting.
- Combat, spell, resist, regeneration, stat, skill, durability, equipment, or targeting formulas that consume the property.
- PvP/PvM differences, publish changes, shard-profile rules, and item-specific exceptions.
- Testable edge cases such as unequipped items, pets/summons, set bonuses, transformed mobiles, and pre-AoS shards.

Cite exact URLs for public sources. Do not invent exact formulas, caps, timers, cliloc IDs, value ranges, or generation weights when sources only describe behavior qualitatively.

## Analyze ModernUO Source

Start at these anchors in the ModernUO/RebirthUO service repository:

- `Projects/UOContent/Misc/AOS.cs` for `AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, `AosSkillBonuses`, `AosElementAttributes`, `BaseAttributes`, `AOS.Damage`, property aggregation, and the `Core.AOS` gate.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` for weapon attributes, hit effects, swing/combat consumers, `CheckHitEffect`, damage bonuses, skill modifiers, and weapon OPL rows.
- `Projects/UOContent/Items/Armor/BaseArmor.cs` for armor attributes, resist/stat/skill interactions, `MageArmor`, and armor OPL rows.
- `Projects/UOContent/Items/Clothing/BaseClothing.cs`, `Projects/UOContent/Items/Jewels/BaseJewel.cs`, `Projects/UOContent/Items/Skill Items/Magical/Spellbook.cs`, `Projects/UOContent/Items/Quivers/BaseQuiver.cs`, and `Projects/UOContent/Items/Talismans/BaseTalisman.cs` for non-weapon item containers and OPL rows.
- `Projects/UOContent/Spells/Base/Spell.cs` and `Projects/UOContent/Spells/Base/SpellHelper.cs` for caster property consumers such as spell damage, lower reagent cost, lower mana cost, faster casting, and faster cast recovery.
- `Projects/UOContent/Misc/RegenRates.cs` and `Projects/UOContent/Mobiles/PlayerMobile.cs` for regeneration, luck, stat, and status consumers.
- `Projects/UOContent/Items/Skill Items/Tools/BaseRunicTool.cs`, artifact folders, loot/generation systems, and crafting systems for property generation and assigned values.
- `Projects/UOContent.Tests/Tests/Utilities/CapturingPropertyList.cs` and relevant item, artifact, combat, spell, and property tests for regression coverage.
- `Distribution/Configuration/` and `Distribution/Configuration/EraProfiles/` for expansion/profile policy.

Then search neighboring systems that can own the actual player-visible behavior:

```bash
rg -n "<PropertyName>|<EnumName>|AosAttribute|AosWeaponAttribute|AosArmorAttribute|AosSkillBonuses|AosElementAttribute" Projects Distribution dev-docs
rg -n "GetProperties\\(|ItemPropertyDisplay|IPropertyList|cliloc|CapturingPropertyList" Projects Distribution dev-docs
rg -n "AosAttributes\\.GetValue|AosWeaponAttributes\\.GetValue|AosArmorAttributes\\.GetValue|CheckHitEffect|SpellDamage|LowerManaCost|LowerRegCost|CastSpeed|CastRecovery" Projects Distribution dev-docs
rg -n "BaseRunicTool|ApplyAttribute|LootPack|MagicItem|Artifact|SetArmor|SkillBonuses|Slayer|DamageTypes" Projects Distribution dev-docs
rg -n "Core\\.(AOS|SE|ML|SA|HS|TOL|EJ)|Expansion\\.(AOS|SE|ML|SA|HS|TOL|EJ)|EraProfile" Projects Distribution dev-docs
rg --files Projects/UOContent Projects/UOContent.Tests/Tests | rg "AOS|BaseWeapon|BaseArmor|BaseClothing|BaseJewel|Spellbook|Quiver|Talisman|Property|Artifact|Runic"
```

For property families, also inspect likely owning areas:

- Caster properties: spells, special moves, spellbooks, AI casting, spell damage modifiers, recovery/cast delay caps, and `uo-magic-spells`.
- Weapon hit effects: `BaseWeapon.OnHit`, area damage, spell hit effects, leech effects, lowering effects, Slayer/special move interactions, and `uo-combat-pipeline`.
- Defensive and stat properties: armor/clothing/jewelry, set bonuses, stat mods, resist calculations, regeneration rates, stealth armor checks, and status packets.
- Generation properties: runic tools, loot packs, artifacts, rewards, crafting, BOD rewards, quest rewards, and era-gated item pools.
- Tooltip properties: base item `GetProperties`, typed container `GetProperties`, cliloc arguments, `ItemPropertyDisplay`, and `modernuo-property-lists`.

Record classes, methods, formulas, gates, OPL rows, generation paths, and tests with file paths and line numbers when possible.

## Compare and Categorize

Compare expected behavior against source behavior. Categorize every meaningful row with one of these labels:

- `Matching behavior`: code and cited references agree closely enough for the selected property and era/profile scope.
- `Minor deviation`: behavior differs but impact appears limited, cosmetic, era-dependent, or low risk.
- `Critical discrepancy`: missing or wrong behavior could affect combat balance, spell balance, item economy, PvP/PvM outcomes, generation, tooltips, save compatibility, exploits, or client-visible core mechanics.
- `Unclear`: sources conflict, evidence is missing, implementation is ambiguous, or the target era/shard policy is not defined.

Useful discrepancy types:

- Missing property, enum value, wrapper, serialization, or aggregation.
- Incorrect tooltip/OPL row, cliloc, formatting, ordering, or era visibility.
- Incorrect cap, stacking rule, formula, value range, generation weight, or negative value behavior.
- Missing or incorrect combat, spell, regen, stat, resist, durability, skill, equipment, or cleanup consumer.
- Incorrect item-type availability, loot/runic/artifact assignment, or expansion/profile gate.
- Source ambiguity.
- Test coverage gap.

## Report Format

Use these exact sections:

```markdown
# <Property Name> Item Property Parity Check

## Property Overview

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

- `IPPC-1`: Align with official sources, keep current implementation, or apply a custom rule?
- `IPPC-2`: Which era/profile should control this unclear behavior?
- `IPPC-3`: Should this item-specific exception apply globally or only to the named context?

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

Do not bundle unrelated findings into one issue just because they affect the same item property or item family.

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
- Keep the main objective visible: reduce ModernUO item property behavior, tooltip, generation, and formula gaps safely.

## Related Skills

- `uo-aos-item-properties` for the AoS property storage model, containers, aggregation, OPL rows, and implementation pitfalls.
- `modernuo-property-lists` for tooltip/OPL mechanics and cliloc formatting.
- `modernuo-era-expansion` for expansion gates such as `Core.AOS`, `Core.SE`, `Core.ML`, and `Core.SA`.
- `uo-combat-pipeline` when the property affects melee, ranged, damage, hit effects, leeches, resists, or special moves.
- `uo-magic-spells` when the property affects casting, spell damage, mana/reagent cost, cast speed, or recovery.
- `uo-domain-research` for source triangulation and decision-grade Ultima Online mechanics reports.
