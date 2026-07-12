---
name: modernuo-gump-system
description: Use when creating or changing ModernUO StaticGump, DynamicGump, builders, placeholders, SendGump/CloseGump flows, or response handling. Covers layout choice, non-empty construction, stale-response authorization, handler-aware strings, and tests. Do not use for migrating legacy RunUO gumps; use migrate-gumps.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, gumps, ui, static-gump, dynamic-gump]
    related_skills:
      - modernuo-code-audit
      - modernuo-string-handling
      - modernuo-commands-targeting
      - modernuo-content-patterns
      - modernuo-test-workflow
      - migrate-gumps
---

# ModernUO Gump System

## Boundary

Own new/current ModernUO gump architecture and behavior. Use [migrate-gumps](../migrate-gumps/SKILL.md) for legacy conversion.

## Workflow

1. Define audience, state owner, fixed versus variable structure, singleton/stacking policy, all controls/IDs, authorization, cancellation, localization, and stale-response behavior.
2. Read [gump-patterns.md](references/gump-patterns.md) and inspect the exact local base/builder APIs plus a sibling gump.
3. Choose `StaticGump<T>` for a stable cached layout with placeholders; choose `DynamicGump` when structure/control count varies per instance.
4. Validate prerequisites before construction in a static `DisplayTo` method. Build at least one visual/dismissible element on every constructed path.
5. Use stable nonzero action button IDs; reserve `0` for close/cancel. Use placeholders/handler-aware interpolated literals without prebuilding strings.
6. In `OnResponse`, revalidate access, actor, target/object identity, deletion, ownership, map/range, and current system state before mutation.
7. Test display rejection, layout path, success, cancel, invalid ID/text/switch, stale/deleted/moved state, repeated open/singleton, and unauthorized response.

## Safety gates

- Never send an empty gump; it can leak an undismissable client/server slot.
- Do not trust state captured when displayed; responses are delayed, user-controlled input.
- Do not leave `Cached => false` in production.
- Escape/limit user text according to the local HTML/text API and verify clilocs rather than inventing IDs.
- Keep dynamic lists bounded and avoid heavy work during layout serialization.

## Verification/self-check

Test non-empty display, all action/cancel/invalid inputs, stale authorization, singleton/stacking, and per-instance strings. Record manual visual/client validation separately from automated behavior checks.

## Output contract

Return selected gump type and rationale, layout/control/state contract, changed files, authorization and stale-state checks, focused verification evidence, and remaining manual client/UI checks.

## Reference routing

- Always read [gump-patterns.md](references/gump-patterns.md).
- Read [modernuo-string-handling](../modernuo-string-handling/SKILL.md) for HTML/interpolation/localization and [modernuo-commands-targeting](../modernuo-commands-targeting/SKILL.md) when UI launches a target flow.
