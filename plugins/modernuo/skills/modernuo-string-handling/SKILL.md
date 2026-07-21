---
name: modernuo-string-handling
description: >
  Use when implementing or reviewing ModernUO runtime string construction with
  interpolated-string handlers, Server.Text.ValueStringBuilder, message/gump
  APIs, packet text, span consumers, or repeated game-code assembly. Route
  IPropertyList delimiter semantics to modernuo-property-lists.
metadata:
  version: 1.2.0
---

# ModernUO String Handling

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Required Evidence

Before choosing an implementation, inspect the consuming repository at its
current revision and record the call site, candidate overload declarations, and
tests or callers that establish ownership, lifetime, culture, and encoding.
Never infer handler support from a method name or from this skill.

If the repository, overload inventory, required lifetime, capacity bound, or
observable formatting contract cannot be established, stop with `blocked`, name
the missing evidence, and request the smallest input needed to continue.

## Workflow

1. Classify the consumer as handler-aware, span-only, owned `string`, encoded
   packet text, property-list arguments, or cold tooling output.
2. Verify the selected overload in source. For a single handler-aware call, keep
   interpolation directly in argument position.
3. For multi-step assembly, use `Server.Text.ValueStringBuilder` only after
   establishing its API and disposal contract at the inspected revision. Use a
   bounded stack buffer only when a safe maximum is evidenced; otherwise use the
   repository's growth-capable factory.
4. Keep text borrowed with `AsSpan()` only while the builder remains alive. Use
   `ToString()` where the consumer stores or outlives the buffer.
5. Preserve visible output, culture, casing, escaping, encoding, and exceptional
   cleanup. Verify maximum expected growth.
6. Compare behavior and allocations with the previous implementation. Label
   allocation conclusions as measured or statically inferred.

## Guardrails and Handoffs

- Do not prescribe `System.Text.StringBuilder` replacement until the call site,
  frequency, and repository-native alternative are verified.
- Branch the handler-aware call when ternary or switch construction would create
  an intermediate string.
- Confirm repository support before using custom format specifiers such as `:L`,
  ref extensions, `Reset()`, or a particular builder factory.
- Load [interpolation and builder patterns](references/interpolation-patterns.md)
  for complex branches, capacity, disposal, and lifetime examples.
- Hand off property-list delimiters to `modernuo-property-lists`, packet encoding
  to `modernuo-networking`, gump HTML/layout behavior to `modernuo-gump-system`,
  measurement design to `modernuo-performance-hot-paths`, and broad review to
  `modernuo-code-audit`.

## Output Contract

Return exactly these fields:

- `Status`: `ready` or `blocked`.
- `Consumer and overload`: inspected symbol plus repository evidence location.
- `Construction strategy`: direct handler, bounded builder, growth-capable
  builder, borrowed span, or owned string.
- `Allocation and ownership boundary`: buffer owner, lifetime, and escape point.
- `Capacity rationale`: evidenced bound or reason growth is required.
- `Culture and encoding`: preserved contract and relevant cases.
- `Changed paths`: files changed, or `none` for review-only work.
- `Verification`: focused behavior, length, cleanup, and regression checks.
- `Performance evidence`: `measured`, `statically inferred`, or `not assessed`.
- `Blocker`: `none`, or the missing evidence and smallest next input.

## Completion Check

Do not return `ready` unless the overload exists at the inspected revision,
ownership and lifetime are safe, visible output is preserved, relevant maximum
length and exceptional cleanup are covered, and every performance claim has the
required evidence label.
