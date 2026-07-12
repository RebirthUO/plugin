---
name: uo-magic-spells
description: Use when adding, debugging, or auditing a ModernUO-based spell, spell-school registration, cast/fizzle/resource sequence, targeting, delayed/field/summon behavior, AI casting, or transient spell effects. Do not use for weapon combat formulas, property storage, or skill-gain rules except where the spell pipeline calls them.
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
    - ultima-online
    - modernuo
    - magic
    - spells
    - parity
    related_skills:
    - uo-official-evidence
    - uo-combat-pipeline
    - uo-skills-stats-races
    - modernuo-regions
version: 1.0.0
author: Crome696
---
# UO Magic and Spells

## Boundary

Own spell metadata/registration and the cast lifecycle from eligibility through targeting, resource consumption, effect application, duration, and cleanup. Route damage math after the spell hands off to `uo-combat-pipeline` and skill progression to `uo-skills-stats-races`.

## Core Workflow

1. State school, ruleset/publish behavior, spell ID/circle, source, target shape, resources, effect, duration/cooldown, PvP/PvM differences, and explicit non-goals.
2. Inspect the active school base, `Spell`, `SpellHelper`, initializer/registry, book/scroll/craft surfaces, nearest spell pattern, effect consumers, AI path, and focused tests. A reserved ID or scroll is not an implemented spell.
3. Trace the sequence: `CheckCast`/region/client/form gates -> cast state/timer -> target -> `CheckSequence` -> resource/mana/tithing/reagent consumption -> reflect/harmful/LOS/range -> effect/damage/summon -> `FinishSequence` -> cleanup.
4. Consume resources at the established commit point. For selection-gump spells, defer consumption until a valid response when cancellation must be free. Route travel and harmful checks through shared helpers; do not bypass region/criminal/follower rules.
5. Keep temporary contexts runtime-only unless persistence is required. Recast must refresh/replace deliberately; cancel timers and clear buffs/mods/references on expiry, death, deletion, logout, map change, item removal, and interruption as applicable.
6. Register under the correct cumulative expansion gate and keep book, scroll, inscription, spell ID, and AI reachability aligned.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Provide a spell contract (metadata, gates, target, cost, formula, duration/cooldown, cleanup), source/repo anchors, changed surfaces, conflicts/policy choices, PvP/PvM risks, and exact validation results.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for the broad spell lifecycle, school tables, field/summon/AI patterns, and common pitfalls.
- Research named spells from current official evidence and the configured
  repository at use time; do not reuse ticket snapshots or stored defaults.

## Verification

- Build and run the focused spell tests plus adjacent registry/book/scroll/effect tests.
- Cover pre-era/target-era registration, success/fizzle/cancel, missing resources, valid/invalid targets, reflect/region rules, formulas/caps, recast, expiry, and lifecycle cleanup.
- Use deterministic timers/RNG and initialized client/world registries; restore all global state.
- Self-check that direct test helpers did not bypass the prerequisite or target path the test claims to prove.
