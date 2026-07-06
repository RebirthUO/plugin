# SA Weapon Attributes Implementation Notes

Session-derived notes for adding Stygian Abyss weapon-hit properties to RebirthUO/ModernUO without bloating `AosWeaponAttribute`.

## Recommended architecture

For SA-specific weapon properties, prefer a separate `SaWeaponAttribute` enum and `SaWeaponAttributes : BaseAttributes` container instead of extending `AosWeaponAttribute` when the work is the beginning of a broader SA property family.

Minimal first slice:

```csharp
[Flags]
public enum SaWeaponAttribute
{
    HitCurse = 0x00000001,
    HitFatigue = 0x00000002,
    HitManaDrain = 0x00000004
}
```

`SaWeaponAttributes.GetValue(Mobile m, SaWeaponAttribute attribute)` should return `0` unless `Core.SA` is active, then aggregate equipped `BaseWeapon.SaWeaponAttributes` similarly to `AosWeaponAttributes.GetValue`.

## BaseWeapon integration checklist

When adding `SaWeaponAttributes` to `BaseWeapon`:

1. Bump `[SerializationGenerator]` version.
2. Add a new `[SerializableField]` after current fields, with `SerializedIgnoreDupe`, `SerializedCommandProperty(canModify: true)`, save flag, and default factory.
3. Initialize the container in the constructor.
4. Initialize the container in legacy/pre-codegen `Deserialize` as an empty default, because old save flags cannot include the new field.
5. Add a migration JSON for the new version and a `MigrateFrom(VNContent content)` method if the project pattern requires copying old generated content into new fields.
6. Add OPL rows in `GetProperties` under `Core.SA` only.
7. Add combat hooks in `OnHit` under `Core.SA` only.
8. Do not add these properties to Runic/Loot/Imbuing generators in the first patch unless the task explicitly asks for distribution changes.

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
