# ML / expansion epic workflow (RebirthUO/service)

Session-derived workflow for **Mondain's Legacy** parity epics. Generalize era
name, paths, and issue prefixes for SE, SA, etc.

## Repo anchor

- Primary checkout: `Documents/GitHub/RebirthUO/service` (not `workspace/service`).
- Era docs: `dev-docs/eras/<era-slug>.md` (e.g. `mondains-legacy.md`). There is
  no `service/docs/` tree — use `dev-docs/` and `publish-era-mapping.md`.
- GitHub issues target repo: `RebirthUO/service`.

## ML structural inventory (quick)

| Area | Path / signal |
|---|---|
| ML flag / regions | `Projects/UOContent/Misc/MondainsLegacy.cs` |
| Source URLs | `MondainsLegacySourceReferences.cs` |
| Peerless drops | `Misc/MLPeerlessArtifacts.cs`, `Engines/Peerless/*Altar.cs` |
| Quest cfg | `Distribution/Data/MLQuests.cfg` |
| Quest defs | `Engines/ML Quests/Definitions/*.cs` |
| Monsters | `Mobiles/Monsters/ML/**/*.cs` |
| Spellweaving | `Spells/Initializer.cs` (IDs 600–615), `Spells/Spellweaving/` |
| Elf race | `Misc/RaceDefinitions.cs` (`Expansion.ML`) |
| Spawns | `Distribution/Data/Spawns/shared/**/{Bedlam,Labyrinth,...}.json` |

## Counting rules (pitfalls)

**MLQuests.cfg bindings:** Count **non-empty lines that do not start with `#`**.
On current `service` this is **285**, not a partial sum of section headers only.

```bash
grep -v '^#' Distribution/Data/MLQuests.cfg | grep -v '^[[:space:]]*$' | wc -l
```

**ML monster types (manifest):** All `.cs` stems under `Mobiles/Monsters/ML/`,
excluding helper types like `MLSetArmorDrops`. Expect **83** creature types;
map each row to `ML-PARITY-MON-NNN`.

**Cooperative Collections gap:** `grep -rl CooperativeCollection Projects/UOContent`
should be empty on a Gap — no `Engines/Collections` module. Child issue:
`ML-MISS-COLL-001`.

## Deliverables

2. **Era ledger** — `dev-docs/eras/mondains-legacy.md`: **Review-Standard** section,
   evidence-based coverage snapshot, engines, quest sections, peerless table, backlog IDs,
   monster list **without test anchor** (write tests before OSI-Delta issues).
3. **Epic markdown** — workspace or `.hermes/plans/`: Kurzfassung, aspect table,
   **Spielersicht** only for **Gap** / **OSI-Delta**, inventar counts, annex (cfg sections,
   SW list, minor arti pool). No unverified % structural guesses.
3. **Monster manifest TSV** — columns:
   `index`, `monster`, `repo_glob`, `status`, `player_audit`, `child_issue`.
   Status: **Present** (test anchor), **OSI-Delta**, or slice ID — not default Partial.
4. **GitHub Epic** — title `[ML-EPIC-000] …`, label `Triage required`; body must
   match cfg count (**285**) after local edits.

## Spielersicht (German issue style)

For RebirthUO triage, epic and slice issues often use German sections:
**Kurzfassung**, **Ziel**, **Quellen**, **Repo-Anker**, **Spielersicht** (was
der Spieler erwartet vs. fehlt), **Acceptance**, **Risiken**. Keep gameplay
claims sourced (UO.com > UOGuide > Stratics).

## Child-issue prefixes

| Prefix | Use |
|---|---|
| `ML-MISS-*` | Whole system missing (e.g. Collections) |
| `ML-PARITY-MON-###` | One creature player parity |
| `ML-PARITY-PEER-00N` | One peerless boss/altar |
| `ML-PARITY-SW-###` | Spellweaving unlock or single spell |
| `ML-PARITY-QUEST-###` | Quest group / world wiring |
| `ML-PARITY-ENG-###` | Engine/runtime (paragon, quest NPCs) |

## Ad-hoc verification

See [review-verification-standard.md](review-verification-standard.md).

Run `scripts/hermes-verify-era-ledger-docs.py` from the skill directory (copy
to `%TEMP%` with `hermes-verify-` prefix if required). With `RUN_DOTNET=1`, also
checks Spellweaving (**53**) and MLQuest (**202**) focused test counts. **Not**
full suite green.

## Blocked follow-ups (UO.com)

When `web_extract` / Firecrawl is unconfigured, add a **Blocked follow-ups** table
(blocker + next action). Do not leave epic/ledger rows as generic Partial.