# Parity Check & Bestandsaufnahme

Every activation of `modernuo-content-taxonomy` must produce a **full 9-domain inventory** and compare ModernUO against official Ultima Online sources before classification or implementation advice.

## Source Hierarchy

Use sources in this order. Do not skip lower tiers when a higher tier has no answer.

1. **Repo-internal** — `dev-docs/eras/` (parity claims, anchors, open gaps), [`mappings.md`](mappings.md), era-specific reference classes (e.g. `MondainsLegacySourceReferences`)
2. **UO.com** — official wiki: `https://uo.com/wiki/ultima-online-wiki/`
3. **UOGuide** — community reference: `https://www.uoguide.com/`
4. **Web search** — only when UO.com/UOGuide disagree, omit facts, or lack URLs for the scoped content
5. **Stratics** — secondary fallback only (already used in ML parity work; do not prefer over UO.com/UOGuide)

### UOGuide URL Convention

- Base: `https://www.uoguide.com/{Title_With_Underscores}`
- Spaces → `_`; apostrophes → `%27` when needed (e.g. `Dryad%27s_Blessing`)
- Category pages: `Skill`, `Quest`, `Crafting`, `Named_Monsters`, `Peerless`, `Artifacts_(Peerless)`

### Era Profile

Parity is always relative to a target expansion/profile:

- `Core.Expansion` / `Core.ML`, `Core.SA`, etc. — see `modernuo-era-expansion.md`
- `Distribution/Configuration/EraProfiles/` — RebirthUO profile JSON
- If the user has not specified an era, **ask** before claiming `Present` or `Gap`

## Parity Status Legend

| Status | Meaning |
|---|---|
| `Present` | Implemented and matches official sources for the target era profile |
| `Partial` | Implemented with known gaps (stats, mechanics, spawn, loot, access) |
| `Gap` | Documented in OSI sources but missing or not wired in ModernUO |
| `Enhanced` | Intentional RebirthUO deviation or addition beyond OSI (QoL, extra content, wired seams ahead of source lock, profile-specific tuning) |
| `SourceLocked` | Effect facts confirmed by approved sources; values implemented in code |
| `RuntimeBlocked` | Source-locked facts exist; live trigger/cadence/hook not wired to combat |

`Enhanced` is **not** a failure — list it separately so reviewers can distinguish bugs from design choices.

Repo parity legend (era docs): [`dev-docs/eras/README.md`](../../eras/README.md).

## Mandatory Workflow

Run all six steps on every skill activation:

1. **Clarify era profile** — `Core.Expansion`, `EraProfiles/`, or ask the user
2. **Build 9-domain matrix** — one summary row per taxonomy domain (see report template)
3. **Scan repo** — `mappings.md` paths, matching `dev-docs/eras/{expansion}.md`, grep/code search for focus entity
4. **Cross-check UO.com + UOGuide** — use domain category URLs below; for ML use `MondainsLegacySourceReferences` constants
5. **Resolve open points** — `WebSearch` / `WebFetch` when sources conflict or lack detail
6. **Emit mandatory report** — full matrix + three lists + focus + open research (always, even for narrow questions)

### Efficiency Rules

- Matrix rows are **domain summaries**, not a full item/mobile catalog
- **Deep parity** (field-by-field) only for the user's focus + direct dependencies
- Pre-seed from `mappings.md` gap notes and era doc `Open gaps` sections
- Cite URLs for every `Gap`, `Partial`, and `Enhanced` entry

## Domain Category URLs (UO.com / UOGuide)

Use these for matrix cross-checks. Replace with entity-specific URLs when the focus is narrower.

| Domain | UO.com (starting point) | UOGuide (starting point) |
|---|---|---|
| World | [World](https://uo.com/wiki/ultima-online-wiki/world/) | [Places](https://www.uoguide.com/Places) |
| Entity | [Items](https://uo.com/wiki/ultima-online-wiki/items/) · [Creatures](https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/) | [Items](https://www.uoguide.com/Items) · [Creatures](https://www.uoguide.com/Creatures) |
| ItemSystem | [Items](https://uo.com/wiki/ultima-online-wiki/items/) · [Artifact collections](https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/) | [Item Properties](https://www.uoguide.com/Item_Properties) · [Artifacts](https://www.uoguide.com/Artifacts) |
| MobileSystem | [PvM / named creatures](https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/) | [Creatures](https://www.uoguide.com/Creatures) · [Named Monsters](https://www.uoguide.com/Named_Monsters) |
| Progression | [Skills](https://uo.com/wiki/ultima-online-wiki/skills/) · [Spells](https://uo.com/wiki/ultima-online-wiki/skills/magery-spells/) | [Skills](https://www.uoguide.com/Skill) · [Spells](https://www.uoguide.com/Spells) |
| EconomyCrafting | [Crafting](https://uo.com/wiki/ultima-online-wiki/gameplay/crafting/) · [Complete recipe list](https://uo.com/wiki/ultima-online-wiki/gameplay/crafting/complete-recipe-list/) | [Crafting](https://www.uoguide.com/Crafting) · [Resources](https://www.uoguide.com/Resources) |
| QuestNarrative | [Quests](https://uo.com/wiki/ultima-online-wiki/gameplay/quests/) · [Peerless quests](https://uo.com/wiki/ultima-online-wiki/gameplay/quests/peerless-quests/) | [Quest](https://www.uoguide.com/Quest) · [Peerless](https://www.uoguide.com/Peerless) |
| Encounter | [Champion spawns](https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/champion-spawns/) · [Treasure Maps](https://uo.com/wiki/ultima-online-wiki/items/maps/treasure-maps/) | [Champion Spawns](https://www.uoguide.com/Champion_Spawns) · [Treasure Map](https://www.uoguide.com/Treasure_Map) |
| ClientPresentation | [Client](https://uo.com/wiki/ultima-online-wiki/technical/client/) (limited) | [Gumps](https://www.uoguide.com/Gumps) (community) |

### ML-Specific Reference Class

For Mondain's Legacy parity, prefer constants in `Projects/UOContent/Misc/MondainsLegacySourceReferences.cs` over ad-hoc URLs. Pair each `*UO` with its `*UOGuide` sibling.

## Mandatory Report Template

Copy this structure into **every** taxonomy skill response:

```markdown
## Bestandsaufnahme (9 Domains)

| Domain | ModernUO (summary) | UO.com | UOGuide | Status |
|--------|-------------------|--------|---------|--------|
| World | … | … | … | Present / Partial / Gap |
| Entity | … | … | … | … |
| ItemSystem | … | … | … | … |
| MobileSystem | … | … | … | … |
| Progression | … | … | … | … |
| EconomyCrafting | … | … | … | … |
| QuestNarrative | … | … | … | … |
| Encounter | … | … | … | … |
| ClientPresentation | … | … | … | … |

**Era profile:** {expansion or profile name}

## Fehlend (Gap)

- [Domain] … — Quelle: {URL}

## Unvollständig (Partial / SourceLocked / RuntimeBlocked)

- [Domain] … — what is missing — Quelle: {URL}

## Enhanced (RebirthUO ≠ OSI)

- [Domain] … — deviation — reason if known

## Fokus dieser Anfrage

- Taxonomy classification: …
- Recommended paths: …

## Offene Punkte / Recherche

- …

## Issue Slice Options

- I can convert these findings into single sliced Markdown issues on request. Each issue should cover one independently actionable gap, partial implementation, runtime blocker, enhanced-deviation decision, or unresolved research decision, with evidence, impact, acceptance criteria, validation notes, and open questions.
```

## Markdown Delivery and Issue Slicing

Every taxonomy parity report must be delivered as Markdown and end with `## Issue Slice Options`. Do not create issue drafts or tracker issues unless the user asks.

When slicing is requested, create one independently actionable issue per finding. Do not bundle unrelated gaps, partial implementations, runtime blockers, enhanced-deviation decisions, or unresolved research decisions into the same issue just because they share a taxonomy domain.

## Deep Parity Checklist (focus entity)

When the user names a specific entity (boss, item, quest, skill), also verify:

| Check | Repo | External |
|---|---|---|
| Type exists | C# class under expected path | UOGuide page exists |
| Stats / properties | ctor defaults, `GetProperties` | UOGuide statistics table |
| Abilities / specials | `MonsterAbility`, spells, hooks | UO.com + UOGuide ability sections |
| Loot / rewards | `GenerateLoot`, artifact tables | UOGuide loot lists |
| Access / keys | `PeerlessAltar`, quest regions | Peerless quest pages |
| Spawns | `Data/Spawns/`, spawner JSON | Dungeon/region pages |
| Era gating | `Core.*` branches, era profile JSON | Expansion intro publish notes |

Document `SourceLocked` vs `RuntimeBlocked` separately when mechanics are confirmed but not live-wired (see era doc anchors, e.g. `mondains-legacy.md#dread-horn`).

## Maintenance

When parity work changes implementation status:

1. Update the relevant `dev-docs/eras/{expansion}.md` anchor and parity table
2. Add a short code back-reference: `// Era: dev-docs/eras/mondains-legacy.md#entity-slug`
3. Refresh gap notes in [`mappings.md`](mappings.md) **Known cross-domain gaps** if the gap is structural

Do not store long URL prose in boss classes — use `MondainsLegacySourceReferences` or era doc anchors.
