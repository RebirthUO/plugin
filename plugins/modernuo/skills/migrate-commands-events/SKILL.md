---
name: migrate-commands-events
description: Use when converting RunUO command registration, EventSink subscriptions, event delegates, or handler signatures to ModernUO. Covers startup registration, renamed connection events, generated events, and persistence handoff. Do not use for command/target design or new event APIs; use the corresponding modernuo-* skill.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, commands, events]
    related_skills:
      - migrate-foundation
      - modernuo-commands-targeting
      - modernuo-events
      - modernuo-configuration
      - modernuo-code-audit
      - migrate-persistence
---

# RunUO to ModernUO Commands and Events

## Boundary

Own migration of existing command registrations, EventSink hooks, delegate wrappers, and handler signatures. Do not redesign command permissions, targeting behavior, or a new event surface here.

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md), then inspect the source registration site, handler signatures, lifetime, and every subscriber.
2. Verify the current local ModernUO event or command declaration; never migrate a remembered name or delegate shape.
3. Register process-lifetime commands and static EventSink handlers in `Configure()`. Remove obsolete delegate constructors and pass method groups directly.
4. Map renamed connection hooks deliberately: RunUO login/logout patterns commonly become `Connected`, `BeforeDisconnected`, or `Disconnected`; choose by required lifecycle semantics, not name similarity.
5. Use attribute-driven `[OnEvent]` handlers only for an existing generated event. Do not also subscribe the same handler manually.
6. Pair instance, reloadable, temporary, or disableable subscriptions with deterministic unsubscription. Route custom world-save files to [migrate-persistence](../migrate-persistence/SKILL.md).
7. Build the owning project and exercise registration, permission rejection, event firing, and cleanup.

## Safety gates

- Preserve the command's access level, argument validation, and player-type checks.
- Do not equate disconnect, logout, death, and deletion; cleanup requirements differ.
- Keep event handlers short and game-loop safe.
- Do not remove legacy persistence until old saves have a tested load path.

## Verification/self-check

Confirm current declarations/signatures, one registration per handler, correct lifetime cleanup, and focused command/event tests. Re-scan for leftover RunUO delegate wrappers and old hook names before completion.

## Output contract

Return the migrated registrations and handlers, an old-to-new hook map with lifetime rationale, files changed, verification commands/results, and any unresolved lifecycle or save-compatibility risk. If only analysis was requested, report findings without editing.

## Reference routing

- For new command permissions or targeting, read [modernuo-commands-targeting](../modernuo-commands-targeting/SKILL.md).
- For generated-event definitions, subscription lifetime, and handler behavior, read [modernuo-events](../modernuo-events/SKILL.md).
- For a repository-independent API cross-check, consult the official [ModernUO commands and targeting guide](https://modernuo.com/docs/development/commands-and-targeting/).
