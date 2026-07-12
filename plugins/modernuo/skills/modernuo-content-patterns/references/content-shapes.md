# UOContent Implementation Shapes

Read only the sections matching the requested content. Local sibling code is authoritative for exact signatures.

## Durable item

- Place under the matching `Projects/UOContent/Items/<Category>/` directory.
- Use `[SerializationGenerator(0)]`, `partial`, and a `[Constructible]` constructor when staff creation is intended.
- Prefer `DefaultName` or a verified `LabelNumber`; do not set both without local precedent.
- Validate backpack/ownership/range before use. Persistent visible fields use generated setters and invalidate properties.
- Test construction, use rejection/success, property output, save round trip, and delete cleanup.

## Mobile or creature

- Place under the matching `Mobiles` domain folder and derive from the nearest behavioral base class.
- Set body/sounds, stats, skills, damage/resists, AI/fight mode, fame/karma, taming, and loot only from target-era evidence or explicit design policy.
- Use overrides such as `DefaultName`, `CorpseName`, resource yields, and abilities when the base contract supports them.
- Test spawn/construct, AI-visible behavior, death/loot, tame/control where relevant, persistence, and deletion.

## Spell

- Derive from the school base and inspect sibling `SpellInfo`, registration ID, scroll/book slot, targeting wrapper, sequence, damage, and era gate.
- Validate before resource consumption; call the correct sequence/finish hooks on every success/cancel/failure path.
- Keep damage types totaling the expected contract and revalidate targets at response time.
- Test registration/metadata plus actual cast outcome, resource consumption, interruption/cancel, invalid targets, era behavior, and temporary-effect cleanup.

## Skill handler

- Register in the repository's expected startup phase and set the callback for the exact `SkillName`.
- Return the locally expected reuse delay. Target callbacks revalidate actor/target state and use the repository skill-check APIs.
- Test callback registration, success/failure boundaries, cooldown, invalid target, and any resource/tool consumption.

## Loot and economy

- Prefer existing `LootPack` or crafting/vendor abstractions that already select era behavior.
- Treat gold, artifacts, recipes, resources, drop chances, durability, insurance, and blessed status as economy changes requiring explicit evidence and tests.
- Never add loot or distribution merely because a type exists.

## Context menus and interactions

- Use the local pooled context-menu signature and validate actor state/range both when displaying and when clicked.
- Do not retain long-lived entity references in menu entries without cleanup or stale-state checks.

## Placement guide

- Items: `Projects/UOContent/Items/<Category>/`
- Creatures/NPCs: `Projects/UOContent/Mobiles/<Domain>/`
- Spells: `Projects/UOContent/Spells/<School>/`
- Skills: `Projects/UOContent/Skills/`
- Engines/systems: `Projects/UOContent/Engines/<System>/`
- Gumps: `Projects/UOContent/Gumps/`

Confirm the actual repository tree before creating a new folder; do not copy this layout blindly into a custom module.
