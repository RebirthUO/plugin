# Publish 86 implicit negative properties

Negative properties that **do not** get their own tooltip label — they alter an existing property row.

## Massive

Full review checklist: `references/massive-item-property-review.md` (GitHub issue #12 pattern).

- Str req **125**; display via cliloc `1061170` only.
- Lower requirements must not reduce below 125 (UO.com); do not copy ServUO `GetLowerStatReq()` scaling when Massive is set.

## Unwieldy (related)

- Publish 86 family; weight shown via existing weight property, not a separate `Unwieldy` row (UO.com / Publish 86 notes).
- When drafting or implementing Unwieldy, mirror the same split: storage on negative attributes, presentation on existing row, ServUO vs UO.com check for override rules.

## Issue drafting

For any Publish 86 negative (`Prized`, `Brittle`, `Massive`, `Unwieldy`, `Antique`, `Cursed`), load `uo-item-property-review` and state explicitly in acceptance criteria whether a **dedicated** tooltip cliloc is required or forbidden.