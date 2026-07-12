# Range Verification Chain

Read this reference when translating a tile/radius specification or auditing a
custom `Get*InBounds` path.

## Standard centered range

The usual range conversion is equivalent to:

```csharp
var radius = Math.Max(0, range);
var edge = radius * 2 + 1;
var bounds = new Rectangle2D(x - radius, y - radius, edge, edge);
```

Verify this in the current `Map.MobileEnumerator.cs` or item/client equivalent.
Do not assume all overloads share it.

`Rectangle2D` normally stores `end = start + width` and tests
`start <= coordinate && coordinate < end`. Therefore a width of `2N+1` selects
integer coordinates from `x-N` through `x+N`, inclusive, while the internal end
coordinate remains exclusive.

| Range | Dimensions | Coordinates selected | Tile count |
|---:|---:|---|---:|
| 0 | `1x1` | source only | 1 |
| 1 | `3x3` | one tile outward | 9 |
| 2 | `5x5` | two tiles outward | 25 |
| 3 | `7x7` | three tiles outward | 49 |
| N | `(2N+1)^2` | N outward in each axis | `(2N+1)^2` |

This is Chebyshev distance: `(x+N, y+N)` is inside. Source exclusion is a later
gameplay filter, not part of the range conversion.

## `makeBoundsInclusive`

Some bounds enumerators accept `makeBoundsInclusive` and expand the supplied edge
rectangle. This convention is used for callers that describe coordinate edges
rather than centered tile radii, such as some client-view rectangles. If true,
derive the actual rectangle from that constructor; do not reuse the standard
centered formula or assume the source remains centered.

## Translating source wording

- **N-tile radius:** normally range argument `N` under ModernUO's Chebyshev
  convention.
- **N-tile diameter/width:** derive the radius from the stated width and verify
  odd/even behavior.
- **N-tile ring:** enumerate the outer bounds and filter/subtract the inner range.
- **Rectangle:** preserve explicit start/end/inclusivity rather than converting to
  a radius without reason.

When prose and a numerical example disagree, state the conflict and use the
approved stronger source/era decision. Do not silently reinterpret radius as
diameter.

## Worked check

If a spell calls `GetMobilesInRange(3 + focus)`:

- focus 0 -> range 3 -> `7x7` centered box;
- focus 1 -> range 4 -> `9x9`;
- focus 6 -> range 9 -> `19x19`.

Then inspect the loop separately for caster exclusion, harmful/party filters, LOS,
Z, map, alive state, and era gates.

## Boundary test table

For source `(100,100)` and range `3`, assert:

- `(100,100)` spatially included;
- `(103,100)` and `(103,103)` included;
- `(104,100)` and `(104,104)` excluded;
- source/gameplay exclusions tested separately;
- custom `makeBoundsInclusive`, ring, and Z behavior tested only when used.

Current source anchors are the map enumerators and
`Projects/Server/Geometry/Rectangle2D.cs`; locate them by symbol rather than stale
line numbers.
