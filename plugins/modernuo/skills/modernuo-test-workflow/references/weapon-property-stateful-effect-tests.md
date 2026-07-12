# Stateful Weapon-Property Regression Tests

Use this pattern when an extended weapon property has a persistent presence bit plus transient hit-effect state (timers, cooldown/immunity, or consumable restrictions).

## Minimum coverage

1. **Storage boundary**: assert the next enum bit, zero-default behavior, GM command-property availability if applicable, duplication, and `BaseWeapon` serialize/deserialize round-trip. Existing saves must deserialize the new bit as absent; no migration is needed when the underlying `BaseAttributes` bit container is already serialized.
2. **Era/UI boundary**: test the property-list cliloc only under the intended `Core.<era>` gate and assert absence before the era.
3. **Combat boundary**: test the real `BaseWeapon.OnHit` path for a standard hit, and separately assert weapon abilities and special moves do not invoke normal-hit-only effects.
4. **Probabilistic branch**: expose an `internal` deterministic chance seam or a narrowly scoped test helper. Do not loop random calls hoping to observe a proc.
5. **Independent branches**: assert each branch both alone and together—for example a mana-gated damage branch must still be tested when the timed branch procs with insufficient mana.
6. **Timer/lifecycle boundary**: drive every tick deterministically, assert expiry/cooldown behavior, and clear state in `finally`. Include target invalidation and attacker invalidation when the active context retains either mobile. Timer contexts must not retain the weapon instance.
7. **Adjacent-system boundary**: test the exact affected consumable/category while active and after expiry; do not overgeneralize the restriction to unrelated consumables.
8. **Distribution boundary**: if the issue adds representation but deliberately does not add loot/runic/imbuing/reforging sources, add a negative assertion on the closest generation entry point.

## Fixture cautions

- Plain `Mobile` stat maxima may clamp `Hits`, `Mana`, and `Stam`; initialize stats and assert relative to actual maxima instead of assumed values.
- Put real consumables at the mobile's world location before testing `CanDrink`; `BasePotion.CanDrink` first rejects out-of-range items.
- Timer-slice combat tests can be affected by natural regeneration. Use a no-regen fixture or assert only the controlled state transition.
- For Time of Legends content tests, save and restore `Core.Expansion` in `finally` and use the sequential UOContent collection.

## Validation

Run the focused property and attribute-storage test classes after a solution build if the fixture needs copied `Distribution/Data` files. Then run the owning broad project before describing it as broad-suite green.
