# Bone Breaker Publish 96 Review Notes

Use when reviewing or implementing the `Bone Breaker` magic item property in RebirthUO/ModernUO.

## Source frame

- Official UO.com Magic Item Properties row: `Bone Breaker`, `Intensity N/A`, `Imbue Weight No`, `Found on Weapons (L)`, `Capped N/A`.
- Official Publish 96 notes introduce `Bone Breaker` under `New Weapon Properties` (Publish 96 worldwide release 2017-02-09).
- RebirthUO has expansion gates (`Core.TOL`, `Core.EJ`) but no publish-number gates. For this mechanic, treat Publish 96 as a post-ToL feature and prefer `Core.TOL` as the practical gate unless the user defines a stricter custom ruleset.
- Do not put publish numbers in symbol names. Keep Publish 96 evidence in comments/docs/PR text/test data.

## Expected behavior

- Applies to weapons from loot (`Weapons (L)`), but initial implementation may be GM/test-only. Loot/runic/imbuing/artifact rollout is a separate economy decision.
- No intensity/cap scaling: a presence-style value (`BoneBreaker > 0`) is sufficient.
- Activates only on normal weapon hits. Must not activate when `WeaponAbility.GetCurrentAbility(attacker)` or `SpecialMove.GetCurrentMove(attacker)` is non-null.
- Has two independent effects:
  1. 20% chance to start a 4-second stamina-drain-over-time effect that blocks refreshment potions while active.
  2. If the wielder has at least 30 mana, apply additional physical damage and consume a 30-mana cost influenced by Lower Mana Cost.
- Victims receive 60 seconds of Bone Breaker drain immunity after the active drain ends.

## Implementation anchors in RebirthUO

- Add a post-ToL/extended weapon-property container near `SaWeaponAttribute` / `SaWeaponAttributes` in `Projects/UOContent/Misc/AOS.cs`.
- Extend `BaseWeapon` with a serialized container, constructor default, migration, and migration JSON. Existing `SaWeaponAttributes` field/index pattern is the closest local precedent.
- Add tooltip in `BaseWeapon.GetProperties` gated by `Core.TOL`; ServUO uses cliloc `1157318` for `Bone Breaker`.
- Hook normal-hit-only gameplay in `BaseWeapon.OnHit` around the existing `a` / `move` variables and hit-property dispatch.
- For LMC, mirror local `WeaponAbility.CalculateMana` / `SpecialMove.ScaleMana` convention: cap LMC at 40% for cost scaling. Preserve the official activation threshold of 30 current mana before applying the bonus.
- Apply the bonus as physical damage, not as the weapon's elemental split.
- Block refresh potions through `BaseRefreshPotion.CanDrink` or a helper it checks; do not globally block all potions unless sources explicitly require it.

## ServUO comparison values

ServUO is not canonical, but useful for fill-in values where UO.com is silent:

- `ExtendedWeaponAttribute.BoneBreaker` presence attribute.
- Tooltip cliloc: `1157318`.
- Normal-hit-only gate: `a == null && move == null`.
- Drain context duration: 4 seconds with 1-second ticks.
- Drain tick: about 10% of `Victim.StamMax`, with lower-bound protection.
- Bonus damage comparison value: +50.
- Immunity duration: 60 seconds.
- ServUO blocks new drain context while immune but still allows the mana-funded bonus damage; choose deliberately and test it.

## Test checklist

- Tooltip appears only at `Core.TOL`/`Core.EJ`; not at `Core.HS` or lower.
- `BoneBreaker = 1` is enough to display and function.
- Normal hit can apply mana-funded physical damage and consume scaled mana.
- `Mana < 30` gives no bonus damage and no mana consumption.
- LMC examples for a 30-mana cost: 0% -> 30, 20% -> 24, 40%+ -> 18.
- WeaponAbility and SpecialMove hits apply neither bonus damage nor stamina drain.
- 20% drain proc starts active context; deterministic test can force proc.
- Refresh and Total Refresh potions are blocked during active drain and allowed after drain ends, even while 60s drain immunity remains.
- Drain immunity prevents a second drain context within 60s.
- LootPack, BaseRunicTool, imbuing, and artifact distributions remain unchanged unless the issue explicitly scopes distribution.
