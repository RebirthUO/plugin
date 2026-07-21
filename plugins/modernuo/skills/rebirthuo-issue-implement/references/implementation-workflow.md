# Issue Implementation Contract

Use only after the parent skill verifies project instructions, repository,
checkout, push remote, live issue revision, and a matching `ResearchPacket` with
`execution_state: COMPLETE` plus `implementation_readiness: READY`.

## Pre-edit sufficiency

The research handoff must contain exact identity, official behavior, current
implementation, expected-versus-actual delta, scope/non-goals, product impact,
safety boundaries, acceptance criteria, validation plan, and a completed
format-preserving issue-body rewrite with post-publication revision fields. The
live issue must have no appended research report, unresolved
`RESEARCH_REQUIRED` or blocker text, or `blocked` label. `BLOCKED`, a stale
revision, or a missing behavior-changing row returns `NOT_READY` before edits.
It is never an implementation default.

## Inspection

- Inspect every edit point, API signature, caller/override, registration,
  configuration/data file, serializer, lifecycle boundary, client surface, test
  fixture, and nearest current precedent implicated by the approved delta.
- A matching existing branch or PR is an update/verification task, not
  permission to recreate, rebase, or overwrite it.
- Preserve unrelated tracked and untracked work. Use an isolated worktree when
  concurrent work or branch switching could affect the user's checkout.

For cliloc work, use `client-cliloc-and-schema-verification.md` as the canonical
production-path check. Load `cliloc-verification.md` only when production
localization APIs cannot be invoked and a temporary decompression diagnostic is
needed; label that result diagnostic rather than production-path verification.
For temporary weapon-bound combat effects, load
`temporary-weapon-effects.md`. For UOContent fixture bootstrapping, generated
persistence, or known test-environment pitfalls, load
`modernuo-content-test-and-persistence-pitfalls.md`.

## Implementation discipline

- Map each changed file and behavior to one acceptance criterion.
- Do not add adjacent loot, balance, era, engine, persistence, or distribution
  changes that are not in the ready contract.
- Keep temporary effects transient and cleanup idempotent.
- Generated serialization changes require the repository generator, exact
  schema output, compatibility tests, and rollback notes.
- After meaningful edits, inspect status and diff before validation.

## Test discipline

- Test observable success, rejection, boundaries, era gates, and
  lifecycle/persistence where applicable; registration-only tests are not
  behavior proof.
- Use deterministic time and RNG seams. Do not weaken production rules or alter
  production data solely to make a fixture boot.
- Build before no-build tests when fixtures consume build output.
- Use the repository's sequential/global-state conventions for expansion,
  timers, registries, client data, and real entities.
- Report exact project, filter, passed/failed/skipped denominator, and whether
  evidence is focused, owning-project, broad, manual, or environment-blocked.

## Validation order

```text
diff check
schema or generated-data check when applicable
owning build
focused behavior tests
owning test project
broader tests in proportion to risk
final diff and status audit
```

Focused tests run again after the final code or test edit. Baseline and
environment failures remain separate from regressions.

## Newly discovered research

Freeze edits, preserve the worktree, and route the unknown to
`rebirthuo-issue-research` before asking the user:

```yaml
implementation_checkpoint:
  repository: owner/repository
  issue_revision: exact revision
  branch_or_worktree: exact location
  completed: []
  validation: []
  state: RESEARCH
  new_claims: []
  preserved_diff: []
  next_skill: rebirthuo-issue-research
```

Research first. Ask only if research exhausts discoverable evidence and finds a
genuine policy choice. Resume only after issue publication and a new matching
`COMPLETE`/`READY` handoff.

## Publication

Only when explicitly authorized and after fresh repository/push-remote checks:

1. stage only scoped paths;
2. commit with a repository-conformant message;
3. push the current branch to the verified remote;
4. create or update a PR with problem, official evidence, observable behavior,
   non-goals, validation, risks/rollback, and issue linkage;
5. read back remote SHA, PR URL, head/base, body, state, and checks.

An ambiguous result requires read-back before retry. Never merge, release, or
deploy by implication.

## ImplementationResult

Every state uses this canonical envelope. `NOT_READY` requires `gate.failures`;
`RESEARCH` requires `research_loop`; `IMPLEMENTED` requires changed files,
acceptance mapping, final audit, and validation; `DELIVERED` additionally
requires proven publication and PR read-back. Unknown or inapplicable values are
`null`, never omitted.

```yaml
repository: { full_name: owner/repository, revision: base SHA }
issue: { number: 123, updated_at: ISO-8601, body_digest: digest }
research: { execution_state: COMPLETE, implementation_readiness: READY, revision: exact revision }
gate: { passed: true, failures: [] }
worktree: { path: path, branch: branch, base: SHA, push_remote: URL }
changed_files: []
acceptance_mapping: []
behavior: { changed: [], unchanged: [] }
validation: [{ command: string, scope: focused | owning | broad | manual, result: passed | failed | blocked, passed: 0, failed: 0, skipped: 0, after_final_edit: true }]
final_audit: { scoped: true, non_goals_preserved: true, status_clean_except: [] }
research_loop: []
risks: []
blockers: []
mutation: { authorized: [], performed: [], failed: [] }
pull_request: { url: null, remote_sha: null, head: null, base: null, state: null, body_digest: null, checks: [] }
confidence: { level: high | medium | low, limitations: [] }
state: NOT_READY | RESEARCH | IMPLEMENTED | DELIVERED
```
