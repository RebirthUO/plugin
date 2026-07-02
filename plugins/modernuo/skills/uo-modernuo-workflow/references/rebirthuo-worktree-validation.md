# RebirthUO Multi-Worktree Validation

Use this reference when validating multiple RebirthUO/ModernUO issue worktrees in one run, especially when each worktree needs `git diff --cached --check`, `dotnet build`, and focused/broad xUnit filters.

## Durable validation pattern

1. Write a reusable shell script instead of hand-running long command chains.
2. Create a timestamped log directory and write one log per worktree plus a `summary.tsv`.
3. Normalize Windows/MSYS worktree file-mode noise before judging dirtiness:
   ```bash
   git config core.filemode false
   git status --short --branch
   ```
   Fresh RebirthUO worktrees on Windows can show mode-only changes for tracked files when `core.filemode=true`; clear that local setting before staging or reporting unrelated dirtiness.
4. Guard against MSYS path alias mistakes before writing or validating files. Prefer native `C:/Users/...` paths when passing paths to `git worktree add` from Git Bash/MSYS. A path like `/c/Users/...` can be recorded by Git as `C:/c/Users/...` in this environment, while file tools using `C:\Users\...` write elsewhere. Before trusting validation, confirm the edited file is inside the registered worktree:
   ```bash
   git worktree list --porcelain | grep -A3 'issue-<n>'
   git -C '<registered-worktree-path>' rev-parse --show-toplevel
   git -C '<registered-worktree-path>' status --short --untracked-files=all -- '<edited-file>'
   ```
   If Git shows no changes but the file exists, search for duplicate non-git directories and copy the file into the registered worktree before validating.
5. Run build/test commands from the worktree root, not only with a path variable nearby. Use `(cd "$wt" && dotnet build ModernUO.slnx ...)` or `workdir=$wt`; otherwise a loop can appear to validate every branch while actually building the parent checkout.
6. Export stable build environment flags:
   ```bash
   export MSBUILDDISABLENODEREUSE=1
   export DOTNET_CLI_TELEMETRY_OPTOUT=1
   export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
   ```
5. Build with a single MSBuild worker when running many worktrees sequentially:
   ```bash
   dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
   ```
5. After a successful build, run tests with no build/restore:
   ```bash
   dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
     --filter "FullyQualifiedName~<TestClassOrPattern>" \
     --no-build --no-restore --nologo --verbosity quiet \
     --logger "console;verbosity=minimal"
   ```
6. Skip tests for a worktree when its build fails; report the build failure as the root validation blocker for that worktree.
7. Keep going after failures so the final report covers every worktree.

## Handling killed or interrupted validation

If a background validation process is killed or times out:

- Inspect the process log first to identify the last completed worktree and step.
- Preserve the partial result as evidence, but rerun with durable per-worktree logs before reporting final status.
- If MSBuild child nodes terminate during process shutdown, do not treat that as a code failure by itself; rerun with `MSBUILDDISABLENODEREUSE=1` and `-m:1` before concluding.

## Reporting format

Report:

- Background process/session id if applicable.
- Log directory and `summary.tsv` path.
- One row per issue/worktree: build result, focused test count, broad test count, and failures.
- Any tests intentionally not run and why.
- For broad-suite failures, whether the same failures reproduce in a clean detached `origin/<base>` worktree. If they do, label them baseline failures and keep the PR focused on the issue-scoped build/focused-test evidence.

Prefer a compact table over pasting full logs. Point to the durable log files for detail.