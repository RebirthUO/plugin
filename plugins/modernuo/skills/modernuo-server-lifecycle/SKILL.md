---
name: modernuo-server-lifecycle
description: >
  Use when changing or reviewing ModernUO startup/shutdown phases,
  ConfigurePrompts/Configure/Initialize ordering, CallPriority, world load/save
  events, networking startup, or the event loop. Do not use for per-entity
  deletion cleanup; route that to modernuo-lifecycle-cleanup.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, lifecycle, startup, shutdown, world-load]
    related_skills:
      - modernuo-code-audit
      - modernuo-threading
      - modernuo-events
      - modernuo-configuration
      - modernuo-world-saves-archives
      - modernuo-test-workflow
---

# ModernUO Server Lifecycle

## Boundary

Own process bootstrap, reflection hook ordering, first-boot interaction, world
readiness, shutdown, and runtime-loop placement. The production sequence, not a
partial test fixture, is authoritative.

## Workflow

1. Trace the current production path through configuration load, assembly load,
   `ConfigurePrompts`, logging, serialization verification/timer setup,
   `Configure`, tile/region/world load, `Initialize`, networking,
   `ServerStarted`, and `RunEventLoop()`.
2. Classify the work by earliest safe phase:
   - `ConfigurePrompts()`: self-gated first-boot console input only.
   - `Configure()`: commands, settings, event subscriptions, and pre-world wiring.
   - `Initialize()`: work requiring tile data, regions, or loaded world entities.
   - lifecycle events: behavior tied to a completed load/save/start/stop boundary.
3. Inspect `CallPriority`, explicit calls, and neighboring hooks. Do not depend on
   reflection enumeration or same-priority order.
4. Keep prompts and their later world-dependent work separate; make headless and
   redirected-input behavior non-blocking.
5. Verify production startup behavior as well as targeted fixture tests.

## Guardrails

- `ConfigurePrompts()` runs before normal logging; use the established console
  path, self-gate, and skip redirected input. It must not touch world entities,
  regions, tile matrices, or map-dependent content.
- Do not prompt from `Configure()` or `Initialize()` where it can block services
  or interleave with runtime logging.
- Use explicit priority/calls/events when order matters; same-priority hooks have
  no reliable relative order.
- Tests may invoke only a curated startup subset. A passing fixture does not prove
  first-boot console behavior or full `Core.Setup()` ordering.
- Keep post-snapshot archive work and background serialization boundaries with
  their owning lifecycle event.

## Output Contract

Return the chosen phase, dependencies available there, ordering mechanism,
headless/test behavior, changed paths, and verification. Review findings must
name the exact phase mismatch and consequence.

## Verification

- Fresh configuration, existing configuration, and redirected/headless input do
  not block or repeat prompts.
- World/tile/region consumers run only after their dependencies are ready.
- Hook order is explicit where required.
- Targeted tests and a production startup/shutdown smoke check are distinguished.

## Reference Routing

- Read `dev-docs/server-lifecycle.md` before moving code between phases.
- Load `modernuo-configuration` for settings, `modernuo-events` for lifecycle
  events, `modernuo-threading` for loop/continuation behavior, and
  `modernuo-world-saves-archives` for post-snapshot backup work.
