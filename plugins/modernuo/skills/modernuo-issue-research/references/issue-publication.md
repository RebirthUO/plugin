# Issue Research Publication

Use this contract after analysis completes for a verified issue in the exact
repository declared by the consuming project's applicable `AGENTS.md`. Every
completed research run publishes findings to that issue unless the user
explicitly requested advice-only work with no GitHub mutation.

Scoped publication authorizes only:

- one format-preserving body rewrite on the identified issue;
- a `blocked` label toggle on that issue (`--add-label` when `BLOCKED`,
  `--remove-label` when `READY`);
- read-back of the updated issue revision, labels, and body digest.

It does not authorize issue comments, unrelated labels, projects, milestones,
issue creation, commits, pushes, or pull requests.

## Publication boundary

1. Re-read the live issue immediately before writing. If `updated_at` or the
   body digest changed since the research capture, reconcile or stop and ask the
   user before overwriting concurrent edits.
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
6. Verify the repository label set contains `blocked` before toggling it. If the
   label is missing, stop and ask the user; do not publish with a guessed
   substitute label.
7. Apply the body rewrite, toggle the `blocked` label, then read back the full
   issue and record the post-publication revision in the `ResearchPacket`.
8. Do not edit the issue title or post issue comments. The rewritten body is
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

Do not add unrelated labels during scoped publication. Other label changes
remain separately authorized.

## Provider commands

Pass the verified repository explicitly to every command:

```bash
gh api repos/{owner}/{repository}
gh label list --repo {owner}/{repository}
gh issue view {number} --repo {owner}/{repository} --json body,updatedAt,url,labels
gh issue edit {number} --repo {owner}/{repository} --body-file research-body.md
gh issue edit {number} --repo {owner}/{repository} --add-label blocked
gh issue edit {number} --repo {owner}/{repository} --remove-label blocked
```

After publication, read back the issue body, `updated_at`, labels, and digest.
Verify heading identity/order, cleaned content, absence of an appended research
section, and the title's unchanged value. Record the body rewrite and label
toggle in `mutation.performed`.

## Advice-only exception

When the user explicitly asks for advice only and forbids GitHub mutation, skip
publication, leave `issue_publication` empty, and set
`mutation.authorized: false`. This is the only read-only completion path.
