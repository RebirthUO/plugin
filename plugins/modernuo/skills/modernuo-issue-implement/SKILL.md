---
name: modernuo-issue-implement
description: Use when the user explicitly asks to implement a ModernUO or UO GitHub issue that has a READY modernuo-issue-research handoff at the current issue revision and a clean, format-preserving rewritten body. Resolve the exact repository only from applicable project AGENTS.md instructions, verify the checkout and push remote, and implement the smallest approved tested change. Do not research unresolved mechanics, choose defaults, merge, or deploy.
version: 3.0.0
author: RebirthUO
metadata:
  hermes:
    tags: [modernuo, github, testing, pull-requests]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: implement
    workflow_tier: primary
    related_skills:
      - modernuo-issue-create
      - modernuo-issue-research
      - modernuo-codebase
      - modernuo-code-audit
      - modernuo-test-workflow
---

# ModernUO Issue Implement

## Boundary

Own Phase 3: implement one issue from a current `ResearchPacket` with
`readiness: READY`. Implementation authorizes scoped local code changes and
proportional verification. Commit, push, PR, comment, label, merge, release, and
deployment remain separate actions unless the requested deliverable includes
them.

## Repository and readiness gate

1. Read applicable `AGENTS.md` instructions and require one exact GitHub
   repository. Missing, ambiguous, or conflicting instructions require a user
   question and stop; never infer from cwd, remotes, organization, or memory.
2. Verify the repository through `gh api`, the checkout identity, intended base,
   and actual push remote. Use explicit repository arguments for all GitHub
   operations.
3. Re-read the issue and confirm the `READY` handoff per
   [implementation contract](references/implementation-workflow.md).
4. If implementation discovers a new behavior-changing gap, preserve the
   current work, return focused questions, and stop. Never continue with a
   suggested default.

## Workflow

1. Pass all gates and read
   [the implementation contract](references/implementation-workflow.md).
2. Inspect target code, callers, registrations, data/config, persistence,
   lifecycle, client surfaces, tests, and current local precedent. Load only the
   narrow domain/engine skills implicated by the approved delta.
3. Isolate conflicting work. Create or reuse a scoped branch/worktree only when
   authorized by the requested deliverable.
4. Implement the smallest acceptance-mapped slice. Official behavior comes from
   the frozen `ResearchPacket`; repository code is implementation evidence, not
   permission to alter that packet or the researched issue scope.
5. Add behavior tests for acceptance and rejection boundaries. Run diff/schema
   checks, the owning build, focused tests after the final edit, and broader
   tests in proportion to risk. Separate baseline/environment failures.
6. Audit the final diff against every acceptance criterion and non-goal. Stage
   only scoped files. Commit, push, and create/update a PR only when authorized;
   revalidate repository/push remote and read back each result.

## Safe failure

Stop before the next mutation on stale research, repository mismatch, scope
conflict, newly discovered unknown, schema drift, focused-test regression, or
ambiguous publish result. Preserve work and report exact continuation state. Do
not convert missing official evidence into an implementation policy.

## Output contract

Return an `ImplementationResult` with repository/issue/research revision,
branch/worktree/base and push remote, changed files, acceptance mapping,
player-visible behavior and non-goals, tests/builds with exact scope, final diff
audit, risks, blockers, mutation record, and verified PR URL/SHA/checks when
created. State every omitted publication action.

## Verification

- Research is `READY` with a clean format-preserving body rewrite, no appended
  research report, no unresolved requirement/blocker text, and no `blocked`
  label.
- Repository, checkout, base, and push remote match project instructions.
- Diff is scoped and maps to acceptance criteria; no unrelated behavior changed.
- Focused checks ran after the final edit and evidence scope is labeled honestly.
- Every external mutation was authorized and read back.
