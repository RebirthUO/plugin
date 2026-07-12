---
name: migrate-systems
description: >
  Use when converting multi-file RunUO engines or systems such as crafting, spawners, economy, or quests to ModernUO.
  Covers system mapping, conversion order, file organization, cross-reference handling, and lifecycle cleanup.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, systems, engines, lifecycle]
    related_skills:
      - migrate-foundation
      - migrate-persistence
      - migrate-serialization
      - migrate-commands-events
      - modernuo-configuration
      - modernuo-events
      - modernuo-lifecycle-cleanup
      - modernuo-code-audit
---

# RunUO -> ModernUO Multi-File System Migration

## When to Use
- Converting RunUO systems with multiple interdependent files
- Converting custom engines (crafting, spawners, economy, quests)
- Organizing RunUO `Scripts/Custom/` code into ModernUO structure

## Conversion Order
1. **Data types / enums** -- Just naming and namespace changes
2. **Persistence classes** -- `EventSink.WorldSave` -> `GenericPersistence`
3. **Core entities (Items/Mobiles)** -- Full serialization migration
4. **Gumps** -- Convert to `DynamicGump`/`StaticGump`
5. **Commands** -- Usually minimal changes
6. **Packets** -- Convert to `SpanWriter` if custom packets exist
7. **Entry point** -- Update Configure/Initialize registration

## File Organization
| RunUO | ModernUO |
|---|---|
| `Scripts/Custom/MySystem/` | `Projects/UOContent/Engines/MySystem/` or `Projects/UOContent/Systems/MySystem/` |
| `Scripts/Items/X.cs` | `Projects/UOContent/Items/{Category}/X.cs` |
| `Scripts/Mobiles/X.cs` | `Projects/UOContent/Mobiles/{Category}/X.cs` |
| `Scripts/Gumps/X.cs` | `Projects/UOContent/Gumps/X.cs` |

## Configuration Migration
| RunUO | ModernUO |
|---|---|
| XML config files | `ServerConfiguration.GetOrUpdateSetting()` or `JsonConfig` |
| Custom .cfg parsing | `ServerConfiguration` for simple, `JsonConfig` for complex |

## Testing
After converting: `dotnet build`, fix errors, test [add for items, verify gumps, check persistence across save/restart.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/10-systems-engines.md` -- detailed system migration patterns
- `dev-docs/configuration.md` -- ModernUO configuration system
- `plugins/modernuo/skills/modernuo-configuration/SKILL.md` -- ModernUO configuration skill
- All other migrate-* skills for system-specific guidance
