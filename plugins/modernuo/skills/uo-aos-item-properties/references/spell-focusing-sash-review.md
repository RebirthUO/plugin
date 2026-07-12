# Spell Focusing / Spell Focusing Sash Review Notes

Use this reference when drafting or implementing the `Spell Focusing` item-property issue or the `Spell Focusing Sash` special item.

## Source hierarchy

- Canonical: UO.com Magic Item Properties (`https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`).
  - Intro note says unusual properties can appear on special items and calls out `Spell Focusing` on the spell focusing sash from a past event.
  - Table row: `Spell Focusing`, intensity `N/A`, imbue weight `No`, found on `Sash`, capped `N/A`.
  - Description: enabled/disabled through an item context menu; affects single-target damage spells; first spell starts at a damage penalty, subsequent spells improve; PvP holds at `+20%` for the next 5 spells; PvM continues to `+30%`; next spell or target change resets to the starting penalty; excludes field spells, poison, and summons.
- Canonical: UO.com Artifacts – Events (`https://uo.com/wiki/ultima-online-wiki/items/artifact-collections/artifacts-events/`).
  - `Spell Focusing Sash`: Weight 1 stone, Spell Focusing, Brittle, Mana Increase 1, Defense Chance Increase 5%, Strength Requirement 10, Durability 255/255.
  - Event sources listed: `In the Shadow of Virtue` and `Treasures of The Undead Lords`.
- Community/reference: UOGuide `Spell Focusing` raw page.
  - Describes damage starting below normal and rising to `+20%`, with low-mana spells used to build the property before high-damage spells.
  - Conflicts with UO.com/engine details on exact starting value; do not treat as canonical over UO.com.
- Community/reference: UOGuide `In the Shadow of Virtue` raw page.
  - Event cycle began Spring 2010 and concluded late March 2011; useful for post-SA event context, not mechanics authority.
- Engine precedent: ServUO `Scripts/Items/Artifacts/Equipment/Clothing/SpellFocusingSash.cs`.
  - Special `BodySash`, label cliloc `1150059`, property row cliloc `1150058`.
  - Runtime state: `SpellCastTarget`, `SpellCastCount`, `SpellDamageOffset`.
  - Buffs: `SpellFocusingBuff` / `SpellFocusingDebuff`, title `1151391`, args `1151392`.
  - Messages: reset `1150117`, tuned `1150118`, peaked `1150116`.
  - Stats match UO.com: BonusMana 1, DefendChance 5, Brittle 1.

## RebirthUO anchors observed during issue drafting

- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs` already has `SpellFocusingBuff` and `SpellFocusingDebuff`.
- `Projects/UOContent/Items/Clothing/BaseClothing.cs` owns clothing serialization, stat containers, and tooltip/property-list dispatch.
- `Projects/UOContent/Spells/Base/SpellHelper.cs` centralizes spell damage application through `SpellHelper.Damage(...)` and delayed AoS spell-damage timers.
- No local `SpellFocusing`, `Spell Focusing`, or `Spell Focusing Sash` implementation was found during the issue draft.
- Existing issue #9 (`Casting Focus`) is a separate item property: SA armor interruption resistance. Do not merge it with Spell Focusing.

## Implementation guidance

- Treat Spell Focusing as a special/event sash mechanic, not a normal rollable AoS armor/clothing property.
- Keep storage item-specific. Runtime target/count/offset state belongs on the sash or a small helper, not in a generic `AosAttributes` bit.
- Avoid serializing stale `Mobile` target references unless a deliberate persistence rule is chosen. Conservative default: reset transient target/count on load, unequip, death/logout, invalid target, and delete.
- Add a context-menu enable/disable path; UO.com explicitly says the item can enable/disable the property through context menu.
- Hook only qualifying single-target direct damage spells. Do not affect field spells, poison, summons, AoE/multi-target spells, non-spell damage, or incoming damage.
- The source conflict on exact sequence order must be resolved explicitly before implementation:
  - UO.com: first spell `-30%`, then `+6%` steps to `0%`, then `+2%` steps; PvP holds at `+20%`, PvM to `+30%`.
  - UOGuide: starts below normal, mentions `-20%` to `+20%`.
  - ServUO inspected implementation appears to increment through `-6, -12, -18, -24, -30`, then `0`, then positive `+2%` steps.
  - Suggested default for RebirthUO parity: follow UO.com unless live/client evidence proves the table wording is reversed.

## Test expectations

- Item construction/tooltip: Spell Focusing Sash stats, Brittle, Spell Focusing row, durability, weight.
- Context-menu toggle: enabled/disabled state and no effect while disabled.
- Damage sequence: deterministic single-target spell damage modifier steps, target-change reset, invalid/dead/deleted target reset.
- PvP/PvM divergence: PvP `+20%` hold behavior; PvM `+30%` max after the sequence decision is made.
- Exclusions: fields, poison, summons, AoE/multi-target spells, non-spell damage, incoming damage.
- Cleanup: unequip/delete/death/logout/save-load removes buffs and clears stale runtime state.
- Distribution guard: no random loot, runic/reforging, imbuing, or event reward rollout unless explicitly scoped.

## Implementation pattern observed in RebirthUO

A complete Spell Focusing Sash implementation in RebirthUO followed this shape; future special artifact modifiers that hook the spell-damage pipeline can adopt the same skeleton.

### Item side

- `Projects/UOContent/Items/Clothing/SpellFocusingSash.cs` derives from `BaseMiddleTorso` (sashes are middle-torso clothing).
- `[Flippable(0x1541, 0x1542)]` matches the EA artifact's tile pair.
- Artifact stats live in the constructor and override `LabelNumber` (`1150059`), `DefaultWeight` (`1.0`), `InitMinHits`/`InitMaxHits` (`255`), and `AosStrReq` (`10`).
- Brittle is forced via `AOS.IsBrittle(SpellFocusingSash) => Core.SA` so the property appears under the SA era gate without a stored bit.
- Runtime state (`_spellCastTarget`, `_spellCastCount`, `_enabled`) lives on the sash; it is per-target and per-caster, so the spell damage hook does not need to walk a global table.
- Lifecycle hooks to reset the sequence: `OnAdded`, `OnRemoved`, `OnDelete`, plus `PlayerMobile.PlayerDeathEvent` / `PlayerDeletedEvent` / `BaseCreature.CreatureDeathEvent` / `CreatureDeletedEvent`, and `EventSink.Logout` registered from a static `Configure()` method.
- Context-menu enable/disable entry is added inside `GetContextMenuEntries` only when the caster is the parent and `Core.SA` is set.

### Eligibility gate (shared between spells and the sash)

- A `virtual bool SpellFocusingEligible => false` was added to `Spell` so direct single-target damage spells can opt in individually without affecting fields, AoE, summons, or non-damaging spells.
- Each opted-in spell overrides `SpellFocusingEligible => true` (e.g. `MagicArrow`, `Harm`, `Fireball`, `Lightning`, `MindBlast`, `EnergyBolt`, `Explosion`, `FlameStrike`, `PainSpike`, `Bombard`, `EagleStrike`, `NetherBolt`, `WordOfDeath`).
- `SpellFocusingSash.TryGetDamageOffset(spell, caster, target, out int offset)` is the single static entry point used by the central damage hook; it also drives the buff icon lifecycle.

### Damage hook

- `Projects/UOContent/Spells/Base/SpellHelper.cs` exposes two `Damage` overloads (pre-AOS flat path and AoS-resisted path) plus a `SpellDamageTimerAOS` for delayed spells. Add the offset call inside each path after `AlterSpellDamageTo` / `AlterSpellDamageFrom` but before the actual `target.Damage(...)` so the modifier flows through the standard pipeline.
- Spells that bypass `SpellHelper.Damage` (e.g. `PainSpikeSpell` which calls `m.Damage` directly with `ignoreEvilOmen: true`) must apply the offset manually at the call site; do not try to funnel them through `SpellHelper.Damage` because their `DFAlgorithm` is spell-specific.
- Apply the offset with `AOS.Scale(damage, 100 + offset)` to keep the modifier a pure percentage on top of the spell's normal pipeline.

### Buff icon wiring

- The `SpellFocusingBuff` / `SpellFocusingDebuff` icons already exist in `BuffIcon.cs`; the sash adds/removes them via `PlayerMobile.AddBuff(...)` / `RemoveBuff(...)` as the offset crosses zero.
- Buff title and secondary clilocs: `1151391` and `1151392` (target name + offset percentage). Reset messages `1150117` / `1150118` / `1150116` correspond to target-change, tuned (offset==0), and peak-cast.
- The buff should be removed on every reset path (equip, unequip, delete, death, logout, disable) to prevent the client from showing a stale icon after the sash stops influencing damage.

### Sequence math (canonical RebirthUO parity)

- First six casts on the same target: `-30 + count * 6` (i.e. `-30, -24, -18, -12, -6, 0`).
- Casts 7+: `2 * (count - 5)`, capped at `+20` against players (held for five casts at the cap before the next reset) and `+30` against monsters.
- Sequence resets at the peak cast, on target change, on invalid/dead/deleted target, on caster death, on logout, and when the sash is disabled.

### Focused test expectations

- Stats and tooltip ordering: weight, item ID/flip, Mana Increase, Defense Chance Increase, Strength Requirement `10`, durability `255/255`, Spell Focusing row before Brittle, Brittle before attribute rows.
- Enabled-state serialization: serialize/deserialize round-trip preserves `Enabled`; context-menu toggle flips it.
- PvM sequence: all 21 casts produce the documented offset table, and the 22nd cast resets to `-30`.
- PvP cap: hitting `+20` is held for five casts, then the next cast resets.
- Target change: switching to a new target resets to `-30` and clears buffs.
- Non-eligible spells (AoE, fields, summons, non-damaging spells) return `false` from `TryGetDamageOffset`.

### Era and distribution guard

- Gate every behavior with `Core.SA`: tooltip rows, gameplay offset, context-menu, and `AOS.IsBrittle`.
- Keep storage on the sash. Do not add an `AosAttributes` bit, an `AosArmorAttribute` slot, or an imbuing weight for Spell Focusing; this is event-artifact storage only.
- Distribution guard: do not add to `BaseRunicTool` loot rolls, Treasure Maps, Champion Spawn tables, or any economy surface unless a separate, explicitly scoped ticket extends it.