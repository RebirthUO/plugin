# Mysticism Spell Trigger research notes

Use when drafting, reviewing, or implementing Spell Trigger (`Spell ID 685`) for ModernUO/RebirthUO Mysticism.

## Source findings

- **Canonical — UO.com Mysticism** (`https://uo.com/wiki/ultima-online-wiki/skills/mysticism/`): Spell Trigger is a fifth-circle Mysticism spell: mana 14, delay 1.50 seconds, minimum skill 45. It uses Dragon's Blood, Garlic, Mandrake Root, and Spider's Silk. It stores a single Mysticism spell in a Spell Stone; double-clicking the stone instantly casts the stored spell; the caster must possess the stored spell in their spellbook; storage cap is based on Mysticism plus Focus/Imbuing; unlike Healing Stone, it does not require a free hand. Current wording says `Cooldown: 5 minutes`. The storable cap starts at Circle Two and increases by one circle per 20 points in both Mysticism and Focus/Imbuing, max Circle Six at 120/120.
- **Canonical — UO.com Publish 60** (`https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/`): Stygian Abyss introduced Mysticism; Spell Trigger allows the caster to store a Mysticism spell in a Spell Stone that instantly casts the stored spell when used.
- **Community/reference — UOGuide Spell Trigger** (`https://www.uoguide.com/Spell_Trigger`): Confirms mana 14, minimum skill 45, spellbook possession, and Mysticism + Focus/Imbuing storage cap. It conflicts with UO.com by listing `Delay (seconds)` as 5 and `Duration` as 5 minutes.
- **Engine precedent — ServUO SpellTriggerSpell** (`https://github.com/ServUO/ServUO/blob/6fd01855840590e22cc73d94b5f7d9a97b1cf537/Scripts/Spells/Mysticism/SpellDefinitions/SpellTriggerSpell.cs`): Opens a selection gump, deletes prior `SpellStone` instances in the caster's backpack before placing a new one, makes `SpellStone` blessed/non-transferable, blocks world-drop and secure trade, deletes the stone on use, and applies a 300-second per-mobile cooldown. Treat as emulator precedent, not canonical history.

## RebirthUO / ModernUO repo anchors

Check current line numbers before citing in an issue or PR, but expected anchors are:

- `Projects/UOContent/Spells/Initializer.cs`: SA Mysticism registration block; `SpellTriggerSpell` is spell ID 685 and may be commented until implemented.
- `Projects/UOContent/Spells/Mysticism/MysticSpell.cs`: provides Mysticism mana/required-skill table, cast-delay base, Mysticism cast skill, and Focus/Imbuing support-skill behavior. Fifth circle already maps to 14 mana, 45.0 required skill, and 1.50s cast delay.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/Mysticism/SpellTriggerScroll.cs`: scroll for spell ID 685, item art `0x2DA6`.
- `Projects/UOContent/Engines/Craft/DefInscription.cs`: SA inscription recipes include Mystic spellbook and Spell Trigger scroll.
- `Projects/UOContent/Items/Skill Items/Magical/MysticSpellbook.cs`: Mystic spellbook offset 677 and 16 slots.
- `Projects/UOContent/Items/Skill Items/Magical/Spellbook.cs`: spell IDs 677-692 map to `SpellbookType.Mystic`.

## Implementation policy defaults

- Prefer UO.com current values and existing `MysticSpell` formulas for cast delay/mana/min skill.
- Treat the 5-minute value as a per-caster cooldown after Spell Stone use, not as automatic Spell Stone expiry, unless stronger client/official evidence is found.
- Show only implemented, registered, known, and storage-cap-eligible Mysticism spells in the selection UI. Do not expose commented/unimplemented spell IDs.
- Replacing prior stones, delete-on-use, non-transfer/drop protection, and secure-trade blocking are important PvP/economy safeguards, not cosmetic behavior.

## Gump-First Casting Architecture (Deferred Reagent Consumption)

Spell Trigger MUST open a selection gump but MUST NOT consume reagents/mana until the user picks a spell, because the issue explicitly requires cancellation/timeout to leave reagents intact. The SummonFamiliar pattern (consume in `OnCast`, then send gump) is therefore wrong here.

Concrete architecture:

1. `CheckCast()` validates prerequisites (skill, focus, mana, SA gate, **storable list non-empty**). Returns `false` on failure with an explanatory `SendMessage`.
2. `OnCast()` ONLY calls `SpellTriggerGump.DisplayTo(Caster, this)`. Does NOT call `CheckSequence()`.
3. The gump's `OnResponse` calls an internal entry point on the spell (e.g. `FinishStoneCreation(int spellId)`) that performs `ConsumeReagents()` + `Caster.Mana -= ScaleMana(GetMana())` + the stone-create/drop effect.
4. Cancelled/expired gumps (ButtonID 0 / no response) leave the spell state at `None` with reagents and mana intact.

Use `Mobile.SendGump(...)` from `OnCast()`; do NOT try to keep the spell state held during the gump wait — the spell framework returns to `None` automatically once `OnCast` returns, and a fresh `ConsumeReagents()` call in the gump response is the canonical resource gate.

The `DisplayTo` factory pattern: validate state before constructing the gump, keep the constructor `private`, never short-circuit inside `BuildLayout`. See the gump-first spells section in `modernuo-gump-system` skill for the reusable pattern.

## Compile Footguns Specific to Spell Trigger Helpers

When implementing helper methods that walk registered Mysticism spell IDs (e.g. to build the storable-list filter), three compile errors reproduce predictably:

- **`SpellRegistry.GetRegistryNumber(int spellId)` does not exist.** It only exists for `Type`, `ISpell`, or `SpecialMove`. Detect registration via `spellId >= 0 && spellId < SpellRegistry.Types.Length && SpellRegistry.Types[spellId] is not null` or, more idiomatically, by checking whether `SpellRegistry.NewSpell(spellId, null, null)` returns non-null.
- **`spell.Circle` and `spell.RequiredSkill` are compile errors on the base `Server.Spells.Spell` class.** They are abstract members defined on concrete schools (`MysticSpell`, `MagerySpell`, etc.). Pattern-match the concrete type: `spell is MysticSpell mystic ? (int)mystic.Circle : 0`. A bare `spell.Circle` will not compile against `Spell`.
- **`SpellCircle.Invalid` does not exist.** Use `SpellCircle.First` as a floor, or pattern-match the school type instead of testing against a sentinel value.

A fourth footgun is serialization-side and applies to the new `SpellStone` Item:

- **The serializer auto-generates `PascalCase` properties from `_camelCase` fields.** Declaring both `[SerializableField(0)] _storedSpellId` AND a manual `public int StoredSpellId { get; private set; }` causes `CS0102: The type 'SpellStone' already contains a definition for 'StoredSpellId'`. Pick one of: (a) let the generator emit the property and use `[InvalidateProperties]` on the field; (b) drop the field attribute and use `[SerializableProperty(0)]` on a hand-written property; (c) keep the field attribute and write the property `get => _storedSpellId;` with no auto-property setter. See the field-vs-property anti-pattern in `modernuo-serialization` skill.

## Lifecycle Cleanup

The cooldowns, stoned state, and selection-cache dicts all hold references to `Mobile`. Map each lifecycle explicitly:

- **Logout**: `EventSink.Logout += OnLogout` removes the caster from the cooldown dict (DoFizzle-style).
- **PlayerDeath / PlayerDeleted**: `[OnEvent]` code-generated handlers remove the caster. Use `ModernUO.CodeGeneratedEvents.OnEventAttribute`.
- **Item delete (Spell Stone)**: `OnDoubleClick` should call `Delete()` regardless of activation success so a stone never lingers; the cooldown is the throttle, not the stone.
- **Cancellation / gump close**: ensure the selection gump's `DisplayTo` factory builds the gump only when the prerequisites hold, and never falls through to a half-built gump. Cancellation simply means no `OnResponse` ever runs, so no resources are spent.

## Risks and Tests to Require

- PvP burst compression: require one-stone-at-a-time, per-caster cooldown, and preserved stored-spell validation.
- Economy/storage leakage: Spell Stones should not become tradeable/stockpilable commodities.
- Region/security bypass: activation must route through the stored spell's normal target, LOS/range, harmful/criminal, travel, summon/follower, and expansion checks.
- Gump cancellation/timeout: should not consume reagents or leave the cast sequence stuck.
- Focused tests should cover registration gate, spellbook lookup, selection bounds, known-spell validation, storage cap, prior-stone replacement, non-transfer/drop/secure-trade behavior, delete-on-use, cooldown, and at least one direct-target plus one self/no-target stored spell path. Use the `ResetSpellRegistry()` + `Core.Expansion` toggle harness from `Projects/UOContent.Tests/Tests/Spells/Mysticism/PurgeMagicSpellTests.cs`.
