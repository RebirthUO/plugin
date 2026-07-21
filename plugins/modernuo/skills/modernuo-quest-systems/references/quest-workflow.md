# Quest Workflow

Read this reference when the request touches more than one quest transition.
Confirm current names and signatures in the consuming checkout before relying
on any pattern.

| Surface | Establish before editing |
|---|---|
| Entry | Offer trigger, eligibility, and accepted state |
| Progress | Objective owner, mutation point, and duplicate-event handling |
| Completion | All required objectives and completion predicate |
| Reward | Recipient, inventory/capacity behavior, and exactly-once guard |
| Exit | Cancellation, restart, deletion, and invalidation behavior |
| Restoration | Persisted fields, migration, and post-load reconstruction |

Use a transition table rather than scattered conditionals. A transition should
state its preconditions, state mutation, visible effect, durable effect, and
rejection behavior. Treat a missing official player-facing rule as unresolved
until evidence or an approved custom policy is available.
