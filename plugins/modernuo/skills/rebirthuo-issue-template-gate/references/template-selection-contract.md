# Live Issue Template Selection Contract

Use this contract only after the parent skill determines that a live template
is required and resolves and verifies the exact repository from applicable
project `AGENTS.md` instructions. When template intake is optional, do not load
this contract; return `TEMPLATE_NOT_REQUIRED` and hand off to fallback intake.

## Snapshot

Inspect the current default-branch revision and the repository's complete
`.github/ISSUE_TEMPLATE/` directory before selecting anything. Include YAML
issue forms, legacy Markdown templates when present, and chooser/configuration
files that influence the available templates. Record the path, revision, and a
content digest for every candidate; do not retain a static template inventory.

The live template controls title prefixes, labels, field labels/order, allowed
options, required fields, and user-facing wording. Repository instructions can
add constraints, but cannot be guessed from an adjacent checkout.

Also snapshot the exact repository's current label inventory separately from
template labels. The gate does not select, apply, create, remove, or infer any
additional labels; it supplies the live inventory to downstream intake and
research for their add-only, issue-specific selection checks.

## Matching protocol

Create a candidate table from the live forms. Compare each candidate against:

- the user's stated goal, observed problem, desired outcome, and non-goals;
- the primary player-visible object or system affected;
- the form's title, description, labels, required fields, and configured
  options; and
- whether each required field has a user-provided value or a claim-specific
  research placeholder with risk and research owner.

Select only when one form is the unambiguous best match. A template is not a
match merely because its title sounds close or because a generic field can be
filled. Preserve the live field labels and order; do not copy a remembered or
previously cached form.

## Blocking outcomes

Return `TEMPLATE_BLOCKED` and ask the user when any of these occurs:

| Condition | Required question |
|---|---|
| No live template exists | Ask whether the user wants to supply an intended template or separately authorize template maintenance. |
| No candidate fits | Ask which live form should govern the request or what missing issue context distinguishes it. |
| Multiple candidates fit | Present only the current candidate names and their material differences; ask the user to select one. |
| User-owned required field is unclear | Ask for the exact missing intent value; do not fabricate it. |
| Template changed before creation | Reconfirm the selection from the current snapshot. |

Do not fall back to a free-form issue. A request to create, edit, or repair a
repository template is separate from issue intake and needs separate mutation
authority.

Do not block on a mechanics field that official or repository research can
answer. Record a structured placeholder instead. Do not ask for an era or
expansion until research has inspected issue context, official chronology,
repository configuration, and existing decisions and still finds multiple
materially different product-valid targets.

## TemplatePacket

Use these record shapes; empty arrays remain valid:

```yaml
candidate: { path: string, digest: sha256, title: string, labels: [], fit: exact | rejected, reasons: [] }
field: { id: string, label: string, required: true, source: user | research, value: string | null }
research_placeholder: { id: R1, field_id: string, claim: string, risk: string, owner: string }
question: { id: TQ1, missing: string, candidates: [], evidence_checked: [], answer_needed: string }
provider_failure: { operation: string, status: string, retryable: true | false, evidence_preserved: [], mutation_performed: false }
```

```yaml
repository:
  full_name: owner/repository
  html_url: canonical URL
  instruction_file: path/to/AGENTS.md
  verified_at: ISO-8601
template_inventory:
  ref: default-branch SHA
  candidates: []
repository_label_inventory:
  checked_at: ISO-8601
  labels: []
template:
  status: TEMPLATE_READY | TEMPLATE_BLOCKED | TEMPLATE_PROVIDER_BLOCKED
  path: .github/ISSUE_TEMPLATE/example.yml
  ref: default-branch SHA
  digest: sha256
  title_prefix: exact live prefix
  labels: []
  fields: []
  selection_rationale: exact distinguishing facts
  research_placeholder_fields: []
  confidence: high | medium | low
  residual_uncertainty: []
questions: []
provider_failure: null | { operation: string, status: string, retryable: true | false, evidence_preserved: [], mutation_performed: false }
mutation:
  performed: []
```

For `TEMPLATE_READY`, `path`, `ref`, `digest`, `title_prefix`, `fields`,
`template.labels`, `repository_label_inventory`, and
`selection_rationale` are required. For `TEMPLATE_BLOCKED`, `questions` is
required and selection fields are null. For `TEMPLATE_PROVIDER_BLOCKED`,
`provider_failure` is required and selection fields are null. The parent must
attach the complete packet to the `IntakePacket` and revalidate its selected
template immediately before issue creation.

For a `TEMPLATE_NOT_REQUIRED` handoff, emit only the verified project
instruction evidence, the explicit request evidence, `mutation.performed: []`,
and `template: null`; do not create a candidate inventory or contact the
provider. The intake contract owns the fallback format.
