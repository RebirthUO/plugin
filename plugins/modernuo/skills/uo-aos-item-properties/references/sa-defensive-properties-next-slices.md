# SA Defensive Item Properties: Next Implementation Slices

Session-derived planning notes for Stygian Abyss defensive item-property slices. Use this when deciding implementation order or drafting the next PR, but re-check the canonical branch before relying on a planned property container.

## Source and repo anchors checked

- Official source: UO.com Magic Item Properties table, `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`.
- **Current RebirthUO/ModernUO `origin/main` (reviewed 2026-07-11) does not contain** `SaWeaponAttribute`, `SaWeaponAttributes`, `ApplySaWeaponHitEffects`, or `SaWeaponAttributesTests` for `HitCurse`, `HitFatigue`, or `HitManaDrain`. Do not use this historical first-slice shape as a current-container precedent.
- `Projects/UOContent/Misc/AOS.cs` instead contains the neutral `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes` overflow container; inspect its current free bit and the property’s own host/era before adding a new value.
- Parry/block anchor for `Reactive Paralyze` on current `origin/main`:
  - `Projects/UOContent/Items/Weapons/BaseWeapon.cs:1609-1713` (`CheckParry`) and `:1715-1779` (`AbsorbDamageAOS`).
  - `Projects/UOContent/Items/Shields/BaseShield.cs` handles shield durability on block/hit.
- Damage pipeline anchor for `Soul Charge` and eater-style properties:
  - `Projects/UOContent/Misc/AOS.cs:115-240`, after elemental resist calculation and before/around final `m.Damage(totalDamage, from)`.
- Caster-interrupt anchor for `Casting Focus` / `Resonance`:
  - `Projects/UOContent/Spells/Base/Spell.cs:85-96` (`OnCasterHurt`).

## Recommended order after the first SA hit slice

### 1. Reactive Paralyze

Best next isolated PR. UO.com lists it on shields and 2-handed weapons with the behavior: chance to paralyze an attacker when the player parries their blow.

Why it is first:

- It has a narrow, existing hook: successful parry/block in `BaseWeapon.AbsorbDamageAOS`.
- It is defensive and conditional, so it has less economy impact than loot-generation properties.
- It tests well: SA gate, no proc before SA, no proc without parry, proc only on successful block, paralysis effect/duration/cooldown if confirmed.

Implementation guidance:

- Prefer a separate SA defensive/parry container if this begins a family (`ReactiveParalyze`, `SoulCharge`, `CastingFocus`, `Resonance`) rather than overloading `AosArmorAttribute`.
- Gate both tooltip and effect by `Core.SA`.
- Do not add to loot/runic/imbuing generation in the first patch.
- Verify exact chance, duration, cooldown/immunity, and whether 2H weapon hosting belongs on `BaseWeapon` or a shared SA container before coding.

### 2. Soul Charge

Good second defensive PR. UO.com lists it on shields with a chance to convert a percentage of damage dealt to the player into mana.

Review evidence captured from RebirthUO #29:

- UO.com Magic Item Properties row: `Soul Charge`, intensity `5 – 30`, imbue weight `No`, found on `Shields (R)(L)`, cap `50`, description `A chance to convert a percentage of damage dealt to the player into mana.`
- Local client cliloc (EA Classic and UOAlive 7.0.114.2) confirms tooltip/message strings:
  - `1113630` = `Soul Charge ~1_val~%`
  - `1113636` = `The soul charge effect converts some of the damage you received into mana.`
- ServUO comparative implementation (`Scripts/Abilities/SAPropEffects.cs`) treats the property value as a percent chance (`shield.ArmorAttributes.SoulCharge > Utility.Random(100)`) and converts post-resist damage to mana at 30%; it uses 50% when Fish Pie Soul Charge is active.
- RebirthUO at review time only had `BuffIcon.FishPie`, not Fish Pie effect logic, so Fish Pie should remain a separate scope unless the issue explicitly includes it.

Why after Reactive Paralyze:

- It needs post-resist damage, so it belongs in `AOS.Damage` rather than item-local `OnHit`.
- It affects sustain and therefore PvP/PvM resource economy more than a parry-only effect.
- It needs cap and chance semantics confirmed before distribution.

Implementation guidance:

- Gate tooltip and effect with `Core.SA`; UO.com is current-live and does not identify an exact introduction publish, but `Core.SA` matches the SA-property slice policy and ServUO's SA property-effect placement.
- Use shield-only scope: property can live in `AosArmorAttribute`/`AosArmorAttributes`, but tooltip/effect should require `this is BaseShield` or an equipped `BaseShield` on `Layer.TwoHanded`.
- Hook after `totalDamage` is computed and before/near applying damage, where actual damage to the defender is known.
- Avoid using pre-resist `damage` for conversion; that over-rewards high-resist builds.
- Formula expectation for the first implementation: proc chance = `SoulCharge` property value; on proc add `floor(totalDamage * 30 / 100)` mana, capped at missing mana (`ManaMax - Mana`). Keep the ServUO/Fish Pie 50% path out unless Fish Pie effect support is in scope.
- Test values: `SoulCharge = 100`, `totalDamage = 100`, `Mana = 0`, `ManaMax >= 100` should give `+30 Mana`; `Mana = 90`, `ManaMax = 100`, `totalDamage = 100` should end at `100`; `Core.ML` and non-shield hosts should have no tooltip/effect.
- Add tests for SA gate, shield-only scope, damage-to-mana formula, mana cap, zero/failed chance, dead/deleted mobiles, and PvP/PvM if the formula differs.

### 3. Casting Focus

Useful caster defensive property, but PvP-sensitive. It should resist interruption in `Spell.OnCasterHurt`, not prevent damage.

Why not earlier:

- Interrupts are core mage counterplay, so small chance/cap errors have large PvP impact.
- It may overlap with `ProtectionSpell.Registry` and other interruption protections.

Implementation guidance:

- Model it as an interruption-resist check before `Disturb(DisturbType.Hurt, ...)`.
- Confirm cap semantics and whether all damage sources qualify.
- Tests should cover caster with/without active spell, Protection interaction, SA gate, and no effect on non-player caster paths if source behavior says so.

### 4. Damage Eater / Kinetic Eater / Resonance family

Important for later modern-loot parity but too broad for the next small PR.

Why later:

- They require damage-type matching, caps, charge storage/conversion timing, and potentially multiple item families.
- They may need a dedicated SA absorption container and timer/charge model.
- They strongly affect sustain and loot value.

## Do not do in the same PR

- Do not enable loot/runic/imbuing distribution before storage + tooltip + gameplay tests pass.
- Do not mass-add UO.com property names as inert enum bits; each property needs a gameplay owner or explicit GM/test-only status.
- Do not add broad modern loot negative properties (`Antique`, `Brittle`, `Prized`, `Unwieldy`, `Massive`) until insurance, durability, and loot-generation policy are scoped.

## Reporting guidance

When asked “what item properties next?”, answer with era/ruleset first. For SA parity after the first hit slice, lead with `Reactive Paralyze`, then `Soul Charge`, then `Casting Focus`, and explicitly label loot/runic/imbuing distribution as a later economy decision.