# SA Weapon Attributes Implementation Notes

Session-derived notes for adding Stygian Abyss weapon-hit properties to RebirthUO/ModernUO without bloating `AosWeaponAttribute`.

## Recommended architecture

AoS should remain the technical umbrella for the item-property system. For post-AoS weapon properties that do not fit safely into the existing `AosWeaponAttribute` bitmask, prefer a neutral AoS overflow container such as `AosExtendedWeaponAttribute` / `AosExtendedWeaponAttributes : BaseAttributes` instead of era-named live containers like `SaWeaponAttributes`.

Minimal first slice:

```csharp
[Flags]
public enum AosExtendedWeaponAttribute
{
    HitCurse = 0x00000001,
    HitFatigue = 0x00000002,
    HitManaDrain = 0x00000004
}
```

`AosExtendedWeaponAttributes.GetValue(Mobile m, AosExtendedWeaponAttribute attribute)` should apply per-property era gates: SA properties return `0` before `Core.SA`, TOL properties return `0` before `Core.TOL`, etc. The container name stays AoS-centric because AoS is the property-system feature; the expansion only controls availability/display/effects.

Keep any old `SaWeaponAttributes`/old `ExtendedWeaponAttributes` types internal and migration-only when refactoring existing save schemas.

## BaseWeapon integration checklist

When adding `AosExtendedWeaponAttributes` to `BaseWeapon`:

1. Bump `[SerializationGenerator]` version.
2. Add or reuse a `[SerializableField]` with `SerializedIgnoreDupe`, `SerializedCommandProperty(canModify: true)`, and a default factory. Reusing an old field number can be valid when merging an era-named container into the neutral AoS overflow container, but preserve old migration JSON.
3. Initialize the container in the constructor.
4. Initialize the container in legacy/pre-codegen `Deserialize` as an empty default, because old save flags cannot include the new field.
5. Add a migration JSON for the new version and a `MigrateFrom(VNContent content)` method that copies legacy `SaWeaponAttributes`/old `ExtendedWeaponAttributes` values into the new `AosExtendedWeaponAttributes` container.
6. Add OPL rows in `GetProperties` under the correct per-property era gate (`Core.SA`, `Core.TOL`, etc.).
7. Add combat hooks under the correct era gate only.
8. Copy the container in `OnAfterDuped`; missing this is an easy bug when adding new `BaseWeapon` attribute containers.
9. Do not add these properties to Runic/Loot/Imbuing generators in the first patch unless the task explicitly asks for distribution changes.

## Effect semantics found during research

Use official UO.com for modern item-property presence/ranges and UOGuide-style detail only for missing mechanics. For these three properties:

- `HitCurse`: proc chance is the property value. Curse-like stat debuff; sources describe a 30-second Hit Curse cooldown. Do not blindly call `CurseSpell.DoCurse` if exact Hit Curse duration/cooldown is required, because normal Magery Curse uses `SpellHelper.GetDuration` and the standard Curse effect table.
- `HitFatigue`: proc chance is the property value. On proc, reduce target stamina by 20% of `damageGiven`.
- `HitManaDrain`: proc chance is the property value. On proc, reduce target mana by 20% of `damageGiven`.

The property value should be treated as proc chance, not as both proc chance and drain magnitude; otherwise high-intensity items double-scale and become too strong in PvP.

## OPL cliloc candidates

Known candidate clilocs to verify against client data/build:

- `1113712` — Hit Curse `~1_val~%`
- `1113700` — Hit Fatigue `~1_val~%`
- `1113699` — Hit Mana Drain `~1_val~%`

If verification is unavailable, prefer a centralized fallback string approach rather than scattering raw strings throughout item code.

## Test strategy

Add focused tests before broad generator changes:

- `Core.SA` aggregator returns equipped weapon SA property values.
- Pre-SA/ML era returns 0 and effects do not fire.
- `HitFatigue` drains exactly `AOS.Scale(damageGiven, 20)` stamina when proc chance succeeds.
- `HitManaDrain` drains exactly `AOS.Scale(damageGiven, 20)` mana when proc chance succeeds.
- `HitCurse` applies a non-stacking/refresh-safe curse-like debuff and observes its cooldown.

Use deterministic RNG helpers (for example `PredictableRandom`) where available, and label focused tests as focused rather than claiming suite-wide coverage.
