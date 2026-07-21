# UOContent Test Fixture Pitfalls

Concrete pitfalls hit while writing regression tests under `Projects/UOContent.Tests/`.
The umbrella skill `modernuo-regression-testing` says "register a minimal
`SpeedLevel.Medium` entry once" but does not show the exact code. This file is
a revision-bound discovery recipe. Before using any path, fixture behavior,
recovery step, or code fragment below, record the consuming repository revision
and confirm it in current source. If the anchor is absent or differs, do not
apply the recipe; adapt it from the current fixture or return `BLOCKED` with the
missing evidence.

## NPCSpeeds — `KeyNotFoundException` on every `BaseCreature` ctor

The UOContent test fixture (`Projects/UOContent.Tests/Fixtures/TestServerInitializer.cs`)
does **not** load `Distribution/Data/npc-speeds.json`, so the `BaseCreature`
constructor's call to `NPCSpeeds.GetSpeeds` throws
`KeyNotFoundException: The given key 'Medium' was not present in the dictionary.`
on the first creature construct.

The fix is to register a `Medium` speed entry in a `static` ctor on the test class
(before any `[Fact]` runs):

```csharp
[Collection("Sequential UOContent Tests")]
public class RisingColossusSpellTests
{
    static RisingColossusSpellTests()
    {
        NPCSpeeds.RegisterSpeed(new NPCSpeeds.SpeedClassEntry
        {
            Level = SpeedLevel.Medium,
            ActiveSpeed = 0.25,
            PassiveSpeed = 0.5,
            Types = [typeof(RisingColossus)]
        });
    }
    // ...tests...
}
```

`NPCSpeeds.SpeedClassEntry` is a `public record` in
`Projects/UOContent/Mobiles/NPCSpeeds.cs` with `Level`, `ActiveSpeed`,
`PassiveSpeed`, `Types` (a `HashSet<Type>`). Use `Types = [typeof(T)]` for the
collection-expression shortcut.

**This is for tests only.** Do not add `GetSpeeds` overrides to production
mobiles as a "test convenience" — that widens the production API for no game
reason. The other summons in the repo (`AnimatedWeapon`, `SummonedAirElemental`)
also rely on the JSON being loaded and would break in tests the same way; they
just don't have tests.

## `new Mobile(World.NewMobile)` requires `DefaultMobileInit()` before `Delete()`

`Mobile.Delete()` walks `Items`. Fresh mobiles that were never
`DefaultMobileInit()`'d have a null backing list and throw
`NullReferenceException` at `Mobile.cs:2464` (the
`for (var i = Items.Count - 1; i >= 0; --i)` loop).

Pattern used by `DryadAllureSpellTests` and `PurgeMagicSpellTests`:

```csharp
var m = new Mobile(World.NewMobile);
m.DefaultMobileInit();
m.InitStats(100, 100, 100);
m.Hits = 100;
m.Mana = 100;
return m;
```

If the test mobile needs to live on a map (e.g. for `MoveToWorld`,
`BaseCreature.Summon`, or `GetDistanceToSqrt`), call
`m.MoveToWorld(new Point3D(5830, 0, 0), Map.Felucca);` before any assertions
that touch the world.

`DefaultMobileInit` also leaves `FollowersMax = 0`, which makes every
`Followers + N > FollowersMax` summon check fail. For summon spell tests, set
`m.FollowersMax = N` (where N is the slot count of the summon being cast)
explicitly.

## `Body` is a `readonly struct` — `Assert.Equal(829, bc.Body)` overload-fails

`Server.Body` is a `public readonly struct` (`Projects/Server/Mobiles/Body.cs`)
implementing `IEquatable<int>`. `xUnit.Assert.Equal(int, Body)` overload
resolution sometimes picks the `(DateTime, DateTime)` overload in a confusing
way and the build fails with "Argument 1: int cannot be converted to DateTime".

Always cast the body to `int` first:

```csharp
Assert.Equal(829, (int)colossus.Body);  // good
// NOT: Assert.Equal(829, colossus.Body);
```

## Test-seam pattern: `internal static TryXxxForTests` on the spell

The repo convention for Mysticism/Spellweaving spell tests is to expose an
`internal static` helper on the spell that mirrors the production cast path
minus the location/region validation:

```csharp
internal static bool TrySummonAtForTests(
    RisingColossusSpell spell, Point3D p,
    out RisingColossus creature, out TimeSpan duration)
{
    var caster = spell.Caster;
    duration = TimeSpan.Zero;
    creature = null;

    if (caster.Followers + 5 > caster.FollowersMax)
    {
        caster.SendLocalizedMessage(1049645); // too many followers
        return false;
    }

    var level = (int)((MysticSpell.GetBaseSkill(caster)
                       + spell.GetDamageSkill(caster)) / 2.0);
    var summon = new RisingColossus(caster, level);
    duration = TimeSpan.FromSeconds(Math.Min(MaxColossusDurationSeconds,
                                             level / 2.0));
    return BaseCreature.Summon(summon, true, caster, p, 0x656, duration)
        && (creature = summon) != null;
}
```

Production `Target(IPoint3D)` calls this same seam and just adds the particle
effect on top. Tests get a real `BaseCreature.Summon` invocation (so follower
count, control master, summon-end timer, etc. all behave as in production)
without needing to drive a target cursor through `SpellTarget<T>`.

Precedent: `ReactiveArmorSpell.OnCastForTests` (test extension in
`PurgeMagicSpellTests.cs:407`).

## Worktree recovery boundary

This testing reference does not prescribe stash, branch, recovery, or file
reconstruction commands. If a worktree differs unexpectedly, preserve the
observed state and use the consuming repository's separately authorized
recovery workflow before resuming test work.

## Era-gate test recipe

For every spell registration test, pin both branches:

```csharp
[Fact]
public void RegisterMysticism_PreSa_DoesNotExposeRisingColossus()
{
    var previousExpansion = Core.Expansion;
    try
    {
        ResetSpellRegistry();         // clear SpellRegistry static tables
        Core.Expansion = Expansion.ML;
        Initializer.Configure();
        Assert.Null(SpellRegistry.NewSpell(692, caster, null));
    }
    finally
    {
        Core.Expansion = previousExpansion;
        ResetSpellRegistry();
        Initializer.Configure();      // restore default registrations
    }
}
```

`ResetSpellRegistry` is private to each test class and uses reflection on
`SpellRegistry`'s `m_Types`, `m_IDsFromTypes`, `m_Count` static fields
(plus `SpellRegistry.SpecialMoves.Clear()`). Pattern is in
`PurgeMagicSpellTests.cs:387-404`.
