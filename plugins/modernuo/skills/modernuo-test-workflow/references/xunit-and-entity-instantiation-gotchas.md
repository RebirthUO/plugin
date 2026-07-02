# xUnit + UOContent Entity Test Gotchas

Hard-won patterns from isolated-issue PR work (e.g. #111 `[SE-MISS-MON-001]` field-table tests). Load when writing or debugging a `[Theory]` / `[MemberData]` test that constructs real `BaseCreature`/`BaseArmor`/`Item` instances.

## 1. `[MemberData]` source shape — `Type[]` is rejected

xUnit requires `IEnumerable<object[]>`, not a raw `Type[]`. Using `public static Type[] SeMonsterTypes` produces analyzer error `xUnit1019`.

```csharp
// WRONG
public static Type[] SeMonsterTypes { get; } = { typeof(BakeKitsune), ... };
[Theory, MemberData(nameof(SeMonsterTypes))]
public void Test(Type t) { ... }

// RIGHT
public static IEnumerable<object[]> SeMonsterTypes => new[]
{
    typeof(BakeKitsune), typeof(DeathwatchBeetle), ...
}.Select(t => new object[] { t });
```

## 2. Record primary-constructor params generate same-name accessors

C# records do NOT auto-PascalCase their parameter names. A record `(int allowedBodies, ...)` exposes `.allowedBodies` (lowercase), so any named-argument call site that uses `allowedBodies: ...` will fail with CS1739 ("no parameter named 'X'") if you also reference `row.AllowedBodies` from a test method.

**Decision:** keep ALL record params PascalCase from the start. Do not mix styles within one record. If you only access via positional args, lowercase is fine — but lowercase breaks record equality expectations and `with`-expression ergonomics.

## 3. `DeathwatchBeetle` (lowercase `w`) — class-name vs filename

The file `Projects/UOContent/Mobiles/Monsters/SE/DeathWatchBeetle.cs` declares `public partial class DeathwatchBeetle`. The legacy client alias `[TypeAlias("Server.Mobiles.DeathWatchBeetle")]` keeps the serialized name, but the C# identifier is `DeathwatchBeetle`. Same pattern for `DeathwatchBeetleHatchling`.

**Pitfall:** typo'ing `typeof(DeathWatchBeetle)` in a test compiles ONLY if you add a `using` alias — otherwise CS0246. Always grep `public partial class` in the source file before writing the `typeof(...)` reference; do not trust the file name.

## 4. `PredictableRandom` is clamped, not seeded, RNG

`Projects/Server.Tests/Helpers/PredictableRandom.cs` replaces `BuiltInRng.Generator` with a `FixedRandom` whose every `Next*` returns `Math.Clamp(value + minValue, minValue, maxValue - 1)`. Consequences:

- All `Utility.Random(N)` calls in a single ctor return the **same** clamped value, not sequence-shifted.
- `Utility.RandomDouble()` returns `seed/20.0` clamped to `[0.0, 1.0]`.
- `SetSkill(min, max)` and `SetResistance(min, max)` go through `Utility.RandomMinMax`, so a per-type seed usually lands on the lower bound.
- BUT `BaseCreature.UpdateResistances()` and follow-up setters in `OnXxx` virtuals can call RNG again. If those calls depend on ctor-side RNG state (e.g. `RandomBool` → branch chosen → follow-up `SetResistance` from a different code path), the **same fixed seed can produce an out-of-range actual value** for one specific class.

**Real failure seen:** `Ronin` EnergyResistance came back as `88` (not in expected `55-75`) while all other 18 SE monsters passed with the same PredictableRandom pattern. Root cause: `UpdateResistances` or later code path shifted the clamp interpretation.

**Fixes (pick one, do not stack):**
1. Drop the failing monster from the `[Theory]` and assert it as a dedicated `[Fact]` with `Assert.Equal(explicitly-observed-value, ...)`, plus a comment citing the source-locked RNG path.
2. Give the failing class its own seed via `SeedFor(Type)` that you tune by hand and document inline.
3. Replace `InRange` with `Assert.Equal(expected, ...)` for the affected field and freeze it as the canonical value, with a `// SourceLocked until proven otherwise` marker.

## 5. `Activator.CreateInstance` vs `RuntimeHelpers.GetUninitializedObject`

`GetUninitializedObject` skips the constructor entirely → `m_Body` stays at default (0 for `Body` struct, 0 for `int`-backed fields), random paths do not run. Use it ONLY for tests that only check static metadata (e.g. `GetMonsterAbilities()`).

For any test that touches ctor-set fields (Str/Dex/Int, Hits, Body, Tamable, Resistances), use `Activator.CreateInstance(type)` inside a `using var random = new PredictableRandom(seed)` block plus `NPCSpeeds.Configure()`. Always `monster.Delete()` in a `finally`.

## 6. `FireBeetle` is `BaseMount` — body set via base ctor

`FireBeetle : BaseMount` calls `base(0xA9, 0x3E95, AIType.AI_Melee)` which sets `Body = 0xA9` in the base. Tests that skip `Activator.CreateInstance` will see `Body == 0` and fail. Tests that use `Activator.CreateInstance` see `Body == 0xA9`.

## 7. `CorpseName` default is `null`

`BaseCreature.CorpseName` returns `null` unless overridden. Tests must handle `null` for monsters like `EliteNinja` (which does NOT override `CorpseName`).

## 8. `[Theory]` enumeration order is deterministic but `MemberData` source order matters

When using a manual `IEnumerable<object[]>`, the iteration order is what xUnit sees. If a later `[Fact]` asserts that `SourceLockedMonsters.Length == SeMonsterTypes.Count()` (the parameter count), the order must match — easier to assert by mapping to a parallel array of `Type` and comparing element-wise.

## Quick verification recipe

```bash
cd "$worktree"
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1 2>&1 | tail -5   # expect: 0 errors
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~<NewTestClass>" --no-build --no-restore \
  --nologo --verbosity normal 2>&1 | grep -E "(Bestanden|Failed|PASS|FAIL)"
```