---
name: modernuo-symbol-discipline
description: 'Use when deciding whether ModernUO-based C# values should be inline,
  locals, constants, static readonly objects, fields, properties, or explicit Policy*
  surfaces. Report overexposure as a warning; do not rewrite existing symbols unless
  cleanup was requested or the user confirms the change.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Symbol Discipline

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Every symbol must justify its lifetime, scope, visibility, and semantic value.
This is a warning/recommendation lens, not permission for behavior or public API
changes.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Find all consumers, reflection/string references, serialization/config/
   command exposure, tests, docs, and client-visible uses.
2. Classify the value with the decision ladder below.
3. Choose the narrowest scope and stable mechanic name. Preserve source/parity
   evidence without embedding ticket or publish labels in the identifier.
4. Report the candidate and ask before rewriting unless the request explicitly
   asks for symbol cleanup.
5. If changed, run reference search plus focused build/tests and confirm no
   behavior or compatibility surface changed unintentionally.

## Decision Ladder

1. Inline obvious one-use values that do not name policy or a formula term.
2. Use locals for reuse, snapshots, side-effect avoidance, or meaningful steps.
3. Use `const` for reusable compile-time rules with durable consumers/evidence.
4. Use `static readonly` for shared runtime objects or identity.
5. Use fields for persistence, timers, ownership, caches, and changing state.
6. Use properties for engine/public/serialized/config/client contracts, not
   wrappers that merely rename another value.

## Policy Names

`Policy*` means a deliberate configured-project decision where official sources
are incomplete or the project intentionally chooses custom behavior. Era gating
alone is not policy.
Require a mechanic-specific name and at least one durable reason: reuse, focused
tests, parity documentation, or a stable downstream consumer. Keep it private or
internal unless public access is genuinely needed.

## Output Contract

```text
[SYMBOL] WARNING: {unnecessary, vague, or overexposed symbol}
  File: {path}:{line}
  Consumers/contracts: {evidence}
  Suggestion: {inline|local|const|static readonly|field|property|rename}
  Compatibility: {none|serialization|reflection|config|public API}
```

For a clean audit, return this explicit evidence instead of implying that no
output means no issue:

```text
[SYMBOL] CLEAR
  File: {path or audited scope}
  Reason: {scope, lifetime, and contract are justified}
  Compatibility: none
```

For implementation, also return old/new mappings, access-level changes, source
evidence location, and verification.

Emit every warning or clear result as one `Decision.records` entry with `kind: symbol-audit`; put the existing warning/clear fields, mappings, and compatibility conclusion in `details`. The text block is an optional rendering of that record, never a separate result schema.

## Verification

- The symbol is reused, exposed, tested/documented, required by a contract, or
  names a non-obvious decision.
- Scope is no wider than its actual consumers.
- `Policy*` denotes explicit policy rather than era context.
- Reference search/build/tests show no compatibility or behavior change.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-symbol-discipline`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-symbol-discipline` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [symbol decision examples](references/symbol-decision-examples.md) when a
  local, wrapper property, or `Policy*` surface is ambiguous.
- When a symbol embeds source publish numbers or is a test identity, use the
  applicable locally available naming workflow; otherwise inspect references
  and current consumers directly before proposing a rename.
- Load the serialization/configuration/API owner before changing a contract name.
