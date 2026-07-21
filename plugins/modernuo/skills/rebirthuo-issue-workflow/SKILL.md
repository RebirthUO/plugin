---
name: rebirthuo-issue-workflow
description: Autonomously take a new RebirthUO request or identified GitHub issue through live-template intake, exhaustive official research, format-preserving issue publication, isolated implementation, branch push, and pull request verification. Existing issues skip creation; full-workflow requests continue between phases without repeated confirmation. Ask only for repository identity, genuine template ambiguity, or a product/custom-policy decision that remains after research exhaustion. Do not merge, release, deploy, or guess missing official behavior.
license: MIT
---

# RebirthUO Issue Workflow

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own the issue-to-PR state machine and continue autonomous in-scope phases for an
explicit full-workflow request. Child skills retain their repository, source,
readiness, mutation, and verification gates.

## Workflow

1. Read applicable `AGENTS.md`, verify the exact repository, classify the route,
   and load [the state machine](references/workflow-state-machine.md).
2. `NEW_REQUEST`: run `rebirthuo-issue-template-gate`, then
   `rebirthuo-issue-create` in workflow mode and continue directly to research.
   `EXISTING_ISSUE`: skip template/create and start at research.
3. Run `rebirthuo-issue-research` autonomously through its exhaustion and
   publication gates. On `implementation_readiness: BLOCKED`, return only its focused last-mile decision
   packet; after the answer, resume the affected claims without repeating
   resolved questions.
4. Hand off only `execution_state: COMPLETE` with current post-publication
   `implementation_readiness: READY` to
   `rebirthuo-issue-implement` in a fresh isolated worktree and scoped branch.
5. When implementation finds a new unknown, preserve its checkpoint, route it
   through research, publish the refreshed issue, and resume implementation
   automatically after a new `COMPLETE`/`READY` packet.
6. Validate, commit, push, create/update the PR, and verify remote SHA, head,
   base, URL, body, state, and checks. Do not merge, release, or deploy.

## Continuation Rules

Do not ask whether to continue between template, create, research,
implementation, push, and PR when the user requested the full workflow. Pause
only for missing repository authority, genuine live-template ambiguity, a
post-exhaustion product/custom-policy choice, external access, or an unsafe
concurrent-state conflict. Resume from the stored checkpoint after resolution.

## Output Contract

Return `WorkflowResult` with route, repository, issue/template identity,
research attempts/readiness/revision, interview and research-loop history,
worktree/branch/base, validation, mutation read-backs, PR URL/SHA/checks, and
`state: REPOSITORY_BLOCKED | TEMPLATE_BLOCKED | INTAKE_BLOCKED |
INTERVIEW_PENDING | RESEARCH_BLOCKED | IMPLEMENTATION_BLOCKED |
DELIVERY_BLOCKED | DELIVERED`. `DELIVERED` requires a
verified PR and zero blockers.

Use the canonical envelope in the state-machine reference. Include structured
confidence/evidence limitations and a resumable delivery checkpoint for every
partial external mutation; never omit state-required fields.

## Verification

- New requests use one current matching template; existing issues create none.
- Research exhausted discoverable evidence before any user question.
- Implementation started only from the matching live `COMPLETE`/`READY` revision.
- Full workflow did not repeat phase-continuation questions.
- Delivery used an isolated worktree, scoped diff, explicit remote, and PR read-back.
