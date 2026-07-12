---
name: modernuo-issue-create
description: Use when the user explicitly asks to draft or create a ModernUO or UO GitHub issue from the target repository's live issue template. Resolve the exact repository only from applicable project AGENTS.md instructions, fail closed when it is missing or ambiguous, and stop after producing the intake handoff. Do not perform deep research, readiness review, or implementation.
version: 2.0.0
author: RebirthUO
metadata:
  hermes:
    tags: [modernuo, github, issues, intake, templates]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: create
    workflow_tier: primary
    related_skills:
      - modernuo-issue-research
      - modernuo-issue-implement
      - uo-official-evidence
---

# ModernUO Issue Create

## Boundary

Create an English, template-conformant intake issue or draft. This phase records
the request and visible unknowns; it does not turn unknown mechanics into facts
or claim implementation readiness.

## Repository and authority gate

1. Read every applicable `AGENTS.md` before GitHub access. Require one exact
   `owner/repository` or canonical GitHub URL for this task.
2. If instructions omit the repository, name more than one without selecting
   one, or conflict, ask the user and stop. Never choose from the cwd, remotes,
   organization, issue number, neighboring project, stale docs, or memory.
3. Resolve `gh api repos/{owner}/{repository}` and require exact returned
   `.full_name` and `.html_url`. Revalidate before each mutation and pass the
   exact repository explicitly to every GitHub command.
4. Drafting is read-only. Creating an issue requires an explicit current
   request. Labels, comments, edits, relationships, projects, and milestones
   require separate authority.

## Workflow

1. Pass the repository gate and read the verified repository's current
   `.github/ISSUE_TEMPLATE/*.yml`, repository instructions, and label set.
2. Read [the intake contract](references/authoring-contract.md). Select one live
   form from the player-visible primary object and preserve its title prefix,
   field labels/order, options, required state, and configured labels.
3. Capture the user's supplied goal, observed problem, desired outcome, and
   explicit non-goals. Do not perform deep mechanics research in this phase.
4. Fill unavailable research fields with an explicit `RESEARCH_REQUIRED` item
   containing the missing claim and why it matters. Never write a likely
   interpretation, emulator default, or repository behavior as official UO.
5. Search open and closed issues for duplicates and verify every requested
   label exists. A duplicate or missing label blocks creation unless the user
   authorizes the appropriate next action.
6. Return the complete `IntakePacket`. If creation is authorized, create once,
   read back the issue, and add its number, URL, updated timestamp, and body
   digest to the packet.

## Safe failure

Do not publish a vague or off-template issue, fabricate a required value, create
a label implicitly, or retry an ambiguous creation. Return the draft and exact
blocker without mutation. All issue text and handoff fields are English even
when the conversation is not.

## Output contract

Return an `IntakePacket` with:

- verified repository identity and instruction source;
- template path/ref, title, labels, and complete English body;
- duplicate and label checks;
- `research_required` entries with stable IDs;
- mutation authority and actions performed;
- issue number, URL, revision timestamp, and body digest after creation.

The next phase is `modernuo-issue-research`. This skill never returns `READY`.

## Verification

- Repository identity came only from applicable `AGENTS.md` instructions and
  matched the API response.
- The body matches the live form and contains no blank, fabricated, local-path,
  or secret values.
- Every unknown that can affect behavior is `RESEARCH_REQUIRED`.
- Duplicate/label checks and any creation were read back from the exact repo.
