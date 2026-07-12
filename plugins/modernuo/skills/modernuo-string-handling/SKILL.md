---
name: modernuo-string-handling
description: >
  Use when constructing ModernUO runtime strings with interpolation handlers,
  ValueStringBuilder, message/gump/packet APIs, or replacing StringBuilder in
  repeated game code. Use modernuo-property-lists for IPropertyList's distinct
  literal-as-delimiter semantics.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, strings, interpolation, performance, gumps]
    related_skills:
      - modernuo-code-audit
      - modernuo-performance-hot-paths
      - modernuo-property-lists
      - modernuo-gump-system
      - modernuo-networking
      - modernuo-content-patterns
---

# ModernUO String Handling

## Boundary

Choose the lowest-allocation repository-native text path without obscuring
correctness. Handler-aware APIs should receive interpolation directly; assembled
or reusable text should use `Server.Text.ValueStringBuilder`. This skill does not
define tooltip delimiter semantics.

## Workflow

1. Identify the consumer and path class: handler-aware message/gump/property/
   packet call, span consumer, stored `string`, or cold tooling output.
2. For one direct call, keep the `$"..."` literal in argument position so the
   interpolated-string-handler overload binds.
3. For multi-step assembly, use a bounded stack-backed `ValueStringBuilder` when
   the maximum is known; use `ValueStringBuilder.Create()` when growth is
   unbounded and dispose it reliably.
4. Pass `AsSpan()` when the consumer accepts spans; call `ToString()` only at a
   boundary that truly requires an owned string.
5. Compare allocations/behavior with the prior implementation and cover culture,
   casing, escaping, encoding, and maximum-length cases relevant to the caller.

## Guardrails

- Do not use `System.Text.StringBuilder` in ModernUO runtime/game string assembly.
- A ternary/switch expression of interpolated branches, pre-built interpolated
  local, `string.Format`, concatenation inside a hole, `.ToString()` inside a
  hole, or LINQ aggregation usually creates intermediate strings.
- Branch the call itself when text differs so each branch retains direct handler
  binding.
- Use the `:L` format specifier where the ModernUO handler supports lowercase;
  do not allocate via `ToLowerInvariant()`.
- `using var` is appropriate unless a helper takes the builder by `ref`; in that
  case use explicit `try/finally`/`Dispose()` because a using variable cannot be
  passed by ref.
- `Reset()` reuses one builder; `Append` returns `void` and is not chainable.
- Culture-sensitive output must be intentional and tested; do not silently force
  invariant formatting.

## Output Contract

Return the consumer/overload selected, allocation boundary, capacity strategy,
format/culture decisions, changed paths, and verification. Performance claims
must identify whether allocations were measured or only inferred statically.

## Verification

- Confirm the intended overload binds and no unnecessary intermediate `string`
  remains.
- Test maximum expected length/growth and disposal on exceptional paths.
- Test culture/casing/escaping/encoding cases that affect visible output.
- Report focused tests and allocation measurements separately.

## Reference Routing

- Read [interpolation and ValueStringBuilder patterns](references/interpolation-patterns.md)
  when converting complex branches, capacity sizing, or ref extensions.
- Load `modernuo-property-lists` for tooltip arguments, `modernuo-networking` for
  packet encodings, and `modernuo-gump-system` for layout/HTML behavior.
- Read `dev-docs/string-handling.md` for the current handler inventory.
