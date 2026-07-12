---
name: modernuo-no-publish-prefix-names
description: >
  Use when naming ModernUO-based symbols for mechanics sourced from an
  Ultima Online publish. Keep publish numbers in evidence comments, tests, docs,
  issues, or PR text, not in runtime symbol prefixes. Do not rename serialized,
  packet, config, or public contracts without a compatibility review.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, rebirthuo, naming, publish, era, code-style]
    related_skills: [modernuo-code-audit, modernuo-codebase, modernuo-era-expansion]
---

# ModernUO No Publish-Prefix Symbol Names

## Boundary

Publish numbers identify evidence, not stable game concepts. Name functions,
fields, constants, helpers, properties, and tests after the mechanic they own;
retain the source citation beside that mechanic. This is a naming-only rule and
must not change gameplay.

## Workflow

1. Search new and modified symbols for `PublishNN`, `PubNN`, `PNN`, and equivalent
   era-ticket prefixes.
2. Identify the stable mechanic, range, cap, formula, or operation the symbol
   represents.
3. Rename to that domain concept at the narrowest useful scope.
4. Move the publish/source citation to an adjacent comment, source-locked test
   note, parity ledger, issue, or PR evidence section.
5. Search references and check compatibility surfaces before applying a rename.

```csharp
// Source-locked to Publish 30.
private const int PoisonCloudMaxDamage = 25;
```

## Guardrails

- Do not delete evidence while removing it from an identifier.
- Avoid vague replacements such as `MaxDamage`; retain enough domain context,
  such as `PoisonCloudMaxDamage`.
- Publish numbers are acceptable in comments, source strings, issue/PR text,
  parity docs, and test display data when they identify the evidence row.
- Keep a publish/era word in a symbol only when it names an actual product type
  or domain contract, not merely when that era supplied the value.
- Renaming serialized members, migration fields, reflection targets, packet
  fields, configuration keys, or public APIs requires an explicit compatibility
  check and may be out of scope.

## Output Contract

Return each old/new symbol mapping, where the source citation was retained, any
compatibility-sensitive symbol left unchanged, and the validation performed.
For audit-only requests, report candidates without editing.

## Verification

- No new or modified symbol begins with a publish-number label.
- Source evidence remains discoverable near the implementation or test.
- Reference search shows no unresolved call sites or reflection/string users.
- Diff/build/tests confirm that only naming changed when rename-only work was
  requested.

## Reference Routing

- Load `modernuo-symbol-discipline` when the question is whether a symbol should
  exist or how visible it should be.
- Load `modernuo-test-naming` for broader test file/class/method normalization.
- Load `modernuo-era-expansion` when the code behavior itself varies by era.
