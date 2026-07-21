# Temporary weapon-bound effects in ModernUO

Use this reference for spells or systems that apply a short-lived combat/casting effect to the weapon a mobile is currently holding.

## Runtime model

- Key the owning dictionary by `BaseWeapon`, not only by caster. The effect belongs to the item and must disappear if that item moves, is disarmed, or is deleted.
- Store the caster, selected option, numeric proc value, duration timer, and independent booleans for each granted behavior.
- Never write temporary values into serialized `AosWeaponAttributes` or `AosAttributes`. Expose runtime query methods instead.
- If one behavior is suppressed by an existing permanent property, do not suppress unrelated temporary behaviors. Example: permanent Spell Channeling can suppress only the temporary channeling grant while retaining a threshold-based Faster Casting penalty.

## Integration points

Keep integration narrow and use the current item/cast context:

- `BaseWeapon` hit resolution: add the runtime bonus for the attacking weapon and selected `AosWeaponAttribute` before the existing chance/property multiplier.
- `BaseWeapon.AllowEquippedCast`: query the current weapon's temporary channeling state alongside the permanent `Attributes.SpellChanneling` value.
- `Spell.GetCastDelay`: query the caster's active weapon-bound effect for the temporary Faster Casting modifier. Preserve existing caps, protection penalties, SA delay handling, and wand early-return behavior.

## Choice-gump sequencing

For a spell that presents several options:

1. Validate the currently held weapon and conflicts during `CheckCast`.
2. On `OnCast`, display a fixed-layout gump and start a bounded cancellation/timeout timer.
3. Do not consume mana or reagents before selection. In the gump response, verify `Caster.Spell`, `SpellState.Sequencing`, current weapon identity, deletion state, and conflicts again.
4. Call `CheckSequence()` only after validation and then apply the runtime effect.
5. On cancel, timeout, disturbance, invalid response, or successful selection, close the gump and finish the spell sequence. Make timer cancellation idempotent.

## Cleanup matrix

Explicitly map and test every lifecycle named by the issue:

| Boundary | Native hook/pattern |
| --- | --- |
| Unequip, disarm, move | `BaseWeapon.OnRemoved` |
| Delete | `BaseWeapon.OnAfterDelete` plus removal path |
| Duration end | owning `Timer.OnTick` |
| Player/creature death | existing generated death events |
| Player/creature delete | existing generated delete events |
| Logout | `Configure()` subscribing to `EventSink.Logout` when policy requires it |

Cleanup should remove the dictionary entry, stop the timer, remove the buff, invalidate weapon properties if still present, and clear timer-held object references. It must be safe to call multiple times because removal and deletion can overlap.

## Source-policy handling

When official sources omit an exact gameplay constant, stop implementation and
route the claim through `rebirthuo-issue-research`. Continue only when a refreshed
`READY` packet supplies official evidence or an explicit, visibly labeled custom
policy with its value, scope, and cap. Never invent a deterministic table or use
emulator precedent as the default.

## Verification checklist

- Build the full solution with one worker and zero warnings/errors.
- Run the focused test class after every fixture or lifecycle change.
- Run the owning UOContent project with real client data configured.
- If the broad solution suite has unrelated OS-culture or timezone failures, report focused/owning-project results separately and preserve the exact baseline failure cluster. Do not call focused tests suite-green.
- Run targeted formatter verification on new files; repository-wide formatter output may include pre-existing violations, so do not reformat unrelated files merely to clear baseline noise.
- Before publishing, inspect issue-scoped paths, commit, push to the intended `origin`, and verify the PR remotely.
