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
  confidence: high | medium | low
  confidence_rationale: directness, freshness, agreement, and remaining limits
```

Official evidence defines expected OSI/EA behavior. Community archives may help
locate official material. ModernUO, ServUO, RunUO, freeshards, client data, and
the target repository establish implementation or presentation facts only.

Confidence calibration is deterministic: `high` requires direct applicable
official evidence, correct current or historical scope, no material conflict,
and reachable implementation evidence where relevant; `medium` permits
indirect or older official evidence with corroboration and no unresolved
behavior-changing gap; `low` applies to conflicting, unavailable, stale,
unreachable, or policy-dependent material evidence. Packet confidence is the
lowest material claim confidence and lists every limiting claim ID.

## Research exhaustion protocol

Complete and record every stage before marking official evidence unavailable
or asking the user:

1. Decompose the issue into atomic claims and collect terminology, aliases,
   objects, systems, dates, publishes, and expansions.
2. Infer likely era from issue facts, official chronology,
   `uo-publish-expansion-mapping`, repository era gates/configuration, and prior
   explicit decisions. Record eliminated candidates and reasons.
3. Search current official sources, then historical official publish notes,
   guides, archives, and adjacent official pages through `uo-official-evidence`.
4. For every miss, perform at least one materially different pass using changed
   terminology, alias, publish/expansion framing, or source route. Repeating the
   same query or endpoint does not count.
5. Inspect target code and relevant RebirthUO/ModernUO domain skills for actual
   implementation and tests without promoting that evidence to official truth.
6. Reconcile conflicts and audit every readiness row. Only then classify a
   claim `unavailable` or `conflicting`.

```yaml
research_attempts:
  - claim_id: C1
    pass: 1
    route: current-official | historical-official | alias-expansion | adjacent-page | repository
    queries_or_locations: []
    result: found | conflict | no-result
era_inference:
  candidates: []
  selected: null
  evidence: []
  ambiguity_is_product_intent: false
```

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

Do not make a conservative default. Ask only after the exhaustion protocol
cannot answer a product decision. Offer supported choices to narrow scope,
supply a direct official source, or authorize a visibly labeled custom policy.
Do not ask the user to perform another generic search.

```yaml
user_questions:
  - id: Q1
    missing: exact decision
    evidence_checked: []
    options: []
    risk_if_guessed: concrete consequence
    answer_needed: one focused response
    resume_claim_ids: [C1]
```

Stop after returning blocking questions in chat, but still publish the current
findings to the issue unless the user requested advice-only work. Explicit user
answers are recorded as `Custom policy` if they intentionally differ from
official UO; they never rewrite the official evidence.

## Issue publication

[Issue publication](issue-publication.md) is the single normative mutation,
concurrency, authorization, retry, and read-back contract. This section defines
only the research packet handoff into that contract.

Pass the desired implementation readiness, live issue identity/revision, and
replacement body to that contract, then record its returned state and proven
actions without restating or weakening its authority rules here.

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
evidence_ledger: []
research_attempts: []
era_inference: {}
expected_actual_delta: []
user_decisions: []
readiness_matrix: {}
blocking_gaps: []
non_blocking_gaps: []
acceptance_criteria: []
test_plan: []
risks: []
issue_publication:
  state: pending | skipped | succeeded | partial | failed
  body_rewrite:
    state: pending | skipped | succeeded | failed
    format_source_digest: pre-publication body digest
    headings_preserved: []
    updated_fields: []
    removed_obsolete_items: []
    unresolved_items_retained: []
    appended_sections: []
    title_changed: false
  labels:
    blocked_applied: false
    blocked_removed: false
    selected: []
    existing_relevant_applied: []
    selection_rationale: []
    read_back: []
  recovery: { retryable: false, last_proven_step: null, failed_step: null, exact_action: null }
mutation:
  authorized: true | false
  performed: []
  failed: []
confidence: { level: high | medium | low, rationale: string, limited_claim_ids: [] }
execution_state: ACTIVE | RESEARCH_REPOSITORY_BLOCKED | ISSUE_INPUT_BLOCKED | ADVICE_COMPLETE | AUTHORIZATION_REQUIRED | PUBLICATION_BLOCKED | COMPLETE
implementation_readiness: READY | BLOCKED | null
```

Record `issue.updated_at` and `body_digest` after publication, not before. A
later issue edit invalidates `READY` until the changed body is reviewed.

Populate `mutation.performed` only with actions proven by read-back. Never list
mutually exclusive label actions prospectively. Advice-only uses publication
state `skipped`, `authorized: false`, empty action arrays,
`execution_state: ADVICE_COMPLETE`, and null implementation readiness. Any
partial failure uses `execution_state: PUBLICATION_BLOCKED`. Only `COMPLETE`
may carry implementation readiness `READY`.

The evidence ledger, readiness matrix, resolved marker mapping, and answered
questions stay in the `ResearchPacket`; do not append them as a second issue
format. The published body contains their current user-facing conclusions in
the existing issue fields. `READY` requires `unresolved_items_retained: []` and
an issue body with no `RESEARCH_REQUIRED`, blocker, or research-contract
scaffolding.
