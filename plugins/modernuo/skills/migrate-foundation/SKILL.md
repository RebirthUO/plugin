---
name: migrate-foundation
description: >
  Use when migrating any RunUO code to ModernUO. Load this foundation skill before specialized migrate-* skills.
  Covers namespace changes, naming conventions, attribute renames, logging, threading, and performance.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, foundation, csharp]
    related_skills:
      - migrate-serialization
      - migrate-items-mobiles
      - migrate-timers
      - migrate-gumps
      - migrate-packets
      - migrate-property-lists
      - migrate-commands-events
      - migrate-persistence
      - migrate-systems
      - modernuo-code-audit
      - modernuo-serialization
      - modernuo-lifecycle-cleanup
      - modernuo-threading
      - modernuo-performance-hot-paths
---

# RunUO -> ModernUO Foundation Migration

## When to Use
- Converting ANY RunUO 2.7 script to ModernUO
- Always apply these changes FIRST before system-specific migration

## Migration Chain

For any RunUO migration, apply skills in this order:

1. `migrate-foundation` — universal syntax, naming, threading, logging, and performance changes.
2. `migrate-serialization` — when the script has `Serialize`/`Deserialize`, save data, `[Constructable]`, `Serial` constructors, or old-save compatibility risk.
3. System-specific migration skill — items/mobiles, timers, gumps, packets, commands/events, property lists, persistence, or multi-file systems.
4. Relevant `modernuo-*` runtime skill — serialization, timers, gumps, property lists, content patterns, threading, or other runtime behavior.
5. `modernuo-code-audit` — final convention, safety, and hot-path pass.
6. `modernuo-test-workflow` — build/test/validation where available.

Completion criterion: every migrated script names which chain entries applied and why skipped entries were not needed.

## Universal Changes Checklist
1. File-scoped namespace: `namespace X { ... }` -> `namespace X;`
2. `using ModernUO.Serialization;` -- add for any serializable type
3. Rename fields: `m_FieldName` -> `_fieldName`
4. `[Constructable]` -> `[Constructible]`
5. `Console.WriteLine` -> `LogFactory.GetLogger(typeof(X))` -> `logger.Information(...)`
6. `DateTime.UtcNow` -> `Core.Now`
7. `World.Mobiles`/`World.Items` iteration -> spatial queries (`map.GetMobilesInRange<T>()`)
8. Remove `lock`, `volatile`, `ConcurrentDictionary`, `Mutex` -- server is single-threaded
9. Remove `Task.Run`, `new Thread` -- use `Timer.StartTimer()` instead
10. `ArrayPool<T>.Shared` -> `STArrayPool<T>.Shared`
11. `new List<T>()` on hot paths -> `PooledRefList<T>.Create()`
12. Modernize property syntax: `{ get { return x; } }` -> `{ get => x; }`
13. Delete `MyType(Serial serial) : base(serial)` constructor -- auto-generated
14. `Name = "text"` in constructor -> `public override string DefaultName => "text";`

## Quick Reference
| RunUO | ModernUO |
|---|---|
| `[Constructable]` | `[Constructible]` |
| `m_Field` | `_field` |
| `Console.WriteLine(...)` | `logger.Information(...)` |
| `DateTime.UtcNow` | `Core.Now` |
| `MyItem(Serial serial) : base(serial)` | DELETE |
| `lock (_obj) { }` | Remove entirely |
| `ConcurrentDictionary` | `Dictionary` |
| `ArrayPool<T>.Shared` | `STArrayPool<T>.Shared` |

## Anti-Patterns
- Don't rename existing `m_` fields in code you're not otherwise migrating
- Don't add threading constructs -- everything is single-threaded
- Don't use allocating LINQ (`.ToList()`, `.GroupBy()`, etc.) on hot paths

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/01-foundation-changes.md` -- complete foundation changes reference
- `dev-docs/code-standards.md` -- ModernUO coding standards and LINQ tiers
- `plugins/modernuo/skills/modernuo-performance-hot-paths/SKILL.md` -- Hot/warm/cold path classification for migration performance choices
- `dev-docs/threading-model.md` -- Why single-threaded, what's allowed
