# ModernUO Plugin

ModernUO is a Codex plugin for RebirthUO development. It packages focused skills for ModernUO server implementation, Ultima Online domain research, migration work, subsystem audits, cross-era content change routing, named UO skill, spell, and item property parity checks, and content parity checks.

## Contents

- `.codex-plugin/plugin.json` defines the plugin manifest and Codex UI metadata.
- `assets/rebirthuo-logo.png` provides the plugin logo and composer icon.
- `skills/` contains ModernUO and Ultima Online guidance skills for code review, migration, cross-era content change gates, named skill, spell, and item property parity checks, content systems, combat, crafting, persistence, networking, regions, quests, housing, and related workflows.
- `reports/` contains generated discovery and analysis reports.

## Usage

Install or load the plugin through the configured local marketplace, then ask Codex for ModernUO or RebirthUO help by topic. Example requests include migration guidance, subsystem audits, era parity checks, cross-era change reviews such as moving content from Samurai Empire to Time of Legends behavior, named UO skill parity checks such as Magery or Blacksmithy, named spell parity checks such as Flamestrike or Blood Oath, named item property parity checks such as Spell Damage or Mage Armor, item property research, serialization reviews, and content implementation planning.

Parity-check and content-taxonomy parity reports are delivered as Markdown and include an option to turn findings into single sliced issues. Issue creation or issue-draft generation happens only when requested, with one independently actionable issue per discrepancy, gap, runtime blocker, or unresolved decision.

The plugin UI uses `assets/rebirthuo-logo.png` through the manifest `interface.logo` and `interface.composerIcon` fields.
