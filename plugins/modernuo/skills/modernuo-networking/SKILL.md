---
name: modernuo-networking
description: 'Use when creating or modifying ModernUO packet encoders, incoming handlers,
  NetState sends, SpanWriter/SpanReader protocol code, or client message fan-out.
  Do not use for ordinary gameplay text alone; route formatting concerns to modernuo-string-handling.

  '
license: MIT
metadata:
  version: 1.2.0
---

# ModernUO Networking and Packets

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own packet layout, registration, validation, send eligibility, and protocol-safe
buffer use. Preserve client compatibility and game-thread ownership. Prefer the
existing `Mobile`, `Item`, and `NetState` message APIs over hand-built packets
when the task is only player-facing text. Domain transaction semantics remain
with the owning gameplay surface; vendor stock, debit, and delivery require a
named available owner or explicit local scope.

## Required context

Before acting, inspect the consuming repository and record its pinned revision, the requested behavior, and the available build/test surface. If a required path, symbol, profile, source claim, or validation surface cannot be verified, return `BLOCKED` with the smallest missing input; do not infer it. Treat sibling skills and repository-local documents as optional: load them only when present, otherwise inspect the current source directly and state the limitation.

## Workflow

1. Find the protocol specification and nearest current packet implementation.
   Record packet/subcommand ID, fixed or variable length, endianness, encoding,
   client/expansion gate, and authorization assumptions.
2. For outgoing packets, expose a `NetState` send helper and a deterministic
   `Create*` encoder. Check `CannotSendPackets()` before building or sending.
3. Use `stackalloc` for small bounded packets and `SpanWriter`/the repository pool
   for variable or larger payloads. Initialize the packet and finalize variable
   lengths exactly once.
4. Register incoming handlers in `Configure()` with the correct length and
   in-game gate. Validate remaining input, entity lookup, state, permissions,
   range/ownership, and value bounds before mutation.
5. Compare encoded bytes and handler behavior with a neighboring packet; add a
   focused round-trip, byte-layout, or handler test when practical.

## Guardrails

- UO packet integers are big-endian unless the protocol explicitly requires a
  `WriteLE`/`Read*LE` variant.
- Never trust client serials, lengths, indexes, strings, or enum values. A
  successful read is not authorization.
- Fixed buffers must match the declared length; variable packets must write the
  actual packet length after the payload.
- Avoid `new byte[]` in repeated sends and avoid pre-building strings when a
  handler-aware message API can format at the call site.
- Do not move game-state mutation to network worker threads. Follow the existing
  incoming dispatch boundary and `modernuo-threading` rules.
- Preserve safe string decoders and control-character filtering where the
  neighboring handler uses them.

## Output Contract

Return the packet contract (ID/sub-ID, direction, length, fields, endianness,
encoding, gates), changed paths, validation decisions, and verification evidence.
For review findings, include the affected byte offset or input field and the
client/security consequence.

## Verification

- Exact byte layout and declared length match the protocol.
- Truncated, oversized, invalid-serial, unauthorized, and disconnected cases fail
  safely where relevant.
- Existing client/era behavior and neighboring packet tests remain green.
- State whether validation used tests, captured bytes, a client smoke check, or
  static reasoning only.

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

Use `evals/behavior_cases.json` to preserve the missing-context blocker, named safety branch, and response fields during review or implementation. For every response, state `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`), the inspected repository revision, calibrated confidence (`high`, `medium`, or `low`), and any evidence or validation limitation. Before completion, run the package trigger-fixture smoke check from the plugin root: `python scripts/validate-modernuo-skill-evals.py plugins/modernuo/skills/modernuo-networking`. When a Codex CLI runtime is available, also forward-test every behavior case with `python scripts/run-modernuo-skill-runtime-smoke.py --output-dir <external-output-dir> plugins/modernuo/skills/modernuo-networking` and report the result plus the `runner_sha256` from its summary; otherwise state that runtime-evaluation limitation explicitly.

## Reference Routing

- Read [packet and message patterns](references/packet-patterns.md) when choosing
  writer/reader methods, allocation strategy, or message fan-out helpers.
- When present, read `dev-docs/networking-packets.md` for the current repository API surface.
- Stop and request a named available owner when vendor packet fields cross into
  stock, authorization, price, quantity, payment, delivery, or stale-session behavior.
- Load `modernuo-string-handling` for interpolated text and
  `modernuo-threading` for dispatch ownership.
