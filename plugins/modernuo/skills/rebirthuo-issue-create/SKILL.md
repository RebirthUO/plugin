---
name: rebirthuo-issue-create
description: Turn RebirthUO ideas into review-ready issues.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    skill_group: rebirthuo
    skill_subgroup: agentic
    workflow_phase: create
    workflow_tier: primary
---
# RebirthUO Request Intake

## Mandatory Repository Gate (Overrides All Later Examples)

This explicit gate overrides every conflicting placeholder, mixed-repository statement, remote-derived target, or historical example later in this skill. Activation is explicit and the only permitted repository is `https://github.com/RebirthUO/rebirthuo` (`RebirthUO/rebirthuo`).

Before **any issue or pull-request read or write**, require an explicit repository URL or `owner/repository` from the current user request. An issue number alone is insufficient. Never infer the target from cwd, `origin`, another remote, organization membership, repository content, or conversation history. Resolve `gh api repos/RebirthUO/rebirthuo` and require successful access plus exact `.full_name == "RebirthUO/rebirthuo"`, `.html_url == "https://github.com/RebirthUO/rebirthuo"`, and `.fork == false`. Reject `RebirthUO/ModernUO`, every other organization repository, fork, and lookalike.

If repository context is missing, request it. If resolution is inaccessible or mismatched, return exactly `BLOCKED: repository identifier requires correction` and stop before reading or mutating issues/PRs. Every `gh issue` and `gh pr` command must pass `-R RebirthUO/rebirthuo`; never substitute another repository.


This skill turns a loose RebirthUO idea into an evidence-backed GitHub issue with the `needs-review` label. It does not implement the idea, skip source checks, or treat memory as proof. It uses Hermes tools plus the local RebirthUO repository, approved UO reference sites, and `gh`; no extra packages are required.

## When to Use

- "Ich habe eine Idee für RebirthUO ..."
- "Mach daraus ein Ticket" or "erst prüfen, dann Issue erstellen".
- A request mixes gameplay design, era parity, UO mechanics, and local code impact.
- The user asks for an interview before issue creation.
- A proposed feature needs `needs-review` before implementation.
- A claim may be backed by UO.com, UOGuide, UOAlive, ServUO, RunUO, or another verified UO server engine.

## Prerequisites

- Local repo: prefer the active/current RebirthUO repo at `C:\Users\Jsiem\Documents\GitHub\RebirthUO\rebirthuo` (`RebirthUO/rebirthuo`). Older requests or source references may point to `RebirthUO/service--old`; use it as evidence when named, not as the ticket target unless the user explicitly says so.
- GitHub CLI authenticated; verify through the `terminal` tool with `gh auth status`.
- Repository target: resolve before creating anything. Prefer explicit `-R RebirthUO/rebirthuo` for current tickets. If a historical instruction says `RebirthUO/service`, verify it exists first; if GitHub cannot resolve it, do not fail the intake—use the current repo target and report the target correction.
- Preferred review label: `needs-review` (`Needs mechanics review before implementation`) when it exists. If the repository only has default labels, do not invent labels during issue intake unless the user asked for label maintenance; use an available fallback such as `enhancement` and report the label gap.
- Read repo instructions with `read_file`: `AGENTS.md` and `CLAUDE.md`.
- Use `web_extract` for web sources when available; use `browser_navigate` if `web_extract` is unavailable.
- Source set approved by the user: `https://uo.com`, `https://uoguide.com`, `https://uoalive.com/wiki/UOA`, ServUO, RunUO, and comparable verified server engines.

## How to Run

Start in the resolved current RebirthUO repo, normally `RebirthUO/rebirthuo`. Use `read_file` for repository instructions, `search_files` for local implementation anchors, `web_extract` or `browser_navigate` for UO references, and `terminal` for `git`, `gh`, build/test, or duplicate issue checks. If the user says to use matching issue templates, read `.github/ISSUE_TEMPLATE/*.yml`, select the single best class-level template, and mirror its field order/headings in the issue body. Interview in German unless the user asks otherwise, but prefer English issue bodies when repository templates or user profile expect English GitHub issues. Create the GitHub issue only after the conceptual clarity gate passes.

## Quick Reference

- Repo root: resolve from the active workspace; normally `C:\Users\Jsiem\Documents\GitHub\RebirthUO\rebirthuo`
- Current GitHub repo: `RebirthUO/rebirthuo`; legacy/source repo examples may use `RebirthUO/service--old`
- Primary content project: `Projects/UOContent/`
- Core engine boundary: `Projects/Server/` requires explicit request before edits
- Build anchor: `dotnet build`
- Template check: `search_files(pattern="*.yml", target="files", path=".github/ISSUE_TEMPLATE")` and read the selected template before drafting when the user asks to use matching templates
- Label check: `gh label list -R RebirthUO/rebirthuo --search needs-review`; if absent, inspect available labels with `gh label list -R RebirthUO/rebirthuo --limit 200` and use the closest existing fallback only after noting the gap
- Duplicate check: `gh issue list -R RebirthUO/rebirthuo --state all --search "<keywords>"`
- Issue create: `gh issue create -R RebirthUO/rebirthuo --title "<template title prefix>: <specific name>" --label "<actual-label>" --body-file "<body-file>"`
- Link a child issue as a real GitHub sub-issue after both issues exist:
  ```bash
  PARENT_ID="$(gh issue view <parent-number> -R RebirthUO/service --json id --jq .id)"
  gh api graphql \
    -f query='mutation($issueId:ID!,$subIssueUrl:String!,$replaceParent:Boolean){ addSubIssue(input:{issueId:$issueId, subIssueUrl:$subIssueUrl, replaceParent:$replaceParent}){ issue{number} subIssue{number title url} } }' \
    -f issueId="$PARENT_ID" \
    -f subIssueUrl="<child-issue-url>" \
    -F replaceParent=true
  ```
- Official source: `https://uo.com`
- Mechanics/history source: `https://uoguide.com`
- UOAlive source: `https://uoalive.com/wiki/UOA`
- ServUO source: `https://github.com/ServUO/ServUO`
- RunUO source: `https://github.com/runuo/runuo`
- Third-party shop/market pages (e.g. UOWTS): useful for observed item text/screenshots only; classify as `Community/reference` or market evidence until corroborated by UO.com, UOGuide, UOAlive, engine code, client data, or repo anchors.
- Shoulder Parrot example research: `references/shoulder-parrot-research.md` captures the source hierarchy, UO.com anchors, RebirthUO anchors, and issue-framing risks for a third-party item page intake.

## Procedure

1. **Load the repo contract.** Use `read_file` on `AGENTS.md` and `CLAUDE.md`; use the `terminal` tool for `git status --short --branch`, `gh auth status`, and `gh label list -R <resolved-owner/repo> --search needs-review`. Resolve the GitHub repo before continuing; current RebirthUO tickets normally target `RebirthUO/rebirthuo`, while `service--old` is evidence/source material unless explicitly chosen as the target. If `needs-review` or template-declared labels are absent, list available labels and choose an existing fallback (`enhancement` for feature/property/system requests is usually acceptable) rather than creating labels as part of intake unless the user explicitly requested label maintenance. You are done when the active branch, repo cleanliness, GitHub auth, target repository, template availability, and label availability/fallback are known.

2. **Open a short interview.** Ask for missing facts in German, grouping questions instead of sending a long survey. Cover: Zielbild, Zielgruppe, era/expansion/ruleset, facet/map, official parity vs custom shard policy, expected values/formulas, affected player loops, and any sources or screenshots the user already has. You are done when the idea can be summarized in two sentences or fewer.

3. **Classify the request.** Decide whether it is a bug, parity gap, balance change, content addition, quality-of-life request, migration request, staff/tooling task, or custom policy decision. Name the affected loop: PvP, PvM, economy, crafting, housing/storage, travel/facets, skills/stats, loot, quests/events, client presentation, or staff operations. You are done when at least one likely affected loop and one likely side-effect loop are named.

4. **Gather source evidence.** For official or parity claims, inspect the relevant page with `web_extract` or `browser_navigate`; do not rely on a homepage if a mechanics subpage exists. Prefer UO.com for official wording, then UOGuide for mechanics/history, UOAlive for UOA-specific documented behavior, then ServUO/RunUO or another verified engine for implementation precedent. You are done when each claim is marked `Canonical`, `Community/reference`, `Engine precedent`, `Repo evidence`, `Custom policy`, or `Unresolved`.

5. **Inspect the local code.** Use `search_files` for feature nouns, class names, item IDs, cliloc IDs, config keys, era gates, and nearby tests; then use `read_file` on the smallest relevant file ranges. Trace registration and reachability, not just class existence: `Configure`, `Initialize`, data files, era checks, config, spawns, loot tables, regions, gumps, packets, and tests. You are done when the ticket can cite concrete repo anchors such as paths, classes, methods, data files, or test files.

6. **Check side effects.** Before issue creation, fill a short risk row: era/ruleset, facet/map, player loop, who benefits, who loses, gold/item faucet or sink impact, storage/housing impact, PvP counterplay, PvM risk/reward, bot/exploit risk, save/client compatibility, and rollback or monitoring need. You are done when the row is present or explicitly not applicable.

7. **Apply the conceptual clarity gate.** Create an issue only when these are present: concise summary, source status, at least one repo anchor, likely implementation surface, acceptance criteria, test plan, and risks/open questions. If the request lacks source status or repo anchors, continue the interview or research instead of creating a vague ticket. Open questions are allowed in the ticket only when they are explicit review questions, not hidden missing work.

8. **Draft the issue.** If the user asks to use matching GitHub issue templates, read the selected `.github/ISSUE_TEMPLATE/*.yml` and mirror its fields as Markdown headings in order, then append reviewer sections such as `Acceptance Criteria`, `Test Plan`, `Risks / Side Effects`, and `Open Questions` when useful. Otherwise use this RebirthUO review structure in German. Prefer English for GitHub issue bodies when repository templates or user profile require English, even if the interview was German.

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

9. **Create the ticket.** Use `write_file` to save the body as `.hermes/tmp/rebirthuo-issue-create.md`, then invoke through the `terminal` tool. Substitute the resolved repository and actual label:

```bash
BODY_FILE=".hermes/tmp/rebirthuo-issue-create.md"
BODY_ARG="$BODY_FILE"
REPO="RebirthUO/rebirthuo"
LABEL="needs-review"
if ! gh label list -R "$REPO" --search "$LABEL" | grep -q "^$LABEL[[:space:]]"; then
  LABEL="enhancement"
fi
if command -v cygpath >/dev/null 2>&1; then BODY_ARG="$(cygpath -w "$BODY_FILE")"; fi
gh issue create -R "$REPO" --title "<template title prefix>: <specific name>" --label "$LABEL" --body-file "$BODY_ARG"
```

If the fallback label was used, mention the missing preferred/template labels in the final report instead of silently implying the normal review label was applied.

10. **Report the result.** Return the issue URL, label, and one sentence on evidence quality. If no issue was created, state the exact missing clarity item and the next interview question.

## Pitfalls

- Do not hard-code `RebirthUO/service` as the current target. Verify the repo exists; if it does not, use `RebirthUO/rebirthuo` for current tickets and treat `service--old` PRs/issues as historical evidence.
- When the user says to use suitable issue templates, do not fall back to the free-form German structure. Read the selected template, keep the template field order/headings, and only add review sections after the template fields.
- Do not create a ticket from a vibe. A RebirthUO request needs both source status and local code anchors.
- Do not treat UOGuide, UOAlive, ServUO, or RunUO as stronger than UO.com when sources conflict; show the conflict and ask which ruleset to target.
- Do not call behavior canonical when the source was unavailable; mark it `Unresolved` or `Custom policy`.
- Do not implement code during this intake unless the user explicitly changes the task from request creation to implementation.
- Do not edit `Projects/Server/` from an intake ticket; note engine impact and require explicit approval.
- Do not skip duplicate checks; similar open issues should be linked instead of duplicated.
- Do not expose exploit or dupe details in a public issue. Create a minimal safe ticket and preserve sensitive detail outside the public body.
- On Windows/MSYS, `gh.exe` can reject MSYS paths for `--body-file`; convert with `cygpath -w`. If `write_file` returned an absolute native `resolved_path`, prefer that exact path for `--body-file`, and run `gh issue create` with `workdir` set to the repo root. Do not rely on a relative `.hermes/tmp/...` path unless the terminal working directory has been explicitly set and verified.
- `gh --jq` uses gojq without shell-style jq arguments; avoid `--arg` in `gh issue view --jq` verification snippets. Inline fixed values safely or pipe JSON to `jq` if variable binding is needed.
- Broad websites are not enough. Fetch the relevant mechanics page or state that the exact source page is still needed.

## Issue Template Maintenance

Use this subsection when editing or creating `.github/ISSUE_TEMPLATE/*.yml` forms for RebirthUO request intake.

1. **Keep templates class-level and product-aware.** Template names/descriptions should state the request class (`New Item Property`, `New Mobile`) rather than a generic feature request. Include fields that force era/ruleset, publish, facet/map or found-on surface, player loop, mechanics, source URLs, and repo anchors where appropriate.
2. **Use GitHub issue-form schema shapes deliberately.** Multi-select choices should be `type: dropdown` with `attributes.multiple: true`; do not use checkbox-style scalar options when a list of selectable options is needed. Required fields use `validations.required: true`; optional evidence fields should say `required: false` explicitly when clarity matters.
3. **Reference field is mandatory design pattern for UO intake templates.** Add a `References` textarea near the top with UO.com, UOGuide, Stratics, ServUO/RunUO, screenshots, and related URLs. Ask for one reference per line and what the source proves.
4. **Class templates should capture the gameplay surfaces for that class.**
   - **Mobile/NPC**: mobile type, era/publish, facets/maps, spawn locations, player loops, stats/skills, AI/behavior, loot/economy, taming/control, NPC services/dialogue, client presentation, and implementation notes.
   - **Item**: item categories, era/publish, source/availability, player loops, item mechanics, equipment details, item properties/set bonuses, crafting/resources, loot/rewards/economy, client presentation, and implementation notes. Include broad categories such as equipment, armor, weapons, shields, jewelry, talismans, clothing, item sets, artifacts, veteran rewards, craftables, resources, plants/seeds, rares/collectibles, containers, consumables, reagents, ammunition, tools, books/scrolls, deeds, housing decorations, quest/event items, and unknown/other.
   - **Spell**: spell school/source, era/publish, spell type, target type, player loops, casting requirements/costs, PvM mechanics, PvP mechanics, formulas/values/duration, restrictions/region rules, spellbook/scroll/reagent flow, client presentation, and implementation notes. Include Magery, Necromancy, Chivalry, Bushido, Ninjitsu, Spellweaving, Mysticism, masteries, racial abilities, monster/NPC spells, quest/event spells, and custom/unknown.
   - **Skill**: request type, skill category, affected skills, era/publish, player loops, skill mechanics, skill gain/training, stats/caps/progression, formulas/test cases, items/tools/resources, restrictions, client presentation, and implementation notes. Include all canonical UO skills, expansion skills, Enticement as removed/legacy, and new/custom/unknown.
   - **Spawn**: spawn type, era/publish, facets/maps, region/location/coordinates, spawn entries, timing/density/range, player loops, mechanics/region rules, rewards/economy, safety/exploit/bot risk, data format/era profile, and implementation notes. Include static spawn packages, generic spawners, mobile/NPC spawns, dungeon/town/champion/boss/quest/event/resource/treasure/ambient spawns, migration/parity, and custom/unknown.
   - **Crafting**: request type, craft system/skill, era/publish, player loops, recipe/crafting details, resources/requirements, skill/success/exceptional formulas, output properties, recipe scroll/learning flow, BODs/rewards/vendors, economy impact, restrictions, client presentation, and implementation notes. Include craftables, recipe changes, resources/subresources, recipe scrolls, runic tools, BODs, tool/station/add-on requirements, craft gump/UI, skill formulas, vendor/reward/drop sources, harvesting links, parity/migration, and custom/unknown.
   - **Quest**: request type, quest system/area, era/publish, facets/maps, quest givers/locations, player loops, objectives/steps, rewards/access unlocks, prerequisites/repeatability/chain rules, dialogue/gumps/quest log, mechanics/rules/edge cases, related items/mobiles/spawns, economy impact, quest config/data, client presentation, and implementation notes. Include ML quests, classic escort, New Haven, Heartwood/Sanctuary/Bedlam/Blighted Grove/Citadel/Twisted Weald/Prism/Labyrinth/Paroxysmus/Tokuno areas, Spellweaving/Paladin/Necromancer, peerless access, event/seasonal, and custom/unknown.
   - **Event**: event type, event system/scope, era/publish, facets/maps, schedule/duration, locations/regions, player loops, event content/components, mechanics/rules, rewards/loot/economy, PvP/PvM/safety, participation/access rules, lifecycle/configuration, client presentation, monitoring/rollback, and implementation notes. Include seasonal/holiday, live/GM, scheduled recurring, daily/weekly/monthly, town invasion, dungeon/encounter, champion/spawn, boss/peerless, quest/narrative, PvP, crafting/resource, vendor/reward, decoration/static, anniversary/shard, maintenance/reset, parity/migration, and custom/unknown.
   - **Engine/System**: request type, system area, era/ruleset, implementation layer, affected gameplay/operator loops, current/expected behavior, configuration/gates, lifecycle/ownership, data/persistence/save compatibility, events/timers/threading, commands/gumps/admin tools, content integration, performance/scale risk, security/fairness/exploit risk, side effects, testing/monitoring/rollback, and implementation notes. Include core server, UOContent engines, RUOContent systems, configuration/JsonConfig, startup/lifecycle, world save/load, accounts/access, networking/packets, commands/targeting, gumps/UI, EventSink/generated events, timers/EventScheduler, serialization/persistence, regions/maps/facets, spawns/encounters, loot/rewards, quests, crafting/economy, housing/multis, vendors/services, skills/stats/races, combat/magic, items/mobiles, monitoring/logging, tests/tooling, and custom/unknown.
5. **Verify as ad-hoc form validation, not suite green.** For issue-template-only edits, create a temporary verifier under the OS temp directory with a `hermes-verify-` prefix, parse the YAML, assert the expected fields/options/labels, run it against the changed template, and delete the temp file. Summarize as focused ad-hoc verification. A full `dotnet build` is not the canonical signal for GitHub issue-form YAML shape. For complex Windows/MSYS verifier scripts, prefer `execute_code` to create/run/delete the temp verifier in one Python process, or otherwise pass native Windows paths consistently; avoid large shell-embedded Python snippets that mix here-docs, emoji, apostrophes, and MSYS path translation.

## Verification

After creation, invoke through the `terminal` tool. Use the actual label applied (`needs-review` or the documented fallback):

```bash
ISSUE=<number>
LABEL=<actual-label>
gh issue view "$ISSUE" -R RebirthUO/rebirthuo --json labels,body --jq "([.labels[].name] | index(\"$LABEL\")) != null and (.body | contains(\"## References\") and contains(\"## Implementation Notes / Repo Anchors\") and contains(\"## Acceptance Criteria\"))"
```

For German/free-form issues, adjust the section checks to the actual headings used, e.g. `## Quellen`, `## Repo-Anker`, and `## Akzeptanzkriterien`.
