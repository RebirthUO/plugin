# Changelog

## 3.3.1 - 2026-07-22

- Converted all five RebirthUO issue behavior fixtures to the portable runtime
  schema, restoring read-only runtime-smoke compatibility.

## 3.3.0 - 2026-07-21

- Made the RebirthUO new-issue template gate optional across the workflow,
  template-gate, and intake contracts. A live template remains mandatory when
  the request or applicable project instructions require it.
- Added a deterministic fallback intake format for optional-template requests;
  repository identity, duplicate checks, official research, publication, and
  implementation-readiness gates remain unchanged.

## 3.2.0 - 2026-07-21

- Added seven portable ModernUO domain skills for quests, crafting, spells,
  housing and multis, factions, vendors, and player-skill behavior.
- Added explicit lifecycle, ownership, official-evidence, and focused
  verification gates for each domain, plus English and German trigger fixtures.
- Updated routing and plugin manifests without embedding a repository name,
  URL, path, or repository-specific assumption in the new skill packages.

## 3.1.0 - 2026-07-21

- Enhanced `modernuo-gump-system` to segment screenshots and descriptions into
  source-marked UI components, consult a user-enabled Ultima MCP when available
  without inventing assets, and require an annotated visual concept for every
  Gump plan.

## 3.0.0 - 2026-07-21

- Renamed `modernuo-repository-scanner` to `skill-scanner` while preserving its
  revision-bound, read-only maintenance, relationship, and capability triage.

## 5.5.0 - 2026-07-21

- Added `modernuo-repository-scanner`, a portable read-only scanner that
  compares an explicit repository revision range with the installed skill
  portfolio, reports maintenance and relationship leads, and leaves new-skill
  candidates for explicit user approval.

## 5.4.0 - 2026-07-21

- Added the reviewed `modernuo-item-properties` package with portable,
  evidence-bearing contracts for item-property mechanics, storage, tooltip
  output, era gates, persistence, and focused tests.
- Enhanced `modernuo-property-lists` for the current property-list interface,
  localized argument formatting, ordering, chunked free text, invalidation, and
  interface-compatible recording tests.
- Removed repository-specific and Hermes-specific package metadata from these
  two skill packages; gameplay claims now retain the official-evidence gate.

## 5.3.0 - 2026-07-21

- Replaced the 21 enhanced packages' heading-only result convention with one
  deterministic YAML envelope, evidence records, and skill-specific decision
  records; parity, geometry, symbol, and test-table views now render from that
  envelope rather than compete with it.
- Expanded the read-only runtime smoke from one fixture framing to direct,
  paraphrased, competing-scope, and incomplete-context prompt variants, and
  records the runner fingerprint in its evidence summary.
- Corrected the custom-module assembly check to preserve unrelated assemblies
  and separated hard test-name findings from soft `Coverage`/`Smoke` review
  candidates.

## 5.2.0 - 2026-07-21

- Added and enhanced 21 repository-portable ModernUO engineering skills for
  era gates, events, UI, lifecycle, content, networking, persistence, spatial
  work, performance, and testing.
- Normalized the packages to canonical Agent Skills metadata, portable routing,
  revision/confidence reporting, German trigger coverage, and runnable trigger
  fixture smoke validation, with optional read-only runtime behavior smoke
  coverage for every declared case.
- Aligned all plugin manifests, README inventory, and skill catalog at 46
  packages; removed Hermes-specific package guidance.

## 5.1.0 - 2026-07-20

- Enhanced `modernuo-configuration`, `modernuo-code-audit`,
  `modernuo-codebase`, and `modernuo-commands-targeting` with explicit input
  gates, blocked outcomes, evidence/confidence reporting, and focused
  verification contracts.
- Removed retired Hermes-specific metadata and dead sibling references from the
  four skill packages; routing now uses present skills or explicit local
  evidence limits.
- Reworked their adapter descriptions and trigger fixtures around user intent,
  including representative German positive requests, and aligned package and
  cross-runtime plugin versions.

## 5.0.0 - 2026-07-20

- Replaced the five public `modernuo-issue-*` skills with hard-renamed
  `rebirthuo-issue-*` skills and aligned active manifests, interfaces,
  documentation, catalog entries, references, and trigger fixtures.
- Overhauled issue research to infer era when evidence permits, retry misses
  through materially different official-source routes, invoke relevant research
  and code-domain skills, and ask only for genuine product or custom-policy
  decisions after evidence exhaustion.
- Made full issue workflows continue autonomously from intake through verified
  pull request, while standalone creation asks once about research, blocked
  issues cannot enter implementation, and new implementation gaps return
  through research before user interview.
- Added multilingual trigger coverage and behavior contracts for template
  placeholders, research retries, era inference, blocked readiness, autonomous
  resumption, and end-to-end PR delivery.

## 4.2.0 - 2026-07-19

- Added `uo-official-evidence` for language-independent routing of Ultima Online
  facts, mechanics, historical behavior, production parity, and implementation
  research through an official-first evidence workflow.
- Added the approved UO.com, production-third-party, freeshard, and server-engine
  source register with strict classification and `UNRESOLVED` handling for
  claims not established by OSI/EA/Broadsword evidence.
- Added multilingual trigger coverage, conflict and evidence-gap behavior
  fixtures, aligned adapter metadata, and an English-authoring plus
  language-independent-triggering portfolio convention.

## 4.1.0 - 2026-07-19

- Added nine reviewed RunUO migration skills under canonical
  `modernuo-migrate-*` identifiers for commands/events, gumps, items/mobiles,
  packets, persistence, property lists, serialization, systems, and timers.
- Added revision-bound input and evidence gates, deterministic terminal states,
  structured result contracts, confidence handling, and behavior fixtures for
  each migration workflow.
- Removed Hermes-only skill frontmatter, repaired foundation and sibling
  routing, aligned interface/manifest/trigger metadata, and documented the
  expanded 15-skill plugin portfolio.

## 4.0.0 - 2026-07-19

- Narrowed `modernuo-world-saves-archives` to generic ModernUO world-save
  lifecycle, snapshot completion, concurrency, shutdown, crash recovery, and
  save-path behavior while preserving its existing skill identifier.
- Removed RebirthUO-only `AutoArchive`, `ArchiveJournal`, completion-marker,
  distribution, pruning, and restore-state assumptions from the portable skill
  contract; external archive systems now require revision-bound inspection.
- Added explicit mode handling, behavior-decision gates, calibrated evidence,
  a conditional lifecycle reference, and realistic trigger, near-neighbor, and
  executable behavioral safety cases with captured-response goldens.
- Replaced the stale required portfolio/catalog/Yao/Hermes validation sequence
  with the current runtime skill validator and skill-local checks.

## 3.4.0 - 2026-07-19

- Refactored `modernuo-threading` with fail-closed input and ownership checks,
  explicit failure states, revisions-bound source evidence, and calibrated
  confidence for static versus measured concurrency conclusions.
- Added a deterministic seven-section threading result contract and behavioral
  eval cases for worker/entity crossings, unknown contexts, parallel-save
  purity, inconclusive shutdown races, and verified event-loop continuations.
- Tightened timer, serialization, and world-save near-neighbor routing and
  documented exact sibling-skill dependency locators.
- Updated all ModernUO package manifests and README usage documentation for the
  strengthened threading workflow.

## 3.3.0 - 2026-07-19

- Added `modernuo-migrate-foundation` as a self-contained, evidence-backed
  cross-cutting RunUO/ServUO migration workflow with explicit compatibility
  gates, terminal states, realistic trigger boundaries, and focused validation.
- Added `uo-publish-expansion-mapping` with an official-source index and a
  complete forward-mapping matrix for ModernUO-supported UO eras.
- Added cumulative implementation-gate guidance, including Publish 81 to
  `Core.TOL`, direct Publish 90 handling, and unresolved-evidence stop rules.
- Kept Publish 99 and later in the TOL era while treating Endless Journey only
  as a distinct account restriction; `Core.EJ` is never selected as an era gate.
- Updated plugin manifests and README usage/validation documentation for the
  new skill and the refactoring branch's current validation surface.

## 3.2.0 - 2026-07-19

- Enhanced `modernuo-timers` with repository-revision evidence, explicit API
  selection, idempotent ownership, callback failure/validity handling,
  exactly-once deadline restoration, and a stable evidence-rich output contract.
- Expanded timer trigger smoke coverage for cancellation, deserialization,
  expiry, API-selection, event-scheduler, and legacy-migration boundaries.
- Removed the legacy Hermes-only frontmatter namespace from `modernuo-timers`;
  routing remains expressed through the Agent Skills description and references.
  Retained the useful skill version as standard `metadata.version` frontmatter.
- Updated ModernUO package manifests and README usage documentation for the
  strengthened timer workflow.

## 3.1.1 - 2026-07-19

- Updated `uo-bulk-orders-bod` for current RebirthUO BOD architecture:
  profession-gated Smith/Tailor/TOL craft paths, pending reward points, bribery,
  generated persistence schemas, and active focused test locations.
- Refreshed content taxonomy so TOL Skill Mastery is no longer listed as a full
  gap; it now records the current `MasterySystem`, `BookOfMasteries`, and
  Intuition passive support as partial repository coverage.
- Added README domain coverage for the BOD owner skill while preserving the
  official-evidence boundary for gameplay claims.

## 3.1.0 - 2026-07-18

- Extended `uo-pets-taming-stables` to cover current Time of Legends Animal
  Training implementation surfaces: Animal Lore entry points, pet-training
  profile persistence, progress, planning, option application, control-slot
  increases, gump revision guards, regeneration/damage consumers, and focused
  tests.
- Added a `pet-training.md` reference that keeps official UO.com Animal
  Training behavior separate from repository and TrueUO-derived implementation
  evidence.
- Updated trigger smoke coverage, generator hints, and README domain coverage
  for pet-training maintenance.

## 3.0.0 - 2026-07-14

- Changed `modernuo-issue-research` publication from an appended
  `## Research contract` to a full in-place rewrite that preserves the live
  issue's headings, field order, and Markdown format.
- Research and review now replace obsolete claims in their existing fields,
  remove resolved `RESEARCH_REQUIRED` markers and blocker/question text, and
  retain only genuinely unresolved items.
- Updated `modernuo-issue-create`, `modernuo-issue-workflow`, and
  `modernuo-issue-implement` handoffs to require a clean current issue body,
  unchanged title, no appended research report, and no unresolved marker or
  blocker text before implementation.

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
