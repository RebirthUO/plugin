# Vendor Packet and UI Boundary

Use this reference when changing incoming vendor replies, outgoing buy/sell lists, gumps/prompts/targets, or client refresh behavior.

## Protocol map

Current anchors:

- `Projects/UOContent/Network/Packets/IncomingVendorPackets.cs`
- `Projects/Server/Network/Packets/OutgoingVendorBuyPackets.cs`
- `Projects/Server/Network/Packets/OutgoingVendorSellPackets.cs`
- `Projects/Server/Mobiles/BaseVendor.cs` for response/list state records
- `Projects/Server.Tests/Tests/Network/Packets/Outgoing/VendorBuyPacketTests.cs`
- `Projects/Server.Tests/Tests/Network/Packets/Outgoing/VendorSellPacketTests.cs`

`modernuo-networking` owns generic packet layout and buffer rules. This skill owns the commerce meaning of decoded fields and resulting state mutation.

## Incoming buy reply

The current handler:

1. Reads and resolves the vendor serial.
2. Checks deletion, range, and the expected client flag.
3. Bounds the number of fixed-width line entries.
4. Decodes item/mobile serial plus requested amount into `BuyItemResponse`.
5. Delegates to `IVendor.OnBuyItems`.
6. Sends the end-vendor-buy response according to handler outcome.

The client serial and amount identify a request only. The vendor transaction must re-resolve stock, current amount, price, actor access, follower capacity, and funds.

## Incoming sell reply

The current handler validates vendor existence/range, count and exact remaining payload size, resolves item serials, drops nonpositive amounts, delegates valid lines to `IVendor.OnSellItems`, and ends the sell session on accepted handling.

The transaction owner must still verify root ownership, movability, transferability, container state, sell-list eligibility, amount, price, and payout.

## Outgoing lists

For buy and sell encoders, record:

- packet ID/subcommand, direction, fixed/variable length, field order, and endianness;
- serial identity used to correlate the reply;
- item/mobile display identity, hue, name/cliloc, price, and amount;
- client/era gates and list-size bounds;
- ordering and deduplication behavior.

Use byte-layout tests. A visually correct vendor window does not prove serial, amount, price, or length encoding.

## Delayed UI

Player-vendor purchase gumps, owner controls, pricing prompts, speech, and targets can outlive the state displayed. On every response, revalidate:

- vendor/item still exists and item remains under that vendor;
- listing object is still valid and price/sale state is current;
- actor is still alive, visible, in range, and authorized;
- house ownership/ban/rental state is current;
- destination capacity and funds still permit the transaction.

Never mutate from a captured `VendorItem`, index, price, or owner check alone.

## Failure behavior

Specify whether malformed/truncated/oversized requests close the session, are ignored, or receive an end packet. Keep this consistent with neighboring handlers and tests. Repeated replies, invalid serials, stale windows, and disconnected clients must not debit, deliver, or expose hidden stock.

Current-main protocol risks to exercise explicitly:

- Buy replies cap entry count but do not first require the payload remainder to be divisible by the fixed entry width; malformed trailing bytes can reach the network exception boundary.
- Outgoing sell prices narrow to an unsigned 16-bit field while settlement uses a wider value.
- Outgoing amounts are unsigned while replies decode signed 16-bit amounts.
- Buy descriptions/counts use byte-sized fields; null or oversized custom values require exact allocation/framing tests.
- Incoming requests are not inherently proof that the client opened this vendor session. Domain code must bind actor, vendor, map, range, feature state, and current stock/listing.

## Verification

Run exact packet tests plus handler tests for truncated payloads, non-divisible remainder, count/length mismatch, too many entries, width narrowing, null/oversized descriptions, invalid vendor/item serials, nonpositive/overflow amounts, deleted/out-of-range/cross-map vendor, unauthorized actor, stale price/stock, repeated or no-session request, feature-disable race, and disconnect. Record any remaining real-client visual check separately.
