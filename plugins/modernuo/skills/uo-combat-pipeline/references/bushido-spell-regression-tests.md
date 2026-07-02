# Bushido spell / stance regression test patterns

Session-derived patterns for RebirthUO/ModernUO Samurai Empire Bushido issue work. Use these when implementing isolated PRs for Bushido/Honor/stance parity issues.

## General fixture pattern

- Use `[Collection("Sequential UOContent Tests")]` for tests that mutate `Core.Expansion`, `Core._now`, timers, `NetState`, static spell tables, poison registration, or mobile world state.
- In `try/finally` or `IDisposable` fixture state, restore:
  - `Core.Expansion`
  - `Core._now`
  - `Timer.Init(0)`
  - spell state tables via public cleanup APIs (`Confidence.EndConfidence`, `Confidence.StopRegenerating`, `Evasion.EndEvasion`, `CounterAttack.StopCountering`, `HonorableExecution.RemovePenalty`)
  - mobile `NetState` links before disposing test net states
  - `Poison = null` when poison status was set
- Test-created players usually need:
  - `new PlayerMobile(World.NewMobile)`
  - `DefaultMobileInit()`
  - `Player = true`
  - `InitStats(100, 100, 100)` when Hits/Stam/Mana deltas matter
  - `MoveToWorld(new Point3D(...), Map.Felucca)` when map/location-sensitive code can run
  - `PacketTestUtilities.CreateTestNetState()` plus a SE-capable client version when spell icon packets or `NetState.SendToggleSpecialAbility` may fire.

## Timer-driven Bushido effects

- Prefer deterministic timer advancement:
  - set `Core._now` to a fixed UTC value;
  - call `Timer.Init(0)`;
  - advance `Core._now` past the expiration;
  - call `Timer.Slice(milliseconds)`.
- Do not rely on wall-clock sleeps.
- For `TimerExecutionToken`-backed effects, assert both the visible state API (`IsConfident`, `IsEvading`, `IsRegenerating`, etc.) and the post-expiry cleanup effect.

## Honorable Execution cleanup

- The failure penalty is represented by `HonorableExecution.IsUnderPenalty(m)` plus named resistance mods and a named Magic Resist skill mod.
- Death/delete cleanup should reuse `HonorableExecution.RemovePenalty(Mobile)` through generated events:
  - `[OnEvent(nameof(PlayerMobile.PlayerDeathEvent))]`
  - `[OnEvent(nameof(PlayerMobile.PlayerDeletedEvent))]`
- Tests can invoke generated events directly (`PlayerMobile.PlayerDeathEvent(player)`, `PlayerMobile.PlayerDeletedEvent(player)`) to prove static state cleanup without requiring a full death pipeline.
- If testing resistance values, avoid overfitting to natural race/skill resistance floors unless the issue requires exact status-window values. For cleanup, named mod presence/absence and `IsUnderPenalty` are usually the stable proof.

## Confidence patterns

- Separate immediate Confidence regeneration from parry refresh:
  - regeneration timer formula: `Confidence.GetRegenerationTotalHits`, `GetRegenerationHitsPerTick`, `RegenerationSeconds`;
  - parry refresh: HP range `1..(int)(Bushido / 12)` and stamina range `1..(int)(Bushido / 5)`.
- For randomized refresh tests, assert formula maxima and `Assert.InRange(actualDelta, 1, expectedMax)` rather than trying to seed the global RNG.
- Poison interruption behavior should distinguish status from damage:
  - setting `player.Poison = Poison.Regular` should not by itself stop `Confidence.IsRegenerating(player)`;
  - damage arriving through `PlayerMobile.OnDamage(...)` should stop regeneration, including when simulating poison damage with `from: null`.
- Ensure poison kinds before using `Poison.Regular`: if `Poison.Regular == null` and `Poison.Poisons.Count == 0`, call `PoisonKinds.Configure()`.

## Confidence / Evasion / Counter Attack active-state replacement

- The common Bushido spell success path is `SamuraiSpell.OnCastSuccessful(Mobile)`, which ends Evasion, Confidence, and Counter Attack before the newly cast spell starts its own state.
- Tests for replacement should call the common success path and then the specific `Begin*` method, matching production's split between shared cleanup and spell-specific state creation:
  - `new Confidence(player, null!).OnCastSuccessful(player); Confidence.BeginConfidence(player);`
  - `new Evasion(player, null!).OnCastSuccessful(player); Evasion.BeginEvasion(player);`
- Cleanup must end all relevant states in `finally`/`Dispose`, because these systems use static dictionaries.

## Evasion magical parry and PvP diminishing returns

- Treat issue bodies that cite missing/stale era-ledger paths as a triage source, then ground mechanics in current repo anchors plus UO.com/UOGuide/Stratics evidence rather than blocking on the missing doc.
- `Evasion.CheckSpellEvasion` is the shared gate for single-target spell damage and breath-like magical damage. When adding a new magical/ranged damage path, pass the attacker/source into Evasion so PvP diminishing state has context.
- For magical-parry tests, force deterministic parry with `Mobile.SkillCheckDirectLocationHandler = (_, skill, chance) => skill == SkillName.Parry;`, start `Evasion.BeginEvasion(defender)`, and assert HP/scalar remains unchanged for spell, breath, and monster ability paths.
- For PvP diminishing tests, capture the `chance` passed to `SkillCheckDirectLocationHandler` across repeated successful parries. UO.com Bushido documents diminishing returns after the first PvP evade, scaling to a max 70% reduction; a 60% evade chance should clamp at 18%.
- Non-PvP control tests should use the same repeated parry path with `attacker.Player = false` and assert the captured Evasion chance does not diminish.
- When using `PlayerMobile` fixtures in harmful/combat paths, prefer `new PlayerMobile()` plus `DefaultMobileInit()` unless the test specifically needs a world serial. `new PlayerMobile(World.NewMobile)` skips the parameterless constructor fields such as `PermaFlags`.
- If a two-handed Bushido weapon such as `NoDachi` is used for parry setup, assert `defender.EquipItem(weapon)` and `Assert.Same(weapon, defender.Weapon)` before relying on parry formulas; otherwise the test may silently fall back to fists/default weapon behavior.

## PR workflow reminder

For issue-batch PRs, each branch should still end at a durable checkpoint: focused RED/GREEN evidence where applicable, `git diff --check`, `dotnet build -m:1`, focused `dotnet test --no-build --no-restore`, commit, push, PR, labels, and a review-summary comment.