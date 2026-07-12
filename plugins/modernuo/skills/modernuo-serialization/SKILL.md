---
name: modernuo-serialization
description: >
  Use when adding or changing ModernUO generated serialization, persistent
  fields/properties, version migrations, legacy readers, GenericPersistence, or
  save/load restoration. Treat changes as save-compatibility work; do not use
  for generic JSON/configuration serialization.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, serialization, saves, migration, codegen]
    related_skills:
      - modernuo-code-audit
      - modernuo-content-patterns
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-property-lists
      - migrate-serialization
---

# ModernUO Serialization

## Boundary

Persistent layout is a compatibility contract. Classify every change as a new
generated type, a generated-version transition, a pre-codegen legacy migration,
or custom/global persistence before editing.

## Workflow

1. Inspect the current class, generated attributes, migration JSON, prior
   versions, legacy read/write order, aliases, timers, and custom setters.
2. For a new generated type, use a `partial` class and version `0`; add
   `[Constructible]` when the content is intended for the in-game add command.
3. For an existing generated type, preserve field indexes, bump the generator
   version for layout changes, create the previous-version migration content,
   and generate/commit the schema with the repository's migration command.
4. For pre-codegen data, preserve the exact old read order and encoded/plain
   version format in the legacy deserializer; do not use that path for normal
   post-codegen bumps.
5. Persist durable state only. Restore timers, caches, registrations, and derived
   state in the appropriate after-deserialization hook.
6. Build the owning project immediately, inspect generated/schema output, and run
   old-save/default/new-round-trip coverage proportional to risk.

## Guardrails

- `[SerializableField(N)]` indexes are save-format contracts; never reorder or
  reuse one casually.
- Custom serialized-property setters must call `this.MarkDirty()` and invalidate
  properties when visible tooltip state changes.
- Never serialize `TimerExecutionToken`. Persist deadline/state and restart on
  load; cancel the runtime token on deletion.
- Custom `Serialize()` may run on background serialization workers. It must only
  read stable fields and write the stream: no entity mutation/deletion, timers,
  packets, `NetState`, or shared mutable state.
- Use synchronous `[AfterDeserialization]` only for own-state restoration. Use
  `false` when other entities must exist or the hook may delete/register/mutate
  world state.
- Build immediately around high field/save-flag indexes; generated flag types
  can expose representation mismatches. Prefer no flag when defaults are safe.

## Output Contract

Return the change classification, version/field map, compatibility path,
generated/migration artifacts, runtime restoration/cleanup, tests, and rollback
risk. State missing old-save evidence.

## Verification

- New/default values, round trip, previous generated version, and legacy stream
  are covered as applicable.
- Migration schema exists and matches indexes/save flags.
- Generated code and the owning solution/project compile.
- Timer/runtime state restores once and delete/load transitions stay safe.

## Reference Routing

- Read [generated fields, migrations, and persistence patterns](references/serialization-migrations.md)
  for attribute selection, schema generation, and legacy examples.
- Load `migrate-serialization` for RunUO/manual-to-generated conversion,
  `modernuo-timers` for time-based state, and `modernuo-property-lists` for
  generated tooltip invalidation.
- Consult `dev-docs/serialization.md` and the current ModernUO serialization docs
  before relying on remembered generator behavior.
