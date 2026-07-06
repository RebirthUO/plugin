# Item-Property Review: Cliloc, Battle Lust, Bane, and Bestial/Berserk Notes

Use this when reviewing RebirthUO item-property issues where UO.com gives a terse property row and the repo/client need concrete tooltip, behavior, set-item, or runtime-effect anchors.

## Battle Lust evidence pattern from #7

Authoritative/source-backed anchors used for Battle Lust review:

- UO.com Magic Item Properties row: `Battle Lust`, `Weapons (R)(L)`, caps `45 pvp` / `90 pvm`, gain every 2s, decay one point every 6s.
- UO.com Publish 60 / Stygian Abyss lists Battle Lust on SA artifact weapons, making `Core.SA` the safe default era gate for implementation.
- UO.com Publish 114 only adds a later buff icon for Battle Lust; do not treat that as the property's introduction.
- UO.com Runic Reforging lists Battle Lust in Vicious/of Slaughter; do not infer loot/runic/imbuing distribution from a property-mechanics ticket unless explicitly scoped.
- Local client cliloc can confirm display strings:
  - `1113710` = `Battle Lust`
  - `1113748` = `The damage you received fuels your battle fury.`
  - `1152385` = long Battle Lust property description with 15% per opponent, 45% PvP / 90% PvM, two-second gain and six-second decay.

ServUO can be used as a community-code oracle only for gaps not stated by official sources. For Battle Lust, ServUO's implementation uses `damage < 30` as the "significant damage" cutoff and multiplies internal lust points by `attacker.Aggressed.Count`, capped at 45 for player defenders and 90 otherwise. Label this as reference implementation evidence, not official UO truth.

## Bestial/Berserk evidence pattern from #8

Authoritative/source-backed anchors used for Berserk review:

- UO.com Magic Item Properties row: `Berserk`, `Intensity N/A`, `Imbue Weight No`, `Found on Bestial Suit`, `Cap N/A`; description says rage triggers when health drops below 50%, the player takes less damage from spells and weapons, healing effects are greatly reduced, healing reduction continues for 8 seconds after rage ends, and a 60 second cooldown prevents re-entry.
- UO.com Magic Item Properties also calls Berserk an unusual property currently only found on the Bestial Suit from Clean-up Britannia. Do not infer general loot/runic/imbuing distribution from this row.
- UO.com Clean-up Britannia confirms `BEASTIAL SUIT`, 4-piece set, `Can Be Imbued`, and `SET BONUS Berserk 5`.
- UO.com Publish 83 only proves the Bestial Set existed by that publish; it is not a clean introduction/era-gate source by itself.
- Local client cliloc can confirm display strings and richer behavior text:
  - `1151541` = `Berserk ~1_VAL~`
  - `1151542` = `Berserk ~1_VAL~ (total)`
  - `1151532` = `You enter a berserk rage!`
  - `1151535` = `Your berserk rage has subsided.`
  - `1151229`-`1151232`, `1151547`-`1151550` = Bestial piece tooltips with `Berserk 1` and set bonus `Berserk 5 (total)`.
  - `1152435` = long Bestial/Berserk description: effect scales from equipped set pieces and remaining health; starts when user takes damage below 50% HP; hues armor by rage stage; reduces all post-resist damage; reduces healing including hit point regeneration; grants additional stamina refresh every second; recedes after no-damage window; after recede gives 8s reduced healing and 60s re-entry lockout.
- ServUO can be used only as community-code reference for numeric gaps. In the checked ServUO snapshot, `BeastialSetHelper` used `block = TotalPieces * Level + 2`, `damage absorb = equipped * Level + 2`, and `Level = DamageTaken / 50` capped 1..5, with a post-resist AOS hook. The checked snippets did not fully cover UO.com/client claims for 60s cooldown, 8s post-rage healing reduction, or stamina refresh; call that out before marking an issue implementable.
- RebirthUO repo anchors to inspect for this class of review: `AOS.Damage` for post-resist damage ordering, `Mobile.Heal`/`OnHeal` for generic healing, `SpellHelper.Heal`, `BaseHealPotion`, `BandageContext`, `RegenRates.Mobile_HitsRegenRate`, `BuffIcon.Berserk`, and local searches for Bestial/CleanUpBritannia/`ISetItem`/`SetItem` infrastructure.
- Review guidance: Berserk is a runtime set effect, not a normal percentage-valued AoS/SA attribute. Storage/tooltip/gameplay/distribution should be split, and an implementation-ready decision needs exact formulas or an explicit RebirthUO custom-policy acceptance of reference-code values.

## Bane evidence pattern from #6

Authoritative/source-backed anchors used for Bane review:

- UO.com Magic Item Properties row: `Bane`, `Weapons(L)`, `Intensity N/A`, `Imbue Weight No`, `Cap N/A`; text says it only triggers when target health is below 50%, chance and damage increase as health decreases, and Bane deals physical damage based on 30% of the target's max hit points.
- UO.com Publish 83 page is the official introduction anchor: `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-83/` says “New Item Property Bane” on certain weapons, only under 50% target HP, chance and damage increase, up to 30% max HP physical damage, capped at 350 physical damage. This makes canonical era `Publish 83`; RebirthUO still needs an explicit mapping because there is no built-in publish-83 flag.
- UOGuide Bane can be used as community mechanics evidence: `https://www.uoguide.com/Bane` says Bane was introduced with Publish 83, 30% Max HP capped at 350 physical before physical resist, damage potential starts near 50% at half HP and scales to 100% near death. It gives examples: 12,000 HP target with 70% physical resist scales about 52→105 damage; 150 HP player with 70% physical resist scales about 7→13.5 damage. It does not provide exact proc-chance numbers.
- Local client cliloc can confirm display and missing table details:
  - `1154671` = `Bane`
  - `1154570` = description stating the damage is physical, can be reduced by the target's physical resistance, can reach up to 30% of maximum hit points, and cannot exceed 350 damage. It also repeats that the chance increases as target HP decreases.
- ServUO can be cited only as reference implementation evidence, not official truth. Checked anchors: `Scripts/Misc/AOS.cs` stores `ExtendedWeaponAttribute.Bane`; `Scripts/Items/Equipment/Weapons/BaseWeapon.cs` uses `min(350, HitsMax * .3) * (1 - Hits/HitsMax)` below 50% HP but has no explicit proc-chance and adds into the current weapon damage before `AOS.Damage`; `Scripts/Mobiles/NPCs/Mannequin/Property/ExtendedWeaponAttribute.cs` confirms clilocs `1154671`/`1154570`. Call out the physical-damage concern if copying ServUO would let elemental weapon splits convert Bane away from physical damage.
- The UO.com row, Publish 83 text, UOGuide, client cliloc, and ServUO reference still do **not** give the exact HP-dependent proc-chance curve or rounding. Mark those as missing unless an OSI test or explicit RebirthUO custom/reference-policy supplies them.
- Repo anchors seen on current RebirthUO `live`: `BaseWeapon` already stores `ExtendedWeaponAttributes` field 32 and the v12 migration schema includes it; `ExtendedWeaponAttributes` currently only has `HitSparks`/`HitSwarm` and is `Core.TOL`-gated; `SaWeaponAttributes` only has `HitCurse`, `HitFatigue`, `HitManaDrain`; `BaseWeapon.GetProperties` has SA/TOL hit rows but no Bane row; `BaseWeapon.ApplyExtendedWeaponHitEffects` and `ApplySaWeaponHitEffects` are nearby hit-effect patterns; `AOS.Damage` is the physical-resist path; `BaseRunicTool.ApplyAttributesTo` and `LootPack.Mutate` do not currently distribute Bane.
- Review guidance: do not model Bane as a percentage-valued SA hit property unless source evidence proves item intensity/proc chance is stored that way. Treat it initially as a bool/flag-like extended weapon property candidate and keep loot/runic/reforging/imbuing distribution separate. Storage+tooltip can be implementation-ready before gameplay; gameplay remains blocked if the proc chance/gate policy is unresolved.

## Prized evidence pattern from #21

Authoritative/source-backed anchors used for Prized review:

- UO.com Magic Item Properties row: `Prized`, `Intensity N/A`, `Imbue Weight No`, `Armor(L), Jewelry(L), Weapons(L), Shields(L)`, `Cap No`; description says item insurance cost is increased and the item cannot be blessed.
- UOGuide `Prized` and `Publish 86` provide the history anchor: Prized was introduced with Publish 86 / global loot changes. RebirthUO has expansion flags rather than publish flags, so reviews should name the canonical era as Publish 86 and require an explicit project gate/policy (usually `Core.HS` as the closest existing expansion approximation unless a granular publish helper/config is introduced).
- Local client cliloc can confirm display and description strings:
  - `1154910` = `Prized`
  - `1155644` = `This property indicates that an item has increased item insurance cost and cannot be blessed.`
- ServUO can be used as a community-code oracle for implementation constants: it models Prized as `NegativeAttribute.Prized`, emits OPL cliloc `1154910`, blocks ClothingBlessDeed, and doubles the computed insurance cost (`cost *= 2`). Label this as reference-policy evidence, not official UO truth.
- RebirthUO repo anchors seen on current `live`: `AosAttribute.Brittle` already stores a negative cross-type bit in `Projects/UOContent/Misc/AOS.cs`; `BaseWeapon`, `BaseArmor`/`BaseShield`, and `BaseJewel` already persist `AosAttributes`, so a minimal Prized slice can add `AosAttribute.Prized` without new host migrations. `PlayerMobile.GetInsuranceCost` currently returns a flat 600 and is used by manual insurance, auto-renew, and the insurance gump; `ClothingBlessDeed` is the concrete bless-deed blocker. Keep Loot/Runic/Imbuing/Reforging/Artifacts out of scope unless explicitly requested.
- Expected focused test values for a minimal slice: cliloc `1154910` on Katana/RingmailChest/WoodenShield/GoldRing in the chosen Publish86+ gate, hidden before the gate; base insurance cost 600 -> Prized 1200 under the ServUO x2 policy; ClothingBlessDeed sends `1045114` and leaves the item/deed unchanged.

## Local cliloc extraction recipe

When a review needs exact tooltip/cliloc strings and the repo has a local UO client under `C:/Users/Jsiem/Documents/GitHub/RebirthUO/clients/...` or `C:/Program Files (x86)/Electronic Arts/Ultima Online Classic/`, inspect `Cliloc.enu` rather than guessing raw text.

Modern UO client cliloc files may be BWT-compressed. RebirthUO has the decompressor algorithm in `Projects/Server/Client/BwtDecompress.cs` and the loader shape in `Projects/Server/Localization/Localization.cs`. Use the reusable script `scripts/extract-cliloc-ids.py` when you need selected IDs:

```bash
python C:/Users/Jsiem/AppData/Local/hermes/profiles/ultima-online/skills/github/rebirthuo-github-review/scripts/extract-cliloc-ids.py \
  "C:/Users/Jsiem/Documents/GitHub/RebirthUO/clients/UOAlive_Package/UOAlive 7.0.114.2/Cliloc.enu" \
  1151541 1151542 1152435
```

If adapting the script inline during a review, prefer a real `.py` file or `execute_code` for the decompressor body rather than a large shell heredoc; that keeps MSYS path/quoting and shell-metacharacter handling out of the cliloc parsing step.

Review output should cite local cliloc as `Client-Cliloc, local <client version> data` and include only the specific cliloc IDs/text used. Do not paste broad cliloc dumps.

## Review guidance

For item-property tickets, make Storage/Tooltip/Gameplay/Distribution separate decisions:

1. Storage: which attribute container/bit owns it (`AosWeaponAttributes`, `SaWeaponAttributes`, runtime state, etc.).
2. Tooltip: exact cliloc or explicit `Quelle fehlt` if unknown.
3. Gameplay: formula, era gate, runtime context and cleanup needs.
4. Distribution: loot, runic, imbuing, artifacts. Keep out of scope unless explicitly requested.

If official sources establish the property but not an implementation constant, mark the constant as source-derived from a reference implementation or require OSI testing before implementation.