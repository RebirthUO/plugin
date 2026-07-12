# Extended Weapon Attribute Refactor Notes

Session-derived guidance from creating the RebirthUO ModernUO system issue for moving late-era weapon properties out of `AosWeaponAttribute`.

## Trigger

Use this note when `AosWeaponAttribute` is close to bit exhaustion or when late-era weapon properties such as Bane, Battle Lust, Sparks, Swarm, or Bone Breaker need a storage home.

## Recommended shape

- Treat the change as a **system/refactor issue**, not a single item-property issue, when the primary work is moving storage containers or save data.
- Prefer a neutral `ExtendedWeaponAttribute` enum plus `ExtendedWeaponAttributes` property object/container over expansion-named containers.
- Keep era gates per property:
  - Bane remains `Core.HS`.
  - Battle Lust remains `Core.SA`.
  - Later properties such as Sparks can use their own gate (for example `Core.TOL` or a stricter publish/custom gate if added).
- Do not reuse freed `AosWeaponAttribute` bits in the same refactor. Leave reuse as a later reviewed decision after migration safety is proven.

## Repo anchors from the session

- `Projects/UOContent/Misc/AOS.cs`: `AosWeaponAttribute` and `AosWeaponAttributes`; Bane/Battle Lust were high bits after `DurabilityBonus`.
- `Projects/UOContent/Misc/AOS.cs`: `BaseAttributes` uses `uint _names` plus sparse `int[] _values`, so legacy bits can remain serialized even after enum members are removed unless migration clears them.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs`: owns serialized attribute containers, initializes defaults, and deep-copies containers in `OnAfterDuped`.
- `Projects/UOContent/Items/Weapons/BattleLust.cs`: reads the weapon property to validate runtime Battle Lust contexts.
- `Projects/UOContent/Items/Weapons/Throwing/StormCaller.cs`: named weapon content can have commented/TODO property assignments from before the extended container existed; when moving Battle Lust storage, activate the real `ExtendedWeaponAttributes.BattleLust` assignment instead of leaving the item with a dead placeholder.
- `Projects/UOContent/Migrations/Server.Items.BaseWeapon.v10.json`: current schema anchor when adding a new serialized `BaseWeapon` container.
- Existing tests: `BanePropertyTests.cs`, `BattleLustPropertyTests.cs`, and `ExtendedWeaponAttributesTests.cs` are the focused baseline for storage, tooltip gates, combat behavior, cleanup, distribution guards, serialization/defaults, and named-content assignments such as Storm Caller.

## Migration checklist

1. Add the new owned container to `BaseWeapon` with constructor/default initialization.
2. Add generated serialization support and the next migration schema if a new field is serialized.
3. Decide explicitly whether old `AosWeaponAttributes` Bane/Battle Lust values are migrated into the new container or intentionally abandoned. Do not let this be implicit.
4. Clear or otherwise eliminate inaccessible old `_names` bits when preserving old saves, so legacy state does not keep serializing invisibly or become reinterpretable if freed bits are reused later.
5. Update `OnAfterDuped` to deep-copy the extended container exactly once.
6. Update combat, tooltip, and runtime cleanup reads to use the new source of truth.
7. Keep staff command-property surfaces available on the new container.
8. Add tests for old-save migration/defaulting, old-high-bit behavior (migrated or intentionally inert), dupe behavior, no double-application, unchanged tooltip gates, and unchanged combat behavior.
9. Check named content that should carry the moved property, not only generic test weapons. For Battle Lust this includes Storm Caller: replace old TODO/commented assignments with `ExtendedWeaponAttributes.BattleLust = 1` and add a small named-item regression test.
10. Add at least one tooltip integration test at the owning item surface (`BaseWeapon.GetProperties`), not only direct container `GetProperties`, so the container call cannot be dropped or reordered silently.
11. Run focused tests plus `dotnet build`; label focused results honestly.

## Review heuristics for this refactor

- Search for all `AosWeaponAttribute.Bane`, `AosWeaponAttribute.BattleLust`, `WeaponAttributes.Bane`, and `WeaponAttributes.BattleLust` references; product code should use `ExtendedWeaponAttributes` after the refactor, while tests may keep old raw constants only to validate migration/old-bit behavior.
- Treat a current-version serialize/deserialize roundtrip as insufficient migration proof. Look for a real/generated previous-version payload or migration-content test that exercises `MigrateFrom(VXContent)`.
- When old high bits are intentionally not migrated, still report any remaining invisible high-bit persistence as a future save-compatibility/reinterpretation risk unless the implementation clears them.
- Verify Battle Lust cleanup reads the new container in all runtime validity paths (`OnRemoved`, internal-map/map-change cleanup, lazy context validity, and property setter removal).
- Verify Bane combat still applies only after a successful damaging hit and still uses physical `AOS.Damage` mitigation regardless of the weapon's elemental split.

## Open implementation decision

If the user names the old raw constants (`Bane = 0x02000000`, `BattleLust = 0x04000000`), do not assume the new container must preserve those raw bit values. The safer default for future capacity is to map old constants during migration to low bits in the new container, while keeping the old constants only in migration code/tests. If maintainers require exact raw-value preservation, document that trade-off explicitly.
