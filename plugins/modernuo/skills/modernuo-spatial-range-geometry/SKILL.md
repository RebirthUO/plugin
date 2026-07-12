---
name: modernuo-spatial-range-geometry
description: >
  Use when proving exact ModernUO tile coverage for GetMobilesInRange,
  GetItemsInRange, GetClientsInRange, Get*InBounds, AoE radii, rings, or
  Rectangle2D conversions. Do not use for path-search behavior or region policy;
  route those to modernuo-pathfinding or modernuo-regions.
version: 1.1.0
author: Crome696
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - modernuo
      - spatial
      - range
      - geometry
      - performance
    related_skills:
      - modernuo-performance-hot-paths
      - modernuo-code-audit
      - modernuo-regions
      - modernuo-content-patterns
      - modernuo-era-expansion
      - modernuo-pathfinding
---

# ModernUO Spatial Range Geometry

## Boundary

Prove the coordinate set selected by a range/bounds call before changing gameplay.
For the standard centered range conversion, range `N` is a 2D Chebyshev radius:
`[x-N, x+N] x [y-N, y+N]`, a `(2N+1) x (2N+1)` box including the source tile
before gameplay filters.

## Workflow

1. Trace the exact current call from the spell/ability/system into the map
   enumerator; do not infer semantics from the method name.
2. Inspect the range-to-`Rectangle2D` conversion. Confirm width/height and the
   half-open `Contains` rule (`start` inclusive, `end` exclusive).
3. Check whether `makeBoundsInclusive` or a custom bounds overload modifies the
   rectangle. Account for that call site explicitly.
4. Separate spatial membership from gameplay filters such as source exclusion,
   LOS, Z, alive/harmful/team checks, and era gates.
5. Translate source wording as radius, diameter, ring, rectangle, or another
   metric. Resolve contradictory prose with a concrete numerical example and
   state the chosen source.
6. Add boundary tests for cardinal and diagonal points at `N`, just outside `N`,
   source inclusion, and any custom inner/outer ring or Z filter.

## Guardrails

- Range `0` is `1x1`; `1` is `3x3`; `3` is `7x7`, not `3x3`.
- The `+1` in `2N+1` represents the source coordinate, not padding.
- Default range queries are Chebyshev, not Manhattan or Euclidean; a diagonal
  offset `(N,N)` is inside.
- Standard mobile/item range enumeration is 2D. Do not claim vertical filtering
  unless the caller adds it.
- `makeBoundsInclusive` is a separate expansion convention; never mix it into the
  default centered-range result.
- Community/source numbers can conflict. Cite which value and era/ruleset the
  implementation follows.

## Output Contract

Return the call chain, input value, rectangle start/end and inclusivity, metric,
dimensions/tile count, source inclusion, post-query filters, source/era, and
verification. For a code change, include before/after coverage.

## Verification

- Test cardinal and diagonal boundary coordinates plus one coordinate outside.
- Confirm default/custom inclusivity and source filtering independently.
- Inspect current repository implementations rather than relying on remembered
  line numbers.
- Run the focused owning test/build or label a static geometry proof as such.

## Reference Routing

- Read [range verification chain and worked cases](references/range-verification.md)
  when translating a specification or auditing a custom bounds path.
- Load `modernuo-pathfinding` for route search, `modernuo-regions` for spatial
  policy, and `modernuo-performance-hot-paths` for query cost.
