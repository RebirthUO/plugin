# ModernUO Testing Patterns

## Fixture ownership

- Use the owning test project's existing fixture and collection.
- Entity/content tests often need normal initialization, map/context, parent
  ownership, and inventory/container setup; prove prerequisites instead of
  accepting zero/default global values.
- Initialize required registries through the same supported configuration seam
  used by the repository and restore prior state in `finally`/disposal.
- Use deterministic clock and RNG seams. Do not sleep, drive the real timer
  wheel, or patch production rules solely for a test.

## Global state

Serialize tests that mutate expansion/profile, registries, maps, timers, skills,
network state, or live entities. Capture old values and restore them even after
assertion failure. Delete spawned entities and detach event subscriptions.

## Data and generated output

- Build first when tests consume copied distribution/generated output.
- Resolve configured client/server data through repository settings or explicit
  test configuration; do not hard-code workstation paths.
- A missing data file that fails before the assertion is an environment or
  fixture blocker. Report the missing path/config and do not reinterpret it as a
  feature regression.

## Worktrees

- Confirm registered worktree root, branch, HEAD, base, and status before each
  command.
- Run commands with the worktree as the actual working directory.
- Never change git configuration to hide file-mode or path problems. Diagnose
  and report the mismatch.
- Keep durable logs for long or multi-worktree runs and continue independent
  worktrees after one failure.

## Evidence labels

| Label | Meaning |
|---|---|
| Focused | Exact class/namespace/behavior filter |
| Adjacent | Neighboring tests for a shared hook |
| Owning project | Full test project that owns the change |
| Broad | Wider solution or repository test set |
| Baseline | Same failure reproduced without the change |
| Environment-blocked | Bootstrap/data/tooling failed before behavior assertion |
| CI | Remote CI result read from the authoritative provider |

Always report command, project/filter, passed/failed/skipped denominator, and
revision. Rerun focused tests after the final edit.
> Before reporting a run, verify that every command has its repository revision,
> test denominator, status, and any environment limitation. Missing evidence is
> a `BLOCKED` result, not a passing test claim.
