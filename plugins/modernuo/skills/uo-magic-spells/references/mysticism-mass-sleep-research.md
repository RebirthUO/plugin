# Mysticism: Mass Sleep research notes

Use these notes when drafting or implementing RebirthUO/ModernUO Mass Sleep work. They are condensed from a 2026 issue-authoring session and should be re-verified against live sources before code changes.

## Source classification

- Canonical: `https://uo.com/wiki/ultima-online-wiki/skills/mysticism/`
  - Mass Sleep is listed as Fifth Circle Mysticism.
  - Mana cost: 14.
  - Delay: 1.50 seconds.
  - Minimum skill: 45.
  - Reagents: Ginseng, Nightshade, Spider's Silk.
  - Text: puts one or more targets within a radius around the target's location into temporary Sleep; works like Sleep on multiple targets, including hidden players.
- Canonical behavior checkpoint: `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-65/`
  - Sleep/Mass Sleep no longer fully prevents casting or attacking.
  - Applies a stupor state with severe casting, cast recovery, attack, and movement speed reductions.
  - Damage breaks the effect.
  - Immunity changed to 3-12 seconds, scaling by player Magic Resist; 30+ Resist is needed to extend immunity beyond 3 seconds.
- Community/reference: `https://www.uoguide.com/Mass_Sleep`
  - Mantra: `Vas Zu`.
  - Mana 14, minimum skill 45, delay 1.5 seconds.
  - Duration up to roughly 15 seconds.
  - Area around target location.
  - Duration compares caster Mysticism plus Focus/Imbuing against target Resisting Spells.
- Community/reference: `https://www.uoguide.com/Stygian_Abyss`
  - Mysticism is a Stygian Abyss skill.
- Engine precedent: ServUO `Scripts/Spells/Mysticism/SpellDefinitions/MassSleepSpell.cs`
  - Spell ID 686, Circle Fifth, `Ginseng`, `Nightshade`, `SpidersSilk`.
  - Radius precedent: `AcquireIndirectTargets(p, 3)`.
  - Duration precedent: `((Mysticism + max(Focus, Imbuing)) / 20) + 3 - (target Resist / 10)`; apply only if positive.
- Engine precedent: ServUO `SleepSpell.cs`
  - Shared Sleep runtime state, Sleep buff icon, damage break, immunity list/timer.

## RebirthUO/ModernUO repo anchors seen in-session

- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs`
  - Mana table `{4,6,9,11,14,20,40,50}` and required skill table `{0.0,8.0,20.0,33.0,45.0,58.0,70.0,83.0}` make Fifth Circle 14 mana / 45.0 skill.
  - Cast delay formula `0.5 + 0.25 * (int)Circle` makes Fifth Circle 1.5 seconds.
  - `CastSkill` is Mysticism; damage/support skill is max(Imbuing, Focus).
- `Projects/UOContent/Spells/Initializer.cs`
  - Under `if (Core.SA)`, Mass Sleep spell ID 686 was present as a commented registration: `// Register(686, typeof(MassSleepSpell));`.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/MassSleepScroll.cs`
  - Scroll already exists with spell ID 686 and item ID `0x2DA7`.
- `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs`
  - Mystic spellbook offset 677, count 16, covering 677-692.
- `Projects/UOContent/Engines/Craft/DefInscription.cs`
  - Inscription already has a MassSleepScroll recipe in the 14-mana Mysticism tier using Ginseng, Nightshade, and Spider's Silk.
- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs`
  - `Sleep` and `MassSleep` buff icon enum entries already exist.
- Current `origin/main`/`upstream/main` evidence from the 2026-07-09 issue review:
  - `MassSleepSpell` and `SleepSpell` classes were still absent.
  - Registration for spell ID 686 remained commented.
  - The scroll/book/recipe/buff-icon scaffolding existed, so implementation needs shared transient sleep/stupor state plus hooks; it is not just an uncomment-registration task.
- Local Mysticism spell patterns to inspect before implementation:
  - `HailStormSpell.cs` for point-targeted Mysticism AoE.
  - `BombardSpell.cs` for harmful Mystic targeting/resist comparison.
  - `SpellPlagueSpell.cs` for timed effect cleanup and buff-icon precedent.
- Cross-school debuff hook precedents for the Publish 65 stupor state:
  - `Projects/UOContent/Spells/Spellweaving/EssenceOfWind.cs` stores per-target cast-speed and swing-speed malus state; `Spell.GetCastDelay` and `BaseWeapon.GetDelay` consult that state.
  - `Projects/UOContent/Spells/Spellweaving/Thunderstorm.cs` exposes `GetCastRecoveryMalus`, consumed by `Spell.GetCastRecovery`.
  - `Projects/UOContent/Mobiles/Monsters/ML/Special/Ilhenir.cs` sends `SpeedControlSetting.Walk` and later resets with `SpeedControlSetting.Disable`, a movement-slow precedent.

## Implementation cautions

- Treat Mass Sleep as SA Mysticism parity content, not custom crowd control, unless the user explicitly asks for a custom ruleset.
- Default to post-Publish 65 stupor semantics rather than pre-Publish 65 hard sleep.
- Do not implement a full attack/cast lockout for current-era behavior.
- Hidden-player interaction is source-backed by UO.com but high-impact for stealth/PvP; test explicitly and document any shard deviation.
- Official sources name the slowdown categories but do not quantify exact constants. Use named constants with tests and existing repo hook shapes as the conservative default: walk-speed control for movement, Essence-of-Wind-style cast-speed/swing-speed maluses, and Thunderstorm-style cast-recovery malus. Tune if a better current-client or engine source is found; do not leave the issue blocked solely waiting for official numeric multipliers.
- Clean runtime state on damage, expiry, death, logout/delete, map changes as applicable, and avoid persisting temporary sleep timers unless an existing effect architecture requires it.
