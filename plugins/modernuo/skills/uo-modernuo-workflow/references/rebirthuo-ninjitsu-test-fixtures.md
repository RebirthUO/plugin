# RebirthUO Ninjitsu isolated test fixture notes

Session-derived notes from SE/Ninjitsu parity issue work. Use these as concrete examples when writing focused `UOContent.Tests` for Ninjitsu spells and combat hooks.

## Process-global initializers in focused tests

Some tests instantiate only the content class under test and therefore bypass normal server startup/configuration. If the assertion depends on one of these registries, initialize it explicitly in the test or fixture:

- Movement delays: call `Server.Movement.Movement.Configure()` before asserting `WalkMountDelay`, `RunMountDelay`, or `PlayerMobile.ComputeMovementSpeed(...)` behavior.
- Poison definitions: if `Poison.GetPoison("Lesser") == null`, call `PoisonKinds.Configure()` before testing poison application/timer behavior.

Avoid treating zero/default values from uninitialized globals as gameplay truth.

## Animal Form examples

- For speed forms such as Ostard/Llama or Wolf/Bake-Kitsune, assert against `Movement.WalkMountDelay` / `Movement.RunMountDelay` after `Movement.Configure()` rather than comparing two possibly-uninitialized delay values.
- For Unicorn poison resistance, use real Poison instances and the actual poison/timer path. Initialize poison kinds first if needed, apply poison, then drive the poison timer/cure path rather than asserting against null registry results.

## Mirror Image examples

Mirror Image tests are runtime/content tests, not pure formula tests. Prefer `Tests/Spells/Ninjitsu` with `[Collection("Sequential UOContent Tests")]` when instantiating `PlayerMobile`, `Clone`, `BaseWeapon`, timers, or map-sector range queries.

Repo anchors observed:

- `Projects/UOContent/Spells/Ninjitsu/MirrorImage.cs` owns clone creation, clone-count bookkeeping, follower-slot use through `SummonMaster`, and duration (`30.0 + Ninjitsu / 4.0`).
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` owns attack diversion: `MirrorImage.HasClone(defender)` plus `defender.GetMobilesInRange<Clone>(4)`.

Pitfall: clone bookkeeping must prove both positive and cleanup paths. A zero-count entry after the last clone is a real risk because `HasClone(m)` is implemented as dictionary membership. Tests for follower-slot/despawn should also prove `HasClone` is false after the last clone is deleted.
