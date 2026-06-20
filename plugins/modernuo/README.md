# ModernUO Plugin

ModernUO is a Codex plugin for RebirthUO development. It packages focused skills for ModernUO server implementation, Ultima Online domain research, migration work, subsystem audits, named UO skill, spell, and item property parity checks, and content parity checks.

## Contents

- `.codex-plugin/plugin.json` defines the plugin manifest and Codex UI metadata.
- `assets/rebirthuo-logo.png` provides the plugin logo and composer icon.
- `skills/` contains ModernUO and Ultima Online guidance skills for code review, migration, named skill, spell, and item property parity checks, content systems, combat, crafting, persistence, networking, regions, quests, housing, and related workflows.
- `reports/` contains generated discovery and analysis reports.

## Usage

Install or load the plugin through the configured local marketplace, then ask Codex for ModernUO or RebirthUO help by topic. Example requests include migration guidance, subsystem audits, era parity checks, named UO skill parity checks such as Magery or Blacksmithy, named spell parity checks such as Flamestrike or Blood Oath, named item property parity checks such as Spell Damage or Mage Armor, item property research, serialization reviews, and content implementation planning.

The plugin UI uses `assets/rebirthuo-logo.png` through the manifest `interface.logo` and `interface.composerIcon` fields.
