---
name: uo-item-property-review
description: Review and plan Ultima Online item-property tickets in RebirthUO/ModernUO, including source classification, era/container placement, tooltip/client cliloc, gameplay hooks, distribution boundaries, and test expectations.
version: 0.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags:
    related_skills:
    skill_group: rebirthuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
---
# UO Item Property Review

## Overview

Use this skill when reviewing, triaging, or planning Ultima Online item-property work for RebirthUO/ModernUO. It keeps property work separated into source evidence, era/ruleset, storage container, tooltip/client presentation, gameplay effect, distribution/economy rollout, and tests.

## When to Use

- A RebirthUO issue asks for a magic item property, weapon property, armor property, negative property, artifact property, or tooltip/property-list change.
- A property appears in UO.com Magic Item Properties, UOGuide, Stratics, ServUO, or local RebirthUO containers and needs era/container placement.
- The change may touch `AOS.cs`, `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, loot/runic/reforging/imbuing, combat, buffs, or property lists.

## Procedure

1. **Classify the source evidence.** Prefer UO.com for current official wording, then UOGuide/Stratics for mechanics/history, then issue evidence, then repo evidence. Use ServUO only for comparison constants or implementation clues, not as official parity proof. For behavior-sensitive comparison claims, pin the exact ServUO/RunUO revision or commit and inspect the relevant source lines; do not treat “ServUO” as one stable behavior when revisions disagree.
2. **Separate property surfaces.** Treat storage, tooltip, gameplay effect, and distribution as separate decisions. A property can be implemented for GM/test use without adding it to loot, runics, reforging, imbuing, artifacts, or vendors.
3. **Choose the era/container deliberately.** Check whether the property belongs in an existing AoS, SA, absorption, defensive, or extended/modern container. Do not choose a container just because a similar implementation exists; match the property's era and product source.
4. **Map repo anchors.** Identify the existing container enum/class, owning item class, `GetProperties` block, gameplay hook, save/migration surface, and focused test file before calling a ticket implementable.
5. **Verify tooltip/client data.** Prefer known clilocs, but mark cliloc IDs as candidates until checked against local client data or existing repo tests. For Classic client files, check the file header first; if it is BWT-compressed, decode it with the repository's `BwtDecompress.Decompress` and `Localization.LoadClilocs` format rather than treating it as ordinary cliloc records. Record the exact resolved text and keep client verification separate from the property-list/OPL decision.

   A practical verification sequence is: locate the configured `Cliloc.enu`, inspect the first six bytes, port or invoke the repository decompressor, parse `(number, flag, length, UTF-8 text)` records, and assert the candidate number's exact text. This turns a ServUO cliloc candidate into client-data evidence without claiming that engine precedent proves official mechanics.
6. **Define gameplay exactness.** For proc properties, specify chance formula, trigger timing, excluded abilities/special moves, PvP/PvM differences, immunity/cooldown/stacking, durability/resource effects, and cleanup.
7. **Guard the economy.** If UO.com says `(L)` or lists found-on items, that is evidence for a future distribution ticket, not automatic permission to change loot generation in a storage/gameplay ticket.
8. **Require focused tests.** Cover era gate, tooltip, effective aggregation, normal trigger, exclusions, cleanup, and non-distribution guard. Label focused tests honestly; do not call them broad-suite green.

## Caddellite Infused Khaldun marker note from session research

When reviewing `Caddellite Infused`, `Mask of Khal Ankur`, `Pendant of Khal Ankur`, `Cultist's Ritual Tome`, Treasures of Khaldun, or Khal Ankur tickets, read `references/caddellite-infused-khaldun-marker.md` before choosing a container. Treat `Caddellite Infused` as a Publish 101 / Dynamic Treasures Khaldun event marker, not a normal AoS/SA magic item property. It should not be added to `AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, SA containers, random loot, runics, reforging, or imbuing as a rollable property. If event mechanics are in scope, plan a persistent content marker plus tooltip cliloc `1158662`, Khaldun damage-gate checks, harvest/craft infusion, and explicit distribution boundaries. For isolated Mask/Pendant parity, the tooltip line can be fixed artifact presentation, but the mechanics are incomplete until Khaldun event damage gating exists.

## Craft Exceptional Bonus talisman note from session research

When reviewing or implementing `Craft Exceptional bonus`, read `references/craft-exceptional-bonus-talisman-review.md` before planning storage or tests. Treat it as a talisman-specific ML crafting property (`Skill` + `ExceptionalBonus` on `BaseTalisman`), not a generic AoS/SA attribute. The key review traps are: UO.com `(L)` does not authorize loot/runic/imbuing rollout; UOGuide says the bonus does not unlock `0%` exceptional chance; `SuccessBonus` must not double-increase exceptional chance; and Smith/Tailor BOD eligibility uses the same `GetExceptionalChance()` path and should be called out as a side effect.

## Bane note from session research

When reviewing or implementing `Bane`, read `references/bane-item-property-review.md` before choosing storage, era gate, or tests. Treat Bane as a post-AoS weapon-only on-hit property with canonical UO.com evidence for `Weapons (L)`, `No` imbue weight, target HP below 50%, 30% target-max-HP physical damage, and the Publish 83 350 raw physical damage cap. UOAlive/ServUO provide pre-resist cap wording, HP-scaling example values, ServUO extended-weapon precedent, and cliloc candidate `1154671`; treat those as community/engine evidence until local RebirthUO review accepts them. Keep distribution separate from storage/tooltip/mechanics.

## Bone Breaker revision-drift note

When reviewing or drafting `Bone Breaker`, read `references/bone-breaker-publish96-revision-drift.md`. Keep UO.com mechanics separate from ServUO comparison values, pin the exact ServUO revision, and surface immunity/Tactics branch drift instead of making an unqualified engine-behavior claim.

## Casting Focus note from session research

When reviewing or implementing `Casting Focus`, read `references/casting-focus-sa-review.md` before choosing storage, host surfaces, tooltip, or tests. Treat the normal/current property as a Stygian Abyss caster defensive interruption-resist property: UO.com lists intensity `1-3`, imbue weight `No`, found on `(R)(L)Armor`, total cap `12%`, and description `A chance to resist interruptions while casting spells`. UOGuide/ServUO show artifact/special examples up to `4%` and non-armor hosts; treat those as named-artifact/special-item parity, not automatic distribution. Prefer a neutral absorption-family container if implementing the broader eater/resonance/focus family, gate tooltip/effect with `Core.SA`, roll in `Spell.OnCasterHurt` before `Disturb(DisturbType.Hurt, ...)`, preserve Protection behavior, and keep loot/runic/imbuing/Fish Pie/mastery bonuses out unless explicitly scoped.

## Focus note from session research

When reviewing or implementing `Focus`, read `references/focus-item-property-research.md` before choosing the era, damage hook, progression sequence, or distribution scope. Treat it as a High Seas / Publish 71 weapon hit property distinct from `Casting Focus` and `Spell Focusing`: canonical UO.com defines a `-50%` to `+20%` same-target cycle and target-change reset, while ServUO's `-40` / `+10` / `+8` precedent is implementation evidence only and conflicts with the canonical starting point. Keep intermediate progression and the exact successful-hit boundary explicit review decisions, use lifecycle-safe transient state, and keep `(L)` loot distribution separate from storage/gameplay work.

## Searing weapon review note

When reviewing or implementing `Searing`, read `references/searing-weapon-review.md` before choosing storage, era gate, activation state, combat timing, or tests. Treat UO.com's current row as canonical for the active context-menu surface, every-active-attack mana cost, 20% melee / 10% ranged proc chance, four direct self-damage, and the four-second player/NPC regeneration penalties. The official row does not quantify extra fire damage or lifecycle/reapplication semantics. Do **not** copy the pinned ServUO 10–15 comparison value as EA fidelity: its mana debit occurs only in its successful-proc branch and conflicts with the official every-attack cost. Keep `triage` until primary evidence or an explicit maintainer policy resolves the missing fire value, insufficient-mana/active-state lifecycle, debuff refresh/stack/immunity, and formal era gate. Keep acquisition, Brittle/200-durability source content, loot, runics, reforging, imbuing, and vendors out of the first property/mechanics slice.

## Spell Focusing Sash note from session research

When reviewing or implementing `Spell Focusing` / `Spell Focusing Sash`, read `references/spell-focusing-sash-review.md` before choosing sequence behavior, state persistence, clothing/Brittle handling, or tests. Treat it as a special event sash property, not Casting Focus and not a rollable clothing/armor property. Prefer UO.com's table order (`-30%` then `+6%` steps to `0%`, then `+2%` to PvP/PvM caps) over conflicting UOGuide/ServUO order unless live-client evidence proves otherwise. Keep target/count transient, advance at the single-target spell damage hook, and do not broaden clothing negative-property or loot distribution in the same ticket.

## Splintering Weapon note from session research

When reviewing or implementing `Splintering Weapon`:

- UO.com Magic Item Properties lists intensity `5–30`, imbue weight `No`, found on `Weapons (L)`, cap `N/A`, bleed + forced-walk, stack/extend with Bleed Attack, substantial durability compromise, 15s player immunity to Splintering bleed/forced-walk, and no processing with Disarm/Infectious Strike/Injected Strike.
- UO.com Publish 96 confirms the Disarm bugfix.
- UOGuide confirms bleed, **4s forced walking**, stack with Bleed Attack, and SA/artifact examples such as Staff of Shattered Dreams, Sword of Shattered Hopes, and Brightblade, commonly at `20%`.
- Prefer the current branch's chosen weapon-property overflow container with `Core.SA` gating. On current RebirthUO/ModernUO `origin/main`, no `SaWeaponAttributes` container exists; `ExtendedWeaponAttributes` already hosts SA weapon properties such as Battle Lust and Blood Drinker alongside TOL/post-TOL properties. Do **not** infer a TOL/post-TOL era from the Publish 96 Disarm bugfix; Splintering Weapon remains SA-era unless stronger source evidence says otherwise.
- `Weapons (L)` is a distribution fact, not automatic approval to enable loot/runic/reforging/imbuing/artifact rollout in the same ticket.
- ServUO comparison hints: cliloc candidate `1112857`, `BuffIcon.SplinteringEffect`, 4s context, player bleed immunity roughly 15/16s, and durability reduction around `HitPoints = Math.Max(0, HitPoints - 10)`. Treat these as implementation clues, not official parity proof.
- Do not copy the Sparks/Swarm all-special-move exclusion pattern. Splintering source exclusions are named: Disarm, Infectious Strike, Injected Strike. If Injected Strike does not exist locally, leave a source-commented TODO or add the exclusion when the move exists.
- Focused tests should cover SA/pre-SA aggregation, tooltip, 100% proc, Disarm/Infectious exclusions, no blanket special-move exclusion, 4s forced-walk cleanup, 15s player immunity, bleed stack/extend behavior, durability loss, transient context cleanup, and no accidental distribution.

## Brittle note from session research

When reviewing or implementing `Brittle`:

- UO.com Magic Item Properties lists intensity `N/A`, imbue weight `No`, found on `(R)(L) Armor, Weapons, Shields`, cap `N/A`, and the core rule: Brittle items cannot have Powder of Fortification applied, but can be repaired.
- UO.com Publish 74 introduces the first Brittle surface through Runic Re-Forging: `Structural Re-Forging` makes the item Brittle; `Fortified Re-Forging` creates a Brittle item with higher durability. Treat this as generation-time durability, not permission for powder to work later.
- UO.com Publish 86 extends negative item properties to global loot, states Brittle-spawned items default to max durability 255, and states items have at most one negative property. Use Publish 74 as initial publish, with Publish 86 as the loot-generation extension.
- UOGuide confirms `Brittle` prevents fortification/durability increase and that Publish 74 introduced Runic Re-Forging.
- Prefer the shared negative-property container/flag model planned for `Prized`; do not put Brittle into positive AoS stat containers just because ServUO has legacy `AosAttribute.Brittle` compatibility.
- ServUO comparison hints: `NegativeAttribute.Brittle`, tooltip cliloc `1116209`, and powder rejection message `1149799` (`That cannot be used on brittle items.`). Treat these as engine/client-data clues until verified locally.
- RebirthUO anchors from the ModernUO worktree: `PowderOfTemperament` currently checks `IDurability.CanFortify`; `Repair.cs` handles weapon/armor repair and should not block Brittle; `BaseWeapon`/`BaseArmor` property-list methods need the tooltip row. Keep clothing/jewelry/talisman out unless a separate source/shard-policy decision expands the found-on surface.
- First implementation should normally be storage + tooltip + powder rejection + repair-allowed tests only; keep Runic Re-Forging and Publish 86 loot distribution as separate economy/generation work unless explicitly scoped.

## Antique note from session research

When reviewing or drafting `Antique`, read `references/antique-item-property-review.md` before choosing storage, host families, combat-decay hooks, powder behavior, enhancement restrictions, or jewelry lifecycle scope. Treat UO.com as canonical for the property row and Publish 86 family; treat UOGuide's active-combat wording, 255/255 initial durability, and cannot-enhance rule as community evidence; treat ServUO's multiple decay paths and cliloc `1076187` as engine/client clues only. Antique is officially found on armor, jewelry, weapons, and shields, but the current ModernUO jewelry class is not on the `IDurability`/`IWearableDurability` combat path and the current repair engine has no jewelry branch. Keep jewelry out of powder eligibility, document the unresolved decay formula, and keep random-loot/Runic Re-Forging distribution separate from the first storage/mechanics slice.

## Blood Drinker note from session research

When reviewing or implementing `Blood Drinker`, read `references/blood-drinker-sa-review.md` before choosing storage, era gate, or Bleed Attack hooks.

- UO.com: fixed presence, imbue `No`, `Weapons (L)`; bleed damage from successful Bleed Attack transfers to attacker health; Publish 60 lists `Life Syphon` with Blood Drinker.
- Coupled to **successful** Bleed Attack only; snapshot property at bleed apply; heal from defender HP delta per tick when `Mobile.Damage` returns void.
- On `origin/main`, prefer `ExtendedWeaponAttributes` with `Core.SA` (same family as Battle Lust), not blind copy of ServUO `AosWeaponAttribute` bits — re-check next free `ExtendedWeaponAttribute` value at implementation time.
- Cliloc candidates: `1113591` (tooltip), `1113606` (heal message). Life Syphon / Vampiric Essence / `(L)` loot are non-blocking follow-ups.

## Soul Charge note from session research

When reviewing or implementing `Soul Charge`, read `references/soul-charge-sa-review.md` before choosing storage, tooltip, damage-pipeline hooks, or tests. Treat Soul Charge as an SA-era shield-only defensive damage-taken proc: UO.com lists intensity `5–30`, imbue weight `No`, found on `Shields (R)(L)`, total cap `50`, and Publish 60 named shield examples at `20%` and `30%`. Prefer `Core.SA`, equipped `BaseShield` host checks, and actual post-resist HP damage as the conversion basis; ServUO supports property-value percent chance, 30% damage-to-mana conversion, and message cliloc `1113636`, while Fish Pie's 50% modifier remains a separate follow-up unless explicitly scoped. Keep `Shields (R)(L)` as distribution evidence only, not automatic loot/runic rollout.

## Damage Eater note from session research

When reviewing or implementing `Damage Eater` / eater-family properties, read `references/damage-eater-sa-review.md` before choosing host surfaces, storage, tooltip clilocs, delayed-heal context, or tests. Treat Damage Eater as a Publish 60 / SA defensive incoming-damage conversion family. Current UO.com supports Armor/Shields, intensity `3–15`, imbue `No`, 30% specific cap, 18% all-damage cap, 20 pending charges, and three-second delayed conversion; UOGuide/ServUO conflict by showing weapon hosting/older ranges, so default to current UO.com unless maintainers choose legacy/custom parity. Prefer a neutral absorption-family container, use `Core.SA`, base math on actual/post-resist damage, enforce non-additive all-damage vs specific behavior, and keep distribution out of the first storage/gameplay slice.

## Reactive Paralyze note from session research

When reviewing or implementing `Reactive Paralyze`:

- UO.com Magic Item Properties lists fixed intensity `N/A`, imbue `No`, `Shields (R)(L)` and `2 handed weapons (R)(L)`, cap `N/A`, and a chance to paralyze the attacker after the wielder parries the blow.
- UO.com Publish 60 (September 8, 2009, Stygian Abyss) lists Reactive Paralyze under `New Item Properties` and on the Boura Tail Shield. UOGuide independently identifies a fixed **30%** chance and describes the effect as casting the Magery Paralyze spell.
- ServUO comparison precedent stores presence bits on both armor and weapon property surfaces, triggers only in the successful-parry branch, uses 30%, and displays cliloc `1112364`. Its direct duration formula differs from normal spell routing: `max(1, max(8, wielder EvalInt / 10) - attacker Magic Resist / 10)` with no explicit PvM multiplier.
- Local EA Classic client data verified `1112364` (`reactive paralyze`) and `1154660` (`Reactive Paralyze`). Prefer `1112364` for equipped-item OPL unless client testing proves otherwise; `1154660` appears in ServUO property metadata/gump use.
- For RebirthUO, use `Core.SA`, trigger only after the existing `BaseWeapon.AbsorbDamageAOS` successful block, support equipped shields and two-handed parry-capable non-ranged weapons, and keep loot/Runic Re-Forging/artifact distribution separate from storage + tooltip + mechanics.
- Document the unresolved duration/reapplication conflict instead of silently copying ServUO: canonical UO.com does not quantify it, UOGuide says Magery Paralyze, while ServUO uses property-specific direct paralysis. A conservative default is the target repo's normal SA Paralyze semantics unless maintainers choose explicit ServUO compatibility.

## Assassin Honed / Balanced Publish 74–81 note

When reviewing or implementing `Assassin Honed` or two-handed-melee `Balanced`, read `references/assassin-honed-balanced-publish74-81.md` before choosing the era gate, storage, combat hook, or scope. Use Publish 74 (2012-01-31) and Publish 81 (2013-04-16) as primary introduction evidence. Preserve the official same-direction wording for Assassin Honed by masking and comparing directions at the successful-hit boundary; use the ServUO `floor(146 / MlSpeed)` amount only as an explicitly-labelled EA-clone fallback because official material does not publish a coefficient. For Balanced, preserve the separate serialized ranged field and add a distinct melee representation queried through a shared helper; the existing potion and evasion paths make the required anchors explicit. Treat the official `(I)` acquisition marker as a separate blocker when conventional Imbuing infrastructure is absent—runtime/storage parity is not approval to fabricate an acquisition path.

## Last Parry Chance runtime display note

When reviewing or drafting `Last Parry Chance`, treat it as runtime client-presentation state, not a persistent or rollable item property. Cross-check `uo-aos-item-properties/references/last-parry-chance-runtime-tooltip.md` before planning storage or tests. UO.com lists imbue weight `No`, found on shields/weapons, and says the item displays the last parry chance after players parry an attack; ServUO precedent stores transient `LastParryChance` on `BaseWeapon`/`BaseShield`, uses cliloc `1158861`, and clears it on removal. For RebirthUO issue bodies, explicitly note that the current item-property template does not have a perfect `Runtime` property-type option; do not force it into AoS/SA/negative/extended storage, and keep loot/runic/reforging/imbuing/artifact distribution out of scope. Important review decisions are whether the displayed percentage should be the actual successful formula branch versus exact ServUO behavior, and whether tooltip display should be `Core.EJ` gated for client compatibility.

## Swarm Publish 96 weapon-property note

When reviewing or implementing `Swarm`, treat it as a Publish 96 / Dungeon Doom Update weapon hit property gated practically by `Core.TOL` unless a finer publish/custom gate exists. UO.com Magic Item Properties lists `N/A` intensity, imbue `No`, `Weapons (L)`, cap `N/A`, physical damage over time, fire damage or torch counterplay, and no activation with special moves. UO.com Publish 96 confirms Dungeon Doom / Worldwide Release 2017-02-09 but does not quantify tick cadence, duration, or raw damage. Use ServUO only as engine precedent for cliloc `1157325`, `BuffIcon.Swarm`/candidate buff clilocs, effects, and a conservative default if needed; prefer canonical physical damage over ServUO's direct-damage tick unless maintainers intentionally choose custom behavior. On current RebirthUO/ModernUO `origin/main`, `ExtendedWeaponAttributes` already hosts `BloodDrinker = 0x00000008`; Swarm should use the next safe bit at implementation time and must not reuse sibling property bits. Keep random loot, Doom rewards, runics, reforging, imbuing, and artifact distribution out of the first storage/gameplay slice unless a separate economy ticket authorizes rollout. Focused tests should cover TOL/pre-TOL tooltip and activation, normal-hit-only trigger, duplicate/context cleanup, physical mitigation, positive post-resist fire cleanup, burning torch cleanup, and distribution guards.

## Toxic Weapon / Publish 121 note from session research

When reviewing or drafting `Toxic Weapon`, read `references/toxic-weapon-publish-121-review.md`. Treat it as current live/post-TOL production-shard content introduced with Publish 121's Draconic Awakening event, not New Legacy. Preserve UO.com's `N/A` intensity, `No` imbue weight, `Weapons (L)` distribution marker, and context-menu activation wording. Keep the undocumented poison-damage/debuff formula, state lifecycle, PvP behavior, and distribution rollout visible as decisions; do not infer Toxic Weapon from separate `Hit Poison Area`, elemental `Poison Damage`, weapon poison charges, or `ApplyPoison`. The repository's current latest gate is `Core.EJ`; the issue form has no `EJ/current live` option, so document that mismatch rather than inventing `Core.NL`.

## Ward Removal note from session research

When reviewing or implementing `Ward Removal`, read `references/ward-removal-review.md` before choosing host surface, era, or scope. Treat it as an active-use special talisman property associated with the Britain Library `Talking to Wisps` talisman, not a generic AoS stat or normal imbuing roll. The current item-property issue template has no `Talismans` or `Active/Usable` option; document the canonical host/type mismatch explicitly instead of misclassifying it. RebirthUO already has partial generic support in `BaseTalisman`: `TalismanRemoval.Ward`, target validation, recharge/charge flow, and removal of Magic Reflection, Reactive Armor, and Protection. First-pass issue/implementation scope should add the concrete item and focused tests while preserving that storage path, Trammel's Publish 54 friendly-player restriction, and the separation from Mysticism `Purge Magic`. UO.com's broad “any protective spells” wording conflicts with UOGuide's “up to six wards” and ServUO's additional Eodonian potion removal; keep the narrow local spell-helper set as the conservative default and record broader categories as follow-up policy.

### Active properties that remove or negate target effects

Treat a target effect as adverse based on its gameplay consequence, not merely on whether it removes a nominally beneficial buff or ward.

1. Inspect the concrete `Target` constructor and its callback separately. `TargetFlags.Beneficial` controls target-cursor classification; it is not authorization and does not make an adverse removal effect legally beneficial.
2. Determine whether an other-mobile target must use the established harmful permission/action path (`CanBeHarmful`, `HarmfulCheck`, `DoHarmful`, or the shard-equivalent helper). Record exactly when this check occurs relative to effect application, charge consumption, cooldown/recharge callbacks, and feedback effects.
3. Prefer the shard's existing harmful rules over a bespoke facet check such as `Map.Trammel`. The common path usually incorporates region/safe-zone, duel, guild, pet, PvP-feature, notoriety, criminality, and facet rules.
4. Decide self-target behavior explicitly. Self may be legal while harmful-action bookkeeping, criminality, aggression, and combatant assignment must not occur.
5. If a shared item target serves multiple property types, preserve the existing behavior for the others. Add a property-specific branch rather than globally changing target flags or Curse/Damage/etc. behavior.
6. Add focused tests for:
   - a denied target: no effect and no charge/cooldown consumption or restart;
   - a legal hostile target: normal harmful-action accounting where intended;
   - self-targeting;
   - unchanged behavior for sibling property/removal types.

See `references/ward-removal-review.md` for the concrete Ward Removal evidence, repo anchors, and the Publish 54 Trammel restriction.

## Bestial Suit / Berserk source-conflict note

When reviewing or planning the Bestial Suit `Berserk` property, read `references/bestial-berserk-publish75-review.md`. The official Publish 75 page contains both an eight-second Bestial-section wording and a later five-second Bug Fixes wording, while its current property row and UOGuide mirror eight seconds. Keep `triage` until maintainers resolve the duration, numeric mitigation/healing values, concrete suit host, and healing-path coverage. Treat `Core.HS` only as a post-High-Seas repository-gate candidate, and keep content/distribution separate from the transient mechanics slice.

## Scope gate: property-only versus reusable mechanics

For the PR-history/base-branch correction workflow, read `references/reusable-property-pr-scope-correction.md` before editing an existing PR. A reusable property/mechanic may already be present in the current base through a merged predecessor PR; in that case, do not duplicate production code just to make the follow-up diff look substantive. Remove only the premature named item/artifact surface, add generic regression coverage with an existing compatible item, and make the PR body/title describe the resulting scope honestly.

Before editing, split the request into four independent surfaces: storage, tooltip/client presentation, gameplay mechanics, and distribution/acquisition. Confirm which surfaces are explicitly in scope; do not infer the others from the source description or from a reference implementation.

Resolve the common ambiguity explicitly: **“no concrete item” does not mean “no gameplay handling.”** A ticket may require storage + tooltip + reusable mechanics while still forbidding a named sash/artifact. In that case, implement the property on an existing generic container, discover it on any equipped compatible item, and put the effect behind a central hook. Do not make the runtime depend on a specific item class.

For a **storage + tooltip only** request:

- Add only the smallest existing property-container representation and its property-list output.
- Do not create the named artifact/item class merely because the property is associated with one.
- Do not add spell/combat hooks, buffs, context menus, lifecycle/reset state, era mechanics, loot, rewards, vendors, runics, reforging, or imbuing.
- Do not add tests for out-of-scope mechanics; test only storage, tooltip output, and the requested era/presentation gate.
- Treat a reference implementation that contains the full item and runtime system as evidence for names/clilocs only, not as the task boundary.

For a **reusable property + mechanics** request:

- Keep storage/tooltip and runtime behavior separate in the diff; no concrete artifact/item is required.
- Define the eligible effect surface explicitly (for example, direct single-target spells rather than every spell damage call) and expose a central opt-in/eligibility seam instead of scattering unbounded heuristics.
- Find any equipped compatible item carrying the property; specify multiple-property behavior, target changes, sequence limits/caps, era gates, delayed damage, death/logout/deletion cleanup, and transient-state ownership before coding.
- Put transient sequence state with the generic property owner or a lifecycle-safe context; never serialize active target/count state.
- Add a test using an ordinary existing item with the property, not the named source artifact, and cover at least application, target/owner reset, and the central hook path.
- Keep loot/acquisition/distribution separate unless explicitly requested.

Before commit or PR update, compare the changed-file list against the scope matrix. A property-only diff must not touch individual spells, central combat damage paths, lifecycle systems, loot/distribution code, or add a new item class. If the user later expands the request to include reusable mechanics, update the scope matrix and allow only the minimal central hook plus explicit eligibility seams; do not silently revert to the full artifact implementation.

## Pitfalls

- Do not treat UO.com `(L)` as approval to enable random loot in the same ticket as storage/gameplay.
- Do not copy the exclusion policy from a different property. Some properties exclude all special moves; others exclude only named moves.
- Do not put SA properties into a TOL/extended container merely because later publish notes mention bugfixes.
- Do not rely on ServUO as canonical behavior. It is useful for likely clilocs, buff IDs, durations, and comparison test values only after UO.com/UOGuide source framing is done.
- Before assigning weapon-property bits, inspect `ExtendedWeaponAttribute` / `SaWeaponAttributes` on `origin/main` (`git show origin/main:Projects/UOContent/Misc/AOS.cs`); stale issue text may cite the wrong enum or ServUO-only bit maps.
- Do not add serialized active effect state for transient hit effects; use timers/contexts with cleanup.

## Verification

A review is complete when it includes source URLs and what each proves, era/ruleset and container decision, repo paths/classes/methods to change, explicit distribution decision, test values and focused/broad validation plan, and PvP/PvM/economy/save/client/performance risks.
