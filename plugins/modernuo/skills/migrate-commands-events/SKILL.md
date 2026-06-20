---
name: migrate-commands-events
description: >
  Trigger: when converting RunUO command registration, EventSink handlers, or event delegate patterns.
  Covers: event name changes, delegate removal, Configure vs Initialize.
---

# RunUO -> ModernUO Commands & Events Migration

## When This Activates
- Converting `EventSink` subscriptions
- Converting event handler signatures
- Moving from `Initialize()` to `Configure()`
- Converting WorldSave/WorldLoad events to GenericPersistence

## Conversion Steps
1. Change `Initialize()` to `Configure()` for event registration
2. Remove delegate constructors: `new LoginEventHandler(OnLogin)` -> `OnLogin`
3. Rename events: `Login` -> `Connected`, `Logout` -> `Disconnected`
4. Update signatures: `OnLogin(LoginEventArgs e)` -> `OnConnected(Mobile m)`
5. WorldSave persistence -> convert to `GenericPersistence` (see migrate-persistence skill)

## Event Mapping
| RunUO | ModernUO |
|---|---|
| `EventSink.Login` | `EventSink.Connected` (Action<Mobile>) |
| `EventSink.Logout` | `EventSink.Disconnected` (Action<Mobile>) |
| `EventSink.WorldSave` | `EventSink.WorldSave` (Action -- no args) |
| `EventSink.Crashed` | `EventSink.ServerCrashed` |
| `new XXXEventHandler(method)` | `method` (direct reference) |

## Commands (Minimal Changes)
Commands use the same `CommandSystem.Register()` API. Main change: use `Configure()` for registration.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.

## See Also
- `dev-docs/runuo-migration-docs/07-commands-events.md` -- detailed migration reference
- `dev-docs/events.md` -- complete ModernUO event system
- `plugins/modernuo/skills/modernuo-events/SKILL.md` -- ModernUO events skill
- `plugins/modernuo/skills/modernuo-commands-targeting/SKILL.md` -- ModernUO commands skill
