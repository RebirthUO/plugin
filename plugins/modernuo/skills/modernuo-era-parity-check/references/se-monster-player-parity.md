# SE / Tokuno monster player-parity audit (bulk)

Session recipe for **spielerrelevante** parity over many creatures (Kampf, Specials, Loot, Spawn, Pets) — distinct from closed `SE-MISS-MON-*` **field-test** tickets.

## When to use

- User asks for monster parity **from a player perspective**, change lists per monster, and sliced GitHub issues.
- Era: `Core.SE` / Samurai Empire / Tokuno (pattern applies to other eras with a monster folder + spawn JSON).

## Source order (uo.com-first)

1. **uo.com** — Publish notes (e.g. Publish 30), dungeon pages (Yomotsu Mines, Fan Dancer Dojo), champion spawns. **Do not** invent `/monsters/{name}/` URLs; 404 pages are not official creature stats.
2. **UOGuide** — per-creature stats and tamable when uo.com is silent (`canonical-community`).
3. **Repo** — `*.cs`, `Distribution/Data/Spawns/**`, `*SourceFieldTests`, ability tests.

## Issue policy (RebirthUO)

| Rule | Detail |
|---|---|
| Prefix | `SE-PARITY-MON-{NNN}` for **gameplay** parity; do **not** reopen closed `SE-MISS-MON` |
| Link | `Related: #112` etc. in body; one GitHub comment on umbrella `#111` with report + manifest |
| Create gate | Issues only for `confirmed` / `source-conflict` at **P0/P1**; `RuntimeBlocked` / `SourceLocked` → report only |
| Bodies | **Deutsch**, high-information style (issue #73 / `modernuo-ticket-triage`) |
| Labels | Run `gh label list --repo RebirthUO/service` first; `parity` may **not** exist — use `Triage required` or project default |

## Repo layout (example)

```
dev-docs/parity/
  README.md
  se-monsters-uocom-sources.md
  se-monsters-repo-profile.json
  se-monsters-player-parity.json
  se-monsters-player-parity-report.md
  se-monsters-issue-manifest.tsv
  monsters/{slug}.md          # Spieler-Änderungsliste
  issues/SE-PARITY-MON-*.md   # bodies for gh issue create
  scripts/
    extract_se_monster_profile.py
    build_player_parity.py
```

Branch: `docs/se-monster-player-parity-audit` from `origin/live` (docs-only PR).

## Spawn JSON (ModernUO)

Tokuno spawns are a **JSON array of Spawner objects**, not flat `Type` rows:

```json
{
  "type": "Spawner",
  "entries": [
    { "name": "BakeKitsune", "maxCount": 8, "probability": 100 }
  ]
}
```

Aggregate spawn evidence with `entries[].name` and sum `maxCount` per creature short name.

## Bulk C# extraction

Regex over `Projects/UOContent/Mobiles/Monsters/SE/*.cs` plus mounts/specials:

- `SetStr` / `SetDex` / `SetHits` / `SetDamage` / `SetResistance` / `SetSkill`
- `MonsterAbilities.*`, `GetWeaponAbility`, hooks (`OnGaveMeleeAttack`, `DoCounter`)
- `TODO` lines → **P0 confirmed** gameplay gaps if player-visible

## UOGuide stat parse pitfalls

- **Damage:** plain-text strip may match damage **type** `100%` as `Damage 100 - 100`. Require `Damage (\d+) - (\d+)` with `max <= 80` or similar sanity cap.
- **±1 bounds** on Str/Dex/Int vs UOGuide are RunUO rounding noise — document as **P2** in report, **do not** file one issue per stat.
- Consolidate material stat drift into **one** `source-conflict` row per monster (`{Class}-stats-uoguide`) at P2 unless user promotes to decision ticket.

## Player rubric per monster sheet

Dimensions: Spawn, Schwierigkeit, Specials, Loot, Pets/Mounts, Quest/Champion, Immunitäten.

Status: `Present` | `Partial` | `Gap` | `SourceLocked` | `RuntimeBlocked` | `Enhanced`.

## Regenerate + verify

```bash
python dev-docs/parity/scripts/extract_se_monster_profile.py
python dev-docs/parity/scripts/build_player_parity.py
```

`build_player_parity.py` should **delete** stale `issues/SE-PARITY-MON-*.md` before writing new bodies (avoid 70+ orphan files after manifest filter).

**Ad-hoc verification** (not suite green): temp script `hermes-verify-*.py` checks script exit 0, 22 monsters, 22 sheets, manifest rows, 2 issue bodies after P0 filter.

## gh issue create

```bash
gh issue create --repo RebirthUO/service \
  --title "[SE-PARITY-MON-001] ..." \
  --label "Triage required" \
  --body-file dev-docs/parity/issues/SE-PARITY-MON-001.md
```

Record created issue numbers in the **master report**; optional `github_issue` column in manifest (regenerate overwrites generated TSV unless script preserves it).

## Known gameplay signals (SE)

- `// TODO: Hit Lightning Area` in `Serado.cs` → P0 special gap (poison area may already exist via `DoCounter`).
- `// TODO: Bone Pile` in `RevenantLion.cs` → P0 special gap.
- `YomotsuElder` + `MonsterAbilities.YomotsuAxeThrow` → **Present** if ability class wired and tests exist (do not assume gap from old triage).