---
name: modernuo-content-taxonomy
description: Use when classifying a UO feature into World, Entity, ItemSystem, MobileSystem,
  Progression, EconomyCrafting, QuestNarrative, Encounter, or ClientPresentation,
  or when a user explicitly requests a cross-domain parity inventory. Routes concepts
  to ModernUO code/data. Do not use for ordinary implementation or deep single-mechanic
  review.
license: MIT
metadata:
  version: 1.2.0
---

# ModernUO Content Taxonomy

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary and branch

Choose one branch:

- **Classification/scoping:** answer “where does this belong?” or decompose a feature across domains. Do not force a full parity inventory.
- **Parity inventory:** only when the user asks for parity, gaps, implementation status, or a 9-domain inventory. Requires a target era/profile and [parity-check.md](parity-check.md).

Use an available local content-implementation workflow after classification.
Use an available narrow domain workflow for deep mechanic review.

## Nine domains

`World`, `Entity`, `ItemSystem`, `MobileSystem`, `Progression`, `EconomyCrafting`, `QuestNarrative`, `Encounter`, and `ClientPresentation`. Read the matching section of [mappings.md](mappings.md) for concepts and code/data anchors.

These are design vocabulary, not guaranteed C# types; ModernUO commonly uses subclasses, data rows, enums/tables, and virtual profiles.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow: classification

1. State the user outcome and target era/profile if behavior depends on it.
2. Identify the primary domain, then direct dependencies. A placed boss may span Entity, MobileSystem, Encounter, loot, World, and ClientPresentation.
3. Read only the matching sections of [mappings.md](mappings.md), then verify every proposed path/type in the current repository.
4. Separate definition/data, runtime instance, registration/bootstrap, persistence, and presentation surfaces.
5. Return the smallest implementation map; mark absent or unverified anchors explicitly.

## Parity workflow

When the parity branch triggers, read [parity-check.md](parity-check.md) and use
an available official-evidence workflow. Do not claim `Present` or `Gap` without
era-scoped official evidence plus current repository evidence.

## Safety gates

- Distinguish `Gap`, `Partial`, `SourceLocked`, `RuntimeBlocked`, and intentional `Custom` behavior.
- Repository code is implementation evidence, not proof of official UO history.
- Client asset fidelity cannot be inferred from server-side numeric IDs alone.
- Do not create issues or mutate trackers unless the user explicitly asks; issue slicing is a draft/report operation by default.

## Verification/self-check

Verify every proposed path/type in the current repository and every parity status against the stated era/profile and cited source class. Re-scan for implementation already present, unverified claims, and cross-domain dependencies.

## Output contract

For classification, return primary/dependent domains, verified ModernUO types/paths, integration order, era assumptions, and open evidence. For parity, return the full English Markdown contract in [parity-check.md](parity-check.md), with citations and confidence. In either branch, identify checks performed and unresolved paths/source conflicts.

For parity, the YAML result contract is the outer envelope: emit each inventory row as a `Decision.records` entry with `kind: parity-row`, then render the human Markdown inventory from those same records after the YAML block. Put cited source records in `Evidence.records`; do not create a competing top-level parity schema.

## Reference routing

- Read [mappings.md](mappings.md) only for the domains in scope.
- Read [parity-check.md](parity-check.md) only for explicit parity/inventory work.
- When ownership or behavior moves between eras or profiles, require an explicit target profile and inspect its local configuration before continuing.

## Intake and result contract

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT` before acting. Record `Repository revision`, `Requested behavior`, `Evidence available`, and `Validation surface`; return `BLOCKED` when any required field is unavailable.

Emit exactly one fenced `yaml` document with this ordered, machine-readable schema. Keep all values factual; use `null` or an empty list rather than prose placeholders. Every datum promised by this skill's earlier output contract belongs in one or more `Decision.records` entries; use one record per affected surface, matrix row, warning, or finding. Place optional narrative after the YAML document only when it adds human context without changing the record values.

```yaml
Outcome: IMPLEMENTED | REVIEWED | BLOCKED
Repository revision:
  commit: <full revision or null>
  dirty: <true | false | null>
Decision:
  kind: REVIEW | PLAN | IMPLEMENT
  summary: <single factual sentence>
  records:
    - kind: <skill-specific contract item>
      subject: <path, symbol, matrix row, or finding>
      status: <verified | proposed | blocked | not-applicable>
      details: <required skill-specific fields>
      evidence_refs: [<Evidence.records.id>]
Evidence:
  records:
    - id: E1
      class: repository | official | test | runtime | user-supplied
      locator: <revision-bound path, URL, command, or null>
      claim: <fact supported by the record>
Verification:
  checks:
    - command_or_method: <command or inspection>
      result: passed | failed | not-run | blocked
      evidence_refs: [E1]
  runtime_smoke:
    result: passed | failed | not-run | unavailable
    runner_sha256: <summary value or null>
Confidence:
  level: high | medium | low
  basis: <evidence and verification basis>
Limitations:
  items: [<unresolved input, source, or validation limit>]
```

Use `high` confidence only with a current revision plus focused verification, `medium` with current static evidence but an unrun required check, and `low` when blocked or a required source is unavailable.

## Portable evidence

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-content-taxonomy`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-content-taxonomy` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
