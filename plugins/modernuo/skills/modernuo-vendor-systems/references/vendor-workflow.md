# Vendor Workflow

Read this reference for a transaction, restock, or inventory change. Confirm
current types and transaction order in the consuming checkout.

| Phase | Required proof |
|---|---|
| Quote | Vendor, player, listing, price, stock, and authorization validity |
| Commit | Currency, inventory, capacity, and stock revalidation |
| Transfer | Recipient, item identity, ownership, and rollback/recovery behavior |
| Restock | Scheduler/trigger, limits, duplicate prevention, and persistence |
| Exit | Cancellation, stale UI, deletion, disconnect, and load restoration |

Treat quote data as stale after any delay. At commitment, re-read authoritative
state instead of trusting the original UI or client selection.
