# ModernUO Plugin

Version 3.4.0 packages 57 portable Agent Skills for official Ultima Online
research, ModernUO engineering, migration, testing, and governed RebirthUO
issue-to-pull-request delivery. It is distributed through the RebirthUO
marketplaces for Codex, Claude Code, and Cursor, while the skill source remains
usable by compatible Agent Skills hosts.

For the repository overview and maintainer validation workflow, see the
[root README](../../README.md). To choose a skill, use the
[skill catalog](skills/SKILL-CATALOG.md); use the
[portfolio routing guide](skills/PORTFOLIO-ROUTING.md) only for work that spans
owners.

## Install or discover

| Host | How to discover ModernUO |
| --- | --- |
| Codex | Use the RebirthUO marketplace declared in [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json). |
| Claude Code | Add the `RebirthUO/plugin` marketplace, then install `modernuo@rebirthuo-plugins`. |
| Cursor | Add this repository as a plugin marketplace; Cursor consumes [`.cursor-plugin/marketplace.json`](../../.cursor-plugin/marketplace.json). |
| Compatible Agent Skills host | Load the neutral packages under [`skills/`](skills/). |

Claude Code commands:

```text
/plugin marketplace add RebirthUO/plugin
/plugin install modernuo@rebirthuo-plugins
```

The versioned host metadata is kept in `.codex-plugin/`, `.claude-plugin/`, and
`.cursor-plugin/`. Do not edit an installed cache; change this reviewed source
and reinstall or refresh it through the host's normal marketplace workflow.

## Choose the right capability

The plugin has a narrow owner for each recurring concern:

- use `uo-official-evidence` for production gameplay behavior and
  `uo-publish-expansion-mapping` for Publish or expansion ownership;
- use `modernuo-codebase` to locate confirmed repository anchors, then select
  the focused ModernUO implementation, audit, migration, or testing owner;
- use `modernuo-gump-system` for gump composition and response safety;
- use `ultima-mcp` only for a bounded lookup of configured local Classic-client
  data;
- use `rebirthuo-issue-workflow` for a complete governed issue-to-PR route, or
  one of its child skills for a single phase.

Examples:

```text
Use $rebirthuo-issue-research to make this existing RebirthUO issue ready for
implementation with current official evidence.
```

```text
Use $modernuo-timers to review the ownership and cancellation of this recurring
game-time callback.
```

```text
Use $ultima-mcp to inspect the requested local Classic-client cliloc only if
an active UltimaMCP tool is available.
```

## Governed issue delivery

`rebirthuo-issue-workflow` coordinates a new request or existing issue through
the following sequence:

1. Resolve the exact repository from the consuming checkout's applicable
   `AGENTS.md`; fail closed when it is absent or ambiguous.
2. For a new issue, select a live template only when the request or project
   instructions require one. Otherwise use the canonical fallback format.
3. Research official behavior, compare the verified repository, and publish a
   format-preserving issue update. Unresolved behavior remains blocked rather
   than receiving an assumed default.
4. Implement only a current unblocked `READY` handoff in an isolated worktree,
   validate it, push a branch, and verify the pull request.

During intake and research, only existing live-verified labels directly
justified by the issue may be applied add-only. The workflow never creates,
renames, removes, or bulk-synchronizes labels; `blocked` remains the only
readiness-state label.

## UltimaMCP boundary

`ultima-mcp` is a read-only, optional client-data capability. It uses only an
explicitly active, documented UltimaMCP operation to inspect a narrow requested
datum such as tiles, art, gumps, clilocs, maps, hues, sounds, or patch metadata.
It reports the query, availability, and result as `ultima-mcp` evidence.

If the tool is unavailable, degraded, or inconclusive, the concrete client datum
remains unresolved. The skill does not install or configure UltimaMCP, expose
its localhost service, alter client files, or invent IDs. Client data does not
prove official gameplay behavior; route those claims to `uo-official-evidence`.

## Customize safely

- Keep `SKILL.md` concise; put conditional detail in `references/`.
- Keep `agents/interface.yaml`, `manifest.json`, and `evals/` aligned with the
  owning skill and preserve multilingual positive trigger coverage for new
  skills.
- Maintain all skill and metadata content in English.
- Never embed a consuming repository identity or local workstation path in a
  portable skill.
- Keep official gameplay evidence separate from community, client, emulator,
  and repository implementation evidence.

## Troubleshooting

| Situation | Expected behavior |
| --- | --- |
| No exact repository in applicable `AGENTS.md` | GitHub-mutating issue skills stop and request the repository identity. |
| No template is required | Intake proceeds with the governed fallback format without querying a template provider. |
| A selected label is missing or not clearly justified | Intake blocks without creating or modifying labels. |
| UltimaMCP is unavailable | Continue with verified non-MCP inputs where useful and mark the client datum unresolved. |
| Official gameplay evidence is incomplete | Keep the claim unresolved or request an explicit custom-policy choice. |

## Maintainer checks

From the repository root, validate each changed skill, its fixtures, metadata,
and resource links. See the [root validation instructions](../../README.md#validate-changes)
for the commands, then run `git diff --check` before committing.

## License

Licensed under the [MIT License](../../LICENSE).
