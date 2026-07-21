# ModernUO Plugin

The `modernuo` plugin packages 56 English Agent Skills for official Ultima
Online research, ModernUO engineering, RunUO migration, testing, and a strict
template-gated issue-to-PR workflow. It is distributed for Codex, Claude Code, Cursor,
and compatible Agent Skills runtimes.

## Purpose

The plugin treats OSI/EA/Broadsword official-server material as the only
authority for expected UO gameplay. Community pages, client data, emulators, and
repository code can locate evidence or prove implementation state, but cannot
silently define official mechanics. Missing or conflicting official evidence
remains unresolved until the user supplies an explicit custom-policy decision.

## Issue-to-PR workflow

1. `rebirthuo-issue-template-gate` snapshots the verified repository's live
   Issue Templates, accepts research placeholders, and asks only on genuine
   template or user-intent ambiguity.
2. `rebirthuo-issue-create` reads the exact GitHub repository from the consuming
   project's applicable `AGENTS.md`, requires the gate's fresh `TemplatePacket`,
   produces or creates an `IntakePacket`, then asks once about research only in
   standalone mode.
3. `rebirthuo-issue-research` exhausts materially different official research
   routes, infers era when evidence permits, inspects the same
   verified repository, and rewrites the issue body under its existing headings.
   It replaces obsolete claims, removes resolved `RESEARCH_REQUIRED` markers and
   blocker text, never appends a research report, toggles the `blocked` label
   only while blockers remain, and produces a `ResearchPacket`. It asks focused
   questions only when a genuine product/custom-policy choice remains.
4. `rebirthuo-issue-implement` accepts only a current unblocked `READY` handoff,
   verifies the configured repository, checkout, and push remote, then
   implements and tests the smallest approved change.
5. `rebirthuo-issue-workflow` coordinates the complete path without repeated
   phase confirmation. Existing issues bypass creation; implementation gaps
   return through research before user questions, then resume from fresh READY.

No phase infers a repository from the cwd, remotes, organization, neighboring
project, issue number, stale documentation, or memory. If project instructions
do not declare one unambiguous `owner/repository` or canonical GitHub URL, the
workflow fails closed and asks the user.

`uo-official-evidence` owns source authority. `modernuo-codebase`, the
engineering/domain skills, and `modernuo-test-workflow` support implementation
without creating a second implicit workflow. Cross-skill ownership is defined
in `plugins/modernuo/skills/PORTFOLIO-ROUTING.md`.

## Contents

- `plugins/modernuo/.codex-plugin/plugin.json` - Codex manifest and UI metadata.
- `plugins/modernuo/.claude-plugin/plugin.json` - Claude Code manifest.
- `plugins/modernuo/.cursor-plugin/plugin.json` - Cursor manifest.
- `.agents/`, `.claude-plugin/`, and `.cursor-plugin/` - marketplace metadata.
- `plugins/modernuo/skills/` - reviewed flat skill packages.
- `plugins/modernuo/skills/PORTFOLIO-ROUTING.md` - portable owner and handoff
  map for cross-cutting requests.

Each skill keeps `SKILL.md` focused on trigger boundaries, procedure, output,
and verification. Conditional detail belongs in `references/`; generated
adapter metadata lives in `agents/interface.yaml`, `manifest.json`, and `evals/`.
Skills are authored in English and match intent across user languages; new
skills include representative multilingual positive trigger fixtures.

The configuration, code-audit, codebase, and commands/targeting skills provide
explicit blocked outcomes, evidence and confidence reporting, and only route to
present, purpose-matched sibling skills.

## Source-backed domain coverage

The portfolio includes focused owners for recurring ModernUO source domains:

- `modernuo-migrate-commands-events`, `modernuo-migrate-gumps`,
  `modernuo-migrate-items-mobiles`, `modernuo-migrate-packets`,
  `modernuo-migrate-persistence`, `modernuo-migrate-property-lists`,
  `modernuo-migrate-serialization`, `modernuo-migrate-systems`, and
  `modernuo-migrate-timers` - revision-bound RunUO migration workflows with
  fail-closed evidence gates, stable result states, focused behavior fixtures,
  and explicit compatibility and validation reporting;

- `modernuo-timers` - game-loop delays and recurrence, API selection,
  cancellation ownership, callback validity, deadline restoration, precision,
  failure behavior, and focused timer/lifecycle verification;
- `modernuo-gump-system` - screenshot- and description-led ModernUO gump
  planning and implementation with source-marked component inventories,
  optional user-enabled Ultima MCP lookups, annotated visual concepts, and
  response-safety verification;
- `skill-scanner` - revision-bound, read-only portfolio triage
  after repository changes: maintenance leads, declared routes, scope-overlap
  warnings, and user-approved capability candidates;
- `modernuo-item-properties` - complete item-property contracts across storage,
  mechanics, Object Property List output, era gates, persistence, and focused
  behavior tests;
- `modernuo-property-lists` - localized tooltip entries, interpolation argument
  shape, order, chunked free text, refresh invalidation, and focused OPL tests;
- `modernuo-threading` - event-loop ownership, worker-thread boundaries,
  parallel-save purity, cancellation/shutdown analysis, fail-closed evidence
  handling, and deterministic confidence-bearing verification reports;
- `modernuo-world-saves-archives` - revision-bound world-save scheduling,
  snapshot completion, concurrency, shutdown/crash recovery, save-path safety,
  and inspected external backup integrations without assuming custom archive
  contracts;
- `modernuo-migrate-foundation` - cross-cutting RunUO/ServUO migration
  inventory, evidence classification, compatibility gates, terminal states,
  and mode-appropriate verification;
- `uo-publish-expansion-mapping` - official Publish chronology, forward mapping
  to the next true expansion, cumulative ModernUO gates, and strict separation
  of Endless Journey account restrictions from the TOL era;
- `uo-official-evidence` - current and historical OSI/EA/Broadsword gameplay
  research with explicit source classes, production-third-party corroboration,
  engine implementation comparison, and unresolved-evidence gates;
The routing guide lists only the installed owners. Requests that need an absent
domain owner stay with confirmed local evidence or stop for explicit scope;
they do not silently route to an implied package. These skills use current
ModernUO code, data, and tests as implementation evidence while routing official
gameplay claims through `uo-official-evidence`.

- `modernuo-quest-systems`, `modernuo-crafting-systems`,
  `modernuo-spell-systems`, `modernuo-housing-multis`,
  `modernuo-faction-systems`, `modernuo-vendor-systems`, and
  `modernuo-player-skill-systems` - portable, evidence-gated workflows for
  their respective domain lifecycles. They inspect the consuming checkout at
  execution time and do not embed a repository identity or local path.

## Source and synchronization

The reviewed source is:

```text
plugins/modernuo/skills/
```

Do not hand-edit an installed plugin cache. Validate this reviewed checkout
first. Skills remain repository-portable: inspect the consuming repository and
its pinned revision before relying on version-sensitive APIs or local docs.

## Quality workflow

```powershell
python C:\Users\Jsiem\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  plugins\modernuo\skills\<skill-name>
```

Also parse JSON/YAML metadata, inspect trigger fixtures, and run
`git diff --check`. Legacy portfolio preparation, Yao, and Hermes steps are not
part of the skill-local validation workflow.

Run the portable fixture smoke check for one or more skill packages:

```powershell
python scripts/validate-modernuo-skill-evals.py `
  plugins/modernuo/skills/<skill-name>
```

When the Codex CLI is available, forward-test the declared behavior cases in a
read-only runtime. The smoke exercises direct, paraphrased, competing-scope,
and incomplete-context prompt variants. Keep response artifacts outside the
repository and include their result, runner SHA-256 (or the explicit runtime
limitation) in the final report:

```powershell
python scripts/run-modernuo-skill-runtime-smoke.py `
  --output-dir <external-output-dir> `
  plugins/modernuo/skills/<skill-name>
```

## Typical requests

- create a template-conformant intake issue in the repository declared by the
  consuming project;
- take a new request or an existing issue through official research, blocker
  interviews, isolated implementation, branch push, and pull request creation;
- deeply research or review an issue, rewrite its existing fields with current
  findings, clean resolved requirements/blockers, and stop for unresolved
  official behavior;
- implement a current research-ready issue with focused tests;
- audit a ModernUO subsystem, serialization migration, lifecycle, or hot path;
- implement or audit an owned ModernUO timer, including cancellation,
  persistence restoration, callback guards, and focused tests;
- decompose a ModernUO Gump screenshot or visual brief into evidence-marked
  components, optionally resolve available Ultima UI data, and produce an
  annotated implementation wireframe before code;
- map a UO Publish to its next applicable true expansion and cumulative
  ModernUO `Core` gate without treating Endless Journey as an expansion;
- migrate RunUO/ServUO code to current ModernUO conventions;
- plan or audit a cross-cutting RunUO/ServUO migration while preserving saved
  state, type identity, lifecycle ownership, and era decisions;
- compare a named UO mechanic with official evidence and repository state;
- review economy, PvP/PvM, housing, client, save, or player-trust effects.

For Claude Code:

```text
/plugin marketplace add RebirthUO/plugin
/plugin install modernuo@rebirthuo-plugins
```

For Cursor, add this repository as a plugin marketplace. Cursor consumes the
same neutral Agent Skills payload through `.cursor-plugin/marketplace.json`.
