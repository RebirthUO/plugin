# Issue-to-PR State Machine

Use this reference after loading `rebirthuo-issue-workflow`. Child skills remain
authoritative for their own packets and gates.

## Route classification

| Route | Evidence | First state | Rule |
|---|---|---|---|
| `NEW_REQUEST` | No user-identified live issue | `INTAKE` | Create exactly one issue through required-template or governed-fallback intake. |
| `EXISTING_ISSUE` | The user points to a specific issue URL or number in the verified repository | `RESEARCH` | Do not call issue creation or open a duplicate. |
| `ROUTE_UNKNOWN` | Issue reference or repository cannot be matched safely | `INTERVIEW_PENDING` | Ask one focused identity question; do not mutate. |

Resolve the repository only from applicable `AGENTS.md` instructions. Verify it
through the provider API before every read or write and pass it explicitly to
each provider command. Never infer it from the working directory, remotes,
organization, nearby repositories, prior sessions, or an issue number alone.

## State transitions

```text
NEW_REQUEST
  -> [TEMPLATE_GATE when required] -> INTAKE -> RESEARCH -> READY -> IMPLEMENT -> PR_VERIFY -> DELIVERED
                         ^            |          ^        |
                         |            v          |        v
                         +---- INTERVIEW_PENDING +-- RESEARCH

EXISTING_ISSUE -> RESEARCH
```

When used, `TEMPLATE_GATE` produces `TemplatePacket: TEMPLATE_READY`, including
preserved template labels and a live repository label inventory. `INTAKE`
produces an `IntakePacket` with `format: template | fallback`; it may create
one issue when the full workflow request is current and explicit, then continues
without another confirmation. `RESEARCH`
produces a `ResearchPacket` with `execution_state` and
`implementation_readiness: READY | BLOCKED | null`
and requires a scoped format-preserving issue rewrite on every completed run.
`IMPLEMENT` produces `ImplementationResult`. Any stale issue revision, template
revision, repository mismatch, unverified write, missing research publication,
test regression, or new behavior-changing gap transitions to
`INTERVIEW_PENDING` or `RESEARCH` rather than forward.

## Optional template and intake integrity

On the new-request route, invoke `rebirthuo-issue-template-gate` only when the
request or applicable project instructions require a live template. Its path,
revision, digest, required fields, labels, and rationale must be carried into
the `IntakePacket`, and the form must be re-read immediately before creation.
If it changed, repeat selection; never apply a stale field map.

When no template is required, `rebirthuo-issue-create` uses its canonical
fallback field order. Record `format: fallback`, `template: null`, and the
reason that made template selection optional. Do not probe, select, or block on
repository templates in this route, and do not invent a request-specific
format.

Carry template labels and `IntakePacket.label_selection` unchanged to research.
The workflow does not decide whether a label is relevant or perform label
mutations; intake and research own their respective add-only checks and
read-backs.

When a template is required, an absent, genuinely ambiguous, or mismatched
template requires a `TemplateQuestions` packet. The user may identify one
current candidate or provide missing request context. Editing a template
remains a separate request.

## Research-exhaustion and EA-clarity gate

Before interview, research must decompose claims, infer era from issue context,
official chronology and repository gates, expand aliases/source routes, retry
misses materially differently, inspect implementation evidence, and audit the
readiness matrix. A first failed query is never an interview trigger.

`READY` means every relevant row is either `verified` or explicitly
`not-applicable` with a scope rationale:

- Each expected gameplay claim has an era-scoped OSI, EA, or Broadsword source.
- Conflicting or unavailable official evidence remains a blocker; repository,
  client, emulator, archive, or community material cannot replace it.
- User interview answers resolve only product, scope, policy, or acceptance
  decisions. If they intentionally differ from official behavior, label them
  `Custom policy`; never rewrite the official evidence ledger.
- Current implementation, observable delta, persistence/lifecycle/security
  impact, acceptance criteria, and validation boundaries are all explicit.

For a non-gameplay change, mark official behavior `not-applicable` and explain
why. This is the only way to bypass an official-mechanics row; do not claim
EA clarity by omission.

## Interview packet and resumption

Ask the minimum focused set of last-mile product questions needed to advance
one state. Every
question must include a stable ID, missing decision or claim, evidence already
checked, supported options when available, risk of guessing, and the exact
answer needed. Return:

```yaml
workflow_checkpoint:
  state: INTERVIEW_PENDING
  route: NEW_REQUEST | EXISTING_ISSUE
  repository: owner/repository
  issue_revision: null | ISO-8601 plus digest
  completed_states: []
  questions: []
  next_state_after_answers: TEMPLATE_GATE | INTAKE | RESEARCH
```

Do not report success, choose defaults, edit code, or make an unrelated GitHub
mutation while this packet is open. After an answer, record it, re-read the
affected live issue/template, repeat only the invalidated claim research with fresh
issue publication, replace the obsolete text with the answer, remove the
resolved requirement/blocker, and ask again if a blocker remains. Continue
until the packet is `COMPLETE`/`READY` or the user explicitly stops the workflow.

## Implementation and publication

Before implementation, require the matching live post-publication issue revision
and `COMPLETE`/`READY` packet with a completed format-preserving body rewrite, no appended
research report, no unresolved requirement/blocker text, and no `blocked`
label. Create a new isolated worktree from the verified intended base and a
unique scoped branch. Preserve the user's existing checkout and unrelated
changes. If the implementation discovers an unknown, save the checkpoint and
return to autonomous research before asking; do not commit a guessed solution.

An explicit full-workflow request authorizes continuation across optional template selection,
intake, research, implementation, scoped push, and PR creation. Do not repeat a
phase-continuation question. This does not authorize merge, release, deployment,
or unrelated GitHub mutations.

After final scoped validation, stage only in-scope paths, commit, push the
verified remote branch, create or update the PR, and read back its URL, head,
base, state, remote SHA, body, and checks. A merge, release, deployment,
unrelated comment, unrelated label, or project update is out of scope unless
separately requested. Scoped format-preserving body rewrites and
`blocked`-label toggles and add-only, justified existing-label actions from
`rebirthuo-issue-research` are in scope for the research phase.

Execute commit, push, PR create/update, and PR verification as separate
read-backed steps. After a partial failure, return `DELIVERY_BLOCKED` with the
last proven step and do not repeat it. Re-read local commit, remote branch SHA,
and existing PR before resuming; retry only the unproven step. Access failure,
unsafe concurrent state, or ambiguous read-back remains blocked.

## WorkflowResult

Use this envelope in every state; unknown values are `null`, not omitted.

```yaml
state: REPOSITORY_BLOCKED | TEMPLATE_BLOCKED | INTAKE_BLOCKED | INTERVIEW_PENDING | RESEARCH_BLOCKED | IMPLEMENTATION_BLOCKED | DELIVERY_BLOCKED | DELIVERED
route: NEW_REQUEST | EXISTING_ISSUE | ROUTE_UNKNOWN
repository: { full_name: owner/repository, verified_at: ISO-8601 }
intake_format: template | fallback | null
template: { status: null, path: null, ref: null, digest: null, optional_reason: null }
issue: { number: null, url: null, updated_at: null, body_digest: null }
labels: { selected: [], applied: [], rationale: [], read_back: [] }
research: { execution_state: null, implementation_readiness: null, revision: null, packet_digest: null }
interviews: []
research_loops: []
implementation: { state: null, worktree: null, branch: null, base: null, validation: [] }
blockers: []
delivery_checkpoint:
  last_proven_step: none | commit | push | pr_write | pr_verify
  local_sha: null
  remote_sha: null
  pr_url: null
  failed_step: null
  retryable: false
pull_request: { url: null, remote_sha: null, head: null, base: null, body_digest: null, state: null, checks: [] }
mutations: { performed: [], failed: [] }
confidence: { level: high | medium | low, evidence_limitations: [], environment_blockers: [] }
questions: []
```

Map child checkpoints deterministically:

| Child checkpoint | WorkflowResult state | Resume target |
| --- | --- | --- |
| required template `TEMPLATE_BLOCKED` or `TEMPLATE_PROVIDER_BLOCKED` | `TEMPLATE_BLOCKED` | template gate |
| create blocked/provider/ambiguous mutation outcome | `INTAKE_BLOCKED` | create |
| research `ISSUE_INPUT_BLOCKED` | `INTERVIEW_PENDING` | affected research rows |
| research repository, authorization, publication, or provider block | `RESEARCH_BLOCKED` | research |
| implement `NOT_READY`, `RESEARCH`, or implementation/validation block | `IMPLEMENTATION_BLOCKED` | research when unknown, otherwise implement |
| implement publication failure | `DELIVERY_BLOCKED` | first unproven delivery step |
| verified implement delivery | `DELIVERED` | none |

`INTERVIEW_PENDING` requires questions; all blocked states require at least one
machine-readable entry in `blockers` plus their owning child checkpoint.
`DELIVERY_BLOCKED` requires a failed step and last proven state. `DELIVERED`
requires `blockers: []`, verified PR URL, matching SHA/head/base,
body/state/checks, and high confidence.
