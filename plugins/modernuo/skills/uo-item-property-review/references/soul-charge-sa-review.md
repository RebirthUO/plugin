# Soul Charge SA Shield Property Review

Use this reference when reviewing or implementing `Soul Charge` item-property tickets for RebirthUO/ModernUO.

## Source evidence

- **Canonical current property row:** UO.com Magic Item Properties lists `Soul Charge` with intensity `5 – 30`, imbue weight `No`, found on `Shields (R)(L)`, total cap `50`, and description `A chance to convert a percentage of damage dealt to the player into mana.`
- **Canonical publish/history:** UO.com Publish 60 / Stygian Abyss launch lists named SA shields with Soul Charge: `Sign of Chaos` has `Soul Charge: 20%`, and `Mystic’s Guard` has `Soul Charge: 30%`.
- **Community/history cross-check:** UOGuide Publish 60 mirrors the named shield examples. If browser navigation times out on UOGuide, a read-only terminal fetch (for example Python `urllib.request.urlopen`) is an acceptable fallback for extracting the same page text, but still classify it as community evidence.
- **Engine precedent:** ServUO `Scripts/Abilities/SAPropEffects.cs` implements shield-only Soul Charge by checking equipped `BaseShield` on `Layer.TwoHanded`, using `ArmorAttributes.SoulCharge` as the percent proc chance, restoring 30% of damage as mana, and sending message cliloc `1113636`. ServUO has a Fish Pie modifier path that raises conversion to 50%; keep that out of scope unless the ticket explicitly includes food/buff behavior.

## RebirthUO repo anchors to verify

Re-check these on the target branch and `origin/main` before locking line numbers:

- `Projects/UOContent/Misc/AOS.cs` — `AOS.Damage` is the central damage pipeline. Hook after final damage and/or actual HP delta are known; existing Battle Lust handling is a useful applied-damage seam.
- `Projects/UOContent/Misc/AOS.cs` — `AosArmorAttribute` / `AosArmorAttributes` are the likely storage surface. At the 2026-07 review, the next free armor bit on `origin/main` was `0x00000010`, but this must be rechecked immediately before implementation.
- `Projects/UOContent/Items/Armor/BaseArmor.cs` — owns `AosArmorAttributes` storage and delegates armor-attribute property-list rows.
- `Projects/UOContent/Items/Shields/BaseShield.cs` — use this as the host boundary; do not let generic armor/clothing hosts trigger the effect.
- `Distribution/Data/expansions.json` and `Projects/Server/ExpansionInfo.cs` — define the `Core.SA` era gate.

## Implementation shape

- Era gate: `Core.SA` for tooltip and gameplay.
- Host scope: equipped `BaseShield` only, normally `Layer.TwoHanded`.
- Chance: Soul Charge property value as a percent chance; clamp any effective aggregate to the published total cap `50`.
- Conversion: `floor(actualDamageReceived * 30 / 100)` mana, capped at `ManaMax - Mana`.
- Damage basis: actual post-resist damage the defender took, not pre-resist input damage.
- Distribution: UO.com `Shields (R)(L)` is source evidence for a later loot/runic/reforging rollout, not approval to change generation in the storage/tooltip/gameplay slice.
- Fish Pie: 50% conversion is engine precedent only; treat as non-blocking follow-up unless explicitly scoped.

## Focused tests

- Storage/API: set/read Soul Charge on a shield via the selected armor-property container.
- Tooltip: SA shield emits `Soul Charge ~value~%`; pre-SA and non-shield hosts do not.
- Gameplay: forced 100% chance with 100 actual damage restores 30 mana.
- Mana cap: 90/100 mana receiving 100 actual damage ends at 100.
- Era and host gates: pre-SA, non-shield armor/clothing, unequipped shield, deleted/dead defender, zero actual damage, and failed/0% proc do not restore mana.
- Distribution guard: no loot/runic/imbuing/artifact/vendor rollout in the first PR unless explicitly scoped.

## Review pitfalls

- Do not tie Soul Charge to parry/block or `BaseShield.OnHit`; it should be evaluated from the damage pipeline so spell/elemental damage can be handled consistently.
- Do not use pre-resist input damage for mana conversion; that over-rewards high-resist builds.
- Do not use broad `AosArmorAttributes.GetValue(m, SoulCharge)` as the gameplay source unless it is filtered to equipped shields; the aggregator may include non-shield armor/clothing.
- Do not treat ServUO as canonical for Fish Pie or cliloc behavior. Use it as engine/client precedent and verify client data or local property-list tests when possible.
