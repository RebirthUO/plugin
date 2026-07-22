---
name: rebirthuo-issue-create
description: Draft or create a RebirthUO GitHub intake issue through an optional live template. Resolve the repository only from applicable project AGENTS.md; preserve exact template structure when a TemplatePacket is supplied or project instructions require one, otherwise use the governed fallback issue format. Encode researchable unknowns as owned claim-specific placeholders, and after verified standalone intake ask once whether to start research. In a full rebirthuo-issue-workflow continue automatically. Do not perform mechanics research, readiness review, or implementation.
license: MIT
metadata:
  version: "3.1.2"
---

# RebirthUO Issue Create

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own template-conformant or governed-fallback intake. Record supplied facts and
convert researchable unknowns into precise work items; do not use vague filler
or invent mechanics.

## Repository and authority gate

1. Read every applicable `AGENTS.md` and require one exact `owner/repository` or
   canonical URL. Ask only when those instructions are missing or conflicting.
2. Verify `gh api repos/{owner}/{repository}` before each GitHub mutation and
   pass the exact repository explicitly. Never infer it from cwd, remotes,
   organization, issue number, adjacent projects, documentation, or memory.
3. Drafting is read-only. Creating the issue requires an explicit request.
   Unrelated comments, label changes, relationships, projects, and milestones
   remain unauthorized. Applying the verified selected labels as part of the
   authorized issue creation is allowed.

## Workflow

1. Load [the intake contract](references/authoring-contract.md). Require a
   fresh `TEMPLATE_READY` packet only when the request or applicable project
   instructions require a live template; otherwise select the canonical
   fallback format without calling the template gate.
2. Capture the goal, observed and desired behavior, supplied scope/non-goals,
   reproduction/context, links, and explicit decisions in the live field order.
3. For each researchable unknown, add a stable `RESEARCH_REQUIRED[Rn]` entry
   naming the exact claim, affected field, risk, and next research owner such
   as `uo-official-evidence`, `uo-publish-expansion-mapping`, or a relevant
   RebirthUO/ModernUO code-domain skill.
4. Search open and closed issues for duplicates and build the label selection:
   preserve every configured live-template label, then add only an existing
   repository label whose relevance is directly supported by the issue's
   requested object, scope, or stated classification. Record a source and
   issue-specific rationale for every selected label. A duplicate, missing
   label, or ambiguous relevance returns `INTAKE_BLOCKED` without creation;
   this skill never creates, removes, renames, or bulk-synchronizes labels.
5. Return the complete `IntakePacket`. When creation is authorized, create
   once, read it back, and record number, URL, timestamp, and body digest.
6. In standalone mode, after draft or creation verification ask exactly once
   whether to invoke `rebirthuo-issue-research`. In an explicit
   `rebirthuo-issue-workflow`, set `continuation: RESEARCH` and hand off without
   asking again.

Provider authentication, authorization, rate-limit, transport, malformed
response, or ambiguous mutation failures return `INTAKE_PROVIDER_BLOCKED` with
operation, retryability, preserved evidence, and no blind retry. After an
ambiguous create result, search exact title/body before any authorized retry.

## Output Contract

Return the contract's `IntakePacket`, including status, blockers, calibrated
confidence/residual uncertainty, `mode: standalone | workflow`,
verified format and repository identity, duplicate/label-selection checks,
selected-label rationale and creation read-back, claim-level
research work, mutation read-back, and
`continuation: ASK_RESEARCH | RESEARCH`. This skill never returns `READY`.

## Verification

- Repository identity matches current provider read-back. Template identity
  matches when `format: template`; fallback intake records its fixed format and
  the optional-template reason.
- Template intake preserves every live field; fallback intake preserves every
  canonical fallback field. Required fields are never blank or invented.
- Each unknown is claim-specific, risk-labeled, and assigned to a research owner.
- Standalone intake asks once; full workflow intake continues automatically.
