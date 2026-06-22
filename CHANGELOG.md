# Changelog

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
