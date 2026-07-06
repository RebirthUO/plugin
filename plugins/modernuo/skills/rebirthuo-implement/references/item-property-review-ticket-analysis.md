# RebirthUO Item Property Review Tickets

Use this reference when a RebirthUO issue is an item-property review ticket from an epic (for example `Item Property: <name>`) and the user asks to analyze it or fill in what is missing before implementation.

## Goal

Turn a `needs-review` property ticket into an implementation-ready ticket, or classify it as still missing data. Do not jump directly to code if the ticket explicitly asks for mechanics/era review first.

## Evidence collection pattern

1. Read the child issue and parent epic.
   - Capture labels, status, source URL, comments, and whether it says `needs-review`.
   - Parent epics often state scope rules such as "implement mechanic first; loot/runic/imbuing separately".
2. Pull official UO source rows.
   - For UO.com magic item properties pages, extract the exact table row for the property: property name, intensity, imbue weight, found-on item types, cap, description.
   - Search UO.com artifact/event pages for the concrete item if the property is only found on a named artifact.
3. Pull repo anchors.
   - Existing attribute containers: `Projects/UOContent/Misc/AOS.cs`.
   - Tooltip/property output on item families such as `BaseClothing`, `BaseArmor`, `BaseWeapon`, `BaseJewel`, `BaseTalisman`.
   - Damage hooks: `Projects/UOContent/Spells/Base/Spell.cs`, `Projects/UOContent/Spells/Base/SpellHelper.cs`, and `Projects/UOContent/Misc/AOS.cs`.
   - Concrete item families, e.g. `BodySash` in `Projects/UOContent/Items/Clothing/MiddleTorso.cs`.
4. Optional emulator cross-check.
   - ServUO can be useful as a secondary implementation reference, not canonical truth.
   - Record both the item class and the hook location; e.g. a property can be a concrete artifact plus a central damage hook rather than a generic attribute.

## Implementation-readiness fields to add

For each property ticket, fill these before coding:

- Era/ruleset gate (`Core.HS`, `Core.TOL`, etc.) and why.
- Exact item family or concrete item; avoid broad generic application unless the source supports it.
- Storage/serialization plan: persistent item stats vs volatile runtime sequence state.
- Tooltip/property lines and cliloc/text fallback strategy.
- Activation path if the source says context menu/toggle/double-click.
- Runtime hook path and exclusions.
- Explicit non-goals: loot, runic, imbuing, artifacts, craft, or drop generation unless the ticket says otherwise.
- Acceptance criteria with formula/table values.
- Focused tests: expansion gate, tooltip, concrete formula sequence, reset conditions, exclusions, and no accidental loot/imbue exposure.

## Spell Focusing example

Official UO.com Magic Item Properties says:

- Property: Spell Focusing
- Intensity: N/A
- Imbue Weight: No
- Found on: Sash
- Cap: N/A
- Enabled/disabled through a context menu.
- Affects damage spells aimed at a single target.
- First spell modifier `-30%`.
- Subsequent spells increase by `+6%` steps to `0%`, then by `+2%` steps.
- PvP remains at `+20%` for the next 5 spells, then resets.
- PvM continues to `+30%`, then resets.
- Next spell after peak, or any target change, resets to `-30%`.
- Excludes field spells, poison, and summons.

UO.com artifact/event pages identify `Spell Focusing Sash` as a `Body Sash` event arc item with:

- Spell Focusing
- Brittle
- Mana Increase 1
- Defense Chance Increase 5%
- Durability 255/255

ServUO reference pattern:

- Concrete `SpellFocusingSash : BodySash`.
- Runtime fields for target/count.
- `ValidateTarget(...)` computes the sequence.
- Hook in `AOS.Damage` for `Core.HS` and spell damage.

Recommended RebirthUO ticket-completion stance:

- Implement as a concrete `SpellFocusingSash : BodySash` unless maintainers choose a generic attribute model.
- Gate at High Seas+ or request an explicit custom-era decision.
- Do not enable loot/runic/imbuing as part of the property ticket.
- Add tests for the exact modifier table, PvP/PvM caps, reset on target change, disabled sash, expansion gate, and exclusions for fields/poison/summons.
