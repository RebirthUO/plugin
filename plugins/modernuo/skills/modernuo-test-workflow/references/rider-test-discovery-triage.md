# Rider test discovery triage for RebirthUO/ModernUO

Use this reference when Rider shows only a subset of tests (for example only newly added/custom tests) while working with `Projects/UOContent.Tests`.

## Durable observations from RebirthUO

- `ModernUO.slnx` contains separate test projects: `Projects/Server.Tests/Server.Tests.csproj`, `Projects/UOContent.Tests/UOContent.Tests.csproj`, and `Projects/RUOContent.Tests/RUOContent.Tests.csproj`.
- Starting `UOContent.Tests` in Rider should be treated as a single-test-assembly/project scope. It should not be assumed to show tests from `Server.Tests` just because `UOContent.Tests.csproj` references `Server.Tests.csproj` for helpers/fixtures.
- `UOContent.Tests.csproj` is SDK-style and normally includes `Tests/**/*.cs` by default unless there are explicit `Compile Remove`, `EnableDefaultCompileItems=false`, `.runsettings`, or Rider filters.
- If a repo inspection shows many `[Fact]`/`[Theory]` attributes under `Projects/UOContent.Tests/Tests/**` but Rider shows only a few tests, suspect Rider run scope, Unit Tests window filters, stale cache, `.slnx` import, or SDK/test-adapter mismatch before suspecting missing test code.

## CLI truth loop

From the repo root, compare Rider against VSTest/xUnit discovery:

```bash
dotnet build ModernUO.slnx --nologo --verbosity minimal -m:1

dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --list-tests \
  --no-build --no-restore \
  --nologo --verbosity minimal \
  --logger "console;verbosity=minimal"

dotnet test Projects/Server.Tests/Server.Tests.csproj \
  --list-tests \
  --no-build --no-restore \
  --nologo --verbosity minimal \
  --logger "console;verbosity=minimal"

dotnet test ModernUO.slnx \
  --list-tests \
  --no-build --no-restore \
  --nologo --verbosity minimal \
  --logger "console;verbosity=minimal"
```

Interpretation:

- CLI lists many `UOContent.Tests` tests but Rider does not: Rider configuration/cache/import problem.
- CLI `UOContent.Tests` lists only the custom tests too: investigate build/project/worktree state (`git status`, removed files, wrong worktree, stale branch).
- CLI `Server.Tests` lists the expected “original tests” separately: use `Server.Tests` or solution-wide run; `UOContent.Tests` alone is the wrong scope for those tests.

## Rider checks

In Rider:

1. Open the solution file (`ModernUO.slnx`), not only a subfolder or one `.csproj`.
2. Verify Solution Explorer shows all test projects loaded.
3. Create a fresh run configuration scoped to project `Projects/UOContent.Tests/UOContent.Tests.csproj` with no class/namespace/FullyQualifiedName/test-case filter.
4. Start tests from the project node, not from a custom-test file or folder.
5. Clear Unit Tests tool window search/status/session filters; group by project or namespace.
6. Reload all projects and refresh Unit Tests discovery.
7. If CLI and Rider still disagree, invalidate Rider caches and compare Rider `.NET CLI executable path` with `dotnet --info`.
8. If `.slnx` support is suspect in the installed Rider version, create a temporary `.sln` for diagnosis and do not commit it unless the user explicitly wants it.
