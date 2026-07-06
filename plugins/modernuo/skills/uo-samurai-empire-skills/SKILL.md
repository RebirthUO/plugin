---
name: uo-samurai-empire-skills
description: Use when explaining, documenting, auditing, or implementing Samurai Empire skill mechanics such as Bushido and Ninjitsu, including PvP/PvM, template, mobility, and RebirthUO doc/test side effects.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    - UltimaOnline
    - SamuraiEmpire
    - Skills
    - Bushido
    - Ninjitsu
    related_skills:
    - uo-magic-spells
    - uo-skills-stats-races
    - uo-combat-pipeline
    - modernuo-era-expansion
license: MIT
---
# Samurai Empire Skills

## Overview

This skill explains the Samurai Empire skill area for Ultima Online, focused on Bushido and Ninjitsu as the SE-defining character systems. It does not treat all Tokuno content as verified parity, and it separates SE skills from AoS, ML, SA, and shard-custom mechanics. It depends on Hermes tools and source-backed UO pages; no extra packages are required.

## When to Use

- "Erkläre die Samurai Empire Skills."
- "Welche Skills gehören zu Samurai Empire?"
- "Bushido/Ninjitsu parity check" or "SE skill implementation plan".
- When deciding whether a mechanic is SE, AoS prerequisite, ML+, or custom.
- When reviewing PvP, PvM, economy, housing, or new-player impact of Bushido/Ninjitsu.
- When building a German or English guide section dedicated only to Samurai Empire skills.

## Prerequisites

- Ruleset must be named before conclusions: Samurai Empire / SE, ModernUO `Expansion.SE`, or custom shard rules.
- Official source pages to check first:
  - `https://uo.com/wiki/ultima-online-wiki/skills/bushido/`
  - `https://uo.com/wiki/ultima-online-wiki/skills/ninjitsu/`
- For RebirthUO code work, load `uo-era-product-timeline`, `uo-skills-stats-races`, and the relevant ModernUO implementation skill before editing.
- No credentials or environment variables are required.

## How to Run

Use `browser_navigate` and `browser_console` to extract the official UO.com Bushido and Ninjitsu pages. Use `search_files` to find `Core.SE`, `Expansion.SE`, `Bushido`, `Ninjitsu`, and individual ability classes before making any implementation claim.

## Quick Reference

- Expansion: Samurai Empire / SE.
- ModernUO era anchor: `Expansion.SE`; cumulative check: `Core.SE`.
- SE skills: Bushido and Ninjitsu.
- Bushido source: `https://uo.com/wiki/ultima-online-wiki/skills/bushido/`.
- Ninjitsu source: `https://uo.com/wiki/ultima-online-wiki/skills/ninjitsu/`.
- Tokuno context: Zento, Rokuon Cultural Center, New Haven Dojo, Lesser Hiryu access.
- Not SE skills: Necromancy, Chivalry, Spellweaving, Mysticism, Imbuing, Throwing.
- AoS prerequisite context: item properties, five-resist combat, insurance, special moves.
- ML+ warning: elves, Spellweaving, Heartwood, peerless structure are not SE.

## Procedure

1. **State the boundary.** Say that Samurai Empire skill work means Bushido and Ninjitsu unless the user explicitly broadens the scope to Tokuno items, pets, mobs, artifacts, or housing. You are done when the answer excludes AoS/ML/SA systems unless marked as prerequisite or custom.

2. **Summarize Bushido as a system.** Use official UO.com wording: Bushido is the art of the samurai and is closer to weapon abilities than true spellcasting. It requires a Book of Bushido, available from a samurai trainer in Zento, and comes with all abilities. Record the training note: the Haven trainer can train up to 40, and accelerated Old Haven gain should be taken after buying skill.

3. **Capture Bushido passives and abilities.** Use this source-backed checklist:

   | Mechanic | Mana | Skill | Source-backed behavior |
   |---|---:|---:|---|
   | Weapon Parry | - | - | Bushido improves weapon parry, especially two-handed, and lessens shield block chance; Human Jack of All Trades does not affect parry chance. |
   | Perfection | - | 50+ with honored foe | Hits on an honored foe build about 10 perfection levels; at 100 Bushido each level gives 10% normal-attack damage and 100 Luck, missed hits lose 3 levels, and defeat restores resources based on final level. |
   | Honorable Execution | 0 | 25 | Lethal success restores HP and grants 20% swing speed increase briefly; failure applies -40 all resistances, removes Resist Spells if present, and blocks Bushido spells/special moves for 7 seconds. |
   | Confidence | 10 | 25 | Defensive stance; parries heal 1 to `Bushido / 12` HP and refresh 1 to `Bushido / 5` stamina; activation regeneration lasts 4 seconds unless interrupted and total heal is `(Bushido * Bushido) / 576 + 15`; cancels Evasion. |
   | Counter Attack | 5 | 40 | Next successful parry automatically counterattacks and can use an active special move. |
   | Lightning Strike | 5 | 50 | Attack with 50% hit chance bonus; 45% Hit Chance Increase cap applies except full 50% can apply under Hit Lower Attack context. |
   | Evasion | 10 | 60 | Short evasive stance allowing parry of magical attacks like dragon breath and energy bolt; parry modifier scales 16-40%, +10% if Bushido is above GM and both Tactics and Anatomy are GM+; Dex below 80 penalizes; PvP diminishing returns can reduce up to 70%. |
   | Momentum Strike | 10 | 70 | Hit can chain to a nearby opponent with second-target damage scaling by Bushido, e.g. 60% at 60 and 100% at GM; if the main target dies on the hit, second-target damage is tripled. |

4. **Capture Bushido combat hooks.** Include that at 90 skill Bushido can substitute for Animal Taming to control and ride Lesser Hiryus. Include that Bushido counts toward ability to perform Special Moves and adds Whirlwind damage bonus with formula `Damage Bonus = (Bushido / 60 * number of opponents)^2`, capped at 100.

5. **Summarize Ninjitsu as a system.** Use official UO.com wording: Ninjitsu is the assassin skill. A Book of Ninjitsu is bought from a scribe in the Rokuon Cultural Center in Zento or from the Ninjitsu instructor in the New Haven Dojo. Hiding and Stealth are must-have supplemental skills, while weapon/magery/tactics/poisoning choices are template-dependent.

6. **Capture Ninjitsu abilities.** Use this source-backed checklist:

   | Ability | Mana | Skill | Source-backed behavior |
   |---|---:|---:|---|
   | Animal Form | 0 | 10 | Transform into animal forms; running while casting repeats last selected form; gain is from casting, not choosing higher forms. |
   | Mirror Image | 10 | 20 | Creates an image that may absorb damage within 4 steps; consumes a follower slot; disappears in 30-60 seconds. |
   | Focus Attack | 10 | 30 | Increases damage and the chance for weapon hit properties for one attack. |
   | Backstab | 30 | 40 | Stealth attack with damage bonus based on Ninjitsu and tracking distance. |
   | Shadowjump | 15 | 50 | Teleports while maintaining stealth only if a destination stealth check succeeds. |
   | Surprise Attack | 20 | 60 | Stealth attack that inflicts a short defense penalty; user cannot re-enter stealth for 5 seconds. |
   | Ki Attack | 25 | 80 | Damage increases with travel distance from activation point; target must be reached in under 2 seconds. |
   | Death Strike | 30 | 85 | If the target moves more than 5 steps or 3 seconds elapse, direct damage is based on attacker Ninjitsu, target Hiding/Stealth average, and tracked tiles; PvP damage is capped at 50%. |

7. **Capture Animal Form exactly.** Use this table when explaining Ninjitsu forms:

   | Skill | Form | Special ability |
   |---:|---|---|
   | 0 | Rabbit or Rat | +20 Stealth. |
   | 40 | Cat or Dog | Increased regeneration based on Ninjitsu. |
   | 50 | Giant Serpent | Inflicts low-level poison on non-ranged weapon hits. |
   | 50 | Bullfrog | Inflicts poison when damaged at short range. |
   | 70 | Ostard or Llama | Increased movement speed. |
   | 85 | Wolf or Bake-Kitsune | Increased movement speed, hit chance bonus, and maximum hit points. |
   | 100 | Unicorn | Increased movement speed and low-level poison immunity. |
   | 100 | Ki-Rin | Increased movement speed and fast stamina regeneration. |

8. **Capture Ninja equipment hooks.** Include official Ninjitsu page notes: smoke bombs and egg bombs require 50+ Ninjitsu; shuriken use ninja belts, need a free hand, work at 3-9 tiles, and can be poisoned; fukiya/darts work at 1-4 tiles and can be poisoned. Do not turn these into item parity claims without item-level source/code verification.

9. **Capture special moves without Tactics.** For Bushido/Ninjitsu, list Armor Pierce, Block, Defense Mastery, Double Shot, Dual Wield, Feint, Frenzied Whirlwind, and Talon Strike as special moves requiring Bushido or Ninjitsu instead of Tactics on specific SE-style weapons. Verify the weapon tables from the official pages before changing code.

10. **Review product side effects.** For every Bushido/Ninjitsu change, write a short impact row:

   | Area | Questions |
   |---|---|
   | PvP | Does Evasion, Death Strike, Shadowjump, Ki Attack, or Surprise Attack remove counterplay or inflate burst? |
   | PvM | Does Perfection, Confidence, Momentum Strike, or Animal Form change solo farming or survivability too much? |
   | Economy | Are skill books, bombs, shuriken, fukiya/darts, Lesser Hiryus, and SE weapons tradeable, crafted, blessed, insured, or sinked? |
   | Housing | Are Tokuno decorative rewards being introduced as prestige goods, and is their supply controlled? |
   | New players | Are Zento/New Haven trainers, books, and 50-skill gain quests available and clearly communicated? |
   | Veterans | Do SE templates create depth without making older AoS templates extinct? |

11. **Tie to code only after source capture.** Use `search_files` for the ability name and era gates. Treat `Core.SE` as cumulative: SE or later, not exactly SE. You are done when each mechanic claim has a source URL and each implementation claim has a repo anchor.

## Pitfalls

- Do not call every Tokuno feature a Samurai Empire skill; this skill area is Bushido and Ninjitsu.
- Do not treat AoS mechanics as SE features. Item properties, insurance, Necromancy, Chivalry, and the five-resist model are prerequisites/context, not SE skills.
- Do not fold ML/SA systems into SE: Spellweaving, Mysticism, Imbuing, Throwing, Elves, Gargoyles, Heartwood, Ter Mur, and Masteries are later or separate systems.
- Do not assume UO.com current behavior equals launch-day Samurai Empire behavior; mark publish-sensitive behavior before parity work.
- Do not claim a RebirthUO feature is live because a class exists. Check registration, expansion gates, maps, trainers, books, items, spawns, and tests.
- Do not ignore PvP diminishing returns, stealth checks, follower slots, poison interactions, and special-move substitutions; these are high-impact balance details.

## Verification

A completed Samurai Empire skills explanation has exactly two SE skills named, official UO.com links for both, a Bushido ability table, a Ninjitsu ability table, an Animal Form table, one `Core.SE`/`Expansion.SE` warning, and side-effect notes for PvP, PvM, economy, housing, new players, and veterans.
