# Player Vendor Lifecycle

Use this reference for player-vendor ownership, listings, proceeds, upkeep, house/rental integration, persistence, dismissal, and cleanup.

## Source map

- `Projects/UOContent/Mobiles/Vendors/PlayerVendor.cs`
- `Projects/UOContent/Mobiles/Vendors/RentedVendor.cs`
- `Projects/UOContent/Mobiles/Vendors/PlayerVendorPlaceholder.cs`
- `Projects/UOContent/Mobiles/Vendors/VendorItem.cs`
- `Projects/UOContent/Mobiles/Vendors/VendorInventory.cs`
- `Projects/UOContent/Multis/Houses/BaseHouse.cs` and vendor/rental consumers

Generic NPC `SBInfo` stock is not the player-vendor model.

## Aggregate state

`PlayerVendor` ties together:

- owner and enclosing `BaseHouse`;
- shop name and placement/placeholder state;
- held proceeds and, for legacy behavior, operating funds;
- a dictionary from physical items to serialized `VendorItem` listing metadata;
- pay/upkeep scheduling;
- backpack/container ownership and customer access.

`VendorItem` stores the listed item, price, description, creation time, validity, and sale/free state. Item movement must keep the listing dictionary synchronized recursively for container contents.

## Interaction boundaries

Owner checks and customer checks differ:

- Owner actions include stocking, repricing/describing, collecting proceeds, moving/returning, and dismissal.
- Customer actions require visibility/range/alive checks, house-ban checks, a valid listing, a non-owner buyer, and revalidation when the purchase gump responds.
- House ownership may define vendor ownership under the active vendor system; do not assume the serialized original owner is always authoritative.

Gumps, prompts, speech, targets, and item-lift/drop callbacks are delayed input. Revalidate vendor existence, owner/house rights, item parent/listing identity, current price, buyer funds/capacity, and range at response time.

## Lifecycle

1. Creation binds the vendor to an owner/house, initializes financial state, listing storage, appearance, and pay scheduling.
2. Owner drops an item into vendor storage; callbacks create listing metadata and prompt for sale state/price/description.
3. Customer selects an item; the purchase flow revalidates the listing, moves item ownership, removes payment, credits proceeds, and invalidates listing state.
4. Owner may collect held proceeds up to destination capacity.
5. Pay scheduling debits available vendor funds; insufficient funds can destroy the vendor.
6. Dismissal, house lifecycle, rental termination, or deletion returns/transfers items and proceeds through the configured destination path.
7. Save/load restores listings, owner/house references, funds, and the next pay boundary; delayed reconciliation handles missing houses.

Current main moves a player-vendor item to the buyer before removing backpack/bank gold, and the bank-withdraw result is not used as a commit gate in that sequence. Treat this as a non-atomic transaction risk: test a bank-state race or failed withdrawal after item movement, and preserve enough state to compensate without duplicating the listing or proceeds.

## Destruction and recovery

`PlayerVendor.Destroy` chooses among owner backpack/world delivery, house moving crate, or a `VendorInventory` recovery record. `VendorInventory` internalizes items, tracks gold and owner/house metadata, expires on a timer, and later moves assets to the house moving crate before deleting itself.

Audit every destruction route for:

- full or missing backpacks/banks/moving crates;
- owner no longer owning the house;
- deleted house, owner, item, vendor, or placeholder;
- nested listed containers;
- duplicate item presence in both vendor and recovery inventory;
- held-gold overflow or partial deposit;
- timer reconstruction after load and symmetric timer stop on deletion.

## Persistence and migration

The player-vendor model contains legacy/new-system branches. Treat migration flags and old financial fields as save compatibility, not dead code. Test loading representative old state, missing-house reconciliation, listing validity, pay timer restart, and one-time asset movement.

## Verification

Cover owner/non-owner/banned customer, stale gump, feature disable after display, reprice during purchase, free/not-for-sale/listed items, nested containers, payment failure after item movement, proceeds collection, pay success/failure, dismissal, owner/house change, rental termination, save/load, recovery expiration, and deletion cleanup. Use deterministic time rather than waiting for pay or grace timers.
