# ModernUO Skill Portfolio Routing

Use this guide only when the request crosses a skill boundary. Select the
narrowest available owner, preserve the active skill's boundary, and do not
invent a missing neighbor. When no listed owner is available, inspect the
confirmed consuming repository directly and record that limitation.

## Shared Handoff

Pass only the information the next owner needs:

```yaml
handoff:
  scope: <confirmed task slice>
  repository_evidence: <revision, paths, or N/A>
  gameplay_evidence: <official sources or unresolved>
  constraints: [<safety, compatibility, or policy constraint>]
  next_owner: <available skill name or local inspection>
```

The receiving owner revalidates its own inputs. A handoff never grants mutation
authority, proves an official gameplay claim, or substitutes for a required
repository or source check.

## Entry Points

| User intent | First owner | Next owner when needed |
|---|---|---|
| Locate a confirmed checkout, its instructions, or validation anchors | `modernuo-codebase` | A narrow engineering, migration, or test owner |
| Review already identified code without changing it | `modernuo-code-audit` | The named domain owner for a deeper concern |
| Establish player-facing production behavior | `uo-official-evidence` | `uo-publish-expansion-mapping` for Publish or era ownership |
| Map a Publish or expansion gate | `uo-publish-expansion-mapping` | `modernuo-era-expansion` for the implementation gate |
| Run a complete issue-to-delivery flow | `rebirthuo-issue-workflow` | Its governed child sequence below |
| Design, run, or assess tests | `modernuo-regression-testing`, `modernuo-test-workflow`, or `modernuo-test-naming` | The other test owner only for its exact concern |

## Engineering Owners

| Concern | Owner | Handoff boundary |
|---|---|---|
| Settings and startup reads | `modernuo-configuration` | Send lifecycle ordering to `modernuo-server-lifecycle`. |
| Commands and interactive targets | `modernuo-commands-targeting` | Send legacy conversion to `modernuo-migrate-commands-events`. |
| New content patterns | `modernuo-content-patterns` | Send classification/parity to `modernuo-content-taxonomy`. |
| Cross-domain content classification | `modernuo-content-taxonomy` | Send a chosen implementation surface to its narrow owner. |
| Craft recipes, resources, quality, repair, and bulk-order integration | `modernuo-crafting-systems` | Send UI-only work to `modernuo-gump-system`. |
| Separate content assembly | `modernuo-custom-module` | Send feature behavior to the applicable domain owner. |
| Runtime expansion gates | `modernuo-era-expansion` | Obtain production facts from `uo-official-evidence` first. |
| Event subscriptions and handlers | `modernuo-events` | Send calendar semantics to `modernuo-event-scheduler`. |
| Calendar and wall-clock schedules | `modernuo-event-scheduler` | Send game-time delays to `modernuo-timers`. |
| Gump creation or review | `modernuo-gump-system` | Send legacy conversion to `modernuo-migrate-gumps`. |
| Faction membership, towns, elections, guards, and faction state | `modernuo-faction-systems` | Send generic UI, timers, regions, or vendors to their narrow owner. |
| Housing, multis, ownership, and component lifecycle | `modernuo-housing-multis` | Send exact geometry or region policy to its narrow owner. |
| Complete item-property behavior | `modernuo-item-properties` | Send tooltip-only emission to `modernuo-property-lists`. |
| Tooltip, cliloc, or property-list output only | `modernuo-property-lists` | Send mechanics, storage, or era work to `modernuo-item-properties`. |
| Object cleanup and resource ownership | `modernuo-lifecycle-cleanup` | Send startup/shutdown to `modernuo-server-lifecycle`. |
| Existing creature-loot preservation | `modernuo-lootpack-preservation` | Stop for an unowned new economy design. |
| Reusable creature combat ability | `modernuo-monster-abilities` | Keep encounter orchestration with its local owner. |
| Packet layout and dispatch | `modernuo-networking` | Send text formatting to `modernuo-string-handling`. |
| AI route search and movement | `modernuo-pathfinding` | Send exact spatial coverage to `modernuo-spatial-range-geometry`. |
| Measured hot-path cost | `modernuo-performance-hot-paths` | Send broad code review to `modernuo-code-audit`. |
| Player skill activation, passive behavior, delay, and gain flows | `modernuo-player-skill-systems` | Send spell or crafting behavior to its narrow owner. |
| Region policy and lifecycle | `modernuo-regions` | Send geometry to `modernuo-spatial-range-geometry`. |
| Persistent entity or global state | `modernuo-serialization` | Send legacy conversion to the matching migration owner. |
| Server startup, shutdown, and event loop | `modernuo-server-lifecycle` | Send per-object cleanup to `modernuo-lifecycle-cleanup`. |
| Range, bounds, and tile geometry | `modernuo-spatial-range-geometry` | Send route search to `modernuo-pathfinding`. |
| Spell casting, validation, targeting, interruption, and effect lifecycle | `modernuo-spell-systems` | Send generic targets, timers, or geometry to their narrow owner. |
| Runtime text construction | `modernuo-string-handling` | Send tooltip delimiters to `modernuo-property-lists`. |
| C# symbol exposure and naming | `modernuo-symbol-discipline` | Send behavior changes to the domain owner. |
| Event-loop ownership and parallel work | `modernuo-threading` | Send ordinary delays to `modernuo-timers`. |
| Delays, recurrence, expiry, and cancellation | `modernuo-timers` | Send calendar semantics to `modernuo-event-scheduler`. |
| Vendor transactions, stock, restock, and inventory workflows | `modernuo-vendor-systems` | Send faction-scoped behavior to `modernuo-faction-systems`. |
| World saves, snapshots, and archives | `modernuo-world-saves-archives` | Send entity fields to `modernuo-serialization`. |

## Migration Owners

Start a cross-cutting legacy conversion with `modernuo-migrate-foundation`.
Use one narrow migration owner when the task is already limited to its surface:
`modernuo-migrate-commands-events`, `modernuo-migrate-gumps`,
`modernuo-migrate-items-mobiles`, `modernuo-migrate-packets`,
`modernuo-migrate-persistence`, `modernuo-migrate-property-lists`,
`modernuo-migrate-serialization`, or `modernuo-migrate-timers`. Use
`modernuo-migrate-systems` only when multiple verified surfaces must move in
one coordinated migration. Each migration owner verifies the target revision;
none treats a sibling's route as API evidence.

## Validation Owners

- `modernuo-regression-testing` owns focused behavioral assertions and fixture
  design.
- `modernuo-test-naming` owns rename-only test naming cleanup.
- `modernuo-test-workflow` owns execution scope, environment constraints,
  focused-versus-broad evidence, and delivery readiness.

## Governed Issue Sequence

`rebirthuo-issue-workflow` is the only orchestrator. Its sequence is
`rebirthuo-issue-template-gate` -> `rebirthuo-issue-create` ->
`rebirthuo-issue-research` -> `rebirthuo-issue-implement`. Each child retains
its own repository, mutation, evidence, and readiness gates. An implementation
unknown returns through research; it never receives an assumed default.
