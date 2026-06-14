# UO ModernUO Copilot Instructions

This repository contains a repo-local Ultima Online and ModernUO agent plugin structure for Cursor, Claude Code, Codex, and GitHub Copilot.

Follow `AGENTS.md` for shared project guidance. Treat `uo-modernuo-agent-plugin/` as the plugin root.

Keep guidance specific to Ultima Online and ModernUO, but not specific to any single shard.

When changing plugin metadata, keep these files aligned:

- `uo-modernuo-agent-plugin/.codex-plugin/plugin.json`
- `uo-modernuo-agent-plugin/.claude-plugin/plugin.json`

Do not add marketplace configuration, MCP servers, hooks, app manifests, generated assets, screenshots, or placeholder integrations unless explicitly requested.

After changing the plugin structure, validate with:

```powershell
python <path-to-plugin-creator>\scripts\validate_plugin.py .\uo-modernuo-agent-plugin
```
