# SE-PARITY-MON triage pattern

Use this reference when processing RebirthUO `SE-PARITY-MON-*` batches that came from a player-facing monster parity audit.

## Durable lessons

- Treat issue-cited `dev-docs/parity/...` paths as issue-supplied context until verified on the target base. If `git ls-tree origin/live` does not show them, do not cite them as repo evidence or recreate them by default.
- UOGuide MediaWiki raw pages are efficient approved-source evidence for monster stats: `https://www.uoguide.com/index.php?title=<Title>&action=raw`.
- UOGuide titles may differ from class names (`RaiJu` -> `Rai-Ju`, `DeathWatchBeetle` -> `Deathwatch_Beetle`). Retry with hyphen/space/case variants before declaring an approved-source miss.
- Parse `{{Creatures ...}}` fields for `firstseen`, `str`, `dex`, `int`, `hitpoints`, `stamina`, `mana`, `basedamage`, `specialskill`, and resist/skill rows. Map `hitpoints` to `SetHits`, `basedamage` to `SetDamage`.
- Existing `*SourceFieldTests.cs`, `TokunoCreatureAbilityTests.cs`, and source-reference constants may already be the correct repo anchors. Search tests before inventing new test targets.
- A batch may legitimately contain multiple action classes:
  - `promote`: complete plan, `Review-Vollstaendigkeit: 100%`, `Confidence: 100%`, no blockers.
  - `comment-only`: useful blocker plan/comment, but keep `Triage required` when an approved-source conflict or missing formula remains.
  - `no-op/closure candidate`: no confirmed gameplay delta; can still move to Human Review if the comment clearly asks human review to close/accept no-op and the evidence gate is 100%.
- For Serado-like conflicts, do not turn a general UOGuide phrase (`Chain Lightning`) into implementation constants. If uo.com Publish notes prove a different sourced special (for example Publish 30 ranged poison cloud), preserve that source-locked implementation and leave lightning mechanics blocked until a maintainer decision or source supplies trigger/radius/damage/chance.

## Minimal automation shape

1. Export full issue JSON with bodies/comments/labels.
2. Build a class/title map for each monster and fetch UOGuide raw pages with retries.
3. Parse creature fields and compare them to constructor `Set*` calls on `origin/live`.
4. Search current tests for `*SourceFieldTests.cs`, ability tests, and source-reference constants.
5. Generate one #73-style comment file per issue and validate required sections plus `### Verifikations-Gate` before posting.
6. Post comments first, then label only `promote` rows, then verify every issue with `gh issue view`.
