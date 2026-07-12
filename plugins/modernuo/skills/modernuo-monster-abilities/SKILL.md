---
name: modernuo-monster-abilities
description: >
  Use when adding, migrating, or reviewing reusable ModernUO-based creature
  combat specials implemented as MonsterAbility classes. Do not route boss phase
  orchestration or WeaponAbility work here; keep those in encounter code or the
  weapon-ability system.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
      - modernuo
      - rebirthuo
      - mobiles
      - monster-abilities
      - combat
    related_skills:
      - modernuo-content-patterns
      - uo-combat-pipeline
      - modernuo-timers
      - modernuo-serialization
      - modernuo-code-audit
---

# ModernUO Monster Abilities

## Boundary

Combat procs, debuffs, counters, breaths, area effects, and summons-on-hit belong
in reusable classes under `Projects/UOContent/Mobiles/Abilities/`. A creature
should normally only expose them through `GetMonsterAbilities()`. Keep encounter
phases, altar/retinue ownership, and HP-threshold orchestration with the owning
encounter. `WeaponAbility` remains a separate engine slot.

## Workflow

1. Search the creature for `GetMonsterAbilities()`, `GetWeaponAbility()`, and
   inline combat hooks such as `OnGaveMeleeAttack`, `OnGotMeleeAttack`,
   `OnDamagedBySpell`, `OnDamage`, and `OnHarmfulSpell`.
2. Classify the behavior as reusable combat special, weapon ability, or encounter
   orchestration before moving code.
3. Reuse an existing ability or select the narrowest base class. Keep tunable
   constants, trigger, chance, cooldown, targeting, and effect ownership on the
   ability.
4. Add a `MonsterAbilityType` value only when typed lookup is needed; register the
   ability in `MonsterAbilities.cs`, then wire the creature.
5. Preserve era gates, target eligibility, damage/debuff semantics, and cooldown
   tracking. Do not manually dispatch logic already reached by trigger flags.
6. Add focused tests for creature registration and the player-visible effect.

## Guardrails

- Call `base.Trigger(...)` where the selected base contract records cooldown.
- Parameterize shared effects instead of cloning one class per creature.
- Debuff/helper items must use ModernUO serialization, cancel owned timers on
  deletion, and restore or delete transient state safely after load.
- Use spatial queries and pooled collections on area-effect hot paths; do not scan
  `World.Mobiles` or add allocating LINQ chains.
- An absent registration does not prove a missing special: record discovered
  inline hooks as migration candidates before changing behavior.
- Audit both `MonsterAbility` and `WeaponAbility`; a creature may use both.

## Output Contract

Implementation output names the ability class, base/trigger, registry and creature
wiring, preserved source behavior, tests, and any inline-hook follow-up. Review
output names the exact path/line, architecture mismatch, gameplay risk, and
focused verification.

## Verification

- Creature exposes the expected ability without duplicate inline dispatch.
- Chance, cooldown, target filters, era gate, and effect values are exercised.
- Helper items clean timers and do not survive load incorrectly.
- The owning project builds and focused ability tests pass; label any remaining
  runtime/manual check explicitly.

## Reference Routing

- Read [ability bases, triggers, templates, and registry checklist](references/reference.md)
  when selecting a base class or implementing a new ability.
- Read [uo.com creature ability audit notes](references/uo-com-creature-ability-audit.md)
  only for official pet/creature ability parity research.
- Load `uo-combat-pipeline` for damage-hook ordering and `modernuo-timers` /
  `modernuo-serialization` for stateful helper items.
