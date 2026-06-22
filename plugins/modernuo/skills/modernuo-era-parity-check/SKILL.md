---
name: modernuo-era-parity-check
description: >
  Use when asked for an Ultima Online expansion, add-on, EraProfile, or
  era-scoped content parity report for RebirthUO/ModernUO. Requires a valid era
  and compares repo evidence with UO.com, UOGuide, Stratics fallback, and
  repo-internal era docs. Produces Markdown reports with aspect coverage,
  expected-vs-actual data deltas for risk rows, validation status, and optional
  single-sliced issue follow-ups.
---

# ModernUO Era Parity Check

Use this skill to show what exists, what is missing, and what differs for one UO
era, with data-backed deltas instead of vague "needs confirmation" findings.

Do not edit ModernUO source code or create issues unless the user explicitly
asks. Report parity evidence and decision points only.

## Required Input

Require one valid era or EraProfile before starting. Accept aliases such as
`SE`, `Samurai Empire`, `Core.SE`, and profile filenames.

Valid eras: Original UO, T2A, UOR, UOTD, LBR, AOS, SE, ML, SA, HS, TOL, EJ.
Known profiles: `ml-baseline.json`, `endless-journey.json`.

If the era is missing or ambiguous, ask for the era and stop.

## Source Order

Use sources in this order and cite every non-`Present` row:

1. Repo docs/tests: `dev-docs/eras/`, source maps, EraProfiles, reference classes.
2. UO.com wiki.
3. UOGuide.
4. UO Stratics as a secondary fallback.
5. RunUO, ServUO, UOAlive, or other community sources only as `Unverified`.

When sources conflict, record it and lower confidence. Separate fact from inference.

## Mandatory Workflow

1. Normalize the era to display name, enum, `Core.*`, era doc, publish range,
   and optional EraProfile.
2. Read era context and scan all aspects from [aspects.md](aspects.md).
3. Collect expected behavior and actual ModernUO evidence from code, data,
   tests, or grep results.
4. Apply the Risk Rows default from
   [references/delta-reporting.md](references/delta-reporting.md): every
   non-`Present`, low-confidence, monster, crafting, and user-focused row must
   include `Expected`, `ModernUO Evidence`, `Delta`, `Validation`, and `Impact`.
5. If no delta can be made, move the item to `Open Research` with sources
   checked and the next validation step.
6. Emit the Markdown report using [report-template.md](report-template.md).

## Status Labels

Allowed states: `Present`, `Partial`, `Gap`, `Enhanced`, `SourceLocked`,
`RuntimeBlocked`, and `Unverified`. `Needs confirmation` is not a final state;
convert it into a delta or `Open Research`.

## Output Contract

Every report must include the sections in [report-template.md](report-template.md):
header, aspect summary, entity detail, Delta Matrix, gap/partial/enhanced lists,
Open Research, optional Focus, and `Issue Slice Options`.

Issue slices must preserve expected-vs-actual evidence, validation, impact,
acceptance criteria, and open questions. Do not bundle unrelated findings.

## Package Quality Evidence

Details live in `references/`, checks in `evals/`, and output risks in
`reports/`. Run Yao validation after package changes.

## Related Skills

- `modernuo-content-taxonomy` for 9-domain inventory routing.
- `uo-domain-research` for source triangulation.
- Named skill, spell, and item-property parity skills for single-subject audits.
