# Monster Ability Reference

## Base Class Matrix

| Base class | File | Choose when | Examples in repo |
|---|---|---|---|
| `MonsterAbility` | `MonsterAbility.cs` | Passives, custom `CanTrigger`, damage modifiers (`AlterMeleeDamage*`), movement hooks | `MagicalBarrier`, `ReflectPhysicalDamage` |
| `MonsterAbilitySingleTarget` | `MonsterAbilitySingleTarget.cs` | Instant single-target proc | `ColossalBlow`, `DestroyEquipment` |
| `MonsterAbilitySingleTargetDoT` | `MonsterAbilitySingleTargetDoT.cs` | Timed debuff with tick/expire | `RuneCorruption`, `FanningFire`, `AngryFire` |
| `AreaEffectMonsterAbility` | `AreaEffectMonsterAbility.cs` | Hits all valid mobiles in `AreaRange` | `PoisonGasAreaAttack`, `DrainLifeAreaAttack` |
| `MonsterAbilityGroup` | `MonsterAbilityGroup.cs` | Weighted random ability per trigger | `Betrayer`, `ExodusOverseer` |

Subclass `MonsterAbility` directly when none of the above fit, or when the ability needs full control over `Trigger()`.

## MonsterAbilityTrigger Reference

| Trigger | Fires when | Typical abilities |
|---|---|---|
| `GiveMeleeDamage` | Creature deals melee (or ranged) damage | `RuneCorruption`, `HowlOfCacophony`, `GraspingClaw` |
| `TakeMeleeDamage` | Creature receives melee damage | `SummonSkeletonsCounter`, `ThrowHatchetCounter` |
| `GiveSpellDamage` | Creature deals spell damage | Spell-based procs |
| `TakeSpellDamage` | Creature receives spell damage | Spell counters |
| `CombatAction` | AI combat tick (breath, special rotation) | `FireBreath`, `FanningFire` |
| `Think` | AI think cycle | Periodic checks |
| `Death` | Creature dies | `DeathExplosion` |
| `Movement` | Creature moves | Movement-triggered effects |
| `GiveDamage` | `GiveMeleeDamage \| GiveSpellDamage` | Combined outgoing damage |
| `TakeDamage` | `TakeMeleeDamage \| TakeSpellDamage` | Combined incoming damage |

`BaseCreature.TriggerAbility()` is called from combat hooks automatically — abilities register via `AbilityTrigger` flags; do not re-implement trigger dispatch in the monster.

## Cooldown and Chance

```csharp
public override double ChanceToTrigger => 0.10;           // 10% per eligible trigger
public override TimeSpan MinTriggerCooldown => TimeSpan.FromSeconds(30);
public override TimeSpan MaxTriggerCooldown => TimeSpan.FromSeconds(30);
```

- `ChanceToTrigger >= 1.0` → always fires when trigger matches and cooldown expired
- Override `CanTrigger()` for extra gates (mana cost, range, bard pacify check)
- Always call `base.Trigger(trigger, source, target)` at end of `Trigger()` override to record cooldown

## Ability Template (single-target proc with debuff item)

```csharp
using System;
using ModernUO.Serialization;

namespace Server.Mobiles;

public partial class MyAbility : MonsterAbility
{
    public const int MaxRange = 3;
    public const int SwingSpeedMalus = -60;
    public static readonly TimeSpan Cooldown = TimeSpan.FromSeconds(30.0);
    public static readonly TimeSpan EffectDuration = TimeSpan.FromSeconds(30.0);

    public override MonsterAbilityType AbilityType => MonsterAbilityType.MyAbility;
    public override MonsterAbilityTrigger AbilityTrigger => MonsterAbilityTrigger.GiveMeleeDamage;
    public override double ChanceToTrigger => 0.10;
    public override TimeSpan MinTriggerCooldown => Cooldown;
    public override TimeSpan MaxTriggerCooldown => Cooldown;

    public override void Trigger(MonsterAbilityTrigger trigger, BaseCreature source, Mobile target)
    {
        if (!CanEffectTarget(source, target))
        {
            return;
        }

        base.Trigger(trigger, source, target);
        ApplyEffect(source, target);
    }

    protected virtual bool CanEffectTarget(BaseCreature source, Mobile target) =>
        target?.Deleted == false &&
        target.Alive &&
        target.Map == source.Map &&
        target.InRange(source, MaxRange) &&
        source.InLOS(target) &&
        source.CanBeHarmful(target);

    protected virtual void ApplyEffect(BaseCreature source, Mobile target)
    {
        RemoveEffect(target);
        source.DoHarmful(target);
        target.AddItem(new MyAbilityDebuffItem());
    }

    internal static bool HasEffect(Mobile target) => FindEffect(target) != null;

    internal static bool RemoveEffect(Mobile target)
    {
        var item = FindEffect(target);
        if (item == null)
        {
            return false;
        }

        item.Delete();
        return true;
    }

    private static MyAbilityDebuffItem FindEffect(Mobile target)
    {
        if (target == null)
        {
            return null;
        }

        var items = target.Items;
        for (var i = 0; i < items.Count; i++)
        {
            if (items[i] is MyAbilityDebuffItem item && !item.Deleted)
            {
                return item;
            }
        }

        return null;
    }

    [SerializationGenerator(0, false)]
    private sealed partial class MyAbilityDebuffItem : Item, IAosItem
    {
        private AosAttributes _attributes;
        private TimerExecutionToken _timerToken;

        public MyAbilityDebuffItem() : base(0x1)
        {
            Visible = false;
            Movable = false;
            Attributes.WeaponSpeed = SwingSpeedMalus;
            Timer.StartTimer(EffectDuration, Delete, out _timerToken);
        }

        public AosAttributes Attributes => _attributes ??= new AosAttributes(this);

        public override void OnAdded(IEntity parent)
        {
            base.OnAdded(parent);
            if (parent is Mobile mobile)
            {
                mobile.Delta(MobileDelta.Properties | MobileDelta.WeaponDamage);
            }
        }

        public override void OnRemoved(IEntity parent)
        {
            if (parent is Mobile mobile)
            {
                mobile.Delta(MobileDelta.Properties | MobileDelta.WeaponDamage);
            }

            base.OnRemoved(parent);
        }

        public override void OnAfterDelete()
        {
            _timerToken.Cancel();
            base.OnAfterDelete();
        }

        [AfterDeserialization(false)]
        private void AfterDeserialize() => Delete();
    }
}
```

Add `MyAbility` to `MonsterAbilityType` enum and `MonsterAbilities.cs` registry.

## Monster Wiring Template

```csharp
// In the creature class — no ability logic here
private static MonsterAbility[] _abilities = { MonsterAbilities.MyAbility };
public override MonsterAbility[] GetMonsterAbilities() => _abilities;
```

Conditional registration (only when a condition holds):

```csharp
public override MonsterAbility[] GetMonsterAbilities() =>
    SomeCondition ? _abilities : MonsterAbilities.Empty;
```

## Test Template

```csharp
#nullable enable
using System;
using Xunit;

namespace Server.Mobiles;

[Collection("Sequential UOContent Tests")]
public class MyAbilityTests
{
    [Fact]
    public void MyCreatureRegistersMyAbility()
    {
        var creature = new MyCreature();

        try
        {
            var ability = Assert.Single(creature.GetMonsterAbilities());
            var myAbility = Assert.IsType<MyAbility>(ability);
            Assert.Equal(MonsterAbilityType.MyAbility, myAbility.AbilityType);
            Assert.Equal(MonsterAbilityTrigger.GiveMeleeDamage, myAbility.AbilityTrigger);
        }
        finally
        {
            creature.Delete();
        }
    }

    [Fact]
    public void MyAbilityAppliesExpectedDebuff()
    {
        var expansion = Core.Expansion;
        var source = CreateSource();
        var defender = CreateDefender();
        var ability = new MyAbility();

        try
        {
            MoveTogether(source, defender);
            ability.Trigger(MonsterAbilityTrigger.GiveMeleeDamage, source, defender);
            Assert.True(MyAbility.HasEffect(defender));
            Assert.True(MyAbility.RemoveEffect(defender));
        }
        finally
        {
            MyAbility.RemoveEffect(defender);
            source.Delete();
            defender.Delete();
            Core.Expansion = expansion;
        }
    }

    private static BaseCreature CreateSource() { /* minimal creature */ throw new NotImplementedException(); }
    private static Mobile CreateDefender() { /* test mobile with known stats */ throw new NotImplementedException(); }
    private static void MoveTogether(BaseCreature source, Mobile defender) { /* same map, in range */ }
}
```

Reference implementations: `RuneCorruptionAbilityTests.cs`, `DeathExplosionAbilityTests.cs`.

## Registry Checklist

When adding a new ability, touch these files:

1. `Mobiles/Abilities/{AbilityName}.cs` — ability class
2. `Mobiles/Abilities/MonsterAbilityType.cs` — enum value (if needed)
3. `Mobiles/Abilities/MonsterAbilities.cs` — singleton registration
4. `Mobiles/Monsters/.../{Creature}.cs` — `GetMonsterAbilities()` wiring only
5. `UOContent.Tests/Tests/Mobiles/Abilities/{AbilityName}Tests.cs` — tests

## Pre-PR Review Checklist

- [ ] Ability lives in `Mobiles/Abilities/`, not inside a monster file
- [ ] Monster only overrides `GetMonsterAbilities()` — no duplicate effect logic
- [ ] Constants (`Range`, `Duration`, malus values) defined on ability class
- [ ] `base.Trigger()` called to track cooldown
- [ ] Debuff items cancel timers in `OnAfterDelete()`
- [ ] Debuff items self-delete in `[AfterDeserialization]` on world load
- [ ] Era gates use `Core.ML` / `Core.AOS` — never assume era silently
- [ ] Spatial queries use `map.GetMobilesInRange` / `source.GetMobilesInRange`, not `World.Mobiles`
- [ ] Ability test covers registration and core effect behavior
- [ ] `dotnet build` succeeds from repo root

## Existing Ability Inventory

Quick lookup of registered singletons in `MonsterAbilities.cs`:

| Registry property | Ability class |
|---|---|
| `FireBreath` / `ChaosBreath` / `ColdBreath` | Breath attacks |
| `GraspingClaw` | Melee slow proc |
| `RuneCorruption` | ML half-resist debuff |
| `FanningFire` | Fire resist debuff + damage (parameterized) |
| `HowlOfCacophony` | ML movement/cast debuff |
| `PoisonGasCounter` / `PoisonGasAreaAttack` | Poison specials |
| `DeathExplosion` | On-death AoE |
| `DrainLifeAttack` / `DrainLifeAreaAttack` | Life drain |
| `SummonSkeletonsCounter` / `SummonLesserUndeadCounter` / `SummonPixiesCounter` | Summon counters |
| `ColossalBlow` | Stun |
| `DestroyEquipment` | Equipment damage |
| `MagicalBarrier` / `ReflectPhysicalDamage` | Defensive passives |
| `AngryFire` / `BloodBathAttack` | SE specials |
| `EnergyBoltCounter` / `FanThrowCounter` / `ThrowHatchetCounter` | Ranged counters |

Reuse an existing ability before creating a duplicate.
