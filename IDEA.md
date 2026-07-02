# Idea: Hermes Compatibility Plugin for AI Coding Assistants

The goal of this plugin is to make Hermes-style capabilities available to other AI coding assistants such as Claude, Codex, Cursor, and GitHub Copilot.

Hermes already provides a powerful skill-based workflow for structured research, documentation, source-code analysis, and project-specific automation. However, many development workflows also happen inside other tools and assistants. This plugin should bridge that gap by synchronizing relevant Hermes skills into the active project so that multiple AI assistants can operate with the same domain knowledge, rules, and workflows.

The initial focus is on Ultima Online related projects, especially UO, ModernUO, and RebirthUO. Skills related to these domains should be made available inside the repository so that any supported assistant can use them consistently when working on research, documentation, parity checks, code analysis, implementation planning, or gap detection.

A scheduled synchronization process should be used to keep the project up to date. A cron job will regularly copy or update the internal Hermes skills that are relevant to Ultima Online, ModernUO, RebirthUO, or the current project context. This ensures that the repository always contains the latest shared instructions, research rules, documentation workflows, and implementation guidelines.

The plugin should not duplicate logic unnecessarily. Instead, it should act as a compatibility and synchronization layer between Hermes and other AI-assisted development environments. The repository becomes the shared context source, while each assistant can consume the synchronized skills in its own supported format.

## Goals

* Provide Hermes-like workflows to Claude, Codex, Cursor, and GitHub Copilot.
* Synchronize project-relevant Hermes skills into the repository.
* Keep Ultima Online, ModernUO, and RebirthUO related skills available to all supported assistants.
* Use a cron-based synchronization process to keep skills up to date.
* Create a shared source of truth for research, documentation, parity checks, source-code comparison, and implementation planning.
* Reduce duplicated prompts and inconsistent assistant behavior across tools.

## Initial Scope

The first version should focus on synchronizing skills related to:

* Ultima Online research
* Broadsword / official UO documentation
* ModernUO source-code analysis
* RebirthUO project-specific extensions
* Era and system parity checks
* Documentation generation
* Gap reports between documentation and implementation

## Long-Term Vision

Over time, this plugin should become a general compatibility layer that allows Hermes skills to be reused across multiple AI development environments. Instead of maintaining separate instructions for every assistant, the project should define its workflows once and make them available everywhere.

This would allow developers to move between Hermes, Claude, Codex, Cursor, and GitHub Copilot while preserving the same project context, quality standards, documentation structure, and implementation rules.
