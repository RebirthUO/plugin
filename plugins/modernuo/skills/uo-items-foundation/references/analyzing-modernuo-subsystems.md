# Analyzing a ModernUO/RebirthUO Subsystem

A reproducible reading recipe for turning a ModernUO/ModernUO-style UO server
codebase into a class-level skill. Validated against the Items subsystem
in this tree; applies to Spells, Skills, AI, Combat, Crafting, Housing, and
similar.

## Reading order

Work top-down. Each layer narrows the surface and feeds the next:

1. **`CLAUDE.md`** at the repo root. Read the 18 Code Audit Rules in full
   before writing any skill content — `_camelCase` private fields, no
   `Task.Run`, single-threaded engine, `PooledRefList` on hot paths, etc.
   The skill's `Pitfalls` section must reflect these.

2. **`docs/server-engine-knowledge-base.md`**. Section 5 ("Atomare Systeme")
   is the canonical system map: every subsystem gets a row with Zweck,
   Abhängigkeiten, Dateien, Parameter. Use the section structure as a
   template for the new skill's "When to Use" + quick-reference table.

3. **The subsystem's deepest plan document** (e.g.
   `docs/superpowers/plans/2026-06-02-item-properties-completion.md` for
   Items). Plans enumerate the open work, the file map, and the precise
   reference paths used by the implementation. They are the most accurate
   source of file:line citations.

4. **The feature/era matrix** (e.g.
   `docs/mondains-legacy-content-matrix.md`). Use the "Status" legend and
   the "Feature Matrix" tables to understand which era gates apply. The
   "Skills To Update Or Verify" and "Implementation Tickets" sections are
   a ready-made acceptance criteria list.

5. **The engine entity** (e.g. `Projects/Server/Items/Item.cs`). Read
   constructors, `partial` declaration, and the `SerializationGenerator`
   attribute. This is the foundation layer — every skill must reference
   but not duplicate this. Cite file:line.

6. **The content-layer base classes** (e.g. `Projects/UOContent/Items/`).
   Map the inheritance chain into a table in the skill. Each base class
   gets one row: use case, file, distinguishing fields.

7. **The AOS / shared infrastructure** (e.g. `Projects/UOContent/Misc/AOS.cs`
   for items). Identify the `BaseAttributes` storage pattern, the
   `IPropertyList` contract, and the static `GetValue` aggregators. These
   are the cross-cutting primitives that every typed property consumer
   depends on.

8. **The content patterns doc** (`dev-docs/content-patterns.md`). The
   "Common Item Base Classes" and "Key Item Properties" tables are the
   canonical reference for what the engine exposes. The "New Item with
   Properties and Behavior" example is the template for any code blocks
   the skill recommends.

9. **Existing tests under `Projects/UOContent.Tests/`**. The test file
   names are the regression surface; they tell you which behaviors are
   contractually tested. Reference them in the skill's "Verification
   Checklist".

## Skill shape that worked for Items

Three skills at class level, each with `related_skills` pointing at the
other two plus the canonical `modernuo-content-patterns`,
`modernuo-serialization`, `modernuo-property-lists`,
`modernuo-era-expansion`:

| Skill | Anchors on | Trigger class |
|---|---|---|
| `uo-items-foundation` | `Item.cs`, `Base*` classes, `GetProperties` | "new item / item persistence / OPL / LootType / decay" |
| `uo-aos-item-properties` | `AOS.cs` `BaseAttributes`, all five containers | "add a property / wire a property into combat / OPL row missing" |
| `uo-crafting-recipes-resources` | `CraftSystem.cs`, `CraftItem.cs`, `Def*.cs`, recipe scrolls, BOD | "new craftable / new recipe / ML recipe gate / runic tool" |

The trigger descriptions all start with "Use when working with the UO ..."
and name the operation that fires the skill, not the file the user
happens to be editing. This is the discriminator that makes a class-level
skill load.

## Citation discipline

- Cite file:line for every non-trivial claim (`Item.cs:195` for the
  `partial class Item` declaration, `AOS.cs:284-310` for the
  `AosAttribute` enum, etc.).
- File paths under `Projects/Server/` are engine code, not the
  primary editing target. Call this out in the skill's "Don't use for"
  block.
- File paths under `Projects/UOContent/` are the primary editing
  target. Anchor most code examples and tips there.

## Pitfalls specific to the analysis workflow

1. **Reading `Item.cs` cold without `CLAUDE.md`**. The 4311-line file
   looks like a normal class. The audit rules (no `World.Items`
   iteration, no `Console.WriteLine`, `[Constructible]` requirement)
   are easy to miss and end up as wrong content in the skill.
2. **Mixing engine and content responsibilities in one skill**. The
   engine files (`Projects/Server/`) are read-only by default; the
   content files (`Projects/UOContent/`) are the editing target. A
   skill that recommends editing `Item.cs` is a footgun. Always
   split: foundation/patterns first, engine deltas as "requires
   explicit approval" tasks.
3. **Skipping the plan documents**. The `docs/superpowers/plans/...`
   and `docs/<era>-content-matrix.md` files are the most accurate
   source of file:line and feature status. Skipping them produces
   stale citations and missed open-work items.
4. **Citing `AOS.cs` line numbers from the full file**. The file is
   1607 lines and the enums move around. After any edit, re-verify
   the line numbers with `search_files` rather than trusting the
   citation.
5. **Producing skill content in the user's chat language**. The
   German kickoff is task framing; the SKILL.md and references must
   be in English for portable skill conventions.

## Verifying the analysis itself

Before declaring the analysis complete:

- [ ] Every file:line citation resolves to an actual file and roughly
      correct line via `search_files` or `read_file` with offset.
- [ ] The skill's `related_skills` graph is bidirectional within the
      new trio and points at the existing `modernuo-*` peers.
- [ ] The skill's `Pitfalls` section cites at least one
      `CLAUDE.md` rule that was actually load-bearing.
- [ ] The skill's `Verification Checklist` references at least one
      existing test file from `Projects/UOContent.Tests/`.
- [ ] Frontmatter validated by the inline Python script
      (see `scripts/validate_hermes_skill.py` pattern in the
      `hermes-skill-creator` skill) — name ≤ 64, description ≤
      1024, file ≤ 100,000, all CromeSDK markers present.
