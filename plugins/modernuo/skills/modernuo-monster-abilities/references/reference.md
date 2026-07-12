# Monster Ability Implementation Reference

Read this reference when selecting an ability base/trigger, adding registry
wiring, or building a stateful effect. Inspect the current source because the
inventory can evolve.

## Base classes

| Base | Choose when | Representative patterns |
|---|---|---|
| `MonsterAbility` | Passive, custom trigger, damage modifier, movement hook | `MagicalBarrier`, `ReflectPhysicalDamage` |
| `MonsterAbilitySingleTarget` | Instant one-target proc | `ColossalBlow`, `DestroyEquipment` |
| `MonsterAbilitySingleTargetDoT` | Timed debuff or damage-over-time | `RuneCorruption`, `FanningFire` |
| `AreaEffectMonsterAbility` | Filtered targets in `AreaRange` | poison gas, life drain |
| `MonsterAbilityGroup` | Weighted selection among abilities | betrayer/overseer groups |

Subclass `MonsterAbility` directly when the specialized bases do not preserve the
required target, cooldown, or effect semantics.

## Trigger flags

| Trigger | Event |
|---|---|
| `GiveMeleeDamage` | creature deals melee/ranged damage |
| `TakeMeleeDamage` | creature receives melee damage |
| `GiveSpellDamage` | creature deals spell damage |
| `TakeSpellDamage` | creature receives spell damage |
| `CombatAction` | AI combat action/rotation |
| `Think` | AI think cycle |
| `Death` | creature death |
| `Movement` | creature movement |
| `GiveDamage` | outgoing melee or spell damage |
| `TakeDamage` | incoming melee or spell damage |

`BaseCreature.TriggerAbility()` dispatches registered flags from combat hooks.
Do not add a second manual dispatch from the monster.

## Ability contract

Typical overrides:

```csharp
public override MonsterAbilityType AbilityType => MonsterAbilityType.MyAbility;
public override MonsterAbilityTrigger AbilityTrigger => MonsterAbilityTrigger.GiveMeleeDamage;
public override double ChanceToTrigger => 0.10;
public override TimeSpan MinTriggerCooldown => TimeSpan.FromSeconds(30);
public override TimeSpan MaxTriggerCooldown => TimeSpan.FromSeconds(30);
```

- `ChanceToTrigger >= 1.0` means every eligible event after cooldown.
- Use `CanTrigger()`/target checks for mana, range, LOS, alive/harmful, pacify, or
  era conditions.
- Follow the selected base's contract for `base.Trigger(...)`; it commonly records
  cooldown. Do not omit it merely because the effect already fired.
- Place shared tuning on the ability. Use constructor parameters for variants
  rather than duplicate classes or monster-local constants.

## Registry and creature wiring

For a new typed ability, update only the surfaces that apply:

1. `Mobiles/Abilities/{AbilityName}.cs` — implementation.
2. `MonsterAbilityType.cs` — enum value when typed lookup/tests require it.
3. `MonsterAbilities.cs` — instance/factory registration.
4. Creature file — `GetMonsterAbilities()` wiring only.
5. Ability test file — registration plus visible effect.

```csharp
private static readonly MonsterAbility[] _abilities =
[
    MonsterAbilities.MyAbility
];

public override MonsterAbility[] GetMonsterAbilities() => _abilities;
```

Before creating a class, inspect the current `MonsterAbilities.cs` and recursive
ability folders for a reusable or parameterizable implementation.

## Stateful debuff/helper items

A helper item that owns an expiring effect should:

- be invisible/non-movable when it is only an implementation detail;
- expose state through the expected AOS/item interfaces;
- update affected mobile deltas on add/remove;
- own and cancel its timer/token;
- use generated serialization where persistent fields exist;
- delete or restore transient effects intentionally after load;
- never serialize `TimerExecutionToken`.

Removing a previous instance before applying a replacement prevents stacking
unless source behavior explicitly stacks. Locate helper items by a direct item
loop rather than allocating LINQ on a combat path.

## Test minimum

- Creature returns the expected ability/type/trigger.
- Eligible and ineligible targets prove range/LOS/alive/harmful/era rules.
- Chance/cooldown are deterministic through the existing test seam/RNG.
- Visible damage/debuff values and expiry are asserted.
- Delete/load cleanup proves no lingering token/helper item.
- `Core.Expansion` and other process-global state are restored.

Use the sequential UOContent collection when constructing real content entities
or mutating process-global state. Load `modernuo-test-workflow` for fixture and
client-data setup.

## Architecture audit

An absent `GetMonsterAbilities()` result is not proof that a special is missing.
Search inline hooks and `GetWeaponAbility()` first. Record legacy inline combat
specials as migration candidates, while keeping boss phase/altar/retinue logic in
encounter code and weapon specials in the `WeaponAbility` system.
