---
name: "uo-housing-houses-multis"
description: "Use when working with the UO housing system in ModernUO/RebirthUO servers - BaseHouse, HouseSign, HouseRegion, multi components, lockdown and secure storage, friend/co-owner/access/ban lists, house placement and customization, IDOC decay stages, demolition-pending vendor rental contracts, addon components (forge/anvil/loom), and HouseGumpAOS. Use when placing a house, debugging a lockdown bug, wiring a friend list, debugging a decay cycle, or auditing a per-facet housing rule."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Housing, Houses, Multis

## Overview

The UO housing system is one of the most distinctive features of the game: players place custom multi-component houses on a facet, decorate them, store items securely, and decay over time if not maintained. The engine treats each house as a `BaseHouse` (a `BaseMulti` subclass) which owns a list of `AddonComponent` items (the multi tiles), a `HouseSign` (the deed), a `HouseRegion` (the rule zone), and several `Item`-based addon entities (forge, anvil, loom, etc.).

The central file is `Projects/UOContent/Multis/Houses/BaseHouse.cs`. Addons live in `Projects/UOContent/Multis/Houses/`. House sign and gump code in `Projects/UOContent/Multis/Houses/HouseSign.cs`, `HouseGumpAOS.cs`, etc. The region subclass is `Projects/UOContent/Regions/HouseRegion.cs`. The decay system is `DynamicDecay.cs`.

This skill covers the multi system, the house placement flow, the lockdown/secure mechanism, the friend/co-owner/access/ban lists, the IDOC decay cycle, the customization mode, the per-facet housing rules, and the addon component model. The new Custom housing system (post-AOS) is the standard for new content.

## When to Use

- Adding a new house design (Custom housing, 7x7 to 18x18).
- Debugging why a lockdown or secure item was lost.
- Wiring a friend list or a co-owner permission check.
- Auditing the IDOC decay cycle.
- Adding a new addon component (forge, loom, anvil, table, etc.).
- Resolving a placement collision.
- Wiring a guild hall or shared house.
- Auditing per-facet housing rules (no housing in Trammel guards, Ilshenar restrictions, Malas special).

Don't use for:

- Base item/mobile entity model (use `uo-items-foundation`).
- The map/facet/region system itself (use `uo-world-facets-regions`).
- The loot/vendors system (covered in `uo-loot-generation-artifacts` and BOD).

## The House Component Model

A `BaseHouse` is composed of:

- `MultiComponent` tiles: the `AddonComponent` items that visually make up the house. Each is a real `Item` with `ItemID` and `Location`, parented to the multi or its foundation.
- `HouseSign`: the deed plaque in front of the house. Owns the `Owner`, the `Friends`, the `CoOwners`, the `Access` list, the `Bans`, and the `Price`.
- `HouseRegion`: the `Region` subclass for the house's footprint. Enforces lockdown rules, the friend list, and the ban list via region hooks.
- Addon components: `BaseAddon` instances (forge, anvil, loom, etc.) that the player places inside the house. These are not part of the multi but are tracked as house storage.
- `Lockdown` / `Secure` counters: the per-house counts of items locked down or secured.

The `BaseHouse` aggregates all of these. The footprint is a 2D polygon defined by the multi's `MultiData` (the tile layout).

## House Placement

Per `www.uoguide.com/Houses`, a player uses a **House Placement Tool** to place a house. The tool is a `HousePlacementTool` item bought from an NPC Architect. The placement flow:

1. Player double-clicks the tool, selects a house design.
2. The tool tests the target `Point3D` for placement validity:
   - The plot must be empty (no blocking tiles, no other multis within 5 tiles).
   - The plot must be on a facet that allows housing (`NoHousingRegion` excludes it).
   - The plot must be in a valid town or wilderness area.
3. The player confirms; the tool deducts gold from the player's bank and creates the `BaseHouse` instance.
4. The multi tiles are added to the world as `AddonComponent` items.
5. The `HouseSign` is created at the front of the house.
6. The `HouseRegion` is registered with the `Map`.
7. The player is set as the `Owner`.

The `HousePlacementTool` is the user-facing entry point. For code-driven placement (e.g. NPC-built structures or quest rewards), the constructor chain `new BaseHouse(...).Construct()` (or a typed subclass) is the path.

## Custom vs Pre-Built Houses

Per the `Houses` article, the two housing categories:

- **Pre-Built**: Original and Renaissance houses. Each is a fixed multi with a fixed price. Examples: `SmallStonePlasterHouse`, `TwoStoryWoodPlasterHouse`, `Keep`, `Castle`.
- **Custom** (post-AOS): Introduced with the Age of Shadows. The player can design the house from a fixed set of foundation pieces (7x7 to 18x18) and customize the interior with addons. The `HouseCustomization` system handles placement and editing.

Custom houses are the dominant post-AOS design. The foundation types include Small, Medium, Large, etc. The 18x18 is the largest common foundation; Keeps and Castles are pre-built with custom contest designs (Publish 101+).

## HouseRegion: The Rule Zone

`HouseRegion` is a `Region` subclass that wraps the house's footprint. The hooks:

- `OnEnter` / `OnExit`: log who enters and exits (for friend list verification, thief entry checks).
- `CanBeHarmful`: restricts PvP in the house (Trammel rules).
- `IsMobileAllowed`: blocks banned players, dead players (for some houses), and `Owner`/`Friend`/`CoOwner`/`Access` rules.
- `OnDeath`: special loot rules (trapped items, friend-only looting, etc.).
- `OnBeginSpellCast`: blocks field spells and field-effect target tracking.
- `OnTravel`: prevents `Recall` from the house to outside (Recall is allowed to/from inside the house, but blocked from outside the house to inside).

The `HouseRegion` is automatically created when a `BaseHouse` is placed and destroyed when the house is demolished.

## Lockdown and Secure

The `BaseHouse` has two storage mechanisms for items inside the house:

- **Lockdown**: items are pinned in place (cannot be moved). Counted in `BaseHouse.LockDownCount`. Items are visible to everyone but only the owner or co-owner can pick them up.
- **Secure**: items go into a per-house "secure container" (a `SecureTradeContainer` or `HouseSecureContainer`). Only the owner or co-owner can access them. Items are not visible to non-friends.

The total lockdown + secure capacity is determined by the house's `MaxLockDowns` (a function of foundation size). Small houses (7x7) have ~100 lockdowns; Keeps/ Castles have 1500+.

The `BaseHouse` checks the lockdown count on every `OnItemAdded`, `OnItemRemoved`, and the `Owner`-driven "lock down" gump action. Exceeding the capacity throws a `HouseLockdownException` and the action is reverted.

The `Container`/`Item` placement on lockdown is via the `BaseContainer` and `BaseAddon` integration. The `LockDown` flag is set on the item via `Item.IsLockedDown` (set via `Item.SetTempFlag(LockedDownFlag, true)`).

## Friend, Co-Owner, Access, Ban Lists

`BaseHouse` has four typed lists (all `Mobile` lists):

- `Owner`: a single `Mobile`. Set at placement.
- `CoOwners`: can use the house, can manage lockdowns, can add friends, but cannot demolish or transfer ownership.
- `Friends`: can enter, can be granted lockdown access by the owner, can be denied by access list.
- `Access`: a flat list of who can enter. Friends and co-owners are implicit members; access is for non-friend players.
- `Bans`: blocked from entry. Enforced by `HouseRegion.IsMobileAllowed`.

The lists are mutable via the `HouseGumpAOS` (the gump the owner opens by double-clicking the sign). Per the `Publish_69` notes, the lists can hold up to 250 members each; larger lists are paginated in the gump.

A `CoOwner` can `Add` or `Remove` from the friends/access/bans lists, set the house name, and manage lockdowns. The `Owner` is the only one who can transfer ownership, demolish, or place a new house.

## Customization Mode

`HouseCustomization` (`Projects/UOContent/Multis/Houses/Customization/`) is the Custom housing editor. The player double-clicks the sign and selects "Customize" to enter the editor. The editor is a gump-driven system that lets the player:

- Place foundation pieces (7x7, 9x9, 11x11, 13x13, 15x15, 18x18).
- Place wall, floor, and stair pieces.
- Place door pieces.
- Place addon items (forge, anvil, loom, etc.).
- Customize the house's hue (Paint hue, per the ML-era "Customizable Houses" publish).
- Save and exit.

The editor uses a Customization State object that holds the in-progress design; the design is committed when the player clicks "Commit" in the gump.

The Customization system is gated by `Core.AOS` (introduced with the expansion). Pre-AOS houses are not customizable.

## IDOC Decay Cycle

`DynamicDecay` (`Projects/UOContent/Multis/Houses/Decay/DynamicDecay.cs`) drives the per-house decay. Per `www.uoguide.com/House_Decay`, the 6 (+1) decay stages:

1. **Like New**
2. **Slightly Worn**
3. **Somewhat Worn**
4. **Fairly Worn**
5. **Greatly Worn**
6. **In Danger of Collapsing**
7. **Demolition Pending** (if rental vendors are present)

Each stage lasts a real-time window (typically 1-2 days per stage, configurable). The decay advances on a server save tick. The `DynamicDecay` checks the `Owner`'s login activity; if the owner has not refreshed (i.e. logged in) within the window, the decay advances.

A `HouseSign` refresh resets the decay timer. Players can refresh by double-clicking the sign, but only the owner or co-owner can do so.

When the house reaches "In Danger of Collapsing" (IDOC), the timer shortens to 5/10/15 hours (per Publish 89). When the timer expires:

- The house collapses (the multi tiles are deleted).
- All items fall to the ground.
- `Grubbers` spawn with a random subset of the house's items in their backpacks.
- Trial accounts cannot pick up IDOC loot (per Publish 89).

If the house has rental vendors, it enters "Demolition Pending" instead of falling. The phase lasts as long as the rental contracts plus 9 days for vendor owners to retrieve their items. The house refreshes automatically during this phase; once the contracts expire, the house falls through the normal IDOC cycle.

The `Refresh` action requires the `Owner` or a `CoOwner` to be near the sign. The `Refresh` is also implicit on `Owner` login. Per `uo.stratics.com/content/misc/decay.shtml`, refreshing twice a week is sufficient to keep most houses stable.

## Per-Facet Housing Rules

The housing availability matrix (per `uo-world-facets-regions`):

- **Felucca**: full housing allowed, including Keeps and Castles.
- **Trammel**: full housing allowed, including Keeps and Castles.
- **Ilshenar**: NO player housing (`NoHousingRegion` covers most of the map). Only NPC structures.
- **Malas**: full housing allowed, especially around Luna/Umbra.
- **Tokuno**: limited housing, expensive real estate.
- **Ter Mur**: full housing allowed, especially in the Royal City area.
- **Eodon (ToL)**: limited housing, special rules.

The check is `Region is NoHousingRegion` or `Map == Map.Ilshenar`. The `BaseHouse.PlacementValid` static helper is the canonical validator.

## Addons and Decoration

An `Addon` is a multi-component decoration. The `BaseAddon` class (`Projects/UOContent/Items/Addons/`) holds the component list. Each `AddonComponent` is an `Item` with a `Location`, `ItemID`, and `Hue`.

Standard addons include:

- Forge, Anvil, Loom, Spinning Wheel (crafting stations).
- Training dummies (Archery Buttes, Sword Training dummies).
- Decorative: Furniture, Rugs, Wall Hangings, Plants.
- Functional: doors, teleporters (intra-house only), house teleporters.

The `BaseAddon` is added to a `BaseHouse` via the `HouseSign.AddAddon(gump)` gump or by double-clicking the addon in a house.

`AddonComponent` items have a `House == house` reference set when added. When the house falls, all `AddonComponent`s with the matching `House` reference are also deleted.

## Custom Contests and Publish 101+

`Keep` and `Castle` designs have been added in periodic contests since Publish 101. The designs are added to the `HousePlacementTool` as a new "Custom Keep" or "Custom Castle" option. The published designs are listed in `Publish_101`, `Publish_103`, etc. on UOGuide.

The custom contest designs are stored as multi data files. The engine reads them at startup and adds the designs to the `HousePlacementTool` menu.

## Common Pitfalls

1. **Iterating `World.Items` to find house components.** Use `BaseHouse.Addons` and `BaseHouse.Components` instead. The house knows what it owns.
2. **Setting `IsLockedDown` directly on an `Item` outside of a `BaseHouse` context.** The `LockedDownFlag` is a temp flag set on the item; the engine relies on the house's lockdown count to validate. Bypassing the count lets players exceed capacity.
3. **Forgetting the `OnItemAdded` / `OnItemRemoved` overrides on the `BaseHouse`.** These count lockdown/secure items, validate placement, and update the sign. Skipping them produces "ghost" lock counts.
4. **Setting the `Owner` to a `PlayerMobile` without checking that the player can own houses.** Trial accounts cannot own Keeps/Castles in some eras. The `HousePlacementTool` validates; bypass constructors may not.
5. **Calling `BaseHouse.Delete()` directly in a quest script.** The proper cleanup is `BaseHouse.Demolish()`, which handles the IDOC notification, the addon cleanup, the sign deletion, the region deregistration, and the floor item drop. Direct delete leaks the region and leaves orphaned addons.
6. **Adding an addon to a house whose `Map` does not match the addon's `Map`.** The addon is added to a different facet, which the player cannot see. The validation in `BaseHouse.AddAddon` checks the map.
7. **Forgetting to set `MaxLockDowns` on a Custom house.** Custom houses have a foundation-size-derived `MaxLockDowns`; the constructor must call the helper.
8. **Mutating `BaseHouse.Owner` directly.** The owner change is a multi-step process that updates the `HouseSign`, the `Bans`, the decay timer, and the regional ownership hooks. Use `BaseHouse.SetOwner(newOwner)` (or the equivalent) which handles the full transition.
9. **Granting access via the `Access` list to a player who is also a `Friend`.** Friends are already in the implicit access set; adding them to `Access` is a duplicate.
10. **Not running the `DynamicDecay` test in staging.** IDOC is a slow real-time cycle; the regression test for the 5/10/15-hour collapse window is the only safe way to validate the timer changes.

## Common Recipes

### Adding a New House Design

```csharp
public class MyCustomHouse : BaseHouse
{
    public MyCustomHouse(Mobile owner) : base(0x13F0 /* multi ID */, owner, 1100 /* storage */, 1100 /* lockdowns */)
    {
        // Multi data is read from MultiData.mul (the canonical multi tile data)
    }
}
```

### Wiring a Custom Gump Action

```csharp
public override void OnDoubleClick(Mobile from)
{
    if (!IsOwner(from) && !IsCoOwner(from))
    {
        from.SendLocalizedMessage(502092); // You must be the owner, co-owner or friend of this house to do that.
        return;
    }
    from.SendGump(new MyCustomHouseGump(from, this));
}
```

### Adding a Friend Programmatically

```csharp
house.AddFriend(targetMobile);
house.InvalidateProperties();
```

### Setting Up an IDOC Test

```csharp
// In a test, force the house to "In Danger of Collapsing"
house.DecayState = DecayState.InDangerOfCollapsing;
house.DecayEnd = DateTime.UtcNow.AddMinutes(5);  // 5 minutes from now
// Run the dynamic decay tick to verify the collapse
DynamicDecay.Tick();
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New house design: `BaseHouse` subclass is created, multi data is registered, lockdown counts match the design's spec.
- [ ] House placement: the `PlacementValid` check passes for legal plots, fails for plots inside `NoHousingRegion` or on a blocked tile.
- [ ] Lockdown: setting `IsLockedDown = true` updates `BaseHouse.LockDownCount`; exceeding capacity throws.
- [ ] Secure: items in `HouseSecureContainer` are only accessible by owner/co-owner.
- [ ] Friend list: the gump's friend list update propagates to `Region.IsMobileAllowed`.
- [ ] Co-owner: co-owner can add friends, set lockdowns, but cannot demolish.
- [ ] Customization: `HouseCustomization` enters edit mode, places pieces, and commits the design.
- [ ] IDOC: the decay stages advance on the configured schedule; the collapse deletes the multi, the addons, and the sign.
- [ ] Decay refresh: `HouseSign.Refresh()` resets the timer; refresh by login works.
- [ ] Per-facet: housing is blocked in `NoHousingRegion` and on Ilshenar, allowed on other facets.
- [ ] Addon cleanup: when the house falls, all addons with `House == thisHouse` are deleted.

## Related Skills

- `uo-items-foundation` - the `Item` and `BaseContainer` model used for storage and lockdown.
- `uo-world-facets-regions` - the `Region` model and the per-facet housing rules.
- `uo-skills-stats-races` - the racial restrictions on house placement (some races cannot place in certain areas).
- `uo-combat-pipeline` - the combat rules that vary per facet (Trammel-safe housing).
- `uo-magic-spells` - the field-spell blocking in house regions.
- `uo-loot-generation-artifacts` - the rental vendor loot and the IDOC `Grubber` spawn.
- `uo-crafting-recipes-resources` - the craftable addon items (forge, anvil, loom).
- `modernuo-content-patterns` - canonical templates for new addons.
- `modernuo-era-expansion` - the era gate for Custom housing (`Core.AOS`).
- `www.uoguide.com/Houses` and `/House_Decay` (offline reference) - the canonical house placement, friend list, and IDOC documentation.
- `uo.stratics.com/content/misc/decay.shtml` (offline reference) - the decay refresh rules and the per-stage timer.
- `docs/mondains-legacy-content-matrix.md:82` (offline reference) - the ML-era `DynamicDecay` and `HouseGumpAOS` regression coverage.
