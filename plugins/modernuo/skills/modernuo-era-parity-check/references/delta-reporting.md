# Delta Reporting Reference

Use this reference whenever a row is non-`Present`, low-confidence, monster,
crafting, or user-focused.

## Risk Rows Default

Broad era reports stay compact, but risk rows must be data-backed. A risk row is
not complete until it has:

- `Expected`: cited target behavior from repo docs, UO.com, UOGuide, Stratics
  fallback, or explicitly labeled unverified sources.
- `ModernUO Evidence`: file path and line, data path, test evidence, or exact
  search result showing current implementation.
- `Delta`: concrete mismatch, missing field, missing hook, different value,
  source conflict, or `no delta found`.
- `Validation`: `confirmed`, `source-conflict`, `repo-only`, `needs-runtime`, or
  `open-research`.
- `Impact`: the practical risk category.

Never leave a final row as "needs confirmation". If evidence is incomplete,
write an `Open Research` item with sources checked and the next validation step.

## Monster Delta Checklist

For monsters and animals, compare these fields when sources expose them:

- Type/class existence and era folder placement.
- Hits, stamina, mana, strength, dexterity, intelligence, karma, fame, virtual
  armor, damage ranges, and resist ranges.
- Skills from source tables vs `SetSkill` calls.
- AI type, fight mode, barding flags, taming/control fields, control slots, and
  pack instinct.
- Spells, special abilities, `MonsterAbility`, `OnGaveMeleeAttack`,
  `OnGotMeleeAttack`, timers, cooldowns, and TODO comments.
- Loot, artifact chances, fame/karma rewards, resource drops, corpse behavior,
  and quest/key drops.
- Spawn files, region/dungeon access, champion/peerless controllers, and
  EraProfile/Core gates.

Use overlapping ranges carefully. If UOGuide says `MagicResist 80.0-95.0` and
code uses `SetSkill(SkillName.MagicResist, 85.0, 95.0)`, the delta is only the
minimum value unless another source disagrees.

## Crafting Delta Checklist

For crafting and craftables, compare these fields when sources expose them:

- Recipe or craft item registration in the correct `Def*.cs` craft system.
- Required skill, minimum skill, success chance, exceptional chance, and make
  requirements.
- Tools, resources, material counts, resource variants, and consumed vs retained
  items.
- Produced item type, quantity, quality, durability, hue, localized name, and
  category placement.
- Recipe scroll requirements, rare recipes, runic tool behavior, BOD rewards,
  talisman bonuses, imbuing hooks, and expansion/profile gates.
- Tests or docs covering the craftable and its era status.

If a crafting row says only "needs confirmation", it is not finished. Either
derive a source-vs-code delta or move it to `Open Research` with exact source and
repo checks still needed.

## Accuracy Guidance

- `90-100%`: UO.com and UOGuide or repo docs agree, and source matches
  field-by-field for the scoped rows.
- `70-89%`: Sources agree and code mostly matches; only minor value or coverage
  deltas remain.
- `50-69%`: Partial implementation, source disagreement, or material fields are
  still unverified.
- `30-49%`: Major missing abilities, loot, recipes, formulas, or spawn wiring.
- `0-29%`: Missing type/system, wrong era gate, or only unverified emulator
  evidence.

Lower confidence when a row depends on runtime behavior that was not exercised.

## Open Research Format

Use stable IDs so follow-up issues can target one unresolved decision:

```markdown
- EPC-OR-{N}: {question} - Checked: {sources and repo paths} - Missing evidence: {field} - Next step: {exact query, file read, test, or runtime scenario}
```

Open research is acceptable. Unsupported certainty is not.
