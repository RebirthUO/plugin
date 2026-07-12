# Hermes guard repeats: temp script reliability notes

## What failed in this session

1. **Wrong worktree path**
   - A wrong `cd` target (`/c/Users/Jsiem/Documents/GitHub/issue-21-soul-charge` instead of `/c/Users/Jsiem/Documents/GitHub/RebirthUO/issue-21-soul-charge`) caused immediate worktree resolution failures.
   - Fix: assert the repo root first (`git rev-parse --show-toplevel`) and use that exact path for all subsequent checks.

2. **Unbound positional parameter under `set -u`**
   - A script variant failed with `unbound variable` when positional parameters were referenced without guarding argument count.
   - Fix: avoid `$1`, `$2`, etc. in guard scripts that are run without arguments; prefer `$0` only for script identity.

3. **Script residue verification**
   - One variant printed `script_removed=no` if cleanup happened before status check and then immediately checked again.
   - Fix: after cleanup, check path existence and print an explicit `script_removed=yes/no` line once.

## Reliable one-shot shape (MSYS)

```bash
cd /c/Users/Jsiem/Documents/GitHub/RebirthUO/issue-21-soul-charge
script_path="$(mktemp -p "/c/Users/Jsiem/AppData/Local/Temp" hermes-verify-XXXXXX.sh)"
cat > "$script_path" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

cd /c/Users/Jsiem/Documents/GitHub/RebirthUO/issue-21-soul-charge

git status --short --branch --untracked-files=all

git diff --check HEAD~1..HEAD -- Projects/UOContent.Tests/Tests/Items/Armor/SoulChargePropertyTests.cs
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
export MODERNUO_TEST_DATA_DIR='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic'
export MODERNUO_CLIENT_PATH="$MODERNUO_TEST_DATA_DIR"
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~SoulChargePropertyTests" \
  --no-build --no-restore --nologo --verbosity minimal --logger "console;verbosity=minimal"
EOF
chmod +x "$script_path"
bash "$script_path"
status=$?
rm -f "$script_path"
[[ -f "$script_path" ]] && echo "script_removed=no" || echo "script_removed=yes"
exit $status
```

- Keep this as a template, then adjust `changed path` + `test filter` per issue.