# Hermes Guard Verification with Locked Distribution DLLs

Use this when the Hermes post-edit guard asks for fresh verification on a committed PR branch, but a normal `dotnet build` is blocked by a running ModernUO process locking files under `Distribution/` (for example `Distribution/Logger.dll`).

## Symptom

A guard script that builds `Projects/UOContent.Tests/UOContent.Tests.csproj` fails during copy-to-Distribution:

```text
MSB3027 / MSB3021: ... Distribution/Logger.dll ... is being used by another process
Die Datei wird durch "ModernUO (<pid>)" gesperrt.
```

Do not kill the user's running server unless explicitly asked. Keep the verification isolated.

## Pattern

1. Create the required temp script with `tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir='C:/Users/Jsiem/AppData/Local/Temp')`.
2. Create a temp build output directory with `tempfile.mkdtemp(prefix='hermes-verify-out-', dir=temp_dir)`.
3. In the script:
   - `cd` into the real worktree.
   - Print repo, branch, local head, remote head, and status.
   - Run `git diff --check HEAD~1..HEAD -- <changed paths>` for committed PR branches.
   - Build with isolated output:
     ```bash
     MSBUILDDISABLENODEREUSE=1 dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj \
       --nologo --verbosity quiet -m:1 \
       -p:OutDir="$build_out/" -p:PublishDir="$build_out/"
     ```
   - Copy test `Data/` into the isolated output before `dotnet test`; an isolated `OutDir` can otherwise miss `Data/skills.json` and fail in `SkillsInfo.Configure()` / `AOS.DisableStatInfluences()`:
     ```bash
     python - "$build_out" <<'PY'
     import pathlib, shutil, sys
     repo = pathlib.Path.cwd()
     out = pathlib.Path(sys.argv[1])
     src = repo / 'Projects' / 'UOContent.Tests' / 'bin' / 'Debug' / 'net10.0' / 'win-x64' / 'Data'
     dst = out / 'Data'
     if not src.exists():
         raise SystemExit(f'missing source test data: {src}')
     shutil.copytree(src, dst, dirs_exist_ok=True)
     print(f'copied {src} -> {dst}')
     PY
     ```
   - Run the focused tests with the same `OutDir`/`PublishDir` and `--no-build --no-restore`.
4. Cleanup:
   - Remove the temp `hermes-verify-*.sh` script.
   - Remove the temp `hermes-verify-out-*` directory.
   - Remove test scratch output such as `Distribution/Data/Pathfinding/` if the focused UOContent fixture recreated it and it is untracked.
5. Report the result explicitly as **ad-hoc/focused verification**, not broad suite green unless the script actually ran the broad suite.

## Pitfalls

- `dotnet test` with an isolated `OutDir` but without copied `Data/` can fail before assertions with `NullReferenceException` in `AOS.DisableStatInfluences()`.
- The first failed temp script can leave an old `hermes-verify-*.sh`; check and remove stale verification scripts when cleaning up.
- If `git status` shows only test scratch files after a passing guard run, remove only those known scratch paths; do not reset the user's worktree.
