---
name: modernuo-test-naming
description: Use when writing, reviewing, or cleaning up ModernUO/RebirthUO C# xUnit tests whose file, class, or method names include noisy AI-generated prefixes such as eras, publishes, branch names, issue IDs, task labels, or generic regression labels. Normalizes test identity to the tested object or area, keeps publish/era words only when they are the actual tested object or domain, and proposes or applies rename-only cleanup without changing test behavior.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - modernuo
    - rebirthuo
    - tests
    - naming
    - code-style
    related_skills:
    - modernuo-test-workflow
    - modernuo-regression-testing
    - modernuo-no-publish-prefix-names
---
# ModernUO Test Naming

## Overview

Use this skill to keep generated tests named after what they test, not after
the branch, ticket, publish note, or AI work batch that produced them.

## Operating Rule

Before renaming, inspect the test body, file path, namespace, fixture/data names,
and referenced production symbols. Choose the smallest name that identifies the
tested object, operation, or stable area.

Report proposed cleanup in this shape:

```text
[TEST-NAME] WARNING: {why the current name is noisy}
  File: {path}:{line}
  Current: {file, class, or method name}
  Suggested: {new name}
  Reason: {tested object or area}
```

If the user asked to normalize or clean up test names, apply straightforward
rename-only changes after recording the warning. Ask before changing when the
target name is ambiguous, would collide with another test, or requires moving
tests between files.

Do not change assertions, fixtures, test data, production code, or behavior just
because a test name is bad.

## Naming Standard

- File and class names should be `{ObjectOrArea}Tests`, matching the tested
  production type, service, packet, engine, content system, or stable test area.
- Method names should follow the existing file style: concise PascalCase or
  `SubjectOrOperation_Scenario_Expected`.
- Start method names with the tested subject or operation, not a publish, era,
  branch, issue, or task label.
- Keep acronyms and domain names that are part of the object: `MLQuest`,
  `MLPeerlessArtifacts`, `EraProfileManager`, `TreasuresOfTokuno`,
  `PublishWindow`, `AOS`, `SE`, and similar real APIs or content areas.
- Keep era or publish words only when the era/publish is the tested object or
  domain. If it is only context, move that information into the scenario,
  inline data, fixture setup, or assertion message.

## Noise To Remove

Flag these when they are only prefixes or labels:

- Publish labels: `Publish81`, `publish81`, `P81`, `Pub90`.
- Era labels: `SE`, `ML`, `TOL`, `SamuraiEmpire`, `MondainsLegacy` when they do
  not name the tested object or stable area.
- Branch/task labels: `sync-modernuo-main`, `feature-*`, `issue123`, `task2`,
  `codex-*`, ticket slugs, or PR names.
- Generic batch labels: `Generated`, `Regression`, `Coverage`, `Smoke`, or
  `AI` when the word does not identify the tested behavior.

## Rename Recipe

1. Identify the tested object or area from production type references, helper
   names, setup calls, and assertions.
2. Rename the file and class to `{ObjectOrArea}Tests` unless the file is an
   intentional broad-area suite.
3. Rename each method to preserve its operation, scenario, and expected result
   while removing source-of-work prefixes.
4. Use `rg` to find references before changing file/class names.
5. Run the narrowest relevant test or at least `dotnet test --no-build` for the
   affected test project when practical.
6. If the tests live on existing PR branches and the user asked for the PRs to
   be changed, follow the GitHub PR workflow after validation: stage, commit,
   push each branch, and verify the PR heads moved. Do not stop at local-only
   rename cleanup.

## Audit-Only Review Workflow

When the user asks to *find* additional AI-generated wrong prefixes, do not edit
first. Produce an evidence-backed candidate list:

1. Scan file stems, class names, and xUnit method names separately.
2. Treat hard source-of-work prefixes as high-confidence noise: `Publish\d+`,
   `Pub\d+`, `P\d+`, `Issue\d+`, `Task\d+`, `Codex`, `Generated`,
   `Regression`, and `AI`.
3. Treat `Coverage` and `Smoke` in file/class names as generic AI batch labels
   unless the suite is intentionally a broad health check. Prefer concrete
   names such as `{System}Tests`, `{ContentArea}Tests`, or
   `{Operation}Tests`.
4. For era words (`MondainsLegacy`, `SamuraiEmpire`, `ML`, `SE`), separate real
   domain names from noisy context:
   - keep when the word names the tested production API, source-reference hub,
     quest engine, artifact family, or stable content area;
   - flag when the test class is already specific (`DisarmAbilityTests`,
     `ParrotContentTests`, `BaseWeapon...Tests`) and only the method starts with
     the era label.
5. Include line numbers and suggest rename-only replacements, but mark ambiguous
   cases as review candidates instead of presenting them as certain fixes.
6. If hard noise count is zero, say so explicitly before listing softer
   era/context candidates.

See `references/test-prefix-audit.md` for a compact checklist and examples from
RebirthUO-style test-name audits.

## Rename-Only PR Cleanup Workflow

When the user asks to apply the normalization and merge it:

- Work from a clean branch/worktree based on the requested base branch so existing user changes in the main working copy are not touched.
- Keep the change rename-only: file/class/method identifiers and direct references only; do not alter assertions, fixtures, production code, or behavior.
- On Windows/MSYS, file mode-only noise can appear in worktrees. Inspect/stage with `git -c core.filemode=false` and stage only the test paths involved.
- After edits, run the prefix scan and expect zero actionable generated-prefix findings, allowing true domain names such as source-reference tests and `MLSetArmorTests`.
- Validate with `git diff --cached --check`, a full build, and targeted renamed-class xUnit filters. If a broad exploratory test run hits unrelated static-state/order-sensitive failures, report it as exploratory rather than mixing behavior fixes into the rename-only PR.
- If the user asked for PR/merge completion, do not stop at local cleanup: commit, push, open the PR, merge it, delete the branch, and verify the PR/base state.

Detailed command snippets live in `references/rename-pr-cleanup.md`.

## Examples

```text
Publish81TreasuresOfTokunoTests.cs
  -> TreasuresOfTokunoTests.cs

Publish81DropsUseToTTwoEra()
  -> DropEra_InsidePublishWindow_UsesToTTwo()

syncModernuoMainMovementThrottleTests.cs
  -> MovementThrottleTests.cs

FeatureMlPeerlessArtifacts_SourceTableCoverage()
  -> OfficialMappingContainsRequiredArtifactForSource()

MLPeerlessArtifactsTests.cs
  -> keep; MLPeerlessArtifacts is the tested object.

EraProfileManagerTests.cs
  -> keep; EraProfileManager is the tested object.

PublishWindow_SchedulesDropAndRewardEras()
  -> keep; PublishWindow is the tested object.
```
