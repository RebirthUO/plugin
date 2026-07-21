# Live Issue Template Selection Contract

Use this contract only after the parent skill resolves and verifies the exact
repository from applicable project `AGENTS.md` instructions.

## Snapshot

Inspect the current default-branch revision and the repository's complete
`.github/ISSUE_TEMPLATE/` directory before selecting anything. Include YAML
issue forms, legacy Markdown templates when present, and chooser/configuration
files that influence the available templates. Record the path, revision, and a
content digest for every candidate; do not retain a static template inventory.

The live template controls title prefixes, labels, field labels/order, allowed
options, required fields, and user-facing wording. Repository instructions can
add constraints, but cannot be guessed from an adjacent checkout.

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
  confidence: high | blocked
  residual_uncertainty: []
questions: []
provider_failure: null
mutation:
  performed: []
```

The parent must attach this packet to the `IntakePacket` and revalidate its
selected template immediately before issue creation.
