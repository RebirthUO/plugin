# ModernUO Plugin

The `modernuo` plugin packages 72 English Agent Skills for official Ultima
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

1. `modernuo-issue-template-gate` snapshots the verified repository's live
   Issue Templates and asks the user whenever no single form fits.
2. `modernuo-issue-create` reads the exact GitHub repository from the consuming
   project's applicable `AGENTS.md`, requires the gate's fresh `TemplatePacket`,
   and produces or creates an `IntakePacket`.
3. `modernuo-issue-research` establishes official behavior, inspects the same
   verified repository, and produces a `ResearchPacket`. It asks focused
   questions and stops whenever a behavior-changing fact or policy is unresolved.
4. `modernuo-issue-implement` accepts only a current `READY` research handoff,
   verifies the configured repository, checkout, and push remote, then
   implements and tests the smallest approved change.
5. `modernuo-issue-workflow` coordinates the complete path. A user-identified
   existing issue bypasses issue creation; the workflow interviews every blocker
   until research is ready, then uses an isolated worktree, pushes a scoped
   branch, and creates or updates a PR.

No phase infers a repository from the cwd, remotes, organization, neighboring
project, issue number, stale documentation, or memory. If project instructions
do not declare one unambiguous `owner/repository` or canonical GitHub URL, the
workflow fails closed and asks the user.

`uo-official-evidence` owns source authority. `uo-living-world-review` checks
cross-system player consequences. `modernuo-codebase`, the engine/domain skills,
and `modernuo-test-workflow` support implementation without creating a second
implicit workflow.

## Contents

- `plugins/modernuo/.codex-plugin/plugin.json` - Codex manifest and UI metadata.
- `plugins/modernuo/.claude-plugin/plugin.json` - Claude Code manifest.
- `plugins/modernuo/.cursor-plugin/plugin.json` - Cursor manifest.
- `.agents/`, `.claude-plugin/`, and `.cursor-plugin/` - marketplace metadata.
- `plugins/modernuo/skills/` - 72 flat skill packages, grouped by frontmatter.
- [`SKILL-CATALOG.md`](plugins/modernuo/skills/SKILL-CATALOG.md) - generated
  workflow and skill index.
- `scripts/` - deterministic preparation, catalog, verification, Yao, and
  Hermes-preview tooling.
- `reports/` - generated validation evidence and the consolidation ledger.

Each skill keeps `SKILL.md` focused on trigger boundaries, procedure, output,
and verification. Conditional detail belongs in `references/`; generated
adapter metadata lives in `agents/interface.yaml`, `manifest.json`, and `evals/`.

## Source-backed domain coverage

The portfolio includes focused owners for recurring ModernUO source domains:

- `uo-spawners-world-population` - spawner runtime, JSON packages,
  import/export, identity, persistence, cleanup, and sector caching;
- `uo-vendors-commerce` - NPC stock and buy/sell transactions plus
  player-vendor listings, proceeds, recovery, packets, and lifecycle;
- `uo-pets-taming-stables` - taming, controlled ownership and follower slots,
  pet orders and transfer, stabling, login/logout, and cleanup;
- `uo-factions-towns-sigils` - Factions membership/ranks, elections/offices,
  towns, sigils/monoliths, silver/tax economy, and persistence.

`uo-items-foundation` also owns item-loss transitions through death/corpses,
stealing, blessing, and insurance. These skills use current ModernUO code,
data, and tests as implementation evidence while routing official gameplay
claims through `uo-official-evidence`.

## Source and synchronization

The reviewed source is:

```text
plugins/modernuo/skills/
```

Do not hand-edit an installed Codex or Hermes cache. Validate this checkout
first. To preview a Hermes profile synchronization:

```powershell
python scripts/sync-plugin-to-hermes.py `
  --hermes-root <profile-skills> `
  --dry-run
```

Run the real synchronization only as a separately authorized action after all
gates pass.

## Quality workflow

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/prepare-yao-portfolio.py
python scripts/generate-skill-catalog.py
python scripts/verify-skill-portfolio.py
python scripts/run-yao-portfolio.py `
  --yao-root <path-to-yao-meta-skill> `
  --extended
```

The checks cover structure, metadata, resource boundaries, English-only
contracts, repository portability, removed-skill references, trigger cases,
Skill IR, runtime conformance, and static trust checks. Local gates are not
provider-backed execution, human blind review, native permission enforcement,
or live telemetry.

## Typical requests

- create a template-conformant intake issue in the repository declared by the
  consuming project;
- take a new request or an existing issue through official research, blocker
  interviews, isolated implementation, branch push, and pull request creation;
- deeply research an issue and stop for unresolved official behavior;
- implement a current research-ready issue with focused tests;
- audit a ModernUO subsystem, serialization migration, lifecycle, or hot path;
- migrate RunUO/ServUO code to current ModernUO conventions;
- compare a named UO mechanic with official evidence and repository state;
- review economy, PvP/PvM, housing, client, save, or player-trust effects.

For Claude Code:

```text
/plugin marketplace add RebirthUO/plugin
/plugin install modernuo@rebirthuo-plugins
```

For Cursor, add this repository as a plugin marketplace. Cursor consumes the
same neutral Agent Skills payload through `.cursor-plugin/marketplace.json`.
