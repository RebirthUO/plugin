---
name: modernuo-monster-abilities
description: >
  Implements monster special attacks as reusable MonsterAbility classes in
  Projects/UOContent/Mobiles/Abilities/, registered via GetMonsterAbilities().
  Use when adding or refactoring boss specials, debuffs, breath attacks,
  counters, summons, or any creature combat ability. Prevents inline ability
  logic in monster files.
---

# ModernUO Monster Abilities

## When This Activates

- Adding or refactoring a creature special attack, debuff, proc, counter, breath, or summon
- Implementing peerless boss combat abilities
- Migrating RunUO inline special logic into ModernUO
- Reviewing monster code for ability architecture

## Default Rule

Every **combat special** is implemented as its own `MonsterAbility` class under `Projects/UOContent/Mobiles/Abilities/` — **not** as inline logic in `OnGaveMeleeAttack`, `OnThink`, `OnDamage`, or as a nested private class inside the monster file.

Monsters only **wire** abilities via `GetMonsterAbilities()`. The ability class owns trigger rules, cooldown, effect payload, and debuff items.

**Good:** `RuneBeetle` → `MonsterAbilities.RuneCorruption`  
**Bad:** `LadyMelisande.TriggerNauseaDebuff()` with nested `NauseaDebuffItem` in the monster file

## Implementation Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Confirm this is a combat special (not boss orchestration)
- [ ] Step 2: Create ability class in Mobiles/Abilities/
- [ ] Step 3: Pick base class and configure trigger/chance/cooldown
- [ ] Step 4: Add MonsterAbilityType enum value if lookup needed
- [ ] Step 5: Register singleton in MonsterAbilities.cs
- [ ] Step 6: Wire monster via GetMonsterAbilities()
- [ ] Step 7: Add ability test under UOContent.Tests
```

### Step 1 — Combat special vs boss orchestration

| Combat special → extract to `MonsterAbility` | Boss orchestration → keep in monster |
|---|---|
| Debuffs, procs, breath, counters, summons-on-hit | Phase spawns at HP thresholds |
| Area effects, life drain, equipment destroy | Peerless altar / encounter lifecycle |
| Mana-cost specials, movement slows | Retinue ownership, altar cleanup |

Combat effects belong in `MonsterAbility` **even on peerless bosses** (see `MonstrousInterredGrizzle` + `HowlOfCacophony`).

### Step 2–3 — Create the ability class

File: `Projects/UOContent/Mobiles/Abilities/{AbilityName}.cs`

Pick a base class (details in [reference.md](reference.md)):

| Base | Use when |
|---|---|
| `MonsterAbility` | Custom trigger logic, passives, damage modifiers |
| `MonsterAbilitySingleTarget` | Single-target proc on melee/spell hit |
| `MonsterAbilitySingleTargetDoT` | Timed debuff / DoT (resist mods, ticking damage) |
| `AreaEffectMonsterAbility` | Hits all valid targets in range |
| `MonsterAbilityGroup` | Weighted random pick from multiple abilities |

Configure overrides:

```csharp
public override MonsterAbilityType AbilityType => MonsterAbilityType.MyAbility;
public override MonsterAbilityTrigger AbilityTrigger => MonsterAbilityTrigger.GiveMeleeDamage;
public override double ChanceToTrigger => 0.10;
public override TimeSpan MinTriggerCooldown => TimeSpan.FromSeconds(30);
public override TimeSpan MaxTriggerCooldown => TimeSpan.FromSeconds(30);
```

Put tunable constants on the ability as `public const` / `public static readonly` — not duplicated on the monster.

For parameterized variants (different creatures, same effect), use constructor parameters like `FanningFire(chance, resistMod, minDmg, maxDmg)`.

### Step 4 — MonsterAbilityType enum

Add a value to `MonsterAbilityType.cs` when `GetAbility(MonsterAbilityType.X)` or tests need typed lookup.

### Step 5 — Register singleton

Add to `MonsterAbilities.cs`:

```csharp
public static MyAbility MyAbility => new();
```

For parameterized abilities, expose factory methods or named instances:

```csharp
public static FanningFire FanningFire => new(0.05, -10, 35, 45);
```

### Step 6 — Wire the monster

Monster file stays thin:

```csharp
private static MonsterAbility[] _abilities = { MonsterAbilities.MyAbility };
public override MonsterAbility[] GetMonsterAbilities() => _abilities;
```

Multiple abilities:

```csharp
private static MonsterAbility[] _abilities =
{
    MonsterAbilities.FireBreath,
    MonsterAbilities.PoisonGasCounter
};
```

Weighted random group:

```csharp
private static MonsterAbility[] _abilities =
{
    new MonsterAbilityGroup(
        new(0.6, MonsterAbilities.EnergyBoltCounter),
        new(0.4, MonsterAbilities.ThrowHatchetCounter)
    )
};
```

Do **not** call ability logic manually from monster hooks when `TriggerAbility` already handles it via `BaseCreature` combat events.

### Step 7 — Tests

Location: `Projects/UOContent.Tests/Tests/Mobiles/Abilities/{AbilityName}Tests.cs`

Minimum coverage:
- Monster registers the expected ability via `GetMonsterAbilities()`
- Effect applies with correct resist/damage/debuff values
- Era-conditional behavior if applicable (`Core.ML`, `Core.AOS`, etc.)

See [reference.md](reference.md) for templates.

## Anti-Patterns

Do **not**:

- Put special-attack logic in `OnGaveMeleeAttack`, `OnTakeMeleeDamage`, `OnThink` when a trigger flag covers it
- Nest `MonsterAbility` subclasses or debuff `Item` classes inside monster files
- Duplicate ability constants on the monster (read from the ability class instead)
- Copy-paste an ability for each creature — parameterize or reuse the singleton
- Store per-creature cooldown on the monster — `MonsterAbility` tracks cooldown per `BaseCreature` internally

## Code Audit Hooks

When editing ability `.cs` files, also apply `modernuo-code-audit` rules:

- Cancel `_timerToken` in debuff item `OnAfterDelete()`
- Use `[SerializationGenerator]` on serializable debuff items; delete stale effects in `[AfterDeserialization]`
- No LINQ on hot paths; use `PooledRefList` / `PooledRefQueue` for target collection
- No `Console.WriteLine` — use `LogFactory.GetLogger`
- PropertyList string literals must be holes (`$"{"Label"}\t{value}"`)

## Related Skills

| Task | Skills |
|---|---|
| New monster + ability | `modernuo-monster-abilities`, `modernuo-content-patterns`, `modernuo-timers` |
| Era-conditional ability | `modernuo-era-expansion` |
| Debuff items with timers | `modernuo-timers`, `modernuo-serialization` |
| Code review | `modernuo-code-audit` |

## Additional Resources

- Base class matrix, trigger reference, code templates, review checklist → [reference.md](reference.md)
- Ability system source → `Projects/UOContent/Mobiles/Abilities/`
- Creature patterns hub → `dev-docs/claude-skills/modernuo-content-patterns.md`
