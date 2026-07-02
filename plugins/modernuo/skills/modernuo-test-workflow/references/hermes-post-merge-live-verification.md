# Hermes Post-Merge Live Verification Guard

Use this when Hermes reports edited files as unverified after the issue branches have already been committed, pushed, PR-opened, and merged into `origin/live`.

## Problem

After a large multi-PR RebirthUO batch, the post-edit guard may still list the original per-worktree edited files even though the durable artifact is now `origin/live`. A normal branch worktree may also be stale or dirty, and `git reset --hard` is destructive enough to be blocked by smart approval.

## Safe pattern

Do **not** run `git reset --hard` in an existing user worktree just to satisfy the guard. Instead:

1. Create a `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script with Python `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=temp_dir)`.
2. Inside that script, create a second temporary verification worktree from `origin/live` under `C:/Users/Jsiem/AppData/Local/Temp`, e.g. `tempfile.mkdtemp(prefix='hermes-live-verify-', dir=temp_dir)`.
3. Add it non-destructively: `git -C "$SOURCE_REPO" worktree add --detach "$VERIFY_WT" origin/live`.
4. `cd "$VERIFY_WT"` and print repo, branch (empty is OK for detached HEAD), `git rev-parse HEAD`, and `git ls-remote origin refs/heads/live`.
5. Assert the temp worktree HEAD equals `origin/live`.
6. Assert clean status with `git status --short --untracked-files=all`.
7. Run changed-path whitespace validation across the merged range, e.g. `git diff --check HEAD~N..HEAD -- <changed paths>` where `N` covers the merged PR batch.
8. Build the owning test project with `MSBUILDDISABLENODEREUSE=1 dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj --nologo --verbosity quiet -m:1`.
9. Run one focused `dotnet test` filter that ORs together all touched test classes, e.g. `FullyQualifiedName~A|FullyQualifiedName~B|...`.
10. Use `trap cleanup EXIT` to `git -C "$SOURCE_REPO" worktree remove "$VERIFY_WT"` and remove the `hermes-verify-*.sh` launcher after execution.

## Reporting language

Report this as **ad-hoc/focused verification on `origin/live`**, not as full-suite green, unless the script actually ran the full suite.

Include:

- temp script path and that it was removed
- temp live worktree path and that it was removed
- verified `origin/live` SHA
- `git diff --check` result
- build result
- focused test result count

## Pitfalls

- Do not retry a blocked `git reset --hard`; switch to the temporary detached worktree pattern.
- Do not validate from the main repo if it may be behind `origin/live`.
- Do not rely on earlier per-branch logs after the guard asks for fresh evidence; create and run a fresh `hermes-verify-*` script in the current turn.
