---
name: modernuo-threading
description: >
  Use when reviewing ModernUO async/await, Task/thread usage, game-loop ownership,
  concurrent collections, pooling, network/server infrastructure, or parallel
  world-save serialization. Do not use for ordinary delayed gameplay actions;
  route scheduling to modernuo-timers.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, threading, event-loop, world-saves, performance]
    related_skills:
      - modernuo-code-audit
      - modernuo-timers
      - modernuo-serialization
      - modernuo-world-saves-archives
      - modernuo-performance-hot-paths
      - modernuo-pathfinding
      - modernuo-test-workflow
---

# ModernUO Threading and Event Loop

## Boundary

Normal game-state mutation belongs to the single game-loop thread. Explicit
server infrastructure may use worker threads for networking, pool maintenance,
and world-save serialization, but those boundaries do not make entities, timers,
maps, or `NetState` generally thread-safe.

## Workflow

1. Identify the current thread/context, continuation target, state touched, and
   whether the code is gameplay or reviewed server infrastructure.
2. Trace how work enters and returns to `EventLoopContext`. For delayed gameplay,
   use timer/event-loop primitives rather than offloading state mutation.
3. Remove unnecessary `Task.Run`, raw threads, locks, atomics, volatile fields, or
   concurrent collections from single-threaded game code.
4. For real worker-thread code, snapshot immutable data, bound ownership, and
   marshal any game-state mutation back to the event loop.
5. Audit serialization callbacks separately: entity `Serialize()` runs on
   background workers during parallel world saves and must be pure.
6. Test ordering/cancellation/shutdown behavior and use stress/diagnostic evidence
   for infrastructure concurrency changes.

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

## Output Contract

Return the execution-context map, state ownership, unsafe crossing or redundant
primitive, chosen event-loop handoff, shutdown/cancellation behavior, and
verification. Distinguish static reasoning from stress/profile evidence.

## Verification

- Continuations that mutate game state execute on the event loop.
- Worker code cannot retain/mutate live entities after cancellation or shutdown.
- Serialization callbacks are pure under parallel workers.
- Ordering and cleanup tests pass; performance/concurrency claims have measured
  evidence where material.

## Reference Routing

- Read `dev-docs/threading-model.md` and current `EventLoopContext`/world-save
  implementations before changing infrastructure.
- Load `modernuo-timers` for delayed actions, `modernuo-serialization` for save
  callback purity, and `modernuo-world-saves-archives` for snapshot/archive
  boundaries.
