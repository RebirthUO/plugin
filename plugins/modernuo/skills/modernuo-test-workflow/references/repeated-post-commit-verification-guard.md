# Repeated Post-Commit Verification Guards

## Trigger

Use this when Hermes repeats the “edited code lacks fresh passing verification” guard after a clean, committed, pushed ModernUO branch has already passed an earlier `hermes-verify-*` run.

The repeat is a new evidence request, not proof that the prior verification failed. Do not change code, rewrite the PR, or claim suite-green from old output.

## Windows/MSYS procedure

1. Create a new native-path script with Python `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=r'C:/Users/Jsiem/AppData/Local/Temp')`.
2. Convert the printed native path using `cygpath -u`; execute it with Bash; remove that exact mapped path even if the build/test fails.
3. In the script, use the exact issue worktree and print:
   - repository path, branch, local `HEAD`, and `git ls-remote` branch head;
   - clean/dirty status;
   - `git diff --check HEAD~1..HEAD -- <all changed paths>`.
4. Set a native Windows client-data value when UOContent tests need it:
   `MODERNUO_TEST_DATA_DIR='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic'`.
5. Run a solution build with `MSBUILDDISABLENODEREUSE=1` and `-m:1`, then the focused changed-behavior test filter with `--no-build --no-restore`.
6. Make this terminal action the last tool call before reporting. Describe the result as **fresh ad-hoc/focused verification**, not CI green or broad-suite green.

## Example test selection

For a new extended weapon property, include both its new test class and shared-container regression class, for example:

```bash
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter 'FullyQualifiedName~NewPropertyTests|FullyQualifiedName~ExtendedWeaponAttributesTests' \
  --no-build --no-restore --nologo --verbosity minimal \
  --logger 'console;verbosity=minimal'
```

This validates storage/serialization alongside the feature-specific behavior and avoids falsely relying only on an isolated formula test.
