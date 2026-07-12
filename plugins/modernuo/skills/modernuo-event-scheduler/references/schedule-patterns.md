# Scheduler Patterns

Verify exact constructors and helpers against the current repository.

## Decision table

| Requirement | Preferred surface |
|---|---|
| Daily at a civil time | `EventScheduler.DailyAt` |
| Weekly on selected day/time | `WeeklyAt` or weekly recurrence |
| Day of month | monthly recurrence |
| Ordinal weekday (second Tuesday) | `MonthlyOrdinalRecurrencePattern` |
| Annual start/end window | `YearlyScheduledEvent` |
| Filtered weekdays/months | recurrence with `AllowedDays` / `AllowedMonths` |
| Short elapsed delay or sub-second tick | `Timer.StartTimer`, not EventScheduler |

`CallbackScheduledEvent` suits a static callback. Derive from `ScheduledEvent` only when the event owns meaningful behavior/state. Call `Cancel()` when its owning system is disabled or replaced.

## Policy questions

Record:

- IANA/Windows time-zone identifier supported by deployment;
- DST invalid-time and ambiguous-time behavior;
- inclusive/exclusive seasonal boundaries;
- last-day behavior for short months and leap years;
- whether missed occurrences run after restart;
- maximum catch-up count;
- duplicate-registration and duplicate-side-effect prevention;
- operator disable/reschedule behavior.

## Test matrix

Calculate next occurrences around normal dates, DST transition, month/year boundary, leap day, seasonal start/end, and restart. Inject or isolate clock calculations when the repository provides a seam; do not make tests sleep for wall-clock time.
