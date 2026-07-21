# World-save lifecycle inspection

Read this reference when a task changes save execution, snapshot completion,
recovery, or an external backup/archive integration.

## Source discovery

Record the consuming repository's full revision, then locate the current:

- world-save request and re-entry guard;
- serialization and snapshot implementation;
- completion event or callback and its artifact/path arguments;
- worker synchronization, exception propagation, and cleanup;
- startup, shutdown, crash-recovery, and save-path configuration;
- focused save, lifecycle, threading, and recovery tests.

Search by behavior and symbols found in the pinned source. Names such as
`World.Save` or `WorldSavePostSnapshot` are useful discovery candidates, not a
portable contract. Treat custom backup markers, archive journals, destinations,
formats, commands, and restore prompts as extension evidence only.

## Failure-boundary analysis

For every changed transition, establish:

| Boundary | Required evidence |
|---|---|
| Request to serialization | Re-entry behavior, caller context, and failure reporting |
| Serialization to snapshot | Worker ownership, completion join, and partial-output handling |
| Snapshot publication | Durable-completion definition and atomic visibility |
| Completion to integration | Exact callback/event contract and duplicate-delivery behavior |
| Integration publication | Temporary/final artifact rules, integrity check, and idempotency |
| Shutdown or crash | In-flight behavior, cleanup, and next-start recovery |
| Retention or overwrite | Protected recovery points and approved data-loss window |

Do not convert an absent guarantee into an assumed one. If the repository does
not establish a required transition, report it as unresolved and stop a
data-destructive implementation.

## Focused verification

Select tests from the actual changed surface. Cover applicable cases:

- successful save and completion notification;
- concurrent or repeated save request;
- serialization or snapshot failure;
- shutdown while work is pending;
- partial artifact rejection and cleanup;
- duplicate integration delivery and retry;
- save-path migration or overwrite collision;
- recovery from the newest approved artifact into an isolated destination.

Report automated commands and observed results separately from manual restore,
shutdown, or crash-recovery evidence. A structural archive check alone does not
prove that the world state can be restored.
