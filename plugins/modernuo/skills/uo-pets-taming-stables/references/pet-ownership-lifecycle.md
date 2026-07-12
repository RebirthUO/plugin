# Pet Ownership Lifecycle

Use this reference for controlled-pet orders, authorization, persistent/fallback order state, login/logout, death, deletion, and cleanup.

## State surfaces

`BaseCreature` owns durable pet state including:

- controlled/summoned flags and current master;
- control target, destination, and `OrderType`;
- control slots, taming owner history, loyalty, bonding/dead-pet state;
- friends, home/range, spawner link, stable state, and deletion timing.

`BaseAI` owns order execution. Current standing-command fallback (`PersistentOrder`) is runtime-only and reconstructed on login by `PetLoginHandler`.

## Order flow

Trace:

```text
speech/context/target -> command authorization -> ControlTarget/ControlOrder
-> OnCurrentOrderChanged -> order-specific state reset -> AI Obey/DoOrder*
-> completion, failure, or persistent-order fallback
```

Current order families include idle, come, drop, friend/unfriend, guard, attack, release, stay, stop, follow, transfer, and rename. Some are transient; stay/follow/guard establish standing behavior. Stop resolves according to the previous order rather than remaining active.

For each command, identify:

- who may issue it: master, friend, or nobody;
- actor/pet/target life, visibility, map/range, and beneficial/harmful rules;
- combat, trade, dead-pet, summoned, or content restrictions;
- target and combat-state mutation;
- completion/fallback order and home anchor;
- messages and side effects.

Never authorize from name/speech parsing alone. Revalidate at target/trade response time.

## Ownership invariants

- One current control master owns follower slots and player follower-set membership.
- A pet friend may receive only the command subset allowed by current code; friendship is not ownership.
- `ControlTarget`, combatant/focus, warmode, and standing order must not retain deleted or unauthorized entities.
- Changing ownership must clear or transfer friends, combat state, persistent order, and pending interactions according to policy.
- Summoned, controlled, bonded, dead, released, and stabled are distinct states; avoid broad `Controlled` checks where one state is required.

Audit each command entry path independently. Current speech dispatch, targeted commands, context menus, transfer trade, and release confirmation do not all use the same owner/friend check. Targeted commands and release confirmation revalidate later, while non-target speech commands can follow a different owner flag path. Verify owner-versus-friend parity for Come, Guard, Drop, Follow, Stay, Stop, Attack, Transfer, and Release; repository behavior is not evidence of official friend permissions.

Release is split across order-change handling and `DoOrderRelease`: one side detaches ownership/combat/bonding, while the other anchors the wild creature, drops contents, and starts delayed cleanup or deletion. Test the complete command path so neither half can run alone and leave follower slots, friends, backpack, home, or delete timers inconsistent.

## Login and persistence

Current `PersistentOrder` is not serialized. `PetLoginHandler` derives follow/stay fallback for controlled pets that have no runtime standing command, based on current master proximity. This is an implementation heuristic, not official evidence.

When changing order persistence:

- preserve backward save compatibility;
- prevent duplicate timers/AI activation;
- test near/far and cross-map login;
- distinguish loaded current order from reconstructed fallback;
- ensure stale home anchors cannot pull pets to an old combat/stay location.

## Death and deletion

Pet death may enter dead-bonded state rather than deleting. Trace owner/follower slots, control order, corpse, resurrection, stable eligibility, and logout behavior separately.

`BaseCreature.OnDelete` and `OnAfterDelete` must:

- clear control/summon master accounting and player follower sets;
- remove auto-stable references;
- stop AI, unsummon, release/delete, loyalty, and other timers;
- clear friends, combat references, spawner ownership, and subsystem registrations.

Owner deletion also cleans stabled pets through `PlayerMobile`; verify ordinary controlled pets and internalized pets do not become orphans.

## Existing tests

`Projects/UOContent.Tests/Tests/Mobiles/AI/PetOrderTests.cs` covers standing-order anchors/fallback, stop semantics, target loss, idle/stay movement intent, release anchoring, login derivation, and an era control. `PetTestStub.cs` provides the focused fixture.

Add missing tests for owner/friend authorization parity, friend retention across transfer/release, attack legality, drop contents, transfer accept/cancel, end-to-end release cleanup, death/resurrection, owner deletion, serialization, and follower-slot reconciliation. The fixture may not load tile data; record movement/client behavior that remains manual.
