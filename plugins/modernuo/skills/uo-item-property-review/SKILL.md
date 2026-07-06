---
name: uo-item-property-review
description: Review and plan Ultima Online item-property tickets in RebirthUO/ModernUO, including source classification, era/container placement, tooltip/client cliloc, gameplay hooks, distribution boundaries, and test expectations.
version: 0.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [UltimaOnline, RebirthUO, ModernUO, item-properties, review, parity]
    related_skills: [rebirthuo-github-review, uo-combat-pipeline, modernuo-era-expansion, modernuo-property-lists, modernuo-test-workflow]
---
# UO Item Property Review

## Overview

Use this skill when reviewing, triaging, or planning Ultima Online item-property work for RebirthUO/ModernUO. It keeps property work separated into source evidence, era/ruleset, storage container, tooltip/client presentation, gameplay effect, distribution/economy rollout, and tests.

## When to Use

- A RebirthUO issue asks for a magic item property, weapon property, armor property, negative property, artifact property, or tooltip/property-list change.
- A property appears in UO.com Magic Item Properties, UOGuide, Stratics, ServUO, or local RebirthUO containers and needs era/container placement.
- The change may touch `AOS.cs`, `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, loot/runic/reforging/imbuing, combat, buffs, or property lists.

## Procedure

1. **Classify the source evidence.** Prefer UO.com for current official wording, then UOGuide/Stratics for mechanics/history, then issue evidence, then repo evidence. Use ServUO only for comparison constants or implementation clues, not as official parity proof.
2. **Separate property surfaces.** Treat storage, tooltip, gameplay effect, and distribution as separate decisions. A property can be implemented for GM/test use without adding it to loot, runics, reforging, imbuing, artifacts, or vendors.
3. **Choose the era/container deliberately.** Check whether the property belongs in an existing AoS, SA, absorption, defensive, or extended/modern container. Do not choose a container just because a similar implementation exists; match the property's era and product source.
4. **Map repo anchors.** Identify the existing container enum/class, owning item class, `GetProperties` block, gameplay hook, save/migration surface, and focused test file before calling a ticket implementable.
5. **Verify tooltip/client data.** Prefer known clilocs, but mark cliloc IDs as candidates until checked against local client data or existing repo tests.
6. **Define gameplay exactness.** For proc properties, specify chance formula, trigger timing, excluded abilities/special moves, PvP/PvM differences, immunity/cooldown/stacking, durability/resource effects, and cleanup.
7. **Guard the economy.** If UO.com says `(L)` or lists found-on items, that is evidence for a future distribution ticket, not automatic permission to change loot generation in a storage/gameplay ticket.
8. **Require focused tests.** Cover era gate, tooltip, effective aggregation, normal trigger, exclusions, cleanup, and non-distribution guard. Label focused tests honestly; do not call them broad-suite green.

## Caddellite Infused Khaldun marker note from session research

When reviewing `Caddellite Infused`, `Mask of Khal Ankur`, `Pendant of Khal Ankur`, `Cultist's Ritual Tome`, Treasures of Khaldun, or Khal Ankur tickets, read `references/caddellite-infused-khaldun-marker.md` before choosing a container. Treat `Caddellite Infused` as a Publish 101 / Dynamic Treasures Khaldun event marker, not a normal AoS/SA magic item property. It should not be added to `AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, SA containers, random loot, runics, reforging, or imbuing as a rollable property. If event mechanics are in scope, plan a persistent content marker plus tooltip cliloc `1158662`, Khaldun damage-gate checks, harvest/craft infusion, and explicit distribution boundaries. For isolated Mask/Pendant parity, the tooltip line can be fixed artifact presentation, but the mechanics are incomplete until Khaldun event damage gating exists.

## Craft Exceptional Bonus talisman note from session research

When reviewing or implementing `Craft Exceptional bonus`, read `references/craft-exceptional-bonus-talisman-review.md` before planning storage or tests. Treat it as a talisman-specific ML crafting property (`Skill` + `ExceptionalBonus` on `BaseTalisman`), not a generic AoS/SA attribute. The key review traps are: UO.com `(L)` does not authorize loot/runic/imbuing rollout; UOGuide says the bonus does not unlock `0%` exceptional chance; `SuccessBonus` must not double-increase exceptional chance; and Smith/Tailor BOD eligibility uses the same `GetExceptionalChance()` path and should be called out as a side effect.

## Splintering Weapon note from session research

When reviewing or implementing `Splintering Weapon`:

- UO.com Magic Item Properties lists intensity `5–30`, imbue weight `No`, found on `Weapons (L)`, cap `N/A`, bleed + forced-walk, stack/extend with Bleed Attack, substantial durability compromise, 15s player immunity to Splintering bleed/forced-walk, and no processing with Disarm/Infectious Strike/Injected Strike.
- UO.com Publish 96 confirms the Disarm bugfix.
- UOGuide confirms bleed, **4s forced walking**, stack with Bleed Attack, and SA/artifact examples such as Staff of Shattered Dreams, Sword of Shattered Hopes, and Brightblade, commonly at `20%`.
- Prefer `SaWeaponAttribute.SplinteringWeapon` / `SaWeaponAttributes` with `Core.SA` gating. Do **not** put it into `ExtendedWeaponAttributes` just because Publish 96 mentions a Disarm bugfix; RebirthUO uses `ExtendedWeaponAttributes` for TOL/post-ToL properties such as Sparks/Swarm.
- `Weapons (L)` is a distribution fact, not automatic approval to enable loot/runic/reforging/imbuing/artifact rollout in the same ticket.
- ServUO comparison hints: cliloc candidate `1112857`, `BuffIcon.SplinteringEffect`, 4s context, player bleed immunity roughly 15/16s, and durability reduction around `HitPoints = Math.Max(0, HitPoints - 10)`. Treat these as implementation clues, not official parity proof.
- Do not copy the Sparks/Swarm all-special-move exclusion pattern. Splintering source exclusions are named: Disarm, Infectious Strike, Injected Strike. If Injected Strike does not exist locally, leave a source-commented TODO or add the exclusion when the move exists.
- Focused tests should cover SA/pre-SA aggregation, tooltip, 100% proc, Disarm/Infectious exclusions, no blanket special-move exclusion, 4s forced-walk cleanup, 15s player immunity, bleed stack/extend behavior, durability loss, transient context cleanup, and no accidental distribution.

## Pitfalls

- Do not treat UO.com `(L)` as approval to enable random loot in the same ticket as storage/gameplay.
- Do not copy the exclusion policy from a different property. Some properties exclude all special moves; others exclude only named moves.
- Do not put SA properties into a TOL/extended container merely because later publish notes mention bugfixes.
- Do not rely on ServUO as canonical behavior. It is useful for likely clilocs, buff IDs, durations, and comparison test values only after UO.com/UOGuide source framing is done.
- Do not add serialized active effect state for transient hit effects; use timers/contexts with cleanup.

## Verification

A review is complete when it includes source URLs and what each proves, era/ruleset and container decision, repo paths/classes/methods to change, explicit distribution decision, test values and focused/broad validation plan, and PvP/PvM/economy/save/client/performance risks.
