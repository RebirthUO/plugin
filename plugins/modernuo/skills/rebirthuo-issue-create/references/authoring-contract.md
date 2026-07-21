# Issue Intake Contract

Use this contract only after the parent skill verifies the repository declared
by the consuming project's applicable `AGENTS.md`.

## Live template ownership

The verified repository's current live issue forms, including YAML and legacy
Markdown forms selected by the template gate, are authoritative. Do not
keep a static form list, title prefix, label list, option list, or required-field
map in this skill. Select one form from the primary player-visible object and
preserve its field labels and order exactly. Split independent deliverables
instead of blending forms.

When maintaining a form, prefer class-level forms and capture only fields that
the repository genuinely requires. Template maintenance is a separate mutation
from creating an issue and requires explicit authorization.

## Intake boundary

Phase 1 records what the user already knows:

- goal and player/operator problem;
- observed and desired outcomes;
- named era, ruleset, facet, or system when supplied;
- user-supplied source links and policy decisions;
- explicit non-goals;
- enough reproduction or context to identify the request.

Do not research formulas, dates, canonical mechanics, implementation anchors,
or side effects here. For each researchable behavior-changing field, add a
claim-specific work item:

```text
RESEARCH_REQUIRED[Rn]: <claim or decision>
Why it matters: <behavior, era, scope, persistence, economy, client, or test risk>
Research owner: <uo-official-evidence | uo-publish-expansion-mapping | relevant code-domain skill>
```

These are temporary intake placeholders, not permanent issue history. The
research phase rewrites each affected field with its verified current content
and removes the marker plus `Why it matters` line when resolved. It retains a
marker only while the corresponding gap is genuinely unresolved.

Never substitute a likely interpretation. Community sites, emulator code,
ModernUO code, and local repository behavior are not official UO evidence.

## IntakePacket

```yaml
repository:
  full_name: owner/repository
  html_url: https://github.com/owner/repository
  instruction_file: path/to/AGENTS.md
  verified_at: ISO-8601
template:
  path: .github/ISSUE_TEMPLATE/example.yml
  ref: verified default-branch revision
  digest: sha256
title: English title with live prefix
labels: []
body: complete English body
research_required:
  - id: R1
    field: exact live form field
    claim: exact missing claim or decision
    risk: why guessing would be unsafe
    owner: exact research skill or domain
duplicate_check:
  result: clear | blocked
  matches: []
status: INTAKE_READY | INTAKE_BLOCKED | INTAKE_PROVIDER_BLOCKED
blockers:
  - code: repository | template | duplicate | missing_label | provider
    evidence: []
    question: { id: IQ1, missing: string, options: [], answer_needed: string }
confidence: high | blocked
residual_uncertainty: []
provider_failure: null | { operation: string, status: string, retryable: true | false, evidence_preserved: [], mutation_performed: false | unknown }
mutation:
  authorized: true | false
  performed: []
issue:
  number: null
  url: null
  updated_at: null
  body_digest: null
mode: standalone | workflow
continuation: ASK_RESEARCH | RESEARCH
```

Set `mutation.authorized: false` for drafts, blocked states, and failures before
write authority. Set it `true` only when the current request explicitly
authorizes creation; a provider failure after that point retains `true` while
`performed` records only read-back-proven actions.

## Publication checks

1. Search exact and near-neighbor terms across open and closed issues.
2. Confirm every configured/requested label exists.
3. Validate English title/body, exact live prefix and field order, links, and
   absence of local paths and secrets.
4. Create once with the exact repository argument.
5. Read back repository, number, URL, title, labels, body, and revision.
6. After an ambiguous result, search for the exact title/body before retrying.

Re-read and compare the selected template digest immediately before creation.
If a configured label is missing, do not create it: return `INTAKE_BLOCKED` with
`code: missing_label` and a separate label-maintenance handoff. Provider errors
populate `provider_failure` with operation, provider status, retryability,
preserved evidence, and `mutation_performed: false | unknown`; an unknown create
result always requires exact title/body search before retry authorization.

Creating an issue does not authorize comments, edits, labels, relationships,
projects, milestones, implementation, commits, pushes, or pull requests.

After verified standalone intake, ask once whether to start
`rebirthuo-issue-research`. In workflow mode, continue automatically and do not
ask the same phase-transition question.
