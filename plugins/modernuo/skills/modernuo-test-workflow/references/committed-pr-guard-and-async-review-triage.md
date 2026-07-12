# Committed PR Guard + Async Review Triage

Use this when a RebirthUO/ModernUO PR branch is already committed/pushed, Hermes still asks for fresh verification evidence, and an async review result arrives after the PR was opened.

## Fresh guard evidence on a committed branch

Create and run a temporary verification script under `C:/Users/Jsiem/AppData/Local/Temp` with a `hermes-verify-` prefix. Do not edit repo files just to satisfy the guard.

The script should:

1. `cd` into the exact PR worktree.
2. Print `git status --short --branch --untracked-files=all` before and after.
3. Print local HEAD, upstream branch HEAD, and upstream base HEAD.
4. Print PR state with `gh pr view <n> -R RebirthUO/ModernUO --json number,url,state,headRefName,baseRefName,mergeable,statusCheckRollup`.
5. Run whitespace verification against the committed change, not the clean worktree:
   `git diff --check HEAD~1..HEAD -- <changed paths>`.
6. Build the owning solution/project.
7. Run focused behavior tests for the changed feature.
8. Remove the temp script and report cleanup.

Report this as **fresh ad-hoc/focused verification** unless the script actually runs a broad owning-project or solution suite.

## Do not let late async review summaries become stale instructions

When a delegated review returns after the branch has been rebased, amended, committed, or pushed:

1. Treat the review as findings to triage, not as verified current truth.
2. Compare each high/medium finding against the current committed code before acting or reporting it as a blocker.
3. If the branch is already PR-ready and the user only asked for guard verification, do not reopen implementation unless a finding is confirmed against current code and materially blocks correctness.
4. In the final note, distinguish:
   - guard verification result,
   - PR/remote state,
   - confirmed current blockers, and
   - stale or follow-up review concerns.

## Example evidence wording

- `git diff --check HEAD~1..HEAD -- <changed paths>` passed.
- Solution/project build passed with 0 warnings / 0 errors.
- Focused behavior tests passed N/N.
- Worktree remained clean and local/remote branch heads matched.
- This is ad-hoc/focused verification, not a broad suite-green claim.
