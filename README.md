# ModernUO Agent Skills

`modernuo` is a portable Agent Skills plugin for official Ultima Online research,
ModernUO engineering, RunUO migration, testing, and governed RebirthUO
issue-to-pull-request delivery. Version 3.4.0 ships 57 English skill packages
for Codex, Claude Code, Cursor, and compatible Agent Skills hosts.

## Start here

- Read the [ModernUO plugin guide](plugins/modernuo/README.md) for installation,
  invocation examples, workflow behavior, and troubleshooting.
- Browse the generated [skill catalog](plugins/modernuo/skills/SKILL-CATALOG.md)
  to find the narrowest owner for a request.
- Use the [portfolio routing guide](plugins/modernuo/skills/PORTFOLIO-ROUTING.md)
  only when work crosses a skill boundary.

## What the plugin provides

The portfolio covers:

- official OSI, EA, and Broadsword gameplay research, Publish-to-expansion
  mapping, and evidence-gated parity work;
- ModernUO implementation, code audits, content, commands, gumps, networking,
  persistence, timers, lifecycle, regions, testing, and performance work;
- focused RunUO/ServUO migration routes and cross-cutting migration planning;
- RebirthUO issue intake, research, implementation, and end-to-end delivery;
- read-only local Classic-client data lookup through `ultima-mcp` when an active
  UltimaMCP tool is explicitly available.

The reviewed source of truth is [plugins/modernuo/skills](plugins/modernuo/skills).
Do not edit an installed plugin cache.

## Evidence boundary

Only official OSI, EA, and Broadsword material establishes expected Ultima
Online gameplay behavior. Repository code, emulator sources, community pages,
client assets, and UltimaMCP results can establish implementation or client-data
facts, but never silently establish official mechanics. When official evidence
is missing or conflicts, the relevant claim remains unresolved until an
explicit custom-policy decision is provided.

`ultima-mcp` is deliberately narrower: it uses only a configured, active,
read-only UltimaMCP operation for local Classic-client data. It does not install
or configure UltimaMCP, modify game files, expose a service, or replace official
gameplay research.

## Supported hosts

| Host | Distribution metadata | Notes |
| --- | --- | --- |
| Codex | [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) and [Codex manifest](plugins/modernuo/.codex-plugin/plugin.json) | Install or enable `modernuo` from the RebirthUO marketplace. |
| Claude Code | [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) | Use the marketplace commands below. |
| Cursor | [.cursor-plugin/marketplace.json](.cursor-plugin/marketplace.json) | Add this repository as a plugin marketplace. |
| Compatible Agent Skills hosts | [skills directory](plugins/modernuo/skills) | Consume the neutral Agent Skills packages and their local metadata. |

For Claude Code:

```text
/plugin marketplace add RebirthUO/plugin
/plugin install modernuo@rebirthuo-plugins
```

## Use a skill

Choose the narrowest skill named by the request or catalog. For example:

```text
Use $rebirthuo-issue-workflow to take this existing RebirthUO issue from
official research through a verified pull request.
```

```text
Use $modernuo-gump-system to plan this gump from the screenshot. If local
client art is needed, use the available $ultima-mcp capability first.
```

The governed issue workflow resolves the exact GitHub repository only from the
consuming project's applicable `AGENTS.md`. It never infers a repository from a
current directory, remote, organization, issue number, neighboring project, or
memory. New issue intake uses a live template only when the request or project
instructions require one; otherwise it uses the documented fallback format.

## Repository layout

```text
plugins/modernuo/
  .codex-plugin/        Codex manifest
  .claude-plugin/       Claude Code manifest
  .cursor-plugin/       Cursor manifest
  skills/               reviewed Agent Skills source
    SKILL-CATALOG.md     generated inventory
    PORTFOLIO-ROUTING.md cross-skill ownership map
```

## Validate changes

Run validation from this repository root. For each changed skill, first run the
runtime validator and the package fixture check:

```powershell
python C:\path\to\skill-creator\scripts\quick_validate.py `
  plugins\modernuo\skills\<skill-name>
python scripts\validate-modernuo-skill-evals.py `
  plugins\modernuo\skills\<skill-name>
```

When the Codex CLI runtime is available, forward-test declared behavior cases
without writing artifacts into the repository:

```powershell
python scripts\run-modernuo-skill-runtime-smoke.py `
  --output-dir <external-output-dir> `
  plugins\modernuo\skills\<skill-name>
```

Also parse changed JSON/YAML metadata, inspect referenced resources and trigger
fixtures, and run `git diff --check`. Keep the three host manifests on the same
plugin version whenever the plugin changes.

## License

This repository is licensed under the [MIT License](LICENSE).
