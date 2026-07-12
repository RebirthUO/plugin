# Toxic Weapon — Publish 121 Review

Use this reference when drafting or reviewing a RebirthUO/ModernUO item-property issue for `Toxic Weapon`.

## Source classification

- **Canonical — current property table:** [UO.com Magic Item Properties](https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/) lists `Toxic Weapon` with intensity `N/A`, imbue weight `No`, found on `Weapons (L)`, and describes activation through an equipped weapon context menu. The documented effect is extra poison damage plus a hit point regeneration debuff.
- **Canonical — introduction boundary:** [Publish 121](https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-121/) includes the Draconic Awakening/Draconic Incursions event and states the event was live on production shards from publish day.
- **Canonical — event examples:** [The Draconic Awakening (Autumn 2025)](https://uo.com/wiki/ultima-online-wiki/seasonal-events/the-draconic-awakening-autumn-2025/) and [Artifacts — Events](https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-events/) list Toxic Weapon on Riftwarden weapons. Those weapons separately show `Hit Poison Area` and `Poison Damage`; do not infer that either property is Toxic Weapon's formula.
- **Ruleset distinction:** New Legacy is documented separately in the Publish 121 deployment material for transfer processing. Do not classify Draconic Awakening as New Legacy merely because both appear in 2025 material.

## Era/publish decision

Use **Publish 121** as the initial publish. Treat the target as current live/post-TOL production-shard content. RebirthUO's current expansion model ends at `Expansion.EJ` and exposes `Core.EJ`; the issue form has no `EJ/current live` option, so use `Unknown` in the dropdown only with an explicit body note explaining the template mismatch. Do not invent `Core.NL`.

## Mechanics boundary

The official sources do not define the extra poison-damage formula, regeneration-debuff magnitude, duration, refresh/stack rules, eligible hit types, special-move interaction, poison resistance/immunity interaction, or PvP rules. Keep these as visible implementation decisions or live-client research items. A conservative first slice is storage + tooltip + reusable mechanics, without a named Riftwarden artifact and without loot/runic/reforging/imbuing rollout.

Do not conflate Toxic Weapon with:

- `Hit Poison Area` (`AosWeaponAttribute.HitPoisonArea`),
- a weapon's poison charges and `ApplyPoison`,
- elemental weapon `Poison Damage`, or
- Poisoning/Infectious Strike.

## RebirthUO anchors

- `Projects/UOContent/Misc/AOS.cs:1230-1342`: `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes`; Toxic Weapon is absent.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs:199-202, 240-241, 983-986, 1858-2389, 3084-3194, 3935-3967`: owned container lifecycle, hit pipeline, tooltip emission, dupe, and persistence.
- `Projects/UOContent/Context Menus/ContextMenuSystem.cs:35-39`: generic item context-menu dispatch; `BaseWeapon` currently has no context-menu override.
- `Projects/Server/Mobiles/Mobile.cs:8538-8659`: poison application, immunity, and poison-timer behavior; decide explicitly whether Toxic Weapon uses this API.

## Review checklist

- [ ] Body says `Publish 121` and production/live shards, not New Legacy.
- [ ] `N/A`, `No`, and `Weapons (L)` are preserved from the official table.
- [ ] Context-menu activation is treated as a stateful weapon feature.
- [ ] Unknown combat values are not fabricated from `Hit Poison Area` or `Poison Damage` values on event weapons.
- [ ] PvP and distribution are explicit decisions; `(L)` is not automatic permission to enable loot generation.
- [ ] `Core.EJ` is considered; no `Core.NL` is invented.
