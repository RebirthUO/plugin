---
name: modernuo-issue-workflow
description: Use when the user wants a ModernUO or UO GitHub request taken from template-gated intake or a user-identified existing issue through evidence-backed research, an interview for every blocker, isolated implementation, branch push, and pull request. Resolve the exact repository only from applicable project AGENTS.md instructions; an existing issue skips new issue creation. Do not use for one phase alone, advice-only work, or unclear official gameplay behavior.
metadata:
  hermes:
    tags: [modernuo, ultima-online, github, issues, workflow, pull-requests]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: workflow
    workflow_tier: primary
    related_skills:
      - modernuo-issue-template-gate
      - modernuo-issue-create
      - modernuo-issue-research
      - modernuo-issue-implement
      - uo-official-evidence
---

# ModernUO Issue Workflow

## Boundary

Own the end-to-end issue-to-PR state machine. Delegate the phase work to the
named child skills; never weaken their repository, evidence, readiness, or
publication gates. An explicit full-workflow request authorizes only the scoped
issue creation on the new-request route, isolated worktree, branch push, and
PR. It never authorizes a merge, release, deployment, labels, unrelated
comments, or other mutations outside the scoped research publication performed
by `modernuo-issue-research`.

## Workflow

1. Read every applicable `AGENTS.md`, classify the input, and load
   [the state machine](references/workflow-state-machine.md). A user-identified
   existing issue takes the existing-issue route and must not create another
   issue.
2. For a new request, run `modernuo-issue-create` as Phase 1. Before it drafts
   or creates anything, require `modernuo-issue-template-gate` to return a
   fresh `TemplatePacket`; if it cannot identify one suitable live template,
   ask the user and keep the case pending.
3. Run `modernuo-issue-research` for the created or existing issue. Each
   completed research run must publish its findings to the issue body and an
   append-only research comment. On every `BLOCKED` result, enter interview
   mode: return only its focused questions, record each answer, and repeat the
   affected research. Do not treat a user preference as official UO evidence.
4. Hand off only a current `READY` `ResearchPacket` with complete EA clarity to
   `modernuo-issue-implement`. Require a newly isolated worktree and scoped
   branch; commit, push, create or update the PR, and read back every mutation.
5. If implementation uncovers a behavior-changing unknown, preserve the
   worktree, return to the research interview loop, and do not publish until a
   new current `READY` handoff exists.

## Interview Continuation

Do not end the workflow as complete while a template, repository, official
claim, policy, acceptance criterion, or validation boundary is unresolved.
Return one `WorkflowCheckpoint` containing the exact question packet and
resume from that state after the user answers. A blocking official claim stays
blocked until official OSI/EA/Broadsword evidence resolves it or the scope is
explicitly narrowed so that claim is not required.

## Output Contract

Return a `WorkflowResult` with route, verified repository, issue identity,
template decision when applicable, current research revision/readiness,
interview history, worktree/branch/base, validation, mutation read-backs, PR
URL/SHA/checks, and `state: INTERVIEW_PENDING | DELIVERED`. `DELIVERED`
requires a verified PR and zero blockers.

## Verification

- New-request runs use a fresh matching live issue template; existing-issue
  runs create no issue.
- Every gameplay claim has complete official evidence or remains pending.
- Research is `READY` at the live post-publication issue revision before edits
  begin, and every research run left body and comment evidence on the issue.
- The implementation uses an isolated worktree, scoped branch, fresh tests,
  explicit push remote, and read-back PR evidence.
