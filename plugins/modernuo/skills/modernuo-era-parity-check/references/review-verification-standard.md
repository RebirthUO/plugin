# Review & verification standard (RebirthUO parity)

User expectation: **a review that ends on „Partial“, „unsicher“, or „Tests fehlen“ without
having run checks or written tests is incomplete work** — not an acceptable deliverable.

## When the user says prüfen / check / verify / audit

Do it **in the same turn** before writing the review row:

| Action | Tool |
|---|---|
| Code exists? | `search_files`, `read_file`, path anchors |
| Feature missing? | `grep` / `terminal` ripgrep — **0 treffer = Gap** |
| Behavior claimed? | `dotnet test` with a **focused filter** — cite pass count |
| OSI field value? | UO.com → UOGuide → Stratics; else **RuntimeBlocked** with tool error |

Do **not** defer with „sollte man prüfen“ or „Tests fehlen“ as the only finding.

## Allowed final statuses (era ledger & epic tables)

| Status | Meaning | Required evidence |
|---|---|---|
| **Present** | Implemented as claimed | Green test **or** `path:line` anchor |
| **Gap** | Expected system/type absent | Search = 0 hits (show command) |
| **OSI-Delta** | Code/tests OK; official value differs | URL/quote + field diff |
| **RuntimeBlocked** | Needs shard/live after attempt | Document failed tool/runtime step |

**Forbidden as terminal states** (without prior action in the same session):

- Generic **Partial** in summary tables
- **Unsicher** / „needs confirmation“
- **Tests fehlen** without adding/running tests or naming a hard blocker

Legacy parity reports may still use `Partial` in aspect scans **only** when immediately
followed by a delta row with Expected/Evidence/Delta/Validation — never alone.

## Tests are part of verification

- If the row depends on engine behavior and a test exists → **run it** and cite count.
- If no test exists but a sibling pattern exists (e.g. `ChiefParoxysmusTests`) →
  **create the test in the same PR/session** before claiming OSI-Delta on stats.
- Label results honestly: **focused filter passed** ≠ full suite green.

## ML epic quick verification (RebirthUO/service)

```bash
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --filter "FullyQualifiedName~MLQuest" --no-restore
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --filter "FullyQualifiedName~Spellweaving" --no-restore
grep -rni CooperativeCollection Projects --include="*.cs"   # expect empty for Gap
```

Monster test coverage gap script (ad-hoc): compare `Mobiles/Monsters/ML/**/*.cs` stems
to strings in `Tests/Mobiles/Monsters/ML/**/*.cs` — list types **without** test anchor
before opening `*-PARITY-MON-*` OSI issues.

## German epic / triage copy

Keep **Spielersicht** for **Gap** and **OSI-Delta** only — what the player expects vs
what evidence shows. Do not use Spielersicht for vague „maybe broken“.

## Ad-hoc doc verify

Run `scripts/hermes-verify-era-ledger-docs.py` (optionally copy to `%TEMP%` with
`hermes-verify-` prefix). Reports **documentation consistency + optional dotnet
filters** — not gameplay parity.