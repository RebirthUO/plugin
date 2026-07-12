# Assassin Honed and Balanced — publish/source review

Use this reference for RebirthUO/ModernUO item-property review where either property is in scope. It records a source-first result, not a mandate to enable acquisition/distribution.

## Primary official evidence

- **Assassin Honed:** [Publish 74, 31 January 2012](https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2012-2/publish-74-31st-january/) introduces the property. Exact official mechanics: successful weapon hit; attacker and target face the **same direction**; bonus derives from original weapon swing speed; ranged weapons have a **50%** proc chance.
- **Balanced, two-handed melee:** [Publish 81, 16 April 2013](https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2013-2/publish-81-16th-april/) says the two-handed melee property was added to Imbuing and such weapons cannot parry or evade.
- **Current official table:** [Magic Item Properties](https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/) lists Assassin Honed as `N/A` intensity / `No` imbue weight / weapons `(L)`, and Balanced as `N/A` / **1.5** / two-handed weapons `(I)`, bows `(R)(L)`. It confirms potions and no parry/evasion for Balanced.

## Secondary cross-check and conflicts

- [UOGuide Assassin Honed](https://www.uoguide.com/Assassin_Honed) agrees on back-facing, original speed, SSI ignored, ranged 50%, and 300% damage cap. It gives illustrative maxima of 73% at 2 seconds and 33% at 4 seconds.
- [UOGuide Balanced](https://www.uoguide.com/Balanced) agrees on free-hand actions and Publish-81 parry/evasion loss, but says Balanced can be imbued onto bows. That conflicts with Publish 81's explicit two-handed-melee Imbuing addition; official evidence wins. Its listed materials (5 Relic Fragments, 10 Amber, 10 Essence of Balance) are secondary only.

## Implementation defaults when official sources do not quantify the value

1. **Assassin Honed direction:** implement the official same-direction relationship at the successful-hit boundary with masked directions:
   `((attacker.Direction & Direction.Mask) == (defender.Direction & Direction.Mask))`.
   Do not compare the raw enum because it includes Running; do not substitute an opposite-direction condition from a comparison engine when it contradicts the official source.
2. **Assassin Honed amount:** official material gives no coefficient. If an EA-clone default is needed, use the explicitly-labelled ServUO comparison formula `floor(146.0 / weapon.MlSpeed)`, added to ordinary percentage damage before the existing 300% cap. It matches UOGuide's 2.00-second → 73% illustration. Keep it a documented fallback, not an official claim.
3. **Era gates:** Publish 74 and 81 have no direct core flags. `Core.HS` is the practical nearest post-High-Seas gate; state this mapping explicitly.
4. **Balanced storage:** preserve existing ranged storage. Add a distinct persistent melee flag/property and a shared query/helper; do not migrate or reinterpret `BaseRanged.Balanced` data.

## origin/main anchors verified during research

- `Projects/UOContent/Items/Weapons/BaseWeapon.cs`: `OnHit` at line 1872; percentage-damage accumulator at 1905; cap at 2005; `CheckParry` at 1609.
- `Projects/UOContent/Items/Weapons/Ranged/BaseRanged.cs:13-21`: existing serialized ranged `_balanced`.
- `Projects/UOContent/Items/Skill Items/Magical/Potions/BasePotion.cs:115-130`: `HasFreeHand` currently recognizes only `BaseRanged.Balanced`.
- `Projects/UOContent/Spells/Bushido/Evasion.cs:80-113`: evasion calls `BaseWeapon.CheckParry`, so a correct parry rejection also prevents effective evasion.
- `Projects/UOContent/Misc/AOS.cs:1231` / `BaseWeapon.cs:195-202`: `ExtendedWeaponAttribute(s)` and persistent weapon attribute container.

## Review outcome pattern

- Assassin Honed is implementation-ready for a **storage/runtime-only** ticket once the fallback coefficient is named; keep acquisition/economy work separate.
- Balanced runtime/storage is ready, but a **full EA acquisition path is not** if the repository has no traditional Imbuing engine/catalogue or required resources. Split or explicitly defer `(I)` distribution rather than claiming full parity.

## Focused test checklist

- Assassin Honed: serialization/dupe/OPL; eight directions plus Running-mask cases; successful hit only; deterministic ranged 50% pass/fail; SSI cannot change `MlSpeed` input; ordinary cap/mitigation still applies.
- Balanced: two-handed melee free-hand potion path; unbalanced and one-handed negative cases; ranged regression; post-HS parry false; `Evasion.CheckSpellEvasion` false; storage/dupe/OPL; no accidental loot or Imbuing rollout.
