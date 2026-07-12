# Spellweaving: Dryad Allure research note

Use this when drafting or implementing a ModernUO/RebirthUO issue or PR for the ML Spellweaving spell **Dryad Allure**.

## Source summary

- **Canonical current behavior:** `https://uo.com/wiki/ultima-online-wiki/skills/spellweaving/`
  - Dryad Allure row: `Rathril`, 40 mana display, 3.0s casting delay, 52 minimum Spellweaving, duration permanent until slain, Arcane Circle / focus bonus of +2% charm chance, charms humanoid/Repond targets, 3 follower slots.
  - Note: the UO.com table may say `Area of Effect: Caster only` while describing a targeted charm. Treat this as a source conflict; UOGuide and engine precedent support one-creature targeting.
- **Community/reference mechanics:** `https://www.uoguide.com/Dryad_Allure`
  - Confirms 40 mana, 52.0 skill, 3.0 casting delay, one creature, until slain/released/abandoned duration, +2% charm chance per additional arcanist, 3 follower slots.
  - Lists eligible humanoid families: meer, savages, ratmen, named Sanctuary ratman/ettin, non-paragon/non-named Repond-group monsters such as titans, cyclopean warriors, ettins, orcs, ogres; excludes reptilian humanoids like lizardmen.
- **Era support:** `https://www.uoguide.com/Ultima_Online:_Mondain%27s_Legacy`
  - Lists Spellweaving as a new Mondain's Legacy skill. Exact Dryad Allure initial publish may still need official-source confirmation.
- **Canonical ML-window publish evidence:**
  - `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2005-2/publish-36-16th-september/`
  - `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2005-2/publish-37-27th-october/`
  - These mention Spellweaving fixes after ML launch; they prove Spellweaving existed in the ML publish window, not Dryad Allure's exact introduction publish.
- **Engine precedent:** `https://raw.githubusercontent.com/ServUO/ServUO/master/Scripts/Spells/Spellweaving/DryadAllure.cs`
  - Implements spell ID 611, `RequiredSkill = 52.0`, `RequiredMana = 40`, `CastDelayBase = 3s`, `Target` range 12, Repond validation, 3 control slots, allured state, success/failure sounds/messages, and backpack-content deletion on success.

## ModernUO/RebirthUO repo anchors observed

- `Projects/UOContent/Spells/Initializer.cs` has the Spellweaving block under `Core.ML`; Dryad Allure was reserved/commented as `Register(611, typeof(DryadAllureSpell));`.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/SpellweavingScrolls.cs` defines `DryadAllureScroll : SpellScroll` with spell ID 611 and item ID `0x2D5C`.
- `Projects/UOContent/Items/Skill Items/Magical/SpellweavingBook.cs` uses `BookOffset => 600` and `BookCount => 16`, so ID 611 is in range.
- `Projects/UOContent/Spells/Spellweaving/ArcanistSpell.cs` already handles ML-capable client checks, arcanist quest context, mana/skill requirements, and cast-time focus capture.
- `Projects/UOContent/Items/Weapons/SlayerGroup.cs` defines the Repond slayer group that maps to expected humanoid targets.
- `Projects/UOContent/Mobiles/BaseCreature.cs` has `ControlSlots` and `SetControlMaster()`, but the inspected tree did not have active `Allured` / `AllureImmune` properties; only a commented `pet.Allured` stable check appeared in `AnimalTrainer`.

## Drafting / implementation cautions

- Do not call UO.com's `Caster only` Area-of-Effect text definitive; record the conflict and use targeted one-creature behavior as the conservative default unless the shard intentionally customizes.
- Treat exact initial publish number as unresolved unless an official Dryad Allure-specific publish note is found; use `Mondain's Legacy / ML launch window` as the suggested default.
- Include exploit controls in acceptance criteria: follower-slot cost, player-target rejection, stabling/storage prevention, release/death/logout/save-load behavior, spawner/region behavior, and loot/backpack policy.
- If adding persistent `Allured` state, require serialization/migration and lifecycle tests.

## RebirthUO implementation/test pattern captured from issue #36

When implementing Dryad Allure in RebirthUO/ModernUO, the smallest safe slice was:

- Add `DryadAllureSpell : ArcanistSpell` in `Projects/UOContent/Spells/Spellweaving/` and register `Register(611, typeof(DryadAllureSpell))` only inside the existing `Core.ML` block in `Spells/Initializer.cs`.
- Use the existing `SpellweavingBook` slot range (`BookOffset = 600`, `BookCount = 16`) and existing `DryadAllureScroll` spell ID `611`; no book/scroll migration is needed when those already exist.
- Validate targets through the existing Repond slayer entry (`SlayerGroup.GetEntryByName(SlayerName.Repond)?.Slays(creature) == true`) plus safety gates: reject null/deleted, summoned, paragon, controlled non-allured, and `AllureImmune` creatures. Player targets are rejected by the `BaseCreature` target path.
- Add `BaseCreature.Allured` as persistent state when allured creatures can survive saves; clear it when `SetControlMaster(null)` releases/control-clears the creature. Keep allured loyalty at max in the loyalty timer instead of letting normal pet loyalty decay release the creature.
- Add a conservative `BaseCreature.AllureImmune` virtual hook. The useful default was `BardImmune || IsInvulnerable`, with per-creature overrides for named/boss/custom immunity.
- On success, set `ControlSlots = 3` before `SetControlMaster(caster)`, clear immediate combat/aggressor state between caster and creature, set `Allured = true`, set max loyalty, delete backpack contents, and send `1074377`.
- On failed charm roll, play failure sound, set `ControlTarget = caster`, `ControlOrder = Attack`, `Combatant = caster`, warmode true, and send `1074378`.
- Preserve exploit safeguards outside the spell too: reject allured creatures in `AnimalTrainer.EndStable`, block `PetOrders.DoOrderTransfer`, and guard `TransferItem.OnSecureTrade` in case a trade item already exists.
- Focused tests can avoid the full cast sequencer by making the chance formula and apply-attempt helper `internal` (UOContent exposes `InternalsVisibleTo` to `UOContent.Tests`). Cover metadata, ML registration gate, book/scroll slot, Repond/unsafe target validation, chance formula including focus bonus, success follower/control/backpack cleanup, failure enrage/no follower leak, and release/control-clear removing `Allured`.
- Use a test `Orc` subclass overriding `GetSpeeds` to avoid depending on NPC speed table setup; use `PredictableRandom(0)` for deterministic success and `PredictableRandom(20)` for deterministic failure because `NextDouble()` returns `value / 20.0`.
