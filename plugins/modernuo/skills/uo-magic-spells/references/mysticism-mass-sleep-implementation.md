# Mass Sleep implementation notes (ModernUO/RebirthUO)

Use this alongside `mysticism-mass-sleep-research.md` when implementing or reviewing post-Publish-65 Mass Sleep.

## Required behavior shape

- Register only under `Core.SA` at spell ID 686.
- Implement a **ground-targeted** radius-3 AoE (`ITargetingSpell<IPoint3D>`, `SpellTarget<IPoint3D>(allowGround: true)`).
- Preserve normal target-cursor / town / map / harmful / LOS validation. Do not add a per-target `Caster.CanSee(target)` filter: current official wording explicitly makes hidden players eligible. Use `ValidIndirectTarget`, `CanBeHarmful`, and `InLOS`.
- Current-era behavior is Publish 65 **stupor**, never a hard attack/cast lockout. Apply named central maluses for Faster Casting, Faster Cast Recovery, swing speed, and player walk speed.
- Duration precedent: `(Mysticism + max(Focus, Imbuing)) / 20 + 3 - target Magic Resist / 10`; do not apply non-positive results.
- On positive damage, remove stupor immediately. For player targets, apply 3–12 seconds of Magic Resist-scaled reapplication immunity (`clamp(floor(resist / 10), 3, 12)`).

## Correct hook coverage

`SpellHelper.Damage` only catches spell damage. A Mass Sleep break-on-damage implementation must also be invoked from the content-layer `PlayerMobile.OnDamage` and `BaseCreature.OnDamage` paths, so weapon and other ordinary incoming damage clear the state. Keep cast/cast-recovery/weapon-delay effects as small central queries in `Spell.GetCastDelay`, `Spell.GetCastRecovery`, and `BaseWeapon.GetDelay` rather than duplicating rules in each spell or weapon.

Store effect and immunity state as transient dictionaries keyed by target. Subscribe cleanup to logout and map changes, and use generated player/creature death/deletion events. Cancel every `TimerExecutionToken`, clear buff icons, and restore player speed control on every removal path. Do not persist this transient state.

## Useful regression coverage

At minimum cover:

1. SA-only spell registry registration at 686 and absence before SA.
2. Fifth-circle metadata, scroll ID, and reagents.
3. Duration uses the higher of Focus/Imbuing and falls to zero at sufficient target resist.
4. Stupor exposes FC/FCR/SSI maluses without blocking casts/attacks.
5. Positive damage clears the effect and starts player immunity at the resistance-derived duration.
6. Expiry, death/delete, logout, and map-change paths clear state without stale timers.

A complete manual client pass should still inspect particles, buff presentation, and actual movement-control behavior.
