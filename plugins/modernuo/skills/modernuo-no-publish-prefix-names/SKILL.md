---
name: modernuo-no-publish-prefix-names
description: Use when naming ModernUO/RebirthUO functions, variables, constants, fields, helpers, tests, or other symbols for era/publish-sourced mechanics. Prevents `PublishXX` or publish-number prefixes in symbol names; keep publish numbers in comments, PR text, docs, source evidence, or test display data instead.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, rebirthuo, naming, publish, era, code-style]
    related_skills: [modernuo-code-audit, uo-modernuo-workflow, modernuo-era-expansion]
---

# ModernUO No Publish-Prefix Symbol Names

## Overview

Use this skill when creating or reviewing ModernUO/RebirthUO code symbols that describe behavior sourced from an Ultima Online publish, era note, or parity ticket.

Publish numbers are evidence, not domain names. A symbol named `Publish30PoisonCloudMaxDamage` bakes a research citation into runtime code and makes future maintenance awkward when the same mechanic is shared across eras, sources, or later publishes. Prefer stable mechanic names in code, and put the publish/source evidence in comments, PR bodies, docs, or test display data.

## When to Use

- Adding or renaming C# constants, fields, locals, methods, helper classes, test helpers, or fixture names.
- Implementing UO mechanics with official publish evidence, e.g. Publish 30, Publish 64, Publish 96.
- Reviewing PRs that introduce symbols with `PublishXX`, `PubXX`, `PXX`, or similar publish-number prefixes.
- Source-locking mechanics in RebirthUO/ModernUO while keeping gameplay code readable.

## Naming Rule

Do not use publish-number prefixes for symbols:

```csharp
// Bad
private const int Publish30PoisonCloudMaxDamage = 25;
private static bool Publish64AllowsHumanLmcBonus(...)
var pub96RequiredTactics = 60;

// Good
private const int PoisonCloudMaxDamage = 25;
private static bool AllowsHumanLmcBonus(...)
var requiredTactics = 60;
```

Publish numbers may remain in evidence-bearing text:

```csharp
// Source-locked to Publish 30: ranged poison cloud for Serado/Yamandon.
private const int PoisonCloudMaxDamage = 25;
```

Allowed places for publish numbers:

- Comments explaining source evidence.
- PR bodies and review comments.
- `dev-docs/` parity ledgers.
- Test data display names or comments when the test proves a source row.
- Issue titles, labels, and source-reference strings.

Disallowed places:

- Function names.
- Variable names.
- Constant names.
- Field names.
- Property names.
- Helper class names.
- Test method names, unless the publish number is the exact named behavior under test and no cleaner domain name exists; prefer source comments over method-name prefixes.

## Replacement Pattern

1. Identify the domain mechanic.
2. Name the symbol after the mechanic, range, cap, or rule.
3. Move publish/source evidence to an adjacent comment or the PR evidence section.
4. Keep tests proving the sourced values.

Examples:

| Bad | Good |
|---|---|
| `Publish30PoisonCloudMinDamage` | `PoisonCloudMinDamage` |
| `Publish30PoisonCloudMaxDamage` | `PoisonCloudMaxDamage` |
| `Publish96PrimaryTacticsRequirement` | `PrimaryTacticsRequirement` |
| `Publish64HumanLmcExcluded` | `HumanLmcBonusExcluded` |

## Verification Checklist

- [ ] No new or modified symbol starts with `Publish`, `Pub`, or `P` followed by a publish number.
- [ ] The mechanic name is stable without the source citation.
- [ ] Source/publish evidence remains visible in a nearby comment, PR body, or test assertion note.
- [ ] Tests still prove the published values or behavior.
- [ ] No gameplay behavior changed just to satisfy naming.

## Common Pitfalls

1. **Deleting evidence instead of moving it.** Keep the publish number in comments/docs/PR evidence when it matters.
2. **Over-generalizing names.** `MaxDamage` alone may be too vague; `PoisonCloudMaxDamage` is clear.
3. **Renaming public serialized members casually.** If a symbol participates in serialization, save data, packet fields, config keys, or public APIs, check compatibility before renaming.
4. **Using publish names as test method prefixes.** Prefer `SeradoCounterUsesRangedPoisonCloudDamageRange` with a source comment over `Publish30SeradoCounter...`.
