---
name: modernuo-issue-template-gate
description: Use when an explicitly requested GitHub issue draft or update must conform to the current template only in https://github.com/RebirthUO/ModernUO. Validate that exact repository before every issue, label, or template read/write; reject all other repositories, forks, and lookalikes.
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
# ModernUO Issue Template Gate

## Mandatory Repository Gate (Overrides All Later Examples)

This explicit gate overrides every conflicting placeholder, mixed-repository statement, remote-derived target, or historical example later in this skill. Activation is explicit and the only permitted repository is `https://github.com/RebirthUO/ModernUO` (`RebirthUO/ModernUO`).

Before **any issue or pull-request read or write**, require an explicit repository URL or `owner/repository` from the current user request. An issue number alone is insufficient. Never infer the target from cwd, `origin`, another remote, organization membership, repository content, or conversation history. Resolve `gh api repos/RebirthUO/ModernUO` and require successful access plus exact `.full_name == "RebirthUO/ModernUO"` and `.html_url == "https://github.com/RebirthUO/ModernUO"`. The canonical repository currently reports `fork: true`; exact canonical identity is allowed, but every other fork or lookalike is rejected.

If repository context is missing, request it. If it differs or validation fails, stop before reading or mutating issues/PRs. Every `gh issue` and `gh pr` command must pass `-R RebirthUO/ModernUO`; never substitute another repository.


This skill forces every explicitly requested `RebirthUO/ModernUO` GitHub issue draft to use the current repository issue template instead of a free-form body. It does not create or update a RebirthUO-repository issue, implement the issue, skip missing template fields, or hide evidence conflicts. It depends on Hermes tools plus the GitHub CLI when repository templates or issue creation must be checked online; no helper script is required.

## When to Use

- The user says "create a ModernUO issue", "erstelle ein Issue", or "mach daraus ein GitHub Issue".
- The user explicitly asks for a ModernUO issue from loose notes, a gameplay idea, a bug report, or an item-property request.
- The user mentions GitHub templates, issue forms, labels, Definition of Done, acceptance criteria, or implementation plans.
- Required facts are missing and must be requested from the user or researched online before drafting.
- The intake is German or mixed-language but the issue must be documented in English.

## Prerequisites

- The current user request names `https://github.com/RebirthUO/ModernUO` or `RebirthUO/ModernUO`, and the mandatory repository gate has verified it.
- GitHub CLI available for online template lookup or issue creation; invoke it through the `terminal` tool.
- Authenticated GitHub CLI only when creating or editing issues: `gh auth status`.
- Local repository access if repo anchors are needed; use `search_files` and `read_file` before claiming code locations.
- Online sources available when the user does not provide enough facts; use `web_extract`, `browser_navigate`, or `terminal` with `gh api` as appropriate.
- All issue title/body content must be in English, even when the conversation or source notes are German.

## How to Run

Start with `search_files` for `.github/ISSUE_TEMPLATE/*.yml` in the target repo. If templates are not present locally or may be stale, invoke `gh api` through the `terminal` tool to read the repository templates from GitHub, then use `read_file` or the API output to copy the template's exact title prefix, labels, and field labels. Draft the issue with template headings, fill missing facts by asking the user or researching online, and only create the issue after duplicate, label, and body-shape checks pass.

## Quick Reference

- Local templates: `search_files(pattern="*.yml", target="files", path=".github/ISSUE_TEMPLATE")`
- Online template list: `gh api repos/RebirthUO/ModernUO/contents/.github/ISSUE_TEMPLATE?ref=main --jq '.[].name'`
- Online template body: `gh api repos/RebirthUO/ModernUO/contents/.github/ISSUE_TEMPLATE/<template>.yml?ref=main --jq .content`
- Existing issue body: `gh issue view <number> -R RebirthUO/ModernUO --json title,labels,body,url`
- Duplicate search: `gh issue list -R RebirthUO/ModernUO --state all --search "<keywords>"`
- Label check: `gh label list -R RebirthUO/ModernUO --json name --jq '.[].name'`
- Missing low-risk class label: if authenticated, adjacent UO class labels already exist, and the task is to create the issue, create the missing template class label before `gh issue create`; otherwise report the label blocker instead of creating an off-template issue.
- Create issue: `gh issue create -R RebirthUO/ModernUO --title "<template prefix>: <specific name>" --label "ultima-online,triage,<class>" --body-file "<body-file>"`
- Update existing issue body: `gh issue edit <number> -R RebirthUO/ModernUO --body-file "<body-file>"`
- Verify issue: `gh issue view <number> -R RebirthUO/ModernUO --json title,labels,body`
- `crafting.yml`: `Crafting: <recipe, resource, or system>`; labels `ultima-online`, `triage`, `crafting`.
- `event.yml`: `Event: <event name>`; labels `ultima-online`, `triage`, `event`.
- `item.yml`: `Item: <item name>`; labels `ultima-online`, `triage`, `item`.
- `item_property.yml`: `Item Property: <property name>`; labels `ultima-online`, `triage`, `item-property`.
- `mobile.yml`: `Mobile: <mobile name>`; labels `ultima-online`, `triage`, `mobile`.
- `quest.yml`: `Quest: <quest name>`; labels `ultima-online`, `triage`, `quest`.
- `skill.yml`: `Skill: <skill name>`; labels `ultima-online`, `triage`, `skill`.
- `spawn.yml`: `Spawn: <spawn name or location>`; labels `ultima-online`, `triage`, `spawn`.
- `spell.yml`: `Spell: <spell name>`; labels `ultima-online`, `triage`, `spell`.
- `system.yml`: `System: <engine or system name>`; labels `ultima-online`, `triage`, `system`.

## Procedure

1. **Validate the fixed repository and read the template source.** Complete the mandatory repository gate first, then use `search_files` for `.github/ISSUE_TEMPLATE/*.yml`. If no current local templates are found, invoke `gh api repos/RebirthUO/ModernUO/contents/.github/ISSUE_TEMPLATE?ref=main` through `terminal`. When the worktree has multiple remotes, never rely on unqualified `gh repo view` or bare issue commands; use only explicit `-R RebirthUO/ModernUO` commands after the gate. Do not select an issue target from the worktree, a remote, organization membership, or a user request for another repository. You are done when the active template files/ref and the verified fixed repository are recorded.

2. **Select exactly one primary template.** Map the request to `crafting`, `event`, `item`, `item_property`, `mobile`, `quest`, `skill`, `spawn`, `spell`, or `system`. If the request spans several templates, choose the player-facing primary object and record secondary surfaces under implementation notes or related work; do not blend multiple templates into an unreviewable hybrid.

3. **Extract the template contract.** Read the selected YAML template and capture its `title`, `labels`, and every `label:` field in order. Keep the template's wording exactly for headings such as `Initial Era`, `Initial Publish`, `Player Loops`, `Client Presentation`, and `Implementation Notes / Repo Anchors`. You are done when the draft skeleton mirrors the template field order.

4. **Build a missing-information ledger.** For each empty field, mark whether it is: user intent, shard policy, era/publish fact, mechanics data, source reference, repo anchor, side-effect analysis, or test evidence. Ask the user for custom intent or policy choices that cannot be inferred. Research public facts online when they are discoverable without deciding shard policy for the user.

5. **Investigate before asking when facts are public.** Use `web_extract` or `browser_navigate` for UO.com, UOGuide, Stratics, archived publish notes, ServUO/RunUO references, screenshots, or URLs named by the user. Use `references/online-research-tools.md` for UO.com table extraction, WordPress REST page discovery, UOGuide MediaWiki API fallbacks, and ServUO/RunUO raw snippets or GitHub contents API directory listings when normal browsing/search is incomplete. Use `search_files` and `read_file` for existing implementation anchors. For spell issues, also use `references/spell-issue-research.md`: check local spell registration placeholders, existing scroll/book assets, and ServUO/RunUO recursive trees because spell definitions may live under nested `SpellDefinitions/` paths rather than the top-level school folder. For SA Mysticism/Spell Trigger-style issues, `references/spell-trigger-issue-research.md` records the UO.com REST discovery pattern, UOGuide conflict, local anchors, and label-creation lesson from a completed issue. For SA Mysticism/Healing Stone issues, `references/mysticism-healing-stone-research.md` records canonical Publish 60/65 evidence, current UO.com vs UOGuide/ServUO conflicts, local ModernUO anchors, and suggested decision defaults. For SA Mysticism/Purge Magic issues, load `uo-magic-spells` and its `references/mysticism-purge-magic-research.md` support file for the immunity conflict, ward-removal mechanics, ServUO nested path, and local registration anchors. You are done when each researched claim has a source classification: `Canonical`, `Community/reference`, `Engine precedent`, `Repo evidence`, `Custom policy`, or `Unresolved`.

6. **Cross-check inconsistencies.** Compare user notes, online sources, and repo evidence. If sources disagree, do not collapse the conflict into one confident statement. Document the conflict in English with `Observed conflict`, `Likely interpretation`, and `Decision needed`, then ask the user only for the decision that cannot be resolved by evidence.

7. **Draft in English with template headings.** Use `write_file` to save the body, usually under `.hermes/tmp/<slug>.md`. Every template field becomes `## <field label>` and must contain either a sourced answer, `Unknown`, `Needs user decision`, or `Needs implementation review`; never leave blank placeholders.

8. **Add reviewer sections only after the template fields.** Add `## Acceptance Criteria`, `## Test Plan`, `## Risks / Side Effects`, and `## Open Questions` when useful. If the post-create verification expects `## Implementation Notes / Repo Anchors` but the selected issue form does not include that label (for example, some item-property forms), add that heading as a reviewer section before `## Acceptance Criteria` rather than creating and then failing verification. Keep all added sections English, behavior-focused, and tied to era/ruleset, PvP/PvM, economy, housing/storage, exploit/bot risk, client presentation, persistence, and rollback where relevant.

9. **Run an issue review and research sweep before asking the user.** Re-read the full draft as if you were the reviewer who must finalize it. For every `Unknown`, `Needs user decision`, `Needs implementation review`, risk, side effect, or open question, decide whether it is publicly researchable, repo-verifiable, or truly a shard policy/design decision. Research public facts through relevant sources before asking the user: official UO.com/publish notes where available, UO Stratics, UOAlive/wiki pages, UOGuide, ServUO/RunUO precedents, screenshots/client data references, and any URLs or source names supplied by the user. Use repo search/read tools for implementation anchors. You are done only when remaining open questions are minimized to decisions evidence cannot resolve.

10. **Finalize open thoughts explicitly.** Update the draft with the new evidence instead of leaving research notes outside the issue. Move resolved items out of `## Open Questions`; keep only unavoidable custom-policy or design choices. For each unresolved item, write `Decision needed`, `Why evidence cannot decide it`, and `Suggested default` when a conservative era-consistent default is defensible. For risks, add a mitigation or test hook where possible rather than leaving a generic warning.

    **Existing-issue update rule for ModernUO:** edit the initial issue description in the relevant sections. Do not add a GitHub comment for review notes, solution updates, implementation guidance, or corrections unless the user explicitly asks for a comment. Keep the entire issue-visible update in English, even if the user conversation, notes, or prior mistaken comment were German. If a mistaken/non-English comment was already added and it contains useful content, move the useful content into the issue body, delete the comment when authorized/appropriate, and verify the comment count/body language afterward.

11. **Validate labels and duplicates before creation.** Invoke `gh issue list` and `gh label list` through `terminal`. For spell issues, run both an exact spell-name search (for example `"Purge Magic"`) and a broader school/family search (for example `"Purge" OR "Mysticism"`); classify same-school sibling gaps as related work rather than duplicates when they cover a different spell. For item-property requests, search both the exact property name and nearby/confusable names, then classify whether each hit is actually the same mechanic. If a near-name hit is a different UO property (for example `Spell Focusing` vs `Casting Focus`), link it as related/separate work in the issue body rather than treating it as a duplicate. If required labels from the template are missing and they are low-risk template taxonomy labels (`ultima-online`, `triage`, or the selected class label such as `spell`), create them with conservative colors/descriptions before issue creation when authenticated; otherwise report the blocker or ask before creating non-template/custom labels. Do not create the issue if an existing issue already covers the same scope unless the user asks for a follow-up or split issue.

12. **Handle migration from an external or retiring repository explicitly.** When the intake authorizes reviewing all open and closed tickets in a separate repository but asks to create only missing ModernUO-core topics:
   - Inventory every source issue, including state, title, labels, and body; do not infer scope from open state alone.
   - Classify each candidate as exactly one of: `Already covered by a ModernUO issue`, `Already functionally implemented without a matching issue`, `ModernUO-core gap suitable for a new issue`, `Shard/custom-layer-only`, or `Overview/epic only`.
   - Before treating an absent target issue as a gap, search the current local implementation and focused tests for active storage, tooltip/client presentation, lifecycle hooks, and gameplay consumption. A serialized enum/property alone is not sufficient evidence of functionality; likewise, a missing title is not evidence that implementation is absent.
   - For every new destination issue, use independently valid canonical/community/repo evidence and local anchors. If the user requests source separation, do not cite, link, name, quote, or otherwise reference the retiring source repository, its issue numbers, parent epic, or project-specific policy. Re-express only mechanics corroborated by acceptable sources.
   - Re-run target duplicate searches immediately before creation, then verify every created issue through GitHub for template headings, labels, English body, and absence of prohibited source identifiers.
   - Report skipped topics with their factual category and local/target evidence; do not create placeholder tickets merely to preserve source inventory.

13. **Create or return the draft.** If approved and authenticated, invoke `gh issue create` through `terminal` with the template title prefix, exact labels, and `--body-file`. If approval, facts, or permissions are missing, return the draft path plus the exact unresolved questions instead of creating a vague issue.

14. **Verify the result.** After creation, view the issue through `terminal` and confirm the title prefix, labels, template headings, English body, source conflicts, acceptance criteria, and test plan survived GitHub formatting. If the body was staged under a repo-local scratch path such as `.hermes/tmp/`, delete the exact body file after successful creation, then remove scratch directories only if they are empty. Re-check `git status` so issue drafting does not leave untracked workspace noise, but do not delete unrelated scratch files from other issue drafts. Report the issue URL, template name, labels, evidence quality, and any remaining user decisions in one concise summary.

## Late/current item-property research note

For current or post-TOL item properties whose source page is a seasonal event, do not infer the era from the event year or from a nearby New Legacy page. Use the UO.com WordPress REST API to search the property/event name, fetch the relevant publish-note page, and distinguish production-shard deployment language from New Legacy-specific material. Record the numbered publish when the publish notes identify it, and map it to the repository's actual gate (for example, `Core.EJ`) rather than inventing a newer expansion flag. If the issue form lacks the repository's current era option, select or document `Unknown` with an explicit mismatch note instead of misclassifying the property.

For item-property mechanics, preserve official qualitative wording and source classifications. Do not derive an undocumented proc formula from separate properties shown on a named event item; keep damage, debuff, activation-state, PvP, and distribution questions visible in the issue.

## Pitfalls

- Do not draft a free-form issue because the template file is not local; check GitHub online before concluding no template exists.
- Keep repository identity fixed across every `gh` call. Ignore local remotes, memory, and `gh repo view` defaults; after the mandatory gate, pass `-R RebirthUO/ModernUO` explicitly for template, duplicate, label, create, edit, and verify commands.
- Do not write the GitHub issue body in German. Translate intake facts into English and preserve source names/quotes only when needed.
- Do not invent template fields, labels, title prefixes, source URLs, repo paths, or commands that were not inspected.
- Do not treat community pages as canonical when official UO publish notes or repo behavior disagree; surface the inconsistency.
- Do not stop at generic `Open Questions` when sources like UO.com, UO Stratics, UOAlive/wiki pages, UOGuide, ServUO/RunUO, repo code, or user-supplied URLs can resolve the point.
- Do not ask the user for facts that can be quickly researched online, but do ask for custom shard policy, priority, or design decisions.
- Do not hide `Unknown` values. A visible unknown is better than a fabricated mechanic, but avoidable unknowns should be researched before returning the draft.
- Do not omit era/ruleset, publish, facet/map, player loop, or side-effect analysis for UO gameplay issues.
- Do not force a property into a template dropdown when the current form lacks the correct host surface. Example: talisman-only item properties may not have `Talismans` under `Found on`; state the mismatch explicitly in the body instead of misclassifying it as Armor/Jewelry/Shields/Spellbooks/Weapons.
- Do not call a focused source check a full validation suite; label evidence quality honestly.
- On Windows/MSYS, convert `--body-file` paths to native Windows paths if `gh.exe` rejects an MSYS path.
- After deleting `.hermes/tmp` scratch files, `git status` may still show unrelated user/branch work. Do not clean, revert, or claim those files as issue-drafting artifacts; report only that scratch cleanup succeeded and separately note any remaining non-scratch dirty paths.

## Verification

Invoke through the `terminal` tool and require a true result after creation:

```bash
gh issue view <number> -R RebirthUO/ModernUO --json title,labels,body --jq '(.title | test("^(Crafting|Event|Item|Item Property|Mobile|Quest|Skill|Spawn|Spell|System): ")) and ([.labels[].name] | index("ultima-online") != null and index("triage") != null) and (.body | contains("## References")) and (.body | contains("## Initial")) and (.body | contains("## Implementation Notes / Repo Anchors")) and (.body | contains("## Acceptance Criteria")) and (.body | contains("## Test Plan"))'
```
