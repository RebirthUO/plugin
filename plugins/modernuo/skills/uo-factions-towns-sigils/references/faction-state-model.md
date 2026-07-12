# Faction State Model

Use this reference for Factions enablement, registries, membership/rank state, persistence, timers, and lifecycle. Re-read current source before relying on numeric policy.

## Source map

| Surface | Current anchors |
|---|---|
| Enablement/persistence | `Projects/UOContent/Engines/Factions/Core/FactionSystem.cs` |
| Faction aggregate | `Core/Faction.cs`, `Core/FactionState.cs` |
| Player membership/rank | `Core/PlayerState.cs`, `Definitions/RankDefinition.cs` |
| Discovery/definitions | `Core/Reflector.cs`, `Definitions/FactionDefinition.cs`, `Instances/Factions/**` |
| Regions | `Core/StrongholdRegion.cs`, faction/town region consumers |
| Staff/reset paths | commands in `Core/Faction.cs` and related controllers |

## Aggregate relationships

```text
Faction
  -> FactionState
     -> Members[PlayerState]
     -> Commander
     -> Election
     -> faction Silver/Tithe
     -> FactionItems
     -> Traps

Town
  -> TownState
     -> Owner Faction
     -> Sheriff / Finance officers
     -> town Silver / Tax / Income time
     -> GuardLists / VendorLists
```

`PlayerState.Attach` connects a persisted faction record back to `PlayerMobile.FactionPlayerState`. Rank is derived from sorted kill-point position and cached; membership mutation must preserve list order, zero-rank offset, rank indexes, office links, commander/election state, and property/notoriety invalidation.

## Enablement

`FactionSystem.Configure` reads the feature setting and registers `GenericPersistence` only when enabled. Current `Enable`/`Disable` methods toggle persistence/configuration; comments explicitly say they do not create or remove faction world objects.

Therefore:

- enabling persistence does not prove stones, monoliths, regions, guards, vendors, or sigils exist;
- disabling persistence is not a safe teardown;
- feature-state changes require a world-object inventory, explicit generation/removal plan, save boundary, and restart test.

Do not present a configuration toggle as a complete operational migration.

`Enable()` does not generate controllers. `Disable()` unregisters persistence without removing regions, timers, members, sigils, guards, or vendors; continued mutation may stop being saved.

## Join and leave lifecycle

Current `Faction` owns join validation and member removal. Paths include solo and guild-mediated join plus delayed leave/kick/reset.

Trace:

1. actor/account/guild/young/ban/overlap and faction-balance checks;
2. `AddMember` creation and attachment of `PlayerState`;
3. initial faction item/equipment and notoriety/property effects;
4. leave request timestamp and delayed completion;
5. `RemoveMember` rank-list cleanup, sigil return, election/vote removal, office/commander release, equipment validation, point redistribution, and attachment removal.

The exact requirements, delays, balance formulas, and starter items are official-evidence gated.

## Timers and derived state

Current systems use timers for elections, atrophy, process ticks, town income, faction items/traps, sigils, leave completion, and related effects. Persistent timestamps and collections are durable; timer objects are runtime state.

`PlayerState.SilverGiven` anti-farm history and active faction skill-loss timers are runtime-only in current main. Restart clears them; do not claim those controls or penalties are durable.

On load:

- faction and town definitions must be discovered in the same stable order used by serialized references;
- `FactionState` and `TownState` reattach to their definition instances;
- member ranking and offices are rebuilt consistently;
- faction items/traps validate attachment/decay;
- recurring timers start once.

Top-level saves do not carry stable faction/town identifiers or explicit counts, and reflection discovery has no explicit sort contract. Changing definition order can remap serialized references. Treat it as a compatibility change and test old saves.

## Cleanup and resets

Reset/admin commands are destructive operational tools. Inventory members, offices, elections, sigils, towns, guards/vendors, faction items, traps, regions, and persistence before use. Require a save/rollback boundary and verify world objects plus in-memory registries after restart.

## Verification

Add focused tests for disabled/enabled startup, definition/reference stability, join rejection/success, guild join, delayed leave, kick/reset, rank reordering, commander/office cleanup, election/vote cleanup, current and legacy persistence, restart-cleared anti-farm/skill-loss state, one-time timer registration, and feature-toggle limitations. No direct Factions, Sigil, or `TownState` suite was found in the inspected tree; report missing test harnesses explicitly.
