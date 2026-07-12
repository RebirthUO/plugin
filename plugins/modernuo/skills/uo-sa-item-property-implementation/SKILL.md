---
name: uo-sa-item-property-implementation
description: Use when implementing Stygian Abyss-era item properties in RebirthUO/ModernUO, especially SA weapon/armor properties that need storage, tooltip, gameplay hooks, runtime timers, distribution boundaries, and focused tests.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    related_skills:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
---
# UO SA Item Property Implementation

## Overview

Use this class-level skill when an implementation-ready RebirthUO issue asks for a Stygian Abyss item property to move from review into code. It complements `uo-aos-item-properties` by focusing on the recurring SA implementation shape: `Core.SA` gates, tooltip clilocs, gameplay hooks, runtime-only contexts, explicit distribution boundaries, and container choices that still treat AoS as the underlying item-property system.

Always verify current repo source and the issue review first. This skill records implementation patterns, not a license to infer mechanics or economy rollout. Before naming or adding a container, read `uo-aos-item-properties/references/aos-property-container-taxonomy.md`: prefer mechanic/family names over expansion labels unless an expansion-named container is deliberately justified.

## Procedure

1. **Confirm implementation readiness.** Require target era/ruleset, item family, source evidence, cliloc/tooltip behavior, gameplay formula, caps, acceptance criteria, and explicit non-goals.
2. **Keep storage separate from distribution.** Adding storage/tooltip/gameplay must not add loot, runic, imbuing, artifact, or generation-table rollout unless the ticket explicitly includes that economy decision.
3. **Use the right container.** Do not default to expansion-named storage such as `SaWeaponAttributes`. AoS is the magic-property system; SA is usually the per-property activation gate. Prefer existing AoS containers when semantics and bit capacity fit, or a neutral mechanic/family overflow container (for example `AosExtendedWeaponAttributes` / `ExtendedWeaponAttributes` for weapon overflow, `AosAbsorptionAttributes` / `AbsorptionAttributes` for eater/casting-focus families). Add a new enum bit and `[CommandProperty(AccessLevel.GameMaster)]` wrapper; avoid new persistent `BaseWeapon` fields unless storage cannot fit a container model.
4. **Gate all behavior by era.** Tooltip and gameplay consumers should be `Core.SA`-gated. Tests need a pre-SA control proving storage is inert and tooltip/effect are absent.
5. **Hook gameplay in the owning pipeline.** Weapon outgoing damage belongs in `BaseWeapon.OnHit`; damage-taken/gain behavior belongs after `AOS.Damage` computes applied positive damage; hit-effect chances belong beside existing SA/AoS hit-effect helpers.
6. **Runtime contexts are runtime-only.** Timed points, cooldowns, decay, immunities, and active effects should use cancellable timers and cleanup paths, not serialized fields, unless the issue explicitly requires save persistence.
7. **Test behavior, not static lists only.** Add tests that instantiate items/mobiles, set the property, drive the real helper/pipeline seam, inspect tooltip entries or state, and cover era controls, caps, cooldowns/decay, and cleanup.
8. **Validate with build and focused tests.** For `UOContent.Tests`, set `MODERNUO_TEST_DATA_DIR` / `MODERNUO_CLIENT_PATH` to a folder containing `tiledata.mul` when the fixture requires client data. If Hermes' verification guard fires after commit/PR, use `modernuo-verification-guard` and run a fresh `hermes-verify-*` script; do not cite stale logs.

## Battle Lust reference pattern

Battle Lust is a canonical SA weapon-property example:

- Source anchors from ticket review: UO.com Magic Item Properties is canonical for `N/A` intensity, `No` imbue weight, `Weapons (R)(L)`, 45 PvP / 90 PvM caps, 2s gain cadence, and 6s decay. UO.com Publish 60 / Stygian Abyss launch anchors initial publish and lists `Blade of Battle` / `Storm Caller`; UO.com SA artifacts add `Axe of Abandon`, `Blade of Battle`, `Claws of the Berserker`, `Storm Caller`; Publish 68 / High Seas adds `Smiling Moon Blade`. UOAlive mirrors mechanics and item examples. Stratics wiki search result exists but is a stub/inaccessible behind Cloudflare, so do not use it as a mechanics authority.
- Property storage: use the current branch's chosen weapon-property container. Historical branches may use `SaWeaponAttributes.BattleLust`; new/container-cleanup work should prefer a neutral extended weapon-property container with `Core.SA` gates.
- Tooltip: cliloc `1113710`, no argument; verify against local client data/property-list tests during implementation.
- Gain: after final applied incoming `AOS.Damage` of at least 30 from another living mobile; exclude self/null/environmental/dead/deleted sources. Do not limit to melee only for the first slice if the damage path goes through `AOS.Damage` with a living source.
- Gain cadence: at most one point per 2 seconds.
- Decay: one point every 6 seconds; remove context at 0.
- Cap: points capped at 15. Do not copy ServUO's apparent `Bonus < 16` off-by-one as the gameplay rule; UO.com/UOAlive support 15% per opponent.
- Damage bonus: `min(points * attacker.Aggressed.Count, defender.Player ? 45 : 90)` before the existing global percentage cap.
- Aggression count: use RebirthUO/ModernUO `Mobile.Aggressed` as the relationship source of truth; do not add pet/summon-specific filters without separate PvP review.
- Cap coupling review: the 45 PvP / 90 PvM Battle Lust caps are property-specific unless repo evidence shows a shared mechanic; do not couple them to the global weapon `percentageBonus` cap (`300`) or the ML direct-damage/Death Strike cap (`35/70`).
- Tests may intentionally assert literal Battle Lust expected values (15 points, 45/90 caps) rather than reusing production constants, because they document the gameplay rule and catch accidental rule changes.
- Cleanup: no bonus if the effective weapon/property is removed, mobile is dead/deleted, or era is pre-SA.
- Distribution: UO.com supports `Weapons (R)(L)` and loot-generation theme evidence, but do not add loot/runic/imbuing/artifact rollout in the storage/gameplay PR.

## Pitfalls

- When reviewing “hardcoded” SA property values, first search for existing shared caps/constants in the repo and classify the cap layer: property-specific cap, global weapon percentage cap, direct-damage cap, or era/ruleset cap. Only suggest centralization when the same gameplay rule is duplicated, not merely because two mechanics both mention PvP/PvM.
- Do not implement under-specified SA mechanics from the UO.com magic-property table alone; require review/source evidence for thresholds, caps, and timing.
- Do not confuse tooltip-only/runtime state rows with persistent rollable properties.
- Do not place post-ToL/Publish 96 properties into an SA-named container just because they are weapon properties. Prefer a neutral extended weapon-property container with per-property era gates, so SA and TOL properties can share storage mechanics without implying the wrong source era.
- Do not call focused SA property tests broad-suite green unless the broad project suite actually ran.
- Do not leave timer contexts with stale `Mobile`/`Item` references; add clear helpers for tests and invalidation paths for lost equipment.

## Defensive incoming-damage property review pattern

For SA defensive properties that consume incoming damage, review every damage-pipeline branch—not only the ordinary resist path:

1. Trace typed portions through normal damage, `ignoreArmor`, direct-damage, PvP caps, quiver/bonus damage, barding, and keep-alive paths. Armor Ignore must preserve the supplied physical/fire/cold/poison/energy portions; do not silently classify typed Armor Ignore damage as direct damage.
2. Verify that values passed to the property are post-resist and normalized against the actual applied hit delta. Add at least one test for each supported type and one mixed/Armor Ignore case.
3. For delayed-charge contexts, test cadence when the queue is not full **and** when it is at `MaxCharges`. A “three seconds from last damage” rule must reset on later eligible damage even if the new event cannot enqueue another charge.
4. Treat a focused property test pass as insufficient if it omits a pipeline branch; inspect the call site and add a regression test for every branch that can change damage classification.

## Verification Checklist

- [ ] Era/ruleset and source decision are explicit.
- [ ] New property bit uses the next safe free bit in the correct container.
- [ ] GM property wrapper exists.
- [ ] Tooltip cliloc appears only in the target era.
- [ ] Gameplay hook is in the owning pipeline and uses applied damage where required.
- [ ] Normal, Armor Ignore, direct, and mixed damage branches preserve matching type information.
- [ ] Queue-full damage still resets a last-damage delayed-heal cadence.
- [ ] Runtime timers/tokens are cancelled or removed on context cleanup.
- [ ] Tests cover positive behavior, pre-era no-op, formula/caps, timing/cooldown/decay and queue-full cadence, and cleanup.
- [ ] Distribution surfaces remain unchanged unless explicitly scoped.
