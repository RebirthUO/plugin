# Era Parity Report Template

Copy this structure into **every** `modernuo-era-parity-check` response.

## Header

```markdown
# Era Parity Report: {Display Name}

| Field | Value |
|---|---|
| Expansion enum | `{Expansion}` |
| Core check | `Core.{XX}` |
| Era doc | `dev-docs/eras/{slug}.md` |
| EraProfile | `{profile name or "default"}` |
| Publish range | {from era doc or publish-index} |
| Report date | {today} |
```

## 1. Aspect Coverage Summary

One row per aspect from [aspects.md](aspects.md). Coverage % = share of era-relevant entities that are `Present` or `SourceLocked`.

```markdown
## Aspect Coverage Summary

| Aspect | Coverage % | State | Primary Source | Top Gap |
|---|---|---|---|---|
| Races | …% | Present / Partial / Gap | {URL} | … |
| Skills | …% | … | … | … |
| Stats | …% | … | … | … |
| Spells | …% | … | … | … |
| Item Properties | …% | … | … | … |
| Armor | …% | … | … | … |
| Weapons | …% | … | … | … |
| Shields | …% | … | … | … |
| Jewelry | …% | … | … | … |
| Talismans | …% | … | … | … |
| Clothing | …% | … | … | … |
| Item Sets | …% | … | … | … |
| Artifacts | …% | … | … | … |
| Veteran Rewards | …% | … | … | … |
| Craftables | …% | … | … | … |
| Resources | …% | … | … | … |
| Plants & Seeds | …% | … | … | … |
| Rares | …% | … | … | … |
| Facets | …% | … | … | … |
| Cities & Towns | …% | … | … | … |
| Dungeons | …% | … | … | … |
| Animals | …% | … | … | … |
| Monsters | …% | … | … | … |
| Champion Spawns | …% | … | … | … |
| Doom Gauntlet | …% | … | … | … |
| Peerless | …% | … | … | … |
| PvP | …% | … | … | … |
| Criminal | …% | … | … | … |
| Murderer | …% | … | … | … |
| Vice vs Virtue | …% | … | … | … |
| Damage Calculations | …% | … | … | … |
| Special Moves | …% | … | … | … |
| Templates | …% | … | … | … |
| Crafting | …% | … | … | … |
| Trading | …% | … | … | … |
| Pets | …% | … | … | … |
| Houses & Boats | …% | … | … | … |
| Quests | …% | … | … | … |
| NPCs | …% | … | … | … |
| Virtues | …% | … | … | … |
| Cooperative Collections | …% | … | … | … |
| Formulas and Game Mechanics | …% | … | … | … |

**Overall era parity:** {weighted average %} — {one-sentence verdict}
```

## 2. Entity / System Detail Table

Fine-grained rows for every `Partial`, `Gap`, `RuntimeBlocked`, `Enhanced`, and user-requested focus items. Include `Present` rows only when the user asked for a full catalog of a subset.

```markdown
## Entity / System Detail

| Name | State | Era | Source | Issue | Accuracy % | Recommendation |
|---|---|---|---|---|---|---|
| Yomotsu_Elder | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Elder | Missing Axe Throw special; skills/stats may differ from UOGuide | 65% | Wire axe-throw; reconcile stats/skills; add parity test |
| {Entity} | {State} | {Era} | {URL} | {what is wrong or missing} | {0–100}% | {actionable next step} |
```

### Column Rules

| Column | Rule |
|---|---|
| **Name** | UOGuide-style slug (`Yomotsu_Elder`) or C# type name (`YomotsuElder`) — be consistent within the report |
| **State** | `Present`, `Partial`, `Gap`, `Enhanced`, `SourceLocked`, `RuntimeBlocked`, `Unverified` |
| **Era** | Display name of the expansion that introduced or owns the content |
| **Source** | Best confirming URL (UO.com preferred; UOGuide for creature tables) |
| **Issue** | Concrete delta: missing skills, wrong stats, unwired spawn, TODO in code, source conflict |
| **Accuracy %** | Confidence that repo matches OSI for this entity (see grading in aspects.md) |
| **Recommendation** | Single actionable fix: implement, wire hook, add test, update era doc, research further |

Add a **Repo path** footnote or sub-column when helpful: `` `Projects/UOContent/...` ``.

## 3. Gap List

```markdown
## Fehlend (Gap)

- [{Aspect}] {Name} — {why missing} — Quelle: {URL} — Repo: {expected path or "none"}
```

## 4. Partial / RuntimeBlocked List

```markdown
## Unvollständig (Partial / SourceLocked / RuntimeBlocked)

- [{Aspect}] {Name} — {what is incomplete} — Quelle: {URL} — Repo: `{path}` — Accuracy: {N}%
```

## 5. Enhanced List

```markdown
## Enhanced (RebirthUO ≠ OSI)

- [{Aspect}] {Name} — {deviation} — reason: {if known}
```

## 6. Open Research

```markdown
## Offene Punkte / Recherche

- {conflict or unknown} — checked: {sources tried} — next step: {WebSearch query or in-game test}
```

## 7. Focus (when user named a subset)

```markdown
## Fokus dieser Anfrage

- Scope: {user focus}
- Immediate actions: {top 3 recommendations by impact}
- Suggested tests: `Projects/UOContent.Tests/...`
```

## Example: Samurai Empire Monsters (excerpt)

```markdown
| Name | State | Era | Source | Issue | Accuracy % | Recommendation |
|---|---|---|---|---|---|---|
| Yomotsu_Elder | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Elder | `// TODO: Axe Throw`; paralyze laugh may differ from OSI cadence | 65% | Implement axe throw; verify paralyze proc rate |
| Yomotsu_Priest | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Priest | Verify spell list and summon behavior | 70% | Cross-check magery skills vs UOGuide |
| Yomotsu_Warrior | Present | Samurai Empire | https://www.uoguide.com/Yomotsu_Warrior | Spawns wired in YomutsoMines.json | 85% | Add targeted parity test |
| Fan_Dancer | Partial | Samurai Empire | https://www.uoguide.com/Fan_Dancer | Fan Dancer's Dojo stealables/loot context | 75% | Verify `FanDancersDojo.json` density |
| Serado | Present | Samurai Empire | https://www.uoguide.com/Sleeping_Dragon | Champion-style SE boss | 80% | Confirm spawn controller wiring |
```
