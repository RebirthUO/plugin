---
name: modernuo-property-lists
description: Use when reviewing, planning, implementing, or auditing ModernUO-based IPropertyList or Object Property List tooltip emission, localized cliloc arguments, entry ordering, chunked free text, and refresh invalidation. Do not use for ordinary messages, gumps, or non-tooltip item mechanics; route complete item-property behavior to modernuo-item-properties.
---

# ModernUO Property Lists

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own client tooltip emission, localized arguments, relative order, free-text
blocks, and property-list refresh behavior. Do not infer item mechanics from a
tooltip request. Ordinary message and gump interpolation handlers have separate
semantics and remain outside this skill.

## Required Context

Inspect the consuming repository's instructions, pinned revision, current
`IPropertyList` surface, property-list implementation, base entity emission
order, cliloc availability, visible state owner, and focused test helper. Define
the expected entry sequence, cliloc or raw-text form, argument order, era gate,
and refresh trigger. If a required localized identifier, ordering rule, or
visibility lifecycle cannot be verified, return `BLOCKED` with the missing
source or decision; do not guess.

## Workflow

1. Read [property-list formatting and ordering](references/property-list-formatting.md)
   and inspect an adjacent current implementation before selecting an overload.
2. Identify whether the entry belongs in the normal property path, a verified
   name-stage hook, a localized cliloc, a raw property, or a multi-line
   free-text block. Preserve the base call and local relative order.
3. For the specialized property-list interpolated handler, put human text and
   string constants in formatted holes; leave only structural delimiters bare.
   Pass values directly and represent a localized argument with the handler's
   supported localized form. Do not copy these rules to other interpolation
   handlers.
4. Use the current chunking primitive or scoped text-block builder only for
   variable free text. Do not use it for a short localized property.
5. Attach refresh to the state transition that changes visible output. Use the
   current generated serialization invalidation pattern for serialized fields;
   call invalidation once from custom state changes and preserve the local dirty
   or persistence rule where applicable.
6. Add focused tests for entry number, arguments, relative order, era presence
   and absence, and refresh behavior. Read
   [recording test doubles](references/recording-property-list-test-doubles.md)
   only when a test double no longer matches the interface.

## Guardrails

- Verify the actual interface and overloads at the pinned revision; do not copy
  a stale recording double or overload list.
- Prefer a stable cliloc over raw text when the repository has one, but do not
  invent a number or argument order.
- Do not allocate with `.ToString()`, concatenation, `string.Format`, LINQ, or
  prebuilt strings inside a property-list interpolation hole.
- Do not move an entry into a name-stage hook without verifying the base
  sequence requires that position.
- Do not invalidate in a tight loop or claim an unrun packet/hash assertion was
  tested.

## Result Contract

Classify the request as `REVIEW`, `PLAN`, or `IMPLEMENT`. Emit exactly one
fenced `yaml` document with this schema; keep values factual and use `null` or
empty lists rather than prose placeholders.

Use `REVIEWED` for a `REVIEW` or `PLAN` result, `IMPLEMENTED` only after an
authorized change with post-change evidence, and `BLOCKED` when a required
input or authority is unavailable.

```yaml
Outcome: IMPLEMENTED | REVIEWED | BLOCKED
Repository revision:
  commit: <full revision or null>
  dirty: <true | false | null>
Decision:
  kind: REVIEW | PLAN | IMPLEMENT
  summary: <single factual sentence>
  records:
    - kind: entry-sequence | argument-format | text-block | invalidation | test-evidence
      subject: <path, symbol, or property>
      status: verified | proposed | blocked | not-applicable
      details: <required facts and decisions>
      evidence_refs: [<Evidence.records.id>]
Evidence:
  records:
    - id: E1
      class: repository | test | runtime | user-supplied
      locator: <revision-bound path, command, or null>
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

Use high confidence only with a current revision and focused post-change
verification; use low confidence for a blocker or missing required source.

## Reference Routing and Verification

- Load `modernuo-item-properties` for mechanics, storage, persistence, or era
  concerns beyond tooltip emission, and `modernuo-test-workflow` for fixture or
  broad-validation concerns, only when those siblings are available.
- Before completion, run `python scripts/validate-modernuo-skill-evals.py
  plugins/modernuo/skills/modernuo-property-lists` from the plugin root. When
  the Codex CLI runtime is available, also run `python
  scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir>
  plugins/modernuo/skills/modernuo-property-lists` and report its result plus
  `runner_sha256`; otherwise record that limitation.
