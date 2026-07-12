# Damage-reactive item-property implementation pitfalls

Use this reference when implementing an incoming-damage property in the UOContent layer.

## Mechanics evidence

For the Damage Eater family, the issue contract and current UO.com wording establish:

- SA-era gating; current host surface is armor and shields, not weapons.
- Kinetic maps to physical damage; Fire, Cold, Poison, and Energy map to their matching post-resist portions.
- The all-damage eater also handles direct damage and is capped at 18%.
- Same-type totals stack up to 30%; all-damage and matching specific values are non-additive: use the larger applicable heal.
- Up to 20 pending healing charges; the selected implementation policy was one queued type portion per quiet three-second interval, with every new damage event resetting the interval. Document this interpretation beside the implementation and assert the exact boundary in tests.
- Stored values are inert before SA. Do not add loot, runic, reforging, imbuing, artifact, vendor, or weapon-host distribution in the initial storage/gameplay slice.

## Combat integration

`AOS.Damage` has optional parameters in this order after the five elemental percentages: `chaos`, `direct`, `keepAlive`, etc. A test/helper call that passes `direct` immediately after `energy` silently treats it as `chaos`; pass `0, direct` explicitly. Inspect the local signature before writing combat tests.

Preserve the existing total-damage formula. Expose post-resist portions separately for the new effect, but do not replace the original summed numerator/division with independently rounded component sums. Normalize component portions against the actual `appliedDamage` so quiver, barding, keep-alive, and direct-damage adjustments do not over-heal.

Armor Ignore is still typed damage, not automatically direct damage. After any chaos percentage is randomized into a concrete type, populate physical, fire, cold, poison, and energy portions from their supplied percentages even though resistance is bypassed. Populate the direct portion only from the `direct` parameter; never fall back to assigning all Armor Ignore damage to `directPostResistDamage`. Add a regression test for Armor Ignore physical/elemental matching so a specific eater cannot be bypassed or an all-damage eater triggered incorrectly.

## Context and cleanup rules

A damage context must not be created for an unmatched damage type and left with no timer. After adding damage, clear a newly created context when it has no pending charges. If a context already has pending charges, any subsequent positive damage should reset the three-second conversion deadline, even when that new damage type does not add a charge or the 20-charge cap is already full.

Use transition-time cleanup where possible:

- armor removal/deletion when the removed armor carried an eater;
- setting the last active eater property to zero while equipped;
- death/deletion event handlers for supported mobile families;
- timer callback validation for `Deleted`, `Alive`, map validity, and active equipped values.

Keep the hot-path no-property check to one equipped-item scan; do not call a six-attribute aggregation loop for every incoming hit when no eater is equipped. Context dictionaries must cancel their timer token and remove the mobile on every cleanup path.

## Client cliloc verification

ServUO IDs are candidates until verified against the shard's client data. ModernUO's `Localization` loader can parse the real `cliloc.enu`; a small temporary program may invoke the private `(lang, file)` overload through reflection against the installed client file. Verify the six tooltip IDs and any healing-message ID before claiming tooltip evidence. Remove temporary verification projects after the check.

## Validation scope

Run owning-project build, focused property tests, owning `UOContent.Tests`, and the broad solution separately. On Windows cultures, `Server.Tests` decimal-format failures can be baseline locale failures; rerun that owning project with the documented invariant-globalization workaround and report normal-culture and workaround scopes separately. Never call focused tests suite-green.
