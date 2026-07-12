# Faction Economy and Integration

Use this reference for silver/tithe/town cash flow, guards/vendors/items/traps, and Factions links to death, combat, notoriety, stealing, regions, equipment, and UI.

## Economy surfaces

Current anchors include:

- `Projects/UOContent/Engines/Factions/Core/Faction.cs`
- `Core/FactionState.cs`, `Core/Town.cs`, `Core/TownState.cs`
- `Core/GuardList.cs`, `Core/VendorList.cs`
- `Definitions/GuardDefinition.cs`, `VendorDefinition.cs`, `FactionItemDefinition.cs`
- `Mobiles/Guards/**`, `Mobiles/Vendors/**`
- `Items/Silver.cs`, `Items/FactionItem.cs`, `Items/Power Faction Items/**`, `Items/Traps/**`

Separate these ledgers:

- faction treasury and tithe;
- town treasury, tax, income, and guard/vendor upkeep;
- physical `Silver` items delivered to players;
- kill points/rank;
- ethics power/history where integrated;
- faction-item and trap ownership/expiration.

Never transfer a value between ledgers merely because each is called a reward or currency.

## Transaction review

For silver awards, town income, tax changes, guard/vendor hiring, faction item imbue/purchase, trap placement, and power-item drops:

1. Identify actor role and authoritative ledger.
2. Revalidate faction/town ownership, office, rank, region/facet, target, cost, capacity, and cooldown.
3. Compute in a wide type and define clamp/overflow behavior.
4. Debit before or atomically with creation only when failure compensation is proven.
5. Register created guards/vendors/items/traps with exactly one owner list.
6. Invalidate UI/properties and persist timestamps/balances.
7. On deletion/capture/reset, unregister and reverse owned resources once.

Town income can delete hired guards/vendors until cash flow is affordable. Test collection mutation, random selection, unregister callbacks, and restart so repeated income processing cannot double-delete or double-charge.

Normal vendor purchase pricing consumes faction town tax through `BaseVendor`; a tax change is therefore a cross-domain commerce change. Current capture handling does not reset every tax-related cooldown implied by historical documentation, so verify intended era behavior rather than copying a publish note into current code.

Finance, sheriff, and town-stone responses generally revalidate role/ownership, but `FactionImbueGump` currently revalidates item possession and silver without equivalently proving current faction, town control, or vendor proximity. Add stale-gump tests after expulsion, capture, role loss, movement, and item transfer.

## Integration map

| Concern | Current integration to inspect | Owning neighbor |
|---|---|---|
| Faction death rewards/penalties | `Faction.HandleDeath`, player/creature death call sites | `uo-combat-pipeline` owns damage/death causation |
| Notoriety/criminality | notoriety handlers and faction relation checks | combat owner for generic notoriety |
| Sigil theft | `Skills/Stealing.cs`, `Sigil.cs` | `uo-items-foundation` for generic stealing/item transfer |
| Stronghold/town location | `StrongholdRegion.cs`, town region definitions | `uo-world-facets-regions` |
| Guards/vendors | faction mobile definitions and town lists | `uo-vendors-commerce` for generic transaction behavior |
| Gumps/targets | `Engines/Factions/Gumps/**` | `modernuo-gump-system` |
| Equipment/items | `FactionItem`, imbue gump, equipment validation | `uo-items-foundation` / property skills |
| Persistence | `FactionSystem`, state serializers | `modernuo-serialization` |

Keep Factions policy in this domain and shared mechanics in the neighbor. Add an integration test when either side's contract changes.

## Feature and era boundaries

Factions are configurable and current code contains inherited historical behavior. Before changing values or eligibility:

- establish whether the target is historical Factions, a later official system, or custom shard policy;
- verify feature/profile enablement and world-object reachability;
- use official sources for timers, costs, rewards, ranks, restrictions, and facet rules;
- label repository-only observations as implementation evidence.

Do not conflate Factions with guild wars, Ethics, Vice versus Virtue, or ordinary Felucca PvP.

## Verification

Create focused tests for each ledger's debit/credit, insufficient funds, overflow, duplicate requests, office/rank denial, stale gumps, tax/vendor price scaling, town capture cleanup and cooldowns, income/upkeep, guard/vendor register/delete, item/trap expiration, death reward controls, same/enemy faction notoriety, sigil stealing integration, save/load, and reset rollback. Where tests are absent, report the gap and use bounded admin/client checks without claiming conformance.
