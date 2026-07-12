# Committed PR Branch Guard: Temp Scratch Checks

When the post-edit guard lists paths outside the repo (for example `C:/Users/Jsiem/AppData/Local/Temp/cliloc-check/...`) alongside committed repo changes, treat them as part of the fresh evidence bundle even if they were transient helper files from earlier in the session.

## Pattern

For a committed, pushed PR branch:

1. Create a fresh `hermes-verify-*.sh` under `C:/Users/Jsiem/AppData/Local/Temp` with `tempfile.mkstemp(...)`.
2. `cd` into the real repo worktree.
3. Print `verify_kind=fresh-ad-hoc-focused`.
4. Print clean `git status --short --branch --untracked-files=all` before and after.
5. Verify local, remote, and PR heads match.
6. Explicitly check that listed temp scratch directories/files are gone, e.g.:
   ```bash
   if [ -e '/c/Users/Jsiem/AppData/Local/Temp/cliloc-check' ]; then
     echo 'temp_cliloc_check_removed=no'
     exit 1
   else
     echo 'temp_cliloc_check_removed=yes'
   fi
   ```
7. Validate the committed repo delta with `git diff --check HEAD~1..HEAD -- <changed repo paths>`.
8. Run build and focused behavior tests.
9. Remove the guard script and report the latest script path and cleanup status.

## Reporting

Call this **fresh ad-hoc/focused verification** unless the script actually ran a broad suite. Include the temp scratch cleanup result separately from the repo worktree status because `git status` cannot prove files outside the repo were removed.
