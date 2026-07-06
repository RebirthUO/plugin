---
name: uo-sa-item-property-implementation
description: Use when implementing Stygian Abyss-era item properties in RebirthUO/ModernUO, especially SA weapon/armor properties that need storage, tooltip, gameplay hooks, runtime timers, distribution boundaries, and focused tests.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ultima-online, modernuo, rebirthuo, stygian-abyss, item-properties, implementation]
    related_skills: [uo-aos-item-properties, uo-item-property-review, uo-combat-pipeline, modernuo-test-workflow, modernuo-verification-guard]
---
# UO SA Item Property Implementation

## Overview

Use this class-level skill when an implementation-ready RebirthUO issue asks for a Stygian Abyss item property to move from review into code. It complements `uo-aos-item-properties` by focusing on the recurring SA implementation shape: separate SA containers, `Core.SA` gates, tooltip clilocs, gameplay hooks, runtime-only contexts, and explicit distribution boundaries.

Always verify current repo source and the issue review first. This skill records implementation patterns, not a license to infer mechanics or economy rollout.

## Procedure

1. **Confirm implementation readiness.** Require target era/ruleset, item family, source evidence, cliloc/tooltip behavior, gameplay formula, caps, acceptance criteria, and explicit non-goals.
2. **Keep storage separate from distribution.** Adding storage/tooltip/gameplay must not add loot, runic, imbuing, artifact, or generation-table rollout unless the ticket explicitly includes that economy decision.
3. **Use the right container.** For SA weapon properties, prefer the existing `SaWeaponAttributes : BaseAttributes` pattern when present. Add a new enum bit and `[CommandProperty(AccessLevel.GameMaster)]` wrapper; avoid new persistent `BaseWeapon` fields unless storage cannot fit the container model.
4. **Gate all behavior by era.** Tooltip and gameplay consumers should be `Core.SA`-gated. Tests need a pre-SA control proving storage is inert and tooltip/effect are absent.
5. **Hook gameplay in the owning pipeline.** Weapon outgoing damage belongs in `BaseWeapon.OnHit`; damage-taken/gain behavior belongs after `AOS.Damage` computes applied positive damage; hit-effect chances belong beside existing SA/AoS hit-effect helpers.
6. **Runtime contexts are runtime-only.** Timed points, cooldowns, decay, immunities, and active effects should use cancellable timers and cleanup paths, not serialized fields, unless the issue explicitly requires save persistence.
7. **Test behavior, not static lists only.** Add tests that instantiate items/mobiles, set the property, drive the real helper/pipeline seam, inspect tooltip entries or state, and cover era controls, caps, cooldowns/decay, and cleanup.
8. **Validate with build and focused tests.** For `UOContent.Tests`, set `MODERNUO_TEST_DATA_DIR` / `MODERNUO_CLIENT_PATH` to a folder containing `tiledata.mul` when the fixture requires client data. If Hermes' verification guard fires after commit/PR, use `modernuo-verification-guard` and run a fresh `hermes-verify-*` script; do not cite stale logs.

## Battle Lust reference pattern

Battle Lust is a canonical SA weapon-property example:

- Property storage: `SaWeaponAttributes.BattleLust`.
- Tooltip: cliloc `1113710`, no argument.
- Gain: after applied incoming `AOS.Damage` of at least 30 from another living mobile.
- Gain cadence: at most one point per 2 seconds.
- Decay: one point every 6 seconds; remove context at 0.
- Cap: points capped at 15.
- Damage bonus: `min(points * attacker.Aggressed.Count, defender.Player ? 45 : 90)` before the existing global percentage cap.
- Cap coupling review: the 45 PvP / 90 PvM Battle Lust caps are property-specific unless repo evidence shows a shared mechanic; do not couple them to the global weapon `percentageBonus` cap (`300`) or the ML direct-damage/Death Strike cap (`35/70`).
- Tests may intentionally assert literal Battle Lust expected values (45/90) rather than reusing production constants, because they document the gameplay rule and catch accidental rule changes.
- Cleanup: no bonus if the effective weapon/property is removed, mobile is dead/deleted, or era is pre-SA.
- Distribution: no loot/runic/imbuing/artifact rollout in the storage/gameplay PR.

## Pitfalls

- When reviewing “hardcoded” SA property values, first search for existing shared caps/constants in the repo and classify the cap layer: property-specific cap, global weapon percentage cap, direct-damage cap, or era/ruleset cap. Only suggest centralization when the same gameplay rule is duplicated, not merely because two mechanics both mention PvP/PvM.
- Do not implement under-specified SA mechanics from the UO.com magic-property table alone; require review/source evidence for thresholds, caps, and timing.
- Do not confuse tooltip-only/runtime state rows with persistent rollable properties.
- Do not place post-ToL/Publish 96 properties into the SA container just because they are weapon properties.
- Do not call focused SA property tests broad-suite green unless the broad project suite actually ran.
- Do not leave timer contexts with stale `Mobile`/`Item` references; add clear helpers for tests and invalidation paths for lost equipment.

## Verification Checklist

- [ ] Era/ruleset and source decision are explicit.
- [ ] New property bit uses the next safe free bit in the correct container.
- [ ] GM property wrapper exists.
- [ ] Tooltip cliloc appears only in the target era.
- [ ] Gameplay hook is in the owning pipeline and uses applied damage where required.
- [ ] Runtime timers/tokens are cancelled or removed on context cleanup.
- [ ] Tests cover positive behavior, pre-era no-op, formula/caps, timing/cooldown/decay, and cleanup.
- [ ] Distribution surfaces remain unchanged unless explicitly scoped.
