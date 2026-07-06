# UOContent Data Copy and Focused Tests

Session-derived pitfall from adding `SaWeaponAttributesTests` under `Projects/UOContent.Tests`.

## Symptom

A focused test run can fail before any test body executes:

```text
System.NullReferenceException
  at Server.AOS.DisableStatInfluences()
  at Server.SkillsInfo.Configure()
  at Server.Tests.TestServerInitializer.Initialize()
```

In that case, the fixture likely reached `SkillsInfo.Configure()` while `SkillInfo.Table` was null because the test output did not contain `Data/skills.json`.

## What to check

For the `UOContent.Tests` output folder, verify the data copy happened:

```bash
test -f Projects/UOContent.Tests/bin/Debug/net10.0/win-x64/Data/skills.json
```

If it is missing, do not debug the gameplay test yet; fix the harness output first.

## Reliable recovery

Run a solution build so the data-copy target has populated the test output, then rerun the focused filter:

```bash
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1

dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~<TestClassName>" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

Report the first failed run as a fixture/data-copy blocker, not as evidence about the product behavior under test. Once the solution build copies `Data/skills.json`, rerun the same focused test before changing production code.
