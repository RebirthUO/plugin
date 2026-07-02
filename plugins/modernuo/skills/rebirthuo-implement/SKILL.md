---
name: rebirthuo-implement
description: "Use when implementing RebirthUO GitHub issues: read each ticket, check for sufficient data, skip under-specified work with a missing-data comment, or create an isolated branch/worktree with tests and a gamer-facing pull request."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rebirthuo, modernuo, github, issues, pull-requests, implementation, triage, testing]
    related_skills: [github-issues, github-pr-workflow, github-code-review, modernuo-ticket-triage, uo-modernuo-workflow, modernuo-test-workflow, modernuo-code-audit]
---

# RebirthUO Issue to Tested Pull Request

## Overview

Use this skill when the user provides one or more GitHub issues and wants each RebirthUO ticket either implemented as an isolated pull request or skipped with a precise missing-data comment.

The workflow is intentionally conservative because RebirthUO is a ModernUO Ultima Online shard project: gameplay, economy, PvP, PvM, housing, saves, era gates, and client behavior can all be affected by small code changes. Do not guess mechanics. Verify issue data, repository behavior, and source evidence before changing code.

Core loop:

1. Read the full GitHub ticket and comments.
2. Decide whether implementation data is sufficient.
3. If data is missing, skip the ticket and comment exactly what is missing.
4. If data is sufficient, create a separate isolated branch/worktree for that issue.
5. Implement the smallest safe change.
6. Add unit coverage plus smoke/integration and end-to-end/manual QA coverage.
7. Commit, push, and open a PR with a gamer/player-facing explanation.

## When to Use

- The user provides GitHub issue URLs or issue numbers for RebirthUO and asks for implementation.
- The user asks to process a batch of RebirthUO tickets into PRs.
- The user wants incomplete tickets skipped with a GitHub comment explaining missing data.
- The requested output includes branches, code changes, tests, pushes, and pull requests.

Do not use for:

- Pure triage-only planning with no implementation request; use `modernuo-ticket-triage`.
- Updating existing PRs after review; use `github-pr-workflow` and PR-update guidance.
- Public exploit writeups. For exploit/security issues, preserve logs, minimize public details, and ask for a safe handling path if scope is unclear.

## Companion Skills to Load

Load companion skills before acting:

- Always: `github-issues` and `github-pr-workflow`.
- RebirthUO/ModernUO issue planning: `modernuo-ticket-triage` and `uo-modernuo-workflow`.
- Tests: `modernuo-test-workflow`.
- `.cs` changes: `modernuo-code-audit` before commit.
- Subsystem-specific skills when obvious: content, combat, crafting, loot, housing, regions, serialization, timers, gumps, packets, quests, skills, spells, or item properties.

## Batch Contract

Process every issue independently unless the user explicitly asks for a combined PR.

One issue means:

- One sufficiency decision.
- One isolated branch/worktree if implemented.
- One staged diff and one validation record.
- One PR or one missing-data comment.

Maintain a compact status table while working:

```markdown
| Issue | Status | Branch/Worktree | Decision | Validation | PR/Comment |
|---|---|---|---|---|---|
| #123 | sufficient / missing-data / blocked / PR-opened | fix/123-short-slug | <summary> | <commands/results> | <url> |
```

For batches, first read all issues enough to discover duplicates, existing PRs, blocked labels, and obvious missing-data tickets. Then skip insufficient tickets immediately and implement sufficient tickets in small validated waves, usually one to three worktrees at a time.

Hard checkpoint rule: do not scaffold or edit the whole remaining range once the first issue proves the pattern. Finish each wave to a durable state — validated, committed, pushed, PR opened, review artifact posted, and PR/head verified — before creating or editing additional worktrees. If a generated-but-uncommitted worktree exists, prioritize either completing it or reverting/removing it before starting more. Tool/session limits make many local-only worktrees a liability, not progress.

## Step 1 — Resolve Repo and Issue IDs

Completion criterion: every user-provided item maps to an exact issue in an exact GitHub repository.

- Full issue URLs define the repository.
- Plain issue numbers use the current git remote's `owner/repo`.
- If the user asks for a category of issues instead of explicit numbers (for example "all open issues with 100% confidence"), first resolve the repo, list open issues, then fetch each issue's comments and filter locally. GitHub issue search/`gh search issues` can parse quoted `repo:` queries unexpectedly and may miss/garble comment-body matches.
- If numbers are ambiguous and no current GitHub repo is available, ask for the repository before continuing.

Useful commands:

```bash
git remote get-url origin
gh repo view --json nameWithOwner,defaultBranchRef --jq '.nameWithOwner + " " + .defaultBranchRef.name'
```

Local confidence discovery pattern:

```bash
python - <<'PY'
import json, re, subprocess
repo='OWNER/REPO'
issues=json.loads(subprocess.check_output([
    'gh','issue','list','--repo',repo,'--state','open','--limit','1000',
    '--json','number,title,url,labels,body'
], text=True, encoding='utf-8'))
patterns=[
    re.compile(r'confidence[^\n\r]{0,80}100\s*%', re.I),
    re.compile(r'100\s*%[^\n\r]{0,80}confidence', re.I),
    re.compile(r'\|\s*Confidence\s*\|\s*100\s*%\s*\|', re.I),
]
for issue in issues:
    detail=json.loads(subprocess.check_output([
        'gh','issue','view',str(issue['number']),'--repo',repo,'--json','comments'
    ], text=True, encoding='utf-8'))
    texts=[issue.get('body') or ''] + [c.get('body') or '' for c in detail.get('comments') or []]
    if any(pattern.search(text) for pattern in patterns for text in texts):
        print(f"#{issue['number']}\t{issue['title']}\t{issue['url']}")
PY
```

## Step 2 — Read the Full Ticket

Completion criterion: title, body, labels, state, comments, author, URL, linked/closing PRs, and issue-supplied evidence are captured.

Use `gh` where available:

```bash
gh issue view ISSUE --repo OWNER/REPO \\
  --json number,title,body,state,labels,comments,assignees,author,url,closedByPullRequestsReferences
```

Before implementing, search for existing PRs and branches so you do not duplicate work:

```bash
gh pr list --repo OWNER/REPO --state all --search "#ISSUE" --json number,title,state,url,headRefName
git branch -a | grep -E "(ISSUE|short-slug)" || true
```

If GitHub access fails, do not invent issue contents. Ask the user to paste the ticket body/comments or restore access.

## Step 3 — Sufficiency Gate

Completion criterion: each issue is classified as `sufficient`, `missing-data`, `blocked-duplicate`, or `blocked-risk`, with explicit reasons.

A ticket is sufficient only when it defines a safe implementation and validation target:

| Required Data | What to Verify |
|---|---|
| Problem statement | What player, staff, operator, or developer-visible behavior is wrong or missing? |
| Expected behavior | What should happen instead, and under which era/ruleset/configuration? |
| Scope | Which subsystem is affected and what is explicitly out of scope? |
| Evidence | Source links, repo anchors, logs, screenshots, reproduction steps, or user-approved custom shard policy. |
| Acceptance criteria | Observable completion conditions that map to code/tests/QA. |
| Testability | A plausible unit test and a smoke/integration/end-to-end or manual QA path. |
| Risk | Save compatibility, economy, PvP/PvM balance, housing, security, performance, client behavior, or deployment risk. |

For RebirthUO gameplay tickets, require era/ruleset/source clarity when behavior can vary by era. If the issue lacks era or custom shard policy and the behavior is era-sensitive, mark it `missing-data` rather than guessing.

Sufficient examples:

- Bug ticket with reproduction steps, actual/expected behavior, affected area, and logs or code anchors.
- Parity ticket with named mechanic, target era/publish, source links, and acceptance criteria.
- Custom feature ticket with explicit desired behavior, non-goals, and risk tolerance.

Insufficient examples:

- "Make dragons stronger" without target stats, era, or balance constraints.
- "Fix crafting" without recipe/item/repro details.
- A mechanics claim without source, target era, or custom policy decision.
- A bug report that refers to missing screenshots/logs.

## Step 4 — Skip Missing-Data Tickets with a Comment

Completion criterion: the issue receives a clear missing-data comment and no branch/code change is created for it.

Do not close the issue unless the user explicitly asked for that tracker action.

Comment template:

```markdown
Thanks for the ticket. I am skipping implementation for now because the ticket is missing data needed to make a safe RebirthUO change.

Missing information:
- <specific missing item 1>
- <specific missing item 2>

Why this matters:
- <risk or ambiguity caused by the missing data>

What would unblock this:
- <exact repro step, source link, era/ruleset decision, log, screenshot, acceptance criterion, or design decision needed>
```

For UO mechanics, add this when relevant:

```markdown
UO/era note:
- Please confirm the target era/ruleset or whether this is intentional custom shard behavior. The correct implementation may differ between T2A, Renaissance, AoS, ML, SA, and modern rulesets.
```

Post with:

```bash
gh issue comment ISSUE --repo OWNER/REPO --body-file /tmp/missing-data-ISSUE.md
```

Record the issue as `missing-data` and move on.

## Step 5 — Create an Isolated Branch/Worktree

Completion criterion: the issue has a clean isolated worktree and branch based on the target base branch.

Prefer a git worktree so the user's active checkout and other issue branches stay isolated:

```bash
git fetch origin
OWNER_REPO=OWNER/REPO
REPO="${OWNER_REPO#*/}"
BASE=$(gh repo view "$OWNER_REPO" --json defaultBranchRef --jq '.defaultBranchRef.name')
ISSUE=123
SLUG=short-kebab-title
BRANCH="fix/${ISSUE}-${SLUG}"
WORKTREE="../${REPO}-issue-${ISSUE}"
git worktree add -b "$BRANCH" "$WORKTREE" "origin/$BASE"
cd "$WORKTREE"
git status --short
git branch --show-current
```

Stop if the isolated worktree is unexpectedly dirty before your changes.

If an existing PR already covers the issue, do not create a duplicate. Reuse/update it only if the user asked for existing PR updates; otherwise report the duplicate and skip implementation.

## Step 6 — Implement the Smallest Safe Change

Completion criterion: every changed file maps directly to the issue's acceptance criteria and no unrelated refactor is included.

Implementation discipline:

1. Search and read relevant files before editing.
2. Trace symbols to definitions/usages instead of guessing APIs.
3. Verify source and repo evidence before making gameplay claims.
4. Keep changes minimal and issue-scoped.
5. Preserve era/ruleset gates and custom shard policy.
6. Avoid hidden economy, PvP, PvM, housing, save, serialization, packet, client, timer, or performance side effects.
7. Update docs/data only when the issue requires it and the target file exists on the branch.
8. For implementation requests, produce a real behavior/code/test delta or explicitly classify the issue as no-op/blocked. Do **not** open a PR whose only meaningful change is a comment, TODO removal, PR-body rewrite, or documentation note and call it implemented. If a review says a TODO is stale but the issue still names a concrete gameplay delta, either implement the concrete delta or report why no safe implementation exists.
9. When replacing a TODO in gameplay/content code, prove the replacement changes or protects behavior: add/adjust tests that instantiate the object, run the relevant method/factory, inspect generated loot/state, or otherwise validate the player-visible outcome. A test that only asserts a type appears in a static list is not enough when the ticket is about generated loot or runtime behavior.

RebirthUO defaults:

- Prefer `Projects/UOContent/` for gameplay/content changes.
- Do not edit `Projects/Server/` unless the issue explicitly requires core engine work.
- Respect source-generated serialization, timer cleanup, the single-threaded game loop, and era checks such as `Core.*` or expansion/profile gates.

## Step 7 — Add Unit, Smoke, and End-to-End Coverage

Completion criterion: tests prove the acceptance criteria at the smallest level available and through at least one player/operator-visible or subsystem path. If automated E2E does not exist, document manual QA honestly.

Required testing intent:

| Level | Purpose | Examples |
|---|---|---|
| Unit | Proves the changed formula, branch, parser, helper, recipe, object, or rule directly. | Method/class tests, formula tests, item/mobile behavior tests. |
| Smoke / integration | Proves the subsystem loads or executes through a realistic repo path. | Build, content registration, command handler, data load, server startup slice. |
| End-to-end | Proves the player/operator-facing scenario. | Existing E2E harness, scripted server scenario, API/browser test, or documented manual QA if automation is unavailable. |

Do not fabricate E2E results. A unit test is not an E2E test. If the repo lacks an automated E2E harness for the scenario, add the closest integration/smoke test and put a manual E2E checklist in the PR body with the reason automation is unavailable.

Run focused validation first, then a broader relevant suite when feasible. If only focused tests ran, label them focused.

## Step 8 — Review, Commit, Push

Completion criterion: the branch is committed, pushed, and the remote branch head matches the local commit.

Before commit:

```bash
git diff --check
git status --short
git diff --stat
```

Run project-specific build/test/lint commands. For RebirthUO, build from the repo root with `dotnet build` when feasible and run focused affected tests plus broader relevant tests according to `modernuo-test-workflow`.

Commit and push:

```bash
git add <changed files>
git commit -m "fix: implement issue ISSUE short description"
git push -u origin HEAD
```

Verify the push:

```bash
git rev-parse HEAD
git ls-remote origin "refs/heads/$(git branch --show-current)"
```

## Step 9 — Open the Pull Request

Completion criterion: a PR URL exists and the PR body includes issue link, gamer/player-facing explanation, evidence, risk, real validation results, and `Closes #ISSUE`.

Lead with what players, staff, or shard operators will notice. Only then add implementation details.

PR body template:

```markdown
## Gamer / Player-Facing Summary
- What players, staff, or shard operators will notice in plain language.
- The target era/ruleset or custom RebirthUO policy this follows.
- What stays unchanged so players can trust the scope.

## Problem
- The current behavior from the issue, with repro/source evidence.

## Behavior Change
- The new behavior after this PR.
- PvP, PvM, economy, crafting, housing, loot, staff, save, client, or operator side effects, including "none expected" when verified.

## Sources / Evidence
- Issue: Closes #ISSUE
- <official/canonical/community/source/repo anchors as applicable>

## Implementation Notes
- Short technical summary of files/systems changed.

## Tests and Validation
- [x] Unit: `<command>` — <real result>
- [x] Smoke/integration: `<command>` — <real result>
- [x] End-to-end or manual QA: `<command/checklist>` — <real result or why manual remains>

## Definition of Done
- [x] Ticket had sufficient data, or missing data was documented on the issue.
- [x] Change is isolated to one branch for this issue.
- [x] Acceptance criteria are covered by tests or explicit QA.
- [x] No unintended era/ruleset/economy/PvP/PvM/housing/save/client side effects were introduced.

Closes #ISSUE
```

Create and verify:

```bash
gh pr create --repo OWNER/REPO --base "$BASE" --head "$BRANCH" --title "fix: short issue title" --body-file /tmp/pr-ISSUE.md
gh pr view --repo OWNER/REPO --json number,url,state,headRefName,baseRefName,statusCheckRollup
```

If GitHub reports no checks, say `no checks reported`; do not imply CI passed.

## Step 10 — Report Results

Completion criterion: the user receives durable handles for every issue.

Use this format:

```markdown
Processed issues:

- #123 — PR opened: <url>
  - Branch: `fix/123-short-slug`
  - Validation: `<command>` passed; `<command>` passed; E2E/manual: <result>
  - Player-facing change: <one sentence>

- #124 — skipped: missing data comment posted: <issue/comment url>
  - Missing: <short list>

- #125 — blocked: <reason>
```

Never claim a test, push, PR, or comment happened unless verified with tool output.

## Common Pitfalls

1. **Implementing under-specified gameplay.** Missing era/ruleset/source or acceptance criteria means comment and skip, not guess.
2. **Comment-only PRs disguised as implementation.** For `/rebirthuo-implement`, a PR that only removes a TODO, changes a comment, or rewrites the PR body is not an implementation. Either deliver a concrete code/test behavior change or classify the issue as no-op/blocked with evidence. User feedback on this was explicit: do not document instead of implement.
3. **Static-list tests that miss runtime behavior.** If the ticket is about loot, generated items, special abilities, combat behavior, or player-visible state, add a test that exercises the generated behavior (e.g. construct the mobile, call the factory/method, inspect the backpack/corpse/ability array), not only a test that a type exists in a static list.
4. **Mixing tickets.** One issue gets one branch/worktree and one PR unless the user explicitly says otherwise.
5. **Treating focused tests as suite-green.** Label focused validation honestly and run broader checks when feasible.
6. **Inventing E2E coverage.** If no harness exists, document manual QA and why.
7. **Code-first PR body.** RebirthUO gameplay PRs need player-facing behavior, sources, side effects, and Definition of Done before code details.
8. **Ignoring existing PRs.** Always check linked PRs, branch names, and issue references before creating new work.
9. **Leaking exploit detail.** Keep public comments minimal and safe for exploit/security tickets.
10. **Skipping push verification.** Local commits are not complete until the remote branch and PR URL are verified.
11. **Post-edit verification guard false negatives.** In multi-worktree batches, Hermes may still flag recently edited paths after PR creation. Do not argue with the guard or cite old logs only. Create a temporary `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script that enters the exact flagged worktrees, prints repo/branch/head/status, runs changed-path `git diff --check`, builds the owning test project, runs focused test filters, removes the script, and report the result explicitly as ad-hoc/focused verification rather than broad suite green.
12. **Test-gap implementation waves and no-op issues.** When a Human Review issue's acceptance criterion is explicitly test-only (for example “add property/table/guard tests”), a test-only PR is a valid implementation if it adds durable regression coverage and no gameplay behavior change. If `origin/live` already has equivalent tests, do **not** open a duplicate/comment-only PR; verify the existing tests in a clean worktree and post a no-op/closure comment with repo anchors and validation. For adjacent issues that touch the same test file, minimize merge conflicts by using a new focused test file when appropriate. See `references/test-gap-and-noop-issue-waves.md`.

## Verification Checklist

- [ ] Every issue was read with title, body, labels, comments, state, and linked PRs.
- [ ] Every issue has a sufficiency decision with reasons.
- [ ] Missing-data issues have a comment listing exactly what is needed.
- [ ] Sufficient issues each have an isolated branch/worktree.
- [ ] Implementation is minimal and issue-scoped.
- [ ] Unit, smoke/integration, and E2E/manual QA coverage are present or explicitly blocked by missing harness support.
- [ ] Validation commands actually ran and results are recorded.
- [ ] Branch was committed, pushed, and remote head verified.
- [ ] PR was opened and verified by URL.
- [ ] PR body explains the change at gamer/player level and includes evidence, risks, tests, and `Closes #ISSUE`.
