# Issue Research Publication

Use this contract after analysis completes for a verified issue in the exact
repository declared by the consuming project's applicable `AGENTS.md`.
Publication requires an explicit issue-update request or scoped authority from
an explicit full `rebirthuo-issue-workflow`. Without it, return
`AUTHORIZATION_REQUIRED` with the proposed body and label action and mutate
nothing. Advice-only remains read-only without an authorization prompt.

Scoped publication authorizes only:

- one format-preserving body rewrite on the identified issue;
- an add-only application of existing, issue-specifically justified labels;
- a `blocked` label toggle on that issue (`--add-label` when `BLOCKED`,
  `--remove-label` when `READY`);
- read-back of the updated issue revision, labels, and body digest.

It does not authorize issue comments, unrelated labels, label removals,
projects, milestones,
issue creation, commits, pushes, or pull requests.

## Publication boundary

1. Re-read the live issue immediately before writing. If `updated_at` or the
   body digest changed, automatically rebuild only when changes are disjoint and
   every user-authored change is preserved. Any overlapping or ambiguous change
   returns `PUBLICATION_BLOCKED` and requires renewed authorization before an
   overwrite; never silently reconcile it.
2. Treat the live body as the formatting source. Preserve its heading order,
   field labels, option wording, and overall Markdown structure. Do not add a
   `## Research contract`, research history, duplicate field, or other appended
   report.
3. Rewrite the content under the existing headings so the body describes only
   the current researched request:
   - replace stale, speculative, or contradicted claims with verified wording;
   - incorporate resolved answers into the relevant field;
   - remove each resolved `RESEARCH_REQUIRED[Rn]` marker and its associated
     `Why it matters` line;
   - remove answered questions, resolved blockers, obsolete requirements, and
     superseded alternatives;
   - retain unresolved requirements or blockers only in their original relevant
     fields, with stable IDs that match the current `ResearchPacket`;
   - remove a stale appended `## Research contract` section if one exists,
     migrating still-current facts into the existing issue fields first.
4. Keep every existing heading, even when its content becomes concise or
   `Not applicable` with a researched rationale. Do not invent a new template
   or reorder fields. Preserve user-authored context that remains current and
   relevant; rewriting is not permission to erase the issue's goal, observed
   behavior, reproduction, non-goals, or valid decisions.
5. Write in English. Do not include internal packet metadata, readiness status,
   repository revisions, local paths, credentials, or secrets in the issue
   body unless the existing template explicitly requests that information.
6. Before any mutation, select additional labels only from the live repository
   label set. Each must be supported directly by the current issue's requested
   object, scope, template classification, or researched conclusion; record
   that evidence as its rationale. Preserve applicable template labels. A
   missing label or ambiguous relevance returns `PUBLICATION_BLOCKED` before
   body rewrite and with no mutation; never guess from label names.
7. Verify the repository label set contains `blocked` before toggling it. If the
   label is missing, stop and ask the user; do not publish with a guessed
   substitute label.
8. Apply one step at a time and read back after each: body rewrite, selected
   add-only labels, required `blocked` action, then final full issue. Record
   only proven actions. If a later
   step fails, return `PUBLICATION_BLOCKED` with state `partial`, successful and
   failed steps, live revision, retryability, and exact recovery action.
9. Do not edit the issue title or post issue comments. The rewritten body is
   the only canonical publication surface.

## Rewrite model

Build the replacement body from the live issue, field by field:

```yaml
body_rewrite:
  format_source: live pre-publication body
  headings:
    preserved: true
    order_preserved: true
    added: []
  content:
    updated_fields: []
    preserved_fields: []
    removed_obsolete_items: []
    unresolved_items_retained: []
  removed_sections:
    - Research contract
```

For `READY`, no `RESEARCH_REQUIRED`, unresolved blocker, or question text may
remain. For `BLOCKED`, keep only current unresolved items in the relevant
existing fields and reference their stable IDs in the internal packet. A
historical `## Research contract` is obsolete publication scaffolding, not part
of the preserved format.

## Blocked label rules

| Readiness | Label action |
|---|---|
| `BLOCKED` | Add `blocked` when the label exists and is not already present |
| `READY` | Remove `blocked` when it is present |

Add only selected existing labels with recorded issue-specific rationale. Never
remove, rename, create, or bulk-synchronize labels. `blocked` is the sole
readiness-state label and retains the toggle above; all other label changes
remain separately authorized.

## Provider commands

Pass the verified repository explicitly to every command:

```bash
gh api repos/{owner}/{repository}
gh label list --repo {owner}/{repository}
gh issue view {number} --repo {owner}/{repository} --json body,updatedAt,url,labels
gh issue edit {number} --repo {owner}/{repository} --body-file research-body.md
gh issue edit {number} --repo {owner}/{repository} --add-label {selected-label}
gh issue edit {number} --repo {owner}/{repository} --add-label blocked
gh issue edit {number} --repo {owner}/{repository} --remove-label blocked
```

After publication, read back the issue body, `updated_at`, labels, and digest.
Verify heading identity/order, cleaned content, absence of an appended research
section, title's unchanged value, every selected label, and the absence of
label removals. Record the body rewrite and label actions in
`mutation.performed`.

Retries are idempotent and state-aware: re-read first, skip an already-proven
body or label state, and retry only the failed operation. Authentication,
authorization, rate-limit, transport, malformed response, or read-back mismatch
returns `failed` or `partial`; never claim `READY` and never repeat a write whose
result is unknown.

## Read-only outcomes

When the user explicitly asks for advice only and forbids GitHub mutation, skip
publication, set publication state `skipped`, set `mutation.authorized: false`,
leave action arrays empty, and report research confidence without a
post-publication readiness claim. This is the only read-only completion path.
For ordinary research without publication authority, use publication state
`pending`, execution state `AUTHORIZATION_REQUIRED`, include the proposed body
and label action, and leave mutation arrays empty.
