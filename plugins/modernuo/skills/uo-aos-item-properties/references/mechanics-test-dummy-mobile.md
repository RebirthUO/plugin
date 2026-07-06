# Mechanics Test Dummy Mobile for Item Properties

Session learning: when designing an in-game probe for new item properties or combat mechanics, prefer a real damageable `BaseCreature` test dummy over an `IsInvulnerable` mobile or the existing training dummy addon.

## Why not `IsInvulnerable`

`IsInvulnerable` is the wrong primitive for item-property hit testing because it prevents the combat path from reaching many property effects:

- `Projects/UOContent/Mobiles/PlayerMobile.cs` overrides `CanBeHarmful` and rejects harmful actions against `BaseCreature` targets with `IsInvulnerable`, showing "cannot be harmed".
- `Projects/UOContent/Mobiles/BaseCreature.cs` also rejects invulnerable creatures in `CanBeHarmful` and returns `false` from `CanBeDamaged()` when `IsDeadPet || IsInvulnerable`.
- `Projects/Server/Mobiles/Mobile.cs` exits `Damage(...)` early when `!CanBeDamaged()`.

For item properties such as weapon hit effects, the target must accept a real harmful action and produce positive `damageGiven`.

## Why a Mobile, not the addon training dummy

The existing `Projects/UOContent/Items/Addons/TrainingDummies.cs` is a skill/animation dummy. It calls `from.CheckSkill(...)` and plays swing/sound effects, but it is not a `Mobile` and does not drive the full `BaseWeapon.OnHit` -> `AOS.Damage` -> post-hit property pipeline.

Use a mobile for testing properties because `Projects/UOContent/Items/Weapons/BaseWeapon.cs` computes `damageGiven = AOS.Damage(...)` and only runs many hit effects when `damageGiven > 0`.

## Recommended shape

Create a staff-only `BaseCreature` under `Projects/UOContent/Mobiles/Special/` (or another content/staff tooling folder):

- `[SerializationGenerator(0)]`, `partial`, `[Constructible]`.
- Passive/non-farming: no loot, no fame/karma value, no corpse reward, no gold or item faucet.
- Do **not** override `IsInvulnerable => true`.
- Allow real damage, then restore Hits after the damage/property pipeline has executed.
- Use `CantWalk = true`, `FightMode.None`, `RangeHome = 0`, or similar passive constraints rather than invulnerability.
- Expose staff-only `[CommandProperty]` options for verbosity and reset behavior.
- Send diagnostic output only to staff/the attacker unless explicitly building a public demonstration tool.

Useful hooks/anchors:

- `BaseCreature.OnDamage(int amount, Mobile from, bool willKill)` observes incoming damage before `Hits` are lowered.
- `BaseCreature.OnGotMeleeAttack(Mobile attacker, int damage)` is called after melee hit processing in `BaseWeapon.OnHit` and is useful for reporting final changed state.
- `Mobile.ShowVisibleDamage` / `Mobile.VisibleDamageType` already controls client visible-damage behavior globally; avoid changing global settings just for the dummy.

## What to report

For item-property work, have the dummy report before/after state for the specific mechanic family:

- `Hits`, `Stam`, `Mana` deltas.
- Stat mods such as `[Magic] Str Curse`, `[Magic] Dex Curse`, `[Magic] Int Curse` for `HitCurse`.
- Resist changes and paralysis/poison/bleed state when relevant.
- Applied era-gated effects: e.g. SA `HitCurse`/`HitFatigue`/`HitManaDrain`, TOL `Sparks`.

## Buff icon caveat

Client BuffIcons in this codebase are primarily a `PlayerMobile` facility:

- `Projects/UOContent/Mobiles/PlayerMobile.cs` owns `AddBuff`, `RemoveBuff`, `ResendBuffs`, and the buff table.
- `Projects/UOContent/Engines/BuffIcons/BuffInfo.cs` configures the feature and starts/removes buff timers.
- `Projects/UOContent/Engines/BuffIcons/BuffIconPackets.cs` sends add/remove buff packets.

Do not assume a monster can display a player-style BuffIcon bar. If the request is UI/BuffIcon validation, prefer a separate staff command or staff item that adds/removes `BuffInfo` on the admin/player probe. If the request is combat-mechanics validation, the mobile should report mechanical state changes instead of trying to show BuffIcons.

## Tests to add

Focused tests should assert:

- The dummy remains `CanBeDamaged()` and harmful-targetable; it is not `IsInvulnerable`.
- Applying damage leaves it alive/usable after the reset policy.
- No loot/corpse/economy reward is created.
- Era-gated effects still respect `Core.SA`, `Core.TOL`, etc.
- Representative properties can be observed using existing test patterns from:
  - `Projects/UOContent.Tests/Tests/Items/Weapons/SaWeaponAttributesTests.cs`
  - `Projects/UOContent.Tests/Tests/Items/Weapons/ExtendedWeaponAttributesTests.cs`
