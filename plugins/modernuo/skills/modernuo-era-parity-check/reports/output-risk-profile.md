# Output Risk Profile

## Artifact Family

Markdown parity report for high-trust implementation planning.

## Primary Risks

- Monster rows describe what is missing without showing expected-vs-actual
  values, code paths, or source-backed deltas.
- Crafting rows end as "needs confirmation" instead of being validated,
  converted into concrete deltas, or moved to Open Research.
- Broad era reports become too dense if every entity receives field-by-field
  analysis instead of reserving deep rows for risk rows.
- Citations support general topic pages but not the specific field being
  claimed.

## Required Self-Repair

- Check every non-`Present`, low-confidence, monster, crafting, and user-focused
  row for `Expected`, `ModernUO Evidence`, `Delta`, `Validation`, and `Impact`.
- Move unresolved claims to `Open Research` with sources checked and exact next
  validation steps.
- Keep aspect summaries compact; only risk rows need deep delta detail.
- Reject final wording that says only "verify", "confirm", or "needs
  confirmation".

## Review Notes

The output is acceptable when a reviewer can turn each risk row into a single
actionable issue without re-reading the entire report.
