---
name: rebirthuo-issue-template-gate
description: Select and validate the exact live GitHub Issue Template for a new RebirthUO issue workflow. Use before drafting or creating a RebirthUO issue; accept explicit research placeholders for mechanics fields and ask only for repository identity, a genuinely ambiguous template, the primary requested object, or another value only the user can supply. Do not draft, create, edit, label, research, or implement an issue.
license: MIT
---

# RebirthUO Issue Template Gate

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own zero-mutation selection of one current issue template. Distinguish missing
product intent from mechanics that the research phase can establish. Never ask
the user for a researchable formula, era, publish, code anchor, or test oracle.

## Workflow

1. Read every applicable `AGENTS.md`, require one exact repository, and verify
   it through the provider API. Never infer identity from the checkout, remotes,
   organization, issue number, or memory.
2. Read [the selection contract](references/template-selection-contract.md) and
   snapshot the live issue forms, chooser configuration, labels, and revision.
3. Match the stated problem, primary player-visible object, and outcome to all
   live forms. Treat a structured `RESEARCH_REQUIRED` placeholder as a known
   source for a mechanics field.
4. Select a form only when one candidate is materially best. Return
   `TEMPLATE_BLOCKED` only when repository identity, template choice, primary
   requested object, or another user-owned value remains ambiguous.
5. Return `TemplatePacket: TEMPLATE_READY` to `rebirthuo-issue-create`. Re-read
   the selected form immediately before creation and repeat selection if its
   digest changed.

Provider authentication, authorization, rate-limit, transport, or malformed
response failures return `TEMPLATE_PROVIDER_BLOCKED` with operation, provider
status, retryability, preserved snapshot evidence, and no mutations. Retry only
when explicitly safe; never substitute cached or inferred repository data.

## Output Contract

Return the contract's `TemplatePacket` with verified repository/instruction
source, complete inventory, selected path/ref/digest, title prefix, fields,
labels, research-placeholder fields, rationale, calibrated confidence/residual
uncertainty, questions, provider failure when present, and
`status: TEMPLATE_READY | TEMPLATE_BLOCKED | TEMPLATE_PROVIDER_BLOCKED`.

Questions use stable IDs, state the candidates/evidence already checked, and
request one user-owned decision. Do not ask which era or expansion until issue
context, official chronology, and repository configuration have been inspected
by research and still leave multiple product-valid targets.

## Verification

- The repository came only from applicable project instructions and matched
  provider read-back.
- The selected form is live, unique, and compatible with the request.
- Researchable unknowns became placeholders; only user-owned ambiguity blocked.
- No GitHub or repository mutation occurred.
