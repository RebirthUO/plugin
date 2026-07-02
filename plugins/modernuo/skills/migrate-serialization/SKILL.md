---
name: migrate-serialization
description: >
  Use when converting RunUO Serialize/Deserialize methods, adding [SerializableField], converting [Constructable] to [Constructible], or migrating manual serialization code.
  Covers source-generated serialization, field conversion, version handling, TypeAlias, and post-load restoration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, runuo, migration, serialization, saves]
    related_skills:
      - migrate-foundation
      - modernuo-serialization
      - modernuo-code-audit
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-content-patterns
---

# RunUO -> ModernUO Serialization Migration

## When to Use
- Converting `Serialize(GenericWriter)`/`Deserialize(GenericReader)` overrides
- Converting `[Constructable]` to `[Constructible]`
- Adding `[SerializableField]` attributes
- Handling save compatibility with `[TypeAlias]`

## Migration Mode Decision

Before editing serialization, classify the task. Do not mix these modes casually:

1. **New ModernUO class**
   - Use `[SerializationGenerator(0)]`.
   - Omit the `encoded` argument.
   - Add `partial` to the class.
   - Add `[Constructible]` where the type should be addable/constructible in game.

2. **Existing generated ModernUO class version bump**
   - Increment `[SerializationGenerator(N)]`.
   - Add `private void MigrateFrom(VXContent content)` for the previous version.
   - Do **not** edit legacy `Deserialize(reader, version)` for normal generated-code bumps.
   - Regenerate and commit migration schema JSON.

3. **Pre-codegen RunUO/manual serialization migration**
   - Read old `Serialize()` first and preserve the old field write/read order exactly.
   - Convert old `Deserialize(GenericReader)` to `private void Deserialize(IGenericReader reader, int version)` only for old-save compatibility.
   - If old `Serialize()` wrote the version with `writer.Write(version)` / `reader.ReadInt()`, use `[SerializationGenerator(N, false)]`.
   - Add `[TypeAlias]` when the namespace or class name changed and old saves may still reference the old type.
   - Keep legacy compatibility code only as long as old saves need to load.

Completion criterion: the migration notes identify which mode is being used and how old saves will load after the change.

## Conversion Steps
1. Add `using ModernUO.Serialization;`
2. Read the old `Serialize()` to find the version number it writes. Bump it by 1 for `[SerializationGenerator]`
3. If old `Deserialize()` used `reader.ReadInt()` (not `ReadEncodedInt()`), pass `false` as second parameter: `[SerializationGenerator(N, false)]`
4. Add `partial` to class declaration
5. Convert each serialized field: `private int m_X` -> `[SerializableField(N)] private int _x`
6. Add `[SerializedCommandProperty(AccessLevel.X)]` if RunUO had `[CommandProperty]`
7. Add `[InvalidateProperties]` if setter called `InvalidateProperties()`
8. DELETE the `Serial` constructor
9. DELETE the `Serialize()` override
10. Convert `Deserialize()` to `private void Deserialize(IGenericReader reader, int version)` to handle pre-codegen saves (remove `override`, `base.Deserialize()`, and version read line). Delete entirely if no existing saves.
11. Change `[Constructable]` to `[Constructible]`
12. Timer fields and other runtime-only state: leave unserialized and restore in `[AfterDeserialization]`; use `[AfterDeserialization(false)]` when setup depends on fully loaded cross-entity/world state or affects game state

## Quick Mapping
| RunUO | ModernUO |
|---|---|
| `public class Foo : Item` | `[SerializationGenerator(N, false)] public partial class Foo : Item` (N = old version + 1) |
| `private int m_X` + manual Serialize | `[SerializableField(0)] private int _x` |
| `[CommandProperty(GM)]` on property | `[SerializedCommandProperty(GM)]` on field |
| `Foo(Serial serial) : base(serial)` | DELETE |
| `Serialize(GenericWriter)` | DELETE -- auto-generated |
| `Deserialize(GenericReader)` | Convert to `private void Deserialize(IGenericReader reader, int version)` for old saves |
| Custom setter with InvalidateProperties() | `[InvalidateProperties]` attribute |
| Custom setter logic | `[SerializableProperty(N)]` with `this.MarkDirty()` |
| `reader.ReadMobile()` | `reader.ReadEntity<Mobile>()` |
| `reader.ReadItem()` | `reader.ReadEntity<Item>()` |

## Anti-Patterns
- Missing `partial` keyword -> build error
- Serializing `TimerExecutionToken` -> build error
- Missing `this.MarkDirty()` in `[SerializableProperty]` setter -> changes not saved
- Wrong field prefix (`m_` instead of `_`)

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/02-serialization.md` -- detailed migration reference with before/after
- `dev-docs/serialization.md` -- complete ModernUO serialization system
- `plugins/modernuo/skills/modernuo-serialization/SKILL.md` -- ModernUO serialization skill (patterns, attributes, examples)
