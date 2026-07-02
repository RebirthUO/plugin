# Bushido Honor Perfection notes

Use this when working on Samurai Empire Honor/Perfection behavior in RebirthUO/ModernUO.

## Source excerpt to preserve

Authoritative source used in session: `https://uo.com/wiki/ultima-online-wiki/skills/bushido/`.

Relevant wording, condensed:

- A Samurai with 50+ Bushido fighting an Honored foe gains Perfection on landed hits.
- Perfection has about 10 levels; at 100 Bushido each level grants a 10% normal-attack damage increase, up to 100% at full Perfection.
- At 100 Bushido, Perfection grants 100 Luck per level achieved.
- At 50 Bushido, each step gives 5% damage and 50 Luck.
- Training ranks gain 1% damage and 10 Luck per 10 full Bushido skill points per level of Perfection, up to 100 Bushido.
- A miss loses 3 levels of Perfection.
- On defeating the opponent, the attacker gains back some health, stamina, and mana based on final Perfection level.

## RebirthUO implementation anchors

- `Projects/UOContent/Engines/Virtues/HonorContext.cs`
  - `PerfectionDamageBonus` accumulates by `bushido / 10` per landed hit, caps at 100.
  - Correct luck scaling is linear from the accumulated damage bonus: `PerfectionLuckBonus = PerfectionDamageBonus * 10`.
  - Kill restore currently uses `Math.Min(PerfectionDamageBonus * (targetFame + 5000) / 25000, 10)` and applies the same restore amount to Hits/Stam/Mana.

## Test patterns

Use focused tests under `Projects/UOContent.Tests/Tests/Engines/Virtues/` with `[Collection("Sequential UOContent Tests")]`.

Player fixture pattern that avoids zero-stat false failures:

```csharp
private static PlayerMobile CreatePlayer()
{
    var player = new PlayerMobile(World.NewMobile);
    player.DefaultMobileInit();
    player.Player = true;
    player.InitStats(100, 100, 100);
    player.MoveToWorld(new Point3D(1000, 1000, 0), Map.Felucca);
    return player;
}
```

Create `HonorContext` directly, drive `OnTargetHit(source)` for Perfection levels, then assert `PerfectionDamageBonus`, `PerfectionLuckBonus`, or call `OnTargetKilled()` for restore behavior. Always cancel/delete in `finally` if the context is still attached.

## Durable pitfall

If a focused `HonorContext` test shows restored Hits/Stam/Mana as `0`, do not assume the formula is wrong. Test-created `PlayerMobile`s often need `InitStats(...)` before setting Hits/Stam/Mana; otherwise stat caps can clamp values unexpectedly.
