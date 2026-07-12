# Prized Publish 86 Review

## When this applies

Use this note when drafting or implementing a RebirthUO/ModernUO issue for the `Prized` item property or for the broader Publish 86 negative-item-property system.

## Source evidence

- **Canonical — UO.com Magic Item Properties** (`https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`): row states `Prized`, intensity `N/A`, imbuing weight `No`, found on `Armor(L), Jewelry(L), Weapons(L) Shields(L)`, total cap `No`, and description `Item insurance cost is increased, cannot be blessed`.
- **Canonical — UO.com Publish 86 notes** (`https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-86/`): introduces negative item properties in Global Loot Changes. The notes list `Prized – Item insurance cost is increased, cannot be blessed`, list other negative properties (`Brittle`, `Massive`, `Unwieldy`, `Cursed`, `Antique`), and state items have at most one negative property.
- **Community/reference — UOGuide Prized** (`https://www.uoguide.com/Prized`): confirms Publish 86 introduction and the same high-level mechanic.
- **Engine precedent — ServUO**:
  - `Scripts/Misc/AOS.cs`: has `NegativeAttribute.Prized = 0x00000002`, `NegativeAttributes.Prized`, and emits cliloc `1154910` for Prized.
  - `Scripts/Mobiles/PlayerMobile.cs`: `GetInsuranceCost(Item item)` doubles cost when `NegativeAttributes.Prized > 0`.
  - `Scripts/Items/Consumables/ClothingBlessDeed.cs`: rejects Prized items in the bless-deed flow.
  - `Scripts/Services/LootGeneration/RunicReforging/RunicReforging.cs`: rolls Prized as part of negative-property generation and keeps the broader one-negative-property economy context.

## RebirthUO anchors observed in ModernUO issue drafting

- No existing `Prized` implementation was found under `Projects/` by searching `Prized|prized|PRIZED`.
- `Projects/UOContent/Mobiles/PlayerMobile.cs:3713` currently uses a flat `GetInsuranceCost(Item item) => 600`; this shared cost path is referenced by manual insurance, death auto-renewal, and the SA insurance gump.
- `Projects/UOContent/Items/Deeds/ClothingBlessDeed.cs` blocks blessed/insured/non-regular items but has no negative-property check.
- `Projects/Server/Items/Item.cs` owns generic `Insured`, `PaidInsurance`, `BlessedFor`, loot-type display, death protection checks, and `CheckBlessed`; Prized should not directly make an item blessed, insured, cursed, or uninsurable.
- Random magical item generation currently routes through `BaseRunicTool.ApplyAttributesTo(...)` from loot paths such as `LootPack` and `BaseCreature.PackArmor/PackWeapon`.
- `Projects/UOContent.Tests/Tests/Items/Weapons/BanePropertyTests.cs` has useful local patterns: a `RecordingPropertyList` helper and a generation-boundary test proving a later property does not roll unless distribution is explicitly added.

## Recommended implementation shape

1. Treat Prized as a **negative item property**, not as a positive AoS stat. Prefer a deliberately named negative-property container/flag model that can also host Publish 86 siblings (`Brittle`, `Massive`, `Unwieldy`, `Antique`, `Cursed`) without muddying `AosAttribute` semantics.
2. Supported official found-on surfaces for the first parity slice: weapons, armor/shields, and jewelry. Do not include spellbooks or clothing unless a source or shard-policy decision expands the surface.
3. Use `Core.HS` as the practical era gate for Publish 86 unless the target branch has a stricter publish-level gate.
4. Tooltip: use cliloc `1154910` for `Prized` unless local client data proves a different row.
5. Insurance: keep Prized insurable, but increase cost in the shared insurance-cost path. ServUO precedent is `normal cost * 2`; call this out as a parity/default decision because UO.com does not quantify the increase.
6. Blessing: reject Prized in clothing bless deeds and search for any other player-facing blessing flows before implementation.
7. Distribution: do not add loot/runic/reforging generation in the same PR unless explicitly scoped. A storage/tooltip/insurance/blessing PR can be GM/test-only; Publish 86 negative-property generation is a separate economy decision.

## Test expectations

- Store/dupe/serialize Prized on at least one weapon, one armor/shield, and one jewelry item.
- Tooltip row appears in the target era and is absent before the target era.
- Normal items use baseline insurance cost; Prized items use the increased cost; manual insurance, death auto-renewal, and the SA insurance gump all agree.
- Clothing bless deed rejects Prized and still accepts a comparable non-Prized regular item.
- Random `BaseRunicTool.ApplyAttributesTo(...)` does not roll Prized unless distribution is intentionally added.

## Pitfalls

- Do not confuse Prized with `Cursed`: UO.com says Prized increases insurance cost and cannot be blessed; it does **not** say it cannot be insured.
- Do not put Prized into a combat/equipped-value aggregator; it is not a PvP/PvM stat.
- Do not silently adopt ServUO's 2x multiplier as a canonical UO.com fact. It is engine precedent and a defensible default, but UO.com only says the cost is increased.
- Do not broaden official found-on surfaces to spellbooks/clothing without a separate source or shard-policy decision.
