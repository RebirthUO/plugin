---
name: "uo-items-foundation"
description: "Use when working with the UO item entity model in ModernUO/RebirthUO servers - Item base class, Constructible constructors, GetProperties OPL output, LootType, Decay, and the standard item base hierarchy (BaseWeapon/BaseArmor/BaseClothing/BaseJewel/BaseContainer). Use before adding a new item, debugging item persistence, or tracing why an item behaves the way it does in-world."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Items Foundation

## Overview

The Ultima Online item system in ModernUO/RebirthUO is a layered entity model: `Item` is the persistent base class in `Projects/Server`, and a set of typed `Base*` classes in `Projects/UOContent` extend it with semantic and rule behavior. Every item that exists in the world, a player's backpack, a corpse, a container chain, or a vendor is an `Item` (or one of its derivatives) on a `Map` and inside a `World` registry.

This skill covers the foundation: the `Item` lifecycle, construction patterns, persistence, display (OPL/GetProperties), and the canonical base classes used by every gameplay system. It is the prerequisite for `uo-aos-item-properties` (which layers magical attributes on top of these base classes) and `uo-crafting-recipes-resources` (which produces instances of these classes through `CraftItem`).

The reference implementation is `Projects/Server/Items/Item.cs` and the base classes live under `Projects/UOContent/Items/`.

## When to Use

- Adding a new item type (weapon, armor, container, food, reagent, spell scroll, decoration, quest token).
- Investigating why an item persists, decays, drops, or moves unexpectedly.
- Reading or writing an item's `GetProperties(IPropertyList list)` OPL output (tooltips).
- Distinguishing engine-level `Item` behavior from content-level `Base*` behavior.
- Tracing item lifetime: spawn, add, equip, transfer, decay, delete.

Don't use for:

- Pure AoS attribute semantics (use `uo-aos-item-properties`).
- Crafting/recipe/resource plumbing (use `uo-crafting-recipes-resources`).
- Spell or skill implementations that only consume items.

## Item Entity Anatomy

`Item` is declared as `public partial class Item` in `Projects/Server/Items/Item.cs:195`. It implements `IHued, IComparable<Item>, ISpawnable, IObjectPropertyListEntity, IValueLinkListNode<Item>`. Partial is mandatory - the serialization source generator emits the second half of the class.

Core fields every item owns:

| Field | Purpose | Reference |
|---|---|---|
| `Serial` | Unique world identifier assigned via `World.NewItem` | `Item.cs:222-236` |
| `m_ItemID` | Tile/graphic id (art) | `Item.cs:212` |
| `m_Hue` | Color (0 = default; `0x4EA` = quest hue) | `Item.cs:211`, `Item.cs:199` |
| `m_Amount` | Stack size (1 for non-stackables) | `Item.cs:204` |
| `m_Layer` | Equipment slot when on a Mobile | `Item.cs:213` |
| `m_Weight` | Stone weight (double) | `Item.cs` around line 448 |
| `m_LootType` | `Regular` / `Newbied` / `Blessed` / `Cursed` | `Item.cs:80-101, 216` |
| `m_Location` / `m_Map` / `m_Parent` | World position, facet, owning Mobile/Item | `Item.cs:215-218` |
| `TempFlags` / `SavedFlags` | Bit flags in `CompactInfo` (locked-down, secure, custom bits) | `Item.cs:240-270` |

`CompactInfo` is the lazy bag for "expensive to default" state. Accessors go through `AcquireCompactInfo()` and `VerifyCompactInfo()` to avoid paying allocation cost for items that have no extra state.

## Construction Pattern

Every concrete item class uses `partial class` plus the serialization generator and a `[Constructible]` constructor. The bare minimum from `dev-docs/content-patterns.md:18-37`:

```csharp
using ModernUO.Serialization;

namespace Server.Items;

[SerializationGenerator(0)]
public partial class SimpleItem : Item
{
    [Constructible]
    public SimpleItem() : base(0x1234)  // itemID from UO art
    {
        Weight = 1.0;
    }

    public override string DefaultName => "a simple item";
    // OR: public override int LabelNumber => 1234567;  // cliloc number
}
```

Key rules:

- Class must be `partial`. The generator emits the `Serialize`/`Deserialize` shim.
- Constructor takes `base(int itemID)` and sets the persistent defaults in the body. Do not put behavior in the constructor; the engine will set everything up before field initializers fire.
- `[Constructible]` is mandatory for the item to be reachable from `[Constructible]` reflection paths (admin `[add` command, `CraftItem.OnCraft`, generation scripts).
- For typed state (charges, owner, timer-bound resources), use `[SerializableField(N)]` plus a `_camelCase` private field. See `MagicLantern` in `dev-docs/content-patterns.md:39-115`.
- Timers and references must be cleared in `OnAfterDelete()` to honor the single-threaded engine model (see `CLAUDE.md:5-7,18-19`).

## Base Class Hierarchy

The content layer under `Projects/UOContent/Items/` builds the gameplay-meaningful hierarchy on top of `Item`:

| Base class | Use for | File |
|---|---|---|
| `Item` | Generic items, decoration, tokens | `Projects/Server/Items/Item.cs:195` |
| `BaseWeapon` | Melee weapons (and ranged via `BaseRanged`) | `Projects/UOContent/Items/Weapons/BaseWeapon.cs` |
| `BaseRanged` | Bows, crossbows (extends `BaseWeapon`) | `Projects/UOContent/Items/Weapons/Ranged/BaseRanged.cs` |
| `BaseArmor` | Armor pieces | `Projects/UOContent/Items/Armor/BaseArmor.cs` |
| `BaseShield` | Shields (extends `BaseArmor`) | `Projects/UOContent/Items/Armor/BaseShield.cs` |
| `BaseClothing` | Wearable clothing | `Projects/UOContent/Items/Clothing/BaseClothing.cs` |
| `BaseJewel` | Rings, bracelets, necklaces | `Projects/UOContent/Items/Jewels/BaseJewel.cs` |
| `BaseContainer` | Bags, boxes, chests (parent chain) | `Projects/UOContent/Items/Containers/BaseContainer.cs` |
| `BaseQuiver` | Quivers (extends `BaseContainer`, used by ranged) | `Projects/UOContent/Items/Quivers/BaseQuiver.cs` |
| `BasePotion` | Potions, including ML Alchemy variants | `Projects/UOContent/Items/Potions/BasePotion.cs` |
| `BaseReagent` | Spell reagents (BlackPearl, Bloodmoss, etc.) | `Projects/UOContent/Items/Reagents/BaseReagent.cs` |
| `BaseFood` / `Food` | Edible items | `Projects/UOContent/Items/Food.cs` |
| `SpellScroll` | Scrolls with `Spell` payload | `Projects/UOContent/Items/Skill Items/Magical/SpellScroll.cs` |

Armor, clothing, and jewelry carry the cosmetic/AoS property surface. Weapons and armor add the typed property containers (`Attributes`, `WeaponAttributes`, `ArmorAttributes`, `SkillBonuses`, `ElementAttributes`) covered by `uo-aos-item-properties`.

## Display: GetProperties and IPropertyList

Every visible item's tooltip is built by `GetProperties(IPropertyList list)`. The engine calls it whenever a client opens the tooltip window, after a state change, or when a `Delta(ItemDelta.Properties)` is queued. Default base behavior (in `Item.cs`) emits the name/label, hue, weight, amount, and the equipped layer. Subclasses call `base.GetProperties(list)` then append their own rows.

`IPropertyList` is the engine contract; it accepts:

- `list.Add(int clilocNumber)` - cliloc row with no argument.
- `list.Add(int clilocNumber, string? arguments)` - cliloc row with args (pass `null` for no-arg).
- `list.Add(int clilocNumber, int value)` - shorthand for numeric arg.
- `list.Add(string text)` - bare string (only for fallback strings like `"No-Trade"`).
- Interpolated `$"..."` string handler overloads - allocation-free when used directly in a literal.

**Rule from `CLAUDE.md:14`**: PropertyList string literals must be holes. `list.Add($"{name}\t{value}")` is correct; `list.Add($"name\t{value}")` is not. The handler treats bare text as delimiters and `{}` holes as arguments. Only `\t` should be a bare literal.

For properties that have no known cliloc in this codebase, use the planned `ItemPropertyDisplay` helper (`docs/superpowers/plans/2026-06-02-item-properties-completion.md:225-232`):

```csharp
ItemPropertyDisplay.AddName(list, "No-Trade");
ItemPropertyDisplay.AddValue(list, "Charges", _charges);
ItemPropertyDisplay.AddPercent(list, "Hit Curse", 25);
```

Invalidation: after changing a property that should re-render, call `InvalidateProperties()`. Property changes typed through `[InvalidateProperties]` and `[SerializedCommandProperty]` are auto-invalidated.

## LootType and Death Behavior

`LootType` (declared in `Item.cs:80-101`) is a `byte` enum:

| Value | Stealable | Lootable from corpse | Typical use |
|---|---:|---:|---|
| `Regular = 0` | Yes | Yes | Normal loot, monster drops, crafted gear |
| `Newbied = 1` | No | Only by murderers | Items flagged at creation that should not transfer to murderers; new-player handouts |
| `Blessed = 2` | No | Never | Quest items, reward items, sealed goods |
| `Cursed = 3` | Yes | Always | Cursed loot (rare; usually set on specific cursed items) |

`LootType` is the cheapest mechanic for "this stays with the player" or "this stays attached to the corpse". For full no-drop/no-trade/shard-bound rules, content code branches on `LootType` plus the move/equip/transfer hooks in `BaseContainer` and `BaseArmor`. The new `No-Drop / No-Trade / Shard Bound` transfer flags tracked in the item-properties plan are content-level additions that ride on top of this enum.

The `DeathMoveResult` enum (`Item.cs:59-75`) tells the engine what to do with an equipped item on death: move it to the corpse, keep it on the body, or return it to the backpack.

## Decay, Visibility, Movement

Decay is engine-managed: a `Decays` flag plus `UpdateDecayRegistration()` in `Item.cs` around line 525. Items that should never decay (player-loot, quest items, blessed containers) leave `Decays = false`. Corpse decay is special-cased to player-attributable corpse lifetime rather than the standard timer.

`Visible` (set via `ImplFlag.Visible`) controls whether clients render the item. Hidden items still exist in the world for targeting, but the client receives a remove-entity packet; this is the standard "GM hides object" path. `Movable` is the equivalent for pick-up - locked-down and secured items in a house flip this to `false` via `SetFlag(ImplFlag.Movable, false)`.

`HandlesOnMovement` is a virtual flag (`Item.cs:394`) - if true, the engine calls `OnMovement(...)` for movement-driven behaviors (e.g. stepped-on traps). Default is `false` to avoid the per-tile cost.

## Resistances and Base Properties

`Item.cs:566-570` exposes five resistance hooks consumed by `AOS.Damage`:

```csharp
public virtual int PhysicalResistance { get; }
public virtual int FireResistance { get; }
public virtual int ColdResistance { get; }
public virtual int PoisonResistance { get; }
public virtual int EnergyResistance { get; }
```

`BaseArmor` overrides these with the material/armor bonuses. `AOS.Damage` reads them when applying AoS damage splits, and `AosAttributes.GetValue(m, AosAttribute.DefendChance)` etc. layer additional percentages on top. This is the bridge into the AoS property system covered by `uo-aos-item-properties`.

## Common Patterns and Recipes

### Quest/Token Item with Charges

From `dev-docs/content-patterns.md:39-115`, a typed charge item combines `[SerializableField]`, an invalidation hook, and a timer. `OnAfterDelete` cancels the timer. `OnDoubleClick` is the action entry point and must always validate the parent (e.g. `IsChildOf(from.Backpack)`) before mutating state.

### Stackable Resource

Reagents and arrows stack. Set `Stackable = true` and increment `Amount` for merges. `Item.cs:305-331` documents `Stackable` semantics. The `m_Amount` setter validates the new value is within `ItemData.MaxStack`.

### Equippable Item

Set `Layer` in the constructor (e.g. `Layer.OneHanded` for a weapon, `Layer.InnerTorso` for chest armor). Override `CanEquip(Mobile from)` to enforce class/race/era gates. `OnEquip` and `OnUnequip` are the symmetric hooks for adding/removing stat mods, attributes, or skill mods.

### Loot Drop Helper

For monster loot generation, do not instantiate items directly. Use the type-based loot generation in `Projects/UOContent/Misc/Loot.cs` and `TypeRandom` to pick an item type, then `Construct()` it via the `[Constructible]` reflection path. For named/artifact drops, the artifact lists in `Projects/UOContent/Items/Artifacts/` are the canonical source.

## Hot Path and Serialization Reminders

From `CLAUDE.md:9`:

- `Item` and all subclasses are `partial class`.
- New persistent fields use `[SerializableField(N)]` plus a private field with `[EncodedInt]`, `[DeltaSerializable]`, or similar generator attributes.
- `TimerExecutionToken` must NOT have `[SerializableField]`. It is rebuilt by `[AfterDeserialization]`.
- Use the MigrationGenerator pattern: bump the version number on `SerializationGenerator(N)` and add `MigrateFrom(V(N-1))` rather than touching the legacy `Deserialize` method.

Hot-path rules (also from `CLAUDE.md:1-7`):

- Single-threaded engine. No `Task.Run`, no `new Thread()`, no `ConcurrentDictionary`, no `lock`.
- Use `map.GetItemsInRange<T>(loc, range)` for spatial lookups, never `World.Items` iteration.
- `STArrayPool<T>.Shared` and `PooledRefList<T>` for hot paths.
- `ValueStringBuilder` for string building inside OPL or combat message paths.

## Pitfalls

1. **Calling `base.GetProperties` last.** Append-only - call `base.GetProperties(list)` first, then add subclass rows. The engine expects the order: name, then standard rows, then subclass-specific rows, then any negative-property rows.
2. **Forgetting `[Constructible]`.** A `[SerializationGenerator]` class without `[Constructible]` cannot be created by admin commands, `CraftItem.OnCraft`, or scripts that use the generic factory. The build will not fail, but the item will be unspawnable in those paths.
3. **Using `m_` prefix on new private fields.** Use `_camelCase`. Legacy `m_` is allowed only on engine code that pre-dates the rule (`CLAUDE.md:12`).
4. **Storing `Mobile` references with `[SerializableField]` without `[DeltaSerializable]` consideration.** Mobile references can be deleted; the engine does not auto-null them. Clear refs in `OnAfterDelete` and validate before use.
5. **Setting `Layer` after `Movable` without testing the equip/unequip path.** Some items look equippable but are not - check `OnEquip`/`OnUnequip` and validate the parent chain.
6. **Assuming LootType alone prevents transfer.** `LootType.Blessed` blocks stealing and corpse looting but does not block player-to-player trading or trade gumps. Use the new `No-Trade / Shard Bound` content flags when they land for full transfer control.
7. **Returning `string` from `DefaultName` without overriding `LabelNumber`.** If you set a `DefaultName` constant, you bypass the cliloc lookup. If you want a localized cliloc label, override `LabelNumber` instead.

## Verification Checklist

- [ ] `dotnet build` from repo root completes with no new warnings.
- [ ] `[Constructible]` is present on every concrete item class.
- [ ] Class is `partial` and the `[SerializationGenerator(N)]` version matches the field count + 1.
- [ ] `[SerializableField]` indices are dense and start at 0.
- [ ] `OnAfterDelete()` cancels any `TimerExecutionToken` and nulls any `Mobile`/`Item` references.
- [ ] `GetProperties` calls `base.GetProperties(list)` first.
- [ ] PropertyList string literals use `$"{}"` hole syntax, not bare concatenation.
- [ ] No use of `World.Items`/`World.Mobiles` iteration; spatial queries used instead.
- [ ] New item appears in a tool (`[add item` or `i Dor 0x1234`) without throwing.

## Related Skills

- `uo-aos-item-properties` - layer magical properties on the base classes covered here.
- `uo-crafting-recipes-resources` - produce instances of these classes via `CraftItem`.
- `modernuo-content-patterns` - canonical templates for new content (Items, Mobiles, Spells, Skills).
- `modernuo-serialization` - serialization generator, migration pattern, `[Constructible]` rules.
- `modernuo-property-lists` - IPropertyList mechanics, OPL strings, cliloc references.
- `modernuo-era-expansion` - gate `Core.AOS`/`Core.SE`/`Core.ML` checks correctly.

## Support Files

- `references/analyzing-modernuo-subsystems.md` - reading recipe for turning a ModernUO/RebirthUO subsystem into a class-level Hermes skill. Use it before analyzing Spells, Skills, AI, Combat, Crafting, or any other UO subsystem so the work follows the same citation discipline and trigger shape used here.
- `scripts/validate_cromesdk_skill.py` - validator for CromeSDK-marked SKILL.md frontmatter. Run it on every personal CromeSDK skill before declaring the work done.
