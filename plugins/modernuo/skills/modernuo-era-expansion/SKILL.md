---
name: modernuo-era-expansion
description: Use when implementing or reviewing era-conditional ModernUO behavior,
  Core.AOS/SE/ML/etc. checks, Expansion values, or an unspecified target era that
  changes mechanics. Establishes cumulative versus exact gates and test coverage.
  For cross-profile ownership changes, require an explicit target profile before continuing.
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO Era and Expansion Behavior

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own a concrete era-conditioned implementation or review. For behavior ownership changes between eras or profiles, require an explicit target profile before continuing; use taxonomy/parity workflows only for broad inventories.

## Era gate

If the target era/profile materially changes behavior and is neither stated nor discoverable from configuration, ask before editing or claiming parity. Do not default silently to AoS, latest-era, or shard policy.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Read [expansion-map.md](references/expansion-map.md), then inspect `ExpansionInfo`, `Core.Expansion`, active expansion/profile configuration, and the nearest local mechanic.
2. State the target era/profile and whether the requirement is:
   - cumulative (`Core.AOS`: AoS and later);
   - exact (`Core.Expansion == Expansion.AOS`);
   - profile/config-specific;
   - intentionally custom/Enhanced.
3. Gather source evidence for values and introduction/changes; distinguish current official behavior, historical publish behavior, repo precedent, and shard policy.
4. Place the branch at the narrowest stable behavior boundary. Preserve earlier and later behavior explicitly and avoid scattering equivalent checks.
5. Test at least the immediately earlier era, target era, and a later era for cumulative gates; test exact/profile behavior separately.
6. Audit side effects on combat, stats, loot/economy, skills, housing, persistence, client presentation, and registration/data loading as applicable.

## Safety gates

- Later expansions satisfy cumulative convenience properties; this may intentionally or accidentally inherit behavior.
- Era-specific APIs/data must not be invoked before their gate.
- Stored fields can still leak behavior through runtime aggregation or tooltips even if one special hook is gated.
- Do not encode publish numbers in symbol names; keep evidence in comments/docs/tests.
- Update matching profile/data/docs only when the requested behavior requires it.

## Verification/self-check

Run the earlier-target-later/profile matrix and inspect both display and runtime behavior where stored values exist. Recheck cumulative versus exact semantics against current `Core` implementation.

## Output contract

Return the target era/profile, evidence class, cumulative/exact decision, changed gates/paths, earlier-target-later behavior matrix, tests/results, and unresolved parity or policy decisions.

## Reference routing

- Always read [expansion-map.md](references/expansion-map.md).
- When ownership or profile activation changes, require an explicit target profile and inspect its local configuration before continuing.
- For an explicit cross-domain parity inventory, use an available local taxonomy
  workflow; otherwise inspect the current source and state the limitation.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-era-expansion`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-era-expansion` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.
