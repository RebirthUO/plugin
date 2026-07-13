# Changelog

## 2.3.1 - 2026-07-13

- Changed `modernuo-issue-research` scoped publication to body-only updates on
  the `## Research contract` section; research runs no longer post issue
  comments.
- Made the `blocked` label a scoped publication action: add on `BLOCKED`,
  remove on `READY`.
- Updated `modernuo-issue-workflow`, `modernuo-issue-implement`, and their
  references to require body-only publication evidence and no `blocked` label
  before implementation may start.

## 2.3.0 - 2026-07-13

- Extended `modernuo-issue-research` so every completed research run publishes
  findings back to the GitHub issue: a structured `## Research contract` body
  section plus an append-only research comment per run.
- Made scoped issue publication implicit for verified issues during research;
  advice-only requests remain the read-only exception.
- Updated `modernuo-issue-workflow` and `modernuo-issue-implement` to require
  post-publication issue revisions and documented contract evidence before
  implementation may start.

## 2.2.0 - 2026-07-12

- Restored `modernuo-issue-template-gate` as a first-class, zero-mutation live
  Issue Template selection gate and added `modernuo-issue-workflow` for the
  complete template-to-PR orchestration path.
- Made the new workflow invoke the template gate before `modernuo-issue-create`,
  skip issue creation when the user points to an existing issue, and loop through
  focused interviews until a current research-ready handoff has complete
  official-evidence clarity.
- Required isolated implementation worktrees, scoped branch push, and verified
  PR read-back after a `READY` research handoff; newly discovered unknowns return
  to research rather than defaulting.
- Added portfolio checks, cataloging, inventory, synchronization, and trigger
  fixtures that keep the four workflow skills connected and prevent retirement
  metadata from silently dropping the template gate.

## 2.1.0 - 2026-07-12

- Added source-backed `uo-spawners-world-population`,
  `uo-vendors-commerce`, `uo-pets-taming-stables`, and
  `uo-factions-towns-sigils` production skills with conditional architecture,
  lifecycle, transaction, persistence, and verification references.
- Extended `uo-items-foundation` with death/corpse disposition, stealing,
  blessing, insurance, criminality, and player-trust exploit checks instead of
  creating an overlapping item-loss skill.
- Tightened routing between world/region, content, skill/stat, BOD, housing,
  networking, vendor, pet, spawner, and Factions owners and added realistic
  collision trigger cases.
- Corrected content-taxonomy claims that referenced Peerless, Imbuing, or
  Throwing implementation surfaces absent from current ModernUO main; these now
  remain research-needed until official and repository evidence supports a
  stronger status.
- Regenerated the 70-skill catalog and Yao production artifacts.

## 2.0.0 - 2026-07-12

- Replaced overlapping RebirthUO/direct-ModernUO issue routes with three public
  phases: `modernuo-issue-create`, `modernuo-issue-research`, and
  `modernuo-issue-implement`.
- Made GitHub repository resolution project-configured: issue workflows now read
  the exact repository from applicable `AGENTS.md` instructions and fail closed
  when it is missing, ambiguous, or mismatched.
- Added strict `IntakePacket`, `ResearchPacket`, and `ImplementationResult`
  handoffs. Research and implementation stop for unresolved behavior instead
  of selecting defaults.
- Added `uo-official-evidence`; only OSI/EA/Broadsword official material can
  establish expected gameplay. Community, client, emulator, and repository
  evidence remain separately classified.
- Added repository-agnostic `modernuo-codebase` navigation and moved
  cross-system product effects into `uo-living-world-review`.
- Removed 12 duplicate, project-specific, or broad routing skills and retired
  ticket/session snapshots and duplicate property case files.
- Consolidated test and verification references into portable, current
  contracts; removed hard-coded workstation paths and repository targets.
- Made the complete payload and generated contracts English-only, updated
  trigger routing, and regenerated the 66-skill catalog and Yao artifacts.

## 1.21.0 - 2026-07-12

- Rebased the plugin onto `origin/main`, superseding the outdated automated 1.20.0 Hermes sync with the authoritative local skill-portfolio overhaul.
- Reorganized the 75-skill portfolio into UO, ModernUO, and RebirthUO groups via frontmatter (`skill_group`, `skill_subgroup`, `workflow_phase`, `workflow_tier`).
- Added [`plugins/modernuo/skills/SKILL-CATALOG.md`](plugins/modernuo/skills/SKILL-CATALOG.md) with agent workflow tables, migrate pairs, and deprecated-skill redirects.
- Documented the primary agentic path: `rebirthuo-issue-create` → `rebirthuo-issue-review` → `rebirthuo-implement` on `RebirthUO/ModernUO`.
- Removed duplicate `ultima-online-product-model` and deprecated `rebirthuo-implementation`; merged implementation guidance into `rebirthuo-implement`.
- Fixed ghost references to removed skills (`modernuo-ticket-triage`, `uo-domain-research`, `modernuo-era-parity-check`).
- Extended `uo-modernuo-workflow` with agentic routing and direct-modernuo escape hatch for `modernuo-issue-*` skills.
- Removed legacy duplicate skills `rebirthuo-github-review` and `rebirthuo-request` superseded by `rebirthuo-issue-review` and `rebirthuo-issue-create`.
- Added maintenance scripts under `scripts/` for metadata injection, catalog generation, portfolio verification, and Hermes sync.

## 1.20.0 - 2026-07-12

- Synchronized the relevant Hermes ModernUO/RebirthUO/UO skills into the plugin, including newly available migration, issue, implementation, era-gate, source-gate, item-property, product-model, and verification workflows.
- Added the ModernUO/RebirthUO GitHub issue and review skill set while excluding unrelated general-purpose Hermes skills.
- Updated all plugin manifests and documented the filtered sync boundary.

## 1.18.0 - 2026-07-03

- Synced `plugins/modernuo/skills/` 1:1 from the active Hermes `ultima-online` profile for Ultima Online, ModernUO, and RebirthUO themed skills.
- Auto-pushed the synchronized plugin update from the daily Hermes cron job.

## 1.17.0 - 2026-07-02

- Synced `plugins/modernuo/skills/` 1:1 from the active Hermes `ultima-online` profile for Ultima Online, ModernUO, and RebirthUO themed skills.
- Auto-pushed the synchronized plugin update from the daily Hermes cron job.

## 1.16.0 - 2026-07-02

- Synced `plugins/modernuo/skills/` 1:1 from the active Hermes `ultima-online` profile for Ultima Online, ModernUO, and RebirthUO themed skills.
- Added missing Hermes-used skills including RebirthUO issue implementation, ModernUO lifecycle/performance/regression/test workflows, RebirthUO codebase and online triage verification, human-review promotion, canonical game-doc authoring, living-world review, era/product timeline, Samurai Empire research, UO research-doc parity, UOGuide item-property extraction, and the Ultima Online product model.
- Refreshed existing ModernUO/UO skill contents and support references from Hermes so the plugin no longer carries divergent local copies.
- Updated plugin manifests and README documentation for the Hermes sync contract.

## 1.15.0 - 2026-06-23

- Added `modernuo-test-naming` to normalize AI-generated xUnit test file, class, and method names around the tested object or area.
- Added trigger evals and interface metadata for publish, era, branch, issue, and task-label test naming cleanup.
- Updated plugin documentation and manifest versions for the new test naming workflow.

## 1.14.0 - 2026-06-22

- Updated `modernuo-ticket-triage` to treat era- or publish-based information as an explicit measurement target before planning changes.
- Added a publish era measurement reference with verified anchors for Publish 81, Publish 90 / Time of Legends, and the Endless Journey special case.
- Updated plugin documentation and manifest versions for publish-to-era measurement triage.

## 1.13.0 - 2026-06-22

- Updated `modernuo-ticket-triage` to cite only information verified in the repository, fetched from internet sources, or supplied by the issue.
- Added `issue-supplied` evidence handling and required unverifiable facts to become open research instead of factual citations.
- Updated plugin documentation and manifest versions for the evidence-existence triage contract.

## 1.12.0 - 2026-06-22

- Updated `modernuo-ticket-triage` to require clear rationale and evidence for every necessary code change.
- Added a publish/era rule so behavior introduced or changed by a publish is treated as an era check with explicit gate or profile impact.
- Updated plugin documentation and manifest versions for the tightened ticket triage contract.

## 1.11.0 - 2026-06-22

- Added `modernuo-ticket-triage` to turn GitHub issues and pasted tickets into source-backed implementation plans.
- Documented broad UO source research with explicit trust tiers, repository anchors, expected-vs-actual deltas, acceptance criteria, and test planning.
- Updated plugin documentation and manifest versions for the new ticket triage workflow.

## 1.10.0 - 2026-06-22

- Enhanced `modernuo-era-parity-check` to require source-backed expected-vs-actual deltas for non-present, low-confidence, monster, crafting, and user-focused risk rows.
- Added delta-reporting guidance, Yao interface metadata, trigger/output evals, and reviewer-visible output risk notes for era parity reports.
- Updated plugin documentation and manifest versions for the new era parity report contract.

## 1.9.0 - 2026-06-22

- Added `modernuo-custom-module` for setting up and maintaining custom ModernUO content modules such as the default `CUOContent` / `CUOContent.Tests` pair.
- Documented custom module runtime registration through solution entries, application project references, and `Distribution/Data/assemblies.json`.
- Updated plugin documentation and manifest versions for the new skill.

## 1.8.0 - 2026-06-21

- Added Cursor marketplace metadata for the `rebirthuo-plugins` marketplace.
- Added a Cursor plugin manifest for `modernuo`.
- Documented Cursor marketplace usage.
- Aligned Codex, Claude Code, and Cursor plugin manifests on version `1.8.0`.

## 1.7.0 - 2026-06-21

- Added Claude Code marketplace metadata for the `rebirthuo-plugins` marketplace.
- Added a Claude Code plugin manifest for `modernuo`.
- Documented Claude Code local and GitHub marketplace installation commands.

## 1.6.1 - 2026-06-21

- Moved the ModernUO plugin README and changelog to the repository root.
- Added a root MIT license for the plugin repository.
- Updated root documentation paths for the `plugins/modernuo` plugin layout.

## 1.6.0 - 2026-06-21

- Added `modernuo-lootpack-preservation` to require recommendation and confirmation before replacing source-derived `LootPack` loot calls with exact-gold or policy-helper implementations.

## 1.5.0 - 2026-06-21

- Added `modernuo-symbol-discipline` to guide when ModernUO/RebirthUO code should inline values or introduce constants, locals, fields, properties, and `Policy*` symbols.

## 1.4.0 - 2026-06-20

- Added `modernuo-era-change-gate` to require era parity involvement when content changes cross expansion or EraProfile boundaries.

## 1.3.1 - 2026-06-20

- Updated parity-check and content-taxonomy parity reports to require Markdown delivery and offer optional single sliced issue creation from report findings.

## 1.3.0 - 2026-06-20

- Added `modernuo-item-property-parity-check` for named Ultima Online item property parity checks against ModernUO/RebirthUO source code.

## 1.2.0 - 2026-06-20

- Added `modernuo-spell-parity-check` for named Ultima Online spell parity checks against ModernUO/RebirthUO source code.

## 1.1.0 - 2026-06-20

- Added `modernuo-skill-parity-check` for named Ultima Online skill parity checks against ModernUO/RebirthUO source code.

## 1.0.1 - 2026-06-20

- Fixed plugin UI metadata to use `assets/rebirthuo-logo.png` as both the logo and composer icon.
- Added plugin README documentation covering purpose, contents, and usage.
