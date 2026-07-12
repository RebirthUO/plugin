# Dynamic and JSON Region Patterns

Read this reference when selecting a region base, JSON registration, parent, or
dynamic lifetime. Confirm current constructor and schema signatures in the repo.

## Base selection

| Need | Typical base |
|---|---|
| General custom area | `BaseRegion` |
| Dungeon defaults such as lighting/no housing | `DungeonRegion` |
| Dungeon with travel blocked | existing `NoTravelSpellsAllowedRegion` |
| Guarded town | `GuardedRegion` or `TownRegion` |
| Housing blocked only | existing `NoHousingRegion` |
| Item/controller-owned area | `BaseRegion` with current spatial parent |

Prefer an existing specialized type over reimplementing its rules. Child region
hooks normally delegate to `Parent`; preserve that chain unless intentionally
overriding the inherited behavior.

## Static JSON region

A static region entry generally provides type, name, map, parent, area, go
location, and optional music/settings. New types also require registration with
the current `RegionJsonSerializer`/`RegionJsonRegistration` mechanism. Validate
the active `Distribution/Data/regions.json` schema instead of copying historical
property names blindly.

## Dynamic item-owned region

Centralize all replacement in one method:

```csharp
private void UpdateRegion()
{
    _region?.Unregister();
    _region = null;

    if (Deleted || Map == null || Map == Map.Internal)
    {
        return;
    }

    _region = new MyItemRegion(this);
    _region.Register();
}
```

Call the same method after location/map changes and on deletion so the old region
is always unregistered before a replacement. Follow the owning hierarchy's
base-call order.

```csharp
private sealed class MyItemRegion : BaseRegion
{
    public MyItemRegion(MySpecialItem item)
        : base(
            null,
            item.Map,
            Region.Find(item.Location, item.Map),
            new Rectangle2D(item.X - 5, item.Y - 5, 11, 11))
    {
    }
}
```

Using the current region as parent preserves dungeon, guard, housing, lighting,
and other inherited rules. An intentionally parentless region needs an explicit
reason and tests for every rule it replaces.

## After-load restoration

Use `[AfterDeserialization(false)]` when registration requires loaded maps,
regions, or other world entities. Some established types defer one more game-loop
tick with a zero-delay timer; use that only when current code demonstrates the
additional dependency. Ensure construction and after-load paths cannot both
register the same region.

## Travel/housing hooks

- Keep established staff bypass behavior for player restrictions.
- Call the base/parent hook unless the new region intentionally blocks it.
- Test entry, exit, and destination semantics separately for travel checks.
- `AllowHousing` should be explicit when the region is intended to block housing.

## Verification matrix

- Inside, edge, and outside coordinates on each map/Z rule.
- Parent rule inherited plus the one overridden rule.
- Location and map changes unregister old/register new once.
- Delete and disable leave no active region.
- Save/load creates exactly one valid region.
- Staff/player and pre-era/target-era behavior when applicable.
