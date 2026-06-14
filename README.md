# UO ModernUO Agent Plugin

Repo-local template for sharing Ultima Online and ModernUO agent instructions across Cursor, Claude Code, Codex, and GitHub Copilot.

The plugin is domain-specific to UO/ModernUO work, but intentionally not tied to any single shard.

## Structure

- `AGENTS.md`: shared project instructions for agent-capable tools.
- `CLAUDE.md`: Claude Code entrypoint that imports `AGENTS.md`.
- `.cursor/rules/`: Cursor project rules.
- `.github/copilot-instructions.md`: GitHub Copilot repository-wide instructions.
- `.github/instructions/`: GitHub Copilot path-specific instructions.
- `uo-modernuo-agent-plugin/`: plugin root with Codex and Claude manifests plus shared skills.

## Validate

```powershell
python <path-to-plugin-creator>\scripts\validate_plugin.py .\uo-modernuo-agent-plugin
```
