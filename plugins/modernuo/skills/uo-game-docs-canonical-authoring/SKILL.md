---
name: uo-game-docs-canonical-authoring
description: Use when authoring canonical-era RebirthUO game-docs under game-docs/GameDocs/01_Broadsword with one file per mechanic, Knot schema, README indexes, and mirrored parity skeletons.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    - UltimaOnline
    - RebirthUO
    - GameDocs
    - Documentation
    - Broadsword
    - CanonicalEra
    category: software-development
    related_skills:
    - uo-domain-research
    - uo-era-product-timeline
    - uo-living-world-review
    - uo-modernuo-workflow
license: MIT
---
# RebirthUO `game-docs/` Canonical-Era Authoring

## Overview

This skill captures the canonical documentation pattern RebirthUO uses under `game-docs/GameDocs/01_Broadsword/<Domain>/<Era>/*`. It applies to every era and every domain where the user asks for canonical/era documentation that lives in the repo.

## When to Use

- "Erstelle eine Skill-Liste für Samurai Empire."
- "Dokumentiere Bushido und Ninjitsu im `game-docs/`."
- "Schreib eine Broadsword-Übersicht für Mondain's Legacy."
- "Ich brauche eine canonical Spell-Doku für Stygian Abyss."
- Any request for canonical/era documentation that should land in `game-docs/GameDocs/01_Broadsword/<Domain>/<Era>/`.
- Any request to extend, restructure, or audit an existing `01_Broadsword/` canonical tree.

Do **not** use for:

- Implementation-status parity work — that's `02_Project_Parity/<Domain>/<Era>/<topic>.md` and `uo-modernuo-era-parity-check`.
- Skill/Spell code work in `Projects/UOContent/` — that's `uo-samurai-empire-skills`, `uo-magic-spells`, `modernuo-content-patterns`.
- A chat-only summary that won't land in the repo.

## Prerequisites

- The RebirthUO repo at `C:\Users\Jsiem\Documents\GitHub\RebirthUO` with `game-docs/GameDocs/` already present.
- For SE work: `uo-samurai-empire-skills` for the canonical Bushido/Ninjitsu source data, `uo-era-product-timeline` for the era-position context.
- For ML/SA/ToL/EJ work: the matching `uo-<topic>-<era>` skill (e.g. `uo-quests-engine-ml` for ML quests).
- For `02_Project_Parity/<Domain>/<Era>/` parity files: `modernuo-era-parity-check` to anchor implementation status.
- No credentials, no extra packages — Hermes tools only.

## Tree Shape (canonical pattern)

The user has explicitly rejected flat "skill list with subcategory heading" outputs. The canonical deliverable is a **per-mechanic file tree** with one node per documented mechanic, each following the Knot schema below.

```
game-docs/GameDocs/01_Broadsword/<Domain>/<Era>/
├── README.md                       # <Domain>/<Era> entry point + node index
├── <skill-or-topic-1>/
│   ├── README.md                   # skill/topic overview (table of nodes)
│   ├── <mechanic-1>.md             # one node per documented mechanic
│   ├── <mechanic-2>.md
│   └── ...
└── <skill-or-topic-2>/
    ├── README.md
    └── ...
```

Concrete example for SE Skills (`<Domain>` = `Skills`, `<Era>` = `Samurai_Empire`):

```
01_Broadsword/Skills/Samurai_Empire/
├── README.md
├── bushido/
│   ├── README.md
│   ├── honorable-execution.md
│   ├── confidence.md
│   ├── counter-attack.md
│   ├── lightning-strike.md
│   ├── evasion.md
│   ├── momentum-strike.md
│   ├── perfection.md
│   ├── weapon-parry.md
│   ├── whirlwind-bonus.md
│   ├── special-moves-without-tactics.md
│   └── lesser-hiryu-riding.md
└── ninjitsu/
    ├── README.md
    ├── animal-form.md
    ├── mirror-image.md
    ├── focus-attack.md
    ├── backstab.md
    ├── shadowjump.md
    ├── surprise-attack.md
    ├── ki-attack.md
    ├── death-strike.md
    ├── ninja-equipment.md
    ├── special-moves-without-tactics.md
    └── tier-3-talismans.md
```

The same shape applies to **Spells**, **Combat**, **Crafting**, **Dungeons**, **Economy**, **Events**, **Facets**, **Housing**, **Items**, **Mobiles**, **Pets**, **Quests**, **Systems** — one README per skill/topic, one `.md` per mechanic.

## Knot Schema (every per-mechanic `.md`)

Every node file follows the same six-section shape (canonical Broadsword):

1. **Kopfblock** — `Skill`, `Typ` (one of `Active`, `Active (Defensiv)`, `Active (Stealth)`, `Active (Teleport)`, `Active (Morph)`, `Passiv`, `Hook (Item)`, `Hook (Pet)`, `Hook (Special-Move)`), `Mana`, `Skill-Gate`, canonical source URL.
2. **Kurzfassung** — 1–2 sentences in the canonical source's wording (uo.com primary, Stratics/UOGuide secondary). Keep the source's exact phrasing for mechanically precise terms (e.g. "PvP damage is capped at 50 %").
3. **Voraussetzungen** — Skill-Gate, Begleitskills (e.g. Hiding/Stealth for Ninjitsu), Trainer-Anker (Zento / New Haven Dojo for SE, Heartwood for ML, etc.), item requirements (Book of Bushido, Scribe-Purchase, etc.).
4. **Mechanik** — table with formulas, caps, PvP-DR, PvP-Cap. Use source-locked values; mark unknowns as `Needs source confirmation`. For era-cross-cutting hooks (e.g. Bushido-90 ersetzt Animal Taming), include the cross-skill formula explicitly.
5. **PvP/PvM/Economy** — short product-impact row:
   - **PvP:** counterplay, burst, DR/Cap effects, solo-vs-group balance.
   - **PvM:** sustain, AoE, anti-burst, solo-vs-group balance.
   - **Economy:** faucets (Books, Loot), sinks (Reagenzien, Bandagen), tradeability/insurance.
   - **Housing / new players / veterans:** if relevant, one line each.
6. **Repo-Anker** — concrete `Projects/UOContent/Skills/<Skill>.cs`, `Projects/UOContent/Spells/<School>/<Ability>.cs`, `Projects/UOContent/Mobiles/Tameable/<Pet>.cs` paths. Cite with `file:line` where known.
7. **Quellen** — primary (uo.com wiki URL), secondary (Stratics, UOGuide).

## README Files (three layers)

- **Top-level `01_Broadsword/<Domain>/<Era>/README.md`** — entry point. Lists every skill/topic folder as a relative markdown link, with a one-line summary of each.
- **Per-skill `<Domain>/<Era>/<skill>/README.md`** — for that skill, lists every mechanic node as a relative markdown link in a `| Mechanik | Mana | Skill-Gate | Knoten |` table. Includes the trainer anchor, book purchase, and cap-100 declaration.
- **Per-topic if not skill-shaped** — same shape: entry point + per-mechanic nodes (e.g. `01_Broadsword/Items/Samurai_Empire/` for SE weapons).

## Cross-References

- **`02_Project_Parity/<Domain>/<Era>/<topic>.md`** — implementation-status mirror. The Broadsword side is canonical (what UO does); the parity side is repo-anchored (what RebirthUO currently does). When a node on the canonical side changes, audit the matching parity file. When the parity file advances from "Triage required" to "Human Review", the canonical file is unchanged.
- **`01_Broadsword/Systems/<Era>.md`** — the era-overview umbrella that the skill/system/etc. nodes reference via relative links. The era-overview file lists the per-domain trees it points to.
- **`00_Index/README.md`** — the top-level index that lists every era and domain. Update it whenever you create a new `<Domain>/<Era>/` tree.

## Procedure

1. **Read the era-overview anchor first.** Read `01_Broadsword/Systems/<Era>.md` to understand what the era officially adds. This is the canonical "what does UO say" answer that the per-mechanic nodes will cite.
2. **Map the skills/topics.** For each skill or topic the era adds, list the per-mechanic nodes you will create. Use the loaded `uo-<era>-<topic>` skill's table as the source-locked node list (e.g. `uo-samurai-empire-skills` already has Bushido's 8 + 3 hooks and Ninjitsu's 8 + 3 hooks tabulated — copy those into the README table).
3. **Create the tree.** Use `mkdir -p` (or `write_file` for each file with auto-created directories). Start with the top-level `README.md`, then the per-skill `README.md`, then every per-mechanic `.md`. Order nodes by skill-gate ascending so the README table reads as a progression.
4. **Apply the Knot schema to every node.** Run through the seven-section template for every node; do not skip the Repo-Anker or Quellen section even if the node is short. The schema is what makes the tree canonical.
5. **Update `00_Index/README.md` last.** Add a row for the new `<Domain>/<Era>/` tree (or extend the existing one). **Always re-read the file before patching** — sibling subagents may have added rows since your last read (parallel-workspace warning: patch tool returns `_warning` when a sibling touched the file).
6. **Verify the tree.** `find` the tree, count `.md` files, confirm one README per skill + one per node, confirm every node has a `Quellen` section pointing back to uo.com or a marked `Needs source confirmation`.

## Pitfalls

- **Defaulting to a single flat Markdown.** The user's previous explicit correction: "Nein dies ist leider falsch. Ich wollte die offizielle Broadsword definition haben und unter broadsword/skills/Samurai_Empire/* jeweils einen Knoten je Dokumentation." A single "skill list with subcategory heading" output is wrong and forces a rewrite. Always produce the per-mechanic file tree.
- **Skipping the Repo-Anker section.** The Knot schema's section 6 is what makes the canonical doc useful for parity work. A node without a repo anchor is a chat-only summary that can't be cross-referenced from `02_Project_Parity/`.
- **Skipping the Quellen section.** Section 7 must cite at least uo.com or Stratics/UOGuide; `Needs source confirmation` is allowed but the field must be filled. Empty `Quellen` is the canonical-doc equivalent of a missing citation in a SKILL.md.
- **Collapsing Hook nodes into the parent skill.** Hooks (Whirlwind-Bonus, Special-Moves-without-Tactics, Lesser-Hiryu-Riding, Tier-3-Talismane, Ninja-Equipment) are independent mechanics and get their own `.md` files. They share a parent skill via cross-link, not via inline consolidation.
- **Treating `02_Project_Parity/<Domain>/<Era>/` parity files as canonical-doc.** The parity tree is implementation-status only; the Broadsword tree is canonical-behavior only. Do not write canonical UO behavior into a parity file or vice versa.
- **Editing `00_Index/README.md` without re-reading.** Sibling subagents modify this file concurrently. The patch tool returns a `_warning` when a sibling touched it; always re-read before retrying or you clobber the sibling's additions. Prefer `patch` (replace) over `write_file` for index updates.
- **Putting German/English mix into the same node file.** Pick one language per node and stick to it (the SE-Skills tree is German — canonical German for German-shard design). Do not mix except for canonical source citations (which stay in the source's language).

## Verification Checklist

- [ ] Top-level `01_Broadsword/<Domain>/<Era>/README.md` exists and links to every per-skill/topic folder.
- [ ] Every per-skill/topic folder has its own `README.md` with a table linking to every per-mechanic node.
- [ ] Every per-mechanic `.md` follows the seven-section Knot schema (Kopfblock, Kurzfassung, Voraussetzungen, Mechanik, PvP/PvM/Economy, Repo-Anker, Quellen).
- [ ] Every node cites at least one canonical source (uo.com / Stratics / UOGuide) or marks `Needs source confirmation`.
- [ ] Every node has a concrete Repo-Anker (file:line where known).
- [ ] `00_Index/README.md` has a row pointing at the new tree, and was re-read immediately before the patch (no clobbered sibling edits).
- [ ] If a `02_Project_Parity/<Domain>/<Era>/<topic>.md` parity file exists, it references the canonical nodes it mirrors.

## Related Skills

- `uo-domain-research` — the umbrella that codifies this recipe as its "Phase 6 Fast Recipe: `game-docs/` authoring".
- `uo-samurai-empire-skills` — provides the source-locked Bushido/Ninjitsu data and the per-mechanic node list for SE-Skills authoring.
- `uo-era-product-timeline` — era-position context (where SE sits in the UO timeline, AoS prerequisite vs SE vs ML/SA).
- `modernuo-era-parity-check` — for the `02_Project_Parity/` implementation-status mirror.
- `uo-modernuo-workflow` — overall RebirthUO working conventions, AGENTS.md / CLAUDE.md compliance.