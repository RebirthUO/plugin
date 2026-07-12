---
name: uo-game-docs-canonical-authoring
description: Use when a configured project asks to create or audit official-era UO documentation in its game-docs canonical tree with one file per mechanic, Knot-schema sections, linked indexes, and parity cross-references. Do not use for implementation-status parity files, code changes, or chat-only summaries.
version: 1.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - ultima-online
      - documentation
      - game-docs
      - broadsword
      - canonical-era
    category: software-development
    related_skills:
      - uo-official-evidence
      - modernuo-era-expansion
      - uo-living-world-review
---

# UO Canonical-Era Game Docs

## Boundary

Own canonical behavior documents under `game-docs/GameDocs/01_Broadsword/<Domain>/<Era>/`. Canonical files say what UO does; `02_Project_Parity/` says what the project implements. Keep those claims separate.

## Core Workflow

1. Resolve the repository root, read its instructions, and require an explicitly
   configured canonical-doc tree and parity tree. If the layout is absent or
   ambiguous, ask the user and stop rather than inventing directories.
2. Establish the era/publish and official behavior with `uo-official-evidence`. Community sources may locate official material but never fill a gameplay claim; unresolved values block canonical authoring.
3. Inventory every mechanic before writing. Create one topic folder and `README.md` per coherent skill/system plus one Markdown node per mechanic or independent hook; do not collapse the result into a flat summary.
4. Apply the Knot schema from [knot-schema.md](references/knot-schema.md) to every node. Keep formulas, caps, PvP/PvM/economy effects, repository anchors, and sources distinct.
5. Update the domain/era README and topic README with relative links. Re-read `00_Index/README.md` immediately before editing it so concurrent additions are preserved.
6. Audit the matching parity document and add links to canonical nodes without copying implementation status into `01_Broadsword`.
7. Validate the tree, links, required headings, source fields, and node counts; report unresolved evidence instead of inventing it.

## Guardrails

- One mechanic or independent hook equals one node file. A single “skill list” document is not the requested artifact.
- Pick one language per node. Preserve source terminology only where precision requires it.
- A local repository anchor documents comparison surface; it does not convert repository behavior into canonical UO truth.
- Never copy long source prose. Paraphrase mechanics and cite the exact page.
- Do not modify code or parity status unless the user separately requests that work.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Return the created/updated tree, era and source status, mechanic inventory, links/index changes, parity cross-references, repository anchors, validation results, and every `Needs source confirmation` gap. Name any intentionally deferred nodes.

## Verification

- Each domain/era and topic directory has a linked `README.md`.
- Each inventoried mechanic/hook has exactly one node using all Knot sections.
- Every formula or publish claim has a source or explicit evidence gap.
- Relative links resolve; index edits preserve concurrent rows.
- Canonical and parity claims remain in their respective trees.

## Reference Routing

Read [Knot schema and tree rules](references/knot-schema.md) before creating nodes. Load the relevant UO mechanics skill for the topic, `uo-official-evidence` for source authority, `uo-living-world-review` for cross-system effects, and `modernuo-content-taxonomy` only for the parity mirror.
