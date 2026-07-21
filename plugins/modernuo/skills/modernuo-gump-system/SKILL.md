---
name: modernuo-gump-system
description: Use when planning, creating, reviewing, or changing ModernUO gumps from a screenshot, visual description, or existing UI flow, including StaticGump, DynamicGump, builders, placeholders, SendGump/CloseGump, and response handling. Produces a source-marked component inventory and an annotated visual concept for planned UI changes; consults a user-enabled Ultima/UO MCP when available without inventing asset IDs. Covers layout choice, non-empty construction, stale-response authorization, handler-aware strings, and tests. Do not use for migrating legacy RunUO gumps; use modernuo-migrate-gumps.
---

# ModernUO Gump System

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own new/current ModernUO gump architecture, visual composition, and behavior.
Use an available local migration workflow for legacy conversion. Do not claim
client-art fidelity, a gump art ID, cliloc, or official gameplay behavior from a
screenshot alone.

## Required context

Before acting, use the decision-kind matrix in [Intake and result contract](#intake-and-result-contract)
to determine whether a repository revision, source/profile, or validation
surface is required. Its `PLAN` row explicitly overrides this generic
precondition for a description-led plan that makes no repository-specific,
source-specific, or implementation claim. Otherwise inspect the consuming
repository and record its pinned revision, the requested behavior, visual
inputs, and available build/test surface. If a required path, symbol, profile,
source claim, or validation surface cannot be verified, return `BLOCKED` with
the smallest missing input; do not infer it. Treat sibling skills and
repository-local documents as optional: load them only when present, otherwise
inspect the current source directly and state the limitation.

## Workflow

1. Define audience, state owner, fixed versus variable structure,
   singleton/stacking policy, all controls/IDs, authorization, cancellation,
   localization, stale-response behavior, and the visual change to make.
2. If a screenshot or mock-up is supplied, inspect it and create a component
   inventory before selecting APIs. Segment it by z-order and region: window
   frame, decoration, static text, data fields, images, input, controls,
   navigation, and feedback. Give every visible or required element a stable
   `C01`-style ID; record approximate bounds relative to the top-left origin,
   parent/overlap/alignment relationships, intended state, interaction, and
   evidence. Treat inferred hidden behavior as proposed, never observed.
3. Read [gump-patterns.md](references/gump-patterns.md) and the exact local
   base/builder APIs plus a sibling gump. Read
   [screenshot-composition.md](references/screenshot-composition.md) only for
   a screenshot/mock-up request or a `PLAN` that requires a visual concept.
4. Check the active tool catalog for a user-enabled MCP that explicitly offers
   Ultima Online data. If one exists and can answer the question, use its
   documented interface only for candidate art, cliloc, text, or other requested
   element data. Record the query and result as `ultima-mcp` evidence. If it is
   absent, inaccessible, or inconclusive, keep the semantic element role and
   mark its concrete asset as unresolved; do not block a description-led plan
   and do not invent IDs. Keep MCP/client/repository evidence separate from
   official gameplay evidence.
5. For every `PLAN`, produce the required visual concept after the inventory:
   an annotated wireframe that maps component IDs to containment, alignment,
   spacing, z-order, and action targets. Base it on the screenshot when present
   or synthesize it from the requested behavior when absent. Mark proposed
   components and unresolved assets visibly.
6. Choose `StaticGump<T>` for a stable cached layout with placeholders; choose
   `DynamicGump` when structure/control count varies per instance. Map every
   actionable component to a stable nonzero button/switch/text-entry ID before
   code. Reserve `0` for close/cancel.
7. Validate prerequisites before construction in a static `DisplayTo` method.
   Build at least one visual/dismissible element on every constructed path. Use
   placeholders/handler-aware interpolated literals without prebuilding strings.
8. In `OnResponse`, revalidate access, actor, target/object identity, deletion,
   ownership, map/range, and current system state before mutation.
9. Test display rejection, layout path, success, cancel, invalid ID/text/switch,
   stale/deleted/moved state, repeated open/singleton, unauthorized response,
   and the visual/component map against the rendered client when available.

## Safety gates

- Never send an empty gump; it can leak an undismissable client/server slot.
- Do not trust state captured when displayed; responses are delayed, user-controlled input.
- Do not leave `Cached => false` in production.
- Escape/limit user text according to the local HTML/text API and verify clilocs rather than inventing IDs.
- Keep dynamic lists bounded and avoid heavy work during layout serialization.
- Label screenshot observations, user requirements, repository/client/MCP lookup,
  and official evidence separately. A screenshot can establish appearance, not a
  hidden action, asset ID, or gameplay rule.

## Verification/self-check

Test non-empty display, all action/cancel/invalid inputs, stale authorization,
singleton/stacking, and per-instance strings. Compare each implemented
interactive control to its component record and visual concept. Record manual
visual/client validation separately from automated behavior checks.
If a required focused validation fails, is blocked, or is unavailable after a
mutation, stop delivery: do not report `IMPLEMENTED`, preserve the changed
files without rollback, return `BLOCKED` with the exact check result and
limitation, and request focused review or the smallest missing validation
input. Roll back only with explicit user authorization.

## Output contract

Return selected gump type and rationale, component inventory, visual concept,
layout/control/state contract, changed files, authorization and stale-state
checks, focused verification evidence, and remaining manual client/UI checks.

## Reference routing

- Always read [gump-patterns.md](references/gump-patterns.md).
- For HTML/interpolation/localization or UI target flows, use the applicable
  locally available specialist workflow; otherwise inspect the current source.

## Intake and result contract

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT` before acting. Always
record `Requested behavior` and `Evidence available`. Apply the remaining
context requirements by decision kind:

| Decision kind | Required context | Unavailable context disposition |
|---|---|---|
| `PLAN` | Requested behavior and the available visual/user evidence | A description-led plan may use `null` repository revision and `not-run` validation with an explicit limitation. Require a repository revision, source/profile, or validation surface only when the plan makes a repository-specific, source-specific, or implementation claim; otherwise block only for missing requested behavior or evidence. |
| `REVIEW` | Repository revision, requested behavior, relevant evidence, and the applicable validation surface | Return `BLOCKED` with the smallest missing input. |
| `IMPLEMENT` | Repository revision, requested behavior, relevant evidence/source/profile, and focused validation surface | Return `BLOCKED` with the smallest missing input. |

Use this terminal-outcome mapping:

| Decision kind | Permitted `Outcome` | Validation disposition |
|---|---|---|
| `PLAN` | `REVIEWED` or `BLOCKED` | A non-mutating unavailable validation is `REVIEWED` with `not-run`/`unavailable` evidence and a limitation. |
| `REVIEW` | `REVIEWED` or `BLOCKED` | A non-mutating unavailable validation is `REVIEWED` with its limitation unless the requested review requires that check to establish its claim. |
| `IMPLEMENT` | `IMPLEMENTED` or `BLOCKED` | `IMPLEMENTED` requires every required focused check to pass; a failed, blocked, or unavailable check is `BLOCKED`. |

Emit exactly one fenced `yaml` document with this ordered, machine-readable
schema. Immediately after its closing fence, emit exactly one heading named
`## Visual Concept`, then exactly one fenced `text` block; do not place prose
or another fenced block between them.
Keep all values factual; use `null` or an empty list rather than prose
placeholders. Every datum promised by this skill's earlier output contract
belongs in one or more `Decision.records` entries; use one record per affected
surface, matrix row, warning, or finding. The visual block is mandatory for
every result: for `PLAN` and visual `REVIEW` or `IMPLEMENT`, emit the required
wireframe; for nonvisual `REVIEW` or `IMPLEMENT`, or any `BLOCKED` result,
emit only `Not applicable: <factual reason>.` in that block. Do not use
additional fenced blocks.

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
      details:
        type: component | validation | warning | finding | summary
        summary: <single factual sentence>
        fields:
          role: <component role when type is component>
          bounds: <component bounds when type is component>
          command_or_method: <validation command when type is validation>
          result: <validation result when type is validation>
          condition: <warning or finding condition when applicable>
          impact: <warning or finding impact when applicable>
      evidence_refs: [<Evidence.records.id>]
Evidence:
  records:
    - id: E1
      class: repository | official | test | runtime | user-supplied | screenshot | ultima-mcp
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

When a wireframe is required, make the visual block a legible, proportional
text wireframe. Include a viewport, component IDs, a legend for
`observed`/`proposed`/`unresolved`, and arrowed action links for every
interactive component. Preserve approximate relative placement rather than
pretending to provide pixel-perfect rendering. Use a `Decision.records` entry
for each component inventory row, MCP resolution, and composition decision so
the diagram never becomes unsupported prose.

Use `high` confidence only with a current revision plus focused verification, `medium` with current static evidence but an unrun required check, and `low` when blocked or a required source is unavailable.

## Portable evidence

Use `evals/behavior_cases.json` to preserve the missing-context blocker,
component/MCP evidence boundary, visual-plan requirement, named safety branch,
and response fields during review or implementation. For every response, state
`Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository
revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence
or validation limitation. Before completion, run the package trigger-fixture
smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-gump-system`.
When a Codex CLI runtime is available, also forward-test every behavior case
with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-gump-system`
and report the result plus the `runner_sha256` from its summary; otherwise state
that runtime-evaluation limitation explicitly.
