# Bushido Honorable Execution: parity/test notes

Session learning from RebirthUO issue wave work around Honorable Execution, Perfection, and Bushido penalties.

## Authoritative behavior anchor

UO.com Bushido reference states that when Honorable Execution does not kill the opponent, the attacker receives:

- `-40` to all resistances
- loss/suppression of Resist Spells if present
- inability to use Bushido spells or special moves for 7 seconds

Use this as the gameplay source when implementing or reviewing SE Honorable Execution lockout behavior.

## Repo anchors to inspect

- `Projects/UOContent/Spells/Bushido/HonorableExecution.cs`
  - Holds Honorable Execution penalty/swing state in a static table.
  - `RemovePenalty(Mobile)` is the single cleanup path for timer state, resistance mods, and Magic Resist skill mod.
- `Projects/UOContent/Spells/Base/SpecialMove.cs`
  - Samurai/Ninjitsu special moves already validate `HonorableExecution.IsUnderPenalty`.
- `Projects/UOContent/Items/Weapons/Abilities/WeaponAbility.cs`
  - Weapon abilities already validate `HonorableExecution.IsUnderPenalty`.
- `Projects/UOContent/Spells/Bushido/SamuraiSpell.cs`
  - Bushido spells should also check the penalty in `CheckCast()` so the UO.com “Bushido spells or special moves” lockout is complete.

## Testing patterns that worked

For focused ModernUO/RebirthUO content tests:

1. Use `[Collection("Sequential UOContent Tests")]` for tests that mutate `Core.Expansion`, `Core._now`, `Timer`, mobile state, static spell tables, or generated events.
2. Save and restore `Core.Expansion` and `Core.Now`/`Core._now` in `finally`/`IDisposable` cleanup.
3. Initialize deterministic timers with `Timer.Init(0)` and advance expiry with:
   ```csharp
   Core._now = start.AddSeconds(seconds);
   Timer.Slice(milliseconds);
   ```
4. For player/mobile spell tests, create `PlayerMobile(World.NewMobile)`, call `DefaultMobileInit()`, set `Player = true`, initialize stats, add a backpack, and move to a real map/location.
5. When a test needs packet sends from ability toggles, attach a disposable `NetState` via `PacketTestUtilities.CreateTestNetState()` and set a SE-era client version such as `5.0.2b`.
6. Before asserting resistance restore values, capture baseline resistances *after* all skill/stat setup. Player resistances can shift after initialization/skill setup, so capturing too early produces false expectations.

## Cleanup/event pattern

If Honorable Execution or similar transient combat effects store state keyed by `Mobile`, add generated-event cleanup for player death/deletion when state should not survive those transitions:

```csharp
using ModernUO.CodeGeneratedEvents;
using Server.Mobiles;

[OnEvent(nameof(PlayerMobile.PlayerDeathEvent))]
[OnEvent(nameof(PlayerMobile.PlayerDeletedEvent))]
public static void OnPlayerEnds(Mobile m) => RemovePenalty(m);
```

This follows existing cleanup patterns in spells like Stone Form, Blood Oath, Animal Form, and other temporary effects.

## RED/GREEN guidance

When implementing a parity fix, first write a focused test that proves the missing behavior:

- For lockout: call `new HonorableExecution().OnHit(attacker, livingDefender, damage)` and assert Bushido spell, special move, and weapon ability usage are blocked until timer expiry.
- For cleanup: assert `RemovePenalty` side effects indirectly through `IsUnderPenalty`, resistance mod names, `GetSkillMod("MagicResistHonorableExecution")`, and restored Magic Resist value.

Avoid only checking the boolean table state; also assert the mods were removed so leaked debuffs cannot pass unnoticed.