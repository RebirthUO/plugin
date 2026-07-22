# Issue Intake Contract

Use this contract only after the parent skill verifies the repository declared
by the consuming project's applicable `AGENTS.md`.

## Optional live template ownership

When a `TEMPLATE_READY` packet is supplied or applicable project instructions
require a live template, the verified repository's current live issue forms,
including YAML and legacy Markdown forms selected by the template gate, are
authoritative. Do not
keep a static form list, title prefix, label list, option list, or required-field
map in this skill. Select one form from the primary player-visible object and
preserve its field labels and order exactly. Split independent deliverables
instead of blending forms.

When no template is required, do not inspect or infer a live form. Use the
canonical fallback format below and record why template selection was optional.
When maintaining a form, prefer class-level forms and capture only fields that
the repository genuinely requires. Template maintenance is a separate mutation
from creating an issue and requires explicit authorization.

## Intake format and boundary

Set exactly one format:

| Format | Selection rule | Required record |
|---|---|---|
| `template` | A supplied `TEMPLATE_READY` packet or applicable project instruction requires a live template. | Current template path, ref, digest, fields, and labels. |
| `fallback` | No template was requested and project instructions impose none. | `template: null`, a stable `template_optional_reason`, and the canonical field order below. |

The canonical fallback field order is: `Title`, `Goal`, `Observed behavior`,
`Desired behavior`, `Scope and non-goals`, `Reproduction or context`, and
`Research requirements`. Preserve every heading even when its content is
`Not applicable` with a concrete reason. The fallback is a deterministic
intake format, not permission to synthesize a repository template.

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
  path: .github/ISSUE_TEMPLATE/example.yml | null
  ref: verified default-branch revision | null
  digest: sha256 | null
format: template | fallback
template_optional_reason: string | null
template_packet: TemplatePacket | null
title: English title with live prefix
labels: []
label_selection:
  - name: existing repository label
    source: template | issue_context
    rationale: exact template configuration or issue fact
    verified_at: ISO-8601
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
  - code: repository | template | duplicate | missing_label | ambiguous_label | provider
    evidence: []
    question: { id: IQ1, missing: string, options: [], answer_needed: string }
confidence: high | medium | low
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
2. Build an add-only label selection before any mutation. Preserve every label
   configured by the verified live template. An additional label is eligible
   only when it already exists in the exact repository and its relevance is
   directly supported by the issue's requested object, scope, or stated
   classification. Record `source`, issue-specific `rationale`, and
   verification time for each selection. Do not use a label merely because its
   name sounds related.
3. Confirm every selected label exists in the current repository label set.
   A missing label returns `INTAKE_BLOCKED` with `code: missing_label`; unclear
   relevance returns `INTAKE_BLOCKED` with `code: ambiguous_label`. Both leave
   `mutation.performed: []` and require no label mutation.
4. Validate English title/body, exact live prefix and field order, links, and
   absence of local paths and secrets.
5. Create once with the exact repository argument and only the selected
   existing labels. Applying those labels is part of the authorized create, not
   a later issue edit.
6. Read back repository, number, URL, title, labels, body, and revision; prove
   that every selected label is present and record no removals.
7. After an ambiguous result, search for the exact title/body before retrying.

For `template`, re-read and compare the selected template digest immediately
before creation. A mismatch invalidates the entire IntakePacket: return to the
template gate, take a fresh snapshot, attach a newly selected
`TEMPLATE_READY` packet, rebuild the body, repeat duplicate and label checks,
and only then create. Never create from a stale packet. For `fallback`, verify
the canonical field order and that no template requirement was introduced by
the current applicable instructions.
If a selected label is missing, do not create it: return `INTAKE_BLOCKED` with
`code: missing_label` and a separate label-maintenance handoff. Provider errors
populate `provider_failure` with operation, provider status, retryability,
preserved evidence, and `mutation_performed: false | unknown`; an unknown create
result always requires exact title/body search before retry authorization.

Creating an issue does not authorize comments, later label edits, relationships,
projects, milestones, implementation, commits, pushes, or pull requests. It
authorizes only applying the verified add-only `label_selection` during creation.

After verified standalone intake, ask once whether to start
`rebirthuo-issue-research`. In workflow mode, continue automatically and do not
ask the same phase-transition question.
