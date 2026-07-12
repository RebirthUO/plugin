# Craft Exceptional Bonus / Talisman Crafting Modifier Review

## Trigger

Use this reference when drafting, reviewing, or implementing the `Craft Exceptional Bonus` item-property/talisman behavior in RebirthUO/ModernUO.

## Source Summary

- **Canonical:** UO.com Magic Item Properties lists `Craft Exceptional bonus` with intensity `1–30`, `Imbue Weight: No`, `Found on: Talismans (L)`, and describes it as increasing the percentage chance to craft an item of exceptional quality.
- **Repo evidence:** RebirthUO stores `BaseTalisman.ExceptionalBonus`, displays cliloc `1072395`, and consumes it from `CraftItem.GetExceptionalChance` when the equipped talisman's skill matches the crafting system's main skill.
- **Engine precedent:** ServUO stores/displays the same value and uses `BaseTalisman.CheckSkill(CraftSystem)` to match talisman craft bonuses to crafting systems.

## RebirthUO Anchors Observed

- `Projects/UOContent/Items/Talismans/BaseTalisman.cs`
  - `_exceptionalBonus` serialized field.
  - Tooltip row `1072395`: `~1_NAME~ Exceptional Bonus: ~2_val~%`.
  - `GetRandomExceptional()` generated non-zero values in the observed `10–30%` range during the review.
- `Projects/UOContent/Engines/Craft/Core/CraftItem.cs`
  - `GetExceptionalChance` applies `ExceptionalBonus / 100.0` when the equipped talisman skill matches `craftSystem.MainSkill`.
- `Projects/UOContent/Misc/Loot.cs`
  - Random talisman generation assigns `ExceptionalBonus`.
- `Projects/UOContent/Items/Talismans/BaseTalisman.Migrations.cs`
  - Old save-flag path preserves `ExceptionalBonus`.

## Review Decisions / Conflicts to Surface

- **Canonical range vs generated range:** UO.com says `1–30%`, while the observed RebirthUO/ServUO-style logarithmic random generation produced non-zero `10–30%`. Do not silently collapse this into one value; document whether the task is about possible property range or random generation distribution.
- **Skill/system matching:** RebirthUO matched by talisman `Skill` against `craftSystem.MainSkill`; ServUO has a craft-system-aware helper. Review Masonry/Glassblowing or other craft-system taxonomy before changing matching behavior.
- **Template mismatch:** Item-property issue templates may not include `Talismans` in the `Found on` dropdown. For issue bodies, explicitly state `Talismans (ML loot/generated talismans)` rather than forcing the property into Armor/Jewelry/Shields/Spellbooks/Weapons.

## Implementation/Test Checklist

- Test `CraftItem.GetExceptionalChance` with no talisman, matching talisman, non-matching talisman, SuccessBonus-only talisman, ExceptionalBonus-only talisman, and `ForceNonExceptional` controls.
- Test `BaseTalisman.ExceptionalBonus` tooltip formatting/cliloc `1072395` and skill label formatting.
- Test serialization/duplication of `ExceptionalBonus`.
- Test or document the selected random-generation/range policy.
- Keep `Craft Bonus` / `SuccessBonus` separate: it affects craft success chance, while `Craft Exceptional Bonus` affects exceptional chance.

## Side Effects

- Economy: increasing exceptional chance changes resource consumption per exceptional output and can raise availability of crafted PvM/PvP equipment.
- Client presentation: this is a talisman property, not a weapon/armor/jewelry AoS roll.
- Era: initial era is Mondain's Legacy (ML); apply ML gating where player-facing talisman behavior requires it.
