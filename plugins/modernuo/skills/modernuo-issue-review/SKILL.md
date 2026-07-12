---
name: modernuo-issue-review
description: Use when the user explicitly asks to research, triage, or update a GitHub issue only in https://github.com/RebirthUO/ModernUO. Validate that exact repository before every issue or pull-request read/write; reject all other repositories, forks, and lookalikes.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: review
    workflow_tier: direct-modernuo
---
# ModernUO Issue Review

## Mandatory Repository Gate (Overrides All Later Examples)

This explicit gate overrides every conflicting placeholder, mixed-repository statement, remote-derived target, or historical example later in this skill. Activation is explicit and the only permitted repository is `https://github.com/RebirthUO/ModernUO` (`RebirthUO/ModernUO`).

Before **any issue or pull-request read or write**, require an explicit repository URL or `owner/repository` from the current user request. An issue number alone is insufficient. Never infer the target from cwd, `origin`, another remote, organization membership, repository content, or conversation history. Resolve `gh api repos/RebirthUO/ModernUO` and require successful access plus exact `.full_name == "RebirthUO/ModernUO"` and `.html_url == "https://github.com/RebirthUO/ModernUO"`. The canonical repository currently reports `fork: true`; exact canonical identity is allowed, but every other fork or lookalike is rejected.

If repository context is missing, request it. If it differs or validation fails, stop before reading or mutating issues/PRs. Every `gh issue` and `gh pr` command must pass `-R RebirthUO/ModernUO`; never substitute another repository.


This skill reviews GitHub issues in `RebirthUO/ModernUO`, including issues about shared ModernUO-based RebirthUO code context, by researching official and community sources plus local repo anchors until open questions are answered or explicitly marked unresolved. It does not review or mutate issues in a separate RebirthUO repository, close issues, or remove triage based on guesswork; it edits the issue body and removes `triage` only when the issue is implementation-ready. It depends on Hermes tools plus an authenticated `gh` CLI; no extra packages are required.

## When to Use

- "Review this ModernUO issue" or "prüfe das Issue".
- "Research this issue and close open questions".
- "Remove triage if the issue is ready".
- An explicitly identified ModernUO issue has `triage`, `Unknown`, `Needs review`, or an `Open Questions` section.
- An explicitly identified ModernUO issue needs internet-backed UO era, publish, mechanics, item, mobile, spell, skill, spawn, loot, crafting, quest, event, or system research.

## Prerequisites

- Authenticated GitHub CLI; check through the `terminal` tool with `gh auth status`.
- The current user request names `https://github.com/RebirthUO/ModernUO` or `RebirthUO/ModernUO`, and the mandatory repository gate has verified it.
- Internet access for `web_search`, `browser_navigate`, `browser_snapshot`, or `browser_console` (see `references/uo-com-wiki-extract.md` when `web_extract` is unavailable).
- Local repository access when repo anchors or implementation scope are part of the review; use `search_files` and `read_file`.
- Permission to edit the issue body and labels. If body edit or label edit fails, report the blocker and leave `triage` unchanged.

## How to Run

Use `terminal` to fetch the issue with `gh`, verify canonical UO pages (`browser_navigate` + `references/uo-com-wiki-extract.md`), and confirm repo anchors with `search_files`, `read_file`, and `grep` in `terminal`. Stage the body under `.hermes/tmp/`, apply with `gh issue edit --body-file`, and remove `triage` only after the readiness gate passes. On Windows/MSYS, pass a native path to `--body-file` (see Pitfalls). When creating temporary helper scripts or staged bodies, prefer shell-created files in the actual worktree (`mkdir -p .hermes/tmp`, terminal redirection, or a native Windows path); do not pass MSYS `/c/...` paths to file-writing tools that resolve paths through Windows semantics, because they can create accidental `C:\c\...` scratch trees.

## Quick Reference

- Auth check: `gh auth status`
- Fetch issue: `gh issue view <number> -R RebirthUO/ModernUO --json title,body,labels,comments,url`
- Duplicate/context search: `gh issue list -R RebirthUO/ModernUO --state all --search "<keywords>"`
- Label list: `gh label list -R RebirthUO/ModernUO --json name --jq '.[].name'`
- Edit body: `gh issue edit <number> -R RebirthUO/ModernUO --body-file <body-file>` (Windows/MSYS: `BODY="$(cygpath -w "$(pwd)/.hermes/tmp/issue-N-body.md")"` then `--body-file "$BODY"`)
- Export body for edit: `mkdir -p .hermes/tmp && gh issue view <N> -R RebirthUO/ModernUO --json body --jq .body > .hermes/tmp/issue-N-body.md`
- Extended weapon container on `origin/main`: `git show origin/main:Projects/UOContent/Misc/AOS.cs | grep -n ExtendedWeapon`
- Related closed container issues: `gh issue list -R RebirthUO/ModernUO --state all --search "ExtendedWeapon" --json number,title,state`
- Remove triage: `gh issue edit <number> -R RebirthUO/ModernUO --remove-label "triage"`
- Success edit: `gh issue edit <number> -R RebirthUO/ModernUO --body-file <body-file> --remove-label "triage"`
- GitHub issue endpoint: `GET /repos/{owner}/{repo}/issues/{issue_number}`
- GitHub labels endpoint: `DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}`
- Official source root: `https://uo.com/wiki/ultima-online-wiki/`
- Official publish notes: `https://uo.com/wiki/ultima-online-wiki/publish-notes/`
- Historical cross-check: `https://www.uoguide.com/`
- UOGuide raw fallback when normal page loads or browser navigation time out: `https://www.uoguide.com/index.php?title=<Page_Name>&action=raw`; fetch with a normal User-Agent if needed, treat as community/reference evidence, quote/paraphrase the wikitext, and cite the public article URL (not the raw endpoint) in the issue.
- Community/reference sources: Stratics, UO forums, ServUO, RunUO, ModernUO/RebirthUO repo evidence.

## Procedure

1. **Capture the issue state.** Invoke through the `terminal` tool:

   ```bash
   gh issue view <number> -R RebirthUO/ModernUO --json title,body,labels,comments,url
   ```

   You are done when the title, body, comments, URL, current labels, and presence or absence of `triage` are known.

2. **Extract the open questions.** Read the issue body and comments for `Open Questions`, `Unknown`, `Needs review`, unchecked acceptance criteria, missing era/publish, unclear mechanics, missing side effects, or missing repo anchors. You are done when every open question has a short research target and a readiness criterion.

3. **Run internet research before deciding.** Use `web_search` for each target, then open canonical URLs with `browser_navigate`. If full-page text is needed (UO.com property tables, publish-note bullets), use `browser_console` per `references/uo-com-wiki-extract.md` — do not skip live verification because the issue body already cites URLs. Prefer UO.com/Broadsword and official publish notes for canonical behavior; use UOGuide as historical cross-check; use Stratics, ServUO, RunUO, ModernUO, and shard docs as community or engine precedent, not as canonical fact when official sources conflict. You are done when each answer has a source URL, source class, and a quoted or paraphrased finding, or is explicitly marked unresolved because no reliable source was found.

4. **Inspect current repo anchors, including merged implementation state.** Use `search_files` and `read_file` on cited paths; if symbol search returns empty unexpectedly, confirm with `grep -rn` in `terminal` on `Projects/` (on Windows/MSYS, `rg` may be absent—use `grep`). Determine the remote that actually matches the issue repo before using remote file anchors: inspect `git remote -v`, fetch the matching default branch, and prefer `git show <matching-remote>/main:<path>` over a blind `origin/main` assumption (in RebirthUO worktrees, `origin` may be a fork while `upstream` is `RebirthUO/ModernUO`). When the worktree branch lags the matching remote main, confirm enum/bit placement with that remote path so issue text does not repeat stale ServUO `AosWeaponAttribute` maps or wrong containers. **Before deciding that an issue is still implementation-ready work, search merged PRs and `origin/main` for the feature; if it is already merged, rewrite stale “not implemented” scope and acceptance wording to describe the shipped implementation, tests, and any follow-up instead of planning duplicate work.** For **item-property** tickets, load `uo-item-property-review` and any matching `references/*-review.md` before locking storage. Refresh stale claims (e.g. “no negative container” vs partial `NegativeAttributes` from a sibling issue). When searching names like `Massive`, exclude false positives (durability enums, display strings). You are done when implementation scope claims cite repo paths with current line anchors or are marked `No repo anchor confirmed`.

When validating a merged implementation, use an exact test-class filter rather than a substring that can match sibling classes (for example, `FocusPropertyTests` can also match `CastingFocusPropertyTests`). If a clean checkout is needed, use a native Windows path for `dotnet` and verify the checkout actually contains the target files before interpreting results. If all selected tests fail during shared fixture/bootstrap initialization before assertions, report that as a validation blocker and do not characterize it as a feature regression or test pass.

5. **Resolve what can be resolved.** For each question, write one of: `Resolved`, `Partially resolved`, `Conflicting sources`, or `Unresolved`. Include era/ruleset, publish, facet/map, PvP/PvM/economy/housing side effects, and implementation boundaries when relevant. You are done when no question is silently omitted.

6. **Revise the issue body, not a new comment.** Preserve the existing template headings and user text unless it is clearly superseded. Add or refresh compact sections such as:
   - `## Research Notes`
   - `## Source Links`
   - `## Resolved Questions`
   - `## Remaining Open Questions`
   - `## Implementation Notes / Repo Anchors`

   For issues that already contain long `## References` and `## Research Notes`, add a dated **review sweep** line under Research Notes after live re-check, move policy-only `## Open Questions` that include a defensible **Suggested default** into `## Resolved Questions` (evidence class: Custom policy / repo precedent), and set `## Remaining Open Questions` to “None blocking” when only follow-up tickets remain.

   Before editing GitHub, run a local residual-blocker scan on the staged body for stale phrases such as `Decision needed`, `Needs source confirmation`, `implementation review needed`, `Confirm whether`, `## Open Questions`, `decide whether`, and `decide and test`. If the triage gate is intended to pass, either rewrite each hit into an explicit implementation default/resolved question or intentionally leave it under `## Remaining Open Questions` and keep `triage`.

   You are done when the body contains the research summary, source links, remaining unknowns if any, and a clear implementation-ready state.

7. **Apply the triage gate.** Remove `triage` only when all blocking open questions are resolved, no source conflict blocks implementation, the acceptance criteria and test plan are clear enough for an implementer, and side effects are named. If an open question is only a missing default that official sources do not quantify, resolve it by explicitly choosing a conservative implementation default from engine precedent or repo policy, label the evidence class, and keep broader rollout as a non-blocking follow-up. If any blocking question remains or internet access failed, leave `triage` in place and explain the blocker in `Remaining Open Questions`.

8. **Edit GitHub.** Save the revised body with `write_file`, then invoke through the `terminal` tool:

   ```bash
   gh issue edit <number> -R RebirthUO/ModernUO --body-file <body-file>
   ```

   If the triage gate passed, combine or follow with:

   ```bash
   gh issue edit <number> -R RebirthUO/ModernUO --remove-label "triage"
   ```

   You are done when the command exits successfully and returns no label-edit error.

9. **Report the result.** Return the issue URL, whether `triage` was removed, the evidence classes used, and any remaining blockers. Do not claim a full implementation or test-suite result from issue review alone.

## Batch Triage-Sweep Pattern

When the request covers **all open `triage` issues**, treat it as a coordinated review sweep, but apply the readiness gate independently to every issue:

1. Inventory the queue once with issue number, title, body, labels, and URL. Record the exact count before edits; do not assume every result belongs to one mechanic family.
2. Group only independent research work in parallel. Build a per-issue evidence ledger containing canonical UO.com wording, UOGuide historical cross-check, era/publish conclusion, current canonical-branch repo anchors, and remaining source conflicts.
3. Inspect the matching repository default branch before trusting a working-tree observation. A local line may be commented, stale, or divergent while `origin/main` has the active implementation; describe the target branch in the issue and label local divergence as workspace context rather than repository fact.
4. Stage one complete body per issue under `.hermes/tmp/`. Preserve the issue template shape, but replace stale generic `Open Questions` with resolved implementation defaults or explicit blocking questions. A qualitative official mechanic may use a conservative, testable implementation default only when it is labeled `Repo precedent` or `Engine precedent / implementation policy`, never as canonical fact.
5. Run the residual-blocker scan **per staged body**. Remove `triage` only from issues with no blocking source/behavior decision; retain it on issues whose missing fact changes the player-visible contract (for example, active-effect ownership, authorization, numerical combat values, or concrete host definition).
6. Publish all body edits first, then remove labels only for the ready issue numbers. Read back every edited issue through `gh issue view`, verify the expected headings and label state, and finally list the remaining triage queue. Report both the ready set and the intentionally retained set with the exact blocker.
7. Clean up only review files created by this sweep. If `.hermes/tmp/` contains unrelated drafts, preserve them.

This pattern is a source-review workflow, not implementation validation: do not claim a build or test result unless code changed and those commands actually ran.

## Practical Review-Sweep Pattern

When an issue already contains a substantial draft, do not rewrite it from scratch. Export the live body, preserve the existing template and acceptance criteria, then make a narrow review sweep:

1. Re-check the canonical URLs live and record the current source class and exact finding. Use official UO.com for player-facing metadata and publish/facet rules; keep UOGuide and emulator code as corroboration or implementation precedent only.
2. Re-check the matching repository default branch, not merely the working tree. State explicitly whether the cited implementation is already merged, partial, or absent. For active-use item properties, inspect the callback path as well as storage: a generic enum/property can exist while a required facet/PvP restriction is still missing.
3. Convert policy questions into explicit first-slice defaults when the implementation boundary is otherwise clear. Label them as repo precedent/custom policy rather than presenting emulator constants as canonical. Keep historical introduction timing and broader parity as non-blocking follow-ups when they do not prevent implementation.
4. Replace stale `## Open Questions` content with `## Resolved Questions` and `## Remaining Open Questions`. Preserve unresolved facts honestly, but make `Remaining Open Questions` say `None blocking` only when the acceptance criteria, tests, side effects, and implementation defaults are concrete.
5. Before publishing, run a residual-blocker scan for `Decision needed`, `Needs source confirmation`, `implementation review needed`, `Confirm whether`, `## Open Questions`, `decide whether`, and `decide and test`. Then verify the edited body and labels through `gh issue view`; require a boolean success check showing research sections exist and `triage` is absent.

A useful distinction is **implementation verification required, non-blocking**: for example, a candidate client cliloc can remain a clearly marked implementation-time verification item while the item identity, behavior, scope, and test plan are already ready. Never call that candidate canonical until local client data confirms it.

## Pitfalls

- When staging a multiline GitHub body through `hermes_tools.terminal()` inside `execute_code`, verify the actual file before publishing: the helper output may include line-number prefixes on captured multiline text. Prefer native shell redirection where practical; otherwise strip only a verified leading `^[0-9]+|` prefix, re-read the complete staged file, and run the residual-blocker scan before `gh issue edit`.
- Do not close the GitHub issue; "close open questions" means answer them in the issue body.
- **Inspect full official source pages for repeated/revised mechanics.** A property table, a named publish subsection, and later bug-fix bullets on the same UO.com page can disagree. Capture each exact statement through page DOM/raw HTML rather than relying on a compact browser snapshot or the first matching row; cross-check the named UOGuide publish page. If the conflict changes a duration, formula, host, PvP/PvM rule, or other player-visible contract, preserve it in `## Remaining Open Questions` and retain `triage` unless a maintainer chooses the RebirthUO policy explicitly.
- Do not remove `triage` when sources are missing, contradictory, or only anecdotal.
- Do not leave `triage` only because a related follow-up or sibling issue exists; mark it as related/non-blocking when the reviewed issue has enough scope, acceptance criteria, sources, and repo anchors for its first implementation slice.
- Do not rely on memory for UO era or publish claims; check live internet sources. When a UO.com Magic Item Properties row lacks introduction timing, also search UO.com directly with an exact phrase URL such as `https://uo.com/?s=%22Last+Parry+Chance%22`; site search can surface publish-note pages that the table itself does not link or quote.
- When official spell sources give a qualitative acceptance rule but no exact formula/table (e.g. Enchant duration: selected-spell-level scaling with a 150-second base/cap), do not leave `triage` solely for the missing numeric table. Move the question to `## Resolved Questions` with an explicit implementation-policy default, require tests to document the chosen constants, and keep future exact-formula discovery as non-blocking follow-up. If a matching domain reference exists in `uo-magic-spells/references/`, load it before editing.
- Do not treat repo code as proof of official UO history; classify it as repo evidence or custom behavior.
- Do not replace the issue body without preserving template fields, existing acceptance criteria, and useful prior notes.
- Do not add comments as the default update path; edit the initial issue body unless permissions block it.
- Do not publish exploit reproduction details beyond what maintainers need to scope a safe fix.
- Do not call a focused source review a completed implementation, broad test pass, or PR-ready branch.
- If the repo uses a different triage label, confirm the exact label before removal; default to `triage` for ModernUO issue templates.
- On Windows/MSYS, `gh.exe` rejects MSYS paths for `--body-file`; stage under `.hermes/tmp/` and pass `cygpath -w` to `gh issue edit`.
- Do not treat an already-drafted issue as review-complete without re-reading the working tree: partial sibling work (e.g. `NegativeAttributes` + `Prized` only) changes repo-evidence wording.
- When an issue's only open questions are policy defaults that official sources do not quantify (advancement timing, transient state persistence, artifact-specific host handling), move them into `## Resolved Questions` with an explicit **implementation policy** decision and set `## Remaining Open Questions` to `None blocking`; avoid leaving a stale `## Open Questions` heading after triage is removed.
- When a spell/content issue has a source conflict where UO.com gives current player-facing values and UOGuide corroborates them, but ServUO/RunUO engine precedent differs, resolve the implementation default to UO.com and classify emulator code as lifecycle/hook precedent only. Do not leave `triage` merely for a compatibility choice unless the user explicitly asked for ServUO parity.
- When a current UO.com spell table conflicts with an explicit UO.com publish-note revamp and community/engine precedent (e.g. generic circle cast delay or recharge timing vs a named spell revamp), prefer the explicit revamp note for the first implementation slice if it gives safer PvP/economy behavior. Document the current-table conflict in `Research Notes`, choose a concrete implementation policy, and move it to `Resolved Questions` rather than leaving `Decision needed` under `Open Questions`. For chance-based cure/heal mechanics, inspect existing local spell formulas (Cure/Cleanse/Cleansing Winds) and propose a testable local formula instead of copying deterministic emulator behavior blindly.
- Do not copy ServUO `AosWeaponAttribute` bit values into RebirthUO anchors without checking `origin/main`. RebirthUO often stores post-AoS weapon properties in `ExtendedWeaponAttributes` (e.g. Bane, Battle Lust) while ServUO may use different containers.
- Do not leave repo bullets that place **Bane** (or other modern weapon props) in `AosWeaponAttributes` after the extended container landed (e.g. closed `ExtendedWeaponAttribute` container tickets). Re-anchor to `Projects/UOContent/Misc/AOS.cs` `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes` and `BaseWeapon.ExtendedWeaponAttributes` with current line numbers.
- For **Publish 96** weapon-property reviews, do not assume Publish-note prose and the Magic Item Properties table agree on exclusions: publish bullets often say “special moves” only, while the MIP row may name Lightning Strike, Death Strike, and Onslaught. Use MIP for acceptance-test wording when both exist; cite both source classes in Research Notes.
- For proc properties with an “independent” second branch plus a victim immunity, separate branch independence from immunity scope. Resolve independence from the canonical wording, then choose and document a broad/narrow immunity policy explicitly; do not let one pinned emulator revision silently decide the other.
- When a tooltip cliloc is only an engine candidate, verify it against the configured client data before locking it into acceptance criteria. ModernUO Classic client files may be BWT-compressed; use the repo's `Projects/Server/Client/BwtDecompress.cs` and `Projects/Server/Localization/Localization.cs` format rather than parsing the raw file as ordinary cliloc records. For an ad-hoc parser, create a disposable C# project under the OS temp directory, copy only `BwtDecompress.cs`, run exact-ID assertions, and remove the project afterwards. Do not stage parser source under the worktree: even deleted scratch `.cs` files can trigger repository verification guards. Record the exact verified string and keep optional buff/effect presentation separate from the OPL decision.
- `BuffIcon.Onslaught` in the repo is not proof that an Onslaught **move** exists locally. Call out debuff-only vs `SpecialMove`/`WeaponAbility` classes before requiring an Onslaught exclusion test.

## Support files

- `references/uo-com-wiki-extract.md` — extract exact UO.com wiki table rows and publish bullets via `browser_console`.
- `references/spellweaving-wildfire-review.md` — condensed Wildfire source findings, RebirthUO mana/formula implementation-policy defaults, and live repo anchors for future Spellweaving Wildfire issue reviews.
- Item-property tickets (Sparks, Swarm, Bane, etc.): also load `uo-item-property-review` and its `references/*-review.md` when present.

## Verification

For a successful review that removed triage, invoke through the `terminal` tool and require `true`:

```bash
gh issue view <number> -R RebirthUO/ModernUO --json body,labels --jq '(.body | contains("## Research Notes") or contains("## Source Links")) and ([.labels[].name] | index("triage") == null)'
```
