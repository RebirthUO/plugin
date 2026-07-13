# Issue Research Publication

Use this contract after analysis completes for a verified issue in the exact
repository declared by the consuming project's applicable `AGENTS.md`. Every
completed research run publishes findings to that issue unless the user
explicitly requested advice-only work with no GitHub mutation.

Scoped publication authorizes only:

- one `## Research contract` body update on the identified issue;
- one append-only research comment for the current run;
- read-back of the updated issue revision and comment URL.

It does not authorize labels, projects, milestones, unrelated comments, issue
creation, commits, pushes, or pull requests.

## Publication boundary

1. Re-read the live issue immediately before writing. If `updated_at` or the
   body digest changed since the research capture, reconcile or stop and ask the
   user before overwriting concurrent edits.
2. Preserve the original intake text. Replace only the `## Research contract`
   section when it already exists; otherwise append it after the intake body.
3. Write in English. Do not include local paths, credentials, or secrets.
4. Apply the body update, post the research comment, then read back the full
   issue and record the post-publication revision in the `ResearchPacket`.

## Body section template

Replace or append exactly one `## Research contract` section:

```markdown
## Research contract

**Readiness:** READY | BLOCKED
**Research run:** ISO-8601 timestamp
**Repository revision:** owner/repository @ commit-or-branch-sha

### Official behavior
- Era/publish scope:
- Expected behavior summary:
- Official sources:
  - https://...

### Current implementation
- Verified paths and status:
- Registration/reachability:

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

### Blocking gaps
- BLOCKED only: concise blocker list with question IDs
```

For `READY`, complete acceptance and validation rows. For `BLOCKED`, keep
acceptance and validation explicit about what remains unknown and reference the
stable question IDs from the current run.

## Research comment template

Post one comment per research run. Use a stable header so later runs are easy to
scan:

```markdown
### ModernUO research run

**When:** ISO-8601 timestamp
**Repository:** owner/repository @ commit-or-branch-sha
**Issue revision before:** ISO-8601 digest-before
**Issue revision after:** ISO-8601 digest-after
**Readiness:** READY | BLOCKED

#### Evidence highlights
- Official:
  - C1: statement — verified | conflicting | unavailable — urls
- Implementation:
  - C2: statement — match | partial | absent | custom | unreachable — paths

#### Expected versus actual
- ...

#### Gaps
- Blocking:
  - Q1: missing decision — risk if guessed
- Non-blocking:
  - ...

#### User questions
- BLOCKED only:
  - Q1: exact answer needed

#### Handoff
- READY: safe to hand off to `modernuo-issue-implement` at the post-publication
  issue revision recorded above.
- BLOCKED: implementation must not start; answer the listed questions and rerun
  research.

See the updated `## Research contract` section in the issue body for the
canonical contract.
```

Comments are append-only. Do not edit or delete prior research comments.

## Provider commands

Pass the verified repository explicitly to every command:

```bash
gh api repos/{owner}/{repository}
gh issue view {number} --repo {owner}/{repository} --json body,updatedAt,url
gh issue edit {number} --repo {owner}/{repository} --body-file research-body.md
gh issue comment {number} --repo {owner}/{repository} --body-file research-comment.md
```

After publication, read back the issue body, `updated_at`, comment URL, and
digest. Record both mutations in `mutation.performed`.

## Advice-only exception

When the user explicitly asks for advice only and forbids GitHub mutation, skip
publication, leave `issue_publication` empty, and set
`mutation.authorized: false`. This is the only read-only completion path.
