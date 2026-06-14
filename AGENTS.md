# UO ModernUO Agent Instructions

## Purpose

This repository contains the repo-local `uo-modernuo-agent-plugin` structure and shared guidance for Ultima Online shard and ModernUO server development across Cursor, Claude Code, Codex, and GitHub Copilot.

## Compatibility Map

- Codex reads `AGENTS.md` and uses `uo-modernuo-agent-plugin/.codex-plugin/plugin.json`.
- Claude Code reads `CLAUDE.md`; load the plugin locally with `claude --plugin-dir ./uo-modernuo-agent-plugin`.
- Cursor reads `AGENTS.md` and `.cursor/rules/*.mdc`.
- GitHub Copilot reads `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, and agent instruction files such as `AGENTS.md`.

## Working Rules

- Keep the plugin name `uo-modernuo-agent-plugin` in folder names, manifests, and documentation.
- Keep guidance specific to Ultima Online and ModernUO, but not specific to any single shard.
- Prefer ModernUO upstream conventions and C#/.NET idioms when instructions mention implementation behavior.
- Preserve UO gameplay semantics, persistence and serialization behavior, command access levels, map/world state, and save/load compatibility unless a task explicitly changes them.
- Avoid shard-specific names, branding, URLs, or assumptions in reusable plugin files.
- Keep the v1 structure repo-local. Do not add marketplace files unless explicitly requested.
- Keep v1 focused on skills and rules. Do not add MCP servers, hooks, app manifests, generated assets, screenshots, or placeholder integrations without a concrete implementation request.
- Keep the Codex and Claude plugin manifests aligned for shared metadata.
- Prefer concise, actionable instructions over broad style guides.
- Validate plugin changes before handing work back.

## Validation

Run this from the repository root after plugin edits:

```powershell
python <path-to-plugin-creator>\scripts\validate_plugin.py .\uo-modernuo-agent-plugin
```
