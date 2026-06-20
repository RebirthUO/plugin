---
name: migrate-timers
description: >
  Trigger: when converting RunUO Timer subclasses, Timer.DelayCall patterns, or TimerPriority usage to ModernUO fire-and-forget timers.
  Covers: Timer subclass elimination, TimerExecutionToken, callback patterns, timer restoration.
---

# RunUO -> ModernUO Timer Migration

## When This Activates
- Converting nested `Timer` subclasses with `OnTick()`
- Converting `Timer.DelayCall()` patterns
- Removing `TimerPriority` usage
- Restoring timers after deserialization

## Conversion Steps
1. Move `OnTick()` logic to a method on the parent class
2. Replace `new InternalTimer(this).Start()` with `Timer.StartTimer(..., callback, out _token)`
3. Add `private TimerExecutionToken _token;` (NOT serialized)
4. Cancel in `OnAfterDelete()`: `_token.Cancel();`
5. Restore in `[AfterDeserialization]`: re-call `Timer.StartTimer(...)`
6. Delete the nested Timer class entirely
7. Remove all `TimerPriority` references

## Quick Mapping
| RunUO | ModernUO |
|---|---|
| `new Timer(delay).Start()` | `Timer.StartTimer(delay, callback)` |
| `new Timer(delay, interval).Start()` | `Timer.StartTimer(delay, interval, callback, out token)` |
| `timer.Stop()` | `token.Cancel()` |
| `Timer.DelayCall(delay, callback)` | `Timer.StartTimer(delay, callback)` |
| `Timer.DelayCall(delay, stateCallback, state)` | `Timer.DelayCall(delay, callback, state)` |
| `TimerPriority.XXX` | Remove -- timer wheel auto-schedules |
| Timer started in `Deserialize()` | `[AfterDeserialization]` method |

## Anti-Patterns
- Serializing `TimerExecutionToken` -- it's a struct tracking a pooled timer
- Starting timers in `Deserialize()` -- world isn't loaded yet, use `[AfterDeserialization]`
- Lambda closures on hot paths -- use `Timer.DelayCall` with state parameters instead

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/03-timers.md` -- detailed migration reference
- `dev-docs/timers.md` -- complete ModernUO timer system
- `plugins/modernuo/skills/modernuo-timers/SKILL.md` -- ModernUO timer skill
