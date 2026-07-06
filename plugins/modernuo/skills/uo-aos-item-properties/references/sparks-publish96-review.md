# Sparks (Publish 96 weapon property) Review Notes

Use these notes when reviewing or implementing the `Sparks` item property in RebirthUO/ModernUO.

## Source-backed classification

- Official UO.com Magic Item Properties lists **Sparks** as:
  - Intensity: `N/A`
  - Imbue weight: `No`
  - Found on: `Weapons (L)`
  - Cap: `N/A`
  - Description: chance to activate energy sparks on targets, causing energy damage over time; will not activate with special moves, Lightning Strike, Death Strike, or Onslaught; post-resist damage is returned to the attacker as mana; effect is doubled on monsters.
- UO.com Publish 96 lists Sparks under the **Dungeon Doom Update** as a new weapon property, alongside Bone Breaker and Swarm.
- UO.com Doom Gauntlet artifact table lists **The Deceiver** with `Sparks 20%`.
- UOGuide `Sparks` page describes it as a special property found on The Deceiver, one of the artifacts added with the Dungeon Doom Update in Publish 96.

Primary URLs:

- `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
- `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-96/`
- `https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-doom-gauntlet/`
- `https://www.uoguide.com/Sparks`

## Era decision

Sparks is **not a Stygian Abyss property** despite fitting near later weapon-hit attributes. It is Publish 96 / Dungeon Doom Update content, i.e. post-ToL live-era behavior.

In RebirthUO, if there is no publish-specific gate, prefer treating Sparks as a modern/extended weapon property gated at `Core.TOL` only if TOL is being used as the shard's modern-live umbrella. If TOL is intended to mean strict Time of Legends launch parity, require a custom publish/profile decision before enabling gameplay or distribution.

## RebirthUO implementation shape

Do **not** add Sparks to `SaWeaponAttributes` just because RebirthUO already has `HitCurse`, `HitFatigue`, and `HitManaDrain` there. A better shape is a separate modern/extended weapon-property container, e.g. `ExtendedWeaponAttribute.HitSparks` / `ExtendedWeaponAttributes`, so Publish 96 properties such as Sparks, Swarm, Bone Breaker, Bane, etc. do not become misleadingly `Core.SA` content.

Suggested implementation slices:

1. Storage + GM command property on weapons.
2. Tooltip/OPL row, era-gated.
3. Gameplay proc and DoT, era-gated.
4. Artifact/drop distribution in a separate ticket.

Do **not** enable LootPack, runic crafting, reforging, or imbuing as part of the property-storage/gameplay ticket. UO.com marks Sparks `Weapons (L)` and `No` imbue weight, but distribution policy must be reviewed separately.

## Known client/implementation clues

ServUO is not authoritative, but useful for API and client constants:

- `ExtendedWeaponAttribute.HitSparks`
- Tooltip cliloc: `1157326` (`Sparks ~1_val~%`)
- `TheDeceiver` sets `ExtendedWeaponAttributes.HitSparks = 20`
- `SparksContext` uses a 5-second context ticking every 1 second and calls `AOS.Damage(..., 0, 0, 0, 0, 100)` for energy damage.

Do not blindly copy ServUO formulas: verify/decide details for tick count, damage range, immunity/stacking, mana-return, and monster doubling. In the inspected ServUO code, `SparksContext.OnTick` used random 20-40 energy damage, but the public UO.com description requires post-resist mana return and monster doubling; make sure the RebirthUO implementation satisfies the source behavior, not only the ServUO approximation.

## Gameplay acceptance criteria

- Sparks is weapon-only and stored on `BaseWeapon`/weapon-equivalent items.
- Tooltip shows `Sparks ~n~%` only in the selected era/profile.
- Pre-selected-era: no effective value, no tooltip, no proc.
- A normal weapon hit can trigger Sparks by the property chance.
- Sparks must not trigger with weapon special moves, Lightning Strike, Death Strike, or Onslaught.
- Sparks deals Energy damage over time through the normal AOS damage/resist pipeline.
- Actual post-resist Sparks damage is returned to the attacker as mana.
- Effect is doubled on monsters.
- Timer/context is transient and cleaned up; avoid serialized timers or save-state dependencies.
- Distribution surfaces (loot/runic/imbuing/artifacts) are separate and intentionally reviewed.

## RebirthUO session implementation pattern

A RebirthUO implementation of Sparks used this shape successfully:

- Keep `SaWeaponAttributes` unchanged for true SA properties; put Sparks under `ExtendedWeaponAttribute.HitSparks` / `ExtendedWeaponAttributes` on `BaseWeapon`.
- Use `Core.TOL` as the practical modern-live gate until a publish-specific feature gate exists.
- Wire gameplay after successful weapon damage in `BaseWeapon.OnHit`, next to other post-hit weapon-property effects, and pass the already-resolved `WeaponAbility` / `SpecialMove` references into a small helper such as `ApplyExtendedWeaponHitEffects(...)`.
- Exclude Sparks when either an active `WeaponAbility` or `SpecialMove` is present. This covers Lightning Strike and Death Strike in RebirthUO because both are `SpecialMove` paths; if Onslaught is later implemented as a `SpecialMove`, the same guard covers it.
- Use a transient non-serialized context keyed by `(attacker, defender)` to prevent duplicate active Sparks contexts. Store `Mobile` refs and a `TimerExecutionToken`; cancel and remove when the effect ends or either mobile becomes invalid/deleted/dead/internal.
- Practical approximation used after maintainer approval: 5 ticks, 1-second interval, each tick rolls 20-40 Energy damage through `AOS.Damage(defender, attacker, damage, 0, 0, 0, 0, 100)`.
- Apply monster/non-player doubling before `AOS.Damage`, then return actual post-resist damage as mana with `attacker.Mana += damageGiven` so normal clamping applies.
- Keep gameplay test seams internal/static rather than driving full swing state when the full swing harness would be brittle: `ApplyExtendedWeaponHitEffects(...)` for proc/gate/exclusion and `ApplySparksTick(...)` for post-resist mana/monster doubling.
- Manual QA should explicitly say `HitSparks = 100` on a GM-created weapon, normal auto-attacks only, expect target visual + Energy DoT + mana return; special moves/Lightning Strike/Death Strike should not proc.

## Test anchors to require

- OPL test: `HitSparks = 20` emits cliloc `1157326` / argument `20` only in the enabled era.
- Era test: pre-enabled era stores safely but returns no effective value and no tooltip/effect.
- Proc test: 100% Sparks triggers on a normal hit.
- Exclusion tests: active WeaponAbility, Lightning Strike, Death Strike, and Onslaught do not trigger Sparks. In current RebirthUO, a generic `SpecialMove` exclusion is the durable automated proxy for Lightning Strike/Death Strike.
- Damage/mana tests: 0 and high Energy Resist targets return mana equal to actual post-resist damage.
- Monster double test: monster/non-player target gets doubled Sparks effect compared to player/mobile baseline.
- Distribution guard test/search: no accidental runic/loot/imbuing inclusion unless explicitly requested.
