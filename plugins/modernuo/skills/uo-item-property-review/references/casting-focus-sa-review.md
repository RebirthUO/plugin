# Casting Focus SA Item Property Review

Use this reference when drafting, reviewing, or implementing `Casting Focus` for RebirthUO/ModernUO.

## Source evidence captured

- **Canonical — UO.com Magic Item Properties**: `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
  - Row: `Casting Focus`
  - Intensity: `1-3`
  - Imbue weight: `No`
  - Found on: `(R)(L)Armor`
  - Cap: `12%`
  - Description: `A chance to resist interruptions while casting spells`
- **Canonical — UO.com Publish 60 / Stygian Abyss**: `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`
  - Official SA artifact evidence includes `Summoner's Kilt` with `Casting Focus: 2%`.
- **Canonical — UO.com Stygian Abyss Artifacts**: `https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-stygian-abyss/`
  - Lists SA artifact examples with Casting Focus values, including 2–3% examples such as Crown of Arcane Temperament / Mantle of the Fallen style entries.
- **Canonical — UO.com Loot Generation**: `https://uo.com/wiki/ultima-online-wiki/items/loot-generation/`
  - Groups `Casting Focus` under `Arcane / of Wizardry` spell-casting modifiers.
- **Community/reference — UOGuide Item Properties**: `https://www.uoguide.com/Item_Properties`
  - Places Casting Focus under Stygian Abyss item properties.
  - Lists `2 - 4%`, type `Hit`, and historical artifact surfaces beyond armor.
- **Engine precedent — ServUO**:
  - `Scripts/Spells/Base/Spell.cs`: `CheckCasterDisruption` sums `SAAbsorptionAttribute.CastingFocus`, caps it at `12`, rolls before `Disturb(DisturbType.Hurt, ...)`, and sends localized message `1113690` on success.
  - `Scripts/Misc/AOS.cs`: uses an absorption-family enum/container (`SAAbsorptionAttribute.CastingFocus`).
  - Equipment property-list code uses cliloc candidate `1113696` for `Casting Focus ~1_val~%`.
  - `Scripts/Services/LootGeneration/ItemPropertyInfo.cs` registers Casting Focus with normal range `1-3`.

## Interpretation

There is a source-surface conflict:

- UO.com current Magic Item Properties gives the normal/current property as armor-hosted, `1-3`, cap `12%`.
- UOGuide and ServUO artifact examples show historical/special item surfaces and values up to `4%`.

Default review position:

- Implement the normal player-facing property from UO.com first: armor-hosted, `1-3`, cap `12%`, `Core.SA` gated.
- Treat 4% values and non-armor hosts as named-artifact/special-item parity, not automatic random-loot/runic/imbuing distribution.
- Keep distribution separate from storage + tooltip + gameplay unless the issue explicitly expands scope.

## RebirthUO repo anchors observed in the Casting Focus issue session

- `Projects/UOContent/Spells/Base/Spell.cs:85-96` is the local hurt-interruption hook: `OnCasterHurt` checks player casting, applies `ProtectionSpell.Registry`, then calls `Disturb(DisturbType.Hurt, false, true)`.
- `Projects/UOContent/Misc/AOS.cs` currently has core AoS attribute containers and weapon properties such as `Bane` / `BattleLust`; no local `CastingFocus`, `SAAbsorptionAttribute`, or absorption-family container was found at that time.
- Tooltip hosts inspected:
  - `Projects/UOContent/Items/Armor/BaseArmor.cs:GetProperties`
  - `Projects/UOContent/Items/Clothing/BaseClothing.cs:GetProperties`
  - `Projects/UOContent/Items/Jewels/BaseJewel.cs:GetProperties`
  - `Projects/UOContent/Items/Weapons/BaseWeapon.cs:GetProperties`
  - `Projects/UOContent/Items/Talismans/BaseTalisman.cs:GetProperties`
- Existing focused item-property test patterns:
  - `Projects/UOContent.Tests/Tests/Items/Weapons/BanePropertyTests.cs`
  - `Projects/UOContent.Tests/Tests/Items/Weapons/BattleLustPropertyTests.cs`

## Implementation guidance

- Prefer a neutral absorption-family container such as `AosAbsorptionAttributes` / `AbsorptionAttributes` if implementing a reusable eater/resonance/focus family. Avoid adding Casting Focus to a weapon-only container.
- Gate tooltip and effect with `Core.SA`; do not rely on the broader `Core.AOS` storage gate.
- The first implementation should roll in `Spell.OnCasterHurt` before `Disturb(DisturbType.Hurt, ...)` and must not reduce or prevent damage.
- Cap effective Casting Focus chance at `12%`.
- Preserve Protection behavior; test Protection success, Casting Focus success after Protection would fail, and both-fail disturbance.
- Do not affect movement, equipment, new-cast, death, or other non-hurt disturbance paths.
- Verify cliloc `1113696` against local client data or established cliloc tooling before finalizing tooltip tests.
- Keep Fish Pie, mastery bonuses, Resonance, eater mechanics, named artifacts, random loot, runic reforging, and imbuing out of the first ticket unless explicitly scoped.

## Focused test expectations

- Storage/dupe/serialization for the chosen host item type(s).
- Tooltip visible in SA+ and hidden pre-SA.
- Aggregation sums equipped valid hosts and caps usable chance at 12%.
- Active player spell: controlled 100%/forced success preserves casting; failed/0% roll disturbs normally; pre-SA does not preserve.
- No active spell remains no-op.
- Protection interaction behaves without double-disturbing.
- Damage taken is unchanged.
- Distribution guard confirms no loot/runic/imbuing tables were changed in a storage/gameplay ticket.
