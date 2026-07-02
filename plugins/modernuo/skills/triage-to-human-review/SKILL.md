---
name: triage-to-human-review
description: Use when moving RebirthUO/ModernUO GitHub issues from `Triage required` to human review. Enforces the issue #73 high-information implementation-plan comment standard, source/repo evidence checks, no premature `Human Review` label, and verified GitHub label/comment transitions.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [github, triage, modernuo, rebirthuo, issues, human-review]
    related_skills: [rebirthuo-online-triage-verification, github-issues, modernuo-ticket-triage, uo-modernuo-workflow, uo-domain-research, modernuo-era-parity-check, modernuo-code-audit]
---

# Triage To Human Review

## Overview

Use this skill to convert RebirthUO/ModernUO GitHub issues from raw `Triage required` tickets into `Human Review` tickets that already contain an implementation-grade handoff comment. The standard is the high-information comment style established on RebirthUO/service issue #73: German by default, concrete, source-backed, repo-anchored, and detailed enough that an implementer should not have to guess the files, formulas, tests, risks, or acceptance criteria.

This skill is a workflow gate. `Human Review` is not a generic "looked at it" label. It means the issue has a complete, evidence-backed `## Konkretisierter Implementierungsplan` comment and is ready for a human maintainer to approve, reject, split, or hand to an implementer.

## When to Use

- User asks to review, triage, prepare, or promote RebirthUO/ModernUO GitHub issues to human review.
- User asks for "all triage tickets" to receive implementation plans.
- User asks to enforce the issue #73 style for future triage tickets.
- User asks to fix label state between `Triage required` and `Human Review`.

Don't use for:

- Implementing the issue. This skill stops at a review-ready plan/comment and labels.
- PR code review. Use `github-code-review` / `modernuo-code-audit` for PRs.
- Creating new feature tickets from scratch unless the user explicitly asks for issue creation.

## Required Companion Skills

Load these before doing substantive work:

1. `rebirthuo-online-triage-verification` for the approved-source online evidence gate and the strict 100% review / 100% confidence requirement before `Human Review`.
2. `github-issues` for `gh issue` commands and label/comment operations.
3. `modernuo-ticket-triage` for source-backed ticket triage, confidence labels, era/publish mapping, and high-information comment standard.
4. `uo-modernuo-workflow` for RebirthUO/ModernUO repository conventions.
5. Domain-specific skills when the issue area is clear, such as combat, crafting, housing, loot, quests, skills, spells, regions, networking, serialization, timers, or era parity.

Completion criterion: every generated comment can name the companion skills/evidence path that justified it, and every promotion decision has an explicit online verification gate result.

## Label State Contract

| Label state | Meaning | Allowed action |
|---|---|---|
| `Triage required` | Issue still needs the high-information plan or needs the existing plan reviewed/upgraded. | Read, research, draft, post full plan. |
| `Human Review` | A full plan comment exists and is ready for human maintainer review. | Only set after posting/verifying the full plan. |
| Both labels | Transitional or inconsistent. | Verify whether a full plan exists; then keep only the correct label. |
| Neither label | Out-of-band issue. | Ask or infer from user scope before touching labels. |

Hard rule: **never set `Human Review` without a complete plan comment on the same issue**. If a user asks to reset the queue, it is valid to set every open issue back to `Triage required` and remove `Human Review`.

## Default Repository And Branch Assumptions

Default target is `RebirthUO/service` unless the user names a different repo.

Before batch work, capture:

```bash
gh issue list --repo RebirthUO/service --state open --limit 300 --json number,title,labels,updatedAt,url,comments
git status --short --branch
git remote -v
git rev-parse --abbrev-ref HEAD
```

If the current checkout is dirty or behind the target branch, do not base code/repo evidence on uncommitted local files. Prefer `origin/live` evidence via `git show origin/live:path`, a clean worktree, or GitHub API reads. Report the dirty/behind state in the comment only when it affects implementation advice.

Completion criterion: the final summary includes the issue count, label counts, and whether any local checkout caveat was found.

## Per-Issue Workflow

### 1. Intake the issue

Read the full issue, labels, existing comments, and linked context:

```bash
gh issue view <N> --repo RebirthUO/service --json number,title,url,state,labels,assignees,author,createdAt,updatedAt,body,comments
```

Capture:

- Issue title and stable ID, such as `SE-MISS-BUSH-001`.
- Body claims, acceptance criteria, ledger/doc paths, source URLs, screenshots, reproduction steps.
- Existing comments, especially whether a `## Konkretisierter Implementierungsplan` already exists.
- Current labels.

Completion criterion: you can state whether the issue is a test gap, code gap, source formula gap, runtime proof, doc/ledger gap, data gap, or not-planned candidate.

### 2. Choose evidence surfaces

Search the repo and sources before drafting. Use issue keywords and normalized UO names.

Typical repo surfaces:

- `Projects/UOContent/` for gameplay/content implementation.
- `Projects/UOContent.Tests/` for regression tests.
- `Projects/Server/` only for engine-level ownership; do not recommend modifying it unless necessary and explicitly justified.
- `Distribution/Data/` and `Distribution/Configuration/` for spawns, maps, era profiles, decorations, assemblies, config.
- `docs/` and `dev-docs/` for matrices, source references, plans, standards, and ledgers.

Useful read-only commands:

```bash
git grep -n "<IssueKeyword>\|<UOName>\|<ModernUOType>" origin/live -- Projects Distribution docs dev-docs || true
git ls-tree -r --name-only origin/live | grep -Ei '<keyword>|<domain>|<ledger>'
```

Completion criterion: every repo claim in the comment has either a file:line, exact search result, or an explicit `open-research` note.

### 3. Gather source evidence

Use official/canonical sources before implementation advice:

- official: UO.com wiki and publish notes.
- canonical-community: UOGuide and legacy Stratics.
- repo: current source/docs/tests/data.
- issue-supplied: issue body/comments.
- secondary/unverified: emulator code, forums, private shard wikis — breadcrumbs only.

If a source mentions publish number, expansion, era, or profile, run the `modernuo-ticket-triage` publish/era measurement rule before recommending a global change.

Completion criterion: the `### Quellen` section lists each source with the exact mechanic/data it proves, not just raw links.

### 4. Draft the #73-style comment

Default language for RebirthUO triage comments is German. Use this structure unless the user requests English:

```markdown
## Konkretisierter Implementierungsplan

### Kurzfassung
<Precise classification and one-paragraph implementation thesis.>

### Ziel
<Concrete bullets for done state.>

### Quellen
- <Source>: <exact claim it supports>

### Relevante Repo-Anker
- `<path>`
  - <what this file/class/method owns>

### Code-Change-Plan
1. <Minimal step with exact file/helper/test target.>
2. <Next minimal step.>
3. <Smallest correction if tests reveal a delta.>
4. <Doc/ledger/label follow-up if applicable.>

### Erwartete Testwerte / Formelhinweise
- <Constants, formulas, expected values, data rows, helper shapes, commands.>

### Akzeptanzkriterien
- <Observable/source-backed conditions.>

### Testplan
```powershell
<focused command>
```

Optional breiter:

```powershell
<broader command>
```

### Risiken / Hinweise fuer den Implementierer
- <Hot path, save compatibility, era gate, PvP/PvM/economy, dirty checkout, missing ledger caveat.>
```

Quality bar:

- Name exact files and likely helper/test names.
- Include formulas and percent-vs-decimal conversions for formula tickets.
- Call out explicit non-goals like `Kein breiter Combat-Refactor` or `Keine Era-Policy-Aenderung ohne separates Ticket`.
- If the issue cites a ledger/doc path that is missing on the target branch, make the doc update conditional; do not invent the file.
- Avoid generic "implement and test" phrasing. Replace it with concrete code/test surfaces.

Completion criterion: an implementer can start the issue without asking "where?", "which source?", "what values?", or "how do I verify?".

## Posting And Label Transition

Posting comments and changing labels are external side effects. Do them only when the user explicitly asked for posting/labeling, not merely drafting.

Safe promotion sequence for one issue:

```bash
cat > /tmp/triage-<N>.md <<'EOF'
<full comment>
EOF

gh issue comment <N> --repo RebirthUO/service --body-file /tmp/triage-<N>.md
gh issue edit <N> --repo RebirthUO/service --add-label "Human Review" --remove-label "Triage required"
gh issue view <N> --repo RebirthUO/service --json labels,comments --jq '{labels:[.labels[].name], lastComment:.comments[-1].body[0:80]}'
```

If the user requests queue reset instead of promotion:

```bash
gh issue edit <N> --repo RebirthUO/service --add-label "Triage required" --remove-label "Human Review"
```

Completion criterion: after every mutation, verify labels with `gh issue view` or a batch `gh issue list` query. Report exact counts.

## Batch Workflow

For many issues:

1. Inventory all open issues and label state.
2. Group issues by domain/prefix (`BUSH`, `NINJ`, `CRAFT`, `MON`, `TOT`, `WORLD`, etc.).
3. Process in small batches, preferably 5-10 issues, so source/repo evidence stays fresh.
4. Use `todo` for batch state.
5. Draft all comments for a batch before posting if the user asked to review drafts first.
6. When posting is authorized, post + label each issue atomically: comment first, label second, verify third.
7. Stop and report if a source/repo blocker appears rather than posting weak comments.

Completion criterion: no issue is moved to `Human Review` unless its verified latest/full comment meets the standard.

## Large Queue Automation Pattern

When the queue is large (roughly 20+ `Triage required` issues), use a resumable manifest-based workflow instead of manually posting issue-by-issue. This reduces duplicate comments and makes final verification auditable.

1. Export the full queue once with bodies, comments, labels, and URLs:

```bash
gh issue list --repo RebirthUO/service --state open --label "Triage required" --limit 300 \
  --json number,title,url,body,comments,labels,updatedAt > /tmp/triage-required.json
```

2. Build a manifest with one row per issue:
   - `comment+label` when no complete `## Konkretisierter Implementierungsplan` exists.
   - `label-only` when a complete current plan already exists; do not post a duplicate.
   - `blocked` only when the generated plan would be weak or evidence is missing.

3. Generate comment files before posting. Validate every file contains the required sections (`Kurzfassung`, `Ziel`, `Quellen`, `Relevante Repo-Anker`, `Code-Change-Plan`, `Erwartete Testwerte / Formelhinweise`, `Akzeptanzkriterien`, `Testplan`, `Risiken / Hinweise`).

4. Post with a resumable state file. For each manifest row, do **comment first**, then label transition, and persist progress after each successful side effect. This allows safe reruns after a network/API interruption.

5. If an existing complete plan is present but the issue still has `Triage required`, perform the label transition only:

```bash
gh issue edit <N> --repo RebirthUO/service --add-label "Human Review" --remove-label "Triage required"
```

6. Final verification must query GitHub, not local state:

```bash
gh issue list --repo RebirthUO/service --state open --label "Triage required" --limit 300 --json number,title,labels

gh issue list --repo RebirthUO/service --state open --label "Human Review" --limit 300 --json number,title,labels,comments
```

Check that every expected issue has `Human Review`, no expected issue still has `Triage required`, and every promoted issue has at least one comment containing `## Konkretisierter Implementierungsplan`.

For `SE-PARITY-MON-*` monster parity batches, use `references/se-parity-mon-triage-pattern.md`: verify issue-cited parity docs exist on `origin/live`, fetch UOGuide MediaWiki raw pages for approved stat evidence, reuse existing `*SourceFieldTests.cs`/ability test anchors, and distinguish `promote`, `comment-only`, and no-op/closure-candidate rows before posting.

Pitfall: GitHub list queries can briefly miss an issue if labels were just edited or if the issue has other labels such as `Hermes Ready`; verify any apparent miss with `gh issue view <N>` before assuming the transition failed.

## Human Review Readiness Checklist

Before setting `Human Review`, confirm:

- [ ] `rebirthuo-online-triage-verification` gate passes with approved online sources only (`uo.com`, `uoguide.com`, `uo.stratics.com`).
- [ ] `Review completeness: 100%` and `Confidence: 100%` are explicitly recorded; otherwise the issue remains `Triage required`.
- [ ] Comment starts with `## Konkretisierter Implementierungsplan` or a user-approved equivalent.
- [ ] `Kurzfassung` classifies the issue type and smallest implementation slice.
- [ ] `Ziel` defines done state with concrete bullets.
- [ ] `Quellen` includes source tiers and exact claims.
- [ ] `Relevante Repo-Anker` names exact paths/classes/methods/tests/docs.
- [ ] `Code-Change-Plan` is numbered and minimal.
- [ ] `Erwartete Testwerte / Formelhinweise` contains constants, formulas, expected data, or explains why none apply.
- [ ] `Akzeptanzkriterien` are source-backed and observable.
- [ ] `Testplan` has focused commands and broader regression/build guidance where relevant.
- [ ] `Risiken / Hinweise` names era/profile, hot-path, save/client, economy, PvP/PvM, dirty-checkout, and missing-doc risks when applicable.
- [ ] No unsupported factual claims or remembered-only sources.
- [ ] No final "needs confirmation"; unresolved items are `open-research`, `needs-runtime`, or `source-conflict` with next step.

## Common Pitfalls

1. **Setting `Human Review` as a triage marker.** It is a readiness label, not a progress label. Post/verify the full comment first.

2. **Posting a thin summary.** A comment that says "add tests and update docs" fails the standard. Name tests, files, formulas, and commands.

3. **Citing stale issue paths as repo facts.** If `dev-docs/eras/foo.md` is in the issue but absent on `origin/live`, say it is absent and make updates conditional.

4. **Trusting local dirty files.** Dirty or behind checkout means use `origin/live`, a clean worktree, or GitHub API for evidence.

5. **Bundling unrelated deltas.** If the issue reveals separate mechanics, recommend follow-up issue slices instead of hiding them inside one plan.

6. **Over-writing implementation policy.** Do not propose broad era policy, combat refactors, economy changes, or `Projects/Server/` edits unless evidence shows they are necessary.

7. **Duplicate comments.** If a complete current comment already exists, do not append another unless updating it is requested or the existing one fails the standard. Prefer mentioning that the issue already meets Human Review criteria.

8. **No verification after mutation.** Always query labels/comments after posting or editing labels.

## Verification Checklist

- [ ] Required companion skills loaded.
- [ ] Issue inventory captured with label counts.
- [ ] Every source/repo claim in comments is verified or marked open.
- [ ] GitHub side effects were explicitly authorized.
- [ ] Comment posted before `Human Review` label.
- [ ] `Triage required` removed only after `Human Review` is verified, unless user explicitly requested reset.
- [ ] Final report includes issue numbers changed, skipped, blocked, and verification counts.
