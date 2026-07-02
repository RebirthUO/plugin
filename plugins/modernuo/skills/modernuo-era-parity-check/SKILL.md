---
name: modernuo-era-parity-check
description: >
  Use when asked for an Ultima Online expansion, add-on, EraProfile, or era-scoped content parity report for RebirthUO/ModernUO. Requires a valid era and compares repo evidence with UO.com, UOGuide, Stratics fallback, and repo-internal era docs.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [modernuo, rebirthuo, era, parity, research]
    related_skills:
      - modernuo-era-change-gate
      - modernuo-era-expansion
      - uo-era-product-timeline
      - uo-domain-research
      - modernuo-ticket-triage
---

# ModernUO Era Parity Check

Use this skill to show what exists, what is missing, and what differs for one UO
era, with data-backed deltas instead of vague "needs confirmation" findings.

Do not edit ModernUO source code or create issues unless the user explicitly
asks. Report parity evidence and decision points only.

## Expansion epic + era ledger (ML, SE, …)

Trigger when the user wants a **master feature list**, **code inventory**, and a
**GitHub Epic** (items, properties, monsters, engines, quests) with
**Spielersicht** gaps for anything not `Present`.

Follow [references/ml-expansion-epic-workflow.md](references/ml-expansion-epic-workflow.md)
and [references/review-verification-standard.md](references/review-verification-standard.md)
for RebirthUO `service` repo layout, cfg/monster counting rules, manifest TSV,
`dev-docs/eras/<era>.md` ledger, child-issue IDs (`ML-PARITY-*`, `ML-MISS-*`),
and ad-hoc doc verification (`scripts/hermes-verify-era-ledger-docs.py`).

Reuse the same pattern for other expansions: normalize era → scan anchors →
aspect summary → player-facing Partial/Gap sections → epic body + optional
`gh issue create` on `RebirthUO/service`.

## Player-facing monster parity (bulk)

Trigger when the user wants **Spielersicht** change lists per creature and
`SE-PARITY-MON-*` or `ML-PARITY-MON-*` issues (not reopening closed
`SE-MISS-MON` field-test tickets).

Follow [references/se-monster-player-parity.md](references/se-monster-player-parity.md):

- **uo.com-first** for mechanics (Publish 30, dungeons, champion); UOGuide only
  for creature stats when uo.com has no stat page.
- One markdown sheet per monster with bullet **Änderungsliste**; master report +
  `se-monsters-issue-manifest.tsv`.
- Issue create gate: P0/P1 `confirmed` / `source-conflict` only; stat noise and
  proc rates without official % → report (`SourceLocked`) not balance issues.

## Required Input

Require one valid era or EraProfile before starting. Accept aliases such as
`SE`, `Samurai Empire`, `Core.SE`, and profile filenames.

Valid eras: Original UO, T2A, UOR, UOTD, LBR, AOS, SE, ML, SA, HS, TOL, EJ.
Known profiles: `ml-baseline.json`, `endless-journey.json`.

If the era is missing or ambiguous, ask for the era and stop.

## Source Order

Use sources in this order and cite every non-`Present` row:

1. Repo docs/tests: `dev-docs/eras/`, source maps, EraProfiles, reference classes.
2. UO.com wiki (führend for official mechanics and publish scope).
3. UOGuide.
4. UO Stratics as a secondary fallback.

For **player monster audits**, uo.com leads even when repo docs exist; repo is
*Ist*, not *Soll*. See `references/se-monster-player-parity.md`.
5. RunUO, ServUO, UOAlive, or other community sources only as `Unverified`.

When a generated issue body points to a parity-ledger path or line that is no longer present on the current base branch, do not block or invent the missing ledger. Treat the issue body itself as the triage source, then ground gameplay claims in current repo anchors plus UO.com/UOGuide/Stratics evidence.

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
   checked and the next validation step — **after** grep/tests in step 3–4, not instead of them.
6. Emit the Markdown report using [report-template.md](report-template.md).
7. For expansion epics, run ad-hoc verify:
   `scripts/hermes-verify-era-ledger-docs.py` (set `REBIRTHUO_SERVICE`, `RUN_DOTNET=1`).

## Status Labels

Allowed states: `Present`, `Partial`, `Gap`, `Enhanced`, `SourceLocked`,
`RuntimeBlocked`, and `Unverified`. `Needs confirmation` is not a final state;
convert it into a delta or `Open Research`.

### Review deliverable rule (user)

Follow [references/review-verification-standard.md](references/review-verification-standard.md):

- **prüfen / verify / audit** → run grep, `read_file`, and/or `dotnet test` **same turn**.
- Never ship a review whose only outcome is **Partial**, **unsicher**, or **Tests fehlen**
  without evidence or a new test in the same pass.
- Era ledgers (`dev-docs/eras/*.md`) prefer **Present | Gap | OSI-Delta | RuntimeBlocked**
  in coverage tables; use **Blocked follow-ups** (not „Open research“) when UO.com fetch failed
  after an attempted tool call.

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
