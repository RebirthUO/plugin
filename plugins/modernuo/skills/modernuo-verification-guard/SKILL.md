---
name: modernuo-verification-guard
description: Use when Hermes reports edited ModernUO/RebirthUO files lack fresh verification evidence and asks for a temporary hermes-verify script, especially committed PR branches where prior direct build/test output is not accepted by the guard.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, rebirthuo, verification, tests, guard, windows-msys]
    related_skills: [modernuo-test-workflow, rebirthuo-implement, github-pr-workflow]
---

# ModernUO Verification Guard

## Overview

Use this skill when the post-edit guard says changed ModernUO/RebirthUO files are unverified and explicitly requests a temporary `hermes-verify-*` script under `C:/Users/Jsiem/AppData/Local/Temp`.

The guard wants a **new evidence bundle**, not a restatement of earlier terminal logs. Treat repeated guard messages as a request to rerun verification in a fresh script, even if the branch has already been built, tested, committed, pushed, and opened as a PR.

## When to Use

- Hermes reports: `No canonical test/lint/build command was detected` after ModernUO/RebirthUO edits.
- The changed paths are already committed/pushed, but the guard still requires fresh evidence.
- A PR branch is clean and needs local/remote/PR head equality plus changed-path diff checks.
- Previous direct `dotnet build` or `dotnet test` output exists but was not recognized by the guard.

## Fresh Script Procedure

1. Create the script with Python `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir='C:/Users/Jsiem/AppData/Local/Temp', text=True)`.
2. The script must `cd` into the exact worktree that contains the edited files.
3. Print `verify_kind=fresh-ad-hoc-focused`.
4. Print worktree status before and after:
   - `git status --short --branch --untracked-files=all`
5. Print and verify branch/head identity:
   - `branch=$(git branch --show-current)`
   - `head=$(git rev-parse HEAD)`
   - `remote_head=$(git ls-remote origin "refs/heads/$branch" | awk '{print $1}')`
   - if a PR exists: `pr_head=$(gh pr view <PR> --repo RebirthUO/service --json headRefOid --jq .headRefOid)`
   - fail if local, remote, or PR heads differ.
6. For committed branches, run changed-path whitespace checks against the committed delta, not the empty worktree:
   - `git diff --check HEAD~1..HEAD -- <changed paths>`
7. Build with single-worker/no node reuse:
   - `MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1`
8. For `UOContent.Tests`, export client-data env vars before tests:
   - `MODERNUO_TEST_DATA_DIR=<folder containing tiledata.mul>`
   - `MODERNUO_CLIENT_PATH=$MODERNUO_TEST_DATA_DIR`
   - verify `test -f "$MODERNUO_TEST_DATA_DIR/tiledata.mul"`.
9. Run the focused behavior test filter for the changed class/mechanic.
10. Run the script through MSYS path conversion, then remove it:
    - `bash "$(cygpath -u "$script")"`
    - `rm -f "$(cygpath -u "$script")"`
    - print `script_removed=yes` when cleanup succeeds.

## Reporting Shape

Report compactly and explicitly label the result **fresh ad-hoc/focused verification** unless the script actually ran a broad suite.

Include:

- latest script path and cleanup status;
- worktree and branch;
- local/remote/PR head equality;
- clean worktree status before/after;
- changed-path `git diff --check HEAD~1..HEAD -- ...` result;
- build command and pass/fail result;
- focused test command and pass/fail result;
- whether client data was required and which env var was set, if applicable.

## Critical Pitfalls

- Do **not** argue with a repeated guard by citing previous logs. Create and run a fresh script again.
- Creating the `hermes-verify-*` script is not verification. The same turn must also execute it, capture the pass/fail output, remove it when possible, and report cleanup status. A final answer after only printing `C:/Users/.../hermes-verify-*.sh` is incomplete and should be treated as unverified.
- Do **not** use an empty worktree diff as proof after commit; validate `HEAD~1..HEAD -- <changed paths>`.
- Do **not** omit PR head equality after a PR exists.
- Do **not** call focused tests broad-suite green.
- Do **not** leave the temp script behind unless cleanup is blocked; if blocked, report the exact path.
- When multiple guard scripts run in the same session, copy the `script_path=...` from the **latest** tool output into the final report. Do not reuse an earlier temp-script path from a prior guard run; a stale path makes the evidence bundle look fabricated even when verification passed.
- Do not save the transient guard warning itself as memory; the durable lesson is the fresh-script evidence pattern.

## Example Script Shape

```bash
python - <<'PY'
import os, stat, tempfile
repo = r'C:/Users/Jsiem/Documents/GitHub/RebirthUO/service-issue-18'
temp_dir = r'C:/Users/Jsiem/AppData/Local/Temp'
fd, path = tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=temp_dir, text=True)
script = f'''#!/usr/bin/env bash
set -euo pipefail
cd '{repo}'
echo 'verify_kind=fresh-ad-hoc-focused'
git status --short --branch --untracked-files=all
branch=$(git branch --show-current)
head=$(git rev-parse HEAD)
remote_head=$(git ls-remote origin "refs/heads/$branch" | awk '{{print $1}}')
echo "branch=$branch"
echo "head=$head"
echo "remote_head=$remote_head"
test "$head" = "$remote_head"
git diff --check HEAD~1..HEAD -- Projects/UOContent/Items/Weapons/BaseWeapon.cs
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
export MODERNUO_TEST_DATA_DIR='C:/path/to/UO-client-data'
export MODERNUO_CLIENT_PATH="$MODERNUO_TEST_DATA_DIR"
test -f "$MODERNUO_TEST_DATA_DIR/tiledata.mul"
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~ChangedBehavior" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
'''
with os.fdopen(fd, 'w', newline='\n') as f:
    f.write(script)
os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
print(path)
PY
```
