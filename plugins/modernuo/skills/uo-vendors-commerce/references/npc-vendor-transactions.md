# NPC Vendor Transactions

Use this reference for NPC stock, buy/sell request validation, payment, delivery, restocking, and failure review. Verify current code before relying on defaults or thresholds.

## Source map

| Surface | Current anchors |
|---|---|
| Protocol-neutral DTOs/contracts | `Projects/Server/Mobiles/BaseVendor.cs`, `Projects/Server/Mobiles/IVendor.cs` |
| Gameplay transaction owner | `Projects/UOContent/Mobiles/Vendors/BaseVendor.cs` |
| Buy stock | `Projects/UOContent/Mobiles/Vendors/GenericBuy.cs`, `SBInfo/**` |
| Sell acceptance | `Projects/UOContent/Mobiles/Vendors/GenericSell.cs`, `SBInfo/**` |
| Concrete vendors | `Projects/UOContent/Mobiles/Vendors/NPC/**` |
| AI and interaction | `Projects/UOContent/Mobiles/AI/VendorAI.cs` |
| Incoming requests | `Projects/UOContent/Network/Packets/IncomingVendorPackets.cs` |
| Outgoing display/results | `Projects/Server/Network/Packets/OutgoingVendorBuyPackets.cs`, `OutgoingVendorSellPackets.cs` |

## Buy flow

Current NPC purchase flow is centered on `BaseVendor.OnBuyItems`:

1. Require an active seller, living buyer, and region/vendor access.
2. Refresh stock state and resolve each client serial against display objects or resale inventory.
3. Clamp quantities, enforce available stock and follower slots for mobile purchases, reject cost overflow, and build a valid subset.
4. Consume backpack gold or withdraw from the bank according to current rules.
5. For each validated line, decrement stock and construct/deliver entities; resale items are split or moved.
6. Deliver to backpack/bank when possible and otherwise place at the buyer's world location.
7. Send full or partial purchase feedback.

Important: current payment occurs before entity construction/delivery. Treat constructor exceptions, unexpected `null`, placement failure, and mid-loop faults as debit/delivery divergence risks. Do not describe the whole request as atomic unless code and tests establish rollback.

## Sell flow

`BaseVendor.OnSellItems` revalidates server-side item ownership and amount. The current path rejects items that are not rooted under the seller, immovable/nonstandard items, and non-empty containers, then checks the active `IShopSellInfo` lists and transaction limit.

Review:

- duplicate client serials and stacked quantities;
- item movement/deletion between display and reply;
- nontransferable, blessed, insured, quest, or otherwise protected items;
- durability/quality/content-sensitive price calculation;
- resale eligibility and destination;
- payout construction/deposit capacity;
- partial acceptance and repeated replies.

Never trust the displayed sell list as authorization at reply time.

## Stock model

`GenericBuyInfo` owns type, constructor arguments, price, amount/max amount, display identity, and optional follower-slot cost. `GetEntity()` constructs a fresh entity through current type-construction infrastructure. Display entities may be cached separately and must never become purchased world entities.

`GenericSellInfo` maps exact item types to base values and applies item-specific adjustments. Adding an item to a buy list does not automatically make it sellable or resellable; inspect both directions.

Restocking mutates current/max quantities using repository policy. Official stock sizes, restock behavior, and prices require official evidence even when current code contains comments citing a source.

## Safety checklist

- Re-resolve vendor, actor, serial, item, stock, quantity, price, range, access, and follower capacity at execution.
- Compute totals in a wider type and reject overflow before debit.
- Define partial-order behavior explicitly; do not charge for rejected lines.
- If debit precedes construction, add tested compensation or prove constructors/delivery cannot fail in scope.
- Keep display-cache entities internal and delete them through their owner.
- Invalidate/refresh stock and UI after mutation using existing APIs.

## Current-main audit targets

- Feature flags are checked when opening vendor UI but not consistently at submit time. Revalidate them in incoming buy/sell callbacks so a stale window cannot bypass a newly disabled feature.
- Bind submissions to the same live vendor/map/session that produced the list. Coordinate range without an explicit same-map or opened-session check is not sufficient authorization.
- Catalog totals use guarded wide arithmetic, but resale accumulation, sell payout, and some held-gold paths use narrower unchecked values. Test overflow through zero/negative totals before treating payment as safe.
- Transaction ordering is non-atomic: NPC buys debit before construction/delivery and NPC sells mutate items before payout. Add compensation or prove every post-mutation operation is infallible in scope.
- Outgoing sell prices narrow to packet width while settlement recomputes an `int`; large configured prices can display and settle differently.
- Generic sell registration uses exact runtime types. Subclass items require explicit registration rather than assuming base-type matching.

## Verification

Run vendor packet tests under `Projects/Server.Tests/Tests/Network/Packets/Outgoing/` and add gameplay transaction tests for success, partial stock, overflow, insufficient funds, follower limits, invalid serials, stale stock, failed construction, full destination containers, resale, duplicate requests, feature-disable races, cross-map vendors, and submits without an opened session.
