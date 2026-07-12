# Taming and Control

Use this reference for Animal Taming attempts, control-master assignment, owner history, follower slots, control chance, transfer, and release. Confirm numeric rules from current code and official evidence before changing them.

## Source map

- `Projects/UOContent/Skills/AnimalTaming.cs`
- `Projects/UOContent/Mobiles/BaseCreature.cs`
- `Projects/UOContent/Mobiles/AI/BaseAI/PetOrders.cs`
- `Projects/UOContent/Mobiles/AI/BaseAI/PetOrderHandlers.cs`
- `Projects/UOContent/Items/SecureTrade/TransferItem.cs` or the active pet-transfer item path
- tameable creature subclasses under `Projects/UOContent/Mobiles/**`

## Taming attempt

Current `AnimalTaming` is a delayed, multi-tick target action:

1. Register the skill callback and acquire a mobile target.
2. Reject non-creatures, untameable/already controlled targets, actor/creature restrictions, follower-capacity overflow, owner-history limits, required subdual, insufficient minimum skill, faction restrictions, and concurrent taming.
3. Start a timed attempt and mark the creature as being tamed.
4. On each tick, revalidate range, actor life, visibility/LOS/path, tameability/control state, owner limit, subdual, and damage since the attempt began.
5. On completion, perform the production skill check, apply first-tame stat/skill policy where applicable, append owner history, and assign control master/order.
6. On every terminal path, release the in-progress marker and skill timing state.

The static in-progress set is a concurrency guard. Tests must prove cancellation, death, deletion, exceptions, and competing tamers cannot leave a creature permanently blocked.

Current main checks follower capacity before starting the timed attempt, but capacity can change before completion. The success path can append to `Owners` before calling `SetControlMaster`, and does not use that method's failure result as a rollback gate. Test mid-attempt slot exhaustion and ensure a failed final assignment does not alter owner history, scaling, bonding, spawner ownership, or control state.

## Ownership and slots

`BaseCreature.SetControlMaster` is the aggregate mutation boundary:

- assigning a master enforces follower capacity, detaches ordinary spawner ownership, clears stale waypoint/home state, and establishes controlled state/order;
- changing `ControlMaster` removes slots/follower registration from the prior owner and adds them to the new owner;
- clearing the master resets controlled target/order state;
- player follower sets and numeric `Followers` must stay synchronized.

Do not set `Controlled`, `ControlMaster`, or follower counts independently. Verify failed assignment leaves the old owner, slots, spawner, and control state unchanged.

`Owners` is historical trust/taming state, not the current owner. `ControlMaster` is current control authority. `SummonMaster` and summoned creatures use related but distinct rules.

## Transfer

Pet transfer uses a secure-trade handoff rather than direct assignment. Revalidate:

- old and prospective owners exist, are distinct players, and satisfy young/account policy;
- the pet can be controlled by both sides;
- destination follower capacity still fits;
- pet/participants are not in disallowed combat or another trade;
- both network states and the secure-trade container remain valid;
- acceptance changes ownership exactly once and cancellation restores the prior standing order.

Treat delayed acceptance as untrusted input. Never use capacity or control chance captured when the trade opened.

`Friends` is independent serialized state. Current transfer/release paths do not necessarily clear prior friends, so make friend retention or revocation an explicit policy and test it rather than assuming ownership change removes access.

## Release

Release clears combat/target/friend/bonding state and removes the control master. Runtime behavior then returns to a spawner/home anchor, begins an untamed deletion timer, drops eligible contents, or deletes immediately according to creature policy.

Test released pets with and without a spawner, dead/bonded/summoned cases, pack contents, stale stay anchors, and save/load during the deletion window.

## Evidence boundary

Minimum skill, owner penalties, stat/skill scaling, control formulas, follower slots, loyalty, gender/race restrictions, and expansion gates are official gameplay claims. Keep them behind `uo-official-evidence`; repository values describe current implementation only.

## Verification

Use deterministic timers and RNG. Cover every rejection, each tick-time invalidation, competing attempts, mid-attempt slot exhaustion, first/re-tame rollback, owner history, successful/failed master assignment, transfer accept/cancel/race, friend-state behavior, release, spawner detachment, and save/load.
