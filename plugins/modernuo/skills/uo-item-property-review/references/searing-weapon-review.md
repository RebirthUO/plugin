# Searing Weapon Review Notes

Use for ModernUO/RebirthUO reviews or implementation planning of the activated lava-fishing weapon property **Searing**.

## Evidence classes

### Canonical — UO.com Magic Item Properties

`https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`

The current row states:

- intensity `1–7`, imbue weight `No`, host `Weapons (L)`;
- activation through a weapon context menu;
- `20%` melee / `10%` ranged chance for additional fire damage;
- `4` direct damage to the wielder on the effect;
- target hit-point-regeneration penalty for `4` seconds: `-20` players, `-60` monsters/NPCs;
- **each attack with an active weapon consumes 1 mana**.

The row does **not** specify the additional fire-damage number, the insufficient-mana transition, active-state lifecycle, initial publish, or regeneration debuff refresh/stack/immunity semantics.

### Canonical historical context — UO.com publishes

- Publish 71 (`https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2011-2/publish-71-21st-july/`) introduces Lava Proof Hook as the replacement for the lava-fishing pole.
- Publish 83 (`https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2013-2/publish-83-12th-september/`) contains a later “Searing Weapons – 1000” reward reference.

Neither source proves Searing's initial publish. High Seas is a defensible repository-policy gate candidate from lava-fishing provenance, not a proven canonical initial gate.

### Historical cross-check — UOGuide

`https://www.uoguide.com/Searing_Weapon` corroborates the listed chance, cost, direct damage, regeneration values, Lava Proof Hook acquisition, and Brittle / 200 durability. It is not authority for undocumented combat/lifecycle values.

### Engine comparison only — pinned ServUO

- `Scripts/Abilities/SAPropEffects.cs` at `6fd01855840590e22cc73d94b5f7d9a97b1cf537` chooses `10–15` pre-resist fire damage and a four-second context.
- `Scripts/Items/Internal/ItemSockets/SearingWeapon.cs` stores a persistent `Extinguished` flag, starts extinguished, exposes an equipped-only context-menu toggle, and extinguishes on unequip.

**Critical conflict:** its BaseWeapon flow decrements mana *inside the successful-proc branch*. Do not use this as an EA-clone default: it conflicts with UO.com's every-active-attack cost. Its attacker/target context is only created when absent, which is comparison evidence for neither a canonical refresh nor a stacking rule.

## Current RebirthUO anchors

Verify against the matching default branch before using line numbers. At review time, `origin/main` was `519e8debb`:

- `Projects/UOContent/Misc/AOS.cs:1252-1380` — `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes`; select the next free bit at implementation time.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:989-998,3968-4000` — extended-attribute copy/default/migration boundaries.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:2150-2393` — post-mitigation hit pipeline and normal-hit-only property seam. A source-required every-attack mana debit cannot be accidentally buried inside a successful-proc branch.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:3191-3194` — property-list ordering.
- `Projects/UOContent/Misc/RegenRates.cs:44-85` — regeneration derives from equipped `AosAttribute.RegenHits`; apply the penalty through transient target context rather than mutating durable item attributes.
- `Projects/UOContent/Items/Weapons/Focus.cs` and `Projects/UOContent.Tests/Tests/Items/Weapons/FocusPropertyTests.cs` — transient-context cleanup and tests for unequip, property removal, death, deletion, logout, and serialization boundaries.

No `BaseWeapon` context-menu implementation was found in that branch; find the correct shared/item seam before coding.

## Review gate and tests

Keep triage when EA-fidelity values or lifecycle behavior remain source-unknown and no maintainer policy has selected a default. Do not make a 10–15 test canonical.

A future implementation test matrix must distinguish:

1. active versus inactive state;
2. every eligible attack mana debit **regardless of proc outcome**;
3. melee/ranged chance;
4. fire mitigation and direct self-damage;
5. player/NPC regeneration values and a chosen reapply policy;
6. insufficient-mana, context toggle, unequip, death, deletion, logout, and serialization;
7. explicit era policy gating; and
8. no acquisition/distribution rollout.
