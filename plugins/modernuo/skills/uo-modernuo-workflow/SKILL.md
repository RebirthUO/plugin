---
name: uo-modernuo-workflow
description: Use when working on Ultima Online or ModernUO projects, shared UO/ModernUO agent instructions, or compatibility across Cursor, Claude, Codex, and GitHub Copilot.
---

# UO ModernUO Workflow

Use this skill when a task touches Ultima Online shard work, ModernUO server development, the shared plugin, or tool-specific adapters.

## Workflow

- Read the repository-level guidance first: `AGENTS.md`, then any tool-specific file that applies to the current surface.
- Treat the scope as Ultima Online and ModernUO project guidance, not guidance for a single shard or brand.
- Prefer ModernUO upstream conventions and C#/.NET idioms when working in server code.
- Preserve UO gameplay semantics, persistence and serialization behavior, command access levels, map/world state, and save/load compatibility unless a task explicitly changes them.
- Avoid hardcoding shard-specific names, URLs, branding, or assumptions in reusable plugin guidance.
- Keep `modernuo/.codex-plugin/plugin.json` and `modernuo/.claude-plugin/plugin.json` aligned for shared identity fields: `name`, `version`, `description`, and `author`.
- Keep this skill instruction-only unless a concrete script, hook, MCP server, or app integration is requested.
- Do not add marketplace entries, MCP config, hooks, app manifests, logos, screenshots, or placeholder assets unless the request explicitly asks for them.
- After changing the plugin structure, run the Codex plugin validator before reporting completion.

## Validation

Run this from the repository root after edits:

```powershell
python <path-to-plugin-creator>\scripts\validate_plugin.py .\modernuo
```
