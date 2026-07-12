# AoS Item-Property Architecture

This reference describes implementation surfaces, not official property values.
Establish the named property's behavior and chronology through
`uo-official-evidence`, then re-locate every repository symbol at the target
revision.

## Property surfaces

Treat these as independent decisions:

| Surface | Questions |
|---|---|
| Storage | Persistent roll, item-specific field, or runtime-only state? |
| Staff API | How is the value inspected and changed safely? |
| Duplication | Does `Dupe` copy it, reset it, or derive it? |
| Persistence | Version/schema, migration, old-save behavior, rollback |
| Tooltip | Cliloc/text, arguments, order, invalidation, era suppression |
| Aggregation | Which equipped item families contribute and how are caps applied? |
| Consumer | Exact event/hook, ordering, raw versus applied values |
| Lifecycle | Expiry, unequip, death, delete, logout, map and save/load |
| Distribution | Loot, runic, reforging, imbuing, crafting, artifact, event |
| Tests | Positive, negative, boundary, host, era, cleanup, round trip |

Storage/display/mechanics do not authorize distribution.

## Storage decision

1. Inspect current containers and serialization rather than copying historical
   enum values.
2. Use an existing container only when the family semantics, aggregation, and
   persistence contract match.
3. A new overflow/family container needs a unique bit or key, staff wrapper,
   default/dupe behavior, versioned persistence, old-save tests, and all owning
   item-family integrations.
4. Keep temporary target/count/timer state outside serialized attribute
   containers unless the official contract requires save persistence.
5. Do not access internal attribute dictionaries directly; use the owning
   setters so property invalidation and stat updates run.

Read `aos-property-container-taxonomy.md` before selecting a container and
`extended-weapon-attribute-refactor.md` only when existing capacity or family
ownership is the actual problem.

## Tooltip and client presentation

- Verify candidate clilocs from configured client data through the repository's
  localization reader/decompressor.
- A client string proves its text/ID, not server mechanics.
- Test property-list ID, arguments, order, cache invalidation, supported hosts,
  and pre-era suppression.
- Runtime display state should remain runtime state when it is not a persistent
  rollable property.

## Gameplay consumer

Define before coding:

- trigger and position in the pipeline;
- raw versus post-mitigation/applied values;
- chance, formula, cap, units, and rounding;
- PvP/PvM differences;
- cooldown, stacking, refresh, immunity, and resource consumption;
- valid/invalid targets and supported item hosts;
- cleanup for every exit boundary.

Do not place a hook at a convenient method without tracing the actual live
consumer. Another engine may help locate a hook shape but cannot supply the
official behavior.

## Distribution boundary

Search every applicable generator after implementation and state whether it is
unchanged. A found-on marker or official item example does not automatically
authorize random loot, crafting, imbuing, runic, reforging, event, or artifact
rollout. Distribution changes require explicit scope and economy review.

## Validation matrix

```markdown
| Surface | Evidence | Test/result |
|---|---|---|
| default and staff API | current repository symbols | ... |
| duplication | owning item family | ... |
| serialization/migration | schema/version | ... |
| tooltip and invalidation | verified client/repo API | ... |
| aggregation | supported/unsupported hosts | ... |
| gameplay trigger/order | behavior contract | ... |
| caps and boundaries | official/custom decision | ... |
| cleanup | every lifecycle edge | ... |
| pre-era suppression | configured era/profile | ... |
| non-distribution | generator search | ... |
```

Run the owning build, focused property tests after the final edit, adjacent
pipeline tests for shared hooks, and broader tests in proportion to risk.
