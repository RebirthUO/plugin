---
name: modernuo-era-change-gate
description: Use when a ModernUO/RebirthUO content change, parity finding, implementation plan, diff, issue, or review crosses Ultima Online era boundaries or changes which expansion/profile owns behavior. Trigger for requests like "content changed from Samurai Empire to Time of Legends", "this ML feature now uses TOL rules", "move this spawn from SE to ML", "era-breaking change", "Core.SE to Core.TOL", or any skill, spell, item, quest, loot, spawn, mobile, world, combat, crafting, or property audit with era/profile ambiguity. Requires the affected era check(s) to be involved, especially `modernuo-era-parity-check`.
---

# ModernUO Era Change Gate

Use this skill to catch content changes that can silently break expansion parity. The job is to identify the affected eras, require the era parity workflow for those eras, and produce a Markdown routing report before implementation or issue slicing continues.

This skill is a gate. It does not replace `modernuo-era-parity-check`; it decides when that skill must be involved and which eras or profiles it must cover.

## Hard Rule

If content behavior, ownership, source evidence, code gates, data placement, profile activation, or documentation moves from one era/profile to another, always involve `modernuo-era-parity-check` for the affected era set before calling the work complete.

Do not treat a named skill, spell, item property, quest, mobile, loot, spawn, region, crafting, or combat check as complete when an era delta is present but no era parity check has been run, requested, or explicitly listed as blocked.

## Era Order And Aliases

Normalize expansion names before deciding scope:

| Display name | Enum | Core check | Common aliases |
|---|---|---|---|
| Original UO | `None` | pre-`Core.T2A` | pre-T2A, classic |
| The Second Age | `T2A` | `Core.T2A` | T2A |
| Renaissance | `UOR` | `Core.UOR` | Renaissance, UO:R |
| Third Dawn | `UOTD` | `Core.UOTD` | TD, 3D |
| Lord Blackthorn's Revenge | `LBR` | `Core.LBR` | LBR |
| Age of Shadows | `AOS` | `Core.AOS` | AoS |
| Samurai Empire | `SE` | `Core.SE` | SE, Tokuno, Bushido, Ninjitsu |
| Mondain's Legacy | `ML` | `Core.ML` | ML, Spellweaving, peerless |
| Stygian Abyss | `SA` | `Core.SA` | SA, gargoyle, imbuing, mysticism, throwing |
| High Seas | `HS` | `Core.HS` | HS, ships, sea market |
| Time of Legends | `TOL` | `Core.TOL` | ToL, skill mastery, Valley of Eodon |
| Endless Journey | `EJ` | `Core.EJ` | EJ, free profile |

Also treat `Distribution/Configuration/EraProfiles/*.json` as era-affecting when a profile enables, blocks, or overrides content.

## Detection Triggers

Activate the gate when any of these appear in the user request, diff, issue, or local evidence:

- A phrase such as "changed from X to Y", "moved to", "now belongs to", "introduced in", "backport", "forward-port", "breaking change", "era difference", or "profile mismatch".
- Code or docs changing `Core.*`, `Expansion.*`, `RequiredExpansion`, `EraProfile`, `EraProfiles/`, `dev-docs/eras/`, `publish-index`, or expansion-named content folders.
- A named parity check that discovers behavior differs between eras, even if the original request named only one skill, spell, item property, entity, or mechanic.
- A content category with known cross-era ownership, such as AOS item properties, SE Bushido/Ninjitsu, ML Spellweaving/peerless/recipes, SA gargoyle skills, HS ship systems, TOL skill masteries, or EJ profile restrictions.

## Affected Era Set

Build the smallest complete set of era checks:

1. Include the source/origin era when content is removed from, reinterpreted from, or claims compatibility with that era.
2. Include the destination/target era when content is added to, gated by, or changed to match that era.
3. Include the actual introducing or dependency era when the breaking behavior belongs there, even if it is between source and target.
4. Include any named `EraProfile` whose activation policy changes.
5. Do not include every intermediate expansion only because it sits between source and target. Add an intermediate era only when evidence shows it owns or changes the behavior.

Example: if Bushido content changes from Samurai Empire behavior to Time of Legends skill mastery behavior, require SE and TOL checks. Add ML only if the changed behavior actually depends on ML content, such as Spellweaving, ML quests, recipes, peerless systems, or an ML era profile.

## Required Workflow

1. **Read the change** - Identify the content object, old behavior, new behavior, source era, target era, code gates, profile gates, and evidence paths.
2. **Normalize eras** - Convert aliases to display name, enum, `Core.*`, era doc path, and optional profile.
3. **Build the affected era set** - Use the rules above. If the set is ambiguous, list candidate eras and the missing evidence.
4. **Involve era parity** - Run, request, or explicitly block `modernuo-era-parity-check` for every affected era/profile before final implementation advice.
5. **Coordinate related checks** - If a named skill, spell, item property, or content taxonomy check triggered the finding, keep it involved but subordinate final decisions to the era-impact result.
6. **Emit Markdown** - Produce the report structure below. End with issue slice options when the output contains findings.

## Markdown Report

Use this structure for every final gate report:

```markdown
# Era Change Gate Report: {content or change title}

## Change Summary

| Field | Value |
|---|---|
| Content | {entity/system/mechanic} |
| Source era/profile | {display name, enum, Core check, profile if any} |
| Target era/profile | {display name, enum, Core check, profile if any} |
| Change type | {gate move, behavior drift, source conflict, profile activation, docs/code mismatch} |
| Evidence | {repo paths, diff notes, user sources, URLs} |

## Affected Era Checks

| Era/profile | Why required | Required skill | Status |
|---|---|---|---|
| Samurai Empire (`SE`) | Original behavior/source owner | `modernuo-era-parity-check` | Required / Done / Blocked |
| Time of Legends (`TOL`) | New behavior/source owner | `modernuo-era-parity-check` | Required / Done / Blocked |

## Related Parity Checks

| Check | Why involved | Status |
|---|---|---|
| `modernuo-skill-parity-check` | {if named skill behavior changed} | Required / Done / Not applicable |
| `modernuo-spell-parity-check` | {if named spell behavior changed} | Required / Done / Not applicable |
| `modernuo-item-property-parity-check` | {if item property behavior changed} | Required / Done / Not applicable |
| `modernuo-content-taxonomy` | {if broad content inventory is needed} | Required / Done / Not applicable |

## Decision Points

- `ECG-1`: {era/profile decision the user must choose or evidence that resolves it}
- `ECG-2`: {implementation or documentation boundary decision}

## Recommended Next Actions

1. Run or attach the required era parity report(s).
2. Reconcile code gates, era docs, and profile JSON after the era reports agree.
3. Only then draft implementation fixes or tracker issues.

## Issue Slice Options
```

In `Issue Slice Options`, offer to turn findings into single sliced Markdown issues. Only create issue drafts or tracker issues when the user asks.

## Issue Slicing Rules

When slicing is requested, create one independently actionable Markdown issue per era-impact finding:

- One issue for each missing required era parity check.
- One issue for each wrong `Core.*` or `Expansion.*` gate.
- One issue for each profile activation mismatch.
- One issue for each source conflict that changes era ownership.
- One issue for each documentation/code mismatch in `dev-docs/eras/` or `EraProfiles/`.

Each issue slice should include:

- Title.
- Source report row or stable decision ID.
- Affected era/profile.
- Expected era behavior with cited source.
- ModernUO evidence with file path, line, or search evidence.
- Impact/risk category.
- Proposed decision direction, without code patches unless already approved.
- Acceptance criteria and suggested validation.
- Open questions or source conflicts.

Do not bundle unrelated eras or independent gates into one issue because they mention the same content object.

## Examples

| Change | Required era checks | Notes |
|---|---|---|
| Bushido behavior changes from SE rules to TOL skill mastery rules | SE + TOL | Add ML only if an ML dependency or profile is part of the change. |
| Spellweaving unlock is moved from ML quest behavior into EJ profile defaults | ML + EJ profile | Use ML for source behavior and EJ for profile activation. |
| An AOS property formula is changed for an ML artifact set | AOS + ML | AOS owns the property system; ML owns the artifact/set context. |
| High Seas ship behavior is changed to match a TOL event | HS + TOL | HS owns ship mechanics; TOL owns the event behavior. |

## Related Skills

- `modernuo-era-parity-check` for the mandatory era-wide parity report.
- `modernuo-era-expansion` for `Core.*`, `Expansion.*`, and era-conditional implementation rules.
- `modernuo-content-taxonomy` for broad content inventory and domain mapping.
- `modernuo-skill-parity-check`, `modernuo-spell-parity-check`, and `modernuo-item-property-parity-check` for named behavior checks that discovered or depend on the era delta.
