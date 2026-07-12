# Extended Weapon Attribute Refactor

Use when the current weapon-property container has insufficient capacity or
mixed ownership and the approved work is a storage-system refactor rather than
one property.

## Design

- Re-locate current containers, bits/keys, serializers, item-family ownership,
  staff APIs, aggregation, consumers, and tests at the target revision.
- Prefer a neutral weapon-family overflow container over an expansion-named
  container when properties from multiple eras share the storage mechanism.
- Keep each property's activation era in its own tooltip, aggregation,
  consumer, distribution, and tests.
- Do not widen or reinterpret a persisted mask without generated schema/version
  changes, explicit old-save mapping, collision analysis, rollback, and tests.
- Keep old storage readable for compatibility; migrate once through the owning
  serializer and avoid dual-write ambiguity.

## Migration matrix

```markdown
| Old owner/value | New owner/value | Introduced version | Collision check | Old-save test |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

## Integration checklist

- container construction and lazy/default behavior;
- item duplication;
- serialization, generated schema, and old saves;
- staff wrappers and property invalidation;
- tooltip and equipped aggregation for every supported weapon family;
- all gameplay consumers;
- pre-era no-op behavior;
- loot/runic/reforging/imbuing/artifact/event distribution unchanged;
- focused migration/property tests plus adjacent shared-pipeline tests.

Refactoring storage does not authorize mechanic, balance, or distribution
changes. Any missing mapping or official behavior returns to research.
