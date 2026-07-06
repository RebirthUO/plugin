# Craft Exceptional Bonus Talisman Review Notes

Use this when reviewing or implementing RebirthUO/ModernUO item-property tickets for `Craft Exceptional bonus` or adjacent talisman crafting bonuses.

## Source framing

- UO.com Magic Item Properties lists `Craft Exceptional bonus` with intensity `1 – 30`, imbue weight `No`, found on `Talismans (L)`, cap `N/A`, and description: increases the percentage chance to craft an item of exceptional quality.
- UOGuide Talismans describes talisman crafting bonuses as `1-30%`, standard and exceptional types, usually paired with the same skill. The exceptional bonus applies directly to the exceptional chance displayed in the crafting window, does **not** add skill points, and does **not** allow exceptional crafting when the base exceptional chance is `0%`.
- Local client cliloc check pattern: extract `1072395`, `1072394`, and `1075085` from `Cliloc.enu`. Observed values:
  - `1072395 = ~1_NAME~ Exceptional Bonus: ~2_val~%`
  - `1072394 = ~1_NAME~ Bonus: ~2_val~%`
  - `1075085 = Requirement: Mondain's Legacy`

## RebirthUO anchors observed during review

- `Projects/UOContent/Items/Talismans/BaseTalisman.cs` stores `Skill`, `SuccessBonus`, and `ExceptionalBonus` as talisman-specific serialized fields.
- `BaseTalisman.GetProperties` emits `1072395` for exceptional bonus and `1072394` for standard success bonus, plus the ML requirement row.
- `Projects/UOContent/Engines/Craft/Core/CraftItem.cs` centralizes the formula in `GetExceptionalChance()`:
  - only applies when `from.Talisman is BaseTalisman talisman && talisman.Skill == system.MainSkill`;
  - subtracts `SuccessBonus / 100.0` from the already success-boosted chance before computing exceptional chance;
  - adds `ExceptionalBonus / 100.0` only if the resulting exceptional base chance is positive.
- `CraftGumpItem` uses `GetExceptionalChance()` for the displayed exceptional chance; `CheckSkills()` uses the same formula for the actual craft roll.
- `SmallSmithBOD` and `SmallTailorBOD` also use `GetExceptionalChance()` for exceptional BOD entry eligibility, so review/implementation notes should mention that side effect explicitly.

## Review decision pattern

For this property, prefer a talisman-specific plan over adding an `AosAttribute`/`Sa*Attribute`:

1. Storage and tooltip belong on `BaseTalisman` (`Skill` + `ExceptionalBonus`).
2. Gameplay belongs in the crafting formula (`CraftItem.GetExceptionalChance`).
3. Do not couple it to generic loot/runic/imbuing distribution. UO.com `(L)` is a distribution fact for later review, not automatic rollout permission.
4. Era frame is ML+ because talismans and the tooltip requirement are ML. If GM/test talismans can exist pre-ML, implementation should explicitly test or gate that behavior.
5. The random talisman generator may already roll values, but its formula/drop rates should not be assumed OSI-parity from the property review alone.

## Expected focused test values

- Matching skill, positive base exceptional chance: `50.0% + ExceptionalBonus 25 => 75.0%`.
- Matching skill, zero base exceptional chance: `0.0% + ExceptionalBonus 25 => 0.0%`.
- Skill mismatch: no exceptional bonus.
- `SuccessBonus = 25` and `ExceptionalBonus = 0`: success chance may increase, but exceptional chance must not be double-increased.
- Tooltip captures cliloc `1072395` with skill cliloc argument and percent.
- Display and roll both use `GetExceptionalChance()`.
- Optional: verify Smith/Tailor BOD exceptional eligibility through the same formula or document it as accepted side effect.
