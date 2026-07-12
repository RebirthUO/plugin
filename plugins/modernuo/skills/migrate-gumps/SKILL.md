---
name: migrate-gumps
description: Use when converting RunUO Gump subclasses, layout calls, SendGump patterns, or OnResponse handlers to ModernUO DynamicGump or StaticGump. Covers type selection, builders, placeholders, DisplayTo validation, and response safety. Do not use for new UI design unrelated to migration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, gumps, ui]
    related_skills:
      - migrate-foundation
      - modernuo-gump-system
      - modernuo-string-handling
      - modernuo-code-audit
      - modernuo-content-patterns
---

# RunUO to ModernUO Gump Migration

## Boundary

Convert an existing gump without changing its player-facing behavior unless requested. Use [modernuo-gump-system](../modernuo-gump-system/SKILL.md) for new UI architecture.

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Inventory pages, controls, button/text-entry IDs, state, validation, and callers.
2. Choose `StaticGump<T>` for fixed layout with per-instance placeholders; choose `DynamicGump` when control count or structure varies.
3. Move layout calls into the matching `BuildLayout(ref ...Builder)`; use `BuildStrings` for static-layout dynamic text.
4. Replace legacy flags with builder methods and update responses to `OnResponse(NetState, in RelayInfo)`. Preserve stable button, switch, and entry IDs; button `0` remains close/cancel.
5. Put prerequisite checks in a static `DisplayTo` method before construction. Make the constructor private when that prevents invalid instances.
6. Replace send/close calls with the local generic gump APIs and add `Singleton` only when stacking is not intended.
7. Verify at least success, cancel, invalid/stale response, and prerequisite-failure paths.

## Safety gates

- Never send an empty gump; a client may be unable to dismiss it.
- Revalidate authority, ownership, range, and object state in `OnResponse`; displayed state may be stale.
- Keep handler-aware interpolated strings at the call site and do not invent cliloc IDs.
- Remove temporary `Cached => false` overrides before delivery.

## Verification/self-check

Prove no constructed path is empty, IDs remain stable, responses revalidate stale state, and success/cancel/invalid paths pass focused tests. Record any visual client check still manual.

## Output contract

Return the migrated class/call sites, chosen gump type and rationale, an ID/state mapping, validation evidence, and remaining client-data or manual-UI checks.

## Reference routing

- Read [modernuo-gump-system](../modernuo-gump-system/SKILL.md) for builder APIs, empty-gump rules, and response validation.
- Read [modernuo-string-handling](../modernuo-string-handling/SKILL.md) only when interpolation, HTML, or localization changes.
