---
name: rebirthuo-request
description: Turn RebirthUO ideas into review-ready issues.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [RebirthUO, Triage, UltimaOnline, GitHub, Review]
---
# RebirthUO Request Intake

This skill turns a loose RebirthUO idea into an evidence-backed GitHub issue with the `needs-review` label. It does not implement the idea, skip source checks, or treat memory as proof. It uses Hermes tools plus the local RebirthUO repository, approved UO reference sites, and `gh`; no extra packages are required.

## When to Use

- "Ich habe eine Idee für RebirthUO ..."
- "Mach daraus ein Ticket" or "erst prüfen, dann Issue erstellen".
- A request mixes gameplay design, era parity, UO mechanics, and local code impact.
- The user asks for an interview before issue creation.
- A proposed feature needs `needs-review` before implementation.
- A claim may be backed by UO.com, UOGuide, UOAlive, ServUO, RunUO, or another verified UO server engine.

## Prerequisites

- Local repo: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- GitHub CLI authenticated; verify through the `terminal` tool with `gh auth status`.
- Repository target: always pass `-R RebirthUO/service` to `gh` commands.
- Existing label: `needs-review` (`Needs mechanics review before implementation`).
- Read repo instructions with `read_file`: `AGENTS.md` and `CLAUDE.md`.
- Use `web_extract` for web sources when available; use `browser_navigate` if `web_extract` is unavailable.
- Source set approved by the user: `https://uo.com`, `https://uoguide.com`, `https://uoalive.com/wiki/UOA`, ServUO, RunUO, and comparable verified server engines.

## How to Run

Start in the RebirthUO service repo. Use `read_file` for repository instructions, `search_files` for local implementation anchors, `web_extract` or `browser_navigate` for UO references, and `terminal` for `git`, `gh`, build/test, or duplicate issue checks. Interview in German unless the user asks otherwise, and create the GitHub issue only after the conceptual clarity gate passes.

## Quick Reference

- Repo root: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`
- Primary content project: `Projects/UOContent/`
- Core engine boundary: `Projects/Server/` requires explicit request before edits
- Build anchor: `dotnet build`
- Label check: `gh label list -R RebirthUO/service --search needs-review`
- Duplicate check: `gh issue list -R RebirthUO/service --state all --search "<keywords>"`
- Issue create: `gh issue create -R RebirthUO/service --title "<title>" --label "needs-review" --body-file "<body-file>"`
- Official source: `https://uo.com`
- Mechanics/history source: `https://uoguide.com`
- UOAlive source: `https://uoalive.com/wiki/UOA`
- ServUO source: `https://github.com/ServUO/ServUO`
- RunUO source: `https://github.com/runuo/runuo`
- Third-party shop/market pages (e.g. UOWTS): useful for observed item text/screenshots only; classify as `Community/reference` or market evidence until corroborated by UO.com, UOGuide, UOAlive, engine code, client data, or repo anchors.
- Shoulder Parrot example research: `references/shoulder-parrot-research.md` captures the source hierarchy, UO.com anchors, RebirthUO anchors, and issue-framing risks for a third-party item page intake.

## Procedure

1. **Load the repo contract.** Use `read_file` on `AGENTS.md` and `CLAUDE.md`; use the `terminal` tool for `git status --short --branch`, `gh auth status`, and `gh label list -R RebirthUO/service --search needs-review`. You are done when the active branch, repo cleanliness, GitHub auth, and label availability are known.

2. **Open a short interview.** Ask for missing facts in German, grouping questions instead of sending a long survey. Cover: Zielbild, Zielgruppe, era/expansion/ruleset, facet/map, official parity vs custom shard policy, expected values/formulas, affected player loops, and any sources or screenshots the user already has. You are done when the idea can be summarized in two sentences or fewer.

3. **Classify the request.** Decide whether it is a bug, parity gap, balance change, content addition, quality-of-life request, migration request, staff/tooling task, or custom policy decision. Name the affected loop: PvP, PvM, economy, crafting, housing/storage, travel/facets, skills/stats, loot, quests/events, client presentation, or staff operations. You are done when at least one likely affected loop and one likely side-effect loop are named.

4. **Gather source evidence.** For official or parity claims, inspect the relevant page with `web_extract` or `browser_navigate`; do not rely on a homepage if a mechanics subpage exists. Prefer UO.com for official wording, then UOGuide for mechanics/history, UOAlive for UOA-specific documented behavior, then ServUO/RunUO or another verified engine for implementation precedent. You are done when each claim is marked `Canonical`, `Community/reference`, `Engine precedent`, `Repo evidence`, `Custom policy`, or `Unresolved`.

5. **Inspect the local code.** Use `search_files` for feature nouns, class names, item IDs, cliloc IDs, config keys, era gates, and nearby tests; then use `read_file` on the smallest relevant file ranges. Trace registration and reachability, not just class existence: `Configure`, `Initialize`, data files, era checks, config, spawns, loot tables, regions, gumps, packets, and tests. You are done when the ticket can cite concrete repo anchors such as paths, classes, methods, data files, or test files.

6. **Check side effects.** Before issue creation, fill a short risk row: era/ruleset, facet/map, player loop, who benefits, who loses, gold/item faucet or sink impact, storage/housing impact, PvP counterplay, PvM risk/reward, bot/exploit risk, save/client compatibility, and rollback or monitoring need. You are done when the row is present or explicitly not applicable.

7. **Apply the conceptual clarity gate.** Create an issue only when these are present: concise summary, source status, at least one repo anchor, likely implementation surface, acceptance criteria, test plan, and risks/open questions. If the request lacks source status or repo anchors, continue the interview or research instead of creating a vague ticket. Open questions are allowed in the ticket only when they are explicit review questions, not hidden missing work.

8. **Draft the issue in German.** Use this structure:

```markdown
## Kurzfassung
<2-4 Sätze: Idee, Zielbild, warum review nötig ist.>

## Ziel
<Spieler-/Staff-/Shard-Ziel und erwartetes Verhalten.>

## Quellen
- <URL oder Engine-Quelle> — <welche Aussage sie stützt>
- <Unresolved/Custom policy, falls nicht belegt>

## Repo-Anker
- `<path>` — <Klasse/Methode/Datenpunkt und Ist-Zustand>

## Code-Change-Plan
1. <kleinster wahrscheinlicher Änderungsschritt>
2. <Tests/Daten/Registrierung>

## Erwartete Werte / Formeln / Testfälle
- <konkrete Werte oder bewusst offene Review-Frage>

## Akzeptanzkriterien
- [ ] <prüfbares Ergebnis>
- [ ] <Era-/Facet-/Config-Grenze>
- [ ] <keine unerwünschte Economy/PvP/PvM/Housing-Nebenwirkung>

## Testplan
- <focused test/search/build command or manual verification>

## Risiken / Nebenwirkungen
- <Economy, PvP, PvM, Housing, Exploit/Bot, Save/Client>

## Offene Fragen
- <nur echte Review-Fragen>
```

9. **Create the ticket.** Use `write_file` to save the body as `.hermes/tmp/rebirthuo-request.md`, then invoke through the `terminal` tool:

```bash
BODY_FILE=".hermes/tmp/rebirthuo-request.md"
BODY_ARG="$BODY_FILE"
if command -v cygpath >/dev/null 2>&1; then BODY_ARG="$(cygpath -w "$BODY_FILE")"; fi
gh issue create -R RebirthUO/service --title "<German title>" --label "needs-review" --body-file "$BODY_ARG"
```

10. **Report the result.** Return the issue URL, label, and one sentence on evidence quality. If no issue was created, state the exact missing clarity item and the next interview question.

## Pitfalls

- Do not create a ticket from a vibe. A RebirthUO request needs both source status and local code anchors.
- Do not treat UOGuide, UOAlive, ServUO, or RunUO as stronger than UO.com when sources conflict; show the conflict and ask which ruleset to target.
- Do not call behavior canonical when the source was unavailable; mark it `Unresolved` or `Custom policy`.
- Do not implement code during this intake unless the user explicitly changes the task from request creation to implementation.
- Do not edit `Projects/Server/` from an intake ticket; note engine impact and require explicit approval.
- Do not skip duplicate checks; similar open issues should be linked instead of duplicated.
- Do not expose exploit or dupe details in a public issue. Create a minimal safe ticket and preserve sensitive detail outside the public body.
- On Windows/MSYS, `gh.exe` can reject MSYS paths for `--body-file`; convert with `cygpath -w`.
- Broad websites are not enough. Fetch the relevant mechanics page or state that the exact source page is still needed.

## Verification

After creation, invoke through the `terminal` tool:

```bash
gh issue view <number> -R RebirthUO/service --json labels,body --jq '([.labels[].name] | index("needs-review")) != null and (.body | contains("## Kurzfassung") and contains("## Quellen") and contains("## Repo-Anker") and contains("## Akzeptanzkriterien"))'
```
