---
name: modernuo-issue-research
description: Use when researching, reviewing, or making an existing ModernUO or UO issue implementation-ready. Resolve the repository only from applicable project AGENTS.md, establish official behavior, compare its code, and rewrite existing issue fields without changing their format. Remove obsolete text and resolved requirements or blockers. Ask about behavior-changing gaps; never append a research report, implement, or choose defaults.
version: 3.0.0
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

Own Phase 2: produce an evidence-backed, implementation-ready current issue.
Unless work is advice-only, rewrite its body in the existing format, replacing
obsolete content and removing resolved requirements/blockers. Scoped
publication includes the `blocked` label; unrelated labels are unauthorized.

## Repository gate

Read applicable `AGENTS.md` and require one exact GitHub repository. If missing,
ambiguous, or conflicting, ask and stop. Never infer it from cwd, remotes,
issue numbers, organizations, neighboring projects, or memory. Verify through
`gh api` before each GitHub operation and pass it explicitly.

## Workflow

1. Read [the research contract](references/research-contract.md),
   [issue publication](references/issue-publication.md), and
   [uo-official-evidence](../uo-official-evidence/SKILL.md).
2. Capture the live issue, comments, labels, linked work, timestamp, and body
   digest; reconcile any `IntakePacket`.
3. Convert every `RESEARCH_REQUIRED` marker and factual claim into an internal
   evidence ledger. Establish expected official behavior from
   OSI/EA/Broadsword sources before inspecting emulator or target-repository
   behavior.
4. Inspect target code, data, configuration, reachability, tests, and merged
   work as implementation evidence, never official-mechanics evidence.
5. Trace era/ruleset, formulas/order, scope/non-goals, PvP/PvM, economy,
   housing/storage, exploit/security, client presentation, persistence,
   lifecycle, performance, rollback, acceptance criteria, and test boundaries.
6. If a gap can change behavior, architecture, era, distribution, player
   impact, persistence, or validation, emit focused `UserQuestions`, mark
   `BLOCKED`, and neither suggest a default nor call the issue ready.
7. After answers, re-read the issue revision and repeat the affected evidence
   and repository checks. Replace obsolete issue text with the verified answer,
   remove its resolved requirement and blocker text, and return `READY` only
   when no blocking gap remains.
8. Rewrite and clean the body per
   [issue publication](references/issue-publication.md), then read back the
   post-publication revision and labels.
9. Mutate unrelated labels only when explicitly authorized.

## User-question gate

Each blocking question has a stable ID, missing decision, evidence checked,
supported options, guessing risk, and answer needed. For `BLOCKED`, return the
packet and retain only current unresolved text in its existing field. Do not
implement.

## Output contract

Return a `ResearchPacket` per [the research contract](references/research-contract.md)
with `issue_publication`, mutation record, and `readiness: READY | BLOCKED`.
Only `READY` at the post-publication issue revision may hand off to
`modernuo-issue-implement`.

## Verification

- Official claims are backed by official evidence or remain blockers.
- `READY` has complete behavior, scope, safety, acceptance, and validation rows.
- Every completed research run left one clean, current, format-preserving issue
  body and the correct `blocked` label state.
- No appended research section, resolved marker, answered question, obsolete
  blocker, or superseded claim remains in the issue body.
- Advice-only requests changed nothing on GitHub.
