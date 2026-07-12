---
name: modernuo-regions
description: >
  Use when creating custom regions, dynamic item-controlled areas, dungeon sub-zones, travel restrictions, housing blocks, spawn control, or any spatial gameplay rule. Covers Region, BaseRegion, GuardedRegion, DungeonRegion, HouseRegion, and CheckTravel.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, regions, facets, spatial-rules, travel]
    related_skills:
      - modernuo-code-audit
      - modernuo-performance-hot-paths
      - modernuo-content-patterns
      - modernuo-serialization
      - modernuo-timers
      - modernuo-lifecycle-cleanup
      - modernuo-era-expansion
      - uo-world-facets-regions
      - modernuo-spatial-range-geometry
---

# ModernUO Regions

## When to Use
- Creating a custom region (dungeon zone, boss arena, restricted area)
- Creating a dynamic region tied to an item (chest effect zone, spawn area)
- Adding travel spell restrictions, housing blocks, or spawn control
- Working with `Region`, `BaseRegion`, `GuardedRegion`, `DungeonRegion`, `HouseRegion`
- Overriding `CheckTravel`, `AllowHousing`, `OnEnter`, `OnBeginSpellCast`, etc.
- Modifying region JSON or `RegionJsonRegistration`

## Key Rules

1. **Inherit from the right base** — `BaseRegion` for general, `DungeonRegion` for dungeons, `GuardedRegion` for towns, `NoTravelSpellsAllowedRegion` for no-travel dungeons
2. **Dynamic regions must Register/Unregister** — call `Register()` after creation, `Unregister()` before recreation or deletion
3. **Use `Region.Find(location, map)` as parent** for dynamic child regions — this inherits the existing region's behavior
4. **Defer registration in `[AfterDeserialization]`** — use `Timer.StartTimer(TimeSpan.Zero, UpdateRegion)` since map/parents may not be loaded yet
5. **Always override `AllowHousing` returning false** if your region should block housing
6. **Staff bypass** — travel/spell checks should allow `AccessLevel > Player`
7. **Virtual hooks delegate to Parent** — you only need to override what you change

## Choosing a Base Class

| You Need | Inherit From |
|---|---|
| Custom overworld area | `BaseRegion` |
| Dungeon area (dark, no housing) | `DungeonRegion` |
| Dungeon + no travel spells | `NoTravelSpellsAllowedRegion` |
| Town with guards | `GuardedRegion` or `TownRegion` |
| No housing only | `NoHousingRegion` |
| Item-controlled dynamic area | `BaseRegion` (parent = `Region.Find(...)`) |

## Quick Patterns

### Static Region (JSON-Defined)

Add to `Distribution/Data/regions.json`:
```json
{
  "$type": "NoTravelSpellsAllowedRegion",
  "Name": "My Dungeon",
  "Map": "Felucca",
  "Parent": { "Name": "Felucca", "Map": "Felucca" },
  "Area": [{ "x1": 100, "y1": 200, "x2": 300, "y2": 400 }],
  "GoLocation": { "x": 150, "y": 250, "z": 0 },
  "Music": "Dungeon9"
}
```

Register the type (if new) in `RegionJsonRegistration.Configure()`:
```csharp
RegionJsonSerializer.Register<MyCustomRegion>();
```

### Custom Region Class

```csharp
public class MyCustomRegion : BaseRegion
{
    public MyCustomRegion(string name, Map map, Region parent, params Rectangle3D[] area)
        : base(name, map, parent, area)
    {
    }

    public override bool AllowHousing(Mobile from, Point3D p) => false;

    public override bool CheckTravel(
        Mobile m, Point3D newLocation, TravelCheckType travelType, out TextDefinition message)
    {
        message = null;
        return m.AccessLevel > AccessLevel.Player;
    }
}
```

### Dynamic Item-Tracked Region

Full pattern for an item that creates a region around itself:

```csharp
public partial class MySpecialItem : Item
{
    private MyItemRegion _region;

    public void UpdateRegion()
    {
        _region?.Unregister();

        if (!Deleted && Map != Map.Internal)
        {
            _region = new MyItemRegion(this);
            _region.Register();
        }
    }

    public override void OnLocationChange(Point3D oldLoc)
    {
        base.OnLocationChange(oldLoc);
        UpdateRegion();
    }

    public override void OnMapChange()
    {
        base.OnMapChange();
        UpdateRegion();
    }

    public override void OnAfterDelete()
    {
        base.OnAfterDelete();
        UpdateRegion(); // Unregisters because Deleted == true
    }

    [AfterDeserialization(false)]
    private void AfterDeserialization()
    {
        Timer.StartTimer(TimeSpan.Zero, UpdateRegion); // Defer to next tick
    }
}

public class MyItemRegion : BaseRegion
{
    public MySpecialItem Item { get; }

    public MyItemRegion(MySpecialItem item)
        : base(null, item.Map,
            Region.Find(item.Location, item.Map),  // Parent = existing region
            new Rectangle2D(item.X - 5, item.Y - 5, 11, 11))
    {
        Item = item;
    }

    public override void OnEnter(Mobile m)
    {
        base.OnEnter(m);
        // Custom enter logic
    }
}
```

### Child Region Inside a Dungeon

When you want effects that don't break dungeon rules (inherits lighting, no housing, etc.):

```csharp
public class BossArenaRegion : BaseRegion
{
    public BossArenaRegion(Item source)
        : base(null, source.Map,
            Region.Find(source.Location, source.Map),  // Parent = dungeon
            new Rectangle2D(source.X - 10, source.Y - 10, 21, 21))
    {
    }

    // Inherits DungeonRegion behavior from parent automatically
    // Only add what's different:

    public override bool CheckTravel(
        Mobile m, Point3D newLocation, TravelCheckType travelType, out TextDefinition message)
    {
        message = null;
        return m.AccessLevel > AccessLevel.Player; // No escape during boss fight
    }

    public override void SpellDamageScalar(Mobile caster, Mobile target, ref double damage)
    {
        base.SpellDamageScalar(caster, target, ref damage);
        damage *= 1.25; // Bonus damage in arena
    }
}
```

### Blocking Specific Spells

```csharp
public override bool OnBeginSpellCast(Mobile m, ISpell s)
{
    if (m.AccessLevel == AccessLevel.Player && s is MarkSpell)
    {
        m.SendLocalizedMessage(501802); // Thy spell doth not appear to work...
        return false;
    }
    return base.OnBeginSpellCast(m, s);
}
```

## Region Hierarchy & IsPartOf

Virtual hooks delegate to `Parent` — child regions inherit all parent behavior:

```csharp
// A child of DungeonRegion automatically has:
// - Dungeon lighting
// - No housing
// - YoungProtected = false

// Check hierarchy:
region.IsPartOf<DungeonRegion>()   // true if this or any ancestor is DungeonRegion
region.GetRegion<GuardedRegion>()  // returns first GuardedRegion in ancestor chain
```

## Existing Region Types Reference

| Type | Key Behavior |
|---|---|
| `BaseRegion` | CheckTravel, spawn weights, RuneName |
| `GuardedRegion` | NPC guards, no housing, town spell restrictions |
| `TownRegion` | Guard behavior + Entrance property |
| `DungeonRegion` | Dungeon lighting, no housing, young not protected |
| `NoTravelSpellsAllowedRegion` | Blocks all travel spells (extends DungeonRegion) |
| `NoHousingRegion` | Blocks housing placement |
| `NoHousingGuardedRegion` | Guards + housing block |
| `GreenAcresRegion` | No housing, no travel, no Mark |
| `JailRegion` | Full lockdown: no skills, spells, combat, travel |
| `HouseRegion` | Dynamic per-house; access, bans, lockdowns |
| `MondainRegion` | Mondain's Legacy dungeon (no travel) |

## Anti-Patterns

- **Registering regions in deserialization constructors**: Map/parents may not be loaded — use `[AfterDeserialization]` with `Timer.StartTimer(TimeSpan.Zero, ...)`
- **Forgetting `Unregister()` on item delete**: Ghost region stays on map — always unregister in `OnAfterDelete()`
- **Not using parent for dynamic regions**: Loses inherited behavior (lighting, guards, etc.) — pass `Region.Find(location, map)` as parent
- **Using `Region.Find(string, Map)` in hot paths**: Linear O(n) scan — use `Region.Find(Point3D, Map)` (sector-indexed)
- **Overriding a hook without calling `base`**: Breaks parent delegation chain — always call `base.Method()` unless intentionally blocking

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/regions.md` — Complete region system documentation
- `dev-docs/timers.md` — Timer system (for deferred registration)
- `plugins/modernuo/skills/modernuo-content-patterns/SKILL.md` — Item/Mobile lifecycle (OnAfterDelete, AfterDeserialization)
- `plugins/modernuo/skills/modernuo-serialization/SKILL.md` — Serialization and AfterDeserialization hooks
