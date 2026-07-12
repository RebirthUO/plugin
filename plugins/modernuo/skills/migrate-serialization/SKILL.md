---
name: migrate-serialization
description: Use when migrating RunUO Serialize/Deserialize methods, Serial constructors, Constructable attributes, or saved fields to ModernUO generated serialization. Covers new types, generated version bumps, legacy manual saves, TypeAlias identity, schemas, and post-load restoration. Do not use for global system files; use persistence migration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: migration
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, runuo, migration, serialization, saves]
    related_skills:
      - migrate-foundation
      - modernuo-serialization
      - modernuo-code-audit
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-content-patterns
---

# RunUO to ModernUO Serialization Migration

## Boundary

Own entity/type save compatibility. Use [migrate-persistence](../migrate-persistence/SKILL.md) for global non-entity data.

## Mode gate

Choose exactly one mode before editing:

1. **New generated type:** `[SerializationGenerator(0)]`, `partial`, indexed persistent fields, and `[Constructible]` when appropriate.
2. **Generated version bump:** increment the version, implement the required `MigrateFrom(VXContent)`, regenerate the schema, and keep prior schemas.
3. **Legacy manual migration:** read old write/read order and version encoding first; retain a compatible legacy reader, use the correct encoded-version setting, and add `TypeAlias` when saved type identity changed.

## Workflow

1. Load [migrate-foundation](../migrate-foundation/SKILL.md). Record type identity, inheritance, every version branch, exact field order/type, defaults, deleted fields, and runtime-only state.
2. Inspect the current generator attributes and a nearby migration in the repository.
3. Convert persistent members with stable indices. Preserve command-property access and property invalidation attributes.
4. Use generated setters or `this.MarkDirty()` for custom persistent mutations.
5. Remove manual methods and `Serial` constructors only after the selected mode provides an old-save path.
6. Restore timers/caches/registrations in the appropriate after-deserialization phase; never serialize execution tokens.
7. Run the repository schema generator when required, then test new round trip, each supported old version, renamed types, deleted/null references, and unsupported versions.

## Safety gates

- Never infer legacy field order from declarations; read `Serialize` and `Deserialize`.
- Do not reuse a field index for different meaning.
- Do not assign migrated data back to obsolete backing fields when generated setters carry dirty/invalidation behavior.
- Preserve generated schema files and document rollback/backup implications.

## Verification/self-check

Compare every supported old version with the migration map, run schema generation/build and round-trip tests, and inspect the final diff for missing schemas, reused indices, or serialized runtime handles.

## Output contract

Return the selected mode, field/version/identity map, code and schema changes, old-save and rollback plan, verification commands/results, and any unsupported legacy version.

## Reference routing

- Read [modernuo-serialization](../modernuo-serialization/SKILL.md) for local attributes and generator commands.
- Read [modernuo-lifecycle-cleanup](../modernuo-lifecycle-cleanup/SKILL.md) when post-load state owns timers or references.
- Cross-check with the official [ModernUO serialization guide](https://modernuo.com/docs/development/serialization/) and [SerializationGenerator repository](https://github.com/modernuo/SerializationGenerator) when local behavior is unclear.
