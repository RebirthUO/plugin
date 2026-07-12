# Sparks Item Property Review Notes

Use when reviewing or implementing **Sparks** (Publish 96 / Dungeon Doom, post-ToL) on RebirthUO/ModernUO.

## Canonical sources

- **UO.com Magic Item Properties** — `Sparks`: intensity `N/A`, imbue `No`, `Weapons (L)`, cap `N/A`; Energy DoT; will not activate with special moves, **Lightning Strike**, **Death Strike**, or **Onslaught**; post-resist damage returned as mana; doubled on monsters.
- **UO.com Publish 96** — Dungeon Doom “New Weapon Properties”: Sparks Energy DoT; will not activate with **special moves**; same mana-return and monster-doubling rules. Worldwide release 2017-02-09.
- **UO.com Doom Gauntlet artifacts** — `The Deceiver`: `Sparks 20%` (distribution follow-up, not storage ticket).

## Source tension (review handling)

- Publish 96 prose is narrower on exclusions than the MIP table. For tests and acceptance criteria, prefer the **MIP named list** when both are cited; note the difference in Research Notes.

## RebirthUO container / era

- Add `ExtendedWeaponAttribute.HitSparks` (next free bit after existing enum members—re-check `origin/main` `AOS.cs`) on existing `ExtendedWeaponAttributes` / `BaseWeapon` wiring (closed container precedent, e.g. issue #7).
- Gate tooltip and gameplay with **`Core.TOL`** unless the shard adds a stricter Publish 96 gate before distribution.
- Do **not** use SA-named containers for Sparks. Do **not** add to `AosWeaponAttribute` for new Publish 96 props.

## ServUO (engine precedent only)

- `ExtendedWeaponAttributes.HitSparks`, tooltip cliloc **`1157326`** (`Sparks ~1_val~%`).
- `SparksContext`: 5 ticks, 1s interval, raw `20-40` Energy per tick; one context per attacker/defender; `BuffIcon.Sparks`.
- **Conflict:** ServUO may tie mana return to the main weapon hit, not each DoT tick. Canonical UO.com wording wins: mana from **post-resist Sparks tick damage**.

## Gameplay defaults (when official numbers absent)

- Label ServUO `5×1s`, `20-40` raw Energy/tick as **Partially resolved** with evidence class *engine precedent*; keep revisit as non-blocking follow-up.
- Exclude procs while `WeaponAbility` or `SpecialMove` is active (covers Lightning Strike / Death Strike in current RebirthUO).
- One active context per `(attacker, defender)`; no stack/refresh on duplicate proc; no post-effect immunity unless sources add it.
- Monster/non-player: double **raw** tick damage before `AOS.Damage`; players do not get doubling.
- Transient timers/contexts only—do not serialize active Sparks state.

## Repo anchors (refresh line numbers each review)

- `Projects/UOContent/Misc/AOS.cs` — `ExtendedWeaponAttribute` enum / `ExtendedWeaponAttributes.GetProperties`
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` — `OnHit` pipeline, `ExtendedWeaponAttributes` serialization/OPL
- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs` — `BuffIcon.Sparks`
- `Projects/UOContent.Tests/Tests/Items/Weapons/BanePropertyTests.cs` (or sibling) — focused test pattern

## Distribution

- `Weapons (L)` and The Deceiver `20%` are **not** permission to change loot/runic/imbuing/reforging in the storage/tooltip/mechanics ticket.