# Bulk Order Deeds Domain Map

Detailed architecture, tables, examples, and historical observations deferred from the skill entrypoint. Re-check symbols and era rules in the active branch.

Current RebirthUO branch note: `BulkOrderSystem` now owns profession-gated BOD
support for Smith, Tailor, Alchemy, Inscription, Tinkering, Cooking, Fletching,
and Carpentry, with later craft paths gated through `Core.TOL`. Treat that as
repository implementation evidence only; verify official publish chronology and
player-facing rules through `uo-official-evidence`.

## Overview

The Bulk Order Deed (BOD) system lets a player pick up a craft order from an NPC, fill it with crafted items, and turn it back in for gold, fame, reward points, or BOD rewards. The BOD book (BOB) stores and filters deeds across the supported profession surface.

Community pages contain chronology leads for early and expanded BOD support,
but those dates and craft lists are not an official contract. Verify every
publish/chronology claim through `uo-official-evidence`, then describe the
configured repository's implemented craft set separately.

The engine code lives in `Projects/UOContent/Engines/Bulk Orders/`. The base class is `BaseBOD.cs`. Profession variants include `Small*/Large*BOD` pairs for Smith, Tailor, Alchemy, Inscription, Tinkering, Cooking, Fletching, and Carpentry. The BOB code is in `Books/`. The gumps include `SmallBODGump.cs`, `LargeBODGump.cs`, `BODBuyGump.cs`, `BODPointsChoiceGump.cs`, `BOBGump.cs`, and `BOBFilterGump.cs`.

This skill covers the BOD hierarchy, the BOD acceptance flow, the turn-in pipeline, pending reward points, the BOB storage and filter system, per-craft reward calculators, era-gated cooldowns, the Bribery system, generated persistence schemas, the BulkMaterialType system, and vendor-side BOD offer mechanics.

## When to Use

- Adding a new BOD type or maintaining an existing profession BOD.
- Debugging a BOD turn-in that does not validate the items.
- Wiring a BOD reward item (e.g. a new dye tub or a new tool).
- Adding a BOD filter to the BOB.
- Auditing the BOD reward pool.
- Adding the Bribery option to a BOD vendor.
- Adjusting the BOD turn-in cooldown for ML.
- Reading the per-era BOD scope and separating official publish evidence from repository feature gates.

Don't use for:

- The base crafting system (use `uo-crafting-recipes-resources`).
- The base item model (use `uo-items-foundation`).
- The quest reward system (use `uo-quests-engine-ml`).
- Loot generation (use `uo-loot-generation-artifacts`).

## The BOD Hierarchy

`Projects/UOContent/Engines/Bulk Orders/BaseBOD.cs` is the abstract base. Concrete branches:

- `SmallBOD` plus profession subclasses such as `SmallSmithBOD`, `SmallTailorBOD`, `SmallAlchemyBOD`, `SmallInscriptionBOD`, `SmallTinkerBOD`, `SmallCookingBOD`, `SmallFletchingBOD`, and `SmallCarpentryBOD`: requires the player to craft one item type, in a small quantity.
- `LargeBOD` plus matching profession subclasses: requires the player to collect several `SmallBOD`s, each filling one item type.

The `SmallBulkEntry` and `LargeBulkEntry` are the per-entry data structures. A `SmallBOD` has one `SmallBulkEntry`; a `LargeBOD` has several `SmallBulkEntry`s (the small BODs that combine into the large).

The `BaseBOD` key fields:

| Field | Purpose |
|---|---|
| `AmountMax` | The required count of the item. |
| `Number` | The BOD's serial number. |
| `Type` | The `Type` of the required item (e.g. `typeof(Katana)`). |
| `Graphic` | The `ItemID` for the required item. |
| `RequireExceptional` | Whether the item must be Exceptional. |
| `Material` | The `BulkMaterialType` (Iron, DullCopper, Shadow, Copper, Bronze, Golden, Agapite, Verite, Valorite, etc.). |
| `Owner` | The `PlayerMobile` who owns the BOD. |
| `Entries` | The per-entry list (size 1 for Small, N for Large). |

## BOD Acceptance

The player gets a BOD from an NPC vendor. The vendor has a context menu entry "Bulk Order Info" (or "Get BOD") that:

1. Checks the player's skill (e.g. `Blacksmithing >= 0.1` for a Smith BOD).
2. Checks the player's per-vendor cooldown (default 6 hours since last pickup).
3. Rolls a BOD type (Small or Large), a material, and an item type.
4. Creates a `SmallBOD` or `LargeBOD` instance and adds it to the player's backpack.
5. If the player's `BOD` cooldown is 0 (pre-ML), the cooldown is not set; if `Core.ML`, the cooldown is set to the configured interval.

`Publish_74` introduced the 6-hour BOD pickup limit (no longer skill-dependent) and the 3-BOD cache (the vendor holds up to 3 unclaimed BODs or 18 hours of pickups; the player can claim all 3 in quick succession).

The BOD's gump is `SmallBODGump` or `LargeBODGump`. The gump shows the item type, the required count, the material, and the optional `Exceptional` flag.

## BOD Turn-In

The player fills the BOD by crafting the required items in the right quantity, with the right material, and the right `Exceptional` status. The player double-clicks the BOD to open the gump. The gump's "Combine" / "Turn In" button:

1. Validates that the player has the right quantity of the right item.
2. Validates the material (the item's `Resource` matches the BOD's `Material`).
3. Validates the `Exceptional` flag (the item's `Quality == Exceptional`).
4. For `LargeBOD`: validates that the player has the right number of `SmallBOD`s (in their backpack) that match the entries.
5. For `LargeBOD`: combines the small BODs into the large BOD.
6. Triggers the turn-in: the BOD is consumed, the items are consumed, and the reward is dropped into the player's backpack.

The turn-in reward is selected from `Projects/UOContent/Engines/Bulk Orders/Rewards.cs`. The reward is a `BaseRewardItem` (e.g. a Colored Anvil, Mining Gloves, a smoldering loot item, etc.) or a `BaseTool` (e.g. a Runic Hammer, a Runic Sewing Kit).

The reward probability is per-craft and per-quality. The `BulkOrderSystem` (the static class) holds the per-craft reward table.

The ML-era turn-in cooldown (per `docs/mondains-legacy-content-matrix.md:78`):

- Pre-ML: no turn-in cooldown.
- ML+: 6-hour turn-in cooldown for the `ML` BOD path. The pre-ML control is 0 (no cooldown).
- The cooldown is checked in `BaseBOD` and enforced in the vendor's turn-in callback.

## The BOB (Bulk Order Book)

`Projects/UOContent/Engines/Bulk Orders/Books/BulkOrderBook.cs` is the BOB item. The BOB stores the player's BODs in a tagged book, with per-craft filters and a per-book capacity (default 500 entries).

The BOB has the following fields:

| Field | Purpose |
|---|---|
| `Entries` | The list of `BaseBOBEntry` items (typed: `BOBSmallEntry`, `BOBLargeEntry`, `BOBLargeSubEntry`). |
| `Filter` | The `BOBFilter` (per-craft, per-type filter). |
| `MaxEntries` | The capacity (500 by default). |

The `BOBGump` is the gump the player sees when they open the BOB. The `BOBFilterGump` is the filter configuration. The `BODBuyGump` is the gump for buying a new BOD directly from the BOB (Publish 95+).

The BOB is gated by the `BOBFilter` system: the player can configure per-craft and per-item-type filters so the BOD accept gump only shows the relevant BODs.

## The BulkMaterialType System

`Projects/UOContent/Engines/Bulk Orders/BulkMaterialType.cs` is the enum that maps a `BulkMaterialType` value to the per-item `CraftResource` and the per-craft material gate. The values:

| Material | CraftResource | Use |
|---|---|---|
| `None` | `Iron` / `Regular` | Default for most BODs. |
| `DullCopper` | `DullCopper` | Tier 1 colored ingot. |
| `ShadowIron` | `ShadowIron` | Tier 2. |
| `Copper` | `Copper` | Tier 3. |
| `Bronze` | `Bronze` | Tier 4. |
| `Golden` | `Golden` | Tier 5. |
| `Agapite` | `Agapite` | Tier 6. |
| `Verite` | `Verite` | Tier 7. |
| `Valorite` | `Valorite` | Tier 8. |
| `Leather` | `Leather` (Regular) | Tailor. |
| `Spined` | `SpinedLeather` | Tailor. |
| `Horned` | `HornedLeather` | Tailor. |
| `Barbed` | `BarbedLeather` | Tailor. |
| `Cloth` | `Regular Cloth` | Tailor. |

The BOD's `Material` is matched against the crafted item's `Resource` (e.g. `CraftResource.DullCopper` for `DullCopper` ingots). The Tailor variants check the leather type and the cloth type.

The `MondainsLegacyBodRewardColorTests` covers the eight special ore hues for the Colored Anvil and mining-glove rewards plus their expected weight/bonus/label contracts.

## Bribery System (Publish 74+)

Per `www.uoguide.com/Bulk_Order_Deed`, the Bribery system (introduced Publish 74) lets the player bribe a BOD vendor to upgrade an empty BOD:

- Upgrades the quantity (e.g. 10 → 15 → 20).
- Upgrades the quality (Regular → Exceptional).
- Upgrades the material (Iron → Dull Copper → ... → Valorite).

The bribery mechanics:

- The player offers gold (the bribe amount) to the vendor.
- The vendor's `GreedLevel` increases per bribe; the bribe cost goes up.
- After a "Guild scrutiny" timeout, the vendor stops accepting bribes.
- Higher-level BODs require higher bribes.

The bribery gump is the same as the BOD offer gump but with a "Bribe" option. The engine validates that the BOD is "empty" (not yet filled) before allowing the bribe.

## Era-Gated Profession Scope

The active `BulkOrderSystem` gates Smith through `Core.UOR`, Tailor through `Core.LBR`, and Alchemy, Inscription, Tinkering, Cooking, Fletching, and Carpentry through `Core.TOL`. Treat this as repository implementation evidence only; use current official sources for publish chronology and player-facing rules.

Inspect the configured repository's current BOD type registrations, craft
systems, reward calculators, generated schemas, and reachability before stating
which crafts are supported. Enum members or placeholders alone do not prove an
active BOD world.

Current focused tests live under `Projects/UOContent.Tests/Tests/Engines/BulkOrders/` and include BOD bribery, BOD integration, reward construction, ledger/cooldown, and profession-scope behavior. Re-read test names in the active branch instead of relying on historical `MondainsLegacy*` names.

## Generated Persistence

The BOD engine now uses generated serialization and migration schemas for BOD books, BOB entries/filters, the bulk-order ledger, `SmallBOD`, and profession-specific BOD subclasses. When adding fields or new persistent BOD types:

- preserve existing field indexes and generated migration versions;
- add the matching schema under `Projects/UOContent/Migrations/`;
- include legacy/default round-trip coverage for the changed persistent type;
- keep runtime-only quote, target, gump, and vendor state out of serialized entity payloads unless an explicit schema contract owns it.

## BOD Rewards

The reward list is in `Projects/UOContent/Engines/Bulk Orders/Rewards.cs`. The major reward categories:

- **Colored Anvil** (Smith): 8 special hues for the smithing anvil.
- **Mining Gloves** (Smith): 8 special hues.
- **Runic Hammer / Runic Sewing Kit** (Smith/Tailor): a tool with 100 charges, used to craft items with the matching material.
- **Power Scroll** (rare Smith BOD reward): 5-point stat bonus.
- **Shoes** (large Tailor BOD): the "Shoe Set" themed items.
- **Decorative rewards**: statues, paintings, etc.

The reward is rolled by the `BODRewardCalculator` (in `Rewards.cs`). The probability is per-reward-tier and per-craft.

## BOD Vendors

The BOD vendors are NPC `BaseCreature` subclasses that hold a `BODVendor` (or similar) component. The vendor's context menu offers:

- `Get BOD`: roll a new BOD.
- `Combine BODs`: combine small BODs into large BODs (for `LargeBOD` enablement).
- `Turn In BOD`: validate and reward the player's BOD.
- `Bribe` (Publish 74+): upgrade the BOD.

The vendors are placed in the world at fixed coordinates (the per-craft guild halls and shops). The `Distribution/Data/Spawns/<era>/<facet>/<region>.json` files include the BOD vendor spawns.

## Common Pitfalls

1. **Forgetting `[Constructible]` on a custom `BaseBOD` subclass.** A BOD class without `[Constructible]` cannot be instantiated by the BOD vendor's roll; the BOD silently fails to be created.
2. **Setting `Material` to a value that the `CraftResource` does not map to.** The `BulkMaterialType` enum is the only valid value; using a non-existent value is a load error.
3. **Not validating the `Exceptional` flag in the turn-in.** A BOD with `RequireExceptional = true` should reject non-Exceptional items. Skipping the check lets players turn in any item.
4. **Setting the BOD's `AmountMax` lower than the actual crafted count.** The BOD's `AmountMax` is the count; the player's inventory count must be `>= AmountMax`. Using a wrong value is a silent misfill.
5. **Forgetting the ML-era turn-in cooldown.** Pre-ML shards must not have the cooldown; ML shards must have it (per `MondainsLegacyRewardServiceRuntimeTests`).
6. **Not using `BODRewardCalculator` for the reward roll.** Hardcoded reward selection bypasses the per-craft probability table and the `Rewards.cs` configuration.
7. **Allowing the bribery system on a pre-Publish-74 BOD world.** The bribery system is a Publish-74 feature; gating it requires the appropriate era flag.
8. **Setting the BOB's `MaxEntries` to a value that the per-character storage cannot handle.** The default 500 is high; the save/load performance is linear in the entry count.
9. **Forgetting the BOB filter's `BOBFilterType` configuration.** The filter is per-craft and per-item-type; without a configured filter, the BOB shows all BODs in the gump.
10. **Wiring the BOD's `Graphic` field to a wrong `ItemID`.** The `Graphic` is the client's representation; an incorrect value shows the wrong item in the BOD gump.

## Common Recipes

### Adding a New BOD Type (Smith)

```csharp
public class MySmithBOD : SmallSmithBOD
{
    [Constructible]
    public MySmithBOD() : base()
    {
        Type = typeof(MySword);
        Graphic = 0x13FF;  // Sword
        AmountMax = 10;
        RequireExceptional = false;
        Material = BulkMaterialType.Iron;
    }
}
```

### Adding a BOD Reward

```csharp
public class MyBODReward : BaseRewardItem
{
    [Constructible]
    public MyBODReward() : base(0x1234)
    {
        Hue = 0x501;
        Weight = 1.0;
    }
}
```

Register in `Rewards.cs` reward table for the matching craft system.

### Configuring a BOB Filter

```csharp
var filter = new BOBFilter(BOBFilterType.Smith);
filter.Smithing = true;
filter.Type = typeof(Katana);

book.Filter = filter;
```

### Wiring a BOD Vendor

```csharp
public class MySmithBODVendor : BaseCreature
{
    [Constructible]
    public MySmithBODVendor() : base(AIType.AI_Vendor, FightMode.None)
    {
        Body = 0x190;  // Male human
        ...
        // BOD offers via context menu
    }
}
```

### Enforcing the ML Turn-In Cooldown

```csharp
// In BaseBOD.OnTurnIn
if (Core.ML && m_LastTurnIn.AddHours(6) > DateTime.UtcNow)
{
    player.SendMessage("You must wait before turning in another BOD.");
    return false;
}
m_LastTurnIn = DateTime.UtcNow;
```

## Verification Checklist

- [ ] `dotnet build` succeeds without new warnings.
- [ ] New BOD type: `[Constructible]` is present, `Type` is a valid `Item` subclass, `Graphic` matches the item's `ItemID`, `Material` is a valid `BulkMaterialType` value.
- [ ] BOD turn-in: items are validated against `Type`, `Material`, and `RequireExceptional`.
- [ ] Large BOD: the small BODs in the player's backpack are combined into the large BOD; the small BODs are consumed.
- [ ] BOB: the BOB stores the BODs, the filter is applied, the gump shows the right entries.
- [ ] BOD reward: `BODRewardCalculator` is used to select the reward, the reward is dropped into the player's backpack.
- [ ] Bribery: the BOD is upgraded (quantity/quality/material) on bribe, the gold is consumed.
- [ ] ML turn-in cooldown: enforced on `Core.ML` shards, not enforced on pre-ML shards.
- [ ] BOD vendor: the context menu offers `Get BOD`, `Combine BODs`, `Turn In BOD`, `Bribe`.
- [ ] Focused BOD tests under `Projects/UOContent.Tests/Tests/Engines/BulkOrders/` pass for the changed path.
- [ ] Generated schema and migration tests cover every persistent BOD/BOB/ledger field change.
- [ ] Per-craft BOD scope matches the active `BulkOrderSystem` era gates and does not convert repository gates into official gameplay claims.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related Skills

- `uo-crafting-recipes-resources` - the crafting system that produces the items the BOD requires.
- `uo-items-foundation` - the `Item` model used for BODs and BOD rewards.
- `uo-skills-stats-races` - the skill check for BOD pickup and the BOB filter.
- `uo-combat-pipeline` - the combat system that consumes the BOD rewards (e.g. `Hammer of Hephaestus` equip bonus).
- `uo-loot-generation-artifacts` - the loot table for the BOD reward pool.
- `uo-quests-engine-ml` - the ML quest system that can reward BODs.
- `uo-world-facets-regions` - the regional placement of the BOD vendors.
- `modernuo-content-patterns` - canonical templates for new BOD types and rewards.
- `modernuo-era-expansion` - per-era BOD scope (Smith/Tailor for pre-Publish-95).
- `www.uoguide.com/Bulk_Order_Deed` is a community discovery reference for
  publish and mechanic leads, not official documentation.
- `uo.com/wiki/ultima-online-wiki/gameplay/crafting/bulk-orders/` (offline reference) - the official BOD turn-in values and reward costs.
- `docs/mondains-legacy-content-matrix.md:78` (offline reference) - the ML-era BOD regression coverage and the per-craft scope.
