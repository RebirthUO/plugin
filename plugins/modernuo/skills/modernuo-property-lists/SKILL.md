---
name: modernuo-property-lists
description: >
  Use when implementing or reviewing ModernUO GetProperties,
  AddNameProperties, IPropertyList/ObjectPropertyList tooltip entries, cliloc
  arguments, property ordering, or invalidation. Do not apply its special
  literal-as-delimiter rule to ordinary message or gump interpolation handlers.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, property-lists, tooltips, cliloc, strings]
    related_skills:
      - modernuo-code-audit
      - modernuo-serialization
      - modernuo-string-handling
      - modernuo-era-expansion
      - modernuo-content-patterns
      - migrate-property-lists
---

# ModernUO Property Lists

## Boundary

Own client tooltip content, localization arguments, relative entry order, and
refresh behavior. Ordinary messages, gumps, and packet strings use different
handlers; route their formatting to `modernuo-string-handling`.

## Workflow

1. Identify the expected cliloc/raw text, argument count/order, era gate, desired
   position, and state changes that should refresh the tooltip.
2. Inspect `Item`/`Mobile` base property emission and a neighboring implementation.
3. Use `GetProperties()` and call `base.GetProperties(list)` first for normal
   appended entries. If the entry must immediately follow name/weight, override
   `AddNameProperties()`, call its base first, then emit the entry.
4. Encode arguments with the `IPropertyList` handler rules and use clilocs where
   stable localized text exists.
5. Add `[InvalidateProperties]` to generated serialized fields or call
   `InvalidateProperties()` when non-generated/non-serialized display state
   changes.
6. Test entry number, arguments, relative order, era presence/absence, and refresh
   behavior at the smallest reliable layer.

## Guardrails

- In `IPropertyList` interpolation, bare literal text is a delimiter. Put human
  text/string constants in holes; normally only `\t` remains bare:
  `list.Add(1060658, $"{"Charges"}\t{charges}")`.
- Do not copy that rule to normal `RawInterpolatedStringHandler` message/gump
  APIs, where literal text is correct.
- Pass values directly in holes; `.ToString()`, concatenation, pre-built strings,
  ternaries, and LINQ formatting allocate or defeat handler binding.
- When an argument is itself a cliloc, use `{number:#}` or `AddLocalized`, not a
  string such as `"#1060000"`.
- Do not append an entry when source/client ordering requires it between base
  name properties and later equipment properties.
- Avoid invalidating in tight loops; invalidate only when visible state changes.

## Output Contract

Return the emitted entry sequence (cliloc/raw, arguments, era gate), chosen hook,
invalidation source, changed paths, and test evidence. For reviews, identify the
exact malformed argument, ordering, or stale-tooltip risk.

## Verification

- Base entries remain present and custom entries appear in the required order.
- Recorded arguments distinguish delimiters, text, values, and cliloc references.
- Target-era and pre-era cases both pass when gated.
- State changes rebuild the tooltip once; unchanged state does not churn it.
- Focused property-list tests/build results are reported with actual scope.

## Reference Routing

- Read [property-list formatting and ordering](references/property-list-formatting.md)
  for concrete cliloc/handler examples.
- Read [recording test doubles](references/recording-property-list-test-doubles.md)
  only when `IPropertyList` interface additions break private test doubles.
- Load `modernuo-serialization` for generated invalidation and
  `modernuo-era-expansion` for expansion gates.
