---
name: modernuo-configuration
description: Use when adding, reviewing, or changing ModernUO server settings, modernuo.json keys, custom JsonConfig files, configuration defaults, or startup reads. Covers key ownership, persistence, validation, compatibility, evidence limits, and focused tests. Do not use for era behavior unless configuration is the actual control surface.
license: MIT
metadata:
  version: "1.2.0"
---

# ModernUO Configuration

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own durable operator-facing settings and custom configuration files. Do not introduce a setting when a constant is genuinely invariant, and do not use a config key to hide an unresolved era-policy decision.

## Workflow

1. Require an existing or proposed configuration file/key and the requested behavior. If neither target nor proposal, or the local API, startup phase, serialization behavior, or era policy cannot be verified, return `BLOCKED` with the exact missing evidence or decision; do not infer it.
2. Define the owner, key, type, default, valid range, read phase, mutation behavior, compatibility, and operator-facing failure mode.
3. Inspect `ServerConfiguration`, `JsonConfig`, the active configuration files, and nearby keys before choosing an API or path.
4. Use `GetOrUpdateSetting` only when writing a missing default is intended; use `GetSetting` for non-mutating reads. Read startup settings in the locally verified `Configure` phase.
5. Use dot-separated stable keys. For structured collections/objects, use a dedicated `JsonConfig` file rather than stringifying data into `modernuo.json`.
6. Validate ranges and incompatible combinations before applying values. Log the actionable key/path without leaking secrets.
7. Preserve renamed/removed keys through a documented compatibility or migration decision; avoid silently resetting operator choices.
8. Test missing, valid, boundary, malformed, legacy, and read-only-file cases plus restart persistence where writes are supported.

## Safety gates

- Never store secrets or tokens in examples, logs, or committed defaults.
- Do not write configuration from arbitrary entity constructors or hot paths.
- Do not assume all values are native JSON types; inspect current serialization behavior.
- Keep generated/runtime output out of source control unless the repository intentionally tracks it.
- A bad optional setting should fail safely with a clear fallback or startup error, not partially initialize a system.
- A malformed required setting must prevent that subsystem from starting, log the actionable key/path without the value when sensitive, and never silently fall back or partially initialize it.

## Verification/self-check

Exercise missing/valid/boundary/malformed/legacy/read-only cases and restart behavior. Re-read keys, defaults, paths, logs, and migration notes for accidental writes or exposed secrets.

## Output contract

Return these sections in order: `Outcome` (`IMPLEMENTED`, `REVIEWED`, or `BLOCKED`); `Configuration Contract` (keys/files, defaults, ownership, validation, and compatibility); `Evidence and Confidence` (local paths/APIs inspected, confidence, and limits); `Verification`; and `Migration Notes`. For review-only work, do not edit. For `BLOCKED`, name the smallest missing input or decision.

## Reference routing

- Read [configuration-patterns.md](references/configuration-patterns.md) for API selection and structured-config shape.
- When the startup phase is unclear, inspect the current repository's startup registration and a local precedent; report `BLOCKED` rather than guessing.
- When a setting changes player-visible era/profile behavior, use [uo-official-evidence](../uo-official-evidence/SKILL.md) for the official claim and [uo-publish-expansion-mapping](../uo-publish-expansion-mapping/SKILL.md) when a Publish-to-expansion mapping is required.
