# ModernUO Plugin

This repository contains the `modernuo` plugin metadata for Codex, Claude Code, and Cursor RebirthUO development. It packages focused skills for ModernUO server implementation, GitHub issue triage into source-backed implementation plans with explicit code-change rationale, publish-to-era measurement checks, and citations limited to repo, internet, or issue-supplied evidence, custom content module setup, Ultima Online domain research, migration work, subsystem audits, cross-era content change routing, LootPack source preservation, symbol discipline for constants, variables, fields, properties, and `Policy*` surfaces, named UO skill, spell, and item property parity checks, evidence-backed era parity reports with expected-vs-actual data deltas, and content parity checks.

## Contents

- `plugins/modernuo/.codex-plugin/plugin.json` defines the plugin manifest and Codex UI metadata.
- `.claude-plugin/marketplace.json` defines the Claude Code marketplace catalog.
- `plugins/modernuo/.claude-plugin/plugin.json` defines the Claude Code plugin manifest.
- `.cursor-plugin/marketplace.json` defines the Cursor marketplace catalog.
- `plugins/modernuo/.cursor-plugin/plugin.json` defines the Cursor plugin manifest.
- `plugins/modernuo/assets/rebirthuo-logo.png` provides the plugin logo and composer icon.
- `plugins/modernuo/skills/` contains ModernUO and Ultima Online guidance skills for code review, GitHub issue triage, custom module setup, migration, LootPack source preservation, symbol discipline, cross-era content change gates, named skill, spell, and item property parity checks, delta-backed era parity reporting, content systems, combat, crafting, persistence, networking, regions, quests, housing, and related workflows.
- `AGENTS.md` contains repository-level Codex instructions for plugin maintenance.

## Usage

For Codex, install or load the plugin through the configured local marketplace, then ask for ModernUO or RebirthUO help by topic. Example requests include triaging a GitHub issue into a source-backed implementation plan, creating a `CUOContent` custom module when no shard shortcut is provided, migration guidance, subsystem audits, LootPack preservation reviews before replacing source-derived `AddLoot(LootPack.*)` calls with exact-gold or policy helpers, symbol-discipline reviews for unnecessary constants, locals, fields, properties, and `Policy*` names, era parity checks with source-backed expected-vs-actual deltas for monsters, crafting, and other risk rows, cross-era change reviews such as moving content from Samurai Empire to Time of Legends behavior, named UO skill parity checks such as Magery or Blacksmithy, named spell parity checks such as Flamestrike or Blood Oath, named item property parity checks such as Spell Damage or Mage Armor, item property research, serialization reviews, and content implementation planning.

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

Ticket triage, parity-check, and content-taxonomy outputs are delivered as Markdown. Ticket triage turns one GitHub issue into an implementation plan with tiered UO source evidence, repository anchors, expected-vs-actual deltas, explicitly justified code changes, publish/era measurement checks, acceptance criteria, tests, and tracker recommendations; it only cites information verified in the repository, fetched from the internet, or supplied by the issue. Era parity reports require expected behavior, ModernUO evidence, concrete deltas, validation status, and impact for every non-present, low-confidence, monster, crafting, and user-focused risk row. Issue creation or issue-draft generation happens only when requested, with one independently actionable issue per discrepancy, gap, runtime blocker, or unresolved decision.

The plugin UI uses `plugins/modernuo/assets/rebirthuo-logo.png` through the manifest `interface.logo` and `interface.composerIcon` fields.
