---
name: ultima-mcp
description: Use when a configured and active Kita72/UltimaMCP server is needed to inspect local Ultima Online Classic client data, including tiles, maps, map renders, art, Gumps, hues, textures, lights, fonts, sounds, animations, multis, skills, clilocs, speech, or patch metadata. Query only an explicitly available UltimaMCP tool through its documented interface, return source-marked read-only client evidence, and keep it separate from official UO gameplay evidence. Do not use to install, configure, expose, or mutate UltimaMCP or game files; use uo-official-evidence for gameplay facts.
metadata:
  version: "1.0.0"
---

# UltimaMCP Client Data

## Boundary

Use a configured, active UltimaMCP only to inspect local Classic-client data.
Treat each result as `ultima-mcp`/client evidence, not as official OSI, EA, or
Broadsword gameplay evidence. Route player-facing mechanics and historical
claims to `uo-official-evidence`.

Do not install or configure the MCP server, invoke undocumented endpoints,
assume tool names, expose the localhost service, modify game files, or attach
to a live client process.

## Workflow

1. Confirm that the active tool catalog explicitly identifies UltimaMCP and
   exposes a documented operation relevant to the narrow requested datum. If it
   is absent, inaccessible, degraded, or lacks that operation, use the fallback
   below.
2. Identify the exact client-data domain and bound the request to the smallest
   useful ID, coordinate, search text, language, range, or render target. Do
   not broaden a search merely to produce a candidate.
3. Use only the exposed read-only MCP operation and its documented input shape.
   Check the available health, diagnostics, or file-status operation first when
   the requested data may be unavailable due to an incomplete local client
   installation.
4. Record the tool identity, narrow query, returned record or asset locator,
   availability/degraded state, and any server-reported limits. Do not embed or
   claim unavailable PNG/WAV content when the server supplies a URL instead.
5. Classify the result as `ultima-mcp` evidence. Keep screenshots,
   repositories, user input, tests, and official sources as separate evidence
   records. A client string, art ID, tile flag, map location, or patch record
   does not establish an official gameplay rule.
6. Hand off client findings to the owning skill when the request also concerns
   UI, implementation, or gameplay. For Gump work, hand off resolved or
   unresolved art/cliloc candidates to `modernuo-gump-system`; it owns layout,
   response safety, and visual composition.

## Transparent fallback

When UltimaMCP is unavailable, inaccessible, degraded, inconclusive, or cannot
answer the request, continue with verified non-MCP inputs where that remains
useful. Mark the concrete client datum `unresolved`; never invent asset IDs,
cliloc text, artwork, map details, tile properties, sounds, or mechanics.
Do not substitute a web search for a missing local-client lookup unless the
user separately asks for web research, and label any such evidence separately.

## Output contract

Return these fields in order:

- `Outcome`: `REVIEWED` when the lookup or transparent fallback is complete, or
  `BLOCKED` only when the requested conclusion cannot proceed without the
  smallest missing client, repository, or official-evidence input.
- `Repository revision`: the inspected revision or `null` for a client-only
  lookup.
- `Decision`: requested domain, query scope, selected operation, and the
  resulting handoff or unresolved disposition.
- `Evidence`: a record for every MCP query with class `ultima-mcp`, tool/asset
  locator, availability state, and supported claim.
- `Verification`: the documented-operation or health/diagnostics check and its
  result; keep MCP data and official-evidence verification separate.
- `Confidence`: calibrated to the tool availability, query specificity, and
  directness of the returned data.
- `Limitations`: missing local files, degraded capabilities, unresolved IDs,
  server limits, and every gameplay claim that still needs official evidence.

## Verification

- A missing active UltimaMCP tool produces a transparent fallback, never an
  assumed local service or a fabricated client result.
- A tool result identifies the narrow query and is labeled `ultima-mcp`.
- A gameplay conclusion cites separate official evidence or remains unresolved.
- A Gump request retains Gump-skill ownership after the client-data handoff.

## Portable evidence

Use `evals/behavior_cases.json` to preserve the active-tool gate, read-only
boundary, transparent fallback, evidence-class separation, and Gump handoff.
Before completion, run `python scripts/validate-modernuo-skill-evals.py
plugins/modernuo/skills/ultima-mcp`. When a Codex CLI runtime is available,
also run `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir
<external-output-dir> plugins/modernuo/skills/ultima-mcp` and report its
summary; otherwise state the runtime-evaluation limitation.
