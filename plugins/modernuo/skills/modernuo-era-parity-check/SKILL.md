---
name: modernuo-era-parity-check
description: >
  Produces a fine-grained Ultima Online era/add-on parity report for RebirthUO/ModernUO
  by comparing source code against UO.com, UOGuide, and Stratics. Requires a valid era name
  (expansion or EraProfile). Covers races, skills, stats, spells, items, world, combat,
  crafting, pets, housing, quests, and game mechanics. Use when auditing expansion parity,
  scoping addon content, or answering what exists vs what is missing for a target era.
---

# Ultima Online Addon/Era Parity Check

## When This Activates

- User asks for an era or add-on parity check, inventory, or gap analysis
- User wants to know what content exists vs is missing for a specific expansion
- User is scoping work for a publish, expansion, or `EraProfile`
- User names a creature, item, system, or mechanic and wants era-scoped parity evidence

## Hard Gate: Valid Era Required

**Do not run the parity workflow until the user supplies a valid era.**

If missing or ambiguous, ask using this list:

| Display name | Enum | Core check | Era doc |
|---|---|---|---|
| Original UO | `None` | (pre-`Core.T2A`) | `dev-docs/eras/original-uo.md` |
| The Second Age | `T2A` | `Core.T2A` | `dev-docs/eras/the-second-age.md` |
| Renaissance | `UOR` | `Core.UOR` | `dev-docs/eras/renaissance.md` |
| Third Dawn | `UOTD` | `Core.UOTD` | `dev-docs/eras/third-dawn.md` |
| Lord Blackthorn's Revenge | `LBR` | `Core.LBR` | `dev-docs/eras/lord-blackthorns-revenge.md` |
| Age of Shadows | `AOS` | `Core.AOS` | `dev-docs/eras/age-of-shadows.md` |
| Samurai Empire | `SE` | `Core.SE` | `dev-docs/eras/samurai-empire.md` |
| Mondain's Legacy | `ML` | `Core.ML` | `dev-docs/eras/mondains-legacy.md` |
| Stygian Abyss | `SA` | `Core.SA` | `dev-docs/eras/stygian-abyss.md` |
| High Seas | `HS` | `Core.HS` | `dev-docs/eras/high-seas.md` |
| Time of Legends | `TOL` | `Core.TOL` | `dev-docs/eras/time-of-legends.md` |
| Endless Journey | `EJ` | `Core.EJ` | `dev-docs/eras/endless-journey.md` |

Also accept **EraProfile** names when the user scopes a shard profile:

- `Distribution/Configuration/EraProfiles/ml-baseline.json`
- `Distribution/Configuration/EraProfiles/endless-journey.json`

Accept aliases (`SE`, `Samurai Empire`, `samurai-empire`, `Core.SE`) and normalize to one display name in the report header.

## Source Hierarchy

Use sources in this order. Do not skip lower tiers when a higher tier has no answer.

1. **Repo-internal** — `dev-docs/eras/{expansion}.md`, `dev-docs/uo-reference-sources.md`, era tests, `MondainsLegacySourceReferences.cs`
2. **UO.com** — `https://uo.com/wiki/ultima-online-wiki/`
3. **UOGuide** — `https://www.uoguide.com/`
4. **UO Stratics** — `https://uo.stratics.com/` (secondary fallback only)
5. **Last resort** — UOAlive, RunUO, ServUO docs or source (label as `Unverified` and cite URL)

When sources conflict, record the conflict in **Issue** and lower the accuracy grade.

## Parity Status Legend

| State | Meaning |
|---|---|
| `Present` | Implemented and matches official sources for the target era |
| `Partial` | Implemented with known gaps (stats, skills, loot, spawns, hooks) |
| `Gap` | Documented in OSI sources but missing or not wired in repo |
| `Enhanced` | Intentional RebirthUO deviation beyond OSI |
| `SourceLocked` | Effect facts confirmed by approved sources; values in code |
| `RuntimeBlocked` | Facts confirmed; live trigger/cadence/hook not wired to combat |
| `Unverified` | Only found in RunUO/ServUO/UOAlive; not confirmed on UO.com/UOGuide |

`Enhanced` is not a failure — list separately from `Gap`/`Partial`.

## Mandatory Workflow

Run all steps on every activation:

1. **Validate era** — normalize display name, enum, `Core.*` check, era doc path, optional `EraProfile` JSON
2. **Load era context** — read `dev-docs/eras/{slug}.md`, `publish-index.md` publish range, profile gates in `EraProfiles/`
3. **Inventory repo by aspect** — scan paths from [aspects.md](aspects.md); grep/code search for era-relevant types
4. **Cross-check external sources** — UO.com first, then UOGuide; Stratics only when both lack detail
5. **Grade accuracy** — per-row `%` confidence (see [report-template.md](report-template.md))
6. **Emit mandatory report** — full aspect sections + summary tables + recommendations

### Efficiency Rules

- **Aspect summary rows** first (coverage % per aspect), then **entity-level rows** for notable `Partial`/`Gap`/`RuntimeBlocked` items
- Deep field-by-field parity only for user focus + direct dependencies
- Pre-seed from era doc tables and `Open gaps` sections before web search
- Cite a URL for every non-`Present` row
- Pair ML entities with `MondainsLegacySourceReferences` constants when available

## Mandatory Output

Copy the report structure from [report-template.md](report-template.md). Every activation must include:

1. **Era header** — display name, enum, `Core.*`, EraProfile, publish range
2. **Aspect coverage summary** — one row per aspect (47 aspects in [aspects.md](aspects.md))
3. **Entity/system detail table** — fine-grained rows with `Name | State | Era | Source | Issue | Accuracy % | Recommendation`
4. **Gap list** — missing content
5. **Partial / RuntimeBlocked list** — incomplete implementations
6. **Enhanced list** — intentional deviations
7. **Open research** — unresolved conflicts

## Deep Parity Checklist (per entity)

When auditing a specific entity (boss, item, skill, quest):

| Check | Repo | External |
|---|---|---|
| Type exists | C# class or data row under expected path | UOGuide page exists |
| Stats / properties | ctor defaults, `SetSkill`, `GetProperties` | UOGuide statistics table |
| Abilities / specials | `MonsterAbility`, spells, `OnGaveMeleeAttack`, TODOs | UO.com + UOGuide ability sections |
| Loot / rewards | `GenerateLoot`, artifact tables | UOGuide loot lists |
| Access / keys | `PeerlessAltar`, quest regions | Peerless/quest pages |
| Spawns | `Data/Spawns/`, spawner JSON | Dungeon/region pages |
| Era gating | `Core.*` branches, EraProfile JSON | Expansion publish notes |

Document `SourceLocked` vs `RuntimeBlocked` separately when mechanics are confirmed but not live-wired.

## Example Row

| Name | State | Era | Source | Issue | Accuracy % | Recommendation |
|---|---|---|---|---|---|---|
| Yomotsu_Elder | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Elder | Missing Axe Throw special; skills/stats may differ from UOGuide table | 65% | Wire axe-throw ability; reconcile `SetSkill`/`SetStr` ranges against UOGuide; add parity test in `Projects/UOContent.Tests/` |

Repo: `Projects/UOContent/Mobiles/Monsters/SE/YomotsuElder.cs` — `// TODO: Axe Throw` at line 88.

## Cross-Links

| Topic | Doc / skill |
|---|---|
| Era checks in code | `modernuo-era-expansion.md`, `dev-docs/era-expansion.md` |
| 9-domain taxonomy | `modernuo-content-taxonomy` |
| Reference URL map | `dev-docs/uo-reference-sources.md` |
| Aspect scan paths | [aspects.md](aspects.md) |
| Report template | [report-template.md](report-template.md) |
| ML source constants | `Projects/UOContent/Misc/MondainsLegacySourceReferences.cs` |
| Era doc maintenance | `dev-docs/eras/README.md` |

## Maintenance

When parity work changes implementation status:

1. Update `dev-docs/eras/{expansion}.md` anchor and parity table
2. Add code back-reference: `// Era: dev-docs/eras/{slug}.md#{entity-slug}`
3. Add or extend targeted tests under `Projects/UOContent.Tests/`

Do not store long URL prose in content classes — use era doc anchors or reference classes.
