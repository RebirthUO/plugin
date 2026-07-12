---
name: modernuo-symbol-discipline
description: >
  Use when deciding whether ModernUO-based C# values should be inline,
  locals, constants, static readonly objects, fields, properties, or explicit
  Policy* surfaces. Report overexposure as a warning; do not rewrite existing
  symbols unless cleanup was requested or the user confirms the change.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - modernuo
      - rebirthuo
      - symbols
      - naming
      - code-style
    related_skills:
      - modernuo-code-audit
      - modernuo-no-publish-prefix-names
      - modernuo-test-naming
---

# ModernUO Symbol Discipline

## Boundary

Every symbol must justify its lifetime, scope, visibility, and semantic value.
This is a warning/recommendation lens, not permission for behavior or public API
changes.

## Workflow

1. Find all consumers, reflection/string references, serialization/config/
   command exposure, tests, docs, and client-visible uses.
2. Classify the value with the decision ladder below.
3. Choose the narrowest scope and stable mechanic name. Preserve source/parity
   evidence without embedding ticket or publish labels in the identifier.
4. Report the candidate and ask before rewriting unless the request explicitly
   asks for symbol cleanup.
5. If changed, run reference search plus focused build/tests and confirm no
   behavior or compatibility surface changed unintentionally.

## Decision Ladder

1. Inline obvious one-use values that do not name policy or a formula term.
2. Use locals for reuse, snapshots, side-effect avoidance, or meaningful steps.
3. Use `const` for reusable compile-time rules with durable consumers/evidence.
4. Use `static readonly` for shared runtime objects or identity.
5. Use fields for persistence, timers, ownership, caches, and changing state.
6. Use properties for engine/public/serialized/config/client contracts, not
   wrappers that merely rename another value.

## Policy Names

`Policy*` means a deliberate configured-project decision where official sources
are incomplete or the project intentionally chooses custom behavior. Era gating
alone is not policy.
Require a mechanic-specific name and at least one durable reason: reuse, focused
tests, parity documentation, or a stable downstream consumer. Keep it private or
internal unless public access is genuinely needed.

## Output Contract

```text
[SYMBOL] WARNING: {unnecessary, vague, or overexposed symbol}
  File: {path}:{line}
  Consumers/contracts: {evidence}
  Suggestion: {inline|local|const|static readonly|field|property|rename}
  Compatibility: {none|serialization|reflection|config|public API}
```

For implementation, also return old/new mappings, access-level changes, source
evidence location, and verification.

## Verification

- The symbol is reused, exposed, tested/documented, required by a contract, or
  names a non-obvious decision.
- Scope is no wider than its actual consumers.
- `Policy*` denotes explicit policy rather than era context.
- Reference search/build/tests show no compatibility or behavior change.

## Reference Routing

- Read [symbol decision examples](references/symbol-decision-examples.md) when a
  local, wrapper property, or `Policy*` surface is ambiguous.
- Load `modernuo-no-publish-prefix-names` when the symbol embeds source publish
  numbers and `modernuo-test-naming` when the symbol is a test identity.
- Load the serialization/configuration/API owner before changing a contract name.
