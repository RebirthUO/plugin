# Blood Drinker Item Property Review Notes

Use when reviewing or implementing the Stygian Abyss `Blood Drinker` weapon property for RebirthUO/ModernUO (e.g. GitHub `RebirthUO/ModernUO` issue #5).

## Source status

- **Canonical** — UO.com Magic Item Properties row:
  - Intensity `N/A`, imbue `No`, found on `Weapons (L)`, cap `N/A`
  - Wording: attacker gains life from Bleed Attack; damage done through bleed is transferred to attacker health
- **Canonical** — UO.com Publish 60 (Stygian Abyss launch): `Life Syphon (Blood Sword)` lists `Blood Drinker`
- **Engine precedent** — ServUO: `BloodDrinker` in `AosWeaponAttribute`; `BleedAttack` snapshots property at bleed start; heals on bleed ticks; tooltip cliloc `1113591`
- **Repo evidence** — RebirthUO `BleedAttack.cs` has no Blood Drinker hook; `Mobile.Damage` returns void — heal amount should use defender HP before/after tick

## RebirthUO planning guidance

- **Era:** `Core.SA` (Publish 60 / Stygian Abyss). Tooltip and gameplay inert pre-SA.
- **Container:** On `origin/main`, post-AoS weapon properties such as Bane and Battle Lust live in `ExtendedWeaponAttributes`. Prefer adding `BloodDrinker` there with `Core.SA` gating rather than copying ServUO's `AosWeaponAttribute` bit. Re-check next free `ExtendedWeaponAttribute` bit at merge time (parallel property PRs may reserve values).
- **Surfaces:** Split storage + tooltip + Bleed Attack heal from distribution. UO.com `No` imbue and `(L)` found-on do **not** authorize imbuing or random loot in the same ticket.
- **Gameplay:**
  - Snapshot `bloodDrinker` when Bleed Attack successfully applies (equipment swap after apply should not flip mid-bleed)
  - Heal attacker for applied bleed damage per tick; PvM uses existing non-player `* 2` bleed damage in `DoBleed`
  - No heal on failed ability, bleed immunity, dead/deleted attacker, or missing property
- **Messages:** `1113606` on heal (engine precedent); verify in property-list or client-data tests

## Focused test expectations

- SA vs pre-SA tooltip (`1113591`)
- Bleed with Blood Drinker heals; without property does not
- Player defender vs non-player defender (PvM multiplier on heal basis)
- Failure / immunity paths
- Serialization or dupe on new extended weapon bit
- No accidental loot/runic/imbuing enablement

## Issue-review defaults (non-blocking follow-ups)

- Named artifacts (Life Syphon, Vampiric Essence): separate ticket
- Exact cliloc verification if local `cliloc.enu` probe is inconclusive: use repo test harness with `MODERNUO_TEST_DATA_DIR`