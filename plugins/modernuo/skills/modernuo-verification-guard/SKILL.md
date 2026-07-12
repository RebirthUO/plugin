---
name: modernuo-verification-guard
description: Use when Hermes reports edited ModernUO/RebirthUO files lack fresh verification evidence and asks for a temporary hermes-verify script, especially committed PR branches where prior direct build/test output is not accepted by the guard.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    related_skills:
    skill_group: modernuo
    skill_subgroup: gate
    workflow_phase: implement
    workflow_tier: support
---
# ModernUO Verification Guard

## Passive ModernUO Context and Mutation Contract

Activate only when the repository or code context is confirmed as ModernUO-based, including the RebirthUO codebase. Generic Ultima Online vocabulary alone is insufficient. Passive activation is read-only and may provide analysis, guidance, research, or validation only. It must not create, update, label, comment on, or close GitHub issues; create branches; commit or push; or open or merge pull requests. Local file edits require an explicit implementation request from the user and do not authorize GitHub mutation.


## Overview

Use this skill when the post-edit guard says changed ModernUO/RebirthUO files are unverified and explicitly requests a temporary `hermes-verify-*` script under `C:/Users/Jsiem/AppData/Local/Temp`.

The guard wants a **new evidence bundle**, not a restatement of earlier terminal logs. Treat repeated guard messages as a request to rerun verification in a fresh script, even if the branch has already been built, tested, committed, pushed, and opened as a PR.

## When to Use

- Hermes reports: `No canonical test/lint/build command was detected` after ModernUO/RebirthUO edits.
- The changed paths are already committed/pushed, but the guard still requires fresh evidence.
- A PR branch is clean and needs local/remote/PR head equality plus changed-path diff checks.
- Previous direct `dotnet build` or `dotnet test` output exists but was not recognized by the guard.

## Fresh Script Procedure

Preferred on this Windows/MSYS host: create, execute, and remove the guard script entirely from the MSYS shell with `script=$(mktemp /tmp/hermes-verify-XXXXXX.sh)` and `native_script=$(cygpath -w "$script")`. MSYS `/tmp` maps to `C:/Users/Jsiem/AppData/Local/Temp`, satisfying the guard while avoiding Windows-Python-to-MSYS path visibility failures. See `references/msys-temp-guard-script.md` for the proven pattern.

1. Create the script under the temp directory with a `hermes-verify-` prefix. Prefer the MSYS `mktemp` pattern above; if using Python `tempfile.mkstemp`, ensure the same runtime can execute the resulting path before proceeding.
2. The script must `cd` into the exact worktree that contains the edited files.
3. Print `verify_kind=fresh-ad-hoc-focused`.
4. Print worktree status before and after:
   - `git status --short --branch --untracked-files=all`
5. Print branch/head identity:
   - `branch=$(git branch --show-current)`
   - `head=$(git rev-parse HEAD)`
   - `remote_head=$(git ls-remote origin "refs/heads/$branch" | awk '{print $1}')`
   - if a PR exists: `pr_head=$(gh pr view <PR> --repo <owner/repo> --json headRefOid --jq .headRefOid)`; use the actual repository from the task, not a copied example repo.
   - For PR/update tasks, fail if local, remote, or PR heads differ because the user expects pushed PR changes.
   - For local-only tasks such as resolving a cherry-pick on `live` before push, do **not** fail the guard just because `head != remote_head`; print `remote_equal=no_local_branch_not_pushed_or_remote_differs` and continue. The verification evidence is still valid for the local committed delta, but the final report must state that the branch is ahead/not pushed.
6. If the guard lists temp helper files/directories outside the repo among changed paths, explicitly verify their cleanup in the script (for example `test ! -e /c/Users/Jsiem/AppData/Local/Temp/cliloc-check`). See `references/committed-pr-branch-temp-scratch-checks.md`.
7. For GitHub issue-only review/edit tasks where the durable change is not repo code, verify the external behavior instead of forcing a build: fetch the issue with `gh issue view --json body,labels,url`, assert expected review headings/body markers, assert `triage` or other labels changed as intended, and assert guard-listed temporary helper/body files are absent. Report this as `fresh-ad-hoc-focused` and explicitly not suite-green.
8. For committed branches, run changed-path whitespace checks against the committed delta, not the empty worktree:
   - `git diff --check HEAD~1..HEAD -- <changed paths>`
9. Build with single-worker/no node reuse:
   - `MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1`
9. For `UOContent.Tests`, export client-data env vars before tests:
   - `MODERNUO_TEST_DATA_DIR=<folder containing tiledata.mul>`
   - `MODERNUO_CLIENT_PATH=$MODERNUO_TEST_DATA_DIR`
   - verify `test -f "$MODERNUO_TEST_DATA_DIR/tiledata.mul"`.
10. Run the focused behavior test filter for the changed class/mechanic.
11. Run the script and then remove it in the same shell invocation:
    - Preferred (single shell): `bash "$script_path"; status=$?; rm -f "$script_path"; echo "script_removed=$([[ -f "$script_path" ]] && echo no || echo yes)"; exit $status`
    - If using Python-created path conversion, run through native path conversion once and only once (`native_script=$(cygpath -w "$script")` -> `bash "$native_script"`).
    - print `script_removed=yes` when cleanup succeeds and remove any `rm` failure from the output.
12. Add explicit script/setup sanity checks at top to avoid common guard regressions:
    - `test -d "$(git rev-parse --show-toplevel)"`
    - `[ -n "$(git rev-parse --show-prefix)" ] || true` (optional)
    - verify script location with `[[ "$script_path" == /c/Users/Jsiem/AppData/Local/Temp/hermes-verify-* ]]`
    - if `set -u` is enabled, do not reference positional args (`$1`, `$2`, ...) when no args are expected.
13. If the guard session repeats, run a **fresh** script with a **new** tempfile each time and report the latest `script_path` in the final bundle.
14. **Native-path fallback after an unrecognized `/tmp` run:** create the file with Python `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=r'C:\\Users\\Jsiem\\AppData\\Local\\Temp', text=True)` and print the native Windows path. Do not pipe that output to `cygpath` — `cygpath` expects a path argument rather than stdin and a failed pipe can leave an orphaned script. Write the script at the returned native path, execute it through its `/c/Users/...` equivalent, then search `C:\\Users\\Jsiem\\AppData\\Local\\Temp` for `hermes-verify-*` after cleanup. This fallback produces an evidence path the guard can recognize literally.


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
- whether client data was required and which env var was set, if applicable. Copy the client-data path exactly from the latest script output; do not abbreviate, translate, or retype it from memory, because a single path typo can make the evidence look fabricated or unusable.

## Critical Pitfalls

- Do **not** argue with a repeated guard by citing previous logs. Create and run a fresh script again.
- Prefer a direct shell execution for the guard script creation/execution bundle when the guard repeats. A helper wrapper such as `execute_code` may produce valid test output, but the post-edit guard may still fail to recognize it as the requested canonical script evidence; rerun the same fresh-script shape directly in the shell and report the latest script path.
- Creating the `hermes-verify-*` script is not verification. The same turn must also execute it, capture the pass/fail output, remove it when possible, and report cleanup status. A final answer after only printing `C:/Users/.../hermes-verify-*.sh` is incomplete and should be treated as unverified.
- Do **not** use an empty worktree diff as proof after commit; validate `HEAD~1..HEAD -- <changed paths>`.
- Do **not** omit PR head equality after a PR exists.
- Do **not** call focused tests "the suite"; focused validation and broad validation must be reported separately.
- If a broad owning suite fails after the changed-behavior build/format/focused gates pass, do not let `set -e` terminate the verification bundle before cleanup or before independent suites run. Capture the broad exit code, print an explicit `broad_suite=blocked` or `broad_suite=passed` marker, continue with the focused/independent checks, and make the script's final exit status reflect the required changed-behavior gates. The final report must still say **ad-hoc/focused verification**, never imply suite-green from focused passes alone. If a fresh rerun later passes the broad suite, report that latest result and note that the earlier failure did not reproduce; do not label it a confirmed baseline failure without a baseline comparison.
- Do **not** leave the temp script behind unless cleanup is blocked; if cleanup is blocked, report the exact path.
- When the guard lists temp helper paths outside the repo, explicitly verify they are removed inside the fresh script; `git status` cannot prove cleanup outside the worktree. See `references/committed-pr-branch-temp-scratch-checks.md`.
- When multiple guard scripts run in the same session, copy the `script_path=...` from the **latest** tool output into the final report. Do not reuse an earlier temp-script path from a prior guard run; a stale path makes the evidence bundle look fabricated even when verification passed.
- Do not save the transient guard warning itself as memory; the durable lesson is the fresh-script evidence pattern.
- If the guard repeats in one session, create a new `mktemp` script each time and re-run end-to-end before reporting again.

## Support references

- `references/guard-repeat-worktree-path-guard.md`: concrete failure signatures and a compact, reusable one-shot template after path drift / cleanup edge cases.

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
remote_head=$(git ls-remote origin "refs/heads/$branch" | awk '{print $1}')
echo "branch=$branch"
echo "head=$head"
echo "remote_head=$remote_head"
if [ -n "$remote_head" ] && [ "$head" = "$remote_head" ]; then
  echo 'remote_equal=yes'
else
  echo 'remote_equal=no_local_branch_not_pushed_or_remote_differs'
fi
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
