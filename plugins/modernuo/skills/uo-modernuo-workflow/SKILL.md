---
name: uo-modernuo-workflow
description: Use when working on Ultima Online or ModernUO projects, shared UO/ModernUO agent instructions, or compatibility across Cursor, Claude, Codex, and GitHub Copilot.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - ultima-online
    - modernuo
    - workflow
    - routing
    - skills
    related_skills:
    - modernuo-code-audit
    - modernuo-content-patterns
    - modernuo-lifecycle-cleanup
    - modernuo-performance-hot-paths
    - modernuo-serialization
    - modernuo-timers
    - modernuo-threading
    - modernuo-string-handling
    - modernuo-property-lists
    - modernuo-gump-system
    - modernuo-commands-targeting
    - modernuo-regions
    - uo-world-facets-regions
    - modernuo-era-expansion
    - modernuo-test-workflow
    - migrate-foundation
    - migrate-serialization
    - modernuo-skill-discovery
    - uo-living-world-review
    - ultima-online-product-model
    - uo-era-product-timeline
    - modernuo-lootpack-preservation
    - modernuo-monster-abilities
    - modernuo-regression-testing
    - modernuo-custom-module
    - modernuo-no-publish-prefix-names
---
# UO ModernUO Workflow

## Overview

Use this skill when a task touches Ultima Online shard work, ModernUO server development, the shared plugin, or tool-specific adapters.

This is a thin coordinator. Its job is to route to the smallest useful child skill, preserve UO product consequences, and avoid duplicating specialized instructions here. After routing, follow the child skill's detailed rules and keep this skill out of the way.

## When to Use

- Any UO, RebirthUO, ModernUO, RunUO migration, era-parity, gameplay, shard-policy, or plugin-guidance task.
- A request spans multiple domains and needs routing before code, docs, triage, or testing.
- You are unsure which specialized UO/ModernUO skill should own the next step.

Do not use this as a replacement for a domain skill. Once the owning domain is clear, load the child skill and work from that narrower checklist.

## Skill Routing

Load child skills by task shape before deep work:

| Task shape | Load |
|---|---|
| Any `.cs` edit under `Projects/` | `modernuo-code-audit` |
| New item, mobile, creature, spell, skill handler, loot table, or content under `Projects/UOContent/` | `modernuo-content-patterns`, `modernuo-serialization`, `modernuo-code-audit` |
| Creature special attacks, boss debuffs/counters/breath/summons | `modernuo-monster-abilities`, `uo-combat-pipeline`, `modernuo-content-patterns` |
| Creature loot, `GenerateLoot()`, `AddLoot(LootPack.*)`, drop-policy changes | `modernuo-lootpack-preservation`, `uo-loot-generation-artifacts`, `modernuo-era-expansion` |
| Regression tests, `Test missing` parity slices, UOContent fixture failures | `modernuo-regression-testing`, `modernuo-test-workflow`, `modernuo-test-naming` |
| Custom content assembly/module beside `UOContent` | `modernuo-custom-module`, `modernuo-server-lifecycle`, `modernuo-test-workflow` |
| Publish-number or era-source naming in symbols/tests | `modernuo-no-publish-prefix-names`, `modernuo-symbol-discipline`, `modernuo-era-expansion` |
| Serialized fields, `[SerializationGenerator]`, version bumps, save/load behavior | `modernuo-serialization` |
| Timers, delays, recurring behavior, expiry, cleanup after deletion | `modernuo-timers`, `modernuo-lifecycle-cleanup`, `modernuo-threading` |
| RunUO migration, any script type | `migrate-foundation` first, then the system-specific migration skill, then `modernuo-code-audit` |
| RunUO manual `Serialize`/`Deserialize` migration | `migrate-foundation`, `migrate-serialization`, `modernuo-serialization` |
| Gumps, dialogs, UI layout, HTML labels | `modernuo-gump-system`, `modernuo-string-handling`, `modernuo-code-audit` |
| Property lists, tooltips, OPL/cliloc output | `modernuo-property-lists`, `modernuo-string-handling` |
| Commands, targeting, player interactions | `modernuo-commands-targeting` |
| Regions, facets, travel rules, spatial gameplay restrictions, dynamic region cleanup | `modernuo-regions`, `modernuo-lifecycle-cleanup`, `uo-world-facets-regions` |
| Era or expansion conditional behavior | `modernuo-era-expansion`; ask which era/ruleset when unclear |
| Async, `Task`, threads, locks, concurrent collections, world-save threading | `modernuo-threading` |
| Dynamic strings, messages, packets, gump HTML, `StringBuilder` replacement | `modernuo-string-handling` |
| Performance, allocations, hot paths, spatial scans, pathfinding tuning, packet fan-out | `modernuo-performance-hot-paths`, then the relevant child skill |
| Tests, validation, PR readiness | `modernuo-test-workflow` |
| Skill coverage or gap analysis | `modernuo-skill-discovery` |

For RunUO migration, use this chain: `migrate-foundation` → `migrate-serialization` when saves are involved → domain migration skill → relevant `modernuo-*` runtime skill → `modernuo-code-audit` → `modernuo-test-workflow` when tests exist.

Completion criterion: after this routing step, every high-risk domain in the request has a loaded child skill or an explicit reason it is not needed.

## Workflow

- Read the repository-level guidance first: `AGENTS.md`, then any tool-specific file that applies to the current surface.
- Treat the scope as Ultima Online and ModernUO project guidance, not guidance for a single shard or brand.
- Prefer ModernUO upstream conventions and C#/.NET idioms when working in server code.
- Preserve UO gameplay semantics, persistence and serialization behavior, command access levels, map/world state, and save/load compatibility unless a task explicitly changes them.
- Avoid hardcoding shard-specific names, URLs, branding, or assumptions in reusable plugin guidance.
- Use `modernuo-server-lifecycle` for startup, bootstrap phases, first-boot prompts, shutdown, and production-vs-test lifecycle differences.
- Use `modernuo-pathfinding` for creature movement, `PathFollower`, `BitmapAStarAlgorithm`, `StepCache`, `.swb` cache files, and pathfinding diagnostics.
- Use `modernuo-world-saves-archives` for backup, restore, archive rollup, journal recovery, and `WorldSavePostSnapshot` work.
- Keep `modernuo/.codex-plugin/plugin.json`, `modernuo/.claude-plugin/plugin.json`, `modernuo/.cursor-plugin/plugin.json`, and marketplace metadata aligned for shared identity fields: `name`, `version`, `description`, `author`, and skill paths.
- When syncing the ModernUO plugin to Hermes, scan the entire active profile skills tree, not only `software-development`. Select UO/ModernUO/RebirthUO-themed skills by **skill name plus frontmatter scope** (`name`, `description`, tags/metadata) rather than arbitrary body text; body-term matching can accidentally include general skills that merely mention RebirthUO in an example. Copy whole selected skill directories including `references/`, `templates/`, `scripts/`, and any other support files, remove plugin extras that are not selected, and verify exact file equality plus source/plugin skill counts after sync. Do not hand-edit synced plugin copies.
- For ModernUO plugin sync verification, use `references/modernuo-plugin-sync-verification.md` as the durable checklist/script pattern: manifest versions, README/CHANGELOG, selected skill set equality, per-file SHA-256 equality, and deletion of temporary ad-hoc verifier scripts.
- Keep this skill instruction-only unless a concrete script, hook, MCP server, or app integration is requested.
- Do not add marketplace entries, MCP config, hooks, app manifests, logos, screenshots, or stub assets unless the request explicitly asks for them.
- After changing the plugin structure, run the Codex plugin validator before reporting completion.
- If no canonical plugin validator/test exists or the guard asks for fresh evidence, create an OS-temp `hermes-verify-*.py` ad-hoc script with `tempfile`, assert the changed manifest behavior and synced skill counts/content, run it, delete it when possible, and label the result as ad-hoc verification rather than suite-green.
- For multi-worktree RebirthUO validation, use `references/rebirthuo-worktree-validation.md`: durable per-worktree logs, `MSBUILDDISABLENODEREUSE=1`, single-worker builds, and `--no-build --no-restore` test reruns after a successful build.
- For **expansion parity epics** (feature inventory + GitHub Epic + `dev-docs/eras/*.md`), use `modernuo-era-parity-check` and its `references/ml-expansion-epic-workflow.md` — anchor `Documents/GitHub/RebirthUO/service`, not `workspace/service`. **Same-turn verification:** grep + focused `dotnet test` before any review row; see `modernuo-era-parity-check/references/review-verification-standard.md` (no deliverable that only says Partial/unsicher/Tests fehlen).
- For isolated Ninjitsu/UOContent test slices, use `references/rebirthuo-ninjitsu-test-fixtures.md`: process-global Movement/Poison initializers, Animal Form fixture traps, and Mirror Image runtime-test anchors. Watch for startup registries that are normally initialized by server boot. Movement-delay assertions need `Server.Movement.Movement.Configure()` before comparing mounted/foot delays; poison assertions may need `PoisonKinds.Configure()` when `Poison.GetPoison("Lesser") == null`. Mirror Image tests belong in runtime Ninjitsu/UOContent tests, not pure formula tests, because follower slots, clone cleanup, timers, and radius interception depend on real `Mobile`/`Clone`/map-sector state.

## ModernUO PR Communication

When opening or updating a PR for ModernUO/UO gameplay or server-mechanics work, make the PR useful to shard maintainers first and code reviewers second:

1. **Gameplay problem** — explain the player-facing, operator-facing, or shard-balance problem in plain English. Include era/ruleset assumptions and why the current behavior is wrong or risky.
2. **Sources / evidence** — cite the domain sources behind the claim (UO.com, UOGuide, Stratics, issue triage comment, parity ledger, logs, or design docs) and cite repo anchors as `path:line-range`. Do not make unsourced mechanics claims.
3. **Behavior change** — state the observable behavior after the PR, plus what intentionally stays unchanged. Call out PvP/PvM/economy/housing/save-compatibility side effects when applicable.
4. **Why this is correct** — connect the implementation to source-era formulas, repo anchors, logs, tests, or acceptance criteria. Be explicit about what the evidence proves and what it does not prove.
5. **Definition of Done** — include a checkbox list mapping every acceptance criterion to sources, code, tests, docs, and validation. This is more important than raw technical detail.
6. **Validation** — list commands that actually ran and their results. If broad suites fail on the base branch, separate baseline failures from PR regressions.

Put implementation details, static scans, and code-review notes after the domain explanation and sources. Avoid PR bodies that are only technical command dumps.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.


## Common Pitfalls

1. **Staying in the coordinator too long.** This skill should route; detailed work belongs to the child skill.
2. **Loading only code skills for gameplay changes.** For UO work, also name era/ruleset, facet/map, player loops, economy/housing/PvP/PvM side effects, and source evidence.
3. **Treating child skills as permanent sediment.** If a child skill only repeats this coordinator and adds no distinct completion criteria, mark it as a consolidation candidate instead of polishing no-op prose.
4. **Calling focused validation broad validation.** Use `modernuo-test-workflow` and label focused test filters honestly.

## Verification Checklist

- [ ] Every high-risk domain in the request has a loaded child skill or an explicit reason it is not needed.
- [ ] The answer names era/ruleset, facet/map, player-loop side effects, source evidence, and repo anchors when gameplay behavior is involved.
- [ ] Any code/docs/test work was verified with real tool output or an explicit blocker.
- [ ] Any skill-curation finding distinguishes keep, patch, absorb, or delete-with-confirmation.
