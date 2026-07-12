---
name: modernuo-world-saves-archives
description: >
  Use when changing ModernUO world-save backups, archive rollups/destinations,
  ArchiveJournal recovery, restore prompts, verification, retention, pruning, or
  post-snapshot events. Do not use for entity field serialization; route that to
  modernuo-serialization.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, world-saves, archives, backups, restore]
    related_skills:
      - modernuo-code-audit
      - modernuo-threading
      - modernuo-server-lifecycle
      - modernuo-events
      - modernuo-configuration
      - modernuo-test-workflow
---

# ModernUO World Saves and Archives

## Boundary

Protect operator-critical shard data from snapshot through backup, archive,
distribution, retention, recovery, and restore. Prefer additive/reversible
changes and prove restore, not merely archive creation.

## Workflow

1. Map the current data flow and failure boundaries: active `Saves`, rotated old
   save, completed snapshot event, backup directory, temp/final archive,
   destinations, journal, retention, and restore selection.
2. Keep automatic backup work after `WorldSavePostSnapshot`; never archive or
   prune a directory that lacks the completion marker.
3. Start a journal operation before archive work and advance only through the
   real states: `Started`, `Archived`, `Distributed`, `Completed`, or `Failed`.
4. Write a temporary archive, verify format/entry count/content policy, then move
   it atomically to the final location. Record destination results and failures.
5. Prune source backups only after archive verification and required distribution
   succeed under the configured retention semantics.
6. Exercise interruption at each state and restore the newest valid backup/archive
   into an isolated destination before claiming safety.

## Guardrails

- `.backup-complete` distinguishes complete rotated saves from partial moves.
- A failed or interrupted archive must remain visible in the journal and must not
  look `Completed`.
- Restore prompting belongs only in the safe startup/console phase and must not
  block headless operation unexpectedly.
- Do not delete source data before verification/distribution are durable.
- Remote destinations require explicit retry/failure/retention semantics; a local
  success must not hide remote failure.
- Keep temp cleanup and failure recording in the same control path.
- World-save serialization workers and archive I/O have distinct threading
  boundaries; neither permits arbitrary live-world mutation.

## Output Contract

Return the before/after flow, journal transitions, completion/verification rules,
destination/retention behavior, rollback and restore procedure, changed paths,
tests, and any operator-visible migration or residual data-loss risk.

## Verification

- Tests cover success plus interruption/failure at every changed journal state.
- Partial backups and invalid archives are excluded from rollup/restore.
- Restore reproduces expected save contents from a real generated artifact.
- Retention never removes the last valid recovery point prematurely.
- Focused archive tests and manual restore smoke evidence are reported separately.

## Reference Routing

- Read current `AutoArchive`, `ArchiveJournal`, `World.Save`, and archive tests
  before changing the state machine.
- Load `modernuo-server-lifecycle` for prompt/event placement,
  `modernuo-threading` for snapshot workers, `modernuo-configuration` for
  settings, and `modernuo-events` for post-snapshot subscription semantics.
