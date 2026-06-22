# Era Parity Report Template

Copy this structure into every `modernuo-era-parity-check` response.

Reports must stay readable: use compact aspect rows first, then deep deltas only
for risk rows. Risk rows are every non-`Present`, low-confidence, monster,
crafting, and user-focused row.

## Header

```markdown
# Era Parity Report: {Display Name}

| Field | Value |
|---|---|
| Expansion enum | `{Expansion}` |
| Core check | `Core.{XX}` or `{pre-core condition}` |
| Era doc | `dev-docs/eras/{slug}.md` |
| EraProfile | `{profile name or "default"}` |
| Publish range | {from era doc or publish-index} |
| Report date | {today} |
```

## 1. Aspect Coverage Summary

One row per aspect from [aspects.md](aspects.md). Coverage % is the share of
era-relevant entities that are `Present` or `SourceLocked`.

```markdown
## Aspect Coverage Summary

| Aspect | Coverage % | State | Primary Source | Top Delta |
|---|---:|---|---|---|
| Races | {N}% | {Present/Partial/Gap} | {URL or repo doc} | {top concrete delta or "none"} |
| Skills | {N}% | {state} | {source} | {delta} |
| Stats | {N}% | {state} | {source} | {delta} |
| Spells | {N}% | {state} | {source} | {delta} |
| Item Properties | {N}% | {state} | {source} | {delta} |
| Armor | {N}% | {state} | {source} | {delta} |
| Weapons | {N}% | {state} | {source} | {delta} |
| Shields | {N}% | {state} | {source} | {delta} |
| Jewelry | {N}% | {state} | {source} | {delta} |
| Talismans | {N}% | {state} | {source} | {delta} |
| Clothing | {N}% | {state} | {source} | {delta} |
| Item Sets | {N}% | {state} | {source} | {delta} |
| Artifacts | {N}% | {state} | {source} | {delta} |
| Veteran Rewards | {N}% | {state} | {source} | {delta} |
| Craftables | {N}% | {state} | {source} | {delta} |
| Resources | {N}% | {state} | {source} | {delta} |
| Plants & Seeds | {N}% | {state} | {source} | {delta} |
| Rares | {N}% | {state} | {source} | {delta} |
| Facets | {N}% | {state} | {source} | {delta} |
| Cities & Towns | {N}% | {state} | {source} | {delta} |
| Dungeons | {N}% | {state} | {source} | {delta} |
| Animals | {N}% | {state} | {source} | {delta} |
| Monsters | {N}% | {state} | {source} | {delta} |
| Champion Spawns | {N}% | {state} | {source} | {delta} |
| Doom Gauntlet | {N}% | {state} | {source} | {delta} |
| Peerless | {N}% | {state} | {source} | {delta} |
| PvP | {N}% | {state} | {source} | {delta} |
| Criminal | {N}% | {state} | {source} | {delta} |
| Murderer | {N}% | {state} | {source} | {delta} |
| Vice vs Virtue | {N}% | {state} | {source} | {delta} |
| Damage Calculations | {N}% | {state} | {source} | {delta} |
| Special Moves | {N}% | {state} | {source} | {delta} |
| Templates | {N}% | {state} | {source} | {delta} |
| Crafting | {N}% | {state} | {source} | {delta} |
| Trading | {N}% | {state} | {source} | {delta} |
| Pets | {N}% | {state} | {source} | {delta} |
| Houses & Boats | {N}% | {state} | {source} | {delta} |
| Quests | {N}% | {state} | {source} | {delta} |
| NPCs | {N}% | {state} | {source} | {delta} |
| Virtues | {N}% | {state} | {source} | {delta} |
| Cooperative Collections | {N}% | {state} | {source} | {delta} |
| Formulas and Game Mechanics | {N}% | {state} | {source} | {delta} |

**Overall era parity:** {weighted average %} - {one-sentence verdict}
```

## 2. Entity / System Detail

Fine-grained rows are required for every `Partial`, `Gap`, `RuntimeBlocked`,
`Enhanced`, `Unverified`, low-confidence, monster, crafting, and user-focused
item. Include `Present` rows only when the user asks for a full catalog of a
subset.

```markdown
## Entity / System Detail

| Name | State | Era | Source | Expected | ModernUO Evidence | Delta | Validation | Impact | Accuracy % | Recommendation |
|---|---|---|---|---|---|---|---|---|---:|---|
| Yomotsu_Elder | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Elder | UOGuide creature table plus documented Axe Throw special | `Projects/UOContent/Mobiles/Monsters/SE/YomotsuElder.cs:{line}` has stats/skills and TODO for Axe Throw | Ability missing; stat/skill values differ only if exact ranges do not overlap | Confirmed code delta | PvM balance / era parity | 65% | Implement or intentionally defer Axe Throw; add a parity test |
| {Entity} | {State} | {Era} | {URL} | {cited target behavior} | `{path}:{line}` or search/data/test evidence | {concrete mismatch or "no delta found"} | {confirmed/source-conflict/repo-only/needs-runtime/open-research} | {risk category} | {0-100}% | {single actionable next step} |
```

### Column Rules

| Column | Rule |
|---|---|
| Name | UOGuide-style slug or C# type name; be consistent within the report |
| State | `Present`, `Partial`, `Gap`, `Enhanced`, `SourceLocked`, `RuntimeBlocked`, or `Unverified` |
| Source | Best confirming URL or repo source; cite every non-`Present` row |
| Expected | Cited target behavior, including ranges when available |
| ModernUO Evidence | File path and line, data path, test evidence, or search evidence |
| Delta | Concrete expected-vs-actual mismatch, missing field, or `no delta found` |
| Validation | `confirmed`, `source-conflict`, `repo-only`, `needs-runtime`, or `open-research` |
| Impact | Save compatibility, client behavior, performance, economy, security, era parity, PvM, PvP, crafting economy, or operator workflow |
| Accuracy % | Confidence that ModernUO matches the era target after source and repo checks |
| Recommendation | One decision-ready next step; do not include patches unless requested |

## 3. Delta Matrix

Required for risk rows. Group by aspect when there are more than five rows.

```markdown
## Delta Matrix

| Aspect | Name | Field | Expected | ModernUO Evidence | Delta | Validation |
|---|---|---|---|---|---|---|
| Monsters | Yomotsu_Elder | Ability | Axe Throw special documented by source | `YomotsuElder.cs:{line}` TODO / no ability hook | Missing ability hook | confirmed |
| Crafting | {Recipe} | Skill requirement | {cited requirement} | `{Def*.cs}:{line}` registers {value} | {numeric or behavioral difference} | {status} |
```

If a row cannot be filled, move it to `Open Research` instead of leaving the
delta as "verify", "confirm", or "unknown".

## 4. Gap List

```markdown
## Gap

- [{Aspect}] {Name} - Expected: {cited target} - ModernUO: {missing path/search evidence} - Delta: {missing content} - Source: {URL}
```

## 5. Partial / RuntimeBlocked List

```markdown
## Partial / SourceLocked / RuntimeBlocked

- [{Aspect}] {Name} - Delta: {what is incomplete} - Evidence: `{path}:{line}` - Source: {URL} - Validation: {status} - Accuracy: {N}%
```

## 6. Enhanced List

```markdown
## Enhanced (RebirthUO != OSI)

- [{Aspect}] {Name} - Expected: {OSI behavior} - ModernUO: {current behavior} - Delta: {intentional deviation} - Reason: {if known}
```

## 7. Open Research

```markdown
## Open Research

- {Stable ID}: {question} - Checked: {sources and repo paths tried} - Missing evidence: {specific field} - Next step: {exact web, code, test, or runtime validation}
```

`Needs confirmation` belongs here unless the report has enough source and repo
evidence to produce a concrete delta.

## 8. Focus

Use this section when the user named a subset.

```markdown
## Focus

- Scope: {user focus}
- Immediate actions: {top 3 recommendations by impact}
- Suggested tests: `Projects/UOContent.Tests/...`
```

## 9. Issue Slice Options

```markdown
## Issue Slice Options

This report can be converted into single sliced Markdown issues on request. Each issue must cover one independently actionable gap, partial implementation, runtime blocker, enhanced-deviation decision, or unresolved research decision. Preserve the source row, expected behavior, ModernUO evidence, delta, validation status, impact, acceptance criteria, suggested validation, and open questions.
```
