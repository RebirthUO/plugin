# GameDocs Atomic Parity Pilot Pattern

Session learning from building an Ultima Online GameDocs scaffold and Animal Taming pilot.

## Durable pattern

When asked to create current Broadsword UO vs ModernUO parity documentation, do not begin by searching code for missing features. Build parity documentation source-first:

1. Establish the Obsidian documentation scaffold and shared taxonomy first (`00_Index`, `01_Broadsword`, `02_Project_Parity`).
2. For a pilot topic, extract concrete official facts from `uo.com` before code inspection.
3. Convert each official fact into atomic, checkable parity records.
4. Search ModernUO code for each atom and record exact file/class/method/data references.
5. Use conservative parity statuses: choose `Unknown` rather than `Different` when formulas have not been mathematically reconciled.
6. Add validation/test ideas for every `Partial` or `Unknown` atom.
7. Keep RebirthUO custom behavior as an overlay page/stub; never mix it into Broadsword parity.
8. Verify expected Markdown files exist and report counts/entry points at the end.

## Useful Obsidian structure

```text
/GameDocs
  /00_Index
    Home.md
    Source_Priority.md
    Documentation_Model.md
    Atomic_Parity_Model.md
    Parity_Status_Definitions.md
    Lootpack_Exception.md
  /01_Broadsword/<Domain>/...
  /02_Project_Parity/<Domain>/<Topic>/
    Index.md
    Official_Facts.md
    Atomic_Parity.md
    ModernUO_Code.md
    Validation.md
    RebirthUO_Overlay.md
```

## Status pitfall

Do not overstate parity. If code evidence appears to differ from official examples but the formula has not been reconciled, mark the atom `Unknown`, not `Different`. If an atom contains two conditions and only one is verified, mark it `Partial`, not `Complete`.

## Source note

If a secondary source such as UOGuide times out or is unavailable, explicitly say no secondary-only facts were asserted rather than blending remembered/community detail into official facts.

## Expansion feature overview pages

When the user asks to "write this into game-docs" for a broad expansion/era feature inventory, use the existing Obsidian vault instead of creating a standalone dev-doc:

- Place broad Broadsword-era overview pages under `game-docs/GameDocs/01_Broadsword/Systems/<Expansion_Name>.md` unless an existing domain page is clearly more specific.
- Add YAML frontmatter consistent with nearby pages: `title`, `domain`, `source_layer`, optional `project_layer`, `rebirthuo_overlay`, `parity_status`, and tags.
- Keep the overview product-facing and conservative: mark item/spawn/loot lists as `Needs source confirmation` unless each claim was source-verified in the same task.
- Link the new page from `game-docs/GameDocs/01_Broadsword/Systems/Index.md`.
- Run `git diff --check -- <changed markdown files>` as lightweight validation; Markdown linting may be absent.
- If the whole `game-docs/` tree is untracked, report that explicitly instead of claiming the documentation is versioned.
