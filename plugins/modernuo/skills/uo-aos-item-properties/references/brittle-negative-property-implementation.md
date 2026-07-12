# Brittle negative-property implementation notes

Session-derived notes from RebirthUO/ModernUO issue #10 implementation.

## Source / era shape

- Brittle is a binary negative item property, not a combat stat.
- RebirthUO's practical first-slice gate is `Core.HS` because the codebase exposes expansion gates, not publish-level Publish 74/86 gates or SA-account entitlement checks.
- Tooltip cliloc: `1116209` (`Brittle`).
- Powder rejection message precedent: `1149799` (`That cannot be used on brittle items.`).

## Storage and host surface

Use the shared `NegativeAttribute` / `NegativeAttributes` container, following Prized/Massive, rather than adding a positive AoS stat.

Expected first-slice hosts:

- `BaseWeapon`
- `BaseArmor` (includes shields)

Do not store Brittle on jewelry, clothing, spellbooks, talismans, or other hosts unless a later source/shard-policy task expands the found-on surface.

Pattern:

- Add the next low bit to `NegativeAttribute`.
- Add a `[CommandProperty]` wrapper on `NegativeAttributes` that returns/stores only when `Owner is BaseWeapon or BaseArmor`.
- Add `NegativeAttributes.IsBrittle(Item item)` with the `Core.HS` gate.
- Add `NegativeAttributes.GetProperties()` row `list.Add(1116209)` only when `Core.HS && Brittle != 0`.

## Powder and repair boundary

Powder of Fortifying/Temperament must reject active Brittle before any durability mutation or charge consumption:

- Check `NegativeAttributes.IsBrittle(item)` after `IDurability`/`CanFortify` validation and before `UnscaleDurability()`.
- Send localized message `1149799`.
- Return without changing `UsesRemaining`, `HitPoints`, or `MaxHitPoints`.

Do **not** change `CanFortify` globally on `BaseWeapon`/`BaseArmor`; artifact-specific overrides use `CanFortify` for separate rules. Brittle is an item-property/powder-use restriction, not a blanket durability interface change.

Normal repair must remain allowed. Do not add a Brittle branch to `Repair.cs` unless a future source explicitly changes this.

## Distribution boundary

Do not add Brittle to `BaseRunicTool.ApplyAttributesTo`, loot packs, runic reforging, or Publish 86 global negative-property generation in the storage PR. Distribution is economy-wide follow-up scope and should be separately gated/tested.

## Regression tests that proved useful

Use `[Collection("Sequential UOContent Tests")]` for item instances and craft/repair flows.

Cover:

- store/dupe/serialize on weapon, armor, and shield;
- unsupported jewelry does not store;
- tooltip present in HS and absent before HS;
- non-Brittle powder still fortifies;
- Brittle weapon/armor/shield rejects powder with no charge/durability mutation;
- pre-HS stored Brittle is no-op for powder;
- repair flow still restores Brittle weapon/armor/shield durability;
- runic attribute generation does not roll Brittle.

For repair-flow tests, initialize skill-check plumbing and set skill caps before invoking `Repair.Do(...)` target flow:

```csharp
SkillCheck.Configure();
SkillCheck.Initialize();
player.SkillsCap = 7200;
player.Skills[SkillName.Blacksmith].Cap = 120.0;
player.Skills[SkillName.Tailoring].Cap = 120.0;
player.Skills[SkillName.Blacksmith].Base = 120.0;
player.Skills[SkillName.Tailoring].Base = 120.0;
```

Use `PredictableRandom(0)` when you need the repair weaken and repair difficulty rolls to succeed deterministically. A high fixed RNG value can make repair fail or weaken only, which looks like Brittle blocked repair when it did not.
