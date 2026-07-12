---
name: uo-vendors-commerce
description: Use when adding, debugging, or auditing ModernUO NPC or player-vendor stock, buy/sell transactions, BaseVendor, GenericBuy/GenericSell, SBInfo, prices, quantities, payment, VendorInventory, vendor gumps, or vendor packet flows. Do not use for BOD turn-ins, quests, crafting registration, faction governance, or housing except at the vendor boundary.
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - ultima-online
      - modernuo
      - vendors
      - commerce
      - economy
    related_skills:
      - modernuo-content-patterns
      - modernuo-networking
      - modernuo-gump-system
      - uo-bulk-orders-bod
      - uo-housing-houses-multis
      - uo-living-world-review
version: 1.0.0
author: RebirthUO
---
# UO Vendors and Commerce

## Boundary

Own NPC and player-vendor commercial semantics: stock construction, display, access, price/quantity, buy/sell validation, payment and delivery, inventory ownership, transaction response, and commerce lifecycle. Route BOD behavior, house/rental ownership, faction governance, quest objectives, and generic packet/gump mechanics to their dedicated owners.

## Core Workflow

1. State vendor family, era/profile, actor, stock or listed item, currency source, price/quantity, access rules, destination, and expected failure behavior.
2. Inspect both server and UOContent vendor bases, stock definitions, incoming handler, outgoing packets, vendor AI/gumps, persistent player-vendor state, and focused packet/transaction tests.
3. Trace one transaction end to end: request -> actor/vendor/range/state validation -> stock/listing revalidation -> funds or offered-item validation -> mutation -> delivery -> stock/balance update -> response packets/UI refresh.
4. Keep validation before irreversible mutation and make failure behavior explicit. Prove partial fulfillment, insufficient funds/capacity, stale listings, constructor failures, and disconnect/reentry cannot duplicate items or currency.
5. For player vendors, trace owner/house/rental rights, listing ownership, proceeds, backpack/inventory transfer, dismissal/expiration, and save/load/delete cleanup separately from NPC stock.
6. Add behavior tests for transaction success and rejection plus packet encoding tests; audit price or supply changes through `uo-living-world-review`.

## Evidence boundary

Establish official prices, stock, fees, limits, and era behavior through `uo-official-evidence`. Repository code proves current implementation only; community vendor lists and emulator defaults cannot establish official economy behavior.

## Output Contract

Return an NPC/player-vendor ownership map, stock/price/access matrix, transaction and rollback trace, packet/UI boundary, persistence and economy/exploit risks, changed source/data/tests, exact automated results, and remaining in-game checks.

## Reference Routing

- Read [npc-vendor-transactions.md](references/npc-vendor-transactions.md) for stock, buy/sell ordering, payment, delivery, and failure containment.
- Read [player-vendor-lifecycle.md](references/player-vendor-lifecycle.md) for ownership, listings, proceeds, house/rental integration, persistence, and cleanup.
- Read [vendor-packet-boundary.md](references/vendor-packet-boundary.md) when request handlers, packet payloads, gumps, or client refresh behavior changes.

## Verification

- Cover permitted and denied access, valid/invalid quantities, stale stock/listings, insufficient funds, full backpacks/banks, partial fulfillment, constructor failure, resale, and repeated requests.
- Run focused vendor buy/sell packet tests and build both server and UOContent projects.
- For player vendors, cover owner/non-owner actions, listing updates, purchase handoff, proceeds, dismissal/house deletion, save/load, and orphan cleanup.
- Self-check that debit and delivery cannot diverge and that a domain-specific vendor change did not alter generic packet infrastructure unnecessarily.
