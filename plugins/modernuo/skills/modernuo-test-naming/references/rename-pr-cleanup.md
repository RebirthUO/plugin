# Rename-Only Test Cleanup PR Workflow

Use this reference when normalizing test names in a ModernUO-based repository
after generated branches or AI-assisted work introduced noisy prefixes.

## Scope discipline

- Make rename-only changes: file names, class names, test method names, and direct references only.
- Do not change assertions, fixtures, setup, production code, or test behavior while cleaning names.
- Keep domain names when they are the tested object, e.g. `MLQuest*`, `MLPeerlessArtifactsTests`, source-reference hubs, or real helper/family names such as `MLSetArmor`.
- Remove era/batch labels when they are only context: `MondainsLegacy...`, `SamuraiEmpire...`, `Coverage`, `Smoke`, `Issue*`, `Publish*`, `Codex`, etc.

## Clean worktree pattern

1. Discover the configured base branch from repository instructions, the requested PR base, or the current tracked upstream before creating a separate cleanup worktree; do not assume `origin/live`.
2. On Windows/MSYS worktrees, file mode changes can appear as false dirty state (`100755 => 100644`). Use `git -c core.filemode=false status/diff/add` for inspection and staging rather than committing mode-only noise.
3. Stage only the test project paths involved, for example:

```bash
git -c core.filemode=false add -A Projects/UOContent.Tests
```

4. Before committing, verify that no non-test files are staged:

```bash
git -c core.filemode=false diff --cached --name-only | grep -v '^Projects/UOContent.Tests/' || true
```

On PowerShell, replace the pipeline with `git -c core.filemode=false diff --cached
--name-only | Where-Object { $_ -notlike 'Projects/UOContent.Tests/*' }`.

## Prefix verification script

After edits, scan file stems, class names, and xUnit methods. Pass the owning test root as `<test-root>`; allow known domain cases such as source-reference tests and `MLSetArmorTests`. The example recognizes common C# xUnit visibility forms, but inspect local conventions before treating a zero result as complete.

Run the bundled scan from the consuming repository root; this works unchanged
in Bash, PowerShell, and other Python-capable shells:

```text
python <skill-path>/references/test-naming-prefix-scan.py <test-root>
```

Expected for a completed cleanup: `0` actionable findings.

## Validation

- Run `git -c core.filemode=false diff --cached --check` before commit.
- Run `dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1`.
- Run targeted renamed-class test filters in batches. Prefer targeted filters over relying only on a full suite when the repository has known static-state/order-sensitive tests.
- If an exploratory full `UOContent.Tests` run fails in unrelated order-sensitive static state after many passes, report it explicitly as exploratory and do not mix behavior fixes into the rename-only PR.

## PR completion

Before any commit, push, PR creation, merge, or branch deletion, resolve the
exact repository from the consuming repository's applicable `AGENTS.md`. If
that file does not name the repository, return `BLOCKED`; never infer it from
the cwd, remotes, organization, issue number, or neighboring project. If the
user asked for the PR to change or merge, local validation is not completion.
Only after that exact resolution, commit, push, create the PR, merge to the
requested base, delete the branch, and verify the PR state and base head.
