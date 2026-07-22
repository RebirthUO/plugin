---
name: rebirthuo-issue-template-gate
description: Select and validate the exact live GitHub Issue Template only when a new RebirthUO issue request or applicable project instructions require template-conformant intake. Accept explicit research placeholders for mechanics fields and ask only for repository identity, a genuinely ambiguous required template, the primary requested object, or another value only the user can supply. Do not draft, create, edit, label, research, or implement an issue.
license: MIT
metadata:
  version: "2.1.1"
---

# RebirthUO Issue Template Gate

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own zero-mutation selection of one current issue template when template use is
required. Distinguish missing product intent from mechanics that the research
phase can establish. Never ask the user for a researchable formula, era,
publish, code anchor, or test oracle.

## Workflow

1. Confirm that the request or applicable `AGENTS.md` requires a live template.
   If neither does, return `TEMPLATE_NOT_REQUIRED` with no provider access and
   hand off to `rebirthuo-issue-create` fallback intake.
2. Read every applicable `AGENTS.md`, require one exact repository, and verify
   it through the provider API. Never infer identity from the checkout, remotes,
   organization, issue number, or memory.
3. Read [the selection contract](references/template-selection-contract.md) and
   snapshot the live issue forms, chooser configuration, labels, and revision.
4. Match the stated problem, primary player-visible object, and outcome to all
   live forms. Treat a structured `RESEARCH_REQUIRED` placeholder as a known
   source for a mechanics field.
5. Select a form only when one candidate is materially best. Return
   `TEMPLATE_BLOCKED` only when repository identity, template choice, primary
   requested object, or another user-owned value remains ambiguous.
6. Return `TemplatePacket: TEMPLATE_READY` to `rebirthuo-issue-create`. Re-read
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
`status: TEMPLATE_NOT_REQUIRED | TEMPLATE_READY | TEMPLATE_BLOCKED |
TEMPLATE_PROVIDER_BLOCKED`.

Questions use stable IDs, state the candidates/evidence already checked, and
request one user-owned decision. Do not ask which era or expansion until issue
context, official chronology, and repository configuration have been inspected
by research and still leave multiple product-valid targets.

## Verification

- The repository came only from applicable project instructions and matched
  provider read-back.
- The selected form is live, unique, and compatible when template intake is
  required; otherwise no provider data was read.
- Researchable unknowns became placeholders; only user-owned ambiguity blocked.
- No GitHub or repository mutation occurred.
