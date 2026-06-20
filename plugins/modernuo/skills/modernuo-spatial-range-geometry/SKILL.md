---
name: "modernuo-spatial-range-geometry"
description: "Calculate exact in-game tile coverage for AoE and spatial queries in ModernUO (GetMobilesInRange, GetItemsInRange, GetClientsInRange, GetMobilesInBounds). Use whenever a spell, ability, quest, spawn rule, or gameplay mechanic uses a numeric range or radius, especially when matching a UO community spec (UOGuide, Stratics, UOAlive) that quotes things like 3 tile radius or 9 tile radius. Covers how the range argument maps to bounding box size, how Rectangle2D contains works (half-open), and the makeBoundsInclusive landmine."
metadata:
  author: "Crome696"
---

# ModernUO Spatial Range Geometry

## When this skill is needed

ANY time you (or another agent) is about to

- Change a numeric range or radius argument to GetMobilesInRange, GetItemsInRange, GetClientsInRange, GetMobilesInBounds
- Match a UO community spec value such as Stratics, UOGuide, or UOAlive wiki saying 3 tile radius, 9 tile radius, or 7 tile area
- Verify that a spell hits 3 tiles out actually means what you think it means
- Write or review an AoE ability, spell, spawn rule, or quest objective that uses range

Trigger keywords the agent should load on: radius, range, AoE, area of effect, tile, GetMobilesInRange, GetItemsInRange, GetMobilesInBounds, Spellweaving, Wildfire, Thunderstorm, Essence of Wind, Rectangle2D.

Do NOT trust a casual reading of tile radius equals N until you have walked the chain below end to end. Off by one errors in this layer are extremely common and silently shift gameplay.

## What range N actually means in ModernUO

In ModernUO, the range passed to a GetMobilesInRange, GetItemsInRange, or GetClientsInRange call is the Chebyshev radius in tiles (king move distance, diagonal counts as 1), counted from the caster tile outward, inclusive of the caster tile.

Concretely

- range 0 -> 1 by 1 box, 1 tile, source tile only
- range 1 -> 3 by 3 box, 9 tiles, source plus 1 tile out in every direction (8 neighbors)
- range 2 -> 5 by 5 box, 25 tiles, source plus 2 tiles out in every direction
- range 3 -> 7 by 7 box, 49 tiles, source plus 3 tiles out in every direction
- range N -> (2N+1) by (2N+1) box, (2N+1) squared tiles, source plus N tiles out in every direction

The caster or source itself is INSIDE the box. It is then typically filtered out by an explicit guard inside the spell or ability loop, something like `if (source == x) continue;`. That guard is a gameplay concern (do not damage yourself), not a spatial concern.

## The verification chain (always run this, in this order)

When you need to know what a range value covers, walk these steps in the actual repo. Do not skip any.

### Step 1 - Find the range to bounds conversion

Look for `GetMobilesInRange<T>(int x, int y, int range)` in `Projects/Server/Maps/Map.MobileEnumerator.cs` (or the Item equivalent enumerator). It will look like

```csharp
var clampedRange = Math.Max(0, range);
var edge = clampedRange * 2 + 1;
return GetMobilesInBounds<T>(new Rectangle2D(x - clampedRange, y - clampedRange, edge, edge));
```

This proves: range is the radius, the box is (2N+1) squared tiles, centered on the source.

### Step 2 - Confirm the box inclusivity

Look at `Projects/Server/Geometry/Rectangle2D.cs`

- Constructor: `_end = new Point2D(x + width, y + height);` - _end is shifted by width and height, so it is EXCLUSIVE (half-open [start, end))
- `Contains(int x, int y)`: `_start.m_X <= x && _end.m_X > x` - the strict greater than on _end confirms _end is exclusive

Therefore the box is half-open: start inclusive, end exclusive. With width = 2N+1, the inclusive integer range of X is exactly [x - N, x + N], which is the source tile and N tiles outward in each direction.

### Step 3 - Confirm makeBoundsInclusive is not in play

`MobileBoundsEnumerable` and `ItemBoundsEnumerable` have a `makeBoundsInclusive` parameter that, when true, expands the bounds by 1 (`++bounds.Width; ++bounds.Height;` in the enumerator ctor). This is used by callers that treat the bounds as coordinate edges rather than tile centers (for example the graphical client view rectangle).

For almost all AoE spells, abilities, and spawn logic, GetMobilesInBounds and GetItemsInBounds is called WITHOUT makeBoundsInclusive (default false). If you see makeBoundsInclusive true in the spell path, the effective box is (2N+3) squared tiles and the source is in the corner, not the center. Re-verify.

### Step 4 - Map to the spec wording

When matching a community spec like Stratics 14 points over a 3 tile radius, decide which interpretation you are using

- N tile radius = Chebyshev distance less than or equal to N from the source -> range argument = N. This is ModernUO convention.
- N tile diameter = full width of the AoE = N -> range argument = (N-1)/2. Rare in UO specs, double-check.
- N tile ring = only the outer ring at distance N -> use the GetMobilesInBounds trick of subtracting an inner rectangle, or filter the result by a min distance.

If a spec gives you both a numerical example AND a formula, always use the numerical example as the ground truth and reverse engineer the formula. For example Stratics Thunderstorm says 14 points at 100 skill with 0 focus and 3 tile radius, and 20 points at 100 skill with 6 focus and 9 tile radius. With damage formula `10 + skill/24` (equals 14 at skill 100) the damage matches. With radius 3 at focus 0 and 9 at focus 6, the formula is `3 + FocusLevel`. Confirmed.

## Pitfalls - read these before answering

1. Rectangle2D is half-open, not inclusive. The single most common error is assuming Contains includes both edges. It does not - the end edge is exclusive. For tile-aligned coordinates this gives the same result as a closed box, but it matters when bounds come from non-tile coordinates (map edges, screen rectangles).

2. The +1 in (2N+1) squared IS the source tile, not a buffer. Box size = 2N+1 can be misread as radius N+0.5, which would suggest range should be N-0.5. No. The +1 accounts for the inclusive source tile. range = 3 -> 7 by 7 box -> 3 tiles outward from the source tile.

3. makeBoundsInclusive is rarely used but is a landmine. When it is true, the source is NOT in the center - it is at one corner of the box. Spells and abilities almost never use it. If you find it in a spell path, treat it as a bug or a deliberate oddity and verify with the original developer or commit message.

4. Distance metric is Chebyshev, not Manhattan, not Euclidean. Diagonals count as 1 tile. A target at (source.x + 3, source.y + 3) is in range for range = 3. A target at (source.x + 3, source.y + 0) is also in range. This matches UO movement, visibility, and line of sight model.

5. Z is ignored by GetMobilesInRange. It is a 2D spatial query. Stacked multi-level dungeons, mounts vs riders, paragon spawns at unusual Z - none of that changes who is in range. If a spec mentions vertical range, you have a different problem.

6. Spec numbers can be wrong, contradictory, or rounded. Stratics, UOGuide, UOAlive, and the in-game spellbook tooltip sometimes disagree. The spellbook tooltip and the current live server are the strongest sources for live gameplay. Community wikis are best for historical and spec-intent questions. When in doubt, cite the specific source for each number you use.

7. Do NOT confuse tile with step in the UO movement sense. They are the same thing for this code path (1 tile = 1 coordinate unit = 1 step in cardinal and diagonal movement). But other UO docs occasionally use tile loosely. Verify against the math.

## Worked example: Thunderstorm

`Projects/UOContent/Spells/Spellweaving/Thunderstorm.cs` uses `Caster.GetMobilesInRange(3 + FocusLevel)`.

- Focus 0 -> range arg 3 -> 7 by 7 -> 49 tiles -> spec says 3 tile radius -> match
- Focus 1 -> range arg 4 -> 9 by 9 -> 81 tiles -> spec says 4 tile radius -> match
- Focus 6 -> range arg 9 -> 19 by 19 -> 361 tiles -> spec says 9 tile radius -> match

Caster excluded by `if (Caster == m || ...) continue;` in the loop.

## How to verify a change in the actual repo

```bash
# 1. confirm the file is on the expected branch
git status --short -- Projects/UOContent/Spells/Spellweaving/Thunderstorm.cs

# 2. confirm the diff is what you expect
git diff -- Projects/UOContent/Spells/Spellweaving/Thunderstorm.cs

# 3. build from the service repository root
dotnet build
```

Optional: a tiny in-game admin range command output can be cross-checked against the expected (2N+1) squared tile count for a known-empty sector.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Related ModernUO files (reference)

- `Projects/Server/Maps/Map.MobileEnumerator.cs` - GetMobilesInRange and MobileBoundsEnumerable
- `Projects/Server/Maps/Map.ItemEnumerator.cs` - same for items
- `Projects/Server/Geometry/Rectangle2D.cs` - Contains (half-open), constructor (_end exclusive)
- `Projects/Server/Items/Item.cs` near line 2529 - Item.GetMobilesInRange forwards to map
- `Projects/Server/Mobiles/Mobile.cs` - Mobile.GetMobilesInRange (same pattern)
- `dev-docs/era-expansion.md` - check whether the spell is gated by Core.AOS, Core.SE, Core.ML, etc.
- `dev-docs/content-patterns.md` - spell and ability content conventions

## Don't

- Don't state a tile count without walking the chain. 3 tile radius = 3 by 3 = 9 tiles is wrong; it is 7 by 7 = 49.
- Don't quote Stratics or UOGuide numbers without saying which source.
- Don't conflate makeBoundsInclusive semantics with default bounds semantics.
- Don't change a range in a spell without also checking every other spell in the same era pack - they often share a radius formula.
