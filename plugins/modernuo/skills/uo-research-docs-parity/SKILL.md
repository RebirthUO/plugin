---
name: uo-research-docs-parity
description: Use when researching Ultima Online era/topic documentation from canonical web sources and comparing RebirthUO game-docs against ModernUO source for complete, partial, missing, or unknown parity.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UltimaOnline, RebirthUO, GameDocs, research, parity, Broadsword]
    related_skills:
      - uo-game-docs-canonical-authoring
      - uo-domain-research
      - modernuo-era-parity-check
      - rebirthuo-modernuo-codebase
---

# Ultima Online Research Docs and Parity

## Overview

Use this skill to research, structure, extend, and validate Ultima Online game documentation for a selected era and topic area, then compare that documentation against the RebirthUO/ModernUO source tree when requested.

The workflow has two modes:

1. **Internet-based documentation research** — build or extend source-cited, atomic, era-separated Broadsword game documentation.
2. **Documentation-to-source-code parity analysis** — compare existing atomic documentation against project source and record whether each system is complete, partial, missing, or unknown.

The core discipline is: define the era and ruleset first, keep every mechanic atomic, cite every factual claim, and never compare undocumented assumptions against source code.

## When to Use

Use when the user asks to:

- research a UO topic for a specific era or publish;
- analyze official/community UO documentation for Skills, Spells, Items, Monsters, Quests, Pets, Crafting, Housing, Combat, Virtues, or another game domain;
- create or extend `game-docs/GameDocs/01_Broadsword` documentation;
- compare `01_Broadsword` documentation with RebirthUO/ModernUO source code;
- produce gap/parity documents for documented UO elements;
- audit whether an atomic UO mechanic is implemented, partial, missing, or unclear in the repo.

Do **not** use for:

- chat-only unsourced summaries;
- implementation work without documentation/parity output;
- exploit reproduction or operational abuse details;
- comparing source against a mechanic that has not first been documented from sources.

## Required User Input

Before starting, the user must provide all three values:

1. **Era** — examples: `Publish 57`, `Mondain's Legacy`, `Stygian Abyss`, `High Seas`, `Time of Legends`, `Modern Broadsword`.
2. **Topic area** — examples: `Skills`, `Spells`, `Items`, `Monsters`, `Quests`, `Pets`, `Crafting`, `Housing`, `Combat`, `Virtues`.
3. **Task type** — exactly one of:
   - `research`
   - `analyze`
   - `project_compare`
   - `source_compare`
   - `gap_analysis`

If any value is missing and cannot be inferred safely, ask for the missing value before continuing. If the user supplied all three, begin immediately.

## Source of Truth Policy

Use these sources first:

1. `https://uo.com/wiki/ultima-online-wiki/` — primary official/current Broadsword source.
2. `https://www.uoguide.com/Main_Page` — deeper historical, mechanical, and gameplay details.
3. `https://uoalive.com/wiki/UOA` — additional structured reference when useful.
4. `https://uo.stratics.com/` — additional historical/mechanics cross-check when available, especially if the user or repo workflow requires Stratics verification.

Priority and conflict rules:

- Prefer `uo.com` when it contains official or current Broadsword information.
- Use UOGuide for historical depth, older-era behavior, formulas, requirements, and gameplay details.
- Use UOAlive as supporting structured reference, not as the sole authority when official or UOGuide sources exist.
- Use Stratics as a strong secondary historical reference when available.
- If sources conflict, document the conflict explicitly in `Source Notes`; never silently merge conflicting claims.
- Every factual game claim must include a visible source reference.
- Mark absent, unclear, or contradictory information as `unknown` rather than inventing mechanics.

## Workflow Selection

Choose the workflow from the task type:

| Task Type | Workflow | Primary Output |
|---|---|---|
| `research` | Internet Research | `game-docs/GameDocs/01_Broadsword` |
| `analyze` | Internet Research | `game-docs/GameDocs/01_Broadsword` |
| `project_compare` | Documentation-to-Source-Code | `game-docs/GameDocs/02_Project_Parity` |
| `source_compare` | Documentation-to-Source-Code | `game-docs/GameDocs/02_Project_Parity` |
| `gap_analysis` | Documentation-to-Source-Code | `game-docs/GameDocs/02_Project_Parity` |

Compatibility note: if the user explicitly requests `GameDocs/02_Open_Parity`, confirm whether this is an intentional alternate tree. RebirthUO's established implementation-status mirror is `game-docs/GameDocs/02_Project_Parity`.

## Internet Research Workflow

Use for `research` and `analyze`.

Output root:

```text
game-docs/GameDocs/01_Broadsword
```

Procedure:

1. **Normalize scope.** Convert the user-supplied era and topic area into path-safe separators, e.g. `Mondain's Legacy` -> `Mondains_Legacy`.
2. **Split broad topics into atomic elements.** If the user asks for a whole topic area, enumerate one skill, spell, monster, item property, quest, formula, region, dungeon, or mechanic per future page.
3. **Search all relevant sources of truth.** Check uo.com, UOGuide, and UOAlive; add Stratics when it is relevant or when repo policy requires it.
4. **Capture exact mechanics.** Record requirements, values, caps, durations, limitations, dependencies, and PvP/PvM/economy side effects.
5. **Separate fact from assumption.** Facts get source links; assumptions and unresolved conflicts go to `Source Notes`.
6. **Write one page per atomic element.** Store under `game-docs/GameDocs/01_Broadsword/<TopicArea>/<Era>/<AtomicInformationElement>.md` unless an existing per-mechanic tree uses a deeper folder/README pattern.
7. **Reuse existing docs.** Read nearby files and update existing pages when extending; avoid duplicate pages.
8. **Run the mandatory cross-reference pass.** Search the docs tree for names, aliases, and related mechanics; update `Related Elements` both ways when appropriate.

Completion criterion: every requested atomic element has exactly one documented page or a recorded `unknown`/not-found note with checked sources.

## Documentation-to-Source-Code Workflow

Use for `project_compare`, `source_compare`, and `gap_analysis`.

Comparison source:

```text
game-docs/GameDocs/01_Broadsword
```

Comparison target:

```text
RebirthUO project source code
```

Parity output root:

```text
game-docs/GameDocs/02_Project_Parity
```

Procedure:

1. **Start from atomic documentation.** Read the relevant `01_Broadsword` page(s). If no documentation exists, create/request the Broadsword documentation first; do not compare assumptions.
2. **Derive search terms.** Use exact name, normalized name, aliases, class names, enum names, item IDs, spell IDs, skill IDs, system terminology, and source-specific terms.
3. **Search source broadly.** Inspect `Projects/UOContent`, `Projects/Server` only when needed, tests, data files, configuration, serialization, and registration points.
4. **Trace implementation.** Identify the element itself, constants, configuration, behavior, serialization, event hooks, tests, and generated/registration paths.
5. **Compare expected to actual.** Use the documented behavior as the expected behavior and code references as evidence.
6. **Assign exactly one status.** Use `complete`, `partial`, `missing`, or `unknown`.
7. **Write the parity page.** Store under `game-docs/GameDocs/02_Project_Parity/<TopicArea>/<Era>/<AtomicInformationElement>.md`.
8. **Run the mandatory cross-reference pass.** Link canonical docs, parity docs, related mechanics, and any existing implementation-status files.

Completion criterion: every parity judgment is backed by source-code evidence or explicitly marked `unknown` because evidence is insufficient.

## Documentation Structure

Documentation must be organized by:

1. documentation area;
2. topic area;
3. era separator;
4. atomic information element.

Internet documentation:

```text
game-docs/GameDocs/01_Broadsword/<TopicArea>/<Era>/<AtomicInformationElement>.md
```

Examples:

```text
game-docs/GameDocs/01_Broadsword/Skills/Age_of_Shadows/Necromancy.md
game-docs/GameDocs/01_Broadsword/Spells/Mondains_Legacy/Spellweaving.md
game-docs/GameDocs/01_Broadsword/Monsters/Modern_Broadsword/Dread_Horn.md
```

Parity documentation:

```text
game-docs/GameDocs/02_Project_Parity/<TopicArea>/<Era>/<AtomicInformationElement>.md
```

Examples:

```text
game-docs/GameDocs/02_Project_Parity/Skills/Age_of_Shadows/Necromancy.md
game-docs/GameDocs/02_Project_Parity/Spells/Mondains_Legacy/Spellweaving.md
game-docs/GameDocs/02_Project_Parity/Monsters/Modern_Broadsword/Dread_Horn.md
```

If an existing canonical tree follows the RebirthUO Knot schema with subfolders and README indexes, follow that local structure instead of flattening it.

## Atomic Information Element Rule

Each page describes exactly one atomic information element: the smallest useful independently verifiable game concept.

Examples:

- one skill;
- one spell;
- one monster;
- one item property;
- one quest;
- one artifact;
- one crafting recipe;
- one combat mechanic;
- one pet ability;
- one virtue;
- one dungeon;
- one region;
- one special move;
- one formula.

Bad:

```text
game-docs/GameDocs/01_Broadsword/Skills/Age_of_Shadows/Magic_Skills.md
```

Good:

```text
game-docs/GameDocs/01_Broadsword/Skills/Age_of_Shadows/Necromancy.md
game-docs/GameDocs/01_Broadsword/Skills/Mondains_Legacy/Spellweaving.md
game-docs/GameDocs/01_Broadsword/Skills/Age_of_Shadows/Magery.md
```

Do not combine unrelated elements into one page. Use links between atomic pages instead of repeated large blocks.

## Internet Research Page Template

Use for pages under `game-docs/GameDocs/01_Broadsword` unless a local Knot-schema page already exists.

```markdown
# <Atomic Information Element>

## Metadata

- Era: <Era>
- Topic Area: <TopicArea>
- Element Type: <Skill | Spell | Monster | Item | System | Mechanic | Quest | Other>
- Sources:
  - <Source URL 1>
  - <Source URL 2>
  - <Source URL 3>

## Summary

Short description of the element and its role in Ultima Online.

## Era Context

Explain when this element belongs to the selected era and whether it existed before, changed during, or was introduced in that era.

## Mechanics

Document known mechanics as atomic, verifiable statements.

- The ability does X. [<source>]
- The effect applies Y. [<source>]
- The duration is Z. [<source>]
- The requirement is A. [<source>]
- The limitation is B. [<source>]

## Values and Rules

| Property | Value | Source |
|---|---:|---|
| <Property> | <Value> | <Source URL> |

## Related Elements

- `<Relative path to related document>`
- `<Relative path to related document>`

## Source Notes

Document uncertainty, source conflicts, missing details, or outdated information.

## Verification Status

- Status: `researched`
- Last Reviewed: `<YYYY-MM-DD>`
```

## Parity Page Template

Use for pages under `game-docs/GameDocs/02_Project_Parity`.

```markdown
# <Atomic Information Element> - Project Parity

## Metadata

- Era: <Era>
- Topic Area: <TopicArea>
- Element Type: <Skill | Spell | Monster | Item | System | Mechanic | Quest | Other>
- Documentation Source:
  - `<Relative path to game-docs/GameDocs/01_Broadsword document>`
- Source Code References:
  - `<Relative path to source file>`
  - `<Relative path to source file>`

## Expected Behavior

Summarize the expected behavior from the Broadsword documentation.

## Source Code Findings

| Code Location | Finding |
|---|---|
| `<file path>` | `<short explanation>` |

## Parity Status

Use exactly one status:

- `complete`
- `partial`
- `missing`
- `unknown`

## Gap Analysis

Describe what is missing, incomplete, inconsistent, or unclear.

## Implementation Notes

Document useful notes for future implementation or refactoring.

## Tests

| Test | Status | Notes |
|---|---|---|
| `<test name or required test>` | `existing | missing | recommended` | `<notes>` |

## Related Elements

- `<Relative path to related document>`
- `<Relative path to related parity document>`

## Verification Status

- Status: `compared`
- Last Reviewed: `<YYYY-MM-DD>`
```

## Parity Status Definitions

Use exactly one status:

- **`complete`** — documented behavior appears implemented and no meaningful gaps were found.
- **`partial`** — the element exists, but one or more mechanics, values, conditions, effects, tests, or edge cases are missing or inconsistent.
- **`missing`** — the documented element does not appear in source code.
- **`unknown`** — documentation, source code, naming, or implementation path is too unclear for a reliable judgment.

## Mandatory Cross-Reference Pass

Whenever documentation is created or extended, perform this pass for both `01_Broadsword` and `02_Project_Parity` output.

1. Search the complete documentation tree for the atomic element name, aliases, related mechanics, related items, related spells, related skills, related monsters, and related systems.
2. If related documentation exists, add references in `Related Elements`.
3. If the current page should be referenced from an existing page, update the existing page as well.
4. Avoid duplicate documentation.
5. Prefer links between atomic pages over repeated large text.
6. If a duplicate or overlapping page is found, report it and suggest consolidation.

## Output Report

After completing a task, report:

```markdown
## Result

- Era: <Era>
- Topic Area: <TopicArea>
- Task: <Task>
- Created:
  - `<path>`
- Updated:
  - `<path>`
- Compared:
  - `<path>`
- Status:
  - `<researched | analyzed | compared | gaps_found | no_changes>`
- Notes:
  - <important notes>
```

For parity tasks, also include:

```markdown
## Parity Summary

| Element | Status | Documentation | Source Code | Notes |
|---|---|---|---|---|
| <Element> | <complete | partial | missing | unknown> | <path> | <path or none> | <notes> |
```

## Quality Bar

A result is acceptable only when:

- the requested era is represented as a path separator;
- each atomic information element has its own page;
- internet documentation is stored under `game-docs/GameDocs/01_Broadsword`;
- documentation-to-code comparison is stored under `game-docs/GameDocs/02_Project_Parity` unless the user explicitly chose another tree;
- every factual game claim has a source reference;
- every parity judgment has source-code evidence or is marked `unknown`;
- the final cross-reference pass has been performed;
- existing documentation was reused or linked instead of duplicated;
- broad topic areas were split into atomic elements before writing;
- source conflicts are visible in `Source Notes`.

## Failure Handling

If required information cannot be found:

1. Do not invent it.
2. Mark the value as `unknown`.
3. Record which sources were checked.
4. Explain what is missing.
5. Create a research note or follow-up note when useful.

If source code cannot be inspected:

1. Do not perform a definitive parity judgment.
2. Mark status as `unknown`.
3. Explain that source-code access is required.
4. Keep researched documentation separate from parity documentation.

## Common Pitfalls

1. **Skipping the era.** UO mechanics are era-sensitive; missing era means the output cannot be trusted.
2. **Writing broad pages.** `Magic_Skills.md` or `All_ML_Quests.md` hides atomic parity. Split first.
3. **Mixing sources without conflict notes.** If uo.com and UOGuide disagree, record both and state the conflict.
4. **Comparing undocumented assumptions.** Source comparison starts from `01_Broadsword`, not memory.
5. **Treating missing search results as proof.** Search aliases, IDs, enums, class names, registration code, data files, and tests before calling something `missing`.
6. **Using `02_Open_Parity` by accident.** RebirthUO's current parity tree is `02_Project_Parity`; only use another tree if the user explicitly requests it.
7. **Forgetting the cross-reference pass.** The task is not complete until related pages are linked and duplicates are reported.

## Verification Checklist

- [ ] Era, topic area, and task type are known.
- [ ] Workflow selected from the allowed task type.
- [ ] Sources checked and source priority applied.
- [ ] Broad topic split into atomic elements.
- [ ] One page per atomic element.
- [ ] All factual claims visibly sourced or marked `unknown`.
- [ ] Internet docs written under `game-docs/GameDocs/01_Broadsword`.
- [ ] Parity docs written under `game-docs/GameDocs/02_Project_Parity` when applicable.
- [ ] Source code searched by exact name, normalized name, aliases, IDs, enums, classes, and system terms.
- [ ] Parity status is exactly one of `complete`, `partial`, `missing`, `unknown`.
- [ ] Cross-reference pass completed and duplicate/overlap issues reported.
- [ ] Final report includes created, updated, compared paths and parity summary when applicable.
