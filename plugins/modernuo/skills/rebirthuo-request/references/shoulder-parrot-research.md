# Shoulder Parrot Research Pattern

Use this as a compact example when a RebirthUO request starts from a third-party shop/item page rather than UO.com or repo code.

## Source classification

- Third-party item/shop pages such as UOWTS can be useful for screenshots, market naming, and observed property text, but treat them as **Community/reference** or **market evidence**, never canonical parity.
- Promote only the facts corroborated by UO.com, UOGuide, UOAlive, ServUO/RunUO, or local repo anchors.
- If the third-party page names properties that UO.com does not list directly, keep them as `Community/reference` unless client data or an engine implementation confirms them.

## Shoulder Parrot findings

Observed third-party page: `https://uowts.com/items/artifacts/the-shoulder-parrot`

UOWTS claims:
- Name: `The Shoulder Parrot`
- Properties: `Blessed`, `Weight: 1 Stone`, `Strength Requirement 10`
- Statless shoulder-slot cosmetic; visible on paperdoll/avatar
- Can be dyed with Natural Dyes; grey part takes dye color
- Double-click makes the parrot fly around the player
- 30 second cooldown on the fly-around action
- Inherits purchaser/player name; other characters can equip it but name does not change
- Robe-slot Transmogrification Potion can apply the parrot skin to other robes

Official UO.com corroboration found:
- `https://uo.com/wiki/ultima-online-wiki/combat/pvm-player-versus-monster/rising-tide/the-black-market-merchant/`
  - Black Market Merchant initially arrived during Rising Tide outside Buccaneer’s Den Bank.
  - Initial inventory includes `a shoulder parrot, as seen on his shoulder, 100,000 doubloons`.
  - This supports source/loop/cost: Rising Tide, maritime cargo/doubloons, Black Market Merchant reward.
- `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-109/`
  - Robe-slot Transmogrification Potion exists.
  - Changelog says shoulder parrots no longer lose flight functionality when using a transmogrification potion.
  - This supports robe-slot transmog relevance and the parrot flight functionality.
- `https://uo.com/wiki/ultima-online-wiki/gameplay/transmogrification-potions/`
  - Transmog potions transfer properties between items of the same equipment slot; Robe Slot exists.
  - Unique name and Blessed status are retained; result cannot be imbued/reforged/enhanced/refined.
- `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-123/`
  - Shoulder Parrots now display on the avatar with full animations.
  - This makes full avatar animation a modern Publish 123+ client behavior, not necessarily an older-era requirement.

Uncorroborated/needs confirmation:
- Exact item ID/art IDs and cliloc label.
- Whether Natural Dye behavior is fully official for the base shoulder parrot rather than observed market behavior.
- Exact implementation of name inheritance on purchase.
- ServUO/RunUO implementation precedent: none found via GitHub code search during the session.

## RebirthUO anchors found

- `Projects/Server/Items/Layer.cs` — local layer enum has no `Layer.Shoulder`; robe-slot/outer-torso treatment is more plausible than adding a new engine layer.
- `Projects/UOContent/Items/Clothing/OuterTorso.cs` — `BaseOuterTorso` uses `Layer.OuterTorso`; `Robe` derives from it and defaults to 3.0 weight.
- `Projects/UOContent/Items/Clothing/BaseClothing.cs` — default AoS strength requirement is 10; clothing supports `LootType.Blessed` and dye hooks.
- `Projects/UOContent/Mobiles/Animals/Town Critters/(UO 3D Only) Parrot.cs` — existing parrot mobile is unrelated to wearable shoulder parrot but may provide creature/body/sound context.
- `Projects/UOContent/Items/Addons/ParrotPerchAddon.cs` — existing parrot perch addon is unrelated to wearable shoulder parrot.
- Searches found no existing local Black Market Merchant, Doubloon, Rising Tide, or Shoulder Parrot implementation.

## Issue framing if requested

Likely classification: **content addition / parity gap**, not a loot artifact.

Affected loops:
- Primary: cosmetics/collection, Black Market Merchant maritime-currency sink.
- Side effects: economy/prestige value, robe-slot transmog, client presentation, animation spam/cooldown.

Risk row:
- Era/ruleset: modern UO, Rising Tide/Publish 106+; transmog fix Publish 109; full avatar animation Publish 123+.
- Facet/map: Black Market Merchant source is Buccaneer’s Den context; maritime cargo/doubloons are ocean/PvM/economy adjacent.
- Economy: 100,000 doubloon sink if canonical merchant is implemented; avoid staff-only hidden item creation.
- PvP/PvM: statless item should not affect combat, but robe-slot transmog can carry appearance/functionality into combat-visible gear.
- Bot/exploit: double-click animation needs cooldown to prevent visual/packet spam.
- Save/client: new wearable class needs source-generated serialization; animation/avatar behavior depends on client support and art IDs.

Suggested issue title:
- `Shoulder Parrot als statless Robe-Slot-Cosmetic / Black-Market-Belohnung prüfen`

Suggested open questions:
- Implement the item alone as custom cosmetic, or wait for Black Market Merchant/doubloon system parity?
- Which publish/client target: Paperdoll-only/legacy behavior, Publish 109 transmog-safe behavior, or Publish 123 full avatar animation?
- Confirm item IDs/clilocs/dye behavior from client data or an engine precedent before implementation.
