---
name: modernuo-commands-targeting
description: Use when creating or changing ModernUO in-game commands, access levels, CommandEventArgs parsing, Target subclasses, or command-to-target flows. Covers registration, validation, stale-target safety, and focused tests. Do not use for migrating legacy registrations or for gump-only interactions.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, commands, targeting, admin-tools, interactions]
    related_skills:
      - modernuo-code-audit
      - modernuo-gump-system
      - modernuo-content-patterns
      - modernuo-threading
      - modernuo-test-workflow
      - migrate-commands-events
---

# ModernUO Commands and Targeting

## Boundary

Own new or changed bracket commands and interactive targeting. Use [migrate-commands-events](../migrate-commands-events/SKILL.md) for RunUO conversion and [modernuo-gump-system](../modernuo-gump-system/SKILL.md) for UI-only flows.

## Workflow

1. Define the actor, minimum access level, arguments, target kinds, range/LOS/ground policy, side effects, cancellation, and observable success/failure.
2. Inspect the current local `CommandSystem.Register`, `CommandEventArgs`, and `Target` APIs plus the nearest command of equal privilege.
3. Register the command in `Configure()` with the least required `AccessLevel`; add accurate `[Usage]` and `[Description]`.
4. Validate argument count and parse failures before any mutation. Return a precise usage/error message without exposing privileged data.
5. Create a narrowly scoped `Target` with explicit range, ground, flags, and type handling. Revalidate access, ownership, deletion, map, range, LOS, and mechanic-specific rules inside `OnTarget`.
6. Keep harmful/beneficial flags aligned with notoriety and combat semantics. Handle cancel and stale/invalid targets without partial mutation.
7. Test unauthorized, malformed, valid, wrong-type, out-of-range/LOS, deleted/stale, and cancel paths.

## Safety gates

- Never rely only on the access check performed at command dispatch; delayed target responses can be stale.
- Do not use unlimited range or disabled LOS without a documented staff/tool requirement.
- Keep mutations atomic after all validation and log privileged destructive actions where local precedent does.
- Do not assume typed accessors distinguish missing from invalid input; inspect their implementation.
- Do not put blocking or background work in a command/target callback.

## Verification/self-check

Run the permission/input/target matrix, inspect logs and side effects, and confirm delayed responses revalidate current state. Recheck that no path mutates before all validation succeeds.

## Output contract

Return registration and target changes, the permission/input/target contract, changed files, focused verification evidence, and remaining manual in-game checks. If reviewing, report findings without editing.

## Reference routing

- Read [commands-targeting-patterns.md](references/commands-targeting-patterns.md) for API shapes and test cases.
- Read [modernuo-gump-system](../modernuo-gump-system/SKILL.md) when a command opens UI and [modernuo-content-patterns](../modernuo-content-patterns/SKILL.md) when it mutates game content.
- Cross-check the official [ModernUO commands and targeting guide](https://modernuo.com/docs/development/commands-and-targeting/).
