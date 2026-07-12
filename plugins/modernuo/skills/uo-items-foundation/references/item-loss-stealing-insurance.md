# Item Loss, Stealing, and Insurance

Use this reference when tracing item ownership through player death, corpse allocation/looting, Stealing, blessing, or insurance. Re-check active code and official evidence before relying on values or era rules.

## Source map

| Surface | Current anchors |
|---|---|
| Core item state | `Projects/Server/Items/Item.cs` (`LootType`, `Insured`, `PaidInsurance`, `BlessedFor`, `DeathMoveResult`) |
| Player death/insurance | `Projects/UOContent/Mobiles/PlayerMobile.cs` |
| Corpse rights/lifecycle | `Projects/UOContent/Items/Misc/Corpses/Corpse.cs` |
| Corpse presentation | `Items/Misc/Corpses/CorpsePackets.cs` and focused tests |
| Stealing | `Projects/UOContent/Skills/Stealing.cs` |
| Stealable artifacts | `Projects/UOContent/Engines/Stealables/StealableArtifacts.cs` |
| Feature setting | `Projects/UOContent/Configuration/ExpansionConfiguration.cs` |

## State vocabulary

Keep these independent:

- `LootType` controls broad death/theft semantics (`Regular`, `Newbied`, `Blessed`, `Cursed`).
- `BlessedFor` is actor-specific protection.
- `Insured` is current insurance selection.
- `PaidInsurance` records paid coverage/renewal state used by insurance flows.
- `QuestItem`, `Nontransferable`, movability, parent chain, house security, and domain-specific flags add separate restrictions.
- `DeathMoveResult` decides corpse, backpack, or retained-equipment movement for one death transition.

Do not collapse them into a generic protected flag. A state can block stealing while still allowing trade, or survive death while remaining movable.

## Death allocation

Trace the production order:

1. `OnBeforeDeath` snapshots equipment and identifies insurance-award context.
2. The engine enumerates equipped and inventory items and calls the player's parent/inventory move-result hooks.
3. `PlayerMobile.CheckInsuranceOnDeath` may charge renewal, change `PaidInsurance`/`Insured`, award an opposing player, and return protected movement.
4. Base item/LootType logic selects corpse, backpack, or retained placement for unprotected items; young/duel/domain rules may override.
5. `Corpse` captures owner/notoriety/aggressor/killer/equipment/restore state and starts decay.
6. `OnDeath` performs criminal/notoriety, insurance messaging, faction and other subsystem effects.

Mutation order matters. Test item-state changes and gold transfers even when later corpse creation or subsystem hooks fail.

Only direct equipped/backpack children are classified by the ordinary death pass. Current AoS pre-death handling hoists nested blessed/insured items before classification; other nested contents follow their containing parent. Include container-parent retention in the disposition matrix.

## Corpse rights

`Corpse` owns looter/aggressor snapshots, instanced visibility, criminal-action checks, item use/lift authorization, restore placement, and decay. Current criminality considers owner, staff, party loot permission, notoriety, map rules, and corpse/player/creature state.

Review:

- owner and party access;
- murderer/criminal/aggressor/killer snapshots across owner deletion/restart;
- instanced item visibility versus actual lift permission;
- harmful-restriction facets;
- self-loot/equipment restore;
- carved/generated corpse items;
- looter recording and criminal/notoriety side effects;
- decay/bones/delete timer cleanup.

Packet visibility is presentation only. A client not seeing an item is not server authorization.

## Stealing flow

Current `Stealing`:

1. Opens a short-range target and revalidates empty hands, region, actor/target state, young/guild/murder restrictions, vendor and staff exclusions, visibility, capacity, movability, protection flags, equipped/corpse/container restrictions, range, weight/amount, and harmful permission.
2. Handles faction sigils through a separate state path.
3. Performs the production skill check and splits stacks when needed.
4. Moves a successful item to the thief, applies criminal/notoriety/perma-flag effects, and records eligible items in an in-memory stolen-item queue.
5. If the thief dies before queue expiry, the player-death event attempts to return the stolen item to its victim.

The stolen-item queue is runtime-only. Explicitly test restart behavior and avoid presenting it as durable recovery. Clean expired/deleted entries and ensure stack splits preserve the correct item identity.

Current death return additionally requires the stolen item's root parent to be the killed thief's corpse. Insurance or another retained containing parent can keep the item in the backpack and bypass that check. Treat insuring a recently stolen item and every retained-parent variant as high-priority exploit tests; fix the ownership contract rather than only the visible insurance path.

## Insurance interaction

Insurance UI/target callbacks must revalidate that the player is alive and the item remains equipped or under that player's backpack, is still insurable, and has current paid/insured state. Gump item arrays and selected booleans are stale client-time snapshots.

At death, auto-renew may withdraw funds, retain coverage, or clear coverage when funds are insufficient; an eligible killer may receive an award. Treat item movement, player debit, killer credit, status messages, and persistence as one reviewed transaction even though current code mutates them in stages.

In the inspected flow, an insured item is retained for the current death even when auto-renew fails and clears both insurance flags. Cancellation also clears `Insured` while paid state may remain reusable. Test current-death disposition separately from post-death coverage state and UI totals, which may include items that do not require an immediate debit.

Exact cost, award, eligibility, auto-renew, duel, and era behavior require official evidence.

## Exploit review

- repeated/stale target or gump response;
- item moved, traded, stacked, deleted, equipped, blessed, or made nontransferable after display;
- duplicate insurance charge or killer award;
- insufficient bank capacity/funds and partial deposits;
- death during secure trade/vendor/house movement;
- stack split identity and stolen-item return;
- insurance or retained-container bypass of the corpse-root stolen-item return check;
- logout/restart between theft and return;
- restart loss of runtime-only stolen-item and instanced-loot allocation state;
- corpse owner deletion and stale rights;
- duplicate looting or packet replay;
- save migration of `Insured`/`PaidInsurance` and legacy paid lists.

## Verification

Build an item-disposition matrix across equipped/backpack/container state, each `LootType`, blessed/insured/paid combinations, young/duel/facet context, and sufficient/insufficient funds. Cover stealing success/failure/caught states, stack splits, criminality, stolen-item death return/expiry/restart, corpse rights/instancing/decay, current and legacy save/load, and exact corpse packets. Use `uo-living-world-review` for economy or player-trust changes.
