# Issue-to-PR State Machine

Use this reference after loading `modernuo-issue-workflow`. Child skills remain
authoritative for their own packets and gates.

## Route classification

| Route | Evidence | First state | Rule |
|---|---|---|---|
| `NEW_REQUEST` | No user-identified live issue | `INTAKE` | Create exactly one issue only after template selection. |
| `EXISTING_ISSUE` | The user points to a specific issue URL or number in the verified repository | `RESEARCH` | Do not call issue creation or open a duplicate. |
| `ROUTE_UNKNOWN` | Issue reference or repository cannot be matched safely | `INTERVIEW_PENDING` | Ask one focused identity question; do not mutate. |

Resolve the repository only from applicable `AGENTS.md` instructions. Verify it
through the provider API before every read or write and pass it explicitly to
each provider command. Never infer it from the working directory, remotes,
organization, nearby repositories, prior sessions, or an issue number alone.

## State transitions

```text
NEW_REQUEST
  -> TEMPLATE_GATE -> INTAKE -> RESEARCH -> READY -> IMPLEMENT -> PR_VERIFY -> DELIVERED
                         ^            |          ^        |
                         |            v          |        v
                         +---- INTERVIEW_PENDING +-- RESEARCH

EXISTING_ISSUE -> RESEARCH
```

`TEMPLATE_GATE` produces `TemplatePacket: TEMPLATE_READY`. `INTAKE` produces
an `IntakePacket`; it may create one issue when the full workflow request is
current and explicit. `RESEARCH` produces `ResearchPacket: READY | BLOCKED`
and requires scoped issue publication on every completed run. `IMPLEMENT`
produces `ImplementationResult`. Any stale issue revision, template revision,
repository mismatch, unverified write, missing research publication, test
regression, or new behavior-changing gap transitions to `INTERVIEW_PENDING` or
`RESEARCH` rather than forward.

## Template and intake integrity

On the new-request route, invoke `modernuo-issue-template-gate` inside the
preflight of `modernuo-issue-create`. Its template path, revision, digest,
required fields, labels, and selection rationale must be carried into the
`IntakePacket`. Re-read the selected form immediately before issue creation.
If it changed, repeat template selection; never apply a stale field map or
invent a generic issue format.

An absent, ambiguous, or mismatched template requires a `TemplateQuestions`
packet. The user may identify one current candidate or provide missing request
context. Editing a template or proceeding with a non-template issue is a
separate request; this workflow does not assume either permission.

## EA-clarity gate

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

Ask the minimum focused set of questions needed to advance one state. Every
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
  next_state_after_answers: TEMPLATE_GATE | RESEARCH
```

Do not report success, choose defaults, edit code, or make an unrelated GitHub
mutation while this packet is open. After an answer, record it, re-read the
affected live issue/template, repeat only the invalidated research with fresh
issue publication, and ask again if a blocker remains. Continue until the packet
is `READY` or the user explicitly stops the workflow.

## Implementation and publication

Before implementation, require the matching live post-publication issue revision
and `READY` packet with completed body-only issue publication and no `blocked`
label. Create a new isolated worktree from the verified intended base and a
unique scoped branch. Preserve the user's existing checkout and unrelated
changes. If the implementation discovers an unknown, save the checkpoint and
return to research; do not commit a guessed solution.

After final scoped validation, stage only in-scope paths, commit, push the
verified remote branch, create or update the PR, and read back its URL, head,
base, state, remote SHA, body, and checks. A merge, release, deployment,
unrelated comment, unrelated label, or project update is out of scope unless
separately requested. Scoped body updates and `blocked`-label toggles from
`modernuo-issue-research` are in scope for the research phase.
