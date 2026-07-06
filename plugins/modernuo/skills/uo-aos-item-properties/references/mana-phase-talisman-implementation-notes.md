# Mana Phase / Mana Phasing Orb Implementation Notes

Use this reference when reviewing or implementing RebirthUO item-property tickets for **Mana Phase**.

## Source summary

- UO.com Magic Item Properties lists `Mana Phase` as:
  - Intensity: `N/A`
  - Imbue Weight: `No`
  - Found on: `Talisman (L)`
  - Effect: `Your next 2 mana checks are free, until you do damage or attempt to use mana. (Whichever comes first)`
- UOGuide `Mana Phase` says the property is found on **Mana Phasing Orbs**. Using a charge makes the next two mana checks free and has a **30 second cooldown**.
- ServUO models this as a concrete `ManaPhasingOrb : BaseTalisman`, not as a generic randomly-distributed AoS attribute. It adds tooltip cliloc `1116158` (`Mana Phase`), uses `BuffIcon.ManaPhase`, gives 50 charges, and 30s recharge.

## RebirthUO anchors observed during review

- `Projects/UOContent/Items/Talismans/BaseTalisman.cs`
  - `BaseTalisman : Item, IAosItem`
  - owns `AosAttributes` and `AosSkillBonuses`
  - constructor sets `Layer.Talisman`
  - `OnDoubleClick` already handles charged talisman use
  - `OnAfterUse()` decrements charges and starts recharge
  - `GetProperties()` emits talisman OPL rows
- `Projects/UOContent/Spells/Base/Spell.cs`
  - `ScaleMana(int mana)` is the central spell mana-cost hook for Mind Rot + LMC
  - `CheckSequence()` performs the final mana check and mana debit
- `Projects/UOContent/Spells/Base/SpecialMove.cs`
  - `ScaleMana(Mobile m, int mana)` is the special-move mana-cost hook
- `Projects/UOContent/Misc/AOS.cs`
  - central AoS damage path if Mana Phase should clear on damage taken/given
- `Projects/UOContent/Mobiles/PlayerMobile.cs`
  - `OnDamage(int amount, Mobile from, bool willKill)` is a player-specific damage hook
- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs`
  - `BuffIcon.ManaPhase` already exists

## Recommended implementation slice

Keep Mana Phase separate from loot/runic/imbuing policy. For a first safe PR:

1. Add `ManaPhasingOrb : BaseTalisman` under `Projects/UOContent/Items/Talismans/`.
2. Give it `[SerializationGenerator(0)]`, `[Constructible]`, `LabelNumber => 1116230`, hue `1165`, `MaxChargeTime = 30`, `Charges = MaxCharges = 50`, and the intended fixed attributes (for example ServUO uses `LowerManaCost = 6`; do **not** add `Brittle` unless that property exists locally).
3. Add tooltip cliloc `1116158` (`Mana Phase`) either in the orb override or via a virtual `BaseTalisman` flag if multiple talismans may later carry it.
4. Store active state as runtime-only data, not save data: a static table keyed by `Mobile` with remaining free checks (`2`). Remove state and buff on unequip/delete.
5. Hook `Spell.ScaleMana(int mana)` and `SpecialMove.ScaleMana(Mobile m, int mana)` before Mind Rot/LMC calculations. If active, consume one free check and return `0`.
6. Do **not** include Spirit Speak, crafting, item skills, or arbitrary direct `Mana -=` paths in the first slice unless the ticket explicitly asks for broader custom behavior; ServUO hooks spells/special moves.
7. Do **not** add loot/runic/imbuing/random talisman generation unless a separate ticket explicitly authorizes distribution/economy policy.

## Parity decision needed before implementation

The wording says the effect lasts until the player `does damage or attempts to use mana`, but the ServUO `AOS.Damage` reference clears Mana Phase when the phased mobile is damaged. Before implementing, decide and document one of:

- Text-literal: clear when the phased mobile **causes damage**.
- ServUO-like: clear when the phased mobile **takes damage**.
- Conservative custom: clear on either damage caused or damage taken.

This choice affects PvP/PvM counterplay, so do not hide it as a technical detail.

## Focused test checklist

Add UOContent tests with `[Collection("Sequential UOContent Tests")]`:

- Tooltip includes cliloc `1116158`.
- Double-click while not equipped does not activate.
- Double-click while equipped and off cooldown activates Mana Phase, decrements a charge, and starts 30s recharge.
- Cooldown blocks immediate reactivation.
- First two `ScaleMana` checks return `0`; the third returns the normal/LMC-scaled value.
- `SpecialMove.ScaleMana` consumes Mana Phase the same way.
- Unequip/removal clears active state and buff.
- Damage-clear behavior matches the explicit parity decision.

Label validation honestly as focused unless the broad owning suite actually ran.