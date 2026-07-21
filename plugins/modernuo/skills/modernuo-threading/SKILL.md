---
name: modernuo-threading
description: >
  Use when reviewing, planning, or implementing authorized ModernUO async/await,
  Task/thread usage, game-loop ownership, concurrent collections, pooling,
  network/server infrastructure, or parallel world-save serialization. Do not
  use for ordinary delayed gameplay actions; route scheduling to modernuo-timers.
license: MIT
metadata:
  version: "1.2.0"
---

# ModernUO Threading and Event Loop

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Normal game-state mutation belongs to the single game-loop thread. Explicit
server infrastructure may use worker threads for networking, pool maintenance,
and world-save serialization, but those boundaries do not make entities, timers,
maps, or `NetState` generally thread-safe.

## Required Inputs

Require the repository root and revision, the relevant source or diff, the
entry point, and evidence for the execution context and mutable state touched.
Use repository source, tests, diagnostics, and measured traces as evidence;
label issue text and user statements as supplied claims until verified.

Resolve a symbolic revision to its full commit ID and record it. For `review`,
require resolvable source plus ownership evidence; for `plan`, also require the
intended change boundary; for `implement`, require writable scoped files and
applicable test commands. A partial diff is acceptable only with its base and
the surrounding ownership code.

If the context, ownership boundary, or worker-infrastructure classification
cannot be proven, ask one focused question only when one user answer can supply
the missing required input and interaction is available; otherwise return
`BLOCKED`. Route ordinary delayed gameplay to `modernuo-timers` and generic
non-ModernUO concurrency out of scope.

Resolve the requested mode as `review`, `plan`, or `implement`. Treat diagnosis,
review, and advice as read-only; edit only when the user explicitly requests a
change or implementation. For an unreadable root, unknown revision, unresolved
entry point, partial diff, or conflicting evidence, attempt one repository-local
resolution, record the conflict, then ask one focused question or return
`BLOCKED`. Never choose between conflicting traces or revisions by assumption.

## Workflow

1. Identify the current thread/context, continuation target, state touched, and
   whether the code is gameplay or reviewed server infrastructure.
2. Trace how work enters and returns to `EventLoopContext`. For delayed gameplay,
   use timer/event-loop primitives rather than offloading state mutation.
3. Identify unnecessary `Task.Run`, raw threads, locks, atomics, volatile fields,
   or concurrent collections in single-threaded game code. Remove them only in
   `implement` mode; otherwise report or plan the smallest safe change.
4. For real worker-thread code, snapshot immutable data, bound ownership, and
   marshal any game-state mutation back to the event loop.
5. Audit serialization callbacks separately: entity `Serialize()` runs on
   background workers during parallel world saves and must be pure.
6. Test ordering/cancellation/shutdown behavior and use stress/diagnostic evidence
   for infrastructure concurrency changes.

Stop with `BLOCKED` rather than proposing a crossing when repository evidence
cannot establish the event-loop handoff or lifetime boundary.

## Guardrails

- Do not touch `Item`, `Mobile`, `World`, `Map`, timer APIs, or `NetState` from
  arbitrary worker threads.
- `await Timer.Pause(...)` is safe when the captured ModernUO synchronization
  context posts continuation back to the event loop. Do not suppress that context
  without proving the new ownership boundary.
- Never use `Thread.Sleep()` on the game loop.
- Game code normally uses `Dictionary`, `PooledRefList<T>.Create()`, and
  `STArrayPool<T>.Shared`; multi-threaded variants belong only to proven worker
  contexts.
- `Serialize()` may read stable fields and write its `IGenericWriter`; it must not
  create/delete/move entities, start/stop timers, send packets, or mutate shared
  state.
- A lock does not make a game entity safe to mutate off-thread.

## Failure Handling

- Report unavailable tools or missing source as `BLOCKED`; do not substitute an
  unverified concurrency claim.
- Report tests that successfully run and observe a race, leak, or unsafe
  crossing as `UNSAFE`; retain exact failure evidence and the smallest repair.
- Treat a test runner, build, profiler, or diagnostic tool failure as an
  evidence failure, not proof of unsafe behavior; apply the retry/fallback rule
  below and return `INCONCLUSIVE` or `BLOCKED` as appropriate.
- Report non-reproduced timing failures as `INCONCLUSIVE`; record attempts and
  missing diagnostics instead of treating absence of reproduction as success.
- Never claim a stress, profile, or runtime result from static inspection.
- If a test, trace, profiler, or diagnostic tool fails, retry once when the
  failure is transient and safe. Then use repository source and focused static
  checks for conclusions they can support, preserve the failed command/error,
  lower confidence, and return `INCONCLUSIVE` or `BLOCKED` for any claim that
  still requires runtime evidence.

## Output Contract

Return these headings in order:

1. `Status` — exactly `SAFE`, `UNSAFE`, `INCONCLUSIVE`, or `BLOCKED`, applied to
   the reviewed current state in `review`, the proposed design in `plan`, or the
   verified resulting state in `implement`. `SAFE` never upgrades plan review or
   static inspection into runtime validation.
2. `Evidence` — requested mode, repository, revision, paths/symbols, and evidence
   type.
3. `Context and Ownership` — execution-context map and mutable-state owner.
4. `Crossings and Handoff` — unsafe/redundant primitive and chosen event-loop
   handoff, or `None`.
5. `Lifecycle` — cancellation, shutdown, ordering, and retained-object behavior.
6. `Verification` — checks run with `passed`, `failed`, or `not run` and reason.
7. `Unresolved` — remaining uncertainty and confidence `high`, `medium`, or
   `low`; use `None` only when every material conclusion is verified.

Completion requires all seven headings, source locators for material claims,
and no safety claim stronger than its recorded static or measured evidence.

## Verification

- `review`: statically trace continuations, ownership, retained objects, and
  serialization purity; run focused existing tests when available.
- `plan`: perform the review checks and name the exact focused test/diagnostic
  commands; mark them `not run` and do not claim their outcomes.
- `implement`: run focused tests for every touched crossing and lifecycle path,
  plus repository-required build/static gates; use stress or profile evidence
  for material infrastructure concurrency/performance claims.
- In every mode, verify that game-state mutation returns to the event loop,
  workers retain no live entities after cancellation/shutdown, and parallel
  serialization callbacks remain pure.

## Reference Routing

- From the configured repository root, read `dev-docs/threading-model.md` and
  locate the current `EventLoopContext` and world-save implementations at the
  reported revision before changing infrastructure. If a named path or symbol
  is absent, search the repository and report the resolved locator; otherwise
  return `BLOCKED`.
- Load sibling skill `../modernuo-timers/SKILL.md` for delayed actions and
  `../modernuo-world-saves-archives/SKILL.md` for save callback purity plus
  snapshot/archive boundaries. Verify each dependency exists before routing; if
  it is unavailable, retain this skill's guardrails, report the missing path,
  and return `BLOCKED` for conclusions that require that dependency.
- Give a sibling the pinned revision, source locators, requested mode, and open
  question; require returned evidence locators and unresolved items, then apply
  this skill's status and confidence rules to the combined result.
- Mark the revision, ownership question, and each consulted skill in the handoff.
  Do not reload a skill already consulted for that same question; reuse its
  returned evidence and finish under this skill's status rules.
- Treat this skill's technical prose as methodology, not versioned runtime fact.
  Revalidate every applied guardrail against the pinned repository's
  `dev-docs/threading-model.md` and current source before asserting behavior.
- Resolve this skill's installed/source directory, then run
  `python <skill-dir>/evals/run_behavior_cases.py --outputs <json>` when candidate
  outputs are available; the JSON object maps each case name to its output text.

## Example

Input: review a `Task.Run` that captures a `Mobile`, awaits work, then mutates it.
Output: `Status: UNSAFE`, cite the revision and source line, map the worker/event
loop contexts, replace the live capture with immutable data plus an event-loop
handoff, document cancellation, and list focused verification with confidence.

Plan example: `Status: SAFE` means the proposed ownership design is statically
safe; list all commands as `not run`. Implement example: status the resulting
code only after focused gates run, and use `INCONCLUSIVE` if required runtime
evidence is unavailable. Harness example: capture one output per fixture name in
a JSON object, then run
`python <skill-dir>/evals/run_behavior_cases.py --outputs out.json`; run
`python <skill-dir>/evals/run_behavior_cases.py --self-test` for rejection paths.
