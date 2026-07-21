---
name: skill-scanner
description: Use when a confirmed ModernUO-based repository has changed and the user needs a read-only evidence report showing which installed ModernUO skills may need maintenance, whether their routing and scope relationships still fit, and which uncovered repository areas could justify an optional new skill. Do not use to update skills automatically, create a proposed skill without user approval, or infer repository identity.
metadata:
  version: "1.0.0"
---

# Skill Scanner

## Boundary

Audit the fit of a ModernUO skill portfolio against a named local repository
change. This skill produces review candidates, relationship evidence, and
optional capability proposals; it never changes a sibling skill, creates a new
skill, or turns a heuristic into a confirmed defect.

## Required Context

Confirm all of the following before scanning:

1. A ModernUO-based checkout and its applicable instructions.
2. A comparison revision or range that answers "changed since what?".
3. The skill-portfolio root to examine; default to this skill's sibling
   directory only when that is the requested portfolio.

If any input cannot be confirmed, return `BLOCKED` with the smallest missing
path or revision. Do not infer a repository from a working-directory name,
remote, organization, or another project.

## Workflow

1. Read the repository instructions and record the full revision and dirty
   state. Treat local source as evidence of repository behavior only, not of
   official Ultima Online gameplay.
2. Run [the scanner](scripts/scan_repository.py) with an explicit `--repo`,
   `--base`, and `--skills-root`. Include `--working-tree` only when the user
   requests uncommitted changes in the comparison.
3. Read [the evidence and triage rules](references/scanner-contract.md) before
   interpreting the report. Separate exact path matches, token heuristics,
   declared sibling routes, scope-overlap warnings, and uncovered-area
   candidates.
4. Inspect each `needs_review` candidate against current repository anchors.
   A changed path alone is never a reason to edit a skill: confirm that an
   instruction, reference, API claim, validation command, or ownership boundary
   is actually stale.
5. Present optional capability candidates as `USER_DECISION_REQUIRED`. Do not
   scaffold, add, or merge a new skill until the user explicitly selects one.
6. Keep all report claims revision-bound and identify every unavailable command
   or incomplete relationship signal.

## Guardrails

- Treat scanner classifications as maintenance triage, not as skill-quality
  scores or automatic edit authorization.
- Preserve the distinction between `exact_path`, `keyword_overlap`, and
  `uncovered_change_area`; only the first is a direct text-to-change signal.
- A declared sibling relation is a routing hint, not a permission to invoke or
  mutate that sibling.
- Do not use a repository source, client, emulator, or community material to
  resolve player-facing UO mechanics. Route those claims to `uo-official-evidence`.
- Do not inspect a different portfolio or create a new package merely because
  a candidate has a high heuristic score.

## Result Contract

Classify the request as `AUDIT` or `BLOCKED`. Emit exactly one fenced `yaml`
document. Use factual values and empty lists rather than prose placeholders.

```yaml
Outcome: REVIEWED | BLOCKED
Repository revision:
  commit: <full revision or null>
  dirty: <true | false | null>
Decision:
  kind: AUDIT | BLOCKED
  summary: <single factual sentence>
  records:
    - kind: skill-maintenance | relationship | scope-overlap | capability-candidate
      subject: <skill name or changed area>
      status: needs_review | verified_current | user_decision_required | blocked
      details: <classification and bounded rationale>
      evidence_refs: [<Evidence.records.id>]
Evidence:
  records:
    - id: E1
      class: repository | scanner | user-supplied
      locator: <revision-bound path, command, or null>
      claim: <fact supported by the record>
Verification:
  checks:
    - command_or_method: <command or inspection>
      result: passed | failed | not-run | blocked
      evidence_refs: [E1]
  scanner:
    result: passed | failed | not-run | unavailable
    report_path: <path or null>
Confidence:
  level: high | medium | low
  basis: <change comparison, evidence coverage, and validation basis>
Limitations:
  items: [<unresolved source, stale relation, or heuristic limit>]
```

Use `high` confidence only when the comparison range, relevant current anchors,
and scanner run are all complete. Use `low` for a blocker or missing base
revision.

## Verification

- Run `python scripts/validate-modernuo-skill-evals.py
  plugins/modernuo/skills/skill-scanner` from the plugin root.
- Run `python plugins/modernuo/skills/skill-scanner/scripts/scan_repository.py
  --repo <confirmed-repository> --base <revision> --skills-root
  plugins/modernuo/skills --format json --output <external-report-path>` and
  parse the JSON before reporting it.
- Run the current runtime smoke when the Codex CLI is available; otherwise
  record it as unavailable.
