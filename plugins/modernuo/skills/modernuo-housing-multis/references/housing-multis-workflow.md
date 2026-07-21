# Housing and Multis Workflow

Read this reference when a request spans placement, ownership, components, or
restoration. Confirm current signatures and persistence patterns in the
consuming checkout.

| Surface | Required proof |
|---|---|
| Placement | Location, map, collision, and authorization checks |
| Access | Owner, co-owner, friend, staff, and denial behavior |
| Components | Creator, owner, update path, and deletion path |
| Contents | Secure/lockdown links and stale-reference handling |
| Lifecycle | Move, transfer, demolish/delete, and post-load reconstruction |

Record every relationship that crosses object boundaries. A deletion-safe design
allows either side to disappear first without retaining a dangling reference.
