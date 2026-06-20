# ModernUO Skill Discovery Report

## Summary

- Installed skills reviewed: current assistant ModernUO skill list plus the repository plugin skill folder.
- Attached skills reviewed: `modernuo-skill-discovery`, `yao-meta-skill`; `personal:chat-language` was requested globally but its configured local path was not present.
- Repository skills reviewed: 45 existing skill folders under `plugins/modernuo/skills/` before this pass.
- Repository skills after this pass: 48 skill folders.
- Developer docs reviewed: `AGENTS.md`, `CLAUDE.md`, `dev-docs/rebirthuo-codebase-analysis.md`, `dev-docs/server-lifecycle.md`, `dev-docs/pathfinding.md`, `dev-docs/threading-model.md`, `dev-docs/code-standards.md`, `dev-docs/uo-reference-sources.md`.
- Code domains scanned: startup/lifecycle, pathfinding, world saves/archives, AI movement, archive tests, pathfinding tests, guilds/factions/vendors as follow-up candidates.
- Candidate new skills implemented: `modernuo-server-lifecycle`, `modernuo-pathfinding`, `modernuo-world-saves-archives`.
- Existing skills updated: all existing `SKILL.md` files received a `How to Report Issues` contract; stale `dev-docs/claude-skills/...` self-links were neutralized to plugin skill paths where appropriate.
- Highest-value gap closed: startup/pathfinding/world-save operator workflows now have dedicated skills instead of being buried in broad audit or threading guidance.

## Skill Inventory

All entries are repository source type.

| Skill | Source | Type | Covered Domain | Notes |
|---|---|---|---|---|
| `migrate-*` skills | `plugins/modernuo/skills/migrate-*` | repository | RunUO migration | Kept compact; reporting contract added. |
| `modernuo-code-audit` | `plugins/modernuo/skills/modernuo-code-audit` | repository | Code review rules | Linked to new lifecycle/pathfinding/world-save skills. |
| `modernuo-*` engine skills | `plugins/modernuo/skills/modernuo-*` | repository | Engine and ModernUO APIs | Existing coverage kept; stale plugin self-links updated. |
| `uo-*` domain skills | `plugins/modernuo/skills/uo-*` | repository | UO gameplay/content domains | Existing coverage kept; reporting contract added. |
| `modernuo-server-lifecycle` | `plugins/modernuo/skills/modernuo-server-lifecycle` | repository | Startup/bootstrap/shutdown | New P0/P1 skill. |
| `modernuo-pathfinding` | `plugins/modernuo/skills/modernuo-pathfinding` | repository | AI movement, A*, StepCache | New P1 skill. |
| `modernuo-world-saves-archives` | `plugins/modernuo/skills/modernuo-world-saves-archives` | repository | Save backup/archive/restore | New P0/P1 skill. |

## Existing Skill Coverage

| Domain | Evidence | Existing Skill Coverage | Gap | Recommendation |
|---|---|---|---|---|
| Server lifecycle/bootstrap | `service/Projects/Server/Main.cs:436`, `:447`, `:452`, `:454`, `:458`, `:459`; `service/dev-docs/server-lifecycle.md` | partial | Complex phase rules had no dedicated plugin skill. | Added `modernuo-server-lifecycle`. |
| Pathfinding/AI movement | `service/dev-docs/pathfinding.md:11`, `:34`, `:60`, `:90`, `:154`; `service/Projects/UOContent/Mobiles/AI/BaseAI/AIMovement.cs:306`; `service/Projects/UOContent/Engines/Pathing/BitmapAStarAlgorithm.cs:36` | partial | Covered indirectly by threading/perf, but not the A*/StepCache domain. | Added `modernuo-pathfinding`. |
| World saves/archives | `service/Projects/UOContent/World Saves/AutoArchive.cs:99`, `:123`, `:126`, `:629`; `service/Projects/UOContent/World Saves/ArchiveJournal.cs:127`, `:187`; `service/Projects/Server/World/World.cs:357` | missing | Operator data-loss workflow had no dedicated skill. | Added `modernuo-world-saves-archives`. |
| Vendors/economy | `service/Projects/UOContent/Mobiles/Vendors/` and `SBInfo` files | partial | Domain is large, but no local focused docs yet. | `research needed`. |
| Guilds/factions/notoriety | `service/Projects/Server/Guild.cs`, `service/Projects/UOContent/Engines/Factions/`, `Notoriety.cs` | partial | High interaction with combat/travel, but needs deeper scan. | `research needed`. |
| Accounts/security | `service/Projects/UOContent/Accounting/` | missing | Security-sensitive, but needs a narrower source scan before drafting. | `research needed`. |

## Recommended New Skills

### P0/P1: `modernuo-server-lifecycle`

**Why this matters:** startup ordering, first-boot prompts, logging boundaries, test fixtures, and world readiness can break boot or hide runtime-only failures.

**Evidence:** `Main.cs` invokes `ConfigurePrompts`, `Configure`, `World.Load`, `Initialize`, networking, `ServerStarted`, then `RunEventLoop`; `server-lifecycle.md` documents phase responsibilities and prompt constraints.

**Overlap check:** related to `modernuo-configuration`, `modernuo-events`, and `modernuo-threading`, but distinct because it owns phase selection and runtime startup boundaries.

### P1: `modernuo-pathfinding`

**Why this matters:** pathfinding is main-thread, bounded, cache-backed, and performance-sensitive. Small changes can cause pet/chase regressions or tick spikes.

**Evidence:** `pathfinding.md` documents `ApproachTarget`, `PathFollower`, `BitmapAStarAlgorithm`, `StepCache`, `.swb` files, and config levers; tests cover AI approach and StepCache file formats.

**Overlap check:** related to threading and spatial range geometry, but distinct because it owns AI navigation and static walkability caching.

### P0/P1: `modernuo-world-saves-archives`

**Why this matters:** archives, backup markers, restore prompts, and journal recovery are data-loss-sensitive operator workflows.

**Evidence:** `AutoArchive.cs` wires `ArchiveJournal`, post-snapshot backup, `.backup-complete`, archive rollups, and restore prompts; `ArchiveJournalTests.cs` validates transitions and recovery.

**Overlap check:** related to lifecycle, events, configuration, and code audit, but distinct because it owns backup/archive/restore behavior.

## Existing Skills to Update

| Skill Set | Missing Content | Evidence | Change Made |
|---|---|---|---|
| All existing `SKILL.md` files | Consistent issue reporting contract | Yao drafting contract requires report guidance for reusable skills. | Added `## How to Report Issues`. |
| Skills with `dev-docs/claude-skills/...` links | Tool-specific self-links after plugin migration | `rg` found stale links across migration and engine skills. | Repointed to `plugins/modernuo/skills/.../SKILL.md`. |
| Hub/audit skills | New skills were not discoverable from common entry points | `uo-modernuo-workflow`, `modernuo-code-audit`, `modernuo-threading`, `modernuo-configuration`. | Added cross-links to new skills. |

## Existing Skills to Generalize or Neutralize

| Skill/File | Current Issue | Suggested Neutral Version | Change Made |
|---|---|---|---|
| `uo-items-foundation/references/analyzing-modernuo-subsystems.md` | Mentions Hermes convention | Portable skill convention | Updated wording. |
| `uo-items-foundation/scripts/validate_cromesdk_skill.py` | Mentions Hermes tags | Required tags | Updated wording. |

## Not Recommended

| Candidate | Reason |
|---|---|
| Immediate `uo-vendors-economy` skill | Large domain and many files, but no focused local doc/source pass yet. |
| Immediate `uo-guilds-factions-notoriety` skill | Important but interleaves combat, travel, guild UI, faction towns, and notoriety; needs separate scan. |
| Immediate `modernuo-accounts-security` skill | Security-sensitive; should be drafted from a focused review of account storage, password protection, login events, and tests. |

## Follow-Up Searches

```powershell
rg -n "BaseVendor|SBInfo|GenericBuyInfo|SellInfo|VendorInventory|PlayerVendor" ..\service\Projects\UOContent ..\service\dev-docs
rg -n "Faction|Notoriety|Guild|Alliance|Town|Stronghold|Murder|Criminal" ..\service\Projects\Server ..\service\Projects\UOContent ..\service\dev-docs
rg -n "Account|PasswordProtection|AccountLogin|PBKDF2|Argon2|IPAddress|AccessLevel" ..\service\Projects\Server ..\service\Projects\UOContent ..\service\dev-docs
```
