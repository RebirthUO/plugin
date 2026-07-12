# Spell Focusing / Spell Focusing Sash review note

Use when reviewing or implementing the Spell Focusing item property or Spell Focusing Sash in RebirthUO/ModernUO.

## Source classification

- **Canonical — UO.com Magic Item Properties**: `Spell Focusing` is a special sash property, not a rollable loot/imbuing property. UO.com lists intensity `N/A`, imbue weight `No`, found on `Sash`, capped `N/A`, enabled/disabled by item context menu, affects single-target damage spells, resets on target change or sequence completion, and excludes field spells, poison, and summons.
- **Canonical — UO.com Artifacts – Events**: `Spell Focusing Sash` stats are weight 1 stone, Spell Focusing, Brittle, Mana Increase 1, Defense Chance Increase 5%, Strength Requirement 10, Durability 255/255; event sources are `In the Shadow of Virtue` and `Treasures of The Undead Lords`.
- **Community cross-check — UOGuide**: `Spell Focusing` says damage starts below normal at `-20%` and rises to `+20%`; this conflicts with the current UO.com table and should not override UO.com for first-pass parity. `In the Shadow of Virtue` gives Spring 2010 through late March 2011 event context.
- **Engine precedent — ServUO**: item-specific `SpellFocusingSash` class uses cliloc candidates `1150059` / `1150058`, runtime `SpellCastTarget` / `SpellCastCount`, buff icons `SpellFocusingBuff` / `SpellFocusingDebuff`, reset/peak messages `1150116` / `1150117` / `1150118`, and does not serialize target/count. Treat as implementation clue, not canonical behavior.

## Review decisions

- Prefer the current UO.com sequence order for first implementation: `-30%`, then `-24%`, `-18%`, `-12%`, `-6%`, `0%`, then `+2%` steps to caps.
- PvP: hold at `+20%` for the next 5 spells, then reset.
- PvM: continue by `+2%` to `+30%`, then reset on the next spell or target change.
- Advance only when a qualifying single-target damage spell reaches the damage application hook against the same valid target. Do not advance on cast start, target selection alone, excluded fields/poison/summons, non-spell damage, or paths that never reach spell damage application.
- Persist only the item and enabled/disabled mode if the toggle is durable. Do not serialize current target/count; reset transient state on load, equip changes, disable, delete, death, logout, invalid/dead/deleted target, and sequence completion.

## RebirthUO repo anchors and pitfalls

- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs` already contains `SpellFocusingBuff` and `SpellFocusingDebuff` enum names.
- Current RebirthUO may have no `SpellFocusing`, `Spell Focusing`, `CastingFocus`, or `Spell Focusing Sash` implementation; verify with repo search before drafting implementation notes.
- `BaseClothing` may not host `NegativeAttributes`; current `NegativeAttributes.Brittle` support can be constrained to weapons/armor. The sash's `Brittle` line needs either artifact-specific tooltip/fortification behavior or a deliberately scoped clothing-negative extension. Do **not** broaden clothing negative-property random distribution as part of this ticket.
- Keep distribution separate: implement the named sash/property behavior without adding loot tables, runic/reforging, imbuing, or event reward acquisition unless explicitly scoped.

## Tests to expect

- Item construction and tooltip stats, including Spell Focusing and Brittle presentation.
- Context-menu enable/disable behavior or documented ModernUO equivalent.
- Damage sequence tests for UO.com order, including target-change reset and invalid/dead/deleted target reset.
- PvP hold and PvM +30% cap behavior.
- Exclusions for fields, poison, summons, AoE/multi-target effects, non-spell damage, incoming damage, and Casting Focus interruption path.
- Equip/unequip/death/logout/save-load cleanup for transient state and buffs.
