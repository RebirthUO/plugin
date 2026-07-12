---
name: modernuo-issue-implement
description: Use when the user explicitly asks to implement a GitHub issue only in https://github.com/RebirthUO/ModernUO. Validate that exact repository and the push remote before reading the issue, creating a branch, committing, pushing, or opening a pull request; reject all other repositories, forks, and lookalikes.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [ModernUO, GitHub, Testing, PullRequests]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: implement
    workflow_tier: direct-modernuo
---
# ModernUO Implement Issue

## Redirect to Canonical Skill

Unless the user explicitly names this skill, load **`rebirthuo-implement`** first. Use this skill only when the issue lives directly in `RebirthUO/ModernUO` without a linked rebirthuo intake ticket and the user explicitly requests the direct-modernuo implementation path.

## Mandatory Repository Gate (Overrides All Later Examples)

This explicit gate overrides every conflicting placeholder, mixed-repository statement, remote-derived target, or historical example later in this skill. Activation is explicit and the only permitted repository is `https://github.com/RebirthUO/ModernUO` (`RebirthUO/ModernUO`).

Before **any issue or pull-request read or write**, require an explicit repository URL or `owner/repository` from the current user request. An issue number alone is insufficient. Never infer the target from cwd, `origin`, another remote, organization membership, repository content, or conversation history. Resolve `gh api repos/RebirthUO/ModernUO` and require successful access plus exact `.full_name == "RebirthUO/ModernUO"` and `.html_url == "https://github.com/RebirthUO/ModernUO"`. The canonical repository currently reports `fork: true`; exact canonical identity is allowed, but every other fork or lookalike is rejected.

If repository context is missing, request it. If it differs or validation fails, stop before reading or mutating issues/PRs. Every `gh issue` and `gh pr` command must pass `-R RebirthUO/ModernUO`; never substitute another repository.

Before creating a branch, committing, pushing, or opening a pull request, verify that the current checkout's push remote resolves to the same exact canonical repository. Do not push to a fork or a remote inferred from the working directory. If the remote cannot be verified as `RebirthUO/ModernUO`, stop before the first Git mutation.


Turn a given ModernUO issue, including one about shared ModernUO-based RebirthUO code context, into an isolated branch, implementation, useful tests, and a pull request only for `RebirthUO/ModernUO`. This skill does not implement a separate RebirthUO-repository issue, merge PRs, bypass review, or make live shard changes; it keeps issue evidence, era/ruleset impact, code, tests, and PR communication tied together. It uses Hermes tools plus existing repo CLIs (`git`, `gh`, `dotnet`) invoked through the `terminal` tool.

## When to Use

- "Implement issue #123" or "take this GitHub issue to PR."
- "Create a branch, fix it, add tests, and open a PR."
- An explicitly identified ModernUO issue URL, issue number, or pasted issue body is the source of truth.
- The issue touches gameplay/content where era, ruleset, PvP/PvM, economy, housing, persistence, or client behavior side effects matter.
- Do not use for issue triage only, code review only, or merging already-open PRs.

## Prerequisites

- Work from the intended ModernUO/RebirthUO repository root in the Hermes workspace.
- `gh auth status` succeeds for the target GitHub repository.
- `dotnet --info` succeeds with the repo's required SDK installed.
- The worktree is clean or every existing change is explicitly in scope.
- If UOContent tests need real client data, set `MODERNUO_TEST_DATA_DIR` to a folder containing UO client data such as `tiledata.mul`; set `MODERNUO_CLIENT_PATH` too when Server tests need client data.
- Know the intended base branch. Use the issue/repo default when the user does not specify one.

## How to Run

1. Load this skill with `skill_view(name='modernuo-issue-implement')` when an issue should become a PR.
2. Use `terminal` to fetch issue details when the issue is a number or URL; use the pasted text directly when the issue is provided inline.
3. Use `read_file` and `search_files` to inspect repository anchors before editing; use `web_extract` for source URLs cited by the issue when available.
4. Use `patch` or `write_file` for code and test changes.
5. Use `terminal` for branch creation, build/test validation, commit, push, PR creation, and PR verification.

## Quick Reference

```bash
gh auth status
git status --short --branch --untracked-files=all
gh issue view <ISSUE> -R RebirthUO/ModernUO --comments --json number,title,body,comments,labels,url
git fetch origin
git switch <base-branch>
git pull --ff-only origin <base-branch>
git switch -c <type>/issue-<number>-<short-slug>
# If any [SerializationGenerator] version changed or migration schema is needed:
dotnet tool restore && dotnet tool run ModernUOSchemaGenerator -- ModernUO.slnx
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/<TestProject>/<TestProject>.csproj --filter "FullyQualifiedName~<FocusedTest>" --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
dotnet test ModernUO.slnx --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
git diff --check
git status --short --untracked-files=all
git add <changed-files>
git commit -m "<type>: <summary>"
git push -u origin HEAD
gh pr create -R RebirthUO/ModernUO --title "<type>: <summary>" --body-file <pr-body-file>
gh pr view -R RebirthUO/ModernUO --json number,url,state,headRefName,baseRefName,statusCheckRollup
gh pr checks -R RebirthUO/ModernUO --watch
```

## Procedure

1. **Capture the issue.** If the input is a GitHub issue number or URL, run:
   ```bash
   gh issue view <ISSUE> -R RebirthUO/ModernUO --comments --json number,title,body,comments,labels,url
   ```
   If the input is pasted text, treat it as the issue body. Extract acceptance criteria, source links, stated non-goals, labels, and any comments that clarify scope. Completion criterion: every requirement and named source is represented in your working notes.

2. **Check sufficiency before coding.** Identify era/ruleset, emulator/repo area, expected player-visible behavior, side effects, and testability. If the issue cites URLs or local docs, gather them with `web_extract`, `browser_navigate`, `read_file`, or `search_files` before implementation. If one detail is missing but the default is obvious, proceed with an explicit assumption; if the missing detail changes the mechanic or safety, ask the user before editing. Completion criterion: the implementation target and non-goals are clear.

3. **Load the narrow domain skills.** Keep this skill as the orchestration layer. Load child skills as needed: `modernuo-code-audit` for `.cs` edits, `modernuo-content-patterns` for items/mobiles/spells/content, `modernuo-serialization` for saved state, `modernuo-timers` and `modernuo-lifecycle-cleanup` for delayed effects, `modernuo-era-expansion` for expansion gates, `modernuo-test-workflow` and `modernuo-regression-testing` for tests, plus specific UO domain skills for combat, loot, crafting, housing, skills, spells, facets, or item properties. Completion criterion: every risky domain has either a loaded skill or an explicit reason it is not relevant.

4. **Start from a safe base.** Verify the worktree and create a branch:
   ```bash
   git status --short --branch --untracked-files=all
   git fetch origin
   git switch <base-branch>
   git pull --ff-only origin <base-branch>
   git switch -c <type>/issue-<number>-<short-slug>
   ```
   Use `fix/` for incorrect behavior, `feat/` for new behavior, and `test/` for test-only coverage.

   If the session is already on an issue branch or the remote PR already exists, do not blindly recreate or rebase it. First verify the branch/remote/PR relationship:
   ```bash
   git status --short --branch --untracked-files=all
   git rev-parse --short HEAD
   git rev-parse --short origin/$(git branch --show-current)
   gh pr list -R RebirthUO/ModernUO --head $(git branch --show-current) --json number,url,state,title,headRefName,baseRefName,statusCheckRollup
   ```
   Treat a clean, matching branch with an open PR as an update/verification task: inspect the existing diff, run fresh validation on the committed branch, and update/report the PR instead of starting over. Completion criterion: the working branch exists, is tied to the intended remote PR or new branch plan, and no unrelated user changes are mixed in.

5. **Inspect before editing.** Use `search_files` to locate existing implementations, tests, serializers, registrations, configs, and similar patterns. Use `read_file` for the exact files you will edit and trace symbols to definitions/usages before changing them. Completion criterion: the chosen edit points match existing repo style and no symbol/API is guessed.

6. **Implement the smallest correct slice.** Use `patch` for existing files and `write_file` for new files. Preserve ModernUO conventions: no unintended engine edits, no accidental era drift, no unsafe threading in game logic, no persistent save mutation for temporary effects, no timer leak, and no loot/economy/PvP/PvM/housing side effect unless the issue requires it. After edits, immediately check `git status --short --untracked-files=all` and `git diff --stat` before building; if an edit tool reports success but the expected files are not in the worktree diff, re-read/verify the actual worktree path and reapply with a direct file write/script rather than continuing on a phantom edit. Completion criterion: the diff maps directly to the issue's acceptance criteria and non-goals and the expected changed paths are visible in git.

7. **Generate useful tests.** Add behavior-level regression tests in the owning test project, not only static registration checks. Prefer tests that prove the player/server-visible outcome, edge cases, era gates, persistence behavior, cleanup, and exploit/safety boundaries. For UOContent entity tests, follow `modernuo-test-workflow` fixture guidance and use `[Collection("Sequential UOContent Tests")]` when process-global state or real entities are involved. Completion criterion: each acceptance criterion has a test or a documented reason it cannot be automated.

8. **Validate locally with honest scope labels.** Run whitespace, generated-schema, build, focused tests, and the broad owning project when feasible:
   ```bash
   git diff --check
   # Required before build/test whenever a [SerializationGenerator] version changed or a migration schema is needed.
   dotnet tool restore && dotnet tool run ModernUOSchemaGenerator -- ModernUO.slnx
   dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
   dotnet test Projects/<TestProject>/<TestProject>.csproj --filter "FullyQualifiedName~<FocusedTest>" --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
   dotnet test ModernUO.slnx --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
   ```
   If broad validation is blocked or shows baseline failures, cluster the failures and label them separately from focused validation. Environment-sensitive broad-suite failures (for example OS culture or missing timezone data) may be reported as blockers/baseline only after the focused and owning project validations prove the issue area green. Completion criterion: real tool output exists for the validation you will claim.

9. **Audit the diff before commit.** Check the branch diff, edited file list, generated tests, PR-facing behavior, and UO side effects. Use `delegate_task` for an independent review when the change is broad or risky. Completion criterion: unrelated files are removed from scope and every changed file has a reason tied to the issue.

10. **Commit and push.** Stage only issue-scoped files:
    ```bash
    git status --short --untracked-files=all
    git add <changed-files>
    git commit -m "<type>: <summary>"
    git push -u origin HEAD
    ```
    Completion criterion: the remote branch contains the validated commit.

11. **Open the PR with domain-first context.** Create a PR body file using these sections: Gameplay problem, Sources / evidence, Behavior change, Why this is correct, Definition of Done, Validation. Include `Closes #<number>` when the PR should close the issue. Then run:
    ```bash
    gh pr create -R RebirthUO/ModernUO --title "<type>: <summary>" --body-file <pr-body-file>
    ```
    On Windows/MSYS, if `gh` rejects an MSYS body-file path, pass a native Windows path, for example with `cygpath -w <pr-body-file>`. Completion criterion: GitHub returns a PR URL.

12. **Verify the published PR.** Run:
    ```bash
    gh pr view -R RebirthUO/ModernUO --json number,url,state,headRefName,baseRefName,statusCheckRollup
    ```
    If checks start, inspect them with `gh pr checks -R RebirthUO/ModernUO` or `gh pr checks -R RebirthUO/ModernUO --watch`. Completion criterion: the final report includes PR URL, branch, commit/push status, validation commands/results, and any remaining CI or broad-suite blocker.

    If Hermes requests fresh verification after the branch is already committed/pushed, do not argue with the guard or merely restate earlier output. Create a temporary `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script, run it against the committed changed paths, print branch/local head/remote head/PR state, run `git diff --check HEAD~1..HEAD -- <changed paths>`, any distribution guard, build, focused tests, and the broad owning project when feasible, then remove the script. Report this explicitly as **ad-hoc verification** rather than CI green or suite-green unless CI/broad suite actually ran.

## Lessons from implementation sessions

- Treat the issue body as the authoritative mechanics contract. Retrieve it into a readable artifact when terminal output is truncated or context is compacted, then preserve explicit policy choices and source conflicts (for example, competing reagent or duration values) in code comments, tests, and the PR rather than silently choosing a value.
- Before any repository read or edit, verify the active Hermes Project/workspace still points at the intended worktree. Another session can silently switch the active project; use absolute worktree paths for `read_file`, `patch`, and `write_file`, and switch back before continuing if needed.
- In an issue worktree, pass absolute worktree paths to `read_file` and `patch` whenever the active Hermes workspace may differ. After any paginated `read_file`, re-read the complete file before a whole-file overwrite or broad patch if the tool warns about partial context.
- Inspect the repository's exact constructor and API signatures before porting an emulator precedent. ServUO constructor shapes and helper names can differ from ModernUO; compile the owning project early, then adapt to the local `BaseCreature`/spell APIs instead of copying unsupported arguments.
- When a shared virtual combat hook such as `BaseWeapon.OnHit` needs an additional per-swing input, trace every override and forwarding call first (melee families, ranged, throwing, and test doubles). Update the full override chain in one edit, preserve a default argument for direct test callers, and build `UOContent` immediately before fixture-level tests. A partial override update neither validates compilation nor proves that the state reaches the normal-hit seam.
- For UOContent fixture tests that exercise map spawning, do not assume arbitrary coordinates are valid land. Derive a test location with `Map.GetAverageZ` and `Map.CanSpawnMobile`, and keep the location outside guarded/house regions so the test proves the intended success path rather than a blocked-location path. First check `TestServerInitializer.TileDataLoaded` and the available client assets: a fixture may have `tiledata.mul` but no `map0.mul`, making terrain/LOS assertions impossible. Keep runtime-state/lifecycle tests on a non-internal test map independent of terrain files, and skip or isolate genuinely map-dependent targeting tests when the required map data is unavailable. Never weaken production visibility/target rules or grant elevated access merely to make a map-dependent test pass.
- For location-restricted summons, validate the target location's region permission explicitly before resource consumption; caster-region spell hooks do not prove target-region safety. Test a real registered restricted region and a real house-region fixture, covering both target-inside and caster-inside cases. A generic outdoor coordinate assertion is a false-positive house test.
- For summon acceptance criteria, add behavior tests for the generated serialization round trip of a durable summon field and for the existing framework's expiry/follower cleanup when feasible. Manual `Delete()` cleanup alone does not prove timed expiry or save compatibility.
- Initialize the owning solution before running `--no-build` focused tests when the fixture depends on generated/copied data. A focused test run against a stale or incompletely initialized output can fail in fixture setup; run the relevant solution/project build first, then run the focused filter and label it focused.
- UOContent tests using `Mobile` do not automatically have a backpack. Build the fixture with `DefaultMobileInit()` plus `AddItem(new Backpack())` before testing backpack-created items, reagents, ownership, or item use; otherwise tests can pass vacuously because item placement fails.
- For direct spell-sequence tests, set both `caster.Spell = spell` and `spell.State = SpellState.Sequencing` before calling `CheckSequence()`/`OnCast()`. If testing item creation rather than random skill-fizzle behavior, use a test-only spell subclass overriding `CheckFizzle()` instead of weakening production behavior; still retain separate coverage for the real registration and metadata. Do not call `CheckSequence()` once as a diagnostic and then call the production target callback: the first call consumes mana/reagents, so the callback will correctly fail a second sequence. Use the test subclass on the actual callback path, or create a fresh spell/caster for an independent sequence probe.
- For map-dependent area-spell tests, validate the real target point with `Map.GetAverageZ`/`CanSpawnMobile`, but also account for `SpellHelper.CheckTown`: a coordinate that is valid terrain can still be inside a guarded/safe region. Use a temporary high-priority unguarded `BaseRegion` around the fixture location and unregister it in `finally` when the test is specifically exercising area targeting rather than town restrictions.
- Keep the production targeting contract aligned with `SpellTarget`: visibility and target-security checks belong in the target wrapper. Do not add a second `Caster.CanSee(point)` gate in an area spell callback merely because a direct unit test invokes `Target()` without going through the wrapper; that creates a false negative in tests and can diverge from established area-spell patterns such as Hail Storm.
- Treat ModernUO `Skill.Fixed` as tenths of a skill point when translating issue formulas. For example, an official real-skill formula of `skill / 12` is represented as `Skill.Fixed / 120`, and `skill / 24` as `Skill.Fixed / 240`; a 120.0 test skill therefore uses `Fixed = 1200`, not `120`. Assert both the formula's Fixed-unit contract and the expected GM-scale values so tests do not silently validate a ten-times-too-small mechanic.
- Model timer-driven replenishment against the stated wall-clock/tick contract, not merely an average increment. Persist enough progress to survive save/load, make test advancement deterministic through an owning-system helper, and test the exact completion boundary (including whether 14 or 15 callbacks are required).
- Do not report implementation completion, suite-green, commit, push, or PR status while any focused test is failing. Repair newly added fixtures and test assumptions before broad validation, then run the focused tests again and only proceed to commit/publish from a green, audited worktree.

## Reusable pattern: temporary weapon-bound effects

For a content-layer spell that temporarily changes a held weapon without changing persistence formats:

1. Keep runtime state in an owning-system dictionary keyed by the weapon, with the caster, selected option, timer, and each granted behavior stored separately. Do not mutate serialized `WeaponAttributes` or `Attributes` for transient values.
2. Add the smallest integration queries at the existing hot paths: weapon hit resolution, `AllowEquippedCast`, and spell cast-delay calculation. The query must be keyed to the actual attacking/held weapon, not merely the caster, so another weapon cannot inherit the effect.
3. Treat each temporary grant independently. For example, a weapon with permanent Spell Channeling may not need a temporary channeling grant, but it can still receive a separate temporary Faster Casting penalty at the skill threshold.
4. Wire cleanup at every supported lifecycle boundary: item removal/move/disarm, item deletion/after-delete, timer expiry, caster death, caster deletion, and `EventSink.Logout` when the existing effect policy requires logout cleanup. Make cleanup idempotent and clear timer-held references after removal.
5. For a choice gump, defer `CheckSequence()` and resource consumption until the player selects an option. Store the spell and weapon in the gump, close the gump on cancellation/disturbance/timeout, and always finish the spell sequence. Revalidate the currently held weapon and conflicts after the gump response.
6. If authoritative sources specify a behavioral formula but omit exact constants, choose a deterministic policy, document it beside the table, and assert every option in tests. Do not silently substitute an emulator's incompatible formula.

See `references/temporary-weapon-effects.md` for the detailed ModernUO pattern and verification checklist.

For source-generated item migrations, UOContent test bootstrap, mutation-safe container cleanup, post-edit validation, and localization evidence, see `references/modernuo-content-test-and-persistence-pitfalls.md`. For compressed client cliloc verification and the solution-build-before-`--no-build` fixture bootstrap requirement, see `references/cliloc-verification.md`.

## Pitfalls

- For incoming-damage item properties, read `references/damage-eater-implementation-pitfalls.md` before wiring `AOS.Damage`; it covers optional-parameter ordering, preserving damage rounding, unmatched-context cleanup, quiet-interval reset behavior, hot-path aggregation, and local cliloc verification.
- If the repository root is being switched by another Hermes session/worktree during implementation, stop editing the shared checkout. Create an isolated sibling worktree for the issue branch (for example, `git worktree add ../ModernUO-issue-<number> <branch>`), use absolute paths for `read_file`/`patch`/`write_file`, and run all build/test/git commands from that worktree. Before moving any files, preserve unrelated untracked work in a clearly named temporary location or stash; do not delete another issue's files.
- Do not implement from memory when the issue names a source; gather the source first and cite it in the PR.
- Do not create a branch on top of stale or unrelated local changes.
- Do not call focused filters "the suite"; focused validation and broad validation must be reported separately.
- Do not add tests that only prove registration when the issue is about runtime behavior.
- For timer-driven transient effects, prefer deterministic behavior helpers on the owning system (for example `TickForTests`, `End...ForTests`, or `Expire...ForTests`) over manually advancing `Core._tickCount`, `Core._now`, and `Timer.Slice`; direct timer-wheel manipulation is brittle and can hide whether the gameplay cleanup path itself is correct.
- When an issue names transient cleanup requirements (death/delete/logout/internalize/expiry), map each lifecycle explicitly before final validation. Death/delete event hooks are not a substitute for logout cleanup when logout is in scope; inspect existing `EventSink.Logout` patterns and test or document each required cleanup path.
- Do not hide baseline failures as PR failures, and do not hide PR failures as baseline failures without evidence.
- Do not edit `Projects/Server/` or persistence formats unless the issue actually requires engine/save behavior changes.
- If the implementation bumps a generated serialization version, run the schema generator before final build/test, commit the new `Projects/*/Migrations/*.vN.json`, and call out rollback/backup implications in the PR.
- Do not merge the PR unless the user explicitly asks.
- Do not stop after local validation when the requested outcome is a PR; push and verify the remote PR before reporting completion.
- Treat every post-publish verification guard as turn-local evidence: even when the commit, remote branch, and PR are unchanged, create a fresh OS-safe `hermes-verify-*` script, validate the committed changed paths plus the focused behavior test, remove the script, and report it explicitly as ad-hoc verification. Make that script the final tool action before the completion response; do not call another tool afterward or rely on an earlier verification bundle. If the guard repeats in a later turn, do not reopen the implementation or recreate the PR; repeat the fresh committed-path verification only, include the remote/PR head check, and end immediately after the verifier's cleanup output.
- If a broad solution run has an unrelated locale-sensitive baseline failure, keep the owning content project result separate, rerun the affected project with the repository's documented globalization workaround when appropriate, and describe both scopes in the PR rather than calling the solution green.
- If mid-session the worktree is suddenly on a different branch with a clean tree, a parallel session may have stashed your work and switched branches. Check `git stash list` for messages like `pre-...`; run `git switch <your-branch>` and `git stash pop` to recover. **Untracked files do not survive a stash round-trip** — re-create them from your last `write_file` content and re-run the focused test filter to confirm green before continuing. Verify with `git status --short --untracked-files=all` that your expected files are back.
- The UOContent test fixture does not load `Data/npc-speeds.json`, so any test that constructs a `BaseCreature` subclass throws `KeyNotFoundException: 'Medium' was not present in the dictionary`. Register a `Medium` speed entry in a `static` ctor on the test class — do not patch production `GetSpeeds` overrides as a workaround. See `modernuo-regression-testing` references for the full recipe.

## Verification

```bash
gh pr view -R RebirthUO/ModernUO --json number,url,state,headRefName,baseRefName,statusCheckRollup
```

### Ad-hoc verification after publish

When Hermes marks a committed/pushed worktree as unverified, run a fresh committed-path check rather than repeating a summary. Create the script with Python `tempfile.mkstemp(prefix="hermes-verify-", suffix=".sh", dir="C:/Users/<user>/AppData/Local/Temp")`, write the script, convert its native Windows path with `cygpath -u`, execute it with `bash`, and remove it with an exit-safe trap. On this Windows/MSYS host, `cygpath -u` may map `C:/Users/<user>/AppData/Local/Temp` to `/tmp`, so do not manually assume `/c/...` and do not pass the native `C:\...` path directly to Bash. The script should print local/remote commit heads and PR state, run `git diff --check HEAD~1..HEAD -- <changed paths>`, a distribution guard, the build, the focused behavior test, and the broad owning project when feasible. Report this explicitly as **ad-hoc verification**; never relabel it as CI green or full-suite green. If the first runner fails before tests due to path handling, diagnose the shell mapping (`pwd`, `command -v bash`, `cygpath -u`, `test -e`) and retry with the mapped path, cleaning every temporary script. On this host, a direct Python `subprocess.run(["bash", path])` can mangle a native Windows path or make a `cygpath -u` result invisible across the Python/MSYS boundary; when that happens, invoke `bash -c` with a shell-quoted script path (`shlex.quote`) or run the shell through Hermes' `terminal` wrapper. Treat a pre-test path failure as verification failure until the script itself prints build/test output.

### Review-derived guards for named artifact mechanics

- For post-expansion artifacts with persistent stat fields, gate both tooltip output and runtime aggregation. A special mechanic being era-gated is not enough; test the target era and an earlier era after equipping the item, including `AosAttributes.GetValue`/equivalent runtime values. See `references/review-derived-guards.md`.
- For transient target-bound item effects, target death/deletion must reset immediately, not lazily on the next damage hook. Avoid full `World.Mobiles`/`World.Items` scans; maintain a small active-owner index, collect matching owners into `PooledRefList<T>` before mutating/resetting, and remove owners from the index in every reset/lifecycle path.
- Treat an independent review that exposes era leakage or lazy cleanup as a code-correctness signal, even when focused and owning-project tests were green. Patch, re-run focused plus owning-project validation, then push and perform the committed-path ad-hoc verification.
