---
name: modernuo-test-workflow
description: Use when writing, modifying, validating, or preparing PRs for ModernUO/RebirthUO xUnit tests, especially UOContent tests that instantiate game entities, isolated issue branches/worktrees, focused `dotnet test` validation, and PR readiness checks.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, rebirthuo, tests, xunit, validation, pr-readiness]
    related_skills:
      - uo-modernuo-workflow
      - modernuo-code-audit
      - modernuo-content-patterns
      - modernuo-serialization
      - modernuo-threading
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-regression-testing
      - modernuo-test-naming
---

# ModernUO Test Workflow

Use this skill for RebirthUO/ModernUO test-only implementation work, especially batches where each GitHub issue must become a separate branch and PR.

## Core Workflow

1. Start from the requested base branch and fetch/pull before branching.
2. Use one branch/worktree per issue when the user asks for isolated PRs.
3. Put test coverage in the project that owns the behavior (`Projects/UOContent.Tests` for content systems, `Projects/Server.Tests` for engine-level behavior).
4. Validate in the actual worktree for the issue, not from the main repo or a sibling directory.
5. Only commit, push, and open a PR after real `diff --check`, build, and focused test output for that branch.

## Windows/MSYS Worktree Path Pitfall

On this Windows host the shell is MSYS/bash. Prefer native-style paths such as `C:/Users/...` when passing paths to `git worktree add`. Verify with `git worktree list --porcelain`, `git -C <worktree> rev-parse --show-toplevel`, and `git -C <worktree> status --short --untracked-files=all` before validating. If a path accidentally becomes `C:/c/Users/...`, files written to `C:/Users/...` are not in the Git worktree even though the paths look similar.

Validation scripts must `cd "$worktree"` or use the worktree as the command working directory. A loop that builds from the main repo can produce false PASS results for misplaced or untracked files.

## UOContent Fixture Rules

Use `[Collection("Sequential UOContent Tests")]` for tests that depend on process-global UOContent initialization, including tests that instantiate real `Item`, `BaseArmor`, `BaseClothing`, `BaseWeapon`, `Mobile`, or content systems, or use `ComponentVerification`, `MultiData`, `TileData`, `ServerConfiguration`, `World`, `Timer`, or `DecayScheduler`.

Without the collection fixture, tests can fail before assertions with setup errors such as `DecayScheduler.Unregister` / `Item.UpdateDecayRegistration` null references, `ServerConfiguration.DataDirectories` null references, or false roof/component validity failures because component tables were not initialized.

## Focused Validation Pattern

When a broad xUnit suite fails, parse TRX files and then rerun each failed cluster with `--filter` before proposing a fix. If a cluster is red only in the broad run but green in focused runs, suspect process-global test state (for UOContent: `Core.Expansion`, `Def*.CraftSystem`, `Recipe.Recipes`, `World`, `Timer`, `NetState`) rather than product behavior. Keep the issue/PR diagnosis separate for independently red focused tests.

## RebirthUO Agent Validation Gate

For RebirthUO test or PR work, agent orchestration must be more intensive when changes touch process-global state (`Core.Expansion`, `Def*.CraftSystem`, `Recipe.Recipes`, `World`, `Timer`, `NetState`) or broad test behavior. Focused tests alone are not sufficient to report completion as suite-green. Agents must run a broad local suite (`dotnet test ModernUO.slnx --no-build --no-restore` or the owning broad test project) or perform a clean baseline comparison when the broad suite is blocked. Broad failures must be clustered from TRX/log output, each failed cluster must get a focused rerun, and reports/PR bodies must explicitly distinguish focused verification, broad-suite status, baseline failures, and remaining blockers.

```bash
cd "$worktree"
git status --short --untracked-files=all
git add -N Projects/UOContent.Tests/Tests/.../*.cs
git diff --check --cached
git diff --check
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~<TestClassName>" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

## Hermes Post-Edit Verification Guard

When Hermes reports that edited files lack fresh passing verification evidence, create a focused temporary script under `C:/Users/Jsiem/AppData/Local/Temp` with an OS-safe `tempfile` path and a `hermes-verify-` filename prefix. The script must `cd` into the actual worktree, print repo/branch/head, run the changed-path whitespace check, build the owning test project or solution, and run the focused `dotnet test` filters for the changed behavior. Execute the script, remove it afterward when possible, and report the result explicitly as **ad-hoc/focused verification**, not as broad suite green unless the script actually ran the broad suite.

If the changed PR branch is already committed/pushed and the worktree is clean, the guard still needs a fresh script run. In that case, validate the committed changed paths with `git diff --check HEAD~1..HEAD -- <changed paths>` instead of relying on an empty worktree diff, print local and remote heads, and include lightweight sanity checks for any edited temporary PR-body/review markdown files. See `references/hermes-post-edit-guard-committed-pr-branches.md` for a reusable script shape and reporting checklist.

If the PRs have already been merged and the durable target is now `origin/live`, do **not** use `git reset --hard` in an existing user worktree to satisfy the guard. Create a temporary detached verification worktree under `C:/Users/Jsiem/AppData/Local/Temp` from `origin/live`, run `git diff --check HEAD~N..HEAD -- <changed paths>`, build the owning test project, run the focused test filters, then remove both the temp worktree and the `hermes-verify-*` script. Report this explicitly as ad-hoc/focused verification on `origin/live`, not full-suite green. See `references/hermes-post-merge-live-verification.md`.

Example shape:

```bash
python - <<'PY'
import os, stat, tempfile
repo = r'C:/Users/Jsiem/Documents/GitHub/RebirthUO/live-service'
temp_dir = r'C:/Users/Jsiem/AppData/Local/Temp'
fd, path = tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=temp_dir, text=True)
script = f'''#!/usr/bin/env bash
set -euo pipefail
cd {repo!r}
echo "repo=$(pwd)"
echo "branch=$(git branch --show-current)"
echo "head=$(git rev-parse --short HEAD)"
git diff --check -- Projects/Server.Tests/Tests/Buffers/ValueStringBuilderTests.cs
MSBUILDDISABLENODEREUSE=1 dotnet build Projects/Server.Tests/Server.Tests.csproj --nologo --verbosity quiet -m:1
dotnet test Projects/Server.Tests/Server.Tests.csproj \
  --filter "FullyQualifiedName~ValueStringBuilderTests" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
'''
with os.fdopen(fd, 'w', newline='\n') as f:
    f.write(script)
os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
print(path)
PY
```

Run and clean up with MSYS path conversion:

```bash
script='C:\Users\Jsiem\AppData\Local\Temp\hermes-verify-xxxx.sh'
bash "$(cygpath -u "$script")"
status=$?
rm -f "$(cygpath -u "$script")"
exit $status
```

## Rider Test Discovery Triage

When Rider shows only a subset of `UOContent.Tests` (for example only newly added/custom tests), first compare Rider against CLI discovery with `dotnet test ... --list-tests`. Keep test-project boundaries explicit: `UOContent.Tests`, `Server.Tests`, and `RUOContent.Tests` are separate assemblies, and a `ProjectReference` to `Server.Tests` for fixtures/helpers does not mean a `UOContent.Tests` run should list every `Server.Tests` test. See `references/rider-test-discovery-triage.md` for the full checklist covering Rider run scopes, Unit Tests window filters, stale caches, `.slnx` import, and SDK/adapter mismatches.

## Ninjitsu / Special-Move UOContent Tests

When adding Samurai Empire Ninjitsu special-move coverage (Focus Attack, Backstab, Shadowjump, Surprise Attack, Ki Attack, Death Strike), prefer small focused tests over full target/combat-pipeline simulation unless the issue explicitly requires a live swing. See `references/ninjitsu-special-move-test-patterns.md` for concrete patterns from RebirthUO parity work.

Key rules:

- Initialize `SkillInfo.Table` before accessing named skill properties in lightweight `Mobile` fixtures, but do not blindly re-run `SkillsInfo.Configure()` inside a broad suite: it resets `SkillInfo.Table` and can drop skill callbacks used by later tests. Prefer a guarded helper (`if (SkillInfo.Table.Length == 0) SkillsInfo.Configure();`) and, when the test may drive `Mobile.CheckSkill(...)` or stat regen side effects, also call `SkillCheck.Configure()`, `SkillCheck.Initialize()`, and guard `AntiMacroSystem.Configure()` when `AntiMacroSystem.Settings` is null.
- Use `[Collection("Sequential UOContent Tests")]` for tests that mutate global state such as `Core.Expansion`, `SkillsInfo`, `SkillCheck`, `SpecialMove.Table`, `Tracking` state, or timer/action locks.
- For `Hidden`/stealth tests, set `Hidden = true` before setting `AllowedStealthSteps`; `OnHiddenChanged()` resets stealth steps.
- Initialize stats before mana assertions (`InitStats(100, 100, 100)`), otherwise `Mana`/`ManaMax`-sensitive checks can silently clamp to zero.
- For tracking/stalking distance bonuses, `Tracking.AddInfo(attacker, defender)` captures the defender's current location; move the defender after capture to create a deterministic distance bonus, then call `Tracking.ClearTrackingInfo(attacker)` in cleanup.
- If a broad UOContent/Tokuno filter fails with `Path "Server.dll" is not an absolute path` from `TestServerInitializer` / `AssemblyHandler.LoadAssemblies(["Server.dll", "UOContent.dll"])`, treat it as a harness/bootstrap blocker and do **not** report broad-suite green. Report focused validation separately and label the broad attempt as blocked.

## Pitfalls When Writing Broad UOContent Tests

- **Craft system globals are era-sensitive and process-global.** `DefBlacksmithy`, `DefCarpentry`, `DefTinkering`, etc. keep static `CraftSystem` instances, and `Recipe.Recipes` is a static global recipe-id dictionary. Broad `UOContent.Tests` runs can fail even when focused tests pass if one test initializes a `Def*` system under `Expansion.EJ`/ML and a later SE test only checks whether an item exists before asserting SE metadata. Reinitializing a recipe-bearing `Def*` system under restored EJ in `finally` can also throw `Attempting to create recipe with preexisting ID.` in later tests. For SE craft metadata tests, initialize/assert under the intended era regardless of prior item presence, and avoid broad-run cleanup that rebuilds ML/EJ recipe registries unless the test also snapshots/clears `Recipe.Recipes` safely.
- **Spellweaving positive-cast tests need an ML-capable NetState.** `ArcanistSpell.CheckExpansion()` rejects `PlayerMobile` casters unless `caster.NetState?.SupportsExpansion(Expansion.ML) == true`. If a test manually drives `OnBeginCast()` / `BeginSequence()` / `Target()` and expects summons or effects (for example Nature's Fury followers), attach a test client such as `using var ns = AttachClient(caster, "5.0.2b")` and detach it in `finally`.

## Pitfalls When Writing Theory Tests That Instantiate Entities

- **Hardcoded decimal/date strings need explicit culture.** RebirthUO developer machines may run with comma-decimal cultures (German UI/locale), so assertions like `"3.14"` against `ValueStringBuilder`/interpolated formatting can fail with actual `"3,14"`. If the expected string is invariant, scope the test with `CultureInfo.CurrentCulture = CultureInfo.InvariantCulture` and restore it in `Dispose`; if the behavior should follow BCL/default formatting, add a comma-decimal culture test to prove current-culture semantics instead of changing production code to invariant.

## Pitfalls When Writing Theory Tests That Instantiate Entities

- **`[MemberData]` source shape.** xUnit requires `IEnumerable<object[]>`, not a raw `Type[]`. Using `public static Type[] SeMonsterTypes { get; } = { ... }` triggers analyzer `xUnit1019`. Wrap with `.Select(t => new object[] { t })`.
- **Record primary-ctor params keep their declared casing.** Pick PascalCase at write time so named-argument call sites match property access. A record `(int allowedBodies, ...)` exposes `.allowedBodies` (lowercase) — `Assert.Equal(row.AllowedBodies, ...)` and `new MonsterRow(allowedBodies: ...)` will not line up; the compiler will fail with CS1739.
- **C# class name ≠ file name for legacy aliases.** Verify with `grep "public partial class"` before writing `typeof(...)`. `Projects/UOContent/Mobiles/Monsters/SE/DeathWatchBeetle.cs` declares `class DeathwatchBeetle` (lowercase `w`) with `[TypeAlias("Server.Mobiles.DeathWatchBeetle")]` for legacy client compatibility. Same for `DeathwatchBeetleHatchling`.
- **`Activator.CreateInstance` vs `RuntimeHelpers.GetUninitializedObject`.** Use `Activator.CreateInstance` inside `using var random = new PredictableRandom(seed)` + `NPCSpeeds.Configure()` for any test that touches ctor-set fields (Str/Dex/Int, Hits, Body, Tamable, Resistances). Use `GetUninitializedObject` ONLY for static-metadata-only checks (e.g. `GetMonsterAbilities()`).
- **`PredictableRandom` returns a clamped fixed value, not a sequence.** All `Utility.Random(N)` calls in a single ctor return the same clamped result; `Utility.RandomDouble()` returns `seed/20.0` clamped to `[0,1]`. If a single class fails with an out-of-range value while siblings pass (Ronin EnergyResistance = 88 instead of 55-75), the failure is RNG-state-ordering specific to that class's ctor (e.g. `UpdateResistances`, follow-up `OnXxx` callbacks). Do not loosen `InRange` globally; extract the failing class to a dedicated `[Fact]` with `Assert.Equal` + `// SourceLocked` marker.
- **Default `CorpseName` is `null`.** `BaseCreature.CorpseName` returns `null` unless overridden. Tests must handle `null` (e.g. for `EliteNinja` which does not override it).
- **`FireBeetle` is `BaseMount`.** Body is set via `BaseMount(0xA9, 0x3E95, AIType.AI_Melee)` in the base ctor, so `Activator.CreateInstance(typeof(FireBeetle))` yields `Body == 0xA9`.

## Support Files

- `references/se-monster-source-field-tests.md` — pattern for Samurai Empire `[SE-MISS-MON-*]` monster source-field tests: SourceLocked/SourceConflict rows, real creature construction, spawn JSON counting, and batch-discipline pitfalls.
- `references/rebirthuo-isolated-test-branches.md` — session-derived details on MSYS worktree false-greens and UOContent fixture symptoms.
- `references/xunit-and-entity-instantiation-gotchas.md` — concrete code-level xUnit pitfalls: `[MemberData]` source shape, record param naming, `DeathwatchBeetle` lowercase-`w` trap, `PredictableRandom` clamp behavior and the Ronin single-class RNG ordering failure, `Activator.CreateInstance` vs `RuntimeHelpers.GetUninitializedObject`, `FireBeetle` `BaseMount` body, `CorpseName == null` default.
- `references/ninjitsu-special-move-test-patterns.md` — session-derived patterns for Focus Attack/Backstab/Shadowjump/Surprise Attack tests: `SkillsInfo.Configure`, `SkillCheck.Initialize`, stealth-step ordering, tracking one-shot bonus setup, special-move reset, timer-duration test seams, and the `Server.dll` relative-path broad-filter blocker.