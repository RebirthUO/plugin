---
name: rebirthuo-review-patterns
description: Reusable review patterns for RebirthUO GitHub issues: mechanics source framing, repo anchors, implementation-readiness gates, German review structure, and durable reference files for recurring UO systems.
version: 0.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags:
    related_skills:
    skill_group: rebirthuo
    skill_subgroup: agentic
    workflow_phase: review
    workflow_tier: reference
---
# RebirthUO Review Patterns

## Passive Safety Contract (Overrides Later Mutation Examples)

This is non-mutating reference guidance. Passive activation authorizes analysis only: no issue/PR read, comment, edit, label change, close action, branch, commit, push, or PR creation. If the user explicitly requests a RebirthUO issue action, load the appropriate exact-repository `rebirthuo-issue-*` skill; this reference itself never performs GitHub mutations.


## When to Use

Use this skill when reviewing RebirthUO GitHub issues before implementation, especially `needs-review` issues that need a German, implementation-ready mechanics review rather than code changes.

## Review Shape

Use the German review structure expected for RebirthUO triage:

- Kurzfassung with `Implementierungsreif` / `Nicht implementierungsreif`
- Ziel
- Quellen & Repo-Anker
- Code-Änderungsplan
- Erwartete Formel-/Testwerte
- Akzeptanzkriterien
- Testplan
- Risiken & Nebenwirkungen
- Fehlende Voraussetzungen only when not implementation-ready

## Core Rules

1. Parse the exact issue URL/repo/number and use explicit `gh ... --repo RebirthUO/service`.
2. Read the issue body, comments, labels, state, author, URL, assignees, and linked PRs before deciding.
3. Prefer source-backed UO.com/UOGuide/Stratics claims, then repo anchors, then issue-supplied/custom policy evidence.
4. Name era/ruleset and `Core.*` gates explicitly. For RebirthUO spell audit work, a parent epic may set EJ/default assumptions, but each sub-issue still needs its own gate and acceptance criteria.
5. Avoid duplicate comments: if a full `## Fachliches Review — #N` exists and the issue has not changed since then, report it as already present rather than posting another copy.
6. If the user asks to update the original ticket/initial issue body instead of adding comments, honor that workflow: interview first, then use `gh issue edit --body-file` or the Issues API PATCH on the issue body. Do not post solution comments unless explicitly asked.
7. Remove `needs-review` only after the chosen public-update action succeeds and only if the decision is `Implementierungsreif`.
8. Verify by reading back labels and the issue body/comment target that was updated.

## Support References

- `references/spellweaving-arcane-empowerment-review.md` — Arcane Empowerment / Spellweaving buff review notes: UO.com formula interpretation, repo anchors, test values, and common pitfalls.
- `references/bane-item-property-review.md` — Bane / Publish 83 weapon-property review notes: source frame, RebirthUO issue #1 interview decisions, repo anchors, and pitfalls.
- `references/gameplay-pr-review-checklist.md` — Isolated-worktree verification, delayed-state and sequence-boundary review, and self-authored PR publication fallback.

## Pull-request Review Additions

For RebirthUO/ModernUO gameplay PRs, passing compilation and focused unit tests are not sufficient evidence of correct behavior. Trace the complete lifecycle: delayed effects, restoration/rollback timers, death/logout/equipment transitions, reflected damage, and multi-stage damage paths. Compare formulas and sequences at exact boundary values, including cap duration, reset timing, target changes, and the first value after reset. Do not accept a test that merely codifies the implementation when it contradicts the PR's own Definition of Done.

Distinguish focused coverage from integration coverage. If a modifier is applied immediately but a later timer consumes the original value, require a regression test for both immediate and delayed outcomes. Report the affected player loop and PvP/PvM risk, not only the code symptom.

When the authenticated GitHub account owns the PR, GitHub rejects formal `APPROVE`/`REQUEST_CHANGES` reviews. Fall back to a top-level `Code Review Summary` comment containing the verdict, exact file/line anchors, validation commands, and the reason formal review was unavailable. Read the comment back and verify its URL before reporting completion.

## Independent Worktree Review Lessons

For gameplay PRs, verify the test harness before interpreting focused failures as production behavior:

- When an equipment test uses `FindItemOnLayer`, explicitly inspect the constructed item's `Layer`. UOContent tests commonly run without tile data, while production constructors derive layers from tile data; set `Layer.TwoHanded` (or the required layer) in the fixture when appropriate.
- Report the exact focused-test denominator and failure location. A helper assertion that fails before the damage/combat call means the mechanic itself was not exercised; do not call that behavioral coverage.
- In hot damage hooks, audit global-state side effects beyond the returned mechanic: a zero-probability path must not consume `Utility.Random`, allocate, or otherwise perturb unrelated combat rolls. Compare with short-circuit patterns such as `chance > 0 && chance > Utility.Random(100)`.
- Separate production findings from baseline or fixture failures. Run the focused class, then the full owning test project, and identify which failures are newly attributable to the changed files.
- For clilocs, distinguish issue/source evidence from local client-data verification. If the repository has no client data, say that explicitly and treat unverified notification text as a validation gap rather than silently asserting it is confirmed.
- Re-check repository state immediately before reporting: `git status --short --branch`, `git log -1`, and `git diff origin/main`. A concurrent agent or hook can commit the reviewed work during validation; re-read the final HEAD diff and clearly state whether the final tree is committed or uncommitted.
- For item-property reviews, reconstruct the complete tooltip call order through `Item.GetProperties` → `AddNameProperties` → inherited attribute `GetProperties`; do not infer order from the new class alone. Test both the special-era order and the pre-era behavior, including whether generic stats remain mechanically active when only the special property is gated.
- For runtime state keyed by a target, distinguish lazy reset on the next damage attempt from event-time cleanup. A target death event usually carries the target, not the caster; verify that the caster's item state and player buff are actually cleared immediately, not merely before the next valid cast.
- A fixture using plain `Mobile` does not exercise `PlayerMobile`-only buff code. Treat passing sequence tests with such a fixture as formula coverage, not buff/lifecycle coverage; add an actual player fixture for buff add/remove and death/logout paths.
- Re-snapshot untracked implementation and test files immediately before reporting. Another process can rewrite an untracked file without changing `git status`, or stage the reviewed files while leaving them uncommitted; if file content, staged/unstaged state, or the focused-test denominator changes during review, re-read the final files, rebuild the owning project, and rerun focused validation against the final contents. Do not anchor findings to the initial snapshot.
- Treat lifecycle tests that manually invoke generated death/deletion event methods as handler-unit coverage only. For claims about death, deletion, logout, or kill cleanup, require at least one integration test that drives the real transition; also verify the fixture uses a fully initialized `PlayerMobile`/entity constructor and has enough health to avoid an accidental fixture-side death path.
- For combat-property reviews, distinguish formula tests from combat-pipeline tests. Direct `OnHit`/`OnMiss` calls or synthetic absorption are not proof of real `OnSwing`/`CheckHit` miss/parry behavior; require an actual pipeline test for parry/miss boundaries and use real `PlayerMobile` fixtures for PvP lifecycle coverage.
- When a property tooltip uses a candidate cliloc, inspect local client data when available using the repository's cliloc format (including the compressed/BWT path) and report the resolved text; a test that only asserts the numeric ID is not local verification.
- For target-sensitive modifiers, trace the target argument through every production hook. A helper that passes `null` from a melee hook can silently select the PvM branch for player targets; require separate PvM/PvP boundary tests for both melee and spell damage.
- A generic central hook must know whether its input already contains an upstream modifier. Do not cap a new PvP bonus using raw item SDI when fixed-damage callers may bypass SDI generation; inspect representative fixed-damage callers and carry provenance or actual-applied SDI explicitly.
- Before applying a spell-only modifier in a shared helper, enumerate all callers. Helpers named for spells may also be used by magic items or resources; keep non-spell effects out unless the contract explicitly includes them.
- Directly invoking an internal modifier or cleanup method is not integration coverage. For era gates, central damage/healing hooks, and generated lifecycle events, add tests that use the real `CheckCast`/central call/event path with actual `PlayerMobile`/`BaseCreature` fixtures and the required client/quest context.

## Pitfalls

- Do not confuse local repo evidence with official UO parity; label it as repo evidence unless a source confirms it.
- Do not call focused tests broad-suite proof.
- Do not let focused tests hide a contradiction between the implementation and the PR's own Definition of Done; independently calculate sequence boundaries and delayed-state behavior.
- Public comments should discuss PvP/PvM/economy/security risks without publishing exploit-ready bypass details.
- On Windows/MSYS, pass a native Windows path to `gh issue comment --body-file` when using a temp Markdown file.
