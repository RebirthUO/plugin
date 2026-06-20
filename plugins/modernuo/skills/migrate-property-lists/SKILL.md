---
name: migrate-property-lists
description: >
  Trigger: when converting RunUO GetProperties(ObjectPropertyList) to ModernUO GetProperties(IPropertyList). Critical string literal rule.
  Covers: IPropertyList interface, string hole rule, cliloc arguments.
---

# RunUO -> ModernUO Property List Migration

## When This Activates
- Converting `GetProperties(ObjectPropertyList list)` overrides
- Updating tooltip/property list code

## Conversion Steps
1. Change signature: `GetProperties(ObjectPropertyList list)` -> `GetProperties(IPropertyList list)`
2. Convert string args to interpolation: `list.Add(num, val.ToString())` -> `list.Add(num, $"{val}")`
3. Apply string hole rule: `$"Text\t{val}"` -> `$"{"Text"}\t{val}"`
4. Tab-separated: `string.Format("{0}\t{1}", a, b)` -> `$"{a}\t{b}"`
5. Cliloc as argument: `"#" + cliloc` -> `$"{cliloc:#}"`

## Critical Rule: String Literals Must Be Holes
Only `\t` should be a bare literal. All text must be inside `{}` holes:
```csharp
// BAD: "Map" is a delimiter
list.Add(1060658, $"Map\t{value}");
// GOOD: "Map" is an argument
list.Add(1060658, $"{"Map"}\t{value}");
```

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/06-property-lists.md` -- detailed migration reference
- `dev-docs/property-lists.md` -- complete ModernUO property list system
- `plugins/modernuo/skills/modernuo-property-lists/SKILL.md` -- ModernUO property list skill
