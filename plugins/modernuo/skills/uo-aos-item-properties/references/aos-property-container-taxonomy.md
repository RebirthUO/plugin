# AoS Property Container Taxonomy

Use this reference to choose storage ownership after the named property's
official contract and current repository shape are known.

## Decisions

1. Treat AoS as the item-property architecture, not proof that every property
   belongs in the original containers or era.
2. Prefer a container whose name describes item family or mechanic ownership.
   Do not create one container per expansion unless ownership is genuinely
   expansion-specific.
3. Put chronology in the property's tooltip, consumer, aggregation,
   distribution, and tests. Storage alone does not make a property active.
4. Inspect current bit/key capacity and serialization before selecting a value.
   Never copy a value or “next free bit” from a reference, issue, or another
   branch.
5. Avoid widening a persisted mask or changing container representation without
   a migration and compatibility plan. A neutral family overflow container may
   be safer when existing capacity is exhausted.

## Persistent-container checklist

- current free value/key verified at target revision;
- semantic owner and supported item families identified;
- staff wrapper and safe setter/invalidation path;
- constructor/default and duplication behavior;
- save flag/version/schema and legacy load/migration;
- old-save and round-trip tests;
- tooltip and consumer era suppression;
- equipped aggregation for each supported host;
- distribution unchanged unless explicitly approved.

## Runtime-state boundary

Target identity, counters, stacks, cooldowns, expiry tokens, and active effects
normally belong to cancellable runtime contexts rather than rollable property
storage. Persist them only when the ready behavior contract requires save
continuity and defines migration and cleanup.
