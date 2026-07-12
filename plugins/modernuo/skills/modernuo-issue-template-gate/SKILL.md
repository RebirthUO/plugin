---
name: modernuo-issue-template-gate
description: Use when a ModernUO or UO issue workflow must select and validate the exact live GitHub Issue_Template before drafting or creating an issue. Resolve the exact repository only from applicable project AGENTS.md instructions, return a fresh TemplatePacket, and ask the user if no single template fits. Do not draft, create, edit, label, research, or implement an issue.
metadata:
  hermes:
    tags: [modernuo, ultima-online, github, issues, templates, gate]
    skill_group: modernuo
    skill_subgroup: agentic
    workflow_phase: gate
    workflow_tier: primary
    related_skills:
      - modernuo-issue-create
      - modernuo-issue-workflow
---

# ModernUO Issue Template Gate

## Boundary

Own zero-mutation selection of one current issue template. This gate prevents
an intake workflow from inventing a form, choosing between plausible forms, or
silently proceeding without the repository's live template.

## Workflow

1. Read every applicable `AGENTS.md`, require one exact repository, and verify
   it through the provider API. Never infer identity from the checkout, remotes,
   organization, issue number, or memory.
2. Read [the template selection contract](references/template-selection-contract.md).
   Snapshot the verified repository's current issue forms, configuration, and
   revision before examining the request.
3. Match the user's stated problem, primary player-visible object, and desired
   outcome to the live form fields. Select a template only when exactly one
   candidate fits and its required fields can be completed without invention.
4. Return `TemplatePacket: TEMPLATE_READY` to `modernuo-issue-create`. Re-read
   the form immediately before creation; a changed snapshot repeats this gate.

## Interview Mode

If no current form exists, no form fits, multiple forms fit, or a required field
is unclear, return `TemplateQuestions` and stop. Ask the user to identify the
intended live form or supply the missing request context. Do not synthesize a
generic body, select a likely form, or modify the templates.

## Output Contract

Return `TemplatePacket` with verified repository/instruction source, issue
template inventory, selected path/ref/digest, title prefix, fields/required
state, labels, selection rationale, unanswered questions, and
`status: TEMPLATE_READY | TEMPLATE_BLOCKED`.

## Verification

- Repository identity came only from applicable project instructions and was
  read back from the provider.
- The selected form is current, unique, and compatible with the request.
- Every required field has a known source; unknowns stay in the question packet.
- This gate made no GitHub or repository mutation.
