# Issue Research Publication

Use this contract after analysis completes for a verified issue in the exact
repository declared by the consuming project's applicable `AGENTS.md`. Every
completed research run publishes findings to that issue unless the user
explicitly requested advice-only work with no GitHub mutation.

Scoped publication authorizes only:

- one `## Research contract` body update on the identified issue;
- a `blocked` label toggle on that issue (`--add-label` when `BLOCKED`,
  `--remove-label` when `READY`);
- read-back of the updated issue revision, labels, and body digest.

It does not authorize issue comments, unrelated labels, projects, milestones,
issue creation, commits, pushes, or pull requests.

## Publication boundary

1. Re-read the live issue immediately before writing. If `updated_at` or the
   body digest changed since the research capture, reconcile or stop and ask the
   user before overwriting concurrent edits.
2. Preserve the original intake text. Replace only the `## Research contract`
   section when it already exists; otherwise append it after the intake body.
3. Write in English. Do not include local paths, credentials, or secrets.
4. Verify the repository label set contains `blocked` before toggling it. If the
   label is missing, stop and ask the user; do not publish with a guessed
   substitute label.
5. Apply the body update, toggle the `blocked` label, then read back the full
   issue and record the post-publication revision in the `ResearchPacket`.
6. Do not post issue comments. The body section is the only canonical
   publication surface.

## Body section template

Replace or append exactly one `## Research contract` section. This section is
the single source of truth for the current research run:

```markdown
## Research contract

**Readiness:** READY | BLOCKED
**Research run:** ISO-8601 timestamp
**Repository revision:** owner/repository @ commit-or-branch-sha
**Issue revision before:** ISO-8601 digest-before
**Issue revision after:** ISO-8601 digest-after

### Official behavior
- Era/publish scope:
- Expected behavior summary:
- Official sources:
  - https://...

### Current implementation
- Verified paths and status:
- Registration/reachability:

### Evidence highlights
- Official:
  - C1: statement — verified | conflicting | unavailable — urls
- Implementation:
  - C2: statement — match | partial | absent | custom | unreachable — paths

### Delta
- Expected versus actual:

### Scope
- Included:
- Non-goals:

### Acceptance criteria
- READY: numbered observable pass/fail boundaries
- BLOCKED: list unresolved blockers instead

### Validation
- Focused tests:
- Build/manual checks:

### Resolved research markers
- RESEARCH_REQUIRED[R1]: answer or blocker reference (Q1)
- RESEARCH_REQUIRED[R2]: answer or blocker reference (Q2)

### Gaps
- Blocking:
  - Q1: missing decision — risk if guessed
- Non-blocking:
  - ...

### User questions
- BLOCKED only:
  - Q1: exact answer needed

### Handoff
- READY: safe to hand off to `modernuo-issue-implement` at the post-publication
  issue revision recorded above. The `blocked` label must not remain on the issue.
- BLOCKED: implementation must not start; answer the listed questions and rerun
  research. The `blocked` label must be present on the issue.
```

For `READY`, complete acceptance and validation rows. For `BLOCKED`, keep
acceptance and validation explicit about what remains unknown and reference the
stable question IDs from the current run.

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
Record the body update and label toggle in `mutation.performed`.

## Advice-only exception

When the user explicitly asks for advice only and forbids GitHub mutation, skip
publication, leave `issue_publication` empty, and set
`mutation.authorized: false`. This is the only read-only completion path.
