# Ad-hoc Focused Verification

Use this when the workspace or desktop verification guard says evidence is stale/unverified after a code or test edit. This supplements, but does not replace, normal project validation.

## Procedure

1. Use Python `tempfile.mkstemp(prefix="hermes-verify-", suffix=".sh", dir=r"C:\Users\<user>\AppData\Local\Temp")`; do not hand-name a temp file.
2. Write a short MSYS/bash script that exports the repository's required test-data variables, builds the owning test project, then runs the narrow filter covering the changed behavior.
3. From Python, invoke it through `hermes_tools.terminal` as `bash "$(cygpath -u '<native-temp-path>')"` with the implementation worktree as `workdir`.
4. Capture exit code and the complete focused result. Remove the script in `finally`, and report cleanup failure if removal fails.
5. Call the result **fresh ad-hoc verification**. Do not call it full-suite green unless the broad suite was separately run and passed.

## RebirthUO/ModernUO template

```bash
#!/usr/bin/env bash
set -o pipefail
export MODERNUO_TEST_DATA_DIR='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic'
export MODERNUO_CLIENT_PATH='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic'
export MSBUILDDISABLENODEREUSE=1

dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj --nologo --verbosity quiet -m:1 && \
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter 'FullyQualifiedName~<ChangedTestClass>|FullyQualifiedName~<RelatedRegressionTests>' \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger 'console;verbosity=minimal'
```

Adjust the test project, filter, and client-data path to the active worktree; never commit the temporary script.