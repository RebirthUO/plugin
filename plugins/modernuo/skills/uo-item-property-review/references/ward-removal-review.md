# Ward Removal review notes

## Scope and classification

`Ward Removal` is a special, active-use talisman property rather than a generic AoS stat, hit proc, or ordinary imbuing property. The canonical named item is the Britain Library Community Collection **Talking to Wisps** talisman. The current `item_property.yml` issue form is incomplete for this class: `Found on` has no `Talismans` option and `Property Type` has no `Active`/`Usable` option. Preserve the mismatch explicitly; never classify the property as armor, jewelry, shields, spellbooks, or weapons merely to satisfy the dropdown.

## Source evidence

- **Canonical, UO.com Magic Item Properties:** <https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/> lists `Ward Removal` as `N/A` intensity, `No` imbue weight, `Talismans (L)`, `N/A` cap, and “Removes any protective spells in effect on a target.”
- **Canonical, UO.com Community Rewards:** <https://uo.com/wiki/ultima-online-wiki/gameplay/npc-commercial-transactions/community-collections/community-rewards/> lists `Talking To Wisps` at 550,000 points with Ward Removal on target, weight 1 stone, Spirit Speak +3, and Evaluate Intelligence +5.
- **Canonical, UO.com Clothing and Talisman Artifacts:** <https://uo.com/wiki/ultima-online-wiki/items/artifacts-by-item-type/clothing-and-talisman-artifacts/> identifies Talking to Wisps as a Library Collection talisman.
- **Canonical, UO.com Publish 54:** <https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2008-2/publish-54-10th-july/> records that the Talisman of Ward Removal no longer works against friendly players in Trammel. Use this as the explicit facet/PvP restriction. It is the earliest directly verified official behavior evidence in the review, not necessarily the introduction publish.
- **Community/reference, UOGuide Ward Removal:** <https://www.uoguide.com/Ward_Removal> says a talisman can remove up to six wards/beneficial buffs from a target.
- **Community/reference, UOGuide named item:** <https://www.uoguide.com/Library_Talisman_-_Talking_to_Wisps_Ward_Removal> identifies the item as a 550,000-point Britain Library reward, requiring a Mondain's Legacy account, activated by double-click, with Spirit Speak +3 and Evaluate Intelligence +5.
- **Engine precedent, ServUO:** `Scripts/Items/Equipment/Talismans/BaseTalisman.cs` removes Magic Reflection, Reactive Armor, Protection, and two Eodonian potion effects; `CollectionsBritLibraryTalismans.cs` defines the named item with label `1073356`, item ID `0x2F5B`, and a 1200-second recharge. Treat these as implementation clues, not canonical parity.

## RebirthUO anchors and current gap

The current repository already has partial generic infrastructure:

- `Projects/UOContent/Items/Talismans/BaseTalisman.cs:14-20`: `TalismanRemoval.Ward = 390`.
- `BaseTalisman.cs:187-193`: serialized removal field and save flag.
- `BaseTalisman.cs:401-533`: equipped double-click and target setup.
- `BaseTalisman.cs:812-994`: target validation, recharge/charge checks, Ward case, current removal of `MagicReflectSpell.EndReflect`, `ReactiveArmorSpell.EndArmor`, and `ProtectionSpell.EndProtection`, localized messages `1072402`/`1072403`, then `OnAfterUse`.
- `Projects/UOContent/Items/Talismans/`: no concrete `TalkingtoWispsTalisman` was present during review.
- `Projects/UOContent/Engines/ML Quests/Items/FriendsOfTheLibraryApplication.cs` and `FriendOfTheLibraryToken.cs`: Britain Library quest/item anchors exist, but reward acquisition should remain separate unless explicitly scoped.
- No Ward Removal-specific focused test was present; use the existing `CraftExceptionalBonusTalismanTests` pattern for construction, OPL, dupe, serialization, and behavior coverage.

## Conservative implementation default

For a first issue/implementation slice, add the concrete Talking to Wisps item and focused tests while reusing the existing `TalismanRemoval.Ward` path. Keep the supported effect list to the three local spell helpers: Magic Reflection, Reactive Armor, and Protection. Do not broaden to arbitrary beneficial buffs or ServUO's Eodonian potion effects without an explicit shard-policy decision and local system support. Keep imbuing, runic crafting/reforging, random loot, and Britain Library reward registration separate from storage/use mechanics.

Separate the property from Mysticism `Purge Magic`: Purge Magic is a spell with skill checks, immunity, mana-disruption fallback, and different targeting semantics, not a duplicate implementation target for Ward Removal.

## Open decisions to preserve

1. Exact introduction publish is unresolved. Use Mondain's Legacy as the era and Publish 54 as the earliest directly verified behavior baseline rather than claiming Publish 36.
2. Official UO.com wording, UOGuide's six-ward wording, local three-spell support, and ServUO's Eodonian additions conflict. Keep the conflict visible and default to the local three-spell slice.
3. The named reward item can be implemented without automatically adding Britain Library acquisition or distribution.
4. Official sources do not define whether a valid target with no supported ward consumes cooldown. Preserve the current `BaseTalisman` use path as the conservative default and test it explicitly.
