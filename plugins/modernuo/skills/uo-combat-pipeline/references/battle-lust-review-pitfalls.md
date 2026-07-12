# Battle Lust / Damage-Reactive Weapon Property Review Pitfalls

Session-derived review notes from a RebirthUO Battle Lust pre-PR audit. Use these when reviewing damage-reactive weapon properties, especially properties that build temporary combat stacks from taking damage and then spend those stacks in `BaseWeapon.OnHit`.

## Review Anchors

- `AOS.Damage(...)` computes a candidate `totalDamage`, but `Mobile.Damage(...)` can still cancel or mutate actual applied damage through deletion/blessed checks and `Region.OnDamage` before hits are lowered.
- `Mobile.DoHarmful(...)` / `HarmfulCheck(...)` owns aggression bookkeeping; using `Mobile.Aggressed` for opponent counts can be valid, but tests should exercise real harmful actions when possible rather than manually appending `AggressorInfo` only.
- `BaseWeapon.OnHit(...)` has a percentage-bonus block capped at 300 before `AOS.Scale(...)`; properties that are supposed to participate in the global weapon-damage cap should be reviewed for placement immediately before that cap.

## Pitfalls To Check

1. **Actual applied damage vs candidate damage.** If a property gains stacks from "damage taken", do not award stacks merely because `AOS.Damage` computed `totalDamage >= threshold`. Verify whether the hook observes damage after `Mobile.Damage` has passed `CanBeDamaged`, `Deleted`, and `Region.OnDamage` checks and after any region mutation.
2. **Lazy cleanup can preserve stacks across invalid transitions.** A static `Dictionary<Mobile, Context>` plus `IsValidOwner(current state)` cleanup only in accessors/timers can let points survive death, weapon removal, map invalidation, or item-property removal if the mobile becomes valid again before the cleanup path runs. Review whether cleanup happens on the transition itself or whether context identity/deadline state proves no invalid interval occurred.
3. **Timer cleanup tests must model transition timing.** A test that calls `GetPoints()` or `GetDamageBonus()` immediately after death/disarm proves only accessor-driven cleanup. Add a scenario like: gain stack -> lose weapon/die/invalid map -> regain valid state before decay tick/accessor -> assert old stacks are gone.
4. **Area/indirect damage side effects.** Adding a global `AOS.Damage` hook affects spells, traps, monster abilities, weapon hit-spells, and area effects that route through AOS damage, not only melee swings. Confirm that the property should respond to all of those sources or gate to the intended source family.
5. **Distribution boundary.** Storage + tooltip + gameplay does not imply loot/runic/imbuing rollout. Check random-property generation tables separately and keep rollout intentionally scoped.

## Suggested Focused Tests

- Pre-era control: property stored but no tooltip/effect before the owning era gate.
- Threshold: `< threshold` does not gain; `>= threshold` after actual applied damage does gain.
- Source eligibility: null, self, deleted, dead-but-not-deleted, and living external mobile.
- Transition cleanup: death, delete, weapon removal, Battle Lust value set to zero, invalid map, and revalidating before the decay timer fires.
- Bonus placement: stack bonus participates in the intended PvP/PvM caps and the global `percentageBonus = Math.Min(..., 300)` cap.
- Non-distribution: runic/loot paths do not roll the property unless explicitly in scope.
