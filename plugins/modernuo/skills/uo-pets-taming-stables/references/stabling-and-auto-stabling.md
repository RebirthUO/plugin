# Stabling and Auto-Stabling

Use this reference for animal-trainer stable/claim flows, stable capacity, fees, internal storage, automatic logout stabling, login claims, and cleanup.

## Source map

- `Projects/UOContent/Mobiles/Vendors/NPC/AnimalTrainer.cs`
- `Projects/UOContent/Mobiles/PlayerMobile.cs`
- `Projects/UOContent/Mobiles/BaseCreature.cs`
- context menu, target, speech, and claim-list gump code nested under `AnimalTrainer`

`uo-vendors-commerce` owns generic vendor stock/transactions. Animal trainers act as an interaction surface here; pet storage and ownership are this skill's domain.

## Manual stable flow

Current trainer flow:

1. Speech/context action validates trainer and player life plus available payment before opening a target.
2. Target response revalidates trainer/player and pet eligibility: nonhuman, controlled by actor, alive, nonsummoned, eligible pack state, not actively fighting, and within stable capacity.
3. Payment is consumed from the configured player sources.
4. Pet target/order is cleared, pet is internalized, control/summon master is removed, stable flags/owner are set, loyalty may be adjusted by era, and the pet is added to the player's stabled set.

Because payment occurs before all state mutations complete, test exceptions/failures after debit. Stable insertion must not leave a charged player with a world pet, an internalized untracked pet, or duplicate stable membership.

## Claim flow

Claim by speech/name/gump:

1. Clean deleted entries from the player's stabled set and clear their stable metadata.
2. Revalidate trainer/player map, range, life, selected pet identity, and membership.
3. Check follower capacity.
4. Assign control master, target/order, world location/map, stable flags, and loyalty.
5. Remove the pet from stabled and auto-stabled sets.

`SetControlMaster` can fail when capacity changed. Do not move/remove stable membership until assignment succeeds. Revalidate a claim-list button by entity membership, not list index alone.

Current claim paths precheck capacity but do not consistently use `SetControlMaster`'s return as the commit gate. Exercise reentrant capacity changes and require stable flags, membership, location, and follower accounting to remain unchanged on assignment failure.

## Stable capacity and fees

Current capacity depends on player skills and current fee/payment rules are embedded in `AnimalTrainer`. These are official gameplay claims: source and gate them by era rather than copying current constants into new guidance. Test boundary values from the active implementation.

## Auto-stabling

`PlayerMobile.AutoStablePets` runs for supported eras during logout/server pet reconciliation. It walks the player's tracked followers, excludes cases defined by current policy, internalizes eligible pets, clears control, marks stable ownership, and adds them to both `Stabled` and `AutoStabled`.

`ClaimAutoStabledPets` runs after login:

- ghosts cannot claim immediately;
- deleted entries are cleaned;
- pets are claimed only while follower capacity permits;
- successful pets regain control/follow state and world placement;
- remaining pets stay stabled with a player message;
- the auto-stabled marker set is then reconciled.

Audit iteration carefully because `SetControlMaster` mutates follower collections. Use snapshots or established collection behavior and prevent double enumeration/mutation bugs.

## Persistence and cleanup

`PlayerMobile` serializes stabled and auto-stabled entity sets and repairs each loaded creature's `IsStabled`/`StabledBy` state. `BaseCreature` suppresses untamed deletion while stabled. Owner deletion deletes stabled entities.

The creature payload does not independently establish the full stable relationship in the inspected path; player collections repair the flags after load. Test missing/partial player state and uncontrolled-pet deletion timing rather than assuming the creature alone can reconstruct stabling.

Verify:

- sets contain only live pets owned by that player;
- `IsStabled`, `StabledBy`, internal map, control master, followers, and both sets agree;
- legacy migrations restore membership once;
- logout/login repeated cycles do not duplicate membership;
- deleted pets are removed from all sets;
- owner deletion and save/load stop or rebuild transient timers safely.

## Verification

Use deterministic clocks and initialized world state. Cover insufficient/exact payment, every pet rejection, stable capacity edges, pack contents/combat race, debit failure, successful stable, claim capacity race, stale gump, deleted pet, dead owner, auto-stable exclusions, cross-map login, repeated logout/login, save/load, and owner deletion.
