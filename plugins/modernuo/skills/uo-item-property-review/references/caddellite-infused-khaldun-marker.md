# Caddellite Infused — Khaldun Event Marker Review

## Trigger

Use this note when a RebirthUO/ModernUO request asks whether `Caddellite Infused` should be implemented as an item property, especially around `Mask of Khal Ankur`, `Pendant of Khal Ankur`, `Cultist's Ritual Tome`, Treasures of Khaldun, or Khal Ankur champion content.

## Source classification

- **Canonical — UO.com Publish 101 / Treasures of Khaldun**: Caddellite was introduced for the Halloween 2018 Treasures of Khaldun event. Normal weapons, spellbooks, and musical instruments had no effect against the empowered Khaldun creatures; only items crafted from Caddellite-infused materials worked. Caddellite resources came from mining/lumberjacking/fishing with special Caddellite harvesting tools in the Lost Lands. Crafting had to occur at the Khaldun camp; crafting elsewhere did not produce Caddellite-infused items. Caddellite-infused weapons could be imbued/reforged and Caddellite did not count toward imbuing weight.
- **Canonical — UO.com Artifacts/Events and later Halloween pages**: `Mask of Khal Ankur`, `Pendant of Khal Ankur`, and `Cultist's Ritual Tome` list `Caddellite Infused` as a fixed item line. Later Dynamic Treasures events reused the Mask/Pendant and often added `Shard Bound`; this does not make Caddellite a generic magic-property roll.
- **Canonical negative evidence — UO.com Magic Item Properties**: `Caddellite` / `Infused` is absent from the general Magic Item Properties table. Treat it as event content, not an AoS/SA property family.
- **Community/reference — UOGuide Treasures of Khaldun**: Confirms the original event required Caddelite/Caddellite-infused weapons, spellbooks, and instruments; also notes later annual reactivations could make rewards available without the original entrance quest or Caddellite combat requirement.
- **Engine precedent — ServUO**: Current ServUO models Caddellite as `Items/Internal/ItemSockets/Caddellite.cs`, not as `AosAttribute`, `AosWeaponAttribute`, or `AosArmorAttribute`. The socket emits cliloc `1158662` (`Caddellite Infused`), implements `CheckDamage`, harvest infusion, craft infusion, and `BuffIcon.CaddelliteInfused`.

## RebirthUO state observed in session

Local RebirthUO did not have `Caddellite`, `Caddelite`, `Caddellite Infused`, `AttachSocket`, or cliloc `1158662`. Relevant available anchors were:

- `Projects/Server/Items/Item.cs` — `SavedFlags`, `GetSavedFlag`, `SetSavedFlag`, base OPL plumbing, and nontransferable transfer hooks.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` — weapon tooltip and combat item surface.
- `Projects/UOContent/Items/Skill Items/Magical/Spellbook.cs` — spellbook tooltip/property surface.
- `Projects/UOContent/Items/Skill Items/Musical Instruments/BaseInstrument.cs` — instrument tooltip/property surface.
- `Projects/UOContent/Engines/CannedEvil/ChampionSpawnInfo.cs` — Khaldun/Khal Ankur champion spawn rows were commented out in the inspected branch.
- `Projects/UOContent/Spells/Seventh/MeteorSwarm.cs` — Meteor Swarm spell already existed for Mask/Pendant ability work.

## Decision guidance

Do **not** implement `Caddellite Infused` as a normal magic item property:

- Not an AoS/SA container value.
- Not a runic/loot/reforging/imbuing rollable property.
- Not a stat-bearing attribute like LMC, SDI, Mage Armor, Splintering, etc.

If Treasures of Khaldun or Khal Ankur parity is in scope, implement it as a **persistent content marker** with a tooltip line and event mechanics:

- Candidate marker: dedicated helper/state such as `CaddelliteInfusion`, or a carefully allocated `Item.SavedFlags` bit if no broader content-flag system exists.
- Tooltip: cliloc `1158662` (`Caddellite Infused`) on affected item families.
- Mechanics: Khaldun event creatures can gate incoming damage through a `CheckDamage`-style helper, treating infused weapons as valid for melee/ranged and infused spellbooks as valid for spell damage. Instruments and pet treats require separate Bard/pet hooks if scoped.
- Crafting/harvest: event tools produce infused resources; crafting in the Khaldun camp with infused resources marks outputs; crafting outside the camp must not mark outputs.
- Distribution: keep separate from storage/tooltip/gameplay. Event rewards can be pre-marked, but random loot/runic/imbuing should not gain Caddellite unless a Treasures of Khaldun ticket explicitly enables it.

For isolated `Mask of Khal Ankur` / `Pendant of Khal Ankur` parity without the full event system, it is acceptable to show the tooltip line as fixed artifact presentation, but document that the line is flavor/parity-only until Khaldun event damage gating exists.

## Pitfalls

- Do not place Caddellite in `AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, `SaWeaponAttribute`, or extended weapon property containers.
- Do not infer random loot distribution from the presence of the tooltip line on fixed event artifacts.
- Do not treat the Mask/Pendant line as sufficient for Khaldun combat parity; source explicitly says Caddellite weapons/spellbooks/instruments were required, and UO.com also notes the Mask/Pendant meteor breath needed a fix to work against Khaldun creatures while Caddellite equipment was still required.
- Do not make Caddellite count toward imbuing weight; UO.com states it does not.
- Spellbooks, instruments, pet treats, and event rewards are separate affected surfaces; avoid solving only weapons and calling Treasures of Khaldun complete.

## Suggested issue framing

Title: `Prüfen: Caddellite Infused als Khaldun-Event-Marker statt AoS-Property`

Acceptance criteria should distinguish:

- Tooltip-only support for fixed artifacts.
- Persistent marker support on weapons/spellbooks/instruments/resources if event mechanics are in scope.
- Khaldun damage-gate behavior.
- Crafting/harvesting/event distribution boundaries.
- Explicit non-goal: no random magic-property rollout.
