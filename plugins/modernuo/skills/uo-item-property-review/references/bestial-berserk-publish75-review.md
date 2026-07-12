# Bestial Suit / Berserk — Publish 75 source review

Use this as a source-conflict checklist when reviewing or planning the Bestial Suit Berserk property. It is evidence for ticket readiness, not an implementation specification.

## Sources captured 2026-07-11

- **Official current property row:** https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/
  - Berserk is `N/A` intensity, `No` imbue weight, and **Bestial Suit only**.
  - Says rage triggers below 50% health, reduces spell/weapon damage and all healing, retains reduced healing for **8 seconds** after rage, and enforces a **60-second** cooldown.

- **Official Publish 75 page:** https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2012-2/publish-75-26th-march/
  - Dated **26 March 2012**.
  - `Bestial (Berserk) Suit` section: no stealth in rage; timeout updated to **8 seconds**; healing is reduced during rage and for **8 seconds** after exit; cooldown is **60 seconds**.
  - A later entry under the same page's `Bug Fixes` says the timeout was lowered to **5 seconds from 15**. This is an internal official-source conflict.

- **UOGuide cross-check:** https://www.uoguide.com/Publish_75
  - Mirrors the eight-second Bestial-section wording; does not resolve the later five-second official entry.

- **High Seas historical context:** https://www.uoguide.com/Ultima_Online:_High_Seas
  - High Seas launched with Publish 68 on 12 October 2010. Publish 75 is post-High-Seas. Treat `Core.HS` as a repository-gate candidate, not proof that the shard must select that gate.

## Review conclusion

Do not remove `triage` or choose mechanics silently until maintainers resolve:

1. Rage duration: official `8 seconds` versus official `5 seconds` later on the same Publish 75 page.
2. Numeric spell/weapon mitigation and healing-reduction values: the captured official sources are qualitative only.
3. Concrete host: Bestial Suit pieces/classes, full-suit versus per-piece activation, and acquisition policy.
4. Healing coverage: current ModernUO `Mobile.Heal` / `OnHeal` catches standard heals, but direct `Hits +=` paths (for example leech and some abilities) bypass it. “All healing effects” must be made testable rather than assumed.

## Repository implications observed on origin/main

- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs` contains a `Berserk` icon, but no Bestial Suit content/runtime system.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` and `Projects/UOContent/Spells/Base/SpellHelper.cs` have distinct damage paths; a generic `AOS.Damage` hook risks reducing unrelated damage sources.
- Bestial Suit content, distribution, and runtime state should remain separate surfaces. Do not add random loot, runic, reforging, imbuing, vendors, or artifacts during the property-mechanics slice.
