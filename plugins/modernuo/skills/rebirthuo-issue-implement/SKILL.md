---
name: rebirthuo-issue-implement
description: Implement one RebirthUO GitHub issue only from a live revision-matching rebirthuo-issue-research handoff with execution_state COMPLETE and implementation_readiness READY whose issue has no unresolved marker or blocked label. Verify repository, checkout, base, and push remote; implement and test the smallest approved delta. Route new unknowns back through research. Do not implement blocked issues, choose defaults, merge, release, or deploy.
license: MIT
metadata:
  version: "4.0.1"
---

# RebirthUO Issue Implement

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own implementation of one researched issue. A researched-but-`BLOCKED` issue is
not eligible for edits. In standalone mode, code changes and local validation
are authorized by an explicit implementation request; commit, push, and PR
creation require the same request to explicitly ask for delivery or publication.
The parent full workflow supplies that scoped delivery authorization. Otherwise
return `IMPLEMENTED` without publishing.

## Readiness gate

1. Resolve and verify the exact repository only from applicable `AGENTS.md`.
   Verify checkout, intended base, and push remote explicitly.
2. Re-read the issue and require a matching post-publication `ResearchPacket`
   with `execution_state: COMPLETE`, `implementation_readiness: READY`, complete
   rows, no unresolved marker or blocker text,
   and no `blocked` label. Any mismatch returns `NOT_READY` without code edits.
3. Load [the implementation contract](references/implementation-workflow.md).

## Workflow

1. Inspect all implicated callers, registrations, data/configuration,
   persistence, lifecycle, client surfaces, tests, and current precedents. Load
   only the relevant RebirthUO/ModernUO implementation and test skills.
2. Use a fresh isolated worktree and scoped branch for issue-to-PR delivery,
   preserving the user's checkout and unrelated changes.
3. Implement the smallest acceptance-mapped delta from the frozen research
   contract and add observable success, rejection, boundary, era, and lifecycle
   tests as applicable.
4. If a behavior-changing unknown appears, freeze and preserve the worktree,
   emit the contract's research handoff, and invoke
   `rebirthuo-issue-research`. Resume only from refreshed `COMPLETE` plus `READY`
   packet; ask the user only if research reaches a genuine policy choice.
5. Run final diff/schema checks, owning build, focused tests after the final
   edit, proportional broader tests, and a scope/non-goal audit.
6. When delivery is authorized, stage only scoped files, commit, push to the
   verified remote, create or update the PR, and read back head/base, URL, body,
   remote SHA, state, and checks.

## Output Contract

Return `ImplementationResult` with gate status, repository/issue/research
revision, worktree/branch/base/remote, changed files, acceptance mapping,
validation scope, final audit, risks, research loop history, mutations, and PR
read-back. Use `state: NOT_READY | RESEARCH | IMPLEMENTED | DELIVERED`.

## Verification

- No code edit occurred before a live matching `COMPLETE`/`READY` gate passed.
- The diff maps to acceptance criteria and preserves every non-goal.
- Focused checks ran after the final edit; baseline failures are separate.
- Every external mutation was authorized, explicit, and read back.
