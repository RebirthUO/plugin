---
name: modernuo-issue-research
description: Use when the user asks to deeply research, review, or make an existing ModernUO or UO issue implementation-ready. Resolve the exact repository only from applicable project AGENTS.md instructions, establish official OSI/EA behavior, compare the verified repository, publish findings back to the issue, and stop to ask focused questions whenever evidence or policy cannot resolve a behavior-changing gap. Do not implement or silently choose defaults.
version: 2.2.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    tags: [modernuo, ultima-online, github, research, readiness]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: research
    workflow_tier: primary
    related_skills:
      - modernuo-issue-create
      - modernuo-issue-implement
      - uo-official-evidence
      - uo-living-world-review
---

# ModernUO Issue Research

## Boundary

Own Phase 2: turn an intake or existing issue into an evidence-backed,
implementation-ready contract. Research publishes to the issue body unless the
user requests advice-only work. Scoped publication includes the `blocked` label
toggle; unrelated labels require separate authorization.

## Repository gate

Read every applicable `AGENTS.md` and require one exact GitHub repository for
the task. If it is missing, ambiguous, or conflicting, ask the user and stop.
Never infer it from cwd, remotes, issue numbers, organizations, neighboring
projects, or memory. Verify the exact identity through `gh api` before every
GitHub read or write and pass the repository explicitly to each command.

## Workflow

1. Read [the research contract](references/research-contract.md),
   [issue publication](references/issue-publication.md), and
   [uo-official-evidence](../uo-official-evidence/SKILL.md).
2. Capture the complete live issue, comments, labels, linked work, updated
   timestamp, and body digest. Reconcile it with any supplied `IntakePacket`.
3. Convert every `RESEARCH_REQUIRED` marker and factual claim into an evidence
   ledger. Establish expected official behavior from OSI/EA/Broadsword sources
   before inspecting emulator or target-repository behavior.
4. Inspect the verified target branch for current code, data, configuration,
   registration/reachability, tests, and merged work. Label this as
   implementation evidence, never official mechanics evidence.
5. Trace era/ruleset, formulas/order, scope/non-goals, PvP/PvM, economy,
   housing/storage, exploit/security, client presentation, persistence,
   lifecycle, performance, rollback, acceptance criteria, and test boundaries.
6. If any missing or conflicting item can change behavior, architecture, era,
   distribution, player impact, persistence, or validation, emit focused
   `UserQuestions` and mark the run `BLOCKED`. Do not recommend or apply a
   default for a blocking item and do not call the issue ready.
7. After answers, re-read the issue revision and repeat the affected evidence
   and repository checks. Return `READY` only when no blocking gap remains.
8. Publish per [issue publication](references/issue-publication.md), then read
   back the post-publication revision and labels.
9. Mutate unrelated labels only when explicitly authorized.

## User-question gate

Each blocking question contains a stable ID, missing decision, evidence already
checked, concrete options only when evidence supports them, risk of guessing,
and the exact answer needed. For `BLOCKED`, return the packet in chat and
publish the blockers to the issue. No implementation follows a blocked run.

## Output contract

Return a `ResearchPacket` per [the research contract](references/research-contract.md)
with `issue_publication`, mutation record, and `readiness: READY | BLOCKED`.
Only `READY` at the post-publication issue revision may hand off to
`modernuo-issue-implement`.

## Verification

- Official claims are backed by official evidence or remain blockers.
- `READY` has complete behavior, scope, safety, acceptance, and validation rows.
- Every completed research run left body evidence and the correct `blocked`
  label state.
- Advice-only requests changed nothing on GitHub.
