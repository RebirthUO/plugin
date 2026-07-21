---
name: modernuo-lootpack-preservation
description: 'Use when editing or migrating ModernUO-based creature loot that contains
  GenerateLoot, AddLoot(LootPack.*), PackGold, PackItem, or loot-policy helpers. Preserve
  source-derived pack behavior unless the request explicitly authorizes an economy
  change. Stop for a named available owner or explicit product scope before a
  new loot-system design.

  '
license: MIT
metadata:
  version: 1.1.0
---

# ModernUO LootPack Preservation

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Treat existing or migration-source `LootPack` calls as economy behavior, not
formatting. This skill guards unrelated creature work from silently changing
gold variance, item rolls, gems, reagents, artifacts, or farming value. It does
not design a new loot system.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Record every scoped loot call, pack name, count, order, special drop, era
   branch, and source tier before editing.
2. Implement unrelated stats, skills, AI, abilities, or serialization while
   leaving that loot surface unchanged.
3. If prose and source code disagree, describe the concrete behavior difference
   and recommend a path. Generic prose such as "gold and magic items" is not a
   replacement recipe.
4. Ask for confirmation before removing or replacing source-derived calls unless
   the request already authorizes that exact economy change.
5. Implement only the confirmed delta and compare the resulting loot block with
   the recorded baseline.

## Guardrails

- Preserve count arguments: `AddLoot(LootPack.Gems, 2)` is not equivalent to the
  one-roll form.
- Replacing several packs with `PackGold(min, max)` changes more than the gold
  range; it can remove item, gem, reagent, and variance behavior.
- Do not introduce a named policy helper as a silent substitute for source code.
- State the relevant era/ruleset before calling a guide-alignment canonical.
- Direct replacement is allowed when explicitly requested, when designing a new
  profile with no source-derived block, or when the user asked to fix proven
  dead, duplicated, uncompilable, or out-of-era loot.

## Confirmation Shape

```text
Recommendation: preserve the source LootPack block. Replacing it with {new form}
would change {gold variance/item rolls/gems/reagents/artifacts}. Should that
economy change be made, or should the source calls remain?
```

## Output Contract

Return the before/after loot calls, source/era used, whether confirmation was
required and obtained, and a plain-language statement of any drop/economy
change. Do not describe an intentional loot replacement as only a refactor.

## Verification

- Expected `AddLoot(LootPack.*[, count])` calls remain unless explicitly replaced.
- No `PackGold` or policy helper silently substitutes for a pack.
- Special drops and era branches remain intact outside the approved scope.
- The diff and focused build/test are reported with their actual scope.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-lootpack-preservation`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-lootpack-preservation` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [economy-change examples](references/economy-change-examples.md) when a
  guide and source-derived pack block imply different drop shapes.
- For brand-new generation, artifact, runic, or distribution design, require an
  explicitly available economy-owner workflow; otherwise return `BLOCKED`
  rather than inventing a replacement design.
- Load `modernuo-era-expansion` when the decision differs by expansion.
- Inspect the current creature, its migration source, and the active loot-pack
  implementation before relying on guide prose.
