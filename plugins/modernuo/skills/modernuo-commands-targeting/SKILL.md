---
name: modernuo-commands-targeting
description: Use when creating, reviewing, or changing ModernUO in-game commands, access levels, CommandEventArgs parsing, Target subclasses, or command-to-target flows. Covers registration, validation, stale-target safety, evidence limits, and focused tests. Do not use for migrating legacy registrations or for gump-only interactions.
license: MIT
metadata:
  version: "1.2.0"
---

# ModernUO Commands and Targeting

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own new or changed bracket commands and interactive targeting. Use [modernuo-migrate-commands-events](../modernuo-migrate-commands-events/SKILL.md) for RunUO/ServUO conversion. For UI-only flows, inspect a current local gump precedent; do not route to an absent generic gump skill.

## Workflow

1. Require access to the local ModernUO source/test environment plus the actor, access policy, arguments, target kinds, range/LOS/ground policy, side effects, cancellation behavior, and local APIs. If any prerequisite, security-relevant policy, or API cannot be verified, return `BLOCKED` with the smallest missing input; do not select a default.
2. Define the observable success/failure behavior and inspect the current local `CommandSystem.Register`, `CommandEventArgs`, and `Target` APIs plus the nearest command of equal privilege.
3. Register the command in `Configure()` with the least required `AccessLevel`; add accurate `[Usage]` and `[Description]`.
4. Validate argument count and parse failures before any mutation. Return a precise usage/error message without exposing privileged data.
5. Create a narrowly scoped `Target` with explicit range, ground, flags, and type handling. After validating command input, assign it to the actor using the locally verified target API. Verify replacement, cancellation, and concurrent-target semantics from current local behavior; do not assume a target cursor survives or is replaced safely. Revalidate access, ownership, deletion, map, range, LOS, and mechanic-specific rules inside `OnTarget`.
6. Keep harmful/beneficial flags aligned with locally verified notoriety and combat semantics. Handle cancel and stale/invalid targets without partial mutation.
7. Test unauthorized, malformed, valid, wrong-type, out-of-range/LOS, deleted/stale, and cancel paths.

## Safety gates

- Never rely only on the access check performed at command dispatch; delayed target responses can be stale.
- Do not use unlimited range or disabled LOS without a documented staff/tool requirement.
- Keep mutations atomic after all validation and log privileged destructive actions where local precedent does.
- Do not assume typed accessors distinguish missing from invalid input; inspect their implementation.
- Do not put blocking or background work in a command/target callback.
- When a command changes gameplay content or player-visible mechanics, require and label OSI/EA/Broadsword evidence for the gameplay claim. Treat local code and the ModernUO guide as implementation/API evidence only; if official evidence is unavailable, report the claim as unresolved and request policy direction.

## Verification/self-check

Run the permission/input/target matrix, inspect logs and side effects, and confirm delayed responses revalidate current state. Recheck that no path mutates before all validation succeeds.

## Output contract

Return these sections in order: `Outcome` (`IMPLEMENTED`, `REVIEWED`, `BLOCKED`, or `OUT_OF_SCOPE`); `Command and Target Contract`; `Evidence and Confidence` (local APIs/paths inspected and limits); `Verification`; and `Manual In-Game Checks`. Every verification row records scenario, expected result, actual result, command/test method, and log/test evidence. Use `high` confidence only with verified local APIs, relevant test evidence, and official evidence for any gameplay claim; `medium` with named incomplete checks; and `low` for `BLOCKED` or unresolved claims. If reviewing, report findings without editing. For `BLOCKED`, state the unresolved access, targeting, API, or prerequisite decision and the smallest input needed. For `OUT_OF_SCOPE`, name the applicable handoff without treating it as blocked.

## Reference routing

- Read [commands-targeting-patterns.md](references/commands-targeting-patterns.md) for API shapes and test cases.
- When a command opens UI or changes game content, inspect the corresponding current local precedent and its lifecycle/authorization path before implementation.
- Cross-check the official [ModernUO commands and targeting guide](https://modernuo.com/docs/development/commands-and-targeting/).
