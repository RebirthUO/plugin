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
- Use `modernuo-server-lifecycle` for startup, bootstrap phases, first-boot prompts, shutdown, and production-vs-test lifecycle differences.
- Use `modernuo-pathfinding` for creature movement, `PathFollower`, `BitmapAStarAlgorithm`, `StepCache`, `.swb` cache files, and pathfinding diagnostics.
- Use `modernuo-world-saves-archives` for backup, restore, archive rollup, journal recovery, and `WorldSavePostSnapshot` work.
- Keep `modernuo/.codex-plugin/plugin.json` and `modernuo/.claude-plugin/plugin.json` aligned for shared identity fields: `name`, `version`, `description`, and `author`.
- Keep this skill instruction-only unless a concrete script, hook, MCP server, or app integration is requested.
- Do not add marketplace entries, MCP config, hooks, app manifests, logos, screenshots, or placeholder assets unless the request explicitly asks for them.
- After changing the plugin structure, run the Codex plugin validator before reporting completion.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## Validation

Run this from the repository root after edits:

```powershell
python <path-to-plugin-creator>\scripts\validate_plugin.py .\modernuo
```
