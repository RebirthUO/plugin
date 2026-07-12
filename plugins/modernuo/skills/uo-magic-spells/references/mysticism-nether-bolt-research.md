# Mysticism: Nether Bolt research notes

Use this when drafting, reviewing, or implementing Nether Bolt in ModernUO/RebirthUO. It condenses the 2026-07-09 issue-review sweep for `RebirthUO/ModernUO#32`; re-check live sources before making new era/publish claims.

## Canonical source findings

- UO.com Mysticism page: Nether Bolt is a **First Circle** Mysticism spell.
  - Mana cost: `4`
  - Delay: `0.50 seconds`
  - Minimum skill: `0`
  - Words: `In Corp Ylem`
  - Reagents: `Black Pearl`, `Sulfurous Ash`
  - Effect: fires nether energy at the target, dealing **Chaos damage**.
  - Reference damage: `120 Mysticism + 120 Focus/Imbuing: 30-37`, comparable to Magic Arrow.
  - PvP burst control: rapid repetition of Nether Bolt, or Nether Bolt + Magic Arrow on one target, should cause no damage beyond the initial hit.
- UO.com Publish 60 Stygian Abyss notes: Publish 60 introduced Mysticism and lists Nether Bolt as firing nether energy at the target for chaos damage.
- UO.com Inscription Craftables: Nether Bolt Mysticism scroll has INT/Mana `4` and required skill `0`.

## Community / engine cross-check

- UOGuide Nether Bolt agrees on words, mana, minimum skill, delay, Black Pearl + Sulfurous Ash, single-target use, slight delay, and chaos-damage description.
- ServUO precedent implements:
  - `MysticSpell`, first circle.
  - Delayed damage.
  - Non-stacking with Magic Arrow.
  - `GetNewAosDamage(10, 1, 4, target)`.
  - 100% chaos damage.
  - `IDamageable` targeting.
  - Nether projectile/sound effects: moving particles item `0x36D4`, hue `0x49A`, sound `0x211`.

## RebirthUO/ModernUO repo anchors from the review sweep

When issue repo is `RebirthUO/ModernUO`, inspect the remote that matches that repo (often `upstream/main` in a local fork worktree), not blindly `origin/main`.

- `Projects/UOContent/Spells/Initializer.cs`: `Core.SA` Mysticism block has spell ID `677` commented as `NetherBoltSpell` before `EagleStrikeSpell` registration.
- `Projects/UOContent/Spells/Mysticism/`: no `NetherBoltSpell.cs` was present during the sweep; existing Mysticism spells included `EagleStrikeSpell`, `BombardSpell`, `HailStormSpell`, `NetherCycloneSpell`, etc.
- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs`: centralizes Mysticism mana table, required skill table, cast delay, and support-skill damage as max(Focus, Imbuing).
- `Projects/UOContent/Spells/Mysticism/EagleStrikeSpell.cs`: nearest single-target Mysticism damage-spell pattern for `ITargetingSpell<Mobile>`, harmful target setup, reflect handling, particles, and delayed damage timing.
- `Projects/UOContent/Spells/Mysticism/BombardSpell.cs` and `Projects/UOContent/Spells/First/MagicArrow.cs`: useful delayed-damage/non-stacking hooks.
- `Projects/UOContent/Spells/Mysticism/NetherCycloneSpell.cs`: existing Mysticism chaos damage split example.
- `Projects/UOContent/Engines/Craft/DefInscription.cs`: SA-gated Nether Bolt inscription entry already existed.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/NetherBoltScroll.cs`: scroll already defined as spell ID `677`.
- `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs`: Mystic spellbook type exists.

## Implementation policy default from issue review

For the first implementation slice, use the local harmful-mobile `ITargetingSpell<Mobile>` pattern rather than adding a new cross-engine `IDamageable` targeting surface. UO.com and UOGuide only establish target/single-target behavior; ServUO uses `IDamageable`, but local comparable single-target spells use `Mobile`. Treat broader `IDamageable` spell targeting as a separate engine-policy follow-up unless current local APIs already support it safely.

## Acceptance-test focus

- SA-gated registration includes spell ID `677`; pre-SA excludes it.
- First circle, mana `4`, required Mysticism `0.0`, Black Pearl + Sulfurous Ash, words `In Corp Ylem`.
- Harmful mobile target validation follows existing spell pipeline: LOS/visibility, reflection, fizzle/interruption, reagents, spell-channeling restrictions.
- Damage is chaos damage, scales with Mysticism plus higher of Focus/Imbuing, and stays Magic Arrow-level.
- Repeated Nether Bolt and Nether Bolt + Magic Arrow on one target respect delayed-damage non-stacking.
- Spellbook/scroll/inscription surfaces expose Nether Bolt consistently with the rest of Mysticism.

## Implementation/test pattern that worked

For the first local implementation slice, the smallest durable change was:

- Add `NetherBoltSpell : MysticSpell, ITargetingSpell<Mobile>` under `Projects/UOContent/Spells/Mysticism/`.
- Use `SpellInfo("Nether Bolt", "In Corp Ylem", -1, 9002, Reagent.BlackPearl, Reagent.SulfurousAsh)` to match existing Mysticism spell style.
- Keep `Circle => SpellCircle.First` and rely on `MysticSpell` for mana `4`, required skill `0.0`, `CastDelayBase`, and max(Focus, Imbuing) damage skill.
- Set `DelayedDamage => true` and `DelayedDamageSpellFamilyStacking` to a static AoS+ family containing `typeof(MagicArrowSpell)`. Patch `MagicArrowSpell` reciprocally to include `typeof(NetherBoltSpell)` so `HasDelayedDamageContext` blocks stacking in either cast order.
- In `Target(Mobile m)`, follow the Magic Arrow/Eagle Strike shape: `CheckHSequence(m)`, `SpellHelper.Turn`, delayed-damage-context guard, `SpellHelper.CheckReflect`, visual/sound, then `SpellHelper.Damage(this, m, GetNewAosDamage(10, 1, 4, m), 0, 0, 0, 0, 0, 100)` for 100% chaos.
- Register `Register(677, typeof(NetherBoltSpell))` inside the existing `Core.SA` Mysticism block; do not expose it in pre-SA registration.

Regression tests that proved useful:

- Metadata/values: name, mantra, first circle, first-circle cast delay, mana 4, required skill 0.0, `SkillName.Mysticism`, Black Pearl + Sulfurous Ash, delayed damage.
- Spellbook/scroll: `MysticSpellbook` offset/count and `NetherBoltScroll` spell ID 677 (reflection is acceptable for the private generated field when testing static metadata).
- Registration gate: reset `SpellRegistry` via reflection, set `Core.Expansion` to ML vs SA, call `Initializer.Configure()`, and assert ID 677 absent/present while a neighboring Mysticism spell such as Eagle Strike remains present under SA.
- Stacking: directly use `StartDelayedDamageContext`, `HasDelayedDamageContext`, and `RemoveDelayedDamageContext` on Nether Bolt and Magic Arrow to prove the shared delayed-damage family in both directions without driving brittle timer slices.
- Damage-skill selection: compare deterministic `GetNewAosDamage(10, 1, 4, target)` for Focus 120 vs Imbuing 120 vs neither using `PredictableRandom`; Focus and Imbuing should match and both exceed no-support-skill damage.
