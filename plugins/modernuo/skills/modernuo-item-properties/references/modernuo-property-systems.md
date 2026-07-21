# ModernUO Property Systems

Use this map to locate an existing implementation before adding item-property
storage. Names and paths are candidates, not assumptions: verify their presence
at the consuming repository's pinned revision.

## Inspect First

- The property-list interface and implementation, including interpolation,
  localized arguments, chunked free-text support, and invalidation.
- The base item type, relevant weapon/armor/clothing/jewelry/talisman/quiver
  type, and the nearest equivalent `GetProperties` implementation.
- The repository's AoS attribute, weapon-attribute, armor-attribute,
  element-attribute, skill-bonus, slayer, item-set, craft-resource, and
  quiver-specific types.
- The active serialization and expansion-gate documentation and focused test
  helpers.

## Storage Selection

Choose in this order:

1. An existing property on the owning item type.
2. An existing shared attribute family that already owns equivalent semantics.
3. An existing focused subsystem such as skills, slayers, talismans, item sets,
   craft resources, or quivers.
4. New content-level state with the repository's serialization/migration
   contract.
5. Engine-level item state only with explicit scope approval.

In current ModernUO-style sources, `AosAttributes` commonly aggregates shared
equipped bonuses, while weapon and armor attribute types own more specialized
effects. Confirm the exact enum member, era behavior, display order, and
aggregation method before using any of them.

## Aggregation and Display

Use the existing static aggregator or item lifecycle hook rather than scanning
equipment ad hoc. Match the local update pattern for resistances, stat mods,
skills, mobile deltas, or timers; no update call is universally correct. Test
the aggregate with the item equipped and removed, and assert the OPL number and
arguments independently of the gameplay assertion.

## Implementation Limits

- Do not create a broad abstraction until repetition in the current repository
  proves it is needed.
- Do not introduce a later-era property into an earlier attribute family without
  checking current era and persistence conventions.
- Do not substitute raw display text for a localized mapping unless that exact
  local category already uses a raw fallback.
- Preserve current repository behavior unless the requested contract explicitly
  authorizes a parity correction.
