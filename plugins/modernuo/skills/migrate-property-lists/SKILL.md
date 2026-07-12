---
name: migrate-property-lists
description: Use when converting RunUO GetProperties(ObjectPropertyList) overrides or tooltip arguments to ModernUO IPropertyList. Covers interpolation arguments, cliloc formatting, and the property-list-only string-hole rule. Do not use for ordinary messages, gump text, or general localization work.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, property-lists, cliloc]
    related_skills:
      - migrate-foundation
      - modernuo-property-lists
      - modernuo-string-handling
      - modernuo-code-audit
      - modernuo-content-patterns
---

# RunUO to ModernUO Property-List Migration

## Boundary

Convert tooltip/property-list overrides and arguments only. The string-hole rule in this skill is specific to `IPropertyList`; do not apply it to messages or gump handlers.

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Inventory each cliloc, argument order, tab delimiter, conditional property, and invalidation source.
2. Change the override to the current `GetProperties(IPropertyList list)` signature and preserve the base call/order.
3. Convert arguments to direct interpolated holes. In property-list interpolation, wrap literal argument text as holes (for example, `$"{"Map"}\t{value}"`); leave only protocol delimiters such as `\t` literal.
4. Use the supported cliloc formatter for cliloc-as-argument values and preserve numeric/culture formatting.
5. Verify unknown IDs through repository localization/client data when exact text matters; do not invent labels.
6. Test base and conditional tooltips, argument order, invalidation after mutation, and the earliest supported era/client.

## Safety gates

- Do not call `.ToString()` merely to feed a handler-aware interpolation.
- Do not change a cliloc or its argument count without verified client text.
- Keep player-provided text escaped/encoded according to the local property-list API.
- Preserve `InvalidateProperties` behavior after persistent or visible state changes.

## Verification/self-check

Verify each cliloc's argument count/order and conditional visibility, then test invalidation and the target client/era. Re-scan that the property-list-only hole rule did not leak into normal strings.

## Output contract

Return changed overrides, a cliloc/argument map, any verified client text, invalidation notes, test/build evidence, and unresolved localization risk.

## Reference routing

- Read [modernuo-property-lists](../modernuo-property-lists/SKILL.md) for exact handlers and formatting.
- Read [modernuo-string-handling](../modernuo-string-handling/SKILL.md) only when adjacent message/gump strings also change.
