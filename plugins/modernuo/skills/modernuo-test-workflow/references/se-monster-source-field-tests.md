# Samurai Empire monster source-field tests

Use this reference for RebirthUO `[SE-MISS-MON-*]` issue batches where the issue is a source/test gap rather than a confirmed gameplay-code bug.

## Pattern

- Keep each issue in its own worktree/branch/PR.
- Prefer test-only coverage when the creature implementation already exists and the issue asks for source rows, stat/ability tests, or SourceLocked documentation.
- Do not create `dev-docs/eras/samurai-empire.md` just because an issue references it. On `origin/live` that ledger may be absent; treat the path as issue-supplied unless the implementation branch actually contains it.
- Use a focused test class under `Projects/UOContent.Tests/Tests/Mobiles/Monsters/SE/` named for the monster or behavior.
- Add an in-test field coverage row with statuses such as `SourceBacked`, `SourceConflict`, `SourceLocked`, `RepoBacked`, and `RuntimeBlocked` so unsupported OSI-era values are explicit instead of guessed.
- Construct real creatures with `using var random = new PredictableRandom(seed); NPCSpeeds.Configure(); var creature = new MonsterType();` when asserting constructor-set stats, body, taming, resistances, abilities, and loot-policy flags.
- Use `[Collection("Sequential UOContent Tests")]` for these tests because they instantiate real UOContent mobiles/items and touch process-global test fixtures.
- Count current spawn evidence by parsing JSON under `Distribution/Data/Spawns/shared/tokuno/` (and other facets when needed, e.g. `shared/malas/Citadel.json` for Elite Ninja). Treat this as repo-backed spawn-package evidence, not OSI density proof.

## Pitfalls found in the #112-#129 batch

- `DeathwatchBeetle` and `DeathwatchBeetleHatchling` use lowercase `w` class names despite legacy `TypeAlias("Server.Mobiles.DeathWatch...")` values. Verify class names before writing test types.
- A non-tame creature can still inherit `ControlSlots == 1`. Do not assume `ControlSlots == 0` solely from `Tamable == false`; document the repo-backed value unless a source-backed code fix is explicitly in scope.
- `PredictableRandom` uses a fixed clamped value, not a sequence. Pick seeds deliberately for ability chance tests: e.g. `0` makes `Utility.RandomDouble()` succeed for a `< 0.2` Yamandon poison-cloud chance, while `10` produces a failing chance path.
- For poison assertions, call `PoisonKinds.Configure()` when `Poison.Lethal` or other poison singletons may be null.
- Yamandon poison-cloud tests can invoke the private `DoCounter` via reflection to prove current behavior without refactoring production code: 20% trigger, bard-provoked creature exclusion, controlled/summoned attacker retargeting to master within 18 tiles, 8-tile area, 20-25 direct poison damage, and `Poison.Lethal`.
- For area tests, move mobiles into the actual map (`MoveToWorld`) and use controlled creatures as victims because Yamandon filters to players or controlled/summoned/team-opposed creatures.

## Verification pattern

For each issue worktree:

```bash
export MSBUILDDISABLENODEREUSE=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
cd "$worktree"
git diff --check origin/live...HEAD -- Projects/UOContent.Tests/Tests/Mobiles/Monsters/SE/<TestClass>.cs
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~<TestClass>" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

If Hermes' post-edit guard still reports missing evidence after the PRs are opened, run the same checks from a temporary `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script in the exact edited worktrees and report it as **ad-hoc/focused verification**, not broad suite green.