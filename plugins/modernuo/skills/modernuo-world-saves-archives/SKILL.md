---
name: modernuo-world-saves-archives
description: Use when working with ModernUO world save backups, archive rollups, archive restore flows, ArchiveJournal state transitions, local archive destinations, save snapshot post-events, crash backups, backup pruning, archive verification, or operator-facing save/restore commands. Use before editing Projects/UOContent/World Saves, EventSink.WorldSavePostSnapshot backup behavior, AutoArchive configuration, .archive-journal.json recovery, managed archive formats, or restore prompts.
---

# ModernUO World Saves & Archives

## Purpose

Use this skill to protect shard data when changing automatic backups, archive rollups, restore prompts, archive destinations, or journaled recovery paths around ModernUO world saves.

## When This Activates

- Editing `Projects/UOContent/World Saves/`, `Projects/Server/World/`, crash backup handling, save commands, or archive tests.
- Changing `AutoArchive`, `ArchiveJournal`, `LocalArchiveDestination`, `ArchiveDestinationRegistry`, `ManagedArchive`, or restore/prune commands.
- Adding archive destinations, retention policies, verification steps, compression formats, or startup restore behavior.
- Debugging missing saves, interrupted archives, broken restore menus, or archive cleanup behavior.

## Key Rules

- Treat world-save data as operator-critical. Prefer additive, reversible changes and verify restore paths, not just archive creation.
- `AutoArchive.Configure()` can run before normal gameplay starts; interactive restore prompting only belongs where console input is still safe.
- `AutoArchive.Initialize()` subscribes to `EventSink.WorldSavePostSnapshot`; do not move backup logic earlier than a completed snapshot.
- Use the journal state machine (`Started`, `Archived`, `Distributed`, `Completed`, `Failed`) to make interrupted archive operations visible and recoverable.
- Do not archive incomplete backup directories. The `.backup-complete` marker exists so rollups can skip partially moved saves.
- Keep archive verification, temp-file cleanup, and failure recording together; a failed archive must not look complete.

## Patterns

### Snapshot Backup Flow

`World.Save()` snapshots the world, `EventSink.WorldSavePostSnapshot` fires with old/new save paths, and `AutoArchive.Backup` moves the old save directory into automatic backups before invoking archive rollup.

### Journaled Archive Flow

Start an `ArchiveJournal` operation before archive creation, move from temp file to final file only after success, record archive metrics, record destination results, then complete or fail the journal entry.

### Restore Flow

On startup with no valid save data, collect complete backup directories and archive files, present newest restore points first, extract archives to a temp directory, then copy selected save contents into the configured `Saves` path.

## Anti-Patterns

- Deleting or pruning source backups before archive creation, verification, and distribution are recorded.
- Treating an archive file as valid without checking entry count, format support, and verification settings.
- Ignoring interrupted `Started` or `Distributed` journal states on startup.
- Mixing ad-hoc filesystem writes with world save snapshot timing.
- Prompting for restore after console handling/logging has moved into normal runtime behavior.
- Adding remote archive destinations without explicit failure reporting and retention semantics.

## Real Examples

- `Projects/UOContent/World Saves/AutoArchive.cs` configures archive paths, retention, restore prompting, post-snapshot backup, rollups, verification, and pruning.
- `Projects/UOContent/World Saves/ArchiveJournal.cs` persists archive operations and recovers interrupted states on startup.
- `Projects/Server/World/World.cs` invokes `EventSink.InvokeWorldSavePostSnapshot(...)` after save snapshot rotation.
- `Projects/UOContent.Tests/Tests/WorldSaves/ArchiveJournalTests.cs` covers state transitions, persistence, and interrupted-operation recovery.
- `Projects/UOContent.Tests/Tests/WorldSaves/AutoArchiveHelperTests.cs` covers destination registration, retention counts, and event argument storage.

## How to Report Issues

Report world-save/archive findings with data-loss risk first:

```text
[WORLD-SAVE] {severity}: {backup/archive/restore issue}
  File: {path}:{line}
  Risk: {data loss, incomplete backup, failed restore, operator confusion, or cleanup drift}
  Evidence: {journal state, archive file, test, command output, or restore repro}
  Suggested check: {ArchiveJournalTests, AutoArchiveHelperTests, restore smoke, or dotnet test}
```

## See Also

- `dev-docs/threading-model.md` - world save threading and main-thread snapshot boundary.
- `plugins/modernuo/skills/modernuo-server-lifecycle/SKILL.md` - startup, prompt, and post-snapshot event boundaries.
- `plugins/modernuo/skills/modernuo-events/SKILL.md` - `EventSink` subscription patterns.
- `plugins/modernuo/skills/modernuo-configuration/SKILL.md` - `ServerConfiguration.GetOrUpdateSetting` patterns.
- `plugins/modernuo/skills/modernuo-code-audit/SKILL.md` - review rules for high-risk `.cs` changes.
