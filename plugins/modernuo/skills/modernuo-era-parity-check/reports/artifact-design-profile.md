# Artifact Design Profile

## Artifact Role

Decision-ready Markdown report for era parity planning and issue slicing.

## Reading Order

1. Header: era, profile, publish range, report date.
2. Aspect coverage summary: compact scan of where risk lives.
3. Entity/system detail: only notable rows and user-focused rows.
4. Delta Matrix: field-level expected-vs-actual evidence for risk rows.
5. Gap, partial/runtime, enhanced, open research, focus, and issue slicing.

## Density Rules

- Use tables when comparing fields; use bullets for action lists and open
  research.
- Keep the aspect table compact by showing only the top delta per aspect.
- Put long evidence paths in `ModernUO Evidence`, not in narrative paragraphs.
- Use stable Open Research IDs for unresolved source conflicts.

## Evidence Rules

- Each risk row must cite a source and a repo evidence point.
- A row with no concrete repo evidence is not a finding; it is Open Research.
- The Delta Matrix is the review surface for monsters and crafting because those
  areas fail when reports only state "what" is missing.
