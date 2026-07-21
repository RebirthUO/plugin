# Source Checks for Item Properties

Use this reference only when the task makes or changes a player-facing gameplay
claim. Implementation code establishes the local seam; it does not establish
live-game behavior.

## Evidence Order

1. Current official OSI, EA, or Broadsword material for player-facing gameplay.
2. Explicit user-approved shard policy or target behavior, labeled as custom
   policy rather than official behavior.
3. Current repository source and tests for implementation facts.
4. Community pages, client data, emulators, and historical notes only as
   separately labeled technical cross-checks.

If the requested formula, eligibility, lifecycle, cap, era, or display behavior
is not established by official evidence, retain the official claim as unresolved
and return `BLOCKED` with the smallest decision needed. A user-approved custom
policy may authorize local behavior, but must never be presented as official
evidence. Never let a technical cross-check fill an official-evidence gap.

## Local Checks

- Search the pinned repository for the property name, likely cliloc, neighboring
  property emission, storage type, and test coverage.
- Inspect the active property-list implementation before constructing localized
  arguments or free-text entries.
- Inspect the current expansion gates and serialization generator before
  asserting an era or persistence behavior.
- Keep conflicts explicit in the result's evidence records; identify whether the
  conflict changes mechanics, display, migration, or tests.

## Common Risks

- A tooltip name alone does not prove a mechanic.
- A similar item does not establish chance, cooldown, duration, or load-time
  behavior.
- Negative properties can affect durability, insurance, blessing, transfer,
  weight, or repair paths beyond their display line.
- Defensive and proc properties need the verified incoming-damage, parry, or hit
  seam plus a non-triggering test.
