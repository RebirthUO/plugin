# Issue Research Contract

## Evidence ledger

Record each claim separately:

```yaml
- id: C1
  statement: exact expected or actual claim
  official_evidence:
    status: verified | conflicting | unavailable
    urls: []
    era_or_publish: exact scope
    checked_at: ISO-8601
  implementation_evidence:
    repository: owner/repository
    revision: commit or default-branch SHA
    paths: []
    status: match | partial | absent | custom | unreachable
  user_decision:
    required: true
    question_id: Q1
    answer: null
```

Official evidence defines expected OSI/EA behavior. Community archives may help
locate official material. ModernUO, ServUO, RunUO, freeshards, client data, and
the target repository establish implementation or presentation facts only.

## Readiness matrix

Every relevant row must be explicit:

| Surface | Required result |
|---|---|
| Identity | Exact repository, issue, revision, and intended base |
| Official behavior | Era-scoped OSI/EA behavior with official citations |
| Current implementation | Verified code/data/registration/tests and reachability |
| Delta | Observable expected-versus-actual difference |
| Scope | Included surfaces and explicit non-goals |
| Product impact | PvP/PvM, economy, housing/storage, client and player trust |
| Safety | Persistence, lifecycle, exploit/security and rollback |
| Acceptance | Observable boundaries and pass/fail values |
| Validation | Focused tests, owning tests, build and any manual check |

`READY` requires every relevant row and no blocking gap.

## Blocking rules

A gap is blocking when it can change:

- official behavior, era, formula, ordering, duration, cap, target, or
  restriction;
- implementation architecture, data ownership, registration, persistence, or
  lifecycle;
- acquisition, distribution, loot, economy, PvP/PvM, client presentation, or
  exploit surface;
- acceptance criteria, boundary values, or the test oracle.

Do not make a conservative default. Ask the user only after the official-source
and repository checks cannot answer the question.

```yaml
user_questions:
  - id: Q1
    missing: exact decision
    evidence_checked: []
    options: []
    risk_if_guessed: concrete consequence
    answer_needed: one focused response
```

Stop after returning blocking questions. Explicit user answers are recorded as
`Custom policy` if they intentionally differ from official UO; they never
rewrite the official evidence.

## ResearchPacket

```yaml
repository:
  full_name: owner/repository
  html_url: canonical URL
issue:
  number: 123
  url: canonical issue URL
  updated_at: ISO-8601
  body_digest: digest
official_evidence: []
implementation_evidence: []
expected_actual_delta: []
user_decisions: []
readiness_matrix: {}
blocking_gaps: []
non_blocking_gaps: []
acceptance_criteria: []
test_plan: []
risks: []
proposed_body_diff: null
mutation:
  authorized: false
  performed: []
readiness: READY | BLOCKED
```

Before handoff, re-read the live issue and update the revision fields. A later
issue edit invalidates `READY` until the changed contract is reviewed.
