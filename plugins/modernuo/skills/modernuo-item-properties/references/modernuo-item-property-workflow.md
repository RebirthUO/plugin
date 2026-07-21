# Item Property Workflow

Use this reference after the consuming repository and requested item property
are known.

## 1. Establish the Contract

Record the property name, affected item classes, current repository revision,
display text or cliloc and argument shape, mechanics, era, storage owner,
persistence, and focused validation surface. Mark each fact as repository,
official, test, or user-supplied evidence. If a gameplay-changing value or
lifecycle rule lacks applicable official or user-supplied authority, return
`BLOCKED`; do not infer it from a similar item.

## 2. Classify the Work

| Class | Required implementation shape |
| --- | --- |
| Display fact | Confirm that it is non-mechanical, add or correct property emission, and invalidate when its state changes. |
| Passive aggregate | Store it on the item, use the current equipped aggregation seam, and test equip plus removal. |
| Active or proc | Store it, find the event seam, define eligibility/chance/cooldown/lifecycle, and test trigger plus blocked paths deterministically. |
| Durability or repair | Wire mutation and repair interactions before displaying the state. |
| Transfer or insurance | Reuse the narrowest current ownership or item-flag mechanism; seek explicit approval before changing broad engine state. |
| Generation or crafting | Complete storage, behavior, display, and tests before wiring generation, crafting, imbuing, or artifacts. |
| Era-gated | Gate both the behavior and the display with the verified current expansion mechanism, then test enabled and disabled states. |

## 3. Choose Storage and Mechanics

Inspect the current base class and an equivalent property. Prefer its existing
property, a focused attribute family, or an existing item-specific subsystem.
For new durable fields, follow the active serialization generator and migration
patterns; a displayed field needs property-list invalidation. Add state at a
broader layer only when the current hierarchy proves all affected item types
need it and the user authorized that scope.

## 4. Emit Display After Behavior

Call the current base emission path in its established order. Use a verified
localized identifier and argument shape where one exists. Keep human-readable
arguments and localized references compatible with the current property-list
handler; load `modernuo-property-lists` for its formatting-specific rules.

## 5. Verify Proportionally

At minimum, assert the emitted property and its behavior. Include equip/remove
for passive effects, trigger and no-trigger paths for procs, era presence and
absence when gated, and a save/load or migration assertion when new durable
state is introduced. Report the exact test command and denominator separately
from static source inspection.
