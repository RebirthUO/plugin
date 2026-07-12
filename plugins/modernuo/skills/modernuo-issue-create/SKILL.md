---
name: modernuo-issue-create
description: Use when the user explicitly asks to draft or create a GitHub issue only in https://github.com/RebirthUO/ModernUO. Validate the exact repository before every issue or label read/write; reject all other repositories, forks, and lookalikes.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: create
    workflow_tier: direct-modernuo
---
# ModernUO Issue Authoring

## Mandatory Repository Gate (Overrides All Later Examples)

This explicit gate overrides every conflicting placeholder, mixed-repository statement, remote-derived target, or historical example later in this skill. Activation is explicit and the only permitted repository is `https://github.com/RebirthUO/ModernUO` (`RebirthUO/ModernUO`).

Before **any issue or pull-request read or write**, require an explicit repository URL or `owner/repository` from the current user request. An issue number alone is insufficient. Never infer the target from cwd, `origin`, another remote, organization membership, repository content, or conversation history. Resolve `gh api repos/RebirthUO/ModernUO` and require successful access plus exact `.full_name == "RebirthUO/ModernUO"` and `.html_url == "https://github.com/RebirthUO/ModernUO"`. The canonical repository currently reports `fork: true`; exact canonical identity is allowed, but every other fork or lookalike is rejected.

If repository context is missing, request it. If it differs or validation fails, stop before reading or mutating issues/PRs. Every `gh issue` and `gh pr` command must pass `-R RebirthUO/ModernUO`; never substitute another repository.


This skill turns an explicitly requested ModernUO issue, including work about shared ModernUO-based RebirthUO code context, into an English GitHub issue in `RebirthUO/ModernUO`. It does not create or update RebirthUO-repository issues, implement code, replace source research, or create vague tickets without era/ruleset and side-effect context. It uses Hermes tools, the local `.github/ISSUE_TEMPLATE/*.yml` files as source of truth, and `gh` only when an issue must be created; no extra packages are required.

## When to Use

- "Create a ModernUO issue" or "mach daraus ein Issue".
- "Use the issue template" or "nach den Templates aufbauen".
- The user asks in German but wants the GitHub issue in English.
- The user has already explicitly asked for an issue about UO item properties, items, mobiles, spells, skills, spawns, crafting, quests, events, or systems.
- A loose gameplay idea needs title, labels, acceptance criteria, test plan, and risks before implementation.

## Prerequisites

- A ModernUO repository with `.github/ISSUE_TEMPLATE/*.yml`.
- Use `search_files` and `read_file` to inspect the current template files every time; templates are the source of truth.
- GitHub CLI authenticated only if creating the issue; verify through the `terminal` tool with `gh auth status`.
- Know the target repository for `gh issue create`; use `-R RebirthUO/ModernUO` when not already in the intended GitHub repo.
- Use English for the issue title and body even if the intake conversation is German.

## How to Run

Use `search_files` to list `.github/ISSUE_TEMPLATE/*.yml`, then `read_file` the selected template and any sibling template that might fit the request. Use `web_extract` or `browser_navigate` for UO references, `search_files` and `read_file` for repo anchors, `write_file` for the issue body, and `terminal` for `git`, `gh`, builds, tests, or verification.

## Quick Reference

- List templates: `search_files(pattern="*.yml", target="files", path=".github/ISSUE_TEMPLATE")`
- Read a template: `read_file(path=".github/ISSUE_TEMPLATE/<template>.yml")`
- Check auth: `gh auth status`
- Create issue: `gh issue create -R RebirthUO/ModernUO --title "<title>" --label "ultima-online,triage,<class>" --body-file "<body-file>"`
- Verify issue: `gh issue view <number> -R RebirthUO/ModernUO --json title,labels,body --jq '<jq-check>'`
- Item property: `.github/ISSUE_TEMPLATE/item_property.yml` -> `Item Property: <property name>` -> `ultima-online`, `triage`, `item-property`
- Item: `.github/ISSUE_TEMPLATE/item.yml` -> `Item: <item name>` -> `ultima-online`, `triage`, `item`
- Mobile: `.github/ISSUE_TEMPLATE/mobile.yml` -> `Mobile: <mobile name>` -> `ultima-online`, `triage`, `mobile`
- Spell: `.github/ISSUE_TEMPLATE/spell.yml` -> `Spell: <spell name>` -> `ultima-online`, `triage`, `spell`
- Skill: `.github/ISSUE_TEMPLATE/skill.yml` -> `Skill: <skill name>` -> `ultima-online`, `triage`, `skill`
- Spawn: `.github/ISSUE_TEMPLATE/spawn.yml` -> `Spawn: <spawn name or location>` -> `ultima-online`, `triage`, `spawn`
- Crafting: `.github/ISSUE_TEMPLATE/crafting.yml` -> `Crafting: <recipe, resource, or system>` -> `ultima-online`, `triage`, `crafting`
- Quest: `.github/ISSUE_TEMPLATE/quest.yml` -> `Quest: <quest name>` -> `ultima-online`, `triage`, `quest`
- Event: `.github/ISSUE_TEMPLATE/event.yml` -> `Event: <event name>` -> `ultima-online`, `triage`, `event`
- System: `.github/ISSUE_TEMPLATE/system.yml` -> `System: <engine or system name>` -> `ultima-online`, `triage`, `system`

## Procedure

1. **Discover the current template set.** Use `search_files` for `.github/ISSUE_TEMPLATE/*.yml`, then `read_file` the likely template. You are done when you have the exact `title`, `labels`, required fields, and template-specific field labels.

2. **Choose one primary issue class.** Map the request to one template: `item_property`, `item`, `mobile`, `spell`, `skill`, `spawn`, `crafting`, `quest`, `event`, or `system`. If the request spans classes, choose the player-facing primary object and capture secondary objects under `Implementation Notes / Repo Anchors` or `Related Templates` rather than making a mixed template.

3. **Keep the issue English and template-shaped.** Use the template title prefix exactly, use the template labels, and mirror the template's field labels as Markdown headings when creating or editing the issue through `gh`. Preserve labels such as `Initial Era`, `Initial Publish`, `Player Loops`, `Client Presentation`, and `Implementation Notes / Repo Anchors` instead of inventing local wording. For existing ModernUO issues, apply review notes, solution updates, and corrections by editing the initial issue description in the relevant sections; do not add comments unless the user explicitly asks for a comment.

4. **Collect the minimum evidence.** Ask or research until the issue can state: name, description, references, era/ruleset, publish if known, affected facets/maps when relevant, player loops, mechanics, economy/PvP/PvM/housing side effects, implementation surface, acceptance criteria, test plan, and open review questions. You are done when missing facts are explicit `Unknown` or `Needs review`, not hidden blanks.

5. **Classify sources.** Use `web_extract` or `browser_navigate` for UO.com, UOGuide, Stratics, ServUO/RunUO, screenshots, logs, or other URLs named by the user. Mark evidence as `Canonical`, `Community/reference`, `Engine precedent`, `Repo evidence`, `Custom policy`, or `Unresolved` so reviewers can tell fact from assumption.

6. **Anchor the repo impact.** Use `search_files` and `read_file` to identify likely classes, data files, config keys, tests, registration points, or `Projects/Server` boundary risks. Do not claim a repo anchor you have not inspected.

7. **Draft with template field headings.** Use `write_file` to save the body, usually under `.hermes/tmp/<slug>.md`. For each template field, write `## <field label>` and the answer. Add these standard reviewer sections after the template fields when useful:
   - `## Acceptance Criteria`
   - `## Test Plan`
   - `## Risks / Side Effects`
   - `## Open Questions`

8. **Apply class-specific emphasis.**
   - `item_property`: PvM/PvP mechanics, intensity range, imbue weight, total cap, found-on surfaces, property type, AoS/SA/TOL gate concerns.
   - `item`: source/availability, item mechanics, equipment details, item properties or set bonuses, crafting/resources, loot/rewards/economy, presentation.
   - `mobile`: facets/maps, spawn locations, stats/skills, AI/behavior, loot/rewards, taming/control, NPC services/dialogue, presentation.
   - `spell`: school/source, spell type, target type, casting costs, PvM/PvP mechanics, formulas, restrictions, spellbook/scroll/reagent flow, presentation.
   - `skill`: request type, category, affected skills, mechanics, gain/training, stats/caps, formulas, items/tools/resources, restrictions.
   - `spawn`: region/location/coordinates, spawn entries, timing/density/range, mechanics/region rules, rewards/economy, safety/exploit/bot risk, data format.
   - `crafting`: craft system/skill, recipe details, resources, formulas, output properties, recipe scrolls, BODs/rewards/vendors, economy.
   - `quest`: quest system/area, givers/locations, objectives, rewards/access, prerequisites/repeatability, dialogue/gumps, quest config/data.
   - `event`: event type/system, schedule, locations, content/components, rules, rewards, PvP/PvM safety, lifecycle/configuration, monitoring/rollback.
   - `system`: request type, system area, implementation layer, affected loops, current/expected behavior, configuration, lifecycle, persistence, events/timers/threading, performance, security/fairness.

9. **Create only after duplicate and label checks.** Invoke through the `terminal` tool. If the template labels do not exist in a freshly templated repo, create the missing low-risk labels first (or report that label creation is blocked) so the issue actually matches the issue form metadata:

```bash
gh issue list -R RebirthUO/ModernUO --state all --search "<keywords>"
gh label list -R RebirthUO/ModernUO --json name --jq '.[].name'
# If missing, create the template labels before issue creation, e.g.:
gh label create "ultima-online" -R RebirthUO/ModernUO --color "5319e7" --description "Ultima Online gameplay/content/system issue"
gh label create "triage" -R RebirthUO/ModernUO --color "ededed" --description "Needs review and scoping"
gh label create "<class>" -R RebirthUO/ModernUO --color "1d76db" --description "ModernUO/RebirthUO <class> issue"
gh issue create -R RebirthUO/ModernUO --title "<template prefix>: <specific name>" --label "ultima-online,triage,<class>" --body-file "<body-file>"
```

10. **Report a compact result.** Return the issue URL, template class, labels, and one sentence on evidence quality. If you only drafted and did not create the issue, return the body path and the exact missing fact or approval needed.

## Pitfalls

- Do not translate German intake text into a German issue; the user's convention is English GitHub issues.
- Do not add GitHub comments for RebirthUO/ModernUO issue reviews, solution notes, implementation guidance, or corrections unless explicitly requested; edit the initial issue description instead and verify the issue-visible text remains English.
- Do not skip era/ruleset. ModernUO behavior depends on expansion gates and shard policy.
- Do not treat community pages as canonical when UO.com or implementation precedent conflicts; show the conflict.
- Do not hide side effects. Economy, PvP counterplay, PvM risk/reward, housing/storage, exploit/bot risk, and client presentation matter.
- Do not claim `Projects/Server` changes are safe just because the request is content-shaped; flag the boundary explicitly.
- Do not use stale template memory. Re-read `.github/ISSUE_TEMPLATE/*.yml` because labels and required fields can change.
- Do not call focused source checks or ad-hoc issue validation a full build or suite-green result.
- On Windows/MSYS, `gh.exe` can reject MSYS paths for `--body-file`; convert the body path to a native Windows path when needed.

## Verification

Invoke through the `terminal` tool after creation and require `true`:

```bash
gh issue view <number> -R RebirthUO/ModernUO --json title,labels,body --jq '([.labels[].name] | index("ultima-online") != null) and (.body | contains("## Description")) and (.body | contains("## Initial Era")) and (.body | contains("## Implementation Notes / Repo Anchors")) and (.body | contains("## Acceptance Criteria")) and (.body | contains("## Test Plan"))'
```
