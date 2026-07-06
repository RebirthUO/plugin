# Mask of Khal Ankur / Dynamic Treasures research notes

Use these notes when triaging or planning late Live-UO Dynamic Treasures / Halloween event artifacts such as the Mask/Pendant of Khal Ankur. This is source detail, not proof that RebirthUO already implements the feature.

## Source hierarchy used

1. **UO.com official event pages** for canonical event wording and reward properties.
2. **UOGuide item page** for community mechanics/history and cross-event notes.
3. **ServUO source** for implementation precedent, especially reward trader wiring and item class behavior.
4. **Local RebirthUO repo anchors** for implementation state and reachability.

## Useful source URLs

- UO.com Treasures of Khaldun: `https://uo.com/wiki/ultima-online-wiki/seasonal-events/halloween-treasures-of-khaldun/`
- UO.com Artifacts - Events: `https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-events/`
- UO.com Armor Artifacts: `https://uo.com/wiki/ultima-online-wiki/items/artifacts-by-item-type/armor-artifacts/`
- UO.com Treasures of the Archlich: `https://uo.com/wiki/ultima-online-wiki/seasonal-events/halloween-treasures-of-the-archlich/`
- UO.com Publish 101: `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-101/`
- UO.com Publish 114: `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-114/`
- UOGuide API: `https://www.uoguide.com/api.php?action=parse&prop=text&page=Mask%20of%20Khal%20Ankur&format=json`
- ServUO Mask precedent: `Scripts/Services/Seasonal Events/TreasuresOfKhaldun/Items/MaskOfKhalAnkur.cs`
- ServUO Pendant precedent: `Scripts/Services/Seasonal Events/TreasuresOfKhaldun/Items/PendantOfKhalAnkur.cs`
- ServUO reward wiring: `Scripts/Services/Seasonal Events/TreasuresOfKhaldun/KhaldunRewards.cs`
- ServUO event points/drop precedent: `Scripts/Services/Seasonal Events/TreasuresOfKhaldun/KhaldunData.cs`

## Canonical/event facts observed

UO.com Treasures of Khaldun lists **Mask of Khal Ankur (50)** as a reward bought with Artifacts of the Cult. It describes:

- Caddellite Infused
- HP Increase 10
- Mana Increase 10
- Enhance Potions 35%
- Lower Mana Cost 10%
- 15% all resists
- Meteor Breath Charges: 1
- Double-click can cast Meteor Swarm
- Interruptable
- Mana-, reagent-, and skill-check-free
- 5 minute recharge while worn; reset when unequipped
- Available as **Pendant of Khal Ankur** for Gargoyles with Mage Armor

UO.com Artifacts - Events lists the Mask under Dynamic Treasures-style events including Khaldun, The Undead Lords, and The Archlich. The Archlich page lists **Mask/Pendant of Khal Ankur (30)** and states the Archlich event rewards are shard bound.

## Community/reference notes

UOGuide says the mask was originally from Treasures of Khaldun and later available during Treasures of the Archlich with Shard Bound. It also notes that the Caddellite Infused property was added for Treasures of Khaldun, but a Caddellite-infused weapon was still needed even while wearing the mask. Treat that as important mechanics nuance: the mask's Caddellite tooltip is not necessarily a substitute for Caddellite damage eligibility.

## Known source conflicts to preserve in tickets

- **Mana Increase:** UO.com/UOWTS/UOGuide list `Mana Increase 10`; current ServUO code sets `Attributes.BonusMana = 15` on both Mask and Pendant. Do not silently choose ServUO over UO.com.
- **Weight:** UO.com event wording does not settle weight in the excerpt; UOWTS and ServUO show Mask weight 3, UOGuide showed 1 stone. Preserve as a review question if exact weight matters.
- **Mage Armor:** UO.com wording specifically says the Gargoyle Pendant is available with Mage Armor. UOGuide's infobox displayed Mage Armor on the Mask page; treat mask-side Mage Armor as unresolved unless a canonical client capture confirms it.
- **Shard Bound:** Archlich event rewards are shard bound; original Khaldun version may not be. Gate this by source event/version.

## RebirthUO local anchors observed during intake

- No local `MaskOfKhalAnkur`, `PendantOfKhalAnkur`, `Caddellite`, `Artifact of the Cult`, or cliloc anchors `1158701`, `1158731`, `1158732`, `1158662` were found in the checked branch.
- Existing Khaldun anchors are classic/local Khaldun content, not the Dynamic Treasures event stack:
  - `Projects/UOContent/Engines/Khaldun/KhaldunGen.cs` — classic Khaldun generator command.
  - `Projects/UOContent/Engines/Khaldun/PuzzleChest.cs` — Khaldun puzzle chest loot.
  - `Projects/UOContent/Mobiles/Monsters/Humanoid/Melee/KhaldunZealot.cs`
  - `Projects/UOContent/Mobiles/Monsters/Humanoid/Melee/KhaldunSummoner.cs`
  - `Projects/UOContent/Mobiles/Monsters/Humanoid/Melee/KhaldunRevenant.cs`
  - `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs` — Khaldun/Khal Ankur champion entry was observed commented out, so class existence or lore terms are not enough to prove reachability.
  - `Projects/UOContent/Spells/Seventh/MeteorSwarm.cs` — Meteor Swarm exists and can be reused if an item-use wrapper is implemented.

## Recommended ticket framing

Prefer a review ticket framed as **"Mask/Pendant of Khal Ankur as Publish-101+/Dynamic-Treasures event artifacts"** rather than a generic missing-item ticket. The conceptual split matters:

1. **Item-only/event reward surface** — implement Mask/Pendant classes, tooltip, charge/recharge, Meteor Swarm cast behavior, and explicit distribution policy.
2. **Full Treasures of Khaldun system** — Caddellite crafting/damage eligibility, Artifacts of the Cult point drops, researcher/reward gump, event region/duration, and optional Khal Ankur champion integration.

## Side-effect reminders

- PvP: free reagentless Meteor Swarm every 5 minutes can be meaningful AoE burst despite interruptibility.
- PvM: the head/pendant slot stats are strong; avoid adding to generic loot packs.
- Economy: tradeable vs shard-bound changes rare/event value and storage/vendor behavior.
- Era: this is Publish 101+/late Live UO Dynamic Treasures content, not classic Khaldun, AoS, ML, or normal champion loot.
- Implementation: treat Caddellite as a mechanics system, not only an OPL string, if full event parity is scoped.
