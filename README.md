# ModernUO Plugin

This repository packages the `modernuo` plugin metadata for Codex, Claude Code, Cursor, and Hermes-adjacent RebirthUO development workflows. The plugin's skill payload is a 1:1 mirror of the active Hermes `ultima-online` profile skills that are thematically used for Ultima Online, ModernUO, and RebirthUO work.

The plugin should not carry local-only or hand-edited ModernUO skill variants. When Hermes learns or updates a UO/ModernUO/RebirthUO skill, sync the matching skill directory from the Hermes profile into `plugins/modernuo/skills/` so the plugin and Hermes use the same guidance.

## Contents

- `plugins/modernuo/.codex-plugin/plugin.json` defines the plugin manifest and Codex UI metadata.
- `.claude-plugin/marketplace.json` defines the Claude Code marketplace catalog.
- `plugins/modernuo/.claude-plugin/plugin.json` defines the Claude Code plugin manifest.
- `.cursor-plugin/marketplace.json` defines the Cursor marketplace catalog.
- `plugins/modernuo/.cursor-plugin/plugin.json` defines the Cursor plugin manifest.
- `plugins/modernuo/assets/rebirthuo-logo.png` provides the plugin logo and composer icon.
- `plugins/modernuo/skills/` contains the Hermes-synced Ultima Online, ModernUO, and RebirthUO skills, including migration, code audit, codebase navigation, issue triage, online verification, human-review promotion, canonical game-doc authoring, test workflow, regression testing, era parity, skill/spell/item-property parity, subsystem/domain research, lifecycle, performance, serialization, timers, networking, regions, combat, crafting, loot, quests, housing, and related workflows.
- `AGENTS.md` contains repository-level maintenance instructions for plugin changes.
- `CHANGELOG.md` records plugin-version changes.

## Skill Sync Contract

The ModernUO plugin is sourced from:

```text
C:\Users\Jsiem\AppData\Local\hermes\profiles\ultima-online\skills\
```

The synced set is every Hermes skill in that profile skills tree whose name or frontmatter description is scoped to Ultima Online, ModernUO, RebirthUO, RunUO/ServUO migration, UOGuide research, or closely related RebirthUO implementation/review/triage workflows. Non-UO general software-development skills such as generic planning, TDD, debugging, code-review, or Hermes skill-authoring guidance are intentionally excluded.

After changing the plugin skill payload, bump the plugin version, update this README if the purpose/usage changed, and add a `CHANGELOG.md` entry.

## Usage

For Codex, install or load the plugin through the configured local marketplace, then ask for ModernUO or RebirthUO help by topic. Example requests include:

- triaging a GitHub issue into a source-backed implementation plan;
- implementing a sufficiently specified RebirthUO GitHub issue as an isolated tested PR;
- verifying a `Triage required` ticket for `Human Review` promotion;
- producing a German RebirthUO implementation plan;
- authoring canonical RebirthUO game-docs for an era mechanic;
- planning or reviewing ModernUO migrations from RunUO/ServUO patterns;
- auditing code for ModernUO lifecycle, performance, serialization, string, packet, gump, timer, threading, or region risks;
- checking named Ultima Online skill, spell, item-property, or era parity against ModernUO/RebirthUO source and approved web sources;
- reviewing UO living-world side effects across era/ruleset, facets, economy, housing, PvP, PvM, and player trust;
- normalizing generated xUnit test names and planning focused or broad validation.

For Claude Code, add the marketplace from a local checkout while testing:

```text
/plugin marketplace add .
/plugin install modernuo@rebirthuo-plugins
```

Or add the GitHub-hosted marketplace:

```text
/plugin marketplace add RebirthUO/plugin
/plugin install modernuo@rebirthuo-plugins
```

For Cursor, add this repository as a plugin marketplace in Cursor's marketplace settings. Cursor reads `.cursor-plugin/marketplace.json`; install or use `modernuo` from the `rebirthuo-plugins` marketplace.

The plugin UI uses `plugins/modernuo/assets/rebirthuo-logo.png` through the manifest `interface.logo` and `interface.composerIcon` fields.