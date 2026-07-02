# Hermes post-edit guard for committed PR branches

Use this when Hermes reports edited files lack fresh verification evidence after a PR branch was already committed/pushed and the worktree is clean.

## Pattern

Create a fresh temporary script under `C:/Users/Jsiem/AppData/Local/Temp` with `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', ...)`, execute it, then remove it. Report this as **ad-hoc/focused verification**, not broad suite green.

The script should verify the exact worktree and committed diff, not just rerun commands from memory:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd 'C:/Users/Jsiem/Documents/GitHub/RebirthUO/<worktree>'
echo "repo=$(pwd)"
echo "branch=$(git branch --show-current)"
echo "head=$(git rev-parse HEAD)"
echo "remote=$(git ls-remote origin refs/heads/<branch> | awk '{print $1}')"
echo "status-start"
git status --short --untracked-files=all
echo "status-end"

echo "== committed changed-path whitespace check =="
git diff --check HEAD~1..HEAD -- \
  Projects/UOContent/.../ChangedProductionFile.cs \
  Projects/UOContent.Tests/.../ChangedTestFile.cs

echo "== temp markdown sanity =="
test -s 'C:/Users/Jsiem/AppData/Local/Temp/<pr-body>.md'
test -s 'C:/Users/Jsiem/AppData/Local/Temp/<review>.md'
grep -F '<important PR-body phrase>' 'C:/Users/Jsiem/AppData/Local/Temp/<pr-body>.md' >/dev/null
grep -F '<important review phrase>' 'C:/Users/Jsiem/AppData/Local/Temp/<review>.md' >/dev/null

echo "== build =="
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1

echo "== focused behavior tests =="
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~<FocusedTestClass>" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

## Notes

- When changes are already committed, use `git diff --check HEAD~1..HEAD -- <changed paths>`; plain `git diff --check` can be empty and may not satisfy the guard.
- Include `git status --short --untracked-files=all` inside the script so a clean worktree is evidenced in the same output as the build/tests.
- Verify remote branch head in the script when the user expects PR updates to be pushed.
- If PR body/review markdown files were edited under `AppData/Local/Temp`, include lightweight sanity checks (`test -s`, `grep -F` for the new claim) because they are not covered by `dotnet build`.
- On MSYS, a native temp path under `C:\Users\Jsiem\AppData\Local\Temp` may display as `/tmp/...` after `cygpath`; that is acceptable if the script was created via `tempfile` in the requested native temp directory and the cleanup confirms removal.
