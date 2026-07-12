---
name: uo-crafting-recipes-resources
description: Use when adding, debugging, or auditing ModernUO-based CraftSystem/CraftItem registrations, recipe scrolls, subresources, expansion gates, tools, exceptional outcomes, or ICraftable hooks. Do not use for gathering, BOD workflows, base item persistence, or property semantics beyond the crafted-output boundary.
license: MIT
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags:
    - ultima-online
    - modernuo
    - crafting
    - resources
    - economy
    related_skills:
    - uo-bulk-orders-bod
    - uo-harvest-gathering-resources
    - uo-items-foundation
    - uo-aos-item-properties
version: 1.0.0
author: Crome696
---
# UO Crafting, Recipes, and Resources

## Boundary

Own declarative recipe registration and the runtime craft transaction: visibility, prerequisites, resources/tools, skill roll, quality, output creation, and `ICraftable.OnCraft`. Route harvesting to `uo-harvest-gathering-resources`, BODs to `uo-bulk-orders-bod`, and output property mechanics to `uo-aos-item-properties`.

## Core Workflow

1. State craft system, target era, recipe source, output, skill ranges, resources, tool/station needs, recipe-scroll policy, and exceptional/mark behavior.
2. Inspect the active `CraftSystem`, `CraftItem`, matching `Def*.cs`, `Recipe` registry, output `ICraftable` implementation, acquisition/drop source, and existing metadata/runtime tests.
3. Trace the real transaction: gump visibility -> expansion/known-recipe gate -> tool/station -> resources/subresource selection -> skill and quality roll -> consumption -> construction -> `OnCraft` -> inventory delivery.
4. Register through the local DSL. Keep recipe IDs globally unique; use the established expansion gate; list every secondary skill/resource; align `SetUseSubRes`, material/hue inheritance, `UseAllRes`, and quest flags with the intended output.
5. Put persistent output behavior on the output type/`OnCraft`, not in ad-hoc gump code. Keep runic, loot-source, BOD, and quest distribution changes explicitly scoped.
6. In tests, prefer runtime `CraftItem` metadata over source grep. Craft systems and `Recipe.Recipes` are process-global: avoid rebuilding under another expansion unless all affected static registries are safely snapshot/restored.

## Evidence boundary

Establish expected official gameplay through `uo-official-evidence`. Community,
emulator, client, and repository sources may provide discovery or implementation
evidence only; unresolved official behavior remains blocked.

## Output Contract

Provide a recipe matrix (output, group/name, gate, skills, resources, tools, recipe ID, quality), acquisition source, changed files, economy/compatibility risks, and exact validation results. State whether gameplay behavior changed or only metadata/tests changed.

## Reference Routing

- Read [domain-map.md](references/domain-map.md) for engine flow, DSL tables, ML recipe ranges, subresources, examples, and project gotchas.
- Read [se-craft-metadata-test-pattern.md](references/se-craft-metadata-test-pattern.md) only for SE recipe coverage or static CraftSystem test isolation.

## Verification

- Build and run focused craft metadata/runtime/gump tests; use `--no-build --no-restore` only after a successful build.
- Cover visible/hidden era cases, learned/unlearned recipe, correct and missing tools/resources/skills, consumption, quality, hue/material inheritance, and output defaults.
- Verify acquisition reachability and global recipe-ID uniqueness.
- Self-check that the test did not leave process-global craft or recipe state changed for later tests.
